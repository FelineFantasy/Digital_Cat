"""
Digital Cat - игра-симулятор кота.
"""

import base64
import json
import os
import random
import time
import zlib
from typing import TypedDict


SAVE_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "save.dat")

PHASES = {
    "утро": "день",
    "день": "вечер",
    "вечер": "ночь",
    "ночь": "утро"
}


class CatState(TypedDict):
    """Типизированное состояние кота."""
    name: str
    satiety: int
    happiness: int
    energy: int
    health: int
    day: int
    money: int
    love: int
    is_alive: bool
    dirty_tray: bool
    day_phase: str


def clear_console():
    """Очищает консоль."""
    os.system('cls' if os.name == 'nt' else 'clear')


def wait_and_clear():
    """Ждёт полтора секунды и очищает консоль."""
    time.sleep(1.526742100500)
    clear_console()


def clamp(value, min_val=0, max_val=100):
    """Ограничивает значение между min_val и max_val."""
    return max(min_val, min(value, max_val))


def _obfuscate(data: bytes) -> bytes:
    """Обфусцировать данные для сохранения."""
    data = zlib.compress(data, level=9)
    return base64.b64encode(data)


def _deobfuscate(data: bytes) -> bytes:
    """Деобфусцирует данные из сохранения."""
    data = base64.b64decode(data)
    return zlib.decompress(data)


def save_game(cat: CatState):
    """Сохраняет игру в файл."""
    json_data = json.dumps(
        cat, ensure_ascii=False, indent=2, separators=(',', ': ')
    )
    obfuscated = _obfuscate(json_data.encode('utf-8'))
    with open(SAVE_FILE, "wb") as f:
        f.write(obfuscated)


def load_game() -> CatState | None:
    """Загружает игру из файла."""
    if not os.path.exists(SAVE_FILE):
        return None
    with open(SAVE_FILE, "rb") as f:
        obfuscated = f.read()
    try:
        json_data = _deobfuscate(obfuscated)
        return json.loads(json_data.decode('utf-8'))
    except Exception as e:
        print(f"Ошибка загрузки сохранения: {e}")
        return None


def safe_choice(prompt: str, min_val: int, max_val: int) -> int:
    """Безопасный ввод числа в диапазоне."""
    while True:
        try:
            val = int(input(prompt).strip())
            if min_val <= val <= max_val:
                return val
        except ValueError:
            pass
        print(f"Введите число от {min_val} до {max_val}")


def is_dead(cat: CatState) -> bool:
    """Проверка, жив ли кот. Если умер — обновляем флаг."""
    if not cat["is_alive"]:
        return True
    if cat["health"] <= 0 or cat["satiety"] <= 0 or cat["happiness"] <= 0:
        cat["is_alive"] = False
        return True
    return False


def random_event(cat: CatState):
    """Генерирует случайные события."""
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


def apply_clamp(cat: CatState):
    """Применяет ограничения ко всем характеристикам."""
    cat["satiety"] = clamp(cat["satiety"])
    cat["happiness"] = clamp(cat["happiness"])
    cat["energy"] = clamp(cat["energy"])
    cat["health"] = clamp(cat["health"])
    cat["love"] = clamp(cat["love"])
    cat["money"] = max(0, cat["money"])


def show_menu():
    """Показывает главное меню."""
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
    print("=" * 50)


def action_feed(cat: CatState):
    """Действие: покормить кота."""
    if cat["satiety"] >= 100:
        print("=" * 50)
        print(f"{cat['name']} уже сыт!")
        wait_and_clear()
        return
    if cat["money"] < 5:
        print("=" * 50)
        print("Недостаточно монет!")
        wait_and_clear()
        return

    cat["money"] -= 5
    cat["satiety"] += 10

    print("=" * 50)
    print(f"Вы покормили {cat['name']}а. -5 монет, +10 сытости.")
    print(f"Теперь монеты: {cat['money']}, сытость: {cat['satiety']}")

    if random.random() < 0.1:
        cat["health"] -= 10
        print("=" * 50)
        print(f"{cat['name']}а стошнило. -10 здоровья.")
        print(f"Теперь здоровье: {cat['health']}")

    wait_and_clear()


def action_pet(cat: CatState):
    """Действие: погладить кота."""
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
        print("=" * 50)
        print(f"Вы погладили {cat['name']}а. +1 к счастью, +1 к любви.")
        print(f"Теперь счастье: {cat['happiness']}, любовь: {cat['love']}")

    wait_and_clear()


def action_play(cat: CatState):
    """Действие: поиграть с котом."""
    if cat["energy"] <= 0:
        print("=" * 50)
        print(f"У {cat['name']} недостаточно энергии!")
    elif cat["energy"] < 5:
        print("=" * 50)
        print(f"У {cat['name']} слишком мало энергии для игры!")
    elif cat["happiness"] >= 100:
        print("=" * 50)
        print(f"{cat['name']} уже счастлив!")
    else:
        cat["energy"] -= 5
        cat["happiness"] += 10
        print("=" * 50)
        print(f"Вы поиграли с {cat['name']}ом. -5 энергии, +10 счастья.")
        print(f"Теперь энергия: {cat['energy']}, счастье: {cat['happiness']}")

    wait_and_clear()


def action_clean(cat: CatState):
    """Действие: убрать лоток."""
    if cat["dirty_tray"]:
        cat["dirty_tray"] = False
        cat["love"] += 5
        cat["happiness"] += 5
        print("=" * 50)
        print(f"Вы убрали лоток за {cat['name']}ом. +5 любви, +5 счастья.")
        print(f"Теперь любовь: {cat['love']}, счастье: {cat['happiness']}")
    else:
        print("=" * 50)
        print("Лоток уже чистый.")

    wait_and_clear()


def action_sleep(cat: CatState):
    """Действие: уложить кота спать."""
    if cat["energy"] >= 100:
        print("=" * 50)
        print(f"У {cat['name']} уже достаточно энергии!")
        wait_and_clear()
        return

    print("=" * 50)
    print(f"Вы уложили {cat['name']}а спать...")

    if random.random() < 0.2:
        cat["happiness"] -= 10
        print(f"{cat['name']} убежал!")
        wait_and_clear()
        return

    print(f"{cat['name']} спит...")
    time.sleep(0.5)

    cat["energy"] += 25
    cat["energy"] = clamp(cat["energy"])
    old_phase = cat["day_phase"]
    cat["day_phase"] = PHASES[old_phase]

    if cat["day_phase"] == "утро":
        cat["day"] += 1
        cat["love"] += 10

    print(f"{cat['name']} проснулся. +25 энергии")
    print(f"Теперь энергия: {cat['energy']}")
    if cat["day_phase"] == "утро":
        print(f"Наступило утро! День {cat['day']}")

    wait_and_clear()


def action_shop(cat: CatState):
    """Действие: сходить в магазин."""
    while True:
        print("=" * 50)
        print("Вы в магазине")
        print("=" * 50)
        print(f"У вас {cat['money']} монет")
        print("0. Выйти в главное меню")
        print("1. Купить игрушку - 15 монет")
        print("2. Купить Dreamies - 10 монет")
        print("3. Купить кошачью мяту - 20 монет")
        print("=" * 50)

        choice = safe_choice("Выберите действие: ", 0, 3)

        match choice:
            case 0:
                print("=" * 50)
                print("Вы вышли из магазина")
                wait_and_clear()
                return
            case 1:
                if cat["money"] >= 15:
                    cat["money"] -= 15
                    cat["happiness"] += 25
                    cat["love"] += 10
                    print("=" * 50)
                    print("Вы купили игрушку. -15 монет, +25 счастья, +10 любви")
                    print(
                        f"Теперь монеты: {cat['money']}, "
                        f"счастье: {cat['happiness']}, любовь: {cat['love']}"
                    )
                else:
                    print("=" * 50)
                    print("Недостаточно монет!")
                wait_and_clear()
            case 2:
                if cat["money"] >= 10:
                    cat["money"] -= 10
                    cat["happiness"] += 10
                    cat["satiety"] = clamp(cat["satiety"] + 25)
                    cat["love"] += 10
                    print("=" * 50)
                    print(
                        "Вы купили Dreamies. -10 монет, +10 счастья, "
                        "+25 сытости, +10 любви"
                    )
                    print(
                        f"Теперь монеты: {cat['money']}, "
                        f"счастье: {cat['happiness']}, "
                        f"сытость: {cat['satiety']}, любовь: {cat['love']}"
                    )
                else:
                    print("=" * 50)
                    print("Недостаточно монет!")
                wait_and_clear()
            case 3:
                if cat["money"] >= 20:
                    cat["money"] -= 20
                    cat["happiness"] += 30
                    cat["satiety"] = clamp(cat["satiety"] + 5)
                    cat["love"] += 20
                    cat["health"] -= 5
                    print("=" * 50)
                    print(
                        "Вы купили кошачью мяту. -20 монет, +30 счастья, "
                        "+5 сытости, +20 любви, -5 здоровья"
                    )
                    print(
                        f"Теперь монеты: {cat['money']}, "
                        f"счастье: {cat['happiness']}, "
                        f"сытость: {cat['satiety']}, "
                        f"любовь: {cat['love']}, здоровье: {cat['health']}"
                    )
                else:
                    print("=" * 50)
                    print("Недостаточно монет!")
                wait_and_clear()


def action_outside(cat: CatState):
    """Действие: выпустить кота на улицу."""
    if cat["satiety"] <= 15:
        print("=" * 50)
        print(f"{cat['name']} слишком голоден для прогулки!")
        wait_and_clear()
        return

    cat["happiness"] += 25
    cat["love"] += 10
    cat["satiety"] -= 15

    print("=" * 50)
    print("Кот вышел на улицу...")
    time.sleep(0.5)
    print(
        "Вы выпустили кота на улицу. +25 счастья, +10 любви, -15 сытости"
    )
    print(
        f"Теперь счастье: {cat['happiness']}, любовь: {cat['love']}, "
        f"сытость: {cat['satiety']}"
    )

    wait_and_clear()


def action_work(cat: CatState):
    """Действие: заработать монеты."""
    if cat["energy"] <= 10:
        print("=" * 50)
        print(f"У {cat['name']}а слишком мало энергии для работы!")
        wait_and_clear()
        return

    cat["energy"] -= 10
    earned = random.randint(10, 25)
    cat["money"] += earned
    cat["happiness"] -= 5

    print("=" * 50)
    print(
        f"{cat['name']} помог вам с работой! -10 энергии, "
        f"+{earned} монет, -5 счастья"
    )
    print(
        f"Теперь энергия: {cat['energy']}, монеты: {cat['money']}, "
        f"счастье: {cat['happiness']}"
    )

    wait_and_clear()


def action_vet(cat: CatState):
    """Действие: сходить к ветеринару."""
    while True:
        print("=" * 50)
        print("Вы в ветеринарной клинике")
        print("=" * 50)
        print(f"Текущее здоровье {cat['name']}а: {cat['health']}")
        print("0. Выйти в главное меню")
        print("1. Витамины - 30 монет (+20 здоровья)")
        print("2. Лечение - 50 монет (+40 здоровья)")
        print("3. Экстренная помощь - 80 монет (здоровье = 100%)")
        print("=" * 50)

        choice = safe_choice("Выберите действие: ", 0, 3)

        match choice:
            case 0:
                print("=" * 50)
                print("Вы вышли из клиники")
                wait_and_clear()
                return
            case 1:
                if cat["money"] >= 30:
                    cat["money"] -= 30
                    cat["health"] = clamp(cat["health"] + 20)
                    cat["satiety"] = clamp(cat["satiety"] + 5)
                    print("=" * 50)
                    print(f"{cat['name']} принял витамины!")
                    print("-30 монет, +20 здоровья, +5 сытости")
                    print(
                        f"Теперь: монеты {cat['money']}, "
                        f"здоровье {cat['health']}, сытость {cat['satiety']}"
                    )
                else:
                    print("=" * 50)
                    print("Недостаточно монет!")
                wait_and_clear()
            case 2:
                if cat["money"] >= 50:
                    cat["money"] -= 50
                    cat["health"] = clamp(cat["health"] + 40)
                    print("=" * 50)
                    print(f"{cat['name']} прошёл лечение!")
                    print("-50 монет, +40 здоровья")
                    print(
                        f"Теперь: монеты {cat['money']}, "
                        f"здоровье {cat['health']}"
                    )
                else:
                    print("=" * 50)
                    print("Недостаточно монет!")
                wait_and_clear()
            case 3:
                if cat["money"] >= 80:
                    cat["money"] -= 80
                    cat["health"] = 100
                    print("=" * 50)
                    print("Экстренная помощь!")
                    print("-80 монет, здоровье восстановлено до 100%")
                    print(
                        f"Теперь: монеты {cat['money']}, "
                        f"здоровье {cat['health']}"
                    )
                else:
                    print("=" * 50)
                    print("Недостаточно монет!")
                wait_and_clear()


def action_stats(cat: CatState):
    """Действие: показать статистику."""
    print("=" * 50)
    print("Статистика кота")
    print("=" * 50)
    print(f"Имя кота: {cat['name']}")
    print(f"Сытость: {cat['satiety']}")
    print(f"Счастье: {cat['happiness']}")
    print(f"Энергия: {cat['energy']}")
    print(f"Здоровье: {cat['health']}")
    print(f"Кот жив: {'Да' if cat['is_alive'] else 'Нет'}")
    print(f"Лоток грязный: {'Да' if cat['dirty_tray'] else 'Нет'}")
    print(f"Фаза дня: {cat['day_phase']}")
    print(f"Дней в игре: {cat['day']}")
    print(f"Монет: {cat['money']}")
    print(f"Любовь: {cat['love']}")

    wait_and_clear()


def show_welcome_screen():
    """Показывает заставку Windows XP/Vista."""
    clear_console()
    print("ᵐⁱᶜʳᵒSOFT WindowsXP [Version Vista]")
    print(
        "(c) Корпорация маленький софт (ᵐⁱᶜʳᵒSOFT Corporation). "
        "Все права не защищены."
    )


def main():
    """Основная функция игры."""
    cat: CatState = {
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

    show_welcome_screen()
    print(f"\n{'=' * 50}")
    print("Привет! Ты попал в игру Digital Cat.")
    print("=" * 50)

    saved = load_game()
    if saved is not None and saved.get("is_alive", False):
        choice = input("Найдено сохранение. Загрузить? (да/нет): ").lower().strip()
        if choice in ("да", "д", "yes", "y"):
            cat = saved
            clear_console()
            print(
                f"Сохранение загружено! День {cat['day']}, {cat['name']} ждёт вас."
            )
            print("Отличный выбор!")
            time.sleep(1)
            clear_console()
        else:
            cat["name"] = input("Придумай имя своему питомцу: ").strip()
            clear_console()
    else:
        cat["name"] = input("Для начала придумай имя своему питомцу: ").strip()
        clear_console()

    while cat["is_alive"]:
        random_event(cat)
        apply_clamp(cat)

        if is_dead(cat):
            print("=" * 50)
            print(f"{cat['name']} умер...")
            print(f"Игра длилась {cat['day']} дней")
            time.sleep(2)
            break

        if cat["day"] >= 100:
            print("=" * 50)
            print("ПОЗДРАВЛЯЮ! ТЫ ПРОШЁЛ ИГРУ!")
            print("=" * 50)
            cat["is_alive"] = False
            save_game(cat)
            time.sleep(2)
            break

        show_welcome_screen()
        print("\n" + "=" * 50)
        show_menu()

        user_choice = input("Выберите действие от 0 до 10: ").strip()

        match user_choice:
            case "0":
                print("=" * 50)
                save_game(cat)
                print("До встречи!")
                return
            case "1":
                action_feed(cat)
            case "2":
                action_pet(cat)
            case "3":
                action_play(cat)
            case "4":
                action_clean(cat)
            case "5":
                action_sleep(cat)
            case "6":
                action_shop(cat)
            case "7":
                action_outside(cat)
            case "8":
                action_work(cat)
            case "9":
                action_vet(cat)
            case "10":
                action_stats(cat)
            case _:
                print("=" * 50)
                print("Введите число от 0 до 10")
                wait_and_clear()
                continue

        apply_clamp(cat)
        if is_dead(cat):
            print("=" * 50)
            print(f"{cat['name']} умер...")
            print(f"Игра длилась {cat['day']} дней")
            time.sleep(2)
            break

        save_game(cat)

    if os.path.exists(SAVE_FILE):
        os.remove(SAVE_FILE)

    print("Игра окончена!")


if __name__ == "__main__":
    main()