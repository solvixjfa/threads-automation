import random


# Template default untuk sistem. Tidak ada emoticon, em dash, atau tanda kutip.
# User bisa override lewat settings nanti, tapi MVP pakai system default dulu.

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
    "greeting": [
        "Halo juga",
        "Hai, apa kabar",
        "Hi there",
        "Halo, senang bertemu",
        "Welcome",
        "Selamat datang",
        "Halo, ada yang bisa dibantu",
        "Hi, nice to see you",
    ],
    "other": [
        "Terima kasih atas komentarnya",
        "Thanks for stopping by",
        "Noted, terima kasih",
        "Thank you for the comment",
        "Makasih ya",
        "Appreciate the comment",
        "Terima kasih",
        "Thanks",
    ],
    # Question dan lead sengaja kosong
    # Dua kategori ini butuh LLM karena harus baca konteks brand_knowledge
}


def pick_template(category: str, custom_templates: list = None) -> str:
    """
    Ambil satu template random untuk kategori tertentu.
    Prioritas: custom templates user, kalau kosong baru pakai system default.
    """
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
