"""Модуль зоомагазина."""
from stats import update_stats


def show_menu(cat):
    """Показать меню магазина."""
    print("=" * 50)
    print("Вы в зоомагазине")
    print("=" * 50)
    print(f"У вас {cat['money']} монет")
    print("1. Купить игрушку - 15 монет")
    print("2. Купить Dreamies - 10 монет")
    print("3. Купить кошачью мяту - 20 монет")

    choice = input("Выберите товар от 1 до 3: ")

    items = {
        "1": {"name": "игрушку", "price": 15, "happiness": 25, "love": 10},
        "2": {"name": "Dreamies", "price": 10, "happiness": 10, "satiety": 25, "love": 10},
        "3": {"name": "кошачью мяту", "price": 20, "happiness": 30, "satiety": 5, "love": 20, "health": -5},
    }

    if choice not in items:
        print("Введите число от 1 до 3")
        return

    item = items[choice]

    if cat["money"] < item["price"]:
        print("Недостаточно монет!")
        return

    cat["money"] -= item["price"]
    cat["happiness"] += item.get("happiness", 0)
    cat["satiety"] += item.get("satiety", 0)
    cat["love"] += item.get("love", 0)
    cat["health"] += item.get("health", 0)
    update_stats(cat)

    print(f"Вы купили {item['name']}. -{item['price']} монет")
