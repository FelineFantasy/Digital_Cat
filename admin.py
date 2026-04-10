"""Модуль админ-меню."""


def show_menu(cat):
    """Показать админ-меню."""
    print("=" * 50)
    print("Админ меню")
    print("=" * 50)
    print("1. Все параметры максимальные")
    print("2. Все параметры минимальны")
    print("3. Все параметры возвращены к исходным")
    print("4. +1000 монет")
    print("5. -1000 монет")

    choice = input("Введите число от 1 до 5: ")

    if choice == "1":
        cat["satiety"] = 100
        cat["happiness"] = 100
        cat["energy"] = 100
        cat["health"] = 100
        cat["love"] = 100
        print("Все параметры максимальны")

    elif choice == "2":
        cat["satiety"] = 0
        cat["happiness"] = 0
        cat["health"] = 0
        cat["energy"] = 0
        cat["love"] = 0
        print("Все параметры минимальны")

    elif choice == "3":
        cat["satiety"] = 50
        cat["happiness"] = 50
        cat["energy"] = 70
        cat["health"] = 100
        cat["day"] = 1
        cat["money"] = 100
        cat["love"] = 50
        cat["dirty_tray"] = False
        cat["day_phase"] = "день"
        print("Все параметры возвращены к исходным")

    elif choice == "4":
        cat["money"] += 1000
        print(f"+1000 монет! Теперь у вас: {cat['money']} монет")

    elif choice == "5":
        cat["money"] -= 1000
        print(f"-1000 монет! Теперь у вас: {cat['money']} монет")

    else:
        print("Введите число от 1 до 5")
