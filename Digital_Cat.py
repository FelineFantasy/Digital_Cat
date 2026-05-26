"""
Digital Cat - игра-симулятор кота.
"""

import base64
import json
import os
import random
import sys
import time
import zlib
from functools import wraps
from typing import TypedDict


def get_base_dir():
    """Возвращает базовую директорию для сохранения файлов."""
    if getattr(sys, 'frozen', False):
        return os.path.dirname(sys.executable)
    else:
        return os.path.dirname(os.path.abspath(__file__))


def get_save_path():
    """Возвращает путь к файлу сохранения."""
    base_dir = get_base_dir()
    os.makedirs(base_dir, exist_ok=True)
    return os.path.join(base_dir, "save.dat")


def get_log_path():
    """Возвращает путь к лог-файлу."""
    base_dir = get_base_dir()
    os.makedirs(base_dir, exist_ok=True)
    return os.path.join(base_dir, "log.txt")


SAVE_FILE = get_save_path()
LOG_FILE = get_log_path()

PHASES = {
    "утро": "день",
    "день": "вечер",
    "вечер": "ночь",
    "ночь": "утро"
}

SCREEN_CLEAR_DELAY = 1.5

VERSION = "v3.0.1"
AUTHOR = "Тимур (FelineFantasy)"
LICENSE = "MIT"

_LOG_BUFFER = []
_LOG_LAST_WRITE = 0


def log_to_file(level: str, msg: str):
    global _LOG_BUFFER, _LOG_LAST_WRITE
    _LOG_BUFFER.append(f"[{level}] {time.strftime('%H:%M:%S')} {msg}\n")
    now = time.time()
    if len(_LOG_BUFFER) >= 10 or now - _LOG_LAST_WRITE >= 60 or level == "ERROR":
        try:
            with open(LOG_FILE, "a", encoding="utf-8") as f:
                f.write("".join(_LOG_BUFFER))
            _LOG_BUFFER = []
            _LOG_LAST_WRITE = now
        except (IOError, OSError):
            pass


def log(func):
    """Декоратор для логирования функций."""

    @wraps(func)
    def wrapper(*args, **kwargs):
        start = time.perf_counter()
        log_to_file("INFO", f"функция {func.__name__} запущена")
        try:
            result = func(*args, **kwargs)
            elapsed = time.perf_counter() - start
            log_to_file(
                "INFO",
                f"функция {func.__name__} завершена, время: {elapsed:.8f}"
            )
            return result
        except Exception as e:
            elapsed = time.perf_counter() - start
            log_to_file(
                "ERROR",
                f"функция {func.__name__} упала через {elapsed:.8f}: {e}"
            )
            raise

    return wrapper


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
    """Ждёт и очищает консоль с задержкой из настроек."""
    time.sleep(SCREEN_CLEAR_DELAY)
    clear_console()


def wait_for_enter():
    """Ждёт нажатия Enter (для действий где нужен ручной контроль)."""
    input("\nНажмите Enter чтобы продолжить...")


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
    try:
        os.makedirs(os.path.dirname(SAVE_FILE), exist_ok=True)
        json_data = json.dumps(
            cat, ensure_ascii=False, indent=2, separators=(',', ': ')
        )
        obfuscated = _obfuscate(json_data.encode('utf-8'))
        with open(SAVE_FILE, "wb") as f:
            f.write(obfuscated)
        log_to_file(
            "DEBUG",
            f"Игра сохранена: день={cat['day']}, имя={cat['name']}, "
            f"путь={SAVE_FILE}"
        )
    except Exception as e:
        log_to_file("ERROR", f"Ошибка сохранения: {e}")


def load_game() -> CatState | None:
    """Загружает игру из файла."""
    if not os.path.exists(SAVE_FILE):
        log_to_file("DEBUG", f"Файл сохранения не найден: {SAVE_FILE}")
        return None
    try:
        with open(SAVE_FILE, "rb") as f:
            obfuscated = f.read()
        json_data = _deobfuscate(obfuscated)
        cat = json.loads(json_data.decode('utf-8'))
        log_to_file(
            "DEBUG",
            f"Игра загружена: день={cat['day']}, имя={cat['name']}, "
            f"путь={SAVE_FILE}"
        )
        return cat
    except Exception as e:
        print(f"Ошибка загрузки сохранения: {e}")
        log_to_file("ERROR", f"Ошибка загрузки сохранения: {e}")
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
    log_to_file(
        "DEBUG",
        f"Проверка alive: health={cat['health']}, satiety={cat['satiety']}, "
        f"happiness={cat['happiness']}"
    )
    if not cat["is_alive"]:
        log_to_file("DEBUG", "Кот уже мёртв (флаг is_alive=False)")
        return True
    if cat["health"] <= 0 or cat["satiety"] <= 0 or cat["happiness"] <= 0:
        cat["is_alive"] = False
        log_to_file(
            "WARNING",
            f"Кот умер! health={cat['health']}, satiety={cat['satiety']}, "
            f"happiness={cat['happiness']}"
        )
        return True
    return False


def random_event(cat: CatState):
    """Генерирует случайные события."""
    if random.random() < 0.1:
        cat["satiety"] -= 3
        cat["happiness"] -= 1
        cat["energy"] -= 1
        log_to_file(
            "DEBUG",
            "Случайное ухудшение: satiety-3, happiness-1, energy-1"
        )

    if cat["dirty_tray"]:
        cat["happiness"] -= 2
        cat["health"] -= 1
        log_to_file("DEBUG", "Грязный лоток: happiness-2, health-1")

    if random.random() < 0.15:
        event = random.randint(1, 4)
        if event == 1:
            print(f"{cat['name']} мяукнул.")
            print("=" * 50)
            log_to_file("DEBUG", "Событие: кот мяукнул")
        elif event == 2 and not cat["dirty_tray"]:
            cat["dirty_tray"] = True
            print(f"{cat['name']} сходил в лоток!")
            print("=" * 50)
            log_to_file("DEBUG", "Событие: кот сходил в лоток")
        elif event == 3:
            found_money = random.randint(1, 5)
            cat["money"] += found_money
            print(f"{cat['name']} нашёл {found_money} монет!")
            print("=" * 50)
            log_to_file(
                "DEBUG", f"Событие: кот нашёл {found_money} монет"
            )
        elif event == 4:
            print(f"{cat['name']} бегает по комнате!")
            print("=" * 50)
            log_to_file("DEBUG", "Событие: кот бегает по комнате")


def apply_clamp(cat: CatState):
    """Применяет ограничения ко всем характеристикам."""
    old_values = (
        cat["satiety"], cat["happiness"], cat["energy"],
        cat["health"], cat["love"], cat["money"]
    )
    cat["satiety"] = clamp(cat["satiety"])
    cat["happiness"] = clamp(cat["happiness"])
    cat["energy"] = clamp(cat["energy"])
    cat["health"] = clamp(cat["health"])
    cat["love"] = clamp(cat["love"])
    cat["money"] = max(0, cat["money"])
    new_values = (
        cat["satiety"], cat["happiness"], cat["energy"],
        cat["health"], cat["love"], cat["money"]
    )
    if old_values != new_values:
        log_to_file("DEBUG", f"apply_clamp: {old_values} -> {new_values}")


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
    print("11. Настройки")
    print("=" * 50)


@log
def action_feed(cat: CatState):
    """Действие: покормить кота."""
    log_to_file(
        "DEBUG",
        f"До кормления: satiety={cat['satiety']}, money={cat['money']}, "
        f"health={cat['health']}"
    )

    if cat["satiety"] >= 100:
        log_to_file("DEBUG", "Кот уже сыт, выход")
        print("=" * 50)
        print(f"{cat['name']} уже сыт!")
        wait_and_clear()
        return
    if cat["money"] < 5:
        log_to_file("DEBUG", f"Недостаточно монет: {cat['money']} < 5")
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
        log_to_file(
            "WARNING",
            f"Кота стошнило! health-10, новое health={cat['health']}"
        )
        print("=" * 50)
        print(f"{cat['name']}а стошнило. -10 здоровья.")
        print(f"Теперь здоровье: {cat['health']}")

    log_to_file(
        "DEBUG",
        f"После кормления: satiety={cat['satiety']}, money={cat['money']}, "
        f"health={cat['health']}"
    )
    wait_and_clear()


@log
def action_pet(cat: CatState):
    """Действие: погладить кота."""
    log_to_file(
        "DEBUG",
        f"До поглаживания: happiness={cat['happiness']}, love={cat['love']}"
    )

    if cat["happiness"] >= 100 and cat["love"] >= 100:
        log_to_file("DEBUG", "Кот уже максимально счастлив и любит")
        print("=" * 50)
        print(f"{cat['name']} уже счастлив и очень любит вас!")
    elif cat["happiness"] >= 100:
        log_to_file("DEBUG", "Кот уже максимально счастлив")
        print("=" * 50)
        print(f"{cat['name']} уже счастлив!")
    elif cat["love"] >= 100:
        log_to_file("DEBUG", "Любовь уже максимальна")
        print("=" * 50)
        print(f"{cat['name']} уже достаточно любит вас!")
    else:
        cat["happiness"] += 1
        cat["love"] += 1
        log_to_file(
            "DEBUG",
            f"После поглаживания: happiness={cat['happiness']}, "
            f"love={cat['love']}"
        )
        print("=" * 50)
        print(f"Вы погладили {cat['name']}а. +1 к счастью, +1 к любви.")
        print(
            f"Теперь счастье: {cat['happiness']}, любовь: {cat['love']}"
        )

    wait_and_clear()


@log
def action_play(cat: CatState):
    """Действие: поиграть с котом."""
    log_to_file(
        "DEBUG",
        f"До игры: energy={cat['energy']}, happiness={cat['happiness']}"
    )

    if cat["energy"] <= 0:
        log_to_file("DEBUG", "Энергия = 0, игра невозможна")
        print("=" * 50)
        print(f"У {cat['name']} недостаточно энергии!")
    elif cat["energy"] < 5:
        log_to_file("DEBUG", f"Энергия {cat['energy']} < 5, игра невозможна")
        print("=" * 50)
        print(f"У {cat['name']} слишком мало энергии для игры!")
    elif cat["happiness"] >= 100:
        log_to_file("DEBUG", "Счастье максимально, игра не нужна")
        print("=" * 50)
        print(f"{cat['name']} уже счастлив!")
    else:
        cat["energy"] -= 5
        cat["happiness"] += 10
        log_to_file(
            "DEBUG",
            f"После игры: energy={cat['energy']}, "
            f"happiness={cat['happiness']}"
        )
        print("=" * 50)
        print(f"Вы поиграли с {cat['name']}ом. -5 энергии, +10 счастья.")
        print(
            f"Теперь энергия: {cat['energy']}, счастье: {cat['happiness']}"
        )

    wait_and_clear()


@log
def action_clean(cat: CatState):
    """Действие: убрать лоток."""
    log_to_file(
        "DEBUG",
        f"Уборка лотка: dirty_tray={cat['dirty_tray']}, love={cat['love']}, "
        f"happiness={cat['happiness']}"
    )

    if cat["dirty_tray"]:
        cat["dirty_tray"] = False
        cat["love"] += 5
        cat["happiness"] += 5
        log_to_file(
            "DEBUG",
            f"После уборки: dirty_tray={cat['dirty_tray']}, "
            f"love={cat['love']}, happiness={cat['happiness']}"
        )
        print("=" * 50)
        print(f"Вы убрали лоток за {cat['name']}ом. +5 любви, +5 счастья.")
        print(f"Теперь любовь: {cat['love']}, счастье: {cat['happiness']}")
    else:
        log_to_file("DEBUG", "Лоток уже чист, уборка не требуется")
        print("=" * 50)
        print("Лоток уже чистый.")

    wait_and_clear()


@log
def action_sleep(cat: CatState):
    """Действие: уложить кота спать."""
    log_to_file(
        "DEBUG",
        f"До сна: energy={cat['energy']}, day_phase={cat['day_phase']}, "
        f"day={cat['day']}"
    )

    if cat["energy"] >= 100:
        log_to_file("DEBUG", "Энергия максимальна, сон не нужен")
        print("=" * 50)
        print(f"У {cat['name']} уже достаточно энергии!")
        wait_and_clear()
        return

    print("=" * 50)
    print(f"Вы уложили {cat['name']}а спать...")

    if random.random() < 0.2:
        cat["happiness"] -= 10
        log_to_file(
            "WARNING",
            f"Кот убежал! happiness-10, новое happiness={cat['happiness']}"
        )
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

    log_to_file(
        "DEBUG",
        f"После сна: energy={cat['energy']}, day_phase={cat['day_phase']}, "
        f"day={cat['day']}, love={cat['love']}"
    )

    print(f"{cat['name']} проснулся. +25 энергии")
    print(f"Теперь энергия: {cat['energy']}")
    if cat["day_phase"] == "утро":
        print(f"Наступило утро! День {cat['day']}")

    wait_and_clear()


@log
def action_shop(cat: CatState):
    """Действие: сходить в магазин (остаётся на экране до выхода)."""
    log_to_file("DEBUG", f"Вход в магазин: money={cat['money']}")
    clear_console()

    def buy_toy():
        if cat["money"] >= 15:
            cat["money"] -= 15
            cat["happiness"] += 25
            cat["love"] += 10
            log_to_file(
                "DEBUG",
                f"Куплена игрушка: money={cat['money']}, "
                f"happiness={cat['happiness']}, love={cat['love']}"
            )
            print("=" * 50)
            print("Вы купили игрушку. -15 монет, +25 счастья, +10 любви")
            print(
                f"Теперь монеты: {cat['money']}, "
                f"счастье: {cat['happiness']}, любовь: {cat['love']}"
            )
        else:
            log_to_file(
                "DEBUG",
                f"Не хватает монет на игрушку: {cat['money']} < 15"
            )
            print("=" * 50)
            print("Недостаточно монет!")
        wait_for_enter()
        clear_console()

    def buy_dreamies():
        if cat["money"] >= 10:
            cat["money"] -= 10
            cat["happiness"] += 10
            cat["satiety"] = clamp(cat["satiety"] + 25)
            cat["love"] += 10
            log_to_file(
                "DEBUG",
                f"Куплены Dreamies: money={cat['money']}, "
                f"happiness={cat['happiness']}, "
                f"satiety={cat['satiety']}, love={cat['love']}"
            )
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
            log_to_file(
                "DEBUG",
                f"Не хватает монет на Dreamies: {cat['money']} < 10"
            )
            print("=" * 50)
            print("Недостаточно монет!")
        wait_for_enter()
        clear_console()

    def buy_catnip():
        if cat["money"] >= 20:
            cat["money"] -= 20
            cat["happiness"] += 30
            cat["satiety"] = clamp(cat["satiety"] + 5)
            cat["love"] += 20
            cat["health"] -= 5
            log_to_file(
                "DEBUG",
                f"Куплена кошачья мята: money={cat['money']}, "
                f"happiness={cat['happiness']}, "
                f"satiety={cat['satiety']}, love={cat['love']}, "
                f"health={cat['health']}"
            )
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
            log_to_file(
                "DEBUG",
                f"Не хватает монет на мяту: {cat['money']} < 20"
            )
            print("=" * 50)
            print("Недостаточно монет!")
        wait_for_enter()
        clear_console()

    shop_actions = {
        1: buy_toy,
        2: buy_dreamies,
        3: buy_catnip,
    }

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

        if choice == 0:
            print("=" * 50)
            print("Вы вышли из магазина")
            log_to_file(
                "DEBUG", f"Выход из магазина: money={cat['money']}"
            )
            wait_for_enter()
            clear_console()
            return
        elif choice in shop_actions:
            shop_actions[choice]()
        else:
            # Не должно случиться из-за safe_choice
            continue


@log
def action_outside(cat: CatState):
    """Действие: выпустить кота на улицу."""
    log_to_file(
        "DEBUG",
        f"До прогулки: satiety={cat['satiety']}, "
        f"happiness={cat['happiness']}, love={cat['love']}"
    )

    if cat["satiety"] <= 15:
        log_to_file(
            "DEBUG",
            f"Кот слишком голоден для прогулки: satiety={cat['satiety']} <= 15"
        )
        print("=" * 50)
        print(f"{cat['name']} слишком голоден для прогулки!")
        wait_and_clear()
        return

    cat["happiness"] += 25
    cat["love"] += 10
    cat["satiety"] -= 15

    log_to_file(
        "DEBUG",
        f"После прогулки: satiety={cat['satiety']}, "
        f"happiness={cat['happiness']}, love={cat['love']}"
    )

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


@log
def action_work(cat: CatState):
    """Действие: заработать монеты."""
    log_to_file(
        "DEBUG",
        f"До работы: energy={cat['energy']}, money={cat['money']}, "
        f"happiness={cat['happiness']}"
    )

    if cat["energy"] <= 10:
        log_to_file(
            "DEBUG",
            f"Недостаточно энергии для работы: {cat['energy']} <= 10"
        )
        print("=" * 50)
        print(f"У {cat['name']}а слишком мало энергии для работы!")
        wait_and_clear()
        return

    cat["energy"] -= 10
    earned = random.randint(10, 25)
    cat["money"] += earned
    cat["happiness"] -= 5

    log_to_file(
        "DEBUG",
        f"После работы: energy={cat['energy']}, money={cat['money']}, "
        f"happiness={cat['happiness']}, earned={earned}"
    )

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


@log
def action_vet(cat: CatState):
    """Действие: сходить к ветеринару (остаётся на экране до выхода)."""
    log_to_file(
        "DEBUG",
        f"Вход в клинику: health={cat['health']}, money={cat['money']}"
    )
    clear_console()

    def vitamins():
        if cat["money"] >= 30:
            cat["money"] -= 30
            cat["health"] = clamp(cat["health"] + 20)
            cat["satiety"] = clamp(cat["satiety"] + 5)
            log_to_file(
                "DEBUG",
                f"Куплены витамины: money={cat['money']}, "
                f"health={cat['health']}, satiety={cat['satiety']}"
            )
            print("=" * 50)
            print(f"{cat['name']} принял витамины!")
            print("-30 монет, +20 здоровья, +5 сытости")
            print(
                f"Теперь: монеты {cat['money']}, "
                f"здоровье {cat['health']}, сытость {cat['satiety']}"
            )
        else:
            log_to_file(
                "DEBUG",
                f"Не хватает монет на витамины: {cat['money']} < 30"
            )
            print("=" * 50)
            print("Недостаточно монет!")
        wait_for_enter()
        clear_console()

    def treatment():
        if cat["money"] >= 50:
            cat["money"] -= 50
            cat["health"] = clamp(cat["health"] + 40)
            log_to_file(
                "DEBUG",
                f"Проведено лечение: money={cat['money']}, "
                f"health={cat['health']}"
            )
            print("=" * 50)
            print(f"{cat['name']} прошёл лечение!")
            print("-50 монет, +40 здоровья")
            print(
                f"Теперь: монеты {cat['money']}, "
                f"здоровье {cat['health']}"
            )
        else:
            log_to_file(
                "DEBUG",
                f"Не хватает монет на лечение: {cat['money']} < 50"
            )
            print("=" * 50)
            print("Недостаточно монет!")
        wait_for_enter()
        clear_console()

    def emergency():
        if cat["money"] >= 80:
            cat["money"] -= 80
            cat["health"] = 100
            log_to_file(
                "DEBUG",
                f"Экстренная помощь: money={cat['money']}, "
                f"health={cat['health']}"
            )
            print("=" * 50)
            print("Экстренная помощь!")
            print("-80 монет, здоровье восстановлено до 100%")
            print(
                f"Теперь: монеты {cat['money']}, "
                f"здоровье {cat['health']}"
            )
        else:
            log_to_file(
                "DEBUG",
                f"Не хватает монет на экстренную помощь: "
                f"{cat['money']} < 80"
            )
            print("=" * 50)
            print("Недостаточно монет!")
        wait_for_enter()
        clear_console()

    vet_actions = {
        1: vitamins,
        2: treatment,
        3: emergency,
    }

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

        if choice == 0:
            print("=" * 50)
            print("Вы вышли из клиники")
            log_to_file(
                "DEBUG",
                f"Выход из клиники: health={cat['health']}, "
                f"money={cat['money']}"
            )
            wait_for_enter()
            clear_console()
            return
        elif choice in vet_actions:
            vet_actions[choice]()
        else:
            continue


@log
def action_stats(cat: CatState):
    """Действие: показать статистику (остаётся на экране)."""
    log_to_file(
        "DEBUG",
        f"Показ статистики: день={cat['day']}, имя={cat['name']}, "
        f"здоровье={cat['health']}"
    )
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
    wait_for_enter()
    clear_console()


@log
def action_settings(cat: CatState):
    """Действие: настройки (остаётся на экране до выхода)."""
    global SCREEN_CLEAR_DELAY
    log_to_file("DEBUG", "Вход в настройки")
    clear_console()

    def change_name():
        new_name = input("Введите новое имя для кота: ")
        log_to_file(
            "INFO",
            f"Имя кота изменено с '{cat['name']}' на '{new_name}'"
        )
        cat["name"] = new_name
        print("=" * 50)
        print(f"Теперь имя кота: {cat['name']}")
        wait_for_enter()
        clear_console()

    def reset_game():
        if os.path.exists(SAVE_FILE):
            os.remove(SAVE_FILE)
            log_to_file(
                "WARNING",
                f"Сохранение игры удалено! Путь: {SAVE_FILE}"
            )
            print("Сохранение игры удалено!")
            print("Завершение работы...")
            time.sleep(3)
            sys.exit()
        else:
            log_to_file(
                "DEBUG",
                "Не удалось удалить сохранение: файл не найден"
            )
            print("=" * 50)
            print("Не удалось удалить сохранение!")
            wait_for_enter()
            clear_console()

    def about():
        log_to_file("DEBUG", "Показана информация об игре")
        print("=" * 50)
        print(f"Digital Cat {VERSION}")
        print(f"Автор: {AUTHOR}")
        print(f"Лицензия: {LICENSE}")
        print("Котов накормлено: бесконечность")
        print("Особая благодарность: коту, который вдохновил")
        wait_for_enter()
        clear_console()

    def change_speed():
        global SCREEN_CLEAR_DELAY
        print("=" * 50)
        print(f"Текущая задержка: {SCREEN_CLEAR_DELAY} сек.")
        try:
            new_delay = float(
                input("Введите новую задержку (0.5 - 5.0): ")
            )
            if 0.5 <= new_delay <= 5.0:
                log_to_file(
                    "INFO",
                    f"Задержка очистки экрана изменена с "
                    f"{SCREEN_CLEAR_DELAY} на {new_delay}"
                )
                SCREEN_CLEAR_DELAY = new_delay  # убрал повторный global
                print(
                    f"Задержка изменена на {SCREEN_CLEAR_DELAY} сек."
                )
            else:
                print("Ошибка! Введите число от 0.5 до 5.0")
        except ValueError:
            print("Ошибка! Это не число.")
        wait_for_enter()
        clear_console()

    settings_actions = {
        1: change_name,
        2: reset_game,
        3: about,
        4: change_speed,
    }

    while True:
        print("=" * 50)
        print("Вы в настройках")
        print("=" * 50)
        print("0. Выйти")
        print("1. Сменить имя кота")
        print("2. Сбросить игру")
        print("3. О игре")
        print("4. Изменить скорость очистки экрана")

        choice = safe_choice("Выберите действие: ", 0, 4)

        if choice == 0:
            print("=" * 50)
            print("Вы вышли из настроек")
            log_to_file("DEBUG", "Выход из настроек")
            wait_for_enter()
            clear_console()
            return
        elif choice in settings_actions:
            settings_actions[choice]()
        else:
            continue


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
    # Очищаем лог-файл при запуске
    try:
        os.makedirs(os.path.dirname(LOG_FILE), exist_ok=True)
        with open(LOG_FILE, "w", encoding="utf-8") as f:
            f.write("")
    except (IOError, OSError):
        pass

    log_to_file("INFO", "=" * 50)
    log_to_file("INFO", "ИГРА ЗАПУЩЕНА")
    log_to_file("INFO", f"Путь к сохранениям: {SAVE_FILE}")
    log_to_file("INFO", f"Путь к логам: {LOG_FILE}")
    log_to_file("INFO", "=" * 50)

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
    print("\n" + "=" * 50)
    print("Привет! Ты попал в игру Digital Cat.")
    print("=" * 50)

    saved = load_game()
    if saved is not None and saved.get("is_alive", False):
        choice = input("Найдено сохранение. Загрузить? (да/нет): ").lower().strip()
        if choice in ("да", "д", "yes", "y"):
            cat = saved
            log_to_file(
                "INFO",
                f"Сохранение загружено: день={cat['day']}, имя={cat['name']}"
            )
            clear_console()
            print(
                f"Сохранение загружено! День {cat['day']}, "
                f"{cat['name']} ждёт вас."
            )
            print("Отличный выбор!")
            time.sleep(1)
            clear_console()
        else:
            cat["name"] = input("Придумай имя своему питомцу: ").strip()
            log_to_file("INFO", f"Создан новый кот с именем: {cat['name']}")
            clear_console()
    else:
        cat["name"] = input("Для начала придумай имя своему питомцу: ").strip()
        log_to_file("INFO", f"Создан новый кот с именем: {cat['name']}")
        clear_console()

    main_actions = {
        "0": lambda: None,
        "1": action_feed,
        "2": action_pet,
        "3": action_play,
        "4": action_clean,
        "5": action_sleep,
        "6": action_shop,
        "7": action_outside,
        "8": action_work,
        "9": action_vet,
        "10": action_stats,
        "11": action_settings,
    }

    try:
        while cat["is_alive"]:
            apply_clamp(cat)

            if is_dead(cat):
                print("=" * 50)
                print(f"{cat['name']} умер...")
                print(f"Игра длилась {cat['day']} дней")
                log_to_file(
                    "WARNING",
                    f"ИГРА ОКОНЧЕНА: кот умер на {cat['day']} дне"
                )
                time.sleep(2)
                break

            if cat["day"] >= 100:
                print("=" * 50)
                print("ПОЗДРАВЛЯЮ! ТЫ ПРОШЁЛ ИГРУ!")
                print("=" * 50)
                log_to_file(
                    "INFO",
                    f"ИГРА ПРОЙДЕНА! День {cat['day']}, имя {cat['name']}"
                )
                cat["is_alive"] = False
                save_game(cat)
                time.sleep(2)
                break

            show_welcome_screen()
            print("\n" + "=" * 50)
            show_menu()

            random_event(cat)

            user_choice = input("Выберите действие от 0 до 11: ").strip()

            if user_choice == "0":
                print("=" * 50)
                save_game(cat)
                log_to_file(
                    "INFO",
                    "Игра завершена пользователем (выход из меню)"
                )
                print("До встречи!")
                return
            elif user_choice in main_actions:
                main_actions[user_choice](cat)
            else:
                print("=" * 50)
                print("Введите число от 0 до 11")
                log_to_file("DEBUG", f"Неверный ввод: {user_choice}")
                wait_and_clear()
                continue

            apply_clamp(cat)
            if is_dead(cat):
                print("=" * 50)
                print(f"{cat['name']} умер...")
                print(f"Игра длилась {cat['day']} дней")
                log_to_file(
                    "WARNING",
                    f"ИГРА ОКОНЧЕНА: кот умер на {cat['day']} дне"
                )
                time.sleep(2)
                break

            save_game(cat)

    except KeyboardInterrupt:
        print("=" * 50)
        save_game(cat)
        log_to_file("INFO", "Игра прервана пользователем (Ctrl+C)")
        print("Прогресс сохранён. До встречи!")
        return

    if os.path.exists(SAVE_FILE):
        os.remove(SAVE_FILE)
        log_to_file(
            "INFO",
            f"Файл сохранения удалён при завершении игры: {SAVE_FILE}"
        )

    print("Игра окончена!")
    log_to_file("INFO", "ИГРА ОКОНЧЕНА (полностью)")
    log_to_file("INFO", "=" * 50)


if __name__ == "__main__":
    main()