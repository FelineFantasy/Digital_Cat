"""Модуль случайных событий."""
import random


def random_event(cat):
    """Обрабатывает случайные события. Возвращает список сообщений."""
    messages = []

    # Голод со временем
    if random.random() < 0.1:
        cat["satiety"] -= 3
        cat["happiness"] -= 1
        cat["energy"] -= 1

    # Грязный лоток влияет на статы
    if cat["dirty_tray"]:
        cat["happiness"] -= 2
        cat["health"] -= 1

    # Случайные события
    if random.random() < 0.15:
        event = random.randint(1, 4)
        if event == 1:
            messages.append(f"{cat['name']} мяукнул.")
        elif event == 2 and not cat["dirty_tray"]:
            cat["dirty_tray"] = True
            messages.append(f"{cat['name']} сходил в лоток!")
        elif event == 3:
            found = random.randint(1, 5)
            cat["money"] += found
            messages.append(f"{cat['name']} нашёл {found} монеты!")
        elif event == 4:
            messages.append(f"{cat['name']} бегает по комнате!")

    return messages
