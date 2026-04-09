# -*- coding: utf-8 -*-
"""Pipeline configuration — language maps, defaults, model mapping."""

# PicSet's targetLanguage code → Chinese display name (used in prompt templating)
LANG_MAP = {
    'none': '无文字(纯视觉)',
    'zh-CN': '中文(简体)',
    'zh-TW': '中文(繁体)',
    'en': '英语',
    'ja': '日语',
    'ko': '韩语',
    'de': '德语',
    'fr': '法语',
    'ar': '阿拉伯语',
    'ru': '俄语',
    'th': '泰语',
    'id': '印尼语',
    'vi': '越南语',
    'ms': '马来语',
    'es': '西班牙语',
    'pt': '葡萄牙语',
    'pt-BR': '巴西葡萄牙语',
    'ro': '罗马尼亚语',
}

DEFAULTS = {
    'image_type': 'detail',      # 'detail' or 'main'
    'image_count': 8,
    'target_language': 'none',
    'aspect_ratio': '3:4',
    'image_size': '2K',
    'speed_mode': 'normal',
}

# When targetLanguage is 'none', prepend this to requirements
NO_TEXT_PREFIX = '注意所有图片不要有设计文案'
