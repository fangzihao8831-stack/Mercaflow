# MercaFlow UI Design — MVP (MeLi Only)

## Core Workflow: Drop → Generate → Fix → Publish

The UI serves ONE job: get product photos from supplier image to MeLi listing as fast as possible.

## What's Different from PicSet
- No 详情图要求 text area — AI analyzes the photo, you just drop it
- Real-time generation — images appear as they're generated, not all-at-once
- Per-image regeneration — click one bad image, fix just that one
- Auto-scoring — every image gets a quality badge instantly
- Queue system — drop multiple products, they process one after another
- Direct to MeLi — generated images feed into listing creation (future)

## Layout: 2-column

```
┌─────────────────────────────────────────────────────────────────────┐
│  MercaFlow                                          [设置] [历史]    │
├────────────────────────┬────────────────────────────────────────────┤
│                        │                                            │
│  LEFT PANEL (Input)    │  RIGHT PANEL (Output)                      │
│                        │                                            │
│  ┌──────────────────┐  │  Step indicator:                           │
│  │  产品图片         │  │  ① 上传 → ② 分析中 → ③ 确认规划 → ④ 生成中 → ⑤ 完成  │
│  │  [Upload area]    │  │                                            │
│  │  drag & drop      │  │  ┌──────────────────────────────────────┐  │
│  │  up to 6 photos   │  │  │  整体设计规范 (collapsible)           │  │
│  └──────────────────┘  │  │  - 色彩系统                            │  │
│                        │  │  - 摄影风格                            │  │
│  ┌──────────────────┐  │  │  - 品质要求                            │  │
│  │  配置模板 ▼       │  │  │  [编辑] button                        │  │
│  │                   │  │  └──────────────────────────────────────┘  │
│  │  • MercadoLibre   │  │                                            │
│  │  • TikTok Shop    │  │  ┌──────────────────────────────────────┐  │
│  │  • Amazon         │  │  │  图片规划 (per image cards)            │  │
│  │  • Shein          │  │  │                                      │  │
│  │  • 自定义          │  │  │  [1] 主视觉图  [编辑] [删除]          │  │
│  │                   │  │  │  [2] 功能展示图  [编辑] [删除]         │  │
│  └──────────────────┘  │  │  [3] 细节特写图  [编辑] [删除]         │  │
│                        │  │  [4] 多色集合图  [编辑] [删除]         │  │
│  ┌──────────────────┐  │  │  [5] 场景应用图  [编辑] [删除]         │  │
│  │  图片组 (Groups)  │  │  │  [+ 添加图片]                         │  │
│  │                   │  │  └──────────────────────────────────────┘  │
│  │  组1: 纯视觉 ×6   │  │                                            │
│  │  ├ 比例: 1:1      │  │  ┌──────────────────────────────────────┐  │
│  │  ├ 清晰度: 2K     │  │  │  生成结果 (image grid)                │  │
│  │  └ 语言: 无文字    │  │  │                                      │  │
│  │                   │  │  │  [img1] [img2] [img3] [img4]          │  │
│  │  组2: 西班牙语 ×2  │  │  │  [img5] [img6] [img7] [img8]         │  │
│  │  ├ 比例: 1:1      │  │  │                                      │  │
│  │  ├ 清晰度: 2K     │  │  │  Each image has:                      │  │
│  │  └ 语言: 西班牙语  │  │  │  - Score badge (85, 92, etc.)         │  │
│  │                   │  │  │  - [重新生成] button                   │  │
│  │  [+ 添加组]       │  │  │  - [下载] button                      │  │
│  └──────────────────┘  │  │  - Flag icon if hallucination          │  │
│                        │  │  └──────────────────────────────────────┘  │
│  ┌──────────────────┐  │                                            │
│  │  高级设置          │  │                                            │
│  │  ├ 模型: Flash    │  │                                            │
│  │  ├ 温度: 0.4      │  │                                            │
│  │  └ 变体检测: 自动  │  │                                            │
│  └──────────────────┘  │                                            │
│                        │                                            │
│  [分析产品] [生成全部] │                                            │
│                        │                                            │
├────────────────────────┴────────────────────────────────────────────┤
│  Status bar: 生成进度 ████████░░ 6/8 | 耗时: 45s | 积分: €2.14     │
└─────────────────────────────────────────────────────────────────────┘
```

## Key Differences from PicSet

### 1. NO 详情图要求 text area
PicSet forces you to type product description. We don't.
- Upload photo → AI analyzes automatically
- Optional: add notes if you want (collapsible "补充说明" field)
- The planning model extracts everything from the image

### 2. 配置模板 (Platform Presets)
One-click presets that configure everything:

```json
{
  "MercadoLibre": {
    "groups": [
      {"count": 6, "ratio": "1:1", "resolution": "2K", "language": "none", "label": "纯视觉详情图"},
      {"count": 2, "ratio": "1:1", "resolution": "2K", "language": "es-MX", "label": "西班牙语卖点图"}
    ],
    "max_images": 10,
    "first_image_white_bg": true,
    "catalog_title_max": 200,
    "description_max": 50000
  },
  "TikTok Shop": {
    "groups": [
      {"count": 5, "ratio": "9:16", "resolution": "2K", "language": "none", "label": "竖版详情图"},
      {"count": 3, "ratio": "1:1", "resolution": "2K", "language": "none", "label": "方形主图"}
    ],
    "max_images": 9
  },
  "Amazon": {
    "groups": [
      {"count": 1, "ratio": "1:1", "resolution": "2K", "language": "none", "label": "白底主图", "white_bg_required": true},
      {"count": 6, "ratio": "1:1", "resolution": "2K", "language": "none", "label": "场景详情图"}
    ],
    "max_images": 9,
    "first_image_white_bg": true
  },
  "Shein": {
    "groups": [
      {"count": 5, "ratio": "3:4", "resolution": "2K", "language": "none", "label": "竖版模特图"}
    ],
    "max_images": 8
  }
}
```

### 3. 图片组 (Image Groups) — Mix settings in one batch
Instead of one global setting, define GROUPS:
- Group 1: 6 images, 1:1, 2K, no text (detailed product shots)
- Group 2: 2 images, 1:1, 2K, Spanish text (selling point images with overlay)

Each group gets its own planning call with different `{TARGET_LANGUAGE}`.
All groups share the same 整体设计规范 for visual consistency.

### 4. 变体检测 (Variant Detection)
When the photo shows multiple colors:
- Auto-detect variants from catalog image
- Show detected variants as chips: [粉色 ✓] [米白 ✓] [薄荷绿 ✓]
- User can toggle which variants to include
- Auto-distribute images: N per variant + shared shots

### 5. Inline Editing
Every 图片规划 card is editable:
- Click [编辑] → expand to show full brief in PicSet format
- Change angle, composition, props, mood
- Re-generate single image without re-planning

### 6. Score & Hallucination Badges
Each generated image shows:
- Score (from evaluator): green 85+ / yellow 70-84 / red <70
- Hallucination flag if structural issues detected
- One-click [重新生成] with auto-corrected prompt

### 7. 一键上架 (One-click Publish) — Future
After images pass validation:
- Auto-generate Spanish title + description
- Calculate price from import cost
- [上架到MercadoLibre] button → creates listing via API
- [创建目录产品] button → submits catalog suggestion

## Component Hierarchy

```
App
├── Header (logo, settings, history)
├── MainLayout (2-column)
│   ├── LeftPanel
│   │   ├── ImageUploader (drag & drop, up to 6 photos)
│   │   ├── PlatformPresets (dropdown with saved configs)
│   │   ├── ImageGroups (list of group configs)
│   │   │   └── GroupCard (count, ratio, resolution, language)
│   │   ├── AdvancedSettings (model, temperature, variant detection)
│   │   └── ActionButtons (分析, 生成全部)
│   └── RightPanel
│       ├── StepIndicator (5 steps)
│       ├── DesignSpecsCard (整体设计规范, collapsible, editable)
│       ├── ShotPlanCards (list of 图片规划, each editable)
│       └── ResultGrid (generated images with scores)
└── StatusBar (progress, time, cost)
```

## MVP Improvements Over PicSet

### 1. Product Queue
Drop multiple supplier photos → they stack as a queue on the left.
Each product processes independently. You can review product 1 while product 2 generates.
No more one-at-a-time waiting.

### 2. Live Generation Feed
Images appear one-by-one as Gemini Pro returns them (parallel workers).
Don't wait 3 minutes for all 8 — see the first image in 20 seconds.
Bad image? Hit [重新生成] immediately while others are still generating.

### 3. Smart Defaults
MeLi settings are hardcoded for MVP:
- 1:1 square, 2K, 无文字(纯视觉), 8 images
- First image: hero shot (white-ish background for search thumbnail)
- If variants detected: auto-includes one multi-color shot
User only adjusts image count (slider: 3-10).

### 4. Variant Chips
When AI detects multiple colors in the catalog image:
```
检测到变体: [粉色 ✓] [米白 ✓] [薄荷绿 ✓]  [全部] [仅主色]
```
Toggle which variants to feature. Default: primary variant + one group shot.

### 5. Quality Gate
Every image auto-scored on generation:
- ✅ Green (85+): ready to use
- ⚠️ Yellow (70-84): review recommended  
- ❌ Red (<70): auto-queued for regeneration

Red images get regenerated automatically with the evaluator's retry_guidance.
You only manually deal with yellow images.

### 6. One-Click Export
After review:
- [下载全部] — zip all passed images
- [复制到MeLi] — future: auto-upload to listing draft

### 7. 补充说明 (Optional Notes)
Collapsible field at the bottom of the left panel.
Most of the time you don't need it — AI handles everything from the photo.
But if you want to specify something ("show the product next to a handbag"), you can.

## Tech Stack
- **Next.js + React + Tailwind + shadcn/ui** — clean, fast, matches PicSet's aesthetic
- **Python FastAPI backend** — wraps our pipeline, handles Vertex AI calls
- **WebSocket** — for real-time image generation feed
- Future: deploy as SaaS if it works
