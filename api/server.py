# -*- coding: utf-8 -*-
"""
MercaFlow API Server
Connects the UI to the image generation pipeline.
Uses Vertex AI (not Gemini Developer API).
"""
import os
import sys
import json
import time
import base64
import asyncio
import subprocess
from pathlib import Path
from typing import Optional
from fastapi import FastAPI, UploadFile, File, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from pydantic import BaseModel

# Add parent dir to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from google.genai import types
from vertex_client import get_client, PLANNING_MODEL, GENERATION_MODEL, PROJECT, LOCATION

app = FastAPI(title="MercaFlow API", version="0.1.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Load env
from dotenv import load_dotenv
load_dotenv(Path(__file__).parent.parent / ".env")

# Load prompt template
PROMPT_TEMPLATE_PATH = Path(__file__).parent.parent / "prompts" / "analysis-prompt.txt"
EVALUATOR_PROMPT_PATH = Path(__file__).parent.parent / "prompts" / "evaluator-prompt.txt"

def get_prompt(image_count: int, target_language: str, requirements: str) -> str:
    with open(PROMPT_TEMPLATE_PATH, encoding="utf-8") as f:
        template = f.read()
    return (
        template
        .replace("{IMAGE_COUNT}", str(image_count))
        .replace("{TARGET_LANGUAGE}", target_language)
        .replace("{REQUIREMENTS}", requirements)
    )

# Vertex AI client (uses ADC — gcloud auth application-default login)
gemini = get_client()


class GenerationConfig(BaseModel):
    image_count: int = 8
    aspect_ratio: str = "1:1"
    resolution: str = "2K"
    language: str = "none"
    model: str = "gemini-3-pro-image-preview"
    planning_model: str = "gemini-3-flash-preview"
    temperature: float = 0.4
    notes: str = ""
    auto_retry: bool = True
    variant_detection: str = "auto"
    parallel_workers: int = 8


class AnalysisResult(BaseModel):
    is_complex_product: bool
    design_specs: str
    images: list


# Store uploaded images temporarily
uploaded_images: dict = {}
generation_results: dict = {}


@app.get("/health")
def health():
    return {
        "status": "ok",
        "vertex_ai": "active",
        "project": PROJECT,
        "location": LOCATION,
        "planning_model": PLANNING_MODEL,
        "generation_model": GENERATION_MODEL,
    }


@app.post("/upload")
async def upload_image(file: UploadFile = File(...)):
    """Upload a product image."""
    content = await file.read()
    image_id = f"img_{int(time.time() * 1000)}"
    
    # Save to temp dir
    upload_dir = Path(__file__).parent.parent / "temp" / "uploads"
    upload_dir.mkdir(parents=True, exist_ok=True)
    
    filepath = upload_dir / f"{image_id}_{file.filename}"
    with open(filepath, "wb") as f:
        f.write(content)
    
    # Store reference
    uploaded_images[image_id] = {
        "path": str(filepath),
        "filename": file.filename,
        "size": len(content),
        "b64": base64.b64encode(content).decode("utf-8"),
    }
    
    return {
        "image_id": image_id,
        "filename": file.filename,
        "size": len(content),
    }


@app.post("/analyze")
async def analyze_product(config: GenerationConfig, image_ids: list[str] = []):
    """
    Run planning step: analyze product images and generate shot briefs.
    Uses Vertex AI Gemini Flash.
    """
    if not image_ids:
        return {"error": "No images provided"}
    
    # Build language string
    lang_map = {
        "none": "无文字(纯视觉)",
        "zh-CN": "中文",
        "es-MX": "西班牙语(墨西哥)",
        "en-US": "英语",
        "pt-BR": "葡萄牙语(巴西)",
    }
    target_lang = lang_map.get(config.language, config.language)
    
    # Build requirements
    requirements = "无文案纯视觉设计，目标平台MercadoLibre拉丁美洲市场"
    if config.notes:
        requirements += f"\n补充说明：{config.notes}"
    
    prompt = get_prompt(config.image_count, target_lang, requirements)
    
    # TODO: Call Vertex AI when billing is active
    # For now, return mock data
    return {
        "status": "mock",
        "message": "Vertex AI billing pending — returning mock analysis",
        "config": config.dict(),
        "prompt_preview": prompt[:500] + "...",
        "result": {
            "is_complex_product": True,
            "design_specs": "# 整体设计规范\n\n## 色彩系统\n- 主色调：待分析\n\n## 摄影风格\n- 光线：柔和自然光\n\n## 品质要求\n- 分辨率：4K/高清\n- 真实感：超写实/照片级",
            "images": [
                {"title": f"图{i+1}：待生成", "description": "等待Vertex AI恢复后生成", "design_content": "待生成"}
                for i in range(config.image_count)
            ],
        },
    }


@app.post("/generate/{image_index}")
async def generate_single(image_index: int, config: GenerationConfig):
    """
    Generate a single image using Vertex AI Gemini Pro.
    """
    # TODO: Implement when billing is active
    return {
        "status": "mock",
        "message": f"Image {image_index} — Vertex AI billing pending",
        "image_index": image_index,
        "config": {
            "model": config.model,
            "aspect_ratio": config.aspect_ratio,
            "resolution": config.resolution,
        },
    }


@app.websocket("/ws/generate")
async def websocket_generate(websocket: WebSocket):
    """
    WebSocket for real-time image generation.
    Client sends config, server streams back images as they're generated.
    """
    await websocket.accept()
    try:
        # Receive config
        data = await websocket.receive_json()
        config = GenerationConfig(**data.get("config", {}))
        image_ids = data.get("image_ids", [])
        
        await websocket.send_json({
            "type": "status",
            "message": "Planning...",
            "step": "analyzing",
        })
        
        # TODO: Real planning call to Vertex AI
        await asyncio.sleep(2)  # Mock delay
        
        await websocket.send_json({
            "type": "plan",
            "design_specs": "Mock design specs",
            "briefs": [
                {"title": f"图{i+1}", "description": "Mock brief"}
                for i in range(config.image_count)
            ],
            "step": "planning",
        })
        
        # TODO: Real generation calls to Vertex AI
        for i in range(config.image_count):
            await websocket.send_json({
                "type": "generating",
                "image_index": i,
                "step": "generating",
            })
            
            await asyncio.sleep(1)  # Mock delay
            
            # Mock generated image
            await websocket.send_json({
                "type": "image_done",
                "image_index": i,
                "title": f"图{i+1}",
                "score": 75 + (i * 3) % 25,
                "step": "generating",
            })
        
        await websocket.send_json({
            "type": "complete",
            "step": "complete",
            "total_images": config.image_count,
        })
        
    except WebSocketDisconnect:
        pass
    except Exception as e:
        await websocket.send_json({"type": "error", "message": str(e)})


@app.get("/images/{image_id}")
async def get_image(image_id: str):
    """Serve an uploaded or generated image."""
    if image_id in uploaded_images:
        return FileResponse(uploaded_images[image_id]["path"])
    return {"error": "Image not found"}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
