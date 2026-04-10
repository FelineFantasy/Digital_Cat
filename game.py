"""Основной игровой цикл."""
from events import random_event
from actions import feed, pet, play, clean_tray, sleep, go_outside, work
from shop import show_menu as shop_menu
from vet import show_menu as vet_menu
from admin import show_menu as admin_menu
from stats import update_stats


def create_cat(name):
    """Создаёт кота как словарь."""
    return {
        "name": name,
        "satiety": 50,
        "happiness": 50,
        "energy": 70,
        "health": 100,
        "day": 1,
        "money": 100,
        "love": 50,
        "is_alive": True,
        "dirty_tray": False,
        "day_phase": "день",
    }


def is_alive(cat):
    """Проверяет, жив ли кот."""
    if cat["health"] <= 0 or cat["satiety"] <= 0 or cat["happiness"] <= 0:
        cat["is_alive"] = False
        print("=" * 50)
        print(f"{cat['name']} умер...")
        print(f"Игра длилась {cat['day']} дней")
        return False
    return True


def show_stats(cat):
    """Показать статистику кота."""
    print("=" * 50)
    print("Статистика кота")
    print("=" * 50)
    print(f"Имя кота: {cat['name']}")
    print(f"Сытость: {cat['satiety']}")
    print(f"Счастье: {cat['happiness']}")
    print(f"Энергия: {cat['energy']}")
    print(f"Здоровье: {cat['health']}")
    print(f"Монет: {cat['money']}")
    print(f"Любовь: {cat['love']}")
    print(f"Дней в игре: {cat['day']}")
    print(f"Фаза дня: {cat['day_phase']}")
    print(f"Лоток грязный: {cat['dirty_tray']}")


# Маппинг действий
ACTIONS = {
    "0": lambda c: False,           # выход
    "1": feed,
    "2": pet,
    "3": play,
    "4": clean_tray,
    "5": sleep,
    "6": shop_menu,
    "7": go_outside,
    "8": work,
    "9": vet_menu,
    "10": show_stats,
}


def main():
    """Основной игровой цикл."""
    print("Привет! Ты попал в игру Digital Cat.")
    print("=" * 50)
    name = input("Для начала придумай имя своему питомцу: ")
    print("Отличный выбор!")

    cat = create_cat(name)

    menu_text = "\n".join([
        "=" * 50,
        "0. Выйти из игры",
        "1. Покормить кота",
        "2. Погладить кота",
        "3. Поиграть с котом",
        "4. Убрать за котом",
        "5. Уложить кота спать",
        "6. Сходить в зоомагазин",
        "7. Выпустить кота на улицу",
        "8. Заработать монеты",
        "9. Сходить к ветеринару",
        "10. Статистика кота",
    ])

    while cat["is_alive"]:
        # Случайные события
        messages = random_event(cat)
        for msg in messages:
            print("=" * 50)
            print(msg)

        update_stats(cat)

        if not is_alive(cat):
            break

        # Меню
        print(menu_text)
        choice = input("Выберите действие от 0 до 10: ")

        action = ACTIONS.get(choice)
        if action is None:
            print("=" * 50)
            print("Введите число от 0 до 10")
        elif choice == "0":
            break
        else:
            action(cat)

        update_stats(cat)

        # Секретное админ-меню
        if choice == "meow_admin":
            admin_menu(cat)

    print("=" * 50)
    print("Игра окончена!")
