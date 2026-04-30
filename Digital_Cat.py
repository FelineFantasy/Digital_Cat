import random
import time
import json
import os
import base64


SAVE_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "save.dat")

PHASES = {
    "утро": "день",
    "день": "вечер",
    "вечер": "ночь",
    "ночь": "утро"
}


clear_console = lambda: os.system('cls' if os.name == 'nt' else 'clear')


def clamp(value, min_val=0, max_val=100):
    """Ограничивает значение между min_val и max_val."""
    return max(min_val, min(value, max_val))


def _obfuscate(data: bytes) -> bytes:
    """Запутывает данные"""
    for _ in range(3):
        data = base64.b85encode(data)
        data = data.hex().encode()
        data = data[::-1]
    return data


def _deobfuscate(data: bytes) -> bytes:
    """Распутывает данные"""
    for _ in range(3):
        data = data[::-1]
        data = bytes.fromhex(data.decode())
        data = base64.b85decode(data)
    return data


def save_game(cat):
    """Сохраняет игру (с запутыванием)"""
    json_data = json.dumps(cat, ensure_ascii=False, indent=2).encode('utf-8')
    obfuscated = _obfuscate(json_data)
    with open(SAVE_FILE, "wb") as f:
        f.write(obfuscated)


def load_game():
    """Загружает игру (с распутыванием)"""
    if not os.path.exists(SAVE_FILE):
        return None

    with open(SAVE_FILE, "rb") as f:
        obfuscated = f.read()

    try:
        json_data = _deobfuscate(obfuscated)
        cat = json.loads(json_data.decode('utf-8'))
        cat["is_alive"] = True
        return cat
    except Exception as e:
        print(f"Ошибка загрузки сохранения: {e}")
        return None


def random_event(cat):
    if random.random() < 0.1:
        cat["satiety"] -= 3
        cat["happiness"] -= 1
        cat["energy"] -= 1

    if cat["dirty_tray"]:
        cat["happiness"] -= 2
        cat["health"] -= 1

    if random.random() < 0.15:
        event = random.randint(1, 4)
        if event == 1:
            print("=" * 50)
            print(f"{cat['name']} мяукнул.")
        elif event == 2 and not cat["dirty_tray"]:
            cat["dirty_tray"] = True
            print("=" * 50)
            print(f"{cat['name']} сходил в лоток!")
        elif event == 3:
            found_money = random.randint(1, 5)
            cat["money"] += found_money
            print("=" * 50)
            print(f"{cat['name']} нашёл {found_money} монет!")
        elif event == 4:
            print("=" * 50)
            print(f"{cat['name']} бегает по комнате!")


cat = {
    "name": "",
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

clear_console()
print("ᵐⁱᶜʳᵒSOFT WindowsXP [Version Vista]")
print("(c) Корпорация маленький софт (ᵐⁱᶜʳᵒSOFT Corporation). Все права не защищены.")
print(f"\n{'=' * 50}")
print("Привет! Ты попал в игру Digital Cat.")
print("=" * 50)

saved = load_game()
if saved is not None:
    choice = input("Найдено сохранение. Загрузить? (да/нет): ").lower()
    if choice in ("да", "д", "yes", "y"):
        cat = saved
        clear_console()
        print(f"Сохранение загружено! День {cat['day']}, {cat['name']} ждёт вас.")
    else:
        cat["name"] = input("Придумай имя своему питомцу: ")
else:
    cat["name"] = input("Для начала придумай имя своему питомцу: ")

start_time = time.time()
print("Отличный выбор!")

while cat["is_alive"]:
    random_event(cat)

    cat["satiety"] = clamp(cat["satiety"])
    cat["happiness"] = clamp(cat["happiness"])
    cat["energy"] = clamp(cat["energy"])
    cat["health"] = clamp(cat["health"])

    if cat["health"] <= 0 or cat["satiety"] <= 0 or cat["happiness"] <= 0:
        cat["is_alive"] = False
        print("=" * 50)
        print(f"{cat['name']} умер...")
        print(f"Игра длилась {cat['day']} дней")
        break

    print("=" * 50)
    print("""0. Выйти из игры
1. Покормить кота
2. Погладить кота
3. Поиграть с котом
4. Убрать за котом
5. Уложить кота спать
6. Сходить в зоомагазин
7. Выпустить кота на улицу
8. Заработать монеты
9. Сходить к ветеринару
10. Статистика кота""")

    user_choice = input("Выберите действие от 0 до 10: ")

    match user_choice:
        case "0":
            print("=" * 50)
            print("До встречи!")
            exit()
        case "1":
            if cat["satiety"] >= 100:
                print("=" * 50)
                print(f"{cat['name']} уже сыт!")
            elif cat["money"] < 5:
                print("=" * 50)
                print("Недостаточно монет!")
            else:
                cat["money"] -= 5
                cat["satiety"] += 10
                cat["satiety"] = clamp(cat["satiety"])

                print("=" * 50)
                print(f"Вы покормили {cat['name']}а. -5 монет, +10 сытости.")
                print(f"Теперь монеты: {cat['money']}, сытость: {cat['satiety']}")

                if random.random() < 0.1:
                    print("=" * 50)
                    cat["health"] -= 10
                    cat["health"] = clamp(cat["health"])
                    print(f"{cat['name']}а стошнило. -10 здоровья.")
                    print(f"Теперь здоровье: {cat['health']}")
            save_game(cat)

        case "2":
            if cat["happiness"] >= 100 and cat["love"] >= 100:
                print("=" * 50)
                print(f"{cat['name']} уже счастлив и очень любит вас!")
            elif cat["happiness"] >= 100:
                print("=" * 50)
                print(f"{cat['name']} уже счастлив!")
            elif cat["love"] >= 100:
                print("=" * 50)
                print(f"{cat['name']} уже достаточно любит вас!")
            else:
                cat["happiness"] += 1
                cat["love"] += 1
                cat["happiness"] = clamp(cat["happiness"])
                cat["love"] = clamp(cat["love"])

                print("=" * 50)
                print(f"Вы погладили {cat['name']}а. +1 к счастью, +1 к любви.")
                print(f"Теперь счастье: {cat['happiness']}, любовь: {cat['love']}")
                save_game(cat)

        case "3":
            if cat["energy"] <= 0:
                print("=" * 50)
                print(f"У {cat['name']} недостаточно энергии!")
            elif cat["happiness"] >= 100:
                print("=" * 50)
                print(f"{cat['name']} уже счастлив!")
            else:
                cat["energy"] -= 5
                cat["happiness"] += 10
                cat["happiness"] = clamp(cat["happiness"])

                print("=" * 50)
                print(f"Вы поиграли с {cat['name']}ом. -5 энергии, +10 счастья.")
                print(f"Теперь энергия: {cat['energy']}, счастье: {cat['happiness']}")
                save_game(cat)

        case "4":
            if cat["dirty_tray"]:
                cat["dirty_tray"] = False
                cat["love"] += 5
                cat["happiness"] += 5
                cat["love"] = clamp(cat["love"])
                cat["happiness"] = clamp(cat["happiness"])

                print("=" * 50)
                print(f"Вы убрали лоток за {cat['name']}ом. +5 любви, +5 счастья.")
                print(f"Теперь любовь: {cat['love']}, счастье: {cat['happiness']}")
                save_game(cat)
            else:
                print("=" * 50)
                print("Лоток уже чистый.")

        case "5":
            if cat["energy"] >= 100:
                print("=" * 50)
                print(f"У {cat['name']} уже достаточно энергии!")
            else:
                print("=" * 50)
                print(f"Вы уложили {cat['name']}а спать...")

                if random.random() < 0.2:
                    print(f"{cat['name']} убежал!")
                    cat["happiness"] -= 10
                    cat["happiness"] = clamp(cat["happiness"])
                    continue
                else:
                    print(f"{cat['name']} спит...")
                    time.sleep(3)

                    cat["energy"] += 25
                    cat["day_phase"] = PHASES[cat["day_phase"]]

                    if cat["day_phase"] == "утро":
                        cat["day"] += 1
                        cat["love"] += 10

                    cat["love"] = clamp(cat["love"])
                    cat["energy"] = clamp(cat["energy"])

                    print(f"{cat['name']} проснулся. +25 энергии")
                    print(f"Теперь энергия: {cat['energy']}")
                    if cat["day_phase"] == "утро":
                        print(f"Наступило утро! День {cat['day']}")

                    if cat["day"] == 100:
                        end_time = time.time()
                        elapsed = end_time - start_time

                        minutes = int(elapsed // 60)
                        seconds = int(elapsed % 60)
                        milliseconds = int((elapsed - int(elapsed)) * 1000)

                        print("=" * 50)
                        print("ПОЗДРАВЛЯЮ! ТЫ ПРОШЁЛ ИГРУ!")
                        print(f"Время игры: {minutes} минут {seconds}.{milliseconds:03d} секунд")
                        print("=" * 50)
                        cat["is_alive"] = False
                        break
                    save_game(cat)

        case "6":
            print("=" * 50)
            print("Вы в зоомагазине")
            print("=" * 50)
            print(f"У вас {cat['money']} монет")
            print("1. Купить игрушку - 15 монет")
            print("2. Купить Dreamies - 10 монет")
            print("3. Купить кошачью мяту - 20 монет")

            shop_choice = input("Выберите товар от 1 до 3: ")

            if shop_choice == "1":
                if cat["money"] >= 15:
                    cat["money"] -= 15
                    cat["happiness"] += 25
                    cat["love"] += 10
                    cat["happiness"] = clamp(cat["happiness"])
                    cat["love"] = clamp(cat["love"])

                    print("=" * 50)
                    print("Вы купили игрушку. -15 монет, +25 счастья, +10 любви")
                    print(f"Теперь монеты: {cat['money']}, "
                          f"счастье: {cat['happiness']}, любовь: {cat['love']}")
                else:
                    print("=" * 50)
                    print("Недостаточно монет!")

            elif shop_choice == "2":
                if cat["money"] >= 10:
                    cat["money"] -= 10
                    cat["happiness"] += 10
                    cat["satiety"] += 25
                    cat["love"] += 10
                    cat["happiness"] = clamp(cat["happiness"])
                    cat["satiety"] = clamp(cat["satiety"])
                    cat["love"] = clamp(cat["love"])

                    print("=" * 50)
                    print("Вы купили Dreamies. -10 монет, +10 счастья, "
                          "+25 сытости, +10 любви")
                    print(f"Теперь монеты: {cat['money']}, "
                          f"счастье: {cat['happiness']}, "
                          f"сытость: {cat['satiety']}, любовь: {cat['love']}")
                else:
                    print("=" * 50)
                    print("Недостаточно монет!")

            elif shop_choice == "3":
                if cat["money"] >= 20:
                    cat["money"] -= 20
                    cat["happiness"] += 30
                    cat["satiety"] += 5
                    cat["love"] += 20
                    cat["health"] -= 5
                    cat["happiness"] = clamp(cat["happiness"])
                    cat["satiety"] = clamp(cat["satiety"])
                    cat["love"] = clamp(cat["love"])
                    cat["health"] = clamp(cat["health"])

                    print("=" * 50)
                    print("Вы купили кошачью мяту. -20 монет, +30 счастья, "
                          "+5 сытости, +20 любви, -5 здоровья")
                    print(f"Теперь монеты: {cat['money']}, "
                          f"счастье: {cat['happiness']}, "
                          f"сытость: {cat['satiety']}, "
                          f"любовь: {cat['love']}, здоровье: {cat['health']}")
                else:
                    print("=" * 50)
                    print("Недостаточно монет!")
            else:
                print("=" * 50)
                print("Введите число от 1 до 3")
            save_game(cat)

        case "7":
            cat["happiness"] += 25
            cat["love"] += 10
            cat["satiety"] -= 15
            cat["happiness"] = clamp(cat["happiness"])
            cat["love"] = clamp(cat["love"])
            cat["satiety"] = clamp(cat["satiety"])

            print("=" * 50)
            print("Кот вышел на улицу...")
            time.sleep(3)
            print("Вы выпустили кота на улицу. +25 счастья, +10 любви, -15 сытости")
            print(f"Теперь счастье: {cat['happiness']}, любовь: {cat['love']}, "
                  f"сытость: {cat['satiety']}")
            save_game(cat)

        case "8":
            if cat["energy"] <= 10:
                print("=" * 50)
                print(f"У {cat['name']}а слишком мало энергии для работы!")
            else:
                cat["energy"] -= 10
                earned = random.randint(10, 25)
                cat["money"] += earned
                cat["happiness"] -= 5
                cat["happiness"] = clamp(cat["happiness"])

                print("=" * 50)
                print(f"{cat['name']} помог вам с работой! -10 энергии, "
                      f"+{earned} монет, -5 счастья")
                print(f"Теперь энергия: {cat['energy']}, монеты: {cat['money']}, "
                      f"счастье: {cat['happiness']}")
                save_game(cat)

        case "9":
            print("=" * 50)
            print("Вы в ветеринарной клинике")
            print("=" * 50)
            print(f"Текущее здоровье {cat['name']}а: {cat['health']}")

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

            vet_choice = input("Выберите услугу от 1 до 3: ")

            if vet_choice == "1":
                if cat["money"] >= 30:
                    cat["money"] -= 30
                    cat["health"] += 20
                    cat["satiety"] += 5
                    cat["health"] = clamp(cat["health"])
                    cat["satiety"] = clamp(cat["satiety"])

                    print("=" * 50)
                    print(f"{cat['name']} принял витамины!")
                    print("-30 монет, +20 здоровья, +5 сытости")
                    print(f"Теперь: монеты {cat['money']}, "
                          f"здоровье {cat['health']}, сытость {cat['satiety']}")
                else:
                    print("=" * 50)
                    print("Недостаточно монет!")

            elif vet_choice == "2":
                if cat["money"] >= 50:
                    cat["money"] -= 50
                    cat["health"] += 40
                    cat["health"] = clamp(cat["health"])

                    print("=" * 50)
                    print(f"{cat['name']} прошёл лечение!")
                    print("-50 монет, +40 здоровья")
                    print(f"Теперь: монеты {cat['money']}, здоровье {cat['health']}")
                else:
                    print("=" * 50)
                    print("Недостаточно монет!")

            elif vet_choice == "3":
                if cat["money"] >= 80:
                    cat["money"] -= 80
                    cat["health"] = 100
                    print("=" * 50)
                    print("Экстренная помощь!")
                    print("-80 монет, здоровье восстановлено до 100%")
                    print(f"Теперь: монеты {cat['money']}, здоровье {cat['health']}")
                else:
                    print("=" * 50)
                    print("Недостаточно монет!")
            else:
                print("=" * 50)
                print("Введите число от 1 до 3")
            save_game(cat)

        case "10":
            print("=" * 50)
            print("Статистика кота")
            print("=" * 50)
            print(f"Имя кота: {cat['name']}")
            print(f"Сытость: {cat['satiety']}")
            print(f"Счастье: {cat['happiness']}")
            print(f"Энергия: {cat['energy']}")
            print(f"Здоровье: {cat['health']}")
            alive_text = "Да" if cat["is_alive"] else "Нет"
            tray_text = "Да" if cat["dirty_tray"] else "Нет"
            print(f"Кот жив: {alive_text}")
            print(f"Лоток грязный: {tray_text}")
            print(f"Фаза дня: {cat['day_phase']}")
            print(f"Дней в игре: {cat['day']}")
            print(f"Монет: {cat['money']}")
            print(f"Любовь: {cat['love']}")
            save_game(cat)

        case _:
            print("=" * 50)
            print("Введите число от 0 до 10")

print("Игра окончена!")