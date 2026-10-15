import random
from typing import Optional


SYSTEM_TEMPLATES = {
    "praise": [
        "Makasih banyak ya",
        "Terima kasih atas apresiasinya",
        "Senang kamu suka",
        "Thanks for the support",
        "Glad you like it",
        "Apresiasi banget",
        "Mantap, terima kasih",
        "Thank you so much",
    ],
    "neutral": [
        "Halo juga",
        "Hai, apa kabar",
        "Hi there",
        "Halo, senang bertemu",
        "Welcome",
        "Selamat datang",
        "Halo, ada yang bisa dibantu",
        "Terima kasih atas komentarnya",
        "Thanks for stopping by",
        "Noted, terima kasih",
        "Thank you for the comment",
        "Appreciate the comment",
    ],
}

# Kategori ini selalu butuh LLM, tidak bisa pakai template custom
LLM_ONLY_CATEGORIES = {"question"}


def get_category_config(rules: dict, category: str) -> dict:
    """
    Ambil config untuk kategori tertentu dari rules JSONB.
    Default: enabled=True, templates=[]
    """
    if not rules or not isinstance(rules, dict):
        return {"enabled": True, "templates": []}
    cat_rules = rules.get(category)
    if not isinstance(cat_rules, dict):
        return {"enabled": True, "templates": []}
    return {
        "enabled": cat_rules.get("enabled", True),
        "templates": cat_rules.get("templates", []) or [],
    }


def is_category_enabled(rules: dict, category: str) -> bool:
    return get_category_config(rules, category)["enabled"]


def pick_template(category: str, custom_templates: list = None) -> str:
    pool = []
    if custom_templates:
        pool = [t for t in custom_templates if t and t.strip()]
    if not pool:
        pool = SYSTEM_TEMPLATES.get(category, [])
    if not pool:
        return ""
    return random.choice(pool)


def has_template(category: str, custom_templates: list = None) -> bool:
    if custom_templates and any(t and t.strip() for t in custom_templates):
        return True
    return bool(SYSTEM_TEMPLATES.get(category))


def get_custom_templates(rules: dict, category: str) -> list:
    return get_category_config(rules, category)["templates"]


# Kategori yang bisa dikonfigurasi user di Settings
USER_CONFIGURABLE_CATEGORIES = ["praise", "neutral", "question", "spam", "toxic"]
