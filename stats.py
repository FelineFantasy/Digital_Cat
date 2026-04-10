"""Утилиты для работы со статами кота."""


def clamp(value, min_val=0, max_val=100):
    """Ограничивает значение диапазоном [min_val, max_val]."""
    return max(min_val, min(value, max_val))


def update_stats(cat):
    """Обновляет все статы кота, ограничивая их диапазоном."""
    cat["satiety"] = clamp(cat["satiety"])
    cat["happiness"] = clamp(cat["happiness"])
    cat["energy"] = clamp(cat["energy"])
    cat["health"] = clamp(cat["health"])
    cat["love"] = clamp(cat["love"])
