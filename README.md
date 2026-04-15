# Digital Cat Game 🐱

[![Python Version](https://img.shields.io/badge/python-3.x-blue.svg)](https://www.python.org/)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)

A virtual pet — cat simulator written in Python. Take care of your cat, play with it, buy treats, and monitor its health!

## 📋 Table of Contents
- [Description](#description)
- [How to Play](#how-to-play)
- [Installation](#installation)
- [Controls](#controls)
- [Project Files](#project-files)
- [Author](#author)

## 📝 Description

**Digital Cat** is a text-based game where you adopt a virtual cat and take care of it. Your cat has several characteristics:
- 🍖 **Сытость (Satiety)** — The cat needs food
- 😊 **Счастье (Happiness)** — The cat wants to play
- ⚡ **Энергия (Energy)** — The cat gets tired
- ❤️ **Здоровье (Health)** — The cat can get sick
- 💰 **Монеты (Coins)** — Can be used to buy items
- 💕 **Любовь (Love)** — The cat grows attached to you

Random events happen every day — the cat might find coins, dirty the litter box, or just meow.

**Win/Lose Conditions:**
- 🏆 **Victory**: Survive 100 days with your cat!
- 💀 **Defeat**: If any of your cat's parameters reaches 0, the game ends.

**Autosave**: The game automatically saves your progress to `save.dat` after each action. You can continue your game from where you left off.

## 🎮 How to Play

1. Run the game
2. Name your pet
3. Choose actions from the menu
4. Keep the cat from dying of hunger or illness

## ⚙️ Installation

### Option 1: Download ZIP
1. Click the green **"Code"** button on this page
2. Select **"Download ZIP"**
3. Extract the archive
4. Run the game: `python Digital_Cat.py`

### Option 2: Clone repository
    git clone https://github.com/FelineFantasy/Digital_Cat.git
    cd Digital_Cat
    python Digital_Cat.py

## 🎮 Controls

The main menu provides several actions:
- Feed the cat
- Play with the cat
- Let the cat sleep
- Check health
- Buy treats
- And more!

## 📁 Project Files

    Digital_Cat/
    ├── Digital_Cat.py          # Main program file
    └── README.md               # Documentation

## 👤 Author

**FelineFantasy**

License: MIT