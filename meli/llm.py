# -*- coding: utf-8 -*-
"""
MercaFlow — Provider-agnostic LLM layer.

Supports three provider modes:
    vertex  — Google Vertex AI (ADC auth, default)
    gemini  — Google Gemini Developer API (API key)
    openai  — Any OpenAI-compatible endpoint (MiniMax, DeepSeek, OpenAI, etc.)

Configure via env vars:
    LLM_PROVIDER      "vertex" | "gemini" | "openai"  (default: vertex)
    LLM_MODEL          model name                      (default: gemini-3-flash-preview)
    VERTEX_PROJECT     GCP project ID                  (vertex only)
    VERTEX_LOCATION    GCP location                    (vertex only, default: global)
    GEMINI_API_KEY     API key                         (gemini only)
    OPENAI_API_KEY     API key                         (openai only)
    OPENAI_BASE_URL    base URL                        (openai only)
"""
import os
import base64
from pathlib import Path


def _detect_mime(data: bytes, path: str = "") -> str:
    """Detect image MIME type from magic bytes, fallback to extension."""
    if data[:8] == b'\x89PNG\r\n\x1a\n':
        return 'image/png'
    if data[:2] == b'\xff\xd8':
        return 'image/jpeg'
    if data[:4] == b'RIFF' and data[8:12] == b'WEBP':
        return 'image/webp'
    if data[:6] in (b'GIF87a', b'GIF89a'):
        return 'image/gif'
    ext = Path(path).suffix.lower()
    return {
        '.png': 'image/png', '.jpg': 'image/jpeg', '.jpeg': 'image/jpeg',
        '.webp': 'image/webp', '.gif': 'image/gif',
    }.get(ext, 'image/jpeg')


def call_vision(image_paths, prompt, max_tokens=4000, system=None, json_output=False):
    """
    Send images + text prompt to the configured LLM provider.

    Args:
        image_paths: list of image file paths
        prompt: text prompt (string)
        max_tokens: max response tokens
        system: optional system instruction
        json_output: if True, request JSON-only output (Google providers only)

    Returns:
        The model's text response (string).
    """
    provider = os.environ.get('LLM_PROVIDER', 'vertex').lower()

    if provider in ('vertex', 'gemini'):
        return _call_google(image_paths, prompt, max_tokens, system, json_output,
                            vertex=(provider == 'vertex'))
    else:
        return _call_openai(image_paths, prompt, max_tokens, system)


# ---------- Google (Vertex AI / Gemini API) ----------

def _call_google(image_paths, prompt, max_tokens, system, json_output, vertex):
    from google import genai
    from google.genai import types

    model = os.environ.get('LLM_MODEL', 'gemini-3-flash-preview')

    if vertex:
        project = os.environ.get('VERTEX_PROJECT', 'project-a1331a0f-a61c-4d85-adb')
        location = os.environ.get('VERTEX_LOCATION', 'global')
        client = genai.Client(vertexai=True, project=project, location=location)
    else:
        api_key = os.environ.get('GEMINI_API_KEY', '')
        if not api_key:
            raise RuntimeError("GEMINI_API_KEY env var required when LLM_PROVIDER=gemini")
        client = genai.Client(api_key=api_key)

    # Build multimodal content: images first, then prompt text
    contents = []
    for img_path in image_paths:
        data = Path(img_path).read_bytes()
        mime = _detect_mime(data, img_path)
        contents.append(types.Part.from_bytes(data=data, mime_type=mime))
    contents.append(prompt)

    # Config
    config = types.GenerateContentConfig(max_output_tokens=max_tokens)
    if system:
        config.system_instruction = system
    if json_output:
        config.response_mime_type = "application/json"

    response = client.models.generate_content(model=model, contents=contents, config=config)
    if response.text is None:
        # Some models return empty content on MAX_TOKENS or safety filters
        raise RuntimeError(
            f"LLM returned empty response (finish_reason="
            f"{response.candidates[0].finish_reason if response.candidates else 'unknown'})"
        )
    return response.text


# ---------- OpenAI-compatible (MiniMax, DeepSeek, OpenAI, etc.) ----------

def _call_openai(image_paths, prompt, max_tokens, system):
    from openai import OpenAI

    model = os.environ.get('LLM_MODEL', 'gemini-3-flash-preview')
    api_key = os.environ.get('OPENAI_API_KEY', '')
    base_url = os.environ.get('OPENAI_BASE_URL', None)

    if not api_key:
        raise RuntimeError("OPENAI_API_KEY env var required when LLM_PROVIDER=openai")

    client = OpenAI(api_key=api_key, base_url=base_url)

    # Build multimodal message content
    content = []
    for img_path in image_paths:
        data = Path(img_path).read_bytes()
        mime = _detect_mime(data, img_path)
        b64 = base64.b64encode(data).decode()
        content.append({
            "type": "image_url",
            "image_url": {"url": f"data:{mime};base64,{b64}"}
        })
    content.append({"type": "text", "text": prompt})

    messages = []
    if system:
        messages.append({"role": "system", "content": system})
    messages.append({"role": "user", "content": content})

    response = client.chat.completions.create(model=model, messages=messages, max_tokens=max_tokens)
    text = response.choices[0].message.content
    if not text:
        reason = response.choices[0].finish_reason if response.choices else "unknown"
        raise RuntimeError(f"LLM returned empty response (finish_reason={reason})")
    return text
