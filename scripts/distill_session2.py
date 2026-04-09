"""Distill pi session 2 JSONL into a focused handoff brief.

Keeps: every user message verbatim, every assistant TEXT response,
every Write/Edit target, every Bash command, tool result excerpts for
file lists/curl output. Strips thinking blocks and verbose tool params.
"""
import json
import re
from pathlib import Path

SRC = Path(r"C:\Users\fangz\.pi\agent\sessions\--C--Users-fangz-OneDrive-Desktop-MercaFlow--\2026-04-04T18-01-03-175Z_695d8a77-aa1a-4c7b-84f7-b92a9dbcdc16.jsonl")
OUT = Path(r"C:\Users\fangz\OneDrive\Desktop\MercaFlow\.pi-handoff\session2_BRIEF.md")

ANSI = re.compile(r"\x1b\[[0-9;]*m")


def clean(s):
    return ANSI.sub("", s or "")


def trim(s, n=1500):
    s = s or ""
    return s if len(s) <= n else s[:n] + f"... [+{len(s)-n}c]"


lines = ["# pi Session 2 — Condensed Handoff Brief", ""]
user_n = 0
files_written = []
files_edited = []
bash_cmds = []

with SRC.open("r", encoding="utf-8") as fh:
    for raw in fh:
        try:
            obj = json.loads(raw)
        except Exception:
            continue
        if obj.get("type") != "message":
            continue
        msg = obj.get("message", {})
        role = msg.get("role")
        content = msg.get("content", [])
        if not isinstance(content, list):
            continue

        if role == "user":
            txt_parts = []
            tool_results = []
            for c in content:
                if not isinstance(c, dict):
                    continue
                if c.get("type") == "text":
                    t = (c.get("text") or "").strip()
                    if t and not t.startswith("<"):
                        txt_parts.append(t)
                elif c.get("type") == "toolResult":
                    tr = c.get("content")
                    if isinstance(tr, list):
                        for sub in tr:
                            if isinstance(sub, dict) and sub.get("type") == "text":
                                tool_results.append(trim(sub.get("text", ""), 400))
                    elif isinstance(tr, str):
                        tool_results.append(trim(tr, 400))
            if txt_parts:
                user_n += 1
                lines.append(f"## U[{user_n}]")
                for p in txt_parts:
                    lines.append(trim(p, 2000))
                lines.append("")
            # Skip pure tool-result noise unless small
            if tool_results and not txt_parts:
                small = [r for r in tool_results if len(r) < 200]
                if small:
                    lines.append(f"_tr:_ " + " | ".join(small[:3]))
                    lines.append("")

        elif role == "assistant":
            asst_text = []
            for c in content:
                if not isinstance(c, dict):
                    continue
                ct = c.get("type")
                if ct == "text":
                    t = clean((c.get("text") or "").strip())
                    if t:
                        asst_text.append(t)
                elif ct == "toolCall":
                    name = c.get("name") or c.get("toolName") or "tool"
                    inp = c.get("input") or c.get("arguments") or {}
                    if isinstance(inp, dict):
                        if name in ("Bash", "shell", "bash"):
                            cmd = inp.get("command") or inp.get("cmd") or ""
                            bash_cmds.append(cmd)
                            asst_text.append(f"`$ {trim(cmd, 400)}`")
                        elif name in ("Write",):
                            fp = inp.get("file_path") or inp.get("path") or ""
                            sz = len(inp.get("content", "") or "")
                            files_written.append((fp, sz))
                            asst_text.append(f"**WROTE** `{fp}` ({sz}c)")
                        elif name in ("Edit", "edit"):
                            fp = inp.get("file_path") or inp.get("path") or ""
                            files_edited.append(fp)
                            asst_text.append(f"**EDIT** `{fp}`")
                        elif name in ("WebFetch", "web_fetch", "fetch"):
                            asst_text.append(f"_fetch_ {inp.get('url', '')}")
                        elif name in ("WebSearch",):
                            asst_text.append(f"_search_ {inp.get('query', '')}")
                        elif name in ("browser_navigate", "browser_click", "browser_fill_form", "browser_type"):
                            asst_text.append(f"_browser.{name}_ {trim(json.dumps(inp, ensure_ascii=False), 300)}")
                        # skip Read/Grep/Glob for brevity
            if asst_text:
                lines.append("### A")
                for t in asst_text:
                    lines.append(trim(t, 2500))
                lines.append("")

lines.append("")
lines.append("---")
lines.append("## Files written (chronological)")
for fp, sz in files_written:
    lines.append(f"- `{fp}` ({sz}c)")
lines.append("")
lines.append("## Files edited (chronological)")
for fp in files_edited:
    lines.append(f"- `{fp}`")
lines.append("")
lines.append(f"## Total bash commands: {len(bash_cmds)}")

OUT.parent.mkdir(parents=True, exist_ok=True)
OUT.write_text("\n".join(lines), encoding="utf-8")
print(f"user turns: {user_n}")
print(f"files written: {len(files_written)}")
print(f"files edited: {len(files_edited)}")
print(f"bash cmds: {len(bash_cmds)}")
print(f"output: {OUT} ({OUT.stat().st_size/1024:.1f} KB)")
