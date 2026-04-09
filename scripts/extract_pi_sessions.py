"""Extract pi.dev session JSONL into a readable handoff markdown.

Strips thinking blocks, condenses tool calls, keeps user messages verbatim
and assistant text, plus important tool results (file writes, commands).
"""
import json
import sys
import re
from pathlib import Path

SESSIONS_DIR = Path(r"C:\Users\fangz\.pi\agent\sessions\--C--Users-fangz-OneDrive-Desktop-MercaFlow--")

SESSIONS = {
    "session1_meli_api": "2026-04-04T17-24-18-621Z_02dbae38-0450-44ef-8309-0d88db11ccfe.jsonl",
    "session2_picset_vertex": "2026-04-04T18-01-03-175Z_695d8a77-aa1a-4c7b-84f7-b92a9dbcdc16.jsonl",
}

ANSI_RE = re.compile(r"\x1b\[[0-9;]*m")


def strip_ansi(s: str) -> str:
    return ANSI_RE.sub("", s or "")


def truncate(s: str, limit: int = 2000) -> str:
    s = s or ""
    if len(s) <= limit:
        return s
    return s[:limit] + f"\n... [truncated {len(s) - limit} chars]"


def extract(path: Path, out: Path, title: str):
    lines = []
    lines.append(f"# {title}\n")
    lines.append(f"Source: `{path.name}`\n")
    lines.append("")

    user_turn = 0
    with path.open("r", encoding="utf-8") as fh:
        for raw in fh:
            try:
                obj = json.loads(raw)
            except Exception:
                continue

            t = obj.get("type")
            if t == "session":
                lines.append(f"- Session started: {obj.get('timestamp')}")
                lines.append(f"- CWD: `{obj.get('cwd')}`")
                lines.append("")
                continue
            if t == "model_change":
                lines.append(f"> model: {obj.get('provider')}/{obj.get('modelId')}")
                lines.append("")
                continue

            if t != "message":
                continue

            msg = obj.get("message", {})
            role = msg.get("role")
            content = msg.get("content", [])
            if not isinstance(content, list):
                continue

            if role == "user":
                parts = []
                for c in content:
                    if not isinstance(c, dict):
                        continue
                    ct = c.get("type")
                    if ct == "text":
                        txt = (c.get("text") or "").strip()
                        if txt and not txt.startswith("<"):
                            parts.append(txt)
                    elif ct == "toolResult":
                        tr = c.get("content")
                        if isinstance(tr, list):
                            for sub in tr:
                                if isinstance(sub, dict) and sub.get("type") == "text":
                                    parts.append(f"[tool-result] {truncate(sub.get('text', ''), 600)}")
                        elif isinstance(tr, str):
                            parts.append(f"[tool-result] {truncate(tr, 600)}")
                if parts:
                    user_turn += 1
                    lines.append(f"## USER [{user_turn}]")
                    for p in parts:
                        lines.append(p)
                    lines.append("")

            elif role == "assistant":
                asst_parts = []
                tool_calls = []
                for c in content:
                    if not isinstance(c, dict):
                        continue
                    ct = c.get("type")
                    if ct == "text":
                        txt = strip_ansi((c.get("text") or "").strip())
                        if txt:
                            asst_parts.append(txt)
                    elif ct == "toolCall":
                        name = c.get("name") or c.get("toolName") or "tool"
                        inp = c.get("input") or c.get("arguments") or {}
                        # condense common tools
                        summary = None
                        if isinstance(inp, dict):
                            if name in ("Bash", "shell"):
                                cmd = inp.get("command") or inp.get("cmd") or ""
                                summary = f"`$ {truncate(cmd, 500)}`"
                            elif name in ("Read",):
                                summary = f"read `{inp.get('file_path') or inp.get('path')}`"
                            elif name in ("Write",):
                                fp = inp.get("file_path") or inp.get("path") or ""
                                summary = f"write `{fp}` ({len(inp.get('content', ''))} chars)"
                            elif name in ("Edit",):
                                summary = f"edit `{inp.get('file_path') or inp.get('path')}`"
                            elif name in ("Grep",):
                                summary = f"grep `{inp.get('pattern')}` in `{inp.get('path') or inp.get('glob') or '.'}`"
                            elif name in ("Glob",):
                                summary = f"glob `{inp.get('pattern')}`"
                            elif name in ("WebFetch", "web_fetch"):
                                summary = f"fetch `{inp.get('url')}`"
                            elif name in ("WebSearch",):
                                summary = f"websearch `{inp.get('query')}`"
                            else:
                                summary = f"{name}({truncate(json.dumps(inp, ensure_ascii=False), 300)})"
                        tool_calls.append(f"- {name}: {summary}")
                if asst_parts or tool_calls:
                    lines.append("### assistant")
                    for p in asst_parts:
                        lines.append(truncate(p, 3000))
                    if tool_calls:
                        lines.append("")
                        lines.append("_tools:_")
                        lines.extend(tool_calls[:20])
                        if len(tool_calls) > 20:
                            lines.append(f"_... +{len(tool_calls)-20} more_")
                    lines.append("")

    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text("\n".join(lines), encoding="utf-8")
    return user_turn, out.stat().st_size


if __name__ == "__main__":
    out_dir = Path(r"C:\Users\fangz\OneDrive\Desktop\MercaFlow\.pi-handoff")
    out_dir.mkdir(exist_ok=True)

    for key, fname in SESSIONS.items():
        src = SESSIONS_DIR / fname
        dst = out_dir / f"{key}.md"
        turns, size = extract(src, dst, key)
        print(f"{key}: {turns} user turns -> {dst} ({size/1024:.1f} KB)")
