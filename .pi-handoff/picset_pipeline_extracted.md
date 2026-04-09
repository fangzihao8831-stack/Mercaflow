# PicSet Pipeline — Complete Extraction (v2)

Source: 61 total records from 2 capture files

## 1. PicSet Edge Functions Called

| Endpoint | Calls |
|---|---|
| `rest/v1/generation_jobs` (polling) | 35 |
| `rest/v1/projects` | 3 |
| `functions/v1/analyze-product-v2` | 3 |
| `functions/v1/ai-write-quota` | 2 |
| `functions/v1/generate-prompts-v2` | 2 |
| `functions/v1/generate-image` | 2 |
| `functions/v1/get-oss-sts` | 1 |
| `functions/v1/ai-write-requirements` | 1 |

## 2. Completed Jobs by Type

| Type | Count |
|---|---|
| `AI_WRITE` | 1 |
| `ANALYSIS` | 3 |
| `UNKNOWN` | 2 |
| `IMAGE_GEN` | 2 |

## 3. Edge Function Requests (what the client sends)

### 3.1 `functions/v1/ai-write-requirements`

**Call 1** (src=`picset-capture.json`, status=`200`)

Request body:
```json
{
  "imageType": "detail",
  "productImage": "temp/b7cf84de-14de-4571-b2ca-a63b614e5b49/1775647293176_product_0.png",
  "productImages": [
    "temp/b7cf84de-14de-4571-b2ca-a63b614e5b49/1775647293176_product_0.png",
    "temp/b7cf84de-14de-4571-b2ca-a63b614e5b49/1775647293197_product_1.png",
    "temp/b7cf84de-14de-4571-b2ca-a63b614e5b49/1775647293207_product_2.png"
  ],
  "uiLanguage": "zh"
}
```

Response body:
```json
{
  "job_id": "59ec688a-690e-443a-a67e-3ad0d35614a7",
  "todayUsed": 1,
  "freeLimit": 5,
  "creditCost": 1
}
```


### 3.2 `functions/v1/analyze-product-v2`

**Call 1** (src=`picset-capture.json`, status=`200`)

Request body:
```json
{
  "productImage": "temp/b7cf84de-14de-4571-b2ca-a63b614e5b49/1775647655401_product_0.png",
  "productImages": [
    "temp/b7cf84de-14de-4571-b2ca-a63b614e5b49/1775647655401_product_0.png",
    "temp/b7cf84de-14de-4571-b2ca-a63b614e5b49/1775647655420_product_1.png",
    "temp/b7cf84de-14de-4571-b2ca-a63b614e5b49/1775647655433_product_2.png"
  ],
  "requirements": "**目标平台：** 未明确\n\n**风格名称：** 优雅名媛风\n\n## 视觉风格\n极简高级感，通过柔和的自然光影突出皮革质感与金色拉链的精致细节。\n\n## 整组图统一场景\n高端大理石梳妆台，背景点缀丝绸衬布与少量高档香水瓶，营造精致生活的氛围。\n\n## 产品信息\n**产品名称：** A638 便携式首饰盒\n\n**核心卖点：** 奢华质感，精致收纳，名媛气质必备。\n\n**适用人群：** 都市白领、追求生活品质的女性。\n\n## 产品参数\n**材质：** 优质PU皮革、金属拉链、柔软植绒内里\n**尺寸：** 8.5*8.5*5.5cm\n**颜色：** 樱花粉、象牙白、薄荷绿、丁香紫\n**功能：** 戒指槽、项链挂钩、多功能收纳格\n\n## 设计风格\n高级/简约/电商质感\n\n## 主题配色\n- **主色调：** 奶油杏色 [#F5F5DC]（用于大理石背景与阴影）\n- **辅助色：** 香槟金 [#D4AF37]（用于文字标题与金属装饰）\n- **点缀色：** 暖咖色 [#8B4513]（用于强调皮革缝线与图标）\n\n## 用户需求原文\n无",
  "uiLanguage": "zh-CN",
  "targetLanguage": "none",
  "imageCount": 1,
  "imageType": "detail",
  "trace_id": "1f4ae94a-5689-4c8c-9f84-ce74da6decc7",
  "project_id": "572820ad-3ea8-484b-955b-37afae21d780"
}
```

Response body:
```json
{
  "job_id": "4b553315-30ff-43bd-aab7-d3ddae8b20f6"
}
```

**Call 2** (src=`picset-capture-2.json`, status=`200`)

Request body:
```json
{
  "productImage": "temp/b7cf84de-14de-4571-b2ca-a63b614e5b49/1775648384210_product_0.png",
  "productImages": [
    "temp/b7cf84de-14de-4571-b2ca-a63b614e5b49/1775648384210_product_0.png"
  ],
  "requirements": "儿童西班牙语描红练习册，骑马钉装订薄册子。目标平台MercadoLibre墨西哥。",
  "uiLanguage": "zh-CN",
  "targetLanguage": "none",
  "imageCount": 1,
  "imageType": "detail",
  "themeColors": null,
  "trace_id": "3a673927-3fd2-4649-ac4d-74bcb6a3d7f2",
  "project_id": "e6a544b2-b4e3-4c9c-86db-c2c415c80b86"
}
```

Response body:
```json
{
  "job_id": "6d2fe6a3-0c12-4ccc-b3bb-8d522b3e0e09"
}
```

**Call 3** (src=`picset-capture-2.json`, status=`200`)

Request body:
```json
{
  "productImage": "temp/b7cf84de-14de-4571-b2ca-a63b614e5b49/1775649149614_product_0.png",
  "productImages": [
    "temp/b7cf84de-14de-4571-b2ca-a63b614e5b49/1775649149614_product_0.png"
  ],
  "requirements": "儿童西班牙语描红练习册，骑马钉装订薄册子。目标平台MercadoLibre墨西哥。",
  "uiLanguage": "zh-CN",
  "targetLanguage": "es",
  "imageCount": 1,
  "imageType": "detail",
  "themeColors": null,
  "trace_id": "7e5a0990-2141-4296-a555-10df08e0dcce",
  "project_id": "c1599af8-dbaa-4dbe-874f-b2d6dbd19df5"
}
```

Response body:
```json
{
  "job_id": "e199520e-05bc-4f3d-919a-58d77337d10e"
}
```


### 3.3 `functions/v1/generate-prompts-v2`

**Call 1** (src=`picset-capture-2.json`, status=`200`)

Request body:
```json
{
  "analysisJson": {
    "images": [
      {
        "title": "沉浸式学习场景展示",
        "description": "通过模拟真实的儿童书桌学习场景，展示练习册的内页细节与骑马钉装订的平摊效果，激发购买欲望。",
        "design_content": "**产品复杂结构判定**：false\n\n##图1：场景化展示图\n\n**设计目标**：展现产品在实际使用中的状态，强调内页的易写性和内容的丰富度。\n\n**产品出现**：是\n\n**图中图元素**：\n-无\n\n**构图方案**：\n- 产品占比：65%\n- 布局方式：采用45度俯视斜向构图。练习册呈自然翻开状态，平铺在浅色木质书桌上，展示出含有“autobús”、“miniván”等单词的内页。\n-文字区域：无文案区域\n\n**内容要素**：\n- 展示重点：通过纯视觉、构图和光影展现产品，不添加任何排版文案。重点展示内页清晰的描红虚线和鲜艳的配图。\n- 突出卖点：骑马钉装订可180度平摊，方便儿童书写；纸张质感厚实不洇墨。\n- 背景元素：浅色木纹桌面，右上角露出半个盛放彩色铅笔的笔筒。\n-装饰元素：一支红色的儿童铅笔斜靠在练习册边缘，旁边散落两块彩色积木，增加生活气息。\n\n**文字内容**（使用 无文字(纯视觉)）：\n- 主标题：None\n- 副标题：None\n- 说明文字：None\n\n**氛围营造**：\n- 情绪关键词：温馨、专注、教育、快乐、整洁\n-光影效果：左上角投射进柔和的晨光，在练习册右侧形成淡淡的投影，营造出静谧的学习午后感。"
      }
    ],
    "_timing": {
      "total_ms": 20934,
      "queue_wait_ms": 0,
      "ai_call_total_ms": 20741,
      "ef_preprocess_ms": 44,
      "config_refresh_ms": 2
    },
    "design_specs": "# 整体设计规范\n\n> 所有图片必须遵循以下统一规范，确保视觉连贯性\n\n## 色彩系统\n-**主色调**：明亮天蓝色（#00AEEF）与活力柠檬黄（#FFF200），呼应封面插画色调，营造积极的学习氛围。\n- **辅助色**：糖果粉与草绿色，用于背景装饰元素，增加画面的趣味性。\n-**背景色**：浅原木色或纯净米白色，模拟真实的儿童书桌场景。\n\n## 字体系统\n- **标题字体**：无(纯视觉设计，不涉及排版文案)\n- **正文字体**：无(纯视觉设计，不涉及排版文案)\n-**字号层级**：无(纯视觉设计，不涉及排版文案)\n\n## 视觉语言\n- **装饰元素**：彩色铅笔、蜡笔、卡通造型的卷笔刀、木质积木，增加教育属性。\n- **图标风格**：无排版图标，仅保留产品本身的插画风格。\n-**留白原则**：采用呼吸感构图，产品周围保持20%-30%的留白，避免视觉拥挤，突出练习册的轻薄便携。\n\n## 摄影风格\n- **光线**：模拟柔和的自然窗光，带有淡淡的阴影，增强立体感。\n- **景深**：中等景深，使产品主体清晰，背景装饰物略微虚化。\n- **相机参数参考**：镜头35mm-50mm，光圈f/4.0，ISO 100。\n\n## 品质要求\n-分辨率：4K/高清\n- 风格：专业产品摄影/商业广告级\n- 真实感：超写实/照片级",
    "is_complex_product": false
  },
  "targetLanguage": "none",
  "imageType": "detail",
  "stream": true,
  "trace_id": "3a673927-3fd2-4649-ac4d-74bcb6a3d7f2",
  "project_id": "e6a544b2-b4e3-4c9c-86db-c2c415c80b86"
}
```

**Call 2** (src=`picset-capture-2.json`, status=`200`)

Request body:
```json
{
  "analysisJson": {
    "images": [
      {
        "title": "核心卖点综合展示图",
        "description": "通过封面与内页的组合展示，直观体现产品的大尺寸特征、清晰的描红设计以及12本装的规格优势。",
        "design_content": "**产品复杂结构判定**：false\n\n##图1：综合功能主图\n\n**设计目标**：在MercadoLibre搜索结果中脱颖而出，快速传达产品核心价值。\n\n**产品出现**：是\n\n**图中图元素**：\n- [左侧：产品封面图，展示可爱的小女孩插画和主标题]\n- [右侧：内页展开图，展示清晰的单词描红区域和对应的彩色插图]\n- [底部：12本练习册堆叠的微缩图，强调套装属性]\n\n**构图方案**：\n- 产品占比：75%\n- 布局方式：左右对开构图，封面位于左侧并略微倾斜以增加动感，内页位于右侧平铺展示细节。\n- 文字区域：顶部居中放置主标题，右下角放置规格标签。\n\n**内容要素**：\n- 展示重点：大字号描红路径、标准的西班牙语单词、丰富的彩色插图。\n- 突出卖点：适合3岁以上儿童、19x26cm大尺寸、骑马钉装订易于平铺。\n- 背景元素：浅蓝色渐变背景，带有淡雅的文具（如尺子、橡皮）水印装饰。\n- 装饰元素：彩色铅笔散落在产品周围，右上角添加一个“放大镜”图标指向内页文字，强调“Letra Grande”。\n\n**文字内容**（使用 西班牙语）：\n- 主标题：Libro de Trazos: Primeras Palabras\n- 副标题：¡Aprender a escribir es divertido y fácil!\n- 说明文字：Letra Grande | Tamaño 19x26cm | Pack de 12 unidades\n\n**氛围营造**：\n- 情绪关键词：趣味、教育、专业、清晰\n- 光影效果：明亮的顶部柔光，为练习册边缘添加轻微的投影，增强立体感。"
      }
    ],
    "_timing": {
      "total_ms": 18416,
      "queue_wait_ms": 0,
      "ai_call_total_ms": 18343,
      "ef_preprocess_ms": 43,
      "config_refresh_ms": 0
    },
    "design_specs": "# 整体设计规范\n\n> 所有图片必须遵循以下统一规范，确保视觉连贯性\n\n## 色彩系统\n- **主色调**：天空蓝（#00AEEF，呼应品牌Logo与底部色块）\n- **辅助色**：活力粉（#E91E63，呼应封面标题）与明黄色（增加儿童产品的趣味感）\n- **背景色**：纯净白或极浅灰，营造整洁、专业的教育氛围\n\n## 字体系统\n- **标题字体**：圆润、亲和力强的无衬线体（如 Quicksand Bold 或 Montserrat Alternates）\n- **正文字体**：清晰易读的幼教风格字体（如 Varela Round）\n- **字号层级**：大标题:副标题:正文 = 3:1.8:1\n\n## 视觉语言\n- **装饰元素**：彩色铅笔、星星奖章、手绘风格的小插画、纸张纹理\n- **图标风格**：扁平化、高对比度、圆角风格图标\n- **留白原则**：保持 20% 以上的边缘留白，确保视觉呼吸感，重点突出产品本身\n\n## 摄影风格\n- **光线**：明亮的自然光感，柔和阴影，避免强反光，模拟教室或书桌环境\n- **景深**：微距展示内页纹理，整体展示保持全焦清晰\n- **相机参数参考**：f/8.0, 1/125s, ISO 100\n\n## 品质要求\n- 分辨率：4K/高清\n- 风格：专业教育产品摄影/商业广告级\n- 真实感：超写实，完美还原纸张质感与印刷色彩",
    "is_complex_product": false
  },
  "targetLanguage": "es",
  "imageType": "detail",
  "stream": true,
  "trace_id": "7e5a0990-2141-4296-a555-10df08e0dcce",
  "project_id": "c1599af8-dbaa-4dbe-874f-b2d6dbd19df5"
}
```


### 3.4 `functions/v1/generate-image`

**Call 1** (src=`picset-capture-2.json`, status=`200`)

Request body:
```json
{
  "productImage": "temp/b7cf84de-14de-4571-b2ca-a63b614e5b49/1775648384210_product_0.png",
  "productImages": [
    "temp/b7cf84de-14de-4571-b2ca-a63b614e5b49/1775648384210_product_0.png"
  ],
  "prompt": "Subject: A high-quality children's Spanish vocabulary workbook. 本图中的主体必须与参考图中的 [Spanish Vocabulary Workbook] 严格一致,产品的形态、外形、颜色、材质、零件数量、连接关系、机械结构必须与参考图完全一致，不得做任何改变。严格还原参考图中产品的所有色彩，不做任何修改。产品本体、各组件、表面及质感的颜色必须与参考图完全一致。 The workbook is shown open to an interior page featuring vibrant illustrations of vehicles and words such as 'autobús' and 'miniván' with clear red tracing lines for handwriting practice. Composition: The composition uses a 45-degree top-down diagonal view, with the workbook occupying approximately 65% of the frame. The layout is balanced with 20%-30% negative space around the product to emphasize its slim and portable nature. Background: The scene is set on a light wood-grained desktop. In the foreground, a red children's pencil rests against the edge of the book, accompanied by two scattered colorful wooden blocks. The midground features the open workbook lying perfectly flat. In the background, the top-right corner reveals a partial view of a pencil holder filled with various colored pencils, slightly blurred to create depth. Lighting: Soft, natural morning light streams in from the top-left corner, casting gentle, subtle shadows to the right of the workbook, creating a three-dimensional effect and a serene atmosphere. Color Scheme: The palette is dominated by bright sky blue (#00AEEF) and vibrant lemon yellow (#FFF200), accented by candy pink and grass green decorative elements, all set against the light wood and rice white tones of the desk. Material Details: The workbook features a saddle-stitched binding that allows it to lay 180 degrees flat. The paper has a thick, premium matte texture that prevents ink bleeding, with clearly visible dotted tracing lines. Atmosphere: The mood is warm, focused, educational, and tidy, evoking a sense of happy learning during a quiet afternoon. Style: Professional commercial product photography with a clean, modern aesthetic. Quality: 4K resolution, shot with a 35mm-50mm lens at f/4.0 and ISO 100. 颜色保真：必须生成参考图中颜色的产品。结构保真度：严格复制参考图中产品的精确物理结构，匹配所有组件的精确数量、位置、比例和空间关系，每个元素必须在几何上精确且在现实世界中物理可实现，不得添加、移除、合并或变形任何结构元素。",
  "model": "nano-banana-pro",
  "aspectRatio": "3:4",
  "imageSize": "2K",
  "imageCount": 1,
  "turboEnabled": false,
  "speedMode": "normal",
  "imageType": "detail",
  "trace_id": "3a673927-3fd2-4649-ac4d-74bcb6a3d7f2",
  "project_id": "e6a544b2-b4e3-4c9c-86db-c2c415c80b86",
  "client_job_id": "3a673927-3fd2-4649-ac4d-74bcb6a3d7f2-0",
  "fe_attempt": 1,
  "metadata": {
    "is_batch": true,
    "batch_index": 0,
    "image_size": "2K",
    "product_images": [
      "temp/b7cf84de-14de-4571-b2ca-a63b614e5b49/1775648384210_product_0.png"
    ]
  }
}
```

Response body:
```json
{
  "job_id": "7f6ae5a2-466e-427f-8300-54c001466d87"
}
```

**Call 2** (src=`picset-capture-2.json`, status=`200`)

Request body:
```json
{
  "productImage": "temp/b7cf84de-14de-4571-b2ca-a63b614e5b49/1775649149614_product_0.png",
  "productImages": [
    "temp/b7cf84de-14de-4571-b2ca-a63b614e5b49/1775649149614_product_0.png"
  ],
  "prompt": "Subject: 本图中的主体必须与参考图中的 [Libro de Trazos: Primeras Palabras] 严格一致,产品的形态、外形、颜色、材质、零件数量、连接关系、机械结构必须与参考图完全一致，不得做任何改变。严格还原参考图中产品的所有色彩，不做任何修改。产品本体、各组件、表面及质感的颜色必须与参考图完全一致。This educational tracing book set features a vibrant cover with a cute little girl illustration and clear interior pages showing Spanish word tracing paths and colorful illustrations. Composition: The product occupies 75% of the frame. It uses a split-screen layout where the cover is on the left, slightly tilted to create a sense of motion, and the interior pages are spread flat on the right to show detail. A stack of 12 miniature books is positioned at the bottom to emphasize the set. The main title is centered at the top, and a specification label is in the bottom right. Background: A multi-layered depth with a foreground of scattered colored pencils. The midground features the books on a clean surface. The background is a soft light blue gradient (#00AEEF) decorated with subtle, elegant watermarks of stationery like rulers and erasers. Lighting: Bright natural light simulation, using a top softbox to create gentle illumination and soft shadows that enhance the 3D volume of the books without harsh reflections. Color Scheme: Dominant Sky Blue (#00AEEF), Vibrant Pink (#E91E63), Bright Yellow, and Pure White. Material Details: High-definition paper texture with visible fiber, matte finish to prevent glare, clear saddle-stitch binding, and sharp, saturated ink printing for the illustrations. Text Layout: The top center features 'Libro de Trazos: Primeras Palabras'. Below it is '¡Aprender a escribir es divertido y fácil!'. In the bottom right corner, 'Letra Grande | Tamaño 19x26cm | Pack de 12 unidades' is displayed clearly using a rounded sans-serif font. Inset Images: A circular magnifying glass icon is placed on the upper right, pointing towards the large tracing letters to highlight the 'Letra Grande' feature. Atmosphere: Fun, educational, professional, and clear. Style: Professional educational product photography, commercial advertising grade, ultra-realistic. Quality: 4K resolution, f/8.0, 1/125s, ISO 100. Color fidelity: Must generate the product in the colors of the reference image. Structural fidelity: Strictly copy the exact physical structure of the product in the reference image, matching all components' precise numbers, positions, proportions, and spatial relationships; every element must be geometrically precise and physically realizable, without adding, removing, merging, or deforming any structural elements.",
  "model": "nano-banana-pro",
  "aspectRatio": "3:4",
  "imageSize": "2K",
  "imageCount": 1,
  "turboEnabled": false,
  "speedMode": "normal",
  "imageType": "detail",
  "trace_id": "7e5a0990-2141-4296-a555-10df08e0dcce",
  "project_id": "c1599af8-dbaa-4dbe-874f-b2d6dbd19df5",
  "client_job_id": "7e5a0990-2141-4296-a555-10df08e0dcce-0",
  "fe_attempt": 1,
  "metadata": {
    "is_batch": true,
    "batch_index": 0,
    "image_size": "2K",
    "product_images": [
      "temp/b7cf84de-14de-4571-b2ca-a63b614e5b49/1775649149614_product_0.png"
    ]
  }
}
```

Response body:
```json
{
  "job_id": "cb11fcae-d9db-47b5-9c90-af00a6f29017"
}
```


### 3.5 `functions/v1/ai-write-quota`

**Call 1** (src=`picset-capture.json`, status=`200`)


Response body:
```json
{
  "todayUsed": 1,
  "freeLimit": 5,
  "creditCost": 1,
  "remainingFree": 4
}
```

**Call 2** (src=`picset-capture-2.json`, status=`200`)


Response body:
```json
{
  "todayUsed": 1,
  "freeLimit": 5,
  "creditCost": 1,
  "remainingFree": 4
}
```


### 3.6 `functions/v1/get-oss-sts`

**Call 1** (src=`picset-capture.json`, status=`200`)


Response body:
```json
{
  "accessKeyId": "STS.NYa5C7886CaE7j1PJKP122HfE",
  "accessKeySecret": "F1qmKLVPxmjSejt7o3dfp4rpAzhH6GFLKAaf8sjmfqcK",
  "securityToken": "CAISzAJ1q6Ft5B2yfSjIr5rUfvmD1ecX9KOuNUyAtEoeXL4e3Y3Npzz2IHhMe3JtAekYt/kwmmhQ6fYclqRuUJJfAEabZsUgsphaqaocogp/4J7b16cNrbH4M0rxYkeJ8a2/SuH9S8ynCZXJQlvYlyh17KLnfDG5JTKMOoGIjpgVBbZ+HHPPD1x8CcxROxFppeIDKHLVLozNCBPxhXfKB0ca0WgVy0EHsPvmm53AskaB1gyglb9J+r6ceMb0M5NeW75kSMqw0eBMca7M7TVd8RAi9t0t1PQbomqf54/EXgYPu03ZY7TOicVuJxR0eq8hALNcqP/1med/vuHDGnArefC40Iq/Ogaop+DIqKOscIvBvYap/jIgONrnZnGe5DSEUhKlEJPqDnk+X/ALBBGO52LCZD+kxFFJtl40rKndKcynlJVS+/4Taz3KsHeHeTDnKxqAARqQiLs7FLCmIZ2Rn/Sh6aHxRYR8JS2ZqlfK3TA4NXSMoeb1OVlgujy682HxR0ikPSYZHD9BefJjKLGl5bhsyCiPsc5jS0ZTpeZUmtaI8HEjXwQPsQz1uVkN832mQC+U8YKlLldsbtSKPwcjCxylj8xJ+FfZkk1iqu+jDsIEV8XGIAA=",
  "expiration": "2026-04-08T12:21:32Z",
  "region": "oss-cn-hangzhou",
  "bucket": "picset-ai-cn",
  "pathPrefix": ""
}
```


## 4. Leaked Server-Side AI Requests

PicSet stores the exact Gemini request in `payload.ai_request` of the `generation_jobs` row. This leaks when we poll the job row — giving us the EXACT prompt, model, config, and image references they send to Google.

### 4.1 `AI_WRITE` — model `gemini-3-flash-preview`, provider `google_direct`

**Config**: `temperature=0.4`, `maxOutputTokens=8192`, `responseMimeType=application/json`

**Provider meta**: source=`google_direct`, target_language=`en`, image_count=`6`
**Job fields**: gen_model=`basic`, gen_resolution=`1k`, gen_family=`nano_banana`, speed_mode=`normal`, workflow_mode=`None`
**Prompt config key**: `batch_detail_ai_write_prompt_zh`

**System prompt / first text part**:
```
你是电商产品详情图组的提示词生成助手。
用户会提供产品图片 + 简单文字描述。

重要规则：
1. 只识别和分析**产品本身**，完全忽略用户上传图片里的背景、场景、灯光、构图、模特、环境风格。
2. 不要被原图的场景影响，只根据产品属性和用户描述提炼信息。
3. 输出内容用于生成一组**风格统一、视觉连贯**的产品详情图。
4. 一次性生成 **3 套完整方案**（A/B/C），供用户三选一。产品客观事实一致，**场景设定、卖点表达、视觉风格、色彩方向**跟随各自风格统一调整。三套色彩必须有明显区分，且基于产品本身颜色材质，不可冲突。
5. 信息不足时写"未明确"，不编造。
6. **平台识别：** 如果用户输入中提及了目标平台（如"亚马逊""淘宝"等），在输出中填写"目标平台"字段；未提及则填"未明确"。
7. **用户需求原文处理：** 用户输入中能被结构化字段吸收的部分（如产品名称、平台、卖点等），正常提炼放进对应字段；无法被已有字段覆盖的部分（如特殊要求、额外说明、个性化描述等），原样保留写入"用户需求原文"。如果用户输入已全部被结构化字段覆盖，则"用户需求原文"填"无"。
8. 输出语言使用中文。

输出 options 数组，每个元素只有 prompt_text 一个字段，所有信息以 Markdown 格式写在其中（输出3个）：

{
  "options": [
    {
      "prompt_text": "**目标平台：** [平台名称 或 未明确]\n\n**风格名称：** [名称]\n\n## 视觉风格\n[风格描述一句话]\n\n## 整组图统一场景\n[整组详情图共用的场景（例如：运动，户外等）确保多张图视觉连贯]\n\n## 产品信息\n**产品名称：** [名称]\n\n**核心卖点：** [该风格调性的核心卖点]\n\n**适用人群：** [人群]\n\n## 产品参数\n[材质、尺寸、颜色、功能等客观信息]\n\n## 设计风格\n[视觉风格标签：简约/高级/清新/科技/国风/ins/日系/韩系/电商质感等]\n\n## 主题配色\n- **主色调：** [色彩名称] [#XXXXXX]（用于背景/大面积色块）\n- **辅助色：** [色彩名称] [#XXXXXX]（用于文字/装饰/图标）\n- **点缀色：** [色彩名称] [#XXXXXX]（用于高光/强调元素）\n\n## 用户需求原文\n[将用户的原始输入文字原样保留，不做任何修改、总结或省略]"
    }
  ]
}

主题配色选色规则：
- 主色调：该方案的主色调，用于背景/大面积色块
- 辅助色：辅助色，用于文字/装饰/图标
- 点缀色：点缀色，用于高光/强调元素
- 色值必须具体精确（如 #2F4F4F），禁止模糊描述
- 三个色之间须有层次对比，形成可用的配色方案
- 三套方案色彩必须有明显区分，且基于产品本身颜色材质，不可冲突

只输出纯 JSON，禁止 Markdown 代码块标签和任何前后解释文字。

```

**Other parts in order**:
- TEXT: This is product image 1 of 3:
- IMAGE URL (image/png): https://cdn.picsetai.cn/temp/b7cf84de-14de-4571-b2ca-a63b614e5b49/1775647293176_product_0.png
- TEXT: This is product image 2 of 3:
- IMAGE URL (image/png): https://cdn.picsetai.cn/temp/b7cf84de-14de-4571-b2ca-a63b614e5b49/1775647293197_product_1.png
- TEXT: This is product image 3 of 3:
- IMAGE URL (image/png): https://cdn.picsetai.cn/temp/b7cf84de-14de-4571-b2ca-a63b614e5b49/1775647293207_product_2.png

### 4.2 `ANALYSIS` — model `gemini-3-flash-preview`, provider `google_direct`

**Config**: `temperature=0.4`, `maxOutputTokens=8192`, `responseMimeType=application/json`

**Provider meta**: source=`google_direct`, target_language=`none`, image_count=`1`
**Job fields**: gen_model=`basic`, gen_resolution=`1k`, gen_family=`nano_banana`, speed_mode=`normal`, workflow_mode=`None`
**Prompt config key**: `batch_analysis_prompt_zh`

**System prompt / first text part**:
```
你是一位资深电商视觉策划专家，精通多品类产品的视觉设计规范制定。请务必为 **正好 1 张** 图片制定独立且互不重复的设计计划。

  你的任务是：
  1. 分析用户提供的产品图片。
  2. 判断产品是否为复杂品类。
  3. 结合用户的需求描述（特别注意用户是否要求"无文字/纯净版"设计）。
  4. 制定整体设计规范（design_specs）。
  5. 为每张图片制定详细的设计计划。

  ---
 复杂结构判断：产品符合以下任一条件即判定为 true：
  （1）含可折叠/伸缩/旋转的机械关节或活动部件
  （2）由多个独立零件组合，零件数量、位置、比例有明确物理约束
  （3）存在精密结构（螺纹、卡扣、铰链、导轨、齿轮等）

  若判定为 true，执行以下约束：

  1. 参考图视角分析：规划每张图前，先分析参考图中实际存在的拍摄角度，为每张图选定一个具体视角（正面、侧面、45度斜角、俯视或局部特写等），写入该图 design_content 的 **选用视角**字段。只能选用参考图中实际存在的角度；允许在已有视角基础上做局部特写放大，但不得改变拍摄方向。严禁：第一人称视角、使用者主观视角、透过产品任何部件的内视角、参考图中不存在的纵深透视构图。
  2. 产品形态锁定：形态、外形、颜色、材质、零件数量、连接关系、机械结构必须与参考图完全一致，不得改变。
  3. 创意边界：仅限场景选择、光影设计、背景氛围、装饰道具。

  若判定为 false：不执行上述任何约束，保持正常创意自由度。

  判断结果写入：① JSON 顶层字段 is_complex_product（布尔值，不加引号）；② 每张图 design_content 第一行 **产品复杂结构判定** 字段。  当is_complex_product 为 true 时，在 design_content 第二行写入 **选用视角**：[从参考图视角分析得出的视角]。
  ---
  其他逻辑规则：
  - 文案区分原则：区分"设计文案"（后期排版加入的标题/卖点）与"产品文字"（产品瓶身/包装上固有的 Logo、成分、标签）。
  - 无文案处理逻辑：若用户需求为"无文案"设计，则 文字内容 下的所有字段填入 "None"，并在 展示重点中强调"通过纯视觉、构图和光影展现产品，不添加任何排版文案"。design_specs 中的 ## 字体系统 部分必须输出为："无(纯视觉设计，不涉及排版文案)"，不提供具体的字体推荐。

  ---
  输出必须是严格的 JSON 格式，包含以下结构：

  {
    "is_complex_product":布尔值，根据复杂结构判断规则动态填写，true 或 false，不加引号,
    "design_specs": "（使用中文编写）# 整体设计规范\n\n> 所有图片必须遵循以下统一规范，确保视觉连贯性\n\n## 色彩系统\n-**主色调**：[根据产品分析确定]（所有图片的文字 and 装饰主色）\n- **辅助色**：[根据产品分析确定]（点缀和高光使用）\n-**背景色**：[根据产品分析确定]\n\n## 字体系统\n- **标题字体**：[推荐字体类型]\n- **正文字体**：[推荐字体类型]\n-**字号层级**：大标题:副标题:正文 = 3:1.8:1\n\n## 视觉语言\n- **装饰元素**：[根据产品类型推荐]\n- **图标风格**：[推荐风格]\n-**留白原则**：[具体说明]\n\n## 摄影风格\n- **光线**：[具体说明]\n- **景深**：[具体说明]\n- **相机参数参考**：[具体参数]\n\n## 品质要求\n-分辨率：4K/高清\n- 风格：专业产品摄影/商业广告级\n- 真实感：超写实/照片级",
    "images": [
      {
        "title": "[中文标题，简洁有力，4-8个字]",
        "description": "[中文描述，说明这张图的设计目标和定位，1-2句话]",
        "design_content": "**产品复杂结构判定**：[true/false]\n**选用视角**：[true 时填写从参考图分析选定的具体视角，如\"正侧面45度\"；false时删除此行]\n\n##图[N]：[图片类型]\n\n**设计目标**：[具体目标]\n\n**产品出现**：[是/否]\n\n**图中图元素**：\n-[如有，详细说明每个图中图的类型、形状、位置、尺寸、内容]\n\n**构图方案**：\n- 产品占比：[百分比]\n- 布局方式：[详细说明]\n-文字区域：[具体位置，若无文案则填写\"无文案区域\"]\n\n**内容要素**：\n- 展示重点：[具体说明]\n- 突出卖点：[具体卖点]\n- 背景元素：[详细描述]\n-装饰元素：[详细描述]\n\n**文字内容**（使用 无文字(纯视觉)）：\n- 主标题：[具体文字 / 若用户要求无文案则填 None]\n- 副标题：[具体文字 /若用户要求无文案则填 None]\n- 说明文字：[具体文字 / 若用户要求无文案则填 None]\n\n**氛围营造**：\n- 情绪关键词：[3-5个关键词]\n-光影效果：[详细说明]"
      }
    ]
  }

  重要规则：
  1. images 数组必须包含用户指定数量的元素。
  2. 每张图的设计内容必须独特，覆盖不同角度和场景。
  3. 设计规范必须基于产品图片的实际特征。
  4. design_content 中的文字内容必须使用目标输出语言：无文字(纯视觉)。
  5. 核心指令：整体设计规范 (design_specs)、图片计划中的 title 和 description 必须使用中文编写；只有 design_content中的"文字内容"部分必须根据目标输出语言 (无文字(纯视觉)) 编写。
  6. 输出限制：只输出纯 JSON 字符串，禁止包含任何 Markdown 代码块标签（如 ```json）、禁止包含任何前导或后置的解释性文字。确保 JSON 格式合法。
  7. is_complex_product 与每张图 design_content 第一行的 **产品复杂结构判定** 必须保持一致，均根据判断结果动态输出，不得写死。

用户需求描述：注意所有图片不要有设计文案**目标平台：** 未明确

**风格名称：** 优雅名媛风

## 视觉风格
极简高级感，通过柔和的自然光影突出皮革质感与金色拉链的精致细节。

## 整组图统一场景
高端大理石梳妆台，背景点缀丝绸衬布与少量高档香水瓶，营造精致生活的氛围。

## 产品信息
**产品名称：** A638 便携式首饰盒

**核心卖点：** 奢华质感，精致收纳，名媛气质必备。

**适用人群：** 都市白领、追求生活品质的女性。

## 产品参数
**材质：** 优质PU皮革、金属拉链、柔软植绒内里
**尺寸：** 8.5*8.5*5.5cm
**颜色：** 樱花粉、象牙白、薄荷绿、丁香紫
**功能：** 戒指槽、项链挂钩、多功能收纳格

## 设计风格
高级/简约/电商质感

## 主题配色
- **主色调：** 奶油杏色 [#F5F5DC]（用于大理石背景与阴影）
- **辅助色：** 香槟金 [#D4AF37]（用于文字标题与金属装饰）
- **点缀色：** 暖咖色 [#8B4513]（用于强调皮革缝线与图标）

## 用户需求原文
无
```

**Other parts in order**:
- TEXT: This is product image 1 of 3:
- IMAGE URL (image/png): https://cdn.picsetai.cn/temp/b7cf84de-14de-4571-b2ca-a63b614e5b49/1775647655401_product_0.png
- TEXT: This is product image 2 of 3:
- IMAGE URL (image/png): https://cdn.picsetai.cn/temp/b7cf84de-14de-4571-b2ca-a63b614e5b49/1775647655420_product_1.png
- TEXT: This is product image 3 of 3:
- IMAGE URL (image/png): https://cdn.picsetai.cn/temp/b7cf84de-14de-4571-b2ca-a63b614e5b49/1775647655433_product_2.png

## 5. Leaked Server-Side Responses (`result_data`)

The Gemini response is stored in `result_data`. This is the full output that PicSet displays in the UI.

### 5.AI_WRITE

**result_data**:
```json
{
  "_timing": {
    "total_ms": 14544,
    "queue_wait_ms": 0,
    "ai_call_total_ms": 14337,
    "config_refresh_ms": 0
  },
  "options": [
    {
      "prompt_text": "**目标平台：** 未明确\n\n**风格名称：** 优雅名媛风\n\n## 视觉风格\n极简高级感，通过柔和的自然光影突出皮革质感与金色拉链的精致细节。\n\n## 整组图统一场景\n高端大理石梳妆台，背景点缀丝绸衬布与少量高档香水瓶，营造精致生活的氛围。\n\n## 产品信息\n**产品名称：** A638 便携式首饰盒\n\n**核心卖点：** 奢华质感，精致收纳，名媛气质必备。\n\n**适用人群：** 都市白领、追求生活品质的女性。\n\n## 产品参数\n**材质：** 优质PU皮革、金属拉链、柔软植绒内里\n**尺寸：** 8.5*8.5*5.5cm\n**颜色：** 樱花粉、象牙白、薄荷绿、丁香紫\n**功能：** 戒指槽、项链挂钩、多功能收纳格\n\n## 设计风格\n高级/简约/电商质感\n\n## 主题配色\n- **主色调：** 奶油杏色 [#F5F5DC]（用于大理石背景与阴影）\n- **辅助色：** 香槟金 [#D4AF37]（用于文字标题与金属装饰）\n- **点缀色：** 暖咖色 [#8B4513]（用于强调皮革缝线与图标）\n\n## 用户需求原文\n无"
    },
    {
      "prompt_text": "**目标平台：** 未明确\n\n**风格名称：** 清新马卡龙风\n\n## 视觉风格\n色彩明快活泼，充满少女心，采用高调照明，视觉感受轻松愉悦。\n\n## 整组图统一场景\n阳光充足的卧室或旅行箱一角，搭配杂志、太阳镜与干花，强调“说走就走”的旅行便携感。\n\n## 产品信息\n**产品名称：** A638 迷你旅行首饰盒\n\n**核心卖点：** 小巧便携，马卡龙色系，旅行首饰不缠绕。\n\n**适用人群：** 学生、旅游爱好者、时尚达人。\n\n## 产品参数\n**材质：** 环保PU皮、双拉链设计\n**尺寸：** 8.5*8.5*5.5cm\n**颜色：** 多色可选（粉/白/绿/紫）\n**功能：** 分区收纳，保护珠宝防磨损\n\n## 设计风格\n清新/ins风/韩系\n\n## 主题配色\n- **主色调：** 樱花粉 [#FFC0CB]（用于背景色块与氛围营造）\n- **辅助色：** 纯白色 [#FFFFFF]（用于文字底色与边框）\n- **点缀色：** 薄荷绿 [#98FB98]（用于功能标注与重点提示）\n\n## 用户需求原文\n无"
    },
    {
      "prompt_text": "**目标平台：** 未明确\n\n**风格名称：** 现代极简收纳风\n\n## 视觉风格\n构图严谨对称，背景纯净，强调产品的几何美感与强大的内部收纳逻辑。\n\n## 整组图统一场景\n纯色几何空间，利用石膏几何体作为产品支撑，展现产品在不同角度下的形态。\n\n## 产品信息\n**产品名称：** A638 方形多功能首饰盒\n\n**核心卖点：** 科学分区，极致空间利用，简约而不简单。\n\n**适用人群：** 极简主义者、收纳控。\n\n## 产品参数\n**材质：** 耐磨PU材质、防锈五金\n**尺寸：** 8.5*8.5*5.5cm\n**颜色：** 莫兰迪色系\n**功能：** 戒指、耳钉、项链分类存放\n\n## 设计风格\n现代/科技感/简约\n\n## 主题配色\n- **主色调：** 丁香紫 [#E6E6FA]（用于背景渐变）\n- **辅助色：** 深岩灰 [#708090]（用于参数文字与线条）\n- **点缀色：** 极光银 [#C0C0C0]（用于高光位与金属质感表现）\n\n## 用户需求原文\n无"
    }
  ]
}
```

### 5.ANALYSIS

**result_data**:
```json
{
  "images": [
    {
      "title": "名媛私享·精致收纳",
      "description": "通过开启状态的45度视角，展示首饰盒内部精密的收纳结构与奢华植绒质感，营造名媛生活氛围。",
      "design_content": "**产品复杂结构判定**：true\n**选用视角**：45度斜角俯视（开启状态）\n\n##图1：场景展示图\n\n**设计目标**：通过纯视觉语言展现产品的收纳功能与材质高级感，无需任何文字辅助说明。\n\n**产品出现**：是\n\n**图中图元素**：\n-无\n\n**构图方案**：\n- 产品占比：45%\n- 布局方式：产品放置于画面中心偏右，呈开启状态，内部挂钩处挂有一条细珍珠项链，戒指槽内放置一枚金戒。\n-文字区域：无文案区域\n\n**内容要素**：\n- 展示重点：通过纯视觉、构图和光影展现产品，不添加任何排版文案。重点突出内部植绒的柔软感与金属拉链的色泽。\n- 突出卖点：内部多功能分区、优质PU皮革纹理、顺滑金属拉链。\n- 背景元素：浅色大理石台面，带有淡淡的石纹；背景左上角有一瓶半透明的香水瓶，处于虚化状态。\n-装饰元素：产品下方垫有一块香槟色丝绸，褶皱自然，增加画面的流动感。\n\n**文字内容**（使用 无文字(纯视觉)）：\n- 主标题：None\n- 副标题：None\n- 说明文字：None\n\n**氛围营造**：\n- 情绪关键词：优雅、静谧、奢华、纯净\n-光影效果：柔和的暖色调侧光，在丝绸和大理石上投射出柔和的阴影，强调皮革的立体缝线感。"
    }
  ],
  "_timing": {
    "total_ms": 12131,
    "queue_wait_ms": 0,
    "ai_call_total_ms": 11895,
    "ef_preprocess_ms": 38,
    "config_refresh_ms": 0
  },
  "design_specs": "# 整体设计规范\n\n> 所有图片必须遵循以下统一规范，确保视觉连贯性\n\n## 色彩系统\n-**主色调**：奶油杏色 [#F5F5DC]（用于大理石背景与环境光影）\n- **辅助色**：香槟金 [#D4AF37]（用于金属拉链的高光表现）\n-**背景色**：暖白色大理石纹理\n\n## 字体系统\n- 无(纯视觉设计，不涉及排版文案)\n\n## 视觉语言\n- **装饰元素**：真丝绸缎衬布、高档玻璃香水瓶、珍珠项链（作为道具放入盒内）\n- **图标风格**：无\n-**留白原则**：大面积留白，采用对角线构图，营造呼吸感与高级感\n\n## 摄影风格\n- **光线**：柔和侧逆光，模拟午后自然窗光，产生长投影\n- **景深**：浅景深，背景香水瓶适度虚化\n- **相机参数参考**：f/2.8, 1/125s, ISO 100, 85mm焦段\n\n## 品质要求\n-分辨率：4K/高清\n- 风格：专业产品摄影/商业广告级\n- 真实感：超写实/照片级",
  "is_complex_product": true
}
```

### 5.IMAGE_GEN

**Payload `prompts`** (this is the English expanded prompt from step 2):
```json
"Subject: A high-quality children's Spanish vocabulary workbook. 本图中的主体必须与参考图中的 [Spanish Vocabulary Workbook] 严格一致,产品的形态、外形、颜色、材质、零件数量、连接关系、机械结构必须与参考图完全一致，不得做任何改变。严格还原参考图中产品的所有色彩，不做任何修改。产品本体、各组件、表面及质感的颜色必须与参考图完全一致。 The workbook is shown open to an interior page featuring vibrant illustrations of vehicles and words such as 'autobús' and 'miniván' with clear red tracing lines for handwriting practice. Composition: The composition uses a 45-degree top-down diagonal view, with the workbook occupying approximately 65% of the frame. The layout is balanced with 20%-30% negative space around the product to emphasize its slim and portable nature. Background: The scene is set on a light wood-grained desktop. In the foreground, a red children's pencil rests against the edge of the book, accompanied by two scattered colorful wooden blocks. The midground features the open workbook lying perfectly flat. In the background, the top-right corner reveals a partial view of a pencil holder filled with various colored pencils, slightly blurred to create depth. Lighting: Soft, natural morning light streams in from the top-left corner, casting gentle, subtle shadows to the right of the workbook, creating a three-dimensional effect and a serene atmosphere. Color Scheme: The palette is dominated by bright sky blue (#00AEEF) and vibrant lemon yellow (#FFF200), accented by candy pink and grass green decorative elements, all set against the light wood and rice white tones of the desk. Material Details: The workbook features a saddle-stitched binding that allows it to lay 180 degrees flat. The paper has a thick, premium matte texture that prevents ink bleeding, with clearly visible dotted tracing lines. Atmosphere: The mood is warm, focused, educational, and tidy, evoking a sense of happy learning during a quiet afternoon. Style: Professional commercial product photography with a clean, modern aesthetic. Quality: 4K resolution, shot with a 35mm-50mm lens at f/4.0 and ISO 100. 颜色保真：必须生成参考图中颜色的产品。结构保真度：严格复制参考图中产品的精确物理结构，匹配所有组件的精确数量、位置、比例和空间关系，每个元素必须在几何上精确且在现实世界中物理可实现，不得添加、移除、合并或变形任何结构元素。"
```

**result_data**:
```json
{
  "_timing": {
    "ai_model": "unknown",
    "total_ms": 33819,
    "ai_provider": "unknown",
    "api_call_ms": 33252,
    "oss_upload_ms": 280,
    "queue_wait_ms": 0,
    "provider_chain": [
      {
        "ms": 33525,
        "ok": true,
        "provider": "apiyi"
      }
    ],
    "ai_call_total_ms": 33528,
    "ef_preprocess_ms": 43,
    "config_refresh_ms": 0,
    "image_download_ms": 259,
    "response_parse_ms": 12,
    "image_download_count": 1
  },
  "oss_url": "https://cdn.picsetai.cn/generations/b7cf84de-14de-4571-b2ca-a63b614e5b49/1775648532_e0f29c5a.jpg",
  "oss_path": "generations/b7cf84de-14de-4571-b2ca-a63b614e5b49/1775648532_e0f29c5a.jpg",
  "thumbnail_url": "https://cdn.picsetai.cn/generations/b7cf84de-14de-4571-b2ca-a63b614e5b49/1775648532_e0f29c5a_thumb.webp",
  "image_mime_type": "image/jpeg"
}
```

## 6. `ANALYSIS` Job Payload (client → server input for step 1)

### 4b553315… — image_count=`1`, target_lang=`none`

```json
{
  "trace_id": "1f4ae94a-5689-4c8c-9f84-ce74da6decc7",
  "imageType": "detail",
  "imageCount": 1,
  "project_id": "572820ad-3ea8-484b-955b-37afae21d780",
  "uiLanguage": "zh-CN",
  "productImage": "temp/b7cf84de-14de-4571-b2ca-a63b614e5b49/1775647655401_product_0.png",
  "requirements": "注意所有图片不要有设计文案**目标平台：** 未明确\n\n**风格名称：** 优雅名媛风\n\n## 视觉风格\n极简高级感，通过柔和的自然光影突出皮革质感与金色拉链的精致细节。\n\n## 整组图统一场景\n高端大理石梳妆台，背景点缀丝绸衬布与少量高档香水瓶，营造精致生活的氛围。\n\n## 产品信息\n**产品名称：** A638 便携式首饰盒\n\n**核心卖点：** 奢华质感，精致收纳，名媛气质必备。\n\n**适用人群：** 都市白领、追求生活品质的女性。\n\n## 产品参数\n**材质：** 优质PU皮革、金属拉链、柔软植绒内里\n**尺寸：** 8.5*8.5*5.5cm\n**颜色：** 樱花粉、象牙白、薄荷绿、丁香紫\n**功能：** 戒指槽、项链挂钩、多功能收纳格\n\n## 设计风格\n高级/简约/电商质感\n\n## 主题配色\n- **主色调：** 奶油杏色 [#F5F5DC]（用于大理石背景与阴影）\n- **辅助色：** 香槟金 [#D4AF37]（用于文字标题与金属装饰）\n- **点缀色：** 暖咖色 [#8B4513]（用于强调皮革缝线与图标）\n\n## 用户需求原文\n无",
  "productImages": [
    "temp/b7cf84de-14de-4571-b2ca-a63b614e5b49/1775647655401_product_0.png",
    "temp/b7cf84de-14de-4571-b2ca-a63b614e5b49/1775647655420_product_1.png",
    "temp/b7cf84de-14de-4571-b2ca-a63b614e5b49/1775647655433_product_2.png"
  ],
  "targetLanguage": "none",
  "promptConfigKey": "batch_analysis_prompt_zh",
  "_ef_preprocess_ms": 38
}
```

### 6d2fe6a3… — image_count=`1`, target_lang=`none`

```json
{
  "trace_id": "3a673927-3fd2-4649-ac4d-74bcb6a3d7f2",
  "imageType": "detail",
  "imageCount": 1,
  "project_id": "e6a544b2-b4e3-4c9c-86db-c2c415c80b86",
  "uiLanguage": "zh-CN",
  "themeColors": null,
  "productImage": "temp/b7cf84de-14de-4571-b2ca-a63b614e5b49/1775648384210_product_0.png",
  "requirements": "注意所有图片不要有设计文案儿童西班牙语描红练习册，骑马钉装订薄册子。目标平台MercadoLibre墨西哥。",
  "productImages": [
    "temp/b7cf84de-14de-4571-b2ca-a63b614e5b49/1775648384210_product_0.png"
  ],
  "targetLanguage": "none",
  "promptConfigKey": "batch_analysis_prompt_zh",
  "_ef_preprocess_ms": 44
}
```

### e199520e… — image_count=`1`, target_lang=`es`

```json
{
  "trace_id": "7e5a0990-2141-4296-a555-10df08e0dcce",
  "imageType": "detail",
  "imageCount": 1,
  "project_id": "c1599af8-dbaa-4dbe-874f-b2d6dbd19df5",
  "uiLanguage": "zh-CN",
  "themeColors": null,
  "productImage": "temp/b7cf84de-14de-4571-b2ca-a63b614e5b49/1775649149614_product_0.png",
  "requirements": "儿童西班牙语描红练习册，骑马钉装订薄册子。目标平台MercadoLibre墨西哥。",
  "productImages": [
    "temp/b7cf84de-14de-4571-b2ca-a63b614e5b49/1775649149614_product_0.png"
  ],
  "targetLanguage": "es",
  "promptConfigKey": "batch_analysis_prompt_zh",
  "_ef_preprocess_ms": 43
}
```

## 7. `IMAGE_GEN` Full Payload

### Job `7f6ae5a2…`

Fields: `gen_model=pro`, `gen_resolution=2k`, `gen_family=nano_banana`, `speed_mode=normal`, `workflow_mode=None`

**Payload (excluding ai_request)**:
```json
{
  "model": "nano-banana-pro",
  "prompt": "Subject: A high-quality children's Spanish vocabulary workbook. 本图中的主体必须与参考图中的 [Spanish Vocabulary Workbook] 严格一致,产品的形态、外形、颜色、材质、零件数量、连接关系、机械结构必须与参考图完全一致，不得做任何改变。严格还原参考图中产品的所有色彩，不做任何修改。产品本体、各组件、表面及质感的颜色必须与参考图完全一致。 The workbook is shown open to an interior page featuring vibrant illustrations of vehicles and words such as 'autobús' and 'miniván' with clear red tracing lines for handwriting practice. Composition: The composition uses a 45-degree top-down diagonal view, with the workbook occupying approximately 65% of the frame. The layout is balanced with 20%-30% negative space around the product to emphasize its slim and portable nature. Background: The scene is set on a light wood-grained desktop. In the foreground, a red children's pencil rests against the edge of the book, accompanied by two scattered colorful wooden blocks. The midground features the open workbook lying perfectly flat. In the background, the top-right corner reveals a partial view of a pencil holder filled with various colored pencils, slightly blurred to create depth. Lighting: Soft, natural morning light streams in from the top-left corner, casting gentle, subtle shadows to the right of the workbook, creating a three-dimensional effect and a serene atmosphere. Color Scheme: The palette is dominated by bright sky blue (#00AEEF) and vibrant lemon yellow (#FFF200), accented by candy pink and grass green decorative elements, all set against the light wood and rice white tones of the desk. Material Details: The workbook features a saddle-stitched binding that allows it to lay 180 degrees flat. The paper has a thick, premium matte texture that prevents ink bleeding, with clearly visible dotted tracing lines. Atmosphere: The mood is warm, focused, educational, and tidy, evoking a sense of happy learning during a quiet afternoon. Style: Professional commercial product photography with a clean, modern aesthetic. Quality: 4K resolution, shot with a 35mm-50mm lens at f/4.0 and ISO 100. 颜色保真：必须生成参考图中颜色的产品。结构保真度：严格复制参考图中产品的精确物理结构，匹配所有组件的精确数量、位置、比例和空间关系，每个元素必须在几何上精确且在现实世界中物理可实现，不得添加、移除、合并或变形任何结构元素。",
  "metadata": {
    "is_batch": true,
    "image_size": "2K",
    "batch_index": 0,
    "product_images": [
      "temp/b7cf84de-14de-4571-b2ca-a63b614e5b49/1775648384210_product_0.png"
    ]
  },
  "trace_id": "3a673927-3fd2-4649-ac4d-74bcb6a3d7f2",
  "imageSize": "2K",
  "imageType": "detail",
  "speedMode": "normal",
  "fe_attempt": 1,
  "imageCount": 1,
  "project_id": "e6a544b2-b4e3-4c9c-86db-c2c415c80b86",
  "aspectRatio": "3:4",
  "productImage": "temp/b7cf84de-14de-4571-b2ca-a63b614e5b49/1775648384210_product_0.png",
  "turboEnabled": false,
  "client_job_id": "3a673927-3fd2-4649-ac4d-74bcb6a3d7f2-0",
  "productImages": [
    "temp/b7cf84de-14de-4571-b2ca-a63b614e5b49/1775648384210_product_0.png"
  ],
  "isNewUserTrial": true,
  "_ef_preprocess_ms": 43
}
```

### Job `cb11fcae…`

Fields: `gen_model=pro`, `gen_resolution=2k`, `gen_family=nano_banana`, `speed_mode=normal`, `workflow_mode=None`

**Payload (excluding ai_request)**:
```json
{
  "model": "nano-banana-pro",
  "prompt": "Subject: 本图中的主体必须与参考图中的 [Libro de Trazos: Primeras Palabras] 严格一致,产品的形态、外形、颜色、材质、零件数量、连接关系、机械结构必须与参考图完全一致，不得做任何改变。严格还原参考图中产品的所有色彩，不做任何修改。产品本体、各组件、表面及质感的颜色必须与参考图完全一致。This educational tracing book set features a vibrant cover with a cute little girl illustration and clear interior pages showing Spanish word tracing paths and colorful illustrations. Composition: The product occupies 75% of the frame. It uses a split-screen layout where the cover is on the left, slightly tilted to create a sense of motion, and the interior pages are spread flat on the right to show detail. A stack of 12 miniature books is positioned at the bottom to emphasize the set. The main title is centered at the top, and a specification label is in the bottom right. Background: A multi-layered depth with a foreground of scattered colored pencils. The midground features the books on a clean surface. The background is a soft light blue gradient (#00AEEF) decorated with subtle, elegant watermarks of stationery like rulers and erasers. Lighting: Bright natural light simulation, using a top softbox to create gentle illumination and soft shadows that enhance the 3D volume of the books without harsh reflections. Color Scheme: Dominant Sky Blue (#00AEEF), Vibrant Pink (#E91E63), Bright Yellow, and Pure White. Material Details: High-definition paper texture with visible fiber, matte finish to prevent glare, clear saddle-stitch binding, and sharp, saturated ink printing for the illustrations. Text Layout: The top center features 'Libro de Trazos: Primeras Palabras'. Below it is '¡Aprender a escribir es divertido y fácil!'. In the bottom right corner, 'Letra Grande | Tamaño 19x26cm | Pack de 12 unidades' is displayed clearly using a rounded sans-serif font. Inset Images: A circular magnifying glass icon is placed on the upper right, pointing towards the large tracing letters to highlight the 'Letra Grande' feature. Atmosphere: Fun, educational, professional, and clear. Style: Professional educational product photography, commercial advertising grade, ultra-realistic. Quality: 4K resolution, f/8.0, 1/125s, ISO 100. Color fidelity: Must generate the product in the colors of the reference image. Structural fidelity: Strictly copy the exact physical structure of the product in the reference image, matching all components' precise numbers, positions, proportions, and spatial relationships; every element must be geometrically precise and physically realizable, without adding, removing, merging, or deforming any structural elements.",
  "metadata": {
    "is_batch": true,
    "image_size": "2K",
    "batch_index": 0,
    "product_images": [
      "temp/b7cf84de-14de-4571-b2ca-a63b614e5b49/1775649149614_product_0.png"
    ]
  },
  "trace_id": "7e5a0990-2141-4296-a555-10df08e0dcce",
  "imageSize": "2K",
  "imageType": "detail",
  "speedMode": "normal",
  "fe_attempt": 1,
  "imageCount": 1,
  "project_id": "c1599af8-dbaa-4dbe-874f-b2d6dbd19df5",
  "aspectRatio": "3:4",
  "productImage": "temp/b7cf84de-14de-4571-b2ca-a63b614e5b49/1775649149614_product_0.png",
  "turboEnabled": false,
  "client_job_id": "7e5a0990-2141-4296-a555-10df08e0dcce-0",
  "productImages": [
    "temp/b7cf84de-14de-4571-b2ca-a63b614e5b49/1775649149614_product_0.png"
  ],
  "isNewUserTrial": true,
  "_ef_preprocess_ms": 43
}
```

## 8. `generate-prompts-v2` SSE Streams (the HIDDEN step)

This endpoint does not write a `generation_jobs` row with an `ai_request` field — it just streams SSE directly back. So we only see the OUTPUT (the expanded English prompts), not PicSet's server-side prompt that produced them. To get PicSet's expansion prompt, we would need prompt injection or bundled JS inspection.

2 SSE call(s) captured

### SSE Call 1 (src=`picset-capture-2.json`)

**Client → server request**:
```json
{
  "analysisJson": {
    "images": [
      {
        "title": "沉浸式学习场景展示",
        "description": "通过模拟真实的儿童书桌学习场景，展示练习册的内页细节与骑马钉装订的平摊效果，激发购买欲望。",
        "design_content": "**产品复杂结构判定**：false\n\n##图1：场景化展示图\n\n**设计目标**：展现产品在实际使用中的状态，强调内页的易写性和内容的丰富度。\n\n**产品出现**：是\n\n**图中图元素**：\n-无\n\n**构图方案**：\n- 产品占比：65%\n- 布局方式：采用45度俯视斜向构图。练习册呈自然翻开状态，平铺在浅色木质书桌上，展示出含有“autobús”、“miniván”等单词的内页。\n-文字区域：无文案区域\n\n**内容要素**：\n- 展示重点：通过纯视觉、构图和光影展现产品，不添加任何排版文案。重点展示内页清晰的描红虚线和鲜艳的配图。\n- 突出卖点：骑马钉装订可180度平摊，方便儿童书写；纸张质感厚实不洇墨。\n- 背景元素：浅色木纹桌面，右上角露出半个盛放彩色铅笔的笔筒。\n-装饰元素：一支红色的儿童铅笔斜靠在练习册边缘，旁边散落两块彩色积木，增加生活气息。\n\n**文字内容**（使用 无文字(纯视觉)）：\n- 主标题：None\n- 副标题：None\n- 说明文字：None\n\n**氛围营造**：\n- 情绪关键词：温馨、专注、教育、快乐、整洁\n-光影效果：左上角投射进柔和的晨光，在练习册右侧形成淡淡的投影，营造出静谧的学习午后感。"
      }
    ],
    "_timing": {
      "total_ms": 20934,
      "queue_wait_ms": 0,
      "ai_call_total_ms": 20741,
      "ef_preprocess_ms": 44,
      "config_refresh_ms": 2
    },
    "design_specs": "# 整体设计规范\n\n> 所有图片必须遵循以下统一规范，确保视觉连贯性\n\n## 色彩系统\n-**主色调**：明亮天蓝色（#00AEEF）与活力柠檬黄（#FFF200），呼应封面插画色调，营造积极的学习氛围。\n- **辅助色**：糖果粉与草绿色，用于背景装饰元素，增加画面的趣味性。\n-**背景色**：浅原木色或纯净米白色，模拟真实的儿童书桌场景。\n\n## 字体系统\n- **标题字体**：无(纯视觉设计，不涉及排版文案)\n- **正文字体**：无(纯视觉设计，不涉及排版文案)\n-**字号层级**：无(纯视觉设计，不涉及排版文案)\n\n## 视觉语言\n- **装饰元素**：彩色铅笔、蜡笔、卡通造型的卷笔刀、木质积木，增加教育属性。\n- **图标风格**：无排版图标，仅保留产品本身的插画风格。\n-**留白原则**：采用呼吸感构图，产品周围保持20%-30%的留白，避免视觉拥挤，突出练习册的轻薄便携。\n\n## 摄影风格\n- **光线**：模拟柔和的自然窗光，带有淡淡的阴影，增强立体感。\n- **景深**：中等景深，使产品主体清晰，背景装饰物略微虚化。\n- **相机参数参考**：镜头35mm-50mm，光圈f/4.0，ISO 100。\n\n## 品质要求\n-分辨率：4K/高清\n- 风格：专业产品摄影/商业广告级\n- 真实感：超写实/照片级",
    "is_complex_product": false
  },
  "targetLanguage": "none",
  "imageType": "detail",
  "stream": true,
  "trace_id": "3a673927-3fd2-4649-ac4d-74bcb6a3d7f2",
  "project_id": "e6a544b2-b4e3-4c9c-86db-c2c415c80b86"
}
```

_fullText parse failed, raw:_
```
[
  {
    "prompt": "Subject: A high-quality children's Spanish vocabulary workbook. 本图中的主体必须与参考图中的 [Spanish Vocabulary Workbook] 严格一致,产品的形态、外形、颜色、材质、零件数量、连接关系、机械结构必须与参考图完全一致，不得做任何改变。严格还原参考图中产品的所有色彩，不做任何修改。产品本体、各组件、表面及质感的颜色必须与参考图完全一致。 The workbook is shown open to an interior page featuring vibrant illustrations of vehicles and words such as 'autobús' and 'miniván' with clear red tracing lines for handwriting practice. Composition: The composition uses a 45-degree top-down diagonal view, with the workbook occupying approximately 65% of the frame. The layout is balanced with 20%-30% negative space around the product to emphasize its slim and portable nature. Background: The scene is set on a light wood-grained desktop. In the foreground, a red children's pencil rests against the edge of the book, accompanied by two scattered colorful wooden blocks. The midground features the open workbook lying perfectly flat. In the background, the top-right corner reveals a partial view of a pencil holder filled with various colored pencils, slightly blurred to create depth. Lighting: Soft, natural morning light streams in from the top-left corner, casting gentle, subtle shadows to the right of the workbook, creating a three-dimensional effect and a serene atmosphere. Color Scheme: The palette is dominated by bright sky blue (#00AEEF) and vibrant lemon yellow (#FFF
```

### SSE Call 2 (src=`picset-capture-2.json`)

**Client → server request**:
```json
{
  "analysisJson": {
    "images": [
      {
        "title": "核心卖点综合展示图",
        "description": "通过封面与内页的组合展示，直观体现产品的大尺寸特征、清晰的描红设计以及12本装的规格优势。",
        "design_content": "**产品复杂结构判定**：false\n\n##图1：综合功能主图\n\n**设计目标**：在MercadoLibre搜索结果中脱颖而出，快速传达产品核心价值。\n\n**产品出现**：是\n\n**图中图元素**：\n- [左侧：产品封面图，展示可爱的小女孩插画和主标题]\n- [右侧：内页展开图，展示清晰的单词描红区域和对应的彩色插图]\n- [底部：12本练习册堆叠的微缩图，强调套装属性]\n\n**构图方案**：\n- 产品占比：75%\n- 布局方式：左右对开构图，封面位于左侧并略微倾斜以增加动感，内页位于右侧平铺展示细节。\n- 文字区域：顶部居中放置主标题，右下角放置规格标签。\n\n**内容要素**：\n- 展示重点：大字号描红路径、标准的西班牙语单词、丰富的彩色插图。\n- 突出卖点：适合3岁以上儿童、19x26cm大尺寸、骑马钉装订易于平铺。\n- 背景元素：浅蓝色渐变背景，带有淡雅的文具（如尺子、橡皮）水印装饰。\n- 装饰元素：彩色铅笔散落在产品周围，右上角添加一个“放大镜”图标指向内页文字，强调“Letra Grande”。\n\n**文字内容**（使用 西班牙语）：\n- 主标题：Libro de Trazos: Primeras Palabras\n- 副标题：¡Aprender a escribir es divertido y fácil!\n- 说明文字：Letra Grande | Tamaño 19x26cm | Pack de 12 unidades\n\n**氛围营造**：\n- 情绪关键词：趣味、教育、专业、清晰\n- 光影效果：明亮的顶部柔光，为练习册边缘添加轻微的投影，增强立体感。"
      }
    ],
    "_timing": {
      "total_ms": 18416,
      "queue_wait_ms": 0,
      "ai_call_total_ms": 18343,
      "ef_preprocess_ms": 43,
      "config_refresh_ms": 0
    },
    "design_specs": "# 整体设计规范\n\n> 所有图片必须遵循以下统一规范，确保视觉连贯性\n\n## 色彩系统\n- **主色调**：天空蓝（#00AEEF，呼应品牌Logo与底部色块）\n- **辅助色**：活力粉（#E91E63，呼应封面标题）与明黄色（增加儿童产品的趣味感）\n- **背景色**：纯净白或极浅灰，营造整洁、专业的教育氛围\n\n## 字体系统\n- **标题字体**：圆润、亲和力强的无衬线体（如 Quicksand Bold 或 Montserrat Alternates）\n- **正文字体**：清晰易读的幼教风格字体（如 Varela Round）\n- **字号层级**：大标题:副标题:正文 = 3:1.8:1\n\n## 视觉语言\n- **装饰元素**：彩色铅笔、星星奖章、手绘风格的小插画、纸张纹理\n- **图标风格**：扁平化、高对比度、圆角风格图标\n- **留白原则**：保持 20% 以上的边缘留白，确保视觉呼吸感，重点突出产品本身\n\n## 摄影风格\n- **光线**：明亮的自然光感，柔和阴影，避免强反光，模拟教室或书桌环境\n- **景深**：微距展示内页纹理，整体展示保持全焦清晰\n- **相机参数参考**：f/8.0, 1/125s, ISO 100\n\n## 品质要求\n- 分辨率：4K/高清\n- 风格：专业教育产品摄影/商业广告级\n- 真实感：超写实，完美还原纸张质感与印刷色彩",
    "is_complex_product": false
  },
  "targetLanguage": "es",
  "imageType": "detail",
  "stream": true,
  "trace_id": "7e5a0990-2141-4296-a555-10df08e0dcce",
  "project_id": "c1599af8-dbaa-4dbe-874f-b2d6dbd19df5"
}
```

_fullText parse failed, raw:_
```
[
  {
    "prompt": "Subject: 本图中的主体必须与参考图中的 [Libro de Trazos: Primeras Palabras] 严格一致,产品的形态、外形、颜色、材质、零件数量、连接关系、机械结构必须与参考图完全一致，不得做任何改变。严格还原参考图中产品的所有色彩，不做任何修改。产品本体、各组件、表面及质感的颜色必须与参考图完全一致。This educational tracing book set features a vibrant cover with a cute little girl illustration and clear interior pages showing Spanish word tracing paths and colorful illustrations. Composition: The product occupies 75% of the frame. It uses a split-screen layout where the cover is on the left, slightly tilted to create a sense of motion, and the interior pages are spread flat on the right to show detail. A stack of 12 miniature books is positioned at the bottom to emphasize the set. The main title is centered at the top, and a specification label is in the bottom right. Background: A multi-layered depth with a foreground of scattered colored pencils. The midground features the books on a clean surface. The background is a soft light blue gradient (#00AEEF) decorated with subtle, elegant watermarks of stationery like rulers and erasers. Lighting: Bright natural light simulation, using a top softbox to create gentle illumination and soft shadows that enhance the 3D volume of the books without harsh reflections. Color Scheme: Dominant Sky Blue (#00AEEF), Vibrant Pink (#E91E63), Bright Yellow, and
```
