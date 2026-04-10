"""Действия кота (кормление, игра, сон и т.д.)."""
import random
import time
from stats import update_stats


def feed(cat):
    """Покормить кота."""
    if cat["satiety"] >= 100:
        print(f"{cat['name']} уже сыт!")
        return
    if cat["money"] < 5:
        print("Недостаточно монет!")
        return

    cat["money"] -= 5
    cat["satiety"] += 10
    update_stats(cat)
    print(f"Вы покормили {cat['name']}. -5 монет, +10 сытости.")
    print(f"Теперь монеты: {cat['money']}, сытость: {cat['satiety']}")

    if random.random() < 0.1:
        cat["health"] -= 10
        update_stats(cat)
        print(f"{cat['name']} стошнило. -10 здоровья.")
        print(f"Теперь здоровье: {cat['health']}")


def pet(cat):
    """Погладить кота."""
    if cat["happiness"] >= 100 and cat["love"] >= 100:
        print(f"{cat['name']} уже счастлив и очень любит вас!")
    elif cat["happiness"] >= 100:
        print(f"{cat['name']} уже счастлив!")
    elif cat["love"] >= 100:
        print(f"{cat['name']} уже достаточно любит вас!")
    else:
        cat["happiness"] += 1
        cat["love"] += 1
        update_stats(cat)
        print(f"Вы погладили {cat['name']}. +1 к счастью, +1 к любви.")
        print(f"Теперь счастье: {cat['happiness']}, любовь: {cat['love']}")


def play(cat):
    """Поиграть с котом."""
    if cat["energy"] <= 0:
        print(f"У {cat['name']} недостаточно энергии!")
        return
    if cat["happiness"] >= 100:
        print(f"{cat['name']} уже счастлив!")
        return

    cat["energy"] -= 5
    cat["happiness"] += 10
    update_stats(cat)
    print(f"Вы поиграли с {cat['name']}. -5 энергии, +10 счастья.")
    print(f"Теперь энергия: {cat['energy']}, счастье: {cat['happiness']}")


def clean_tray(cat):
    """Убрать лоток."""
    if cat["dirty_tray"]:
        cat["dirty_tray"] = False
        cat["love"] += 5
        cat["happiness"] += 5
        update_stats(cat)
        print(f"Вы убрали лоток за {cat['name']}. +5 любви, +5 счастья.")
        print(f"Теперь любовь: {cat['love']}, счастье: {cat['happiness']}")
    else:
        print("Лоток уже чистый.")


def sleep(cat):
    """Уложить кота спать."""
    if cat["energy"] >= 100:
        print(f"У {cat['name']} уже достаточно энергии!")
        return

    print(f"Вы уложили {cat['name']} спать...")

    if random.random() < 0.2:
        cat["happiness"] -= 10
        update_stats(cat)
        print(f"{cat['name']} убежал!")
        return

    print(f"{cat['name']} спит...")
    time.sleep(3)

    cat["energy"] += 25
    update_stats(cat)

    # Смена фазы дня
    phases = {"утро": "день", "день": "вечер", "вечер": "ночь", "ночь": "утро"}
    cat["day_phase"] = phases[cat["day_phase"]]

    if cat["day_phase"] == "утро":
        cat["day"] += 1
        cat["love"] += 10
        update_stats(cat)
        print(f"Наступило утро! День {cat['day']}")

    print(f"{cat['name']} проснулся. +25 энергии")
    print(f"Теперь энергия: {cat['energy']}")


def go_outside(cat):
    """Выпустить кота на улицу."""
    cat["happiness"] += 25
    cat["love"] += 10
    cat["satiety"] -= 15
    update_stats(cat)
    print("Кот вышел на улицу...")
    time.sleep(3)
    print(f"+25 счастья, +10 любви, -15 сытости")
    print(f"Теперь счастье: {cat['happiness']}, любовь: {cat['love']}, сытость: {cat['satiety']}")


def work(cat):
    """Заработать монеты."""
    if cat["energy"] < 10:
        print(f"У {cat['name']} слишком мало энергии для работы!")
        return

    cat["energy"] -= 10
    earned = random.randint(10, 25)
    cat["money"] += earned
    cat["happiness"] -= 5
    update_stats(cat)
    print(f"{cat['name']} помог с работой! -10 энергии, +{earned} монет, -5 счастья")
    print(f"Теперь энергия: {cat['energy']}, монеты: {cat['money']}, счастье: {cat['happiness']}")
