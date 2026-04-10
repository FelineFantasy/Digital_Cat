"""Модуль ветеринарной клиники."""
from stats import update_stats


def show_menu(cat):
    """Показать меню ветклиники."""
    print("=" * 50)
    print("Вы в ветеринарной клинике")
    print("=" * 50)
    print(f"Текущее здоровье {cat['name']}: {cat['health']}")

    if cat["health"] >= 90:
        print(f"{cat['name']} здоров!")
    elif cat["health"] >= 70:
        print("Состояние хорошее!")
    elif cat["health"] >= 50:
        print("Состояние среднее!")
    else:
        print("Нужно срочное лечение!")

    print("=" * 50)
    print("Услуги:")
    print("1. Витамины - 30 монет (+20 здоровья)")
    print("2. Лечение - 50 монет (+40 здоровья)")
    print("3. Экстренная помощь - 80 монет (здоровье = 100%)")

    choice = input("Выберите услугу от 1 до 3: ")

    services = {
        "1": {"name": "витамины", "price": 30, "health": 20, "satiety": 5},
        "2": {"name": "лечение", "price": 50, "health": 40},
        "3": {"name": "экстренная помощь", "price": 80, "health": 100},
    }

    if choice not in services:
        print("Введите число от 1 до 3")
        return

    service = services[choice]

    if cat["money"] < service["price"]:
        print("Недостаточно монет!")
        return

    cat["money"] -= service["price"]

    if choice == "3":
        cat["health"] = 100
    else:
        cat["health"] += service["health"]

    cat["satiety"] += service.get("satiety", 0)
    update_stats(cat)

    print(f"{cat['name']} принял {service['name']}!")
