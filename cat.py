import random
import time

class DigitalCat:
    def __init__(self, name):
        self.name = name
        self.satiety = 50
        self.happiness = 50
        self.energy = 70
        self.health = 100
        self.day = 1
        self.money = 100
        self.love = 50
        self.is_alive = True
        self.dirty_tray = False
        self.day_phase = "день"

    def check_bounds(self, value):
        if value < 0:
            return 0
        elif value > 100:
            return 100
        return value

    def update_stats(self):
        self.satiety = self.check_bounds(self.satiety)
        self.happiness = self.check_bounds(self.happiness)
        self.energy = self.check_bounds(self.energy)
        self.health = self.check_bounds(self.health)
        self.love = self.check_bounds(self.love)

    def random_event(self):
        if random.random() < 0.1:
            self.satiety -= 3
            self.happiness -= 1
            self.energy -= 1

        if self.dirty_tray:
            self.happiness -= 2
            self.health -= 1

        if random.random() < 0.15:
            event = random.randint(1, 4)
            if event == 1:
                print("=" * 50)
                print(f"{self.name} мяукнул.")
            elif event == 2 and not self.dirty_tray:
                self.dirty_tray = True
                print("=" * 50)
                print(f"{self.name} сходил в лоток!")
            elif event == 3:
                found_money = random.randint(1, 5)
                self.money += found_money
                print("=" * 50)
                print(f"{self.name} нашёл {found_money} монеты!")
            elif event == 4:
                print("=" * 50)
                print(f"{self.name} бегает по комнате!")

    def check_alive(self):
        if self.health <= 0 or self.satiety <= 0 or self.happiness <= 0:
            self.is_alive = False
            print("=" * 50)
            print(f"{self.name} умер...")
            print(f"Игра длилась {self.day} дней")
            return False
        return True

    def feed(self):
        if self.satiety >= 100:
            print("=" * 50)
            print(f"{self.name} уже сыт!")
        elif self.money < 5:
            print("=" * 50)
            print("Недостаточно монет!")
        else:
            self.money -= 5
            self.satiety += 10
            self.satiety = self.check_bounds(self.satiety)
            print("=" * 50)
            print(f"Вы покормили {self.name}. -5 монет, +10 сытости.")
            print(f"Теперь монеты: {self.money}, сытость: {self.satiety}")

            if random.random() < 0.1:
                print("=" * 50)
                self.health -= 10
                self.health = self.check_bounds(self.health)
                print(f"{self.name} стошнило. -10 здоровья.")
                print(f"Теперь здоровье: {self.health}")

    def pet(self):
        if self.happiness >= 100 and self.love >= 100:
            print("=" * 50)
            print(f"{self.name} уже счастлив и очень любит вас!")
        elif self.happiness >= 100:
            print("=" * 50)
            print(f"{self.name} уже счастлив!")
        elif self.love >= 100:
            print("=" * 50)
            print(f"{self.name} уже достаточно любит вас!")
        else:
            self.happiness += 1
            self.love += 1
            self.happiness = self.check_bounds(self.happiness)
            self.love = self.check_bounds(self.love)
            print("=" * 50)
            print(f"Вы погладили {self.name}. +1 к счастью, +1 к любви.")
            print(f"Теперь счастье: {self.happiness}, любовь: {self.love}")

    def play(self):
        if self.energy <= 0:
            print("=" * 50)
            print(f"У {self.name} недостаточно энергии!")
        elif self.happiness >= 100:
            print("=" * 50)
            print(f"{self.name} уже счастлив!")
        else:
            self.energy -= 5
            self.happiness += 10
            self.happiness = self.check_bounds(self.happiness)
            print("=" * 50)
            print(f"Вы поиграли с {self.name}. -5 энергии, +10 счастья.")
            print(f"Теперь энергия: {self.energy}, счастье: {self.happiness}")

    def clean_tray(self):
        if self.dirty_tray:
            self.dirty_tray = False
            self.love += 5
            self.happiness += 5
            self.love = self.check_bounds(self.love)
            self.happiness = self.check_bounds(self.happiness)
            print("=" * 50)
            print(f"Вы убрали лоток за {self.name}. +5 любви, +5 счастья.")
            print(f"Теперь любовь: {self.love}, счастье: {self.happiness}")
        else:
            print("=" * 50)
            print("Лоток уже чистый.")

    def sleep(self):
        if self.energy >= 100:
            print("=" * 50)
            print(f"У {self.name} уже достаточно энергии!")
        else:
            print("=" * 50)
            print(f"Вы уложили {self.name} спать...")

            if random.random() < 0.2:
                print(f"{self.name} убежал!")
                self.happiness -= 10
                self.happiness = self.check_bounds(self.happiness)
            else:
                print(f"{self.name} спит...")
                time.sleep(3)

                self.energy += 25
                self.energy = self.check_bounds(self.energy)

                if self.day_phase == "утро":
                    self.day_phase = "день"
                elif self.day_phase == "день":
                    self.day_phase = "вечер"
                elif self.day_phase == "вечер":
                    self.day_phase = "ночь"
                elif self.day_phase == "ночь":
                    self.day_phase = "утро"
                    self.day += 1
                    self.love += 10
                    self.love = self.check_bounds(self.love)

                print(f"{self.name} проснулся. +25 энергии")
                print(f"Теперь энергия: {self.energy}")
                if self.day_phase == "утро":
                    print(f"Наступило утро! День {self.day}")

    def go_outside(self):
        self.happiness += 25
        self.love += 10
        self.satiety -= 15
        self.happiness = self.check_bounds(self.happiness)
        self.love = self.check_bounds(self.love)
        self.satiety = self.check_bounds(self.satiety)

        print("=" * 50)
        print("Кот вышел на улицу...")
        time.sleep(3)
        print("Вы выпустили кота на улицу. +25 счастья, +10 любви, -15 сытости")
        print(f"Теперь счастье: {self.happiness}, любовь: {self.love}, сытость: {self.satiety}")

    def work(self):
        if self.energy < 10:
            print("=" * 50)
            print(f"У {self.name} слишком мало энергии для работы!")
        else:
            self.energy -= 10
            earned = random.randint(10, 25)
            self.money += earned
            self.happiness -= 5
            self.happiness = self.check_bounds(self.happiness)
            print("=" * 50)
            print(f"{self.name} помог вам с работой! -10 энергии, +{earned} монет, -5 счастья")
            print(f"Теперь энергия: {self.energy}, монеты: {self.money}, счастье: {self.happiness}")

    def show_stats(self):
        print("=" * 50)
        print("Статистика кота")
        print("=" * 50)
        print(f"Имя кота: {self.name}")
        print(f"Сытость: {self.satiety}")
        print(f"Счастье: {self.happiness}")
        print(f"Энергия: {self.energy}")
        print(f"Здоровье: {self.health}")
        print(f"Монет: {self.money}")
        print(f"Любовь: {self.love}")
        print(f"Дней в игре: {self.day}")
        print(f"Фаза дня: {self.day_phase}")
        print(f"Лоток грязный: {self.dirty_tray}")