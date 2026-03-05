class Vet:
    @staticmethod
    def show_menu(cat):
        print("=" * 50)
        print("Вы в ветеринарной клинике")
        print("=" * 50)
        print(f"Текущее здоровье {cat.name}: {cat.health}")

        if cat.health >= 90:
            print(f"{cat.name} здоров!")
        elif cat.health >= 70:
            print("Состояние хорошее!")
        elif cat.health >= 50:
            print("Состояние среднее!")
        else:
            print("Нужно срочное лечение!")

        print("=" * 50)
        print("Услуги:")
        print("1. Витамины - 30 монет (+20 здоровья)")
        print("2. Лечение - 50 монет (+40 здоровья)")
        print("3. Экстренная помощь - 80 монет (здоровье = 100%)")

        vet_choice = input("Выберите услугу от 1 до 3: ")

        if vet_choice == "1":
            if cat.money >= 30:
                cat.money -= 30
                cat.health += 20
                cat.satiety += 5
                cat.health = cat.check_bounds(cat.health)
                cat.satiety = cat.check_bounds(cat.satiety)
                print("=" * 50)
                print(f"{cat.name} принял витамины!")
                print(f"-30 монет, +20 здоровья, +5 сытости")
                print(f"Теперь: монеты {cat.money}, здоровье {cat.health}, сытость {cat.satiety}")
            else:
                print("=" * 50)
                print("Недостаточно монет!")

        elif vet_choice == "2":
            if cat.money >= 50:
                cat.money -= 50
                cat.health += 40
                cat.health = cat.check_bounds(cat.health)
                print("=" * 50)
                print(f"{cat.name} прошёл лечение!")
                print(f"-50 монет, +40 здоровья")
                print(f"Теперь: монеты {cat.money}, здоровье {cat.health}")
            else:
                print("=" * 50)
                print("Недостаточно монет!")

        elif vet_choice == "3":
            if cat.money >= 80:
                cat.money -= 80
                cat.health = 100
                print("=" * 50)
                print("Экстренная помощь!")
                print(f"-80 монет, здоровье восстановлено до 100%")
                print(f"Теперь: монеты {cat.money}, здоровье {cat.health}")
            else:
                print("=" * 50)
                print("Недостаточно монет!")
        else:
            print("=" * 50)
            print("Введите число от 1 до 3")