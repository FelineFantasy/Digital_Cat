class Shop:
    @staticmethod
    def show_menu(cat):
        print("=" * 50)
        print("Вы в зоомагазине")
        print("=" * 50)
        print(f"У вас {cat.money} монет")
        print("1. Купить игрушку - 15 монет")
        print("2. Купить Dreamies - 10 монет")
        print("3. Купить кошачью мяту - 20 монет")

        shop_choice = input("Выберите товар от 1 до 3: ")

        if shop_choice == "1":
            if cat.money >= 15:
                cat.money -= 15
                cat.happiness += 25
                cat.love += 10
                cat.happiness = cat.check_bounds(cat.happiness)
                cat.love = cat.check_bounds(cat.love)
                print("=" * 50)
                print("Вы купили игрушку. -15 монет, +25 счастья, +10 любви")
                print(f"Теперь монеты: {cat.money}, счастье: {cat.happiness}, любовь: {cat.love}")
            else:
                print("=" * 50)
                print("Недостаточно монет!")

        elif shop_choice == "2":
            if cat.money >= 10:
                cat.money -= 10
                cat.happiness += 10
                cat.satiety += 25
                cat.love += 10
                cat.happiness = cat.check_bounds(cat.happiness)
                cat.satiety = cat.check_bounds(cat.satiety)
                cat.love = cat.check_bounds(cat.love)
                print("=" * 50)
                print("Вы купили Dreamies. -10 монет, +10 счастья, +25 сытости, +10 любви")
                print(f"Теперь монеты: {cat.money}, счастье: {cat.happiness}, сытость: {cat.satiety}, любовь: {cat.love}")
            else:
                print("=" * 50)
                print("Недостаточно монет!")

        elif shop_choice == "3":
            if cat.money >= 20:
                cat.money -= 20
                cat.happiness += 30
                cat.satiety += 5
                cat.love += 20
                cat.health -= 5
                cat.happiness = cat.check_bounds(cat.happiness)
                cat.satiety = cat.check_bounds(cat.satiety)
                cat.love = cat.check_bounds(cat.love)
                cat.health = cat.check_bounds(cat.health)
                print("=" * 50)
                print("Вы купили кошачью мяту. -20 монет, +30 счастья, +5 сытости, +20 любви, -5 здоровья")
                print(f"Теперь монеты: {cat.money}, счастье: {cat.happiness}, сытость: {cat.satiety}, любовь: {cat.love}, здоровье: {cat.health}")
            else:
                print("=" * 50)
                print("Недостаточно монет!")
        else:
            print("=" * 50)
            print("Введите число от 1 до 3")