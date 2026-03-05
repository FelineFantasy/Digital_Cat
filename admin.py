class Admin:
    @staticmethod
    def show_menu(cat):
        print("=" * 50)
        print("Админ меню")
        print("=" * 50)
        print("1. Все параметры максимальные")
        print("2. Все параметры минимальны")
        print("3. Все параметры возращены к исходным")
        print("4. +1000 монет")
        print("5. -1000 монет")

        admin_choice = input("Введите число от 1 до 5: ")

        if admin_choice == "1":
            cat.satiety = 100
            cat.happiness = 100
            cat.energy = 100
            cat.health = 100
            cat.love = 100
            print("=" * 50)
            print("Все параметры максимальны")

        elif admin_choice == "2":
            cat.satiety = 0
            cat.happiness = 0
            cat.health = 0
            cat.energy = 0
            cat.love = 0
            print("=" * 50)
            print("Все параметры минимальны")

        elif admin_choice == "3":
            cat.satiety = 50
            cat.happiness = 50
            cat.energy = 70
            cat.health = 100
            cat.day = 1
            cat.money = 100
            cat.love = 50
            cat.dirty_tray = False
            cat.day_phase = "день"
            print("=" * 50)
            print("Все параметры возращены к исходным")

        elif admin_choice == "4":
            cat.money += 1000
            print("=" * 50)
            print(f"+1000 монет! Теперь у вас: {cat.money} монет")

        elif admin_choice == "5":
            cat.money -= 1000
            print("=" * 50)
            print(f"-1000 монет! Теперь у вас: {cat.money} монет")

        else:
            print("=" * 50)
            print("Введите число от 1 до 5")