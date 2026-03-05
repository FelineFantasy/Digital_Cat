from cat import DigitalCat
from shop import Shop
from vet import Vet
from admin import Admin

class Game:
    def __init__(self):
        self.cat = None

    def main(self):
        print("Привет! Ты попал в игру Digital Cat.")
        print("=" * 50)
        name_cat = input("Для начала придумай имя своему питомцу: ")
        print("Отличный выбор!")

        self.cat = DigitalCat(name_cat)

        while self.cat.is_alive:
            self.cat.random_event()
            self.cat.update_stats()

            if not self.cat.check_alive():
                break

            print("=" * 50)
            print("0. Выйти из игры")
            print("1. Покормить кота")
            print("2. Погладить кота")
            print("3. Поиграть с котом")
            print("4. Убрать за котом")
            print("5. Уложить кота спать")
            print("6. Сходить в зоомагазин")
            print("7. Выпустить кота на улицу")
            print("8. Заработать монеты")
            print("9. Сходить к ветеринару")
            print("10. Статистика кота")

            choice = input("Выберите действие от 0 до 10: ")

            if choice == "0":
                break

            if choice == "1":
                self.cat.feed()
            elif choice == "2":
                self.cat.pet()
            elif choice == "3":
                self.cat.play()
            elif choice == "4":
                self.cat.clean_tray()
            elif choice == "5":
                self.cat.sleep()
            elif choice == "6":
                Shop.show_menu(self.cat)
            elif choice == "7":
                self.cat.go_outside()
            elif choice == "8":
                self.cat.work()
            elif choice == "9":
                Vet.show_menu(self.cat)
            elif choice == "10":
                self.cat.show_stats()
            elif choice == "meow_admin":
                Admin.show_menu(self.cat)
            else:
                print("=" * 50)
                print("Введите число от 0 до 10")

            self.cat.update_stats()

        print("=" * 50)
        print("Игра окончена!")