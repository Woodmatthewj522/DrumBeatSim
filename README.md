# 🥁 Mini Drum Hero for PC

A lightweight rhythm game inspired by Guitar Hero — built entirely in Python with Pygame.

Created by: mw
Date: 09/17/2025
IDE: Visual Studio 2022

# 🎵 Overview

Mini Drum Hero is a simple, fun rhythm game where you hit notes in time with a song.
You can play, pause, and even record your own note charts synced to your favorite track.

The game includes full gameplay logic, scoring, miss tracking, and a chart recording system that saves to JSON for replay.

# ✨ Features

🥁 3 playable lanes (R, H, and B keys)

🎶 Built-in recording mode to create custom note charts synced to music

💾 Chart saving/loading with JSON (recorded_chart.json)

🎯 Graded hit accuracy (Perfect / Good / Ok / Miss)

💔 Fail after too many misses (10 max)

⏸️ Pause and resume music

💡 Clean visual layout and easy to extend

# 🧩 Controls
Key	Action
ENTER	Start game (from menu) / Restart (after Game Over)
ESC	Quit game (after Game Over)
R	Hit note (Lane 1) / Enter Recording mode (when paused)
H	Hit note (Lane 2)
B	Hit note (Lane 3)
SPACE	Pause / Resume game
P	Pause / Resume game (alternate)
SPACE (in recording mode)	Stop and save recorded chart
#
# 🎮 Game Modes
▶️ Play Mode
- *Record mode needs fixed*
#
- Play along to a pre-made chart (recorded_chart.json).

- Notes scroll down — hit them as they reach the hit zone.

- Score is based on timing accuracy.

- Missing too many notes ends the game.
#
# 🎙️ Recording Mode - *Needs Fixed* 10/25

- Enter by pausing during play and pressing R.

- Press R, H, or B while the song plays to record note timings.

- Press SPACE when done — the chart saves to recorded_chart.json.

- Replay the new chart from the main menu!

# 📂 File Structure
mini_drum_hero/

├── mini_drum_hero.py        # Main game file

├── song1.mp3                # Music file used for gameplay

├── recorded_chart.json      # Auto-generated note chart (after recording)

├── README.md                # This file

# ⚙️ Requirements

Python Version: 3.8+

# Dependencies:

pygame

# Install it using:

pip install pygame
#
# ▶️ How to Run

Place your desired MP3 file in the same directory and name it song1.mp3.

# Run the game:

python mini_drum_hero.py

Press ENTER on the menu to start playing.

(Optional) Enter recording mode to make your own chart.

# 🧠 Scoring System
Hit Timing	Points
Perfect	100
Good	60
Ok	20
Miss	0

*Timing is based on how close the note is to the hit line when pressed.*

# 💡 Tips

Stay on rhythm — the better your timing, the higher your score!

You can replace song1.mp3 with any song (just keep the name the same).

To create a custom chart, record with your chosen track and save as recorded_chart.json.

# 🧩 Future Enhancements

Record mode fixes

Add visual feedback for hits (animations or flash effects)

Multi-song menu

Difficulty modes

Lane customization and colors

Combo streaks and multiplier scoring

# 📜 License

This project is free for personal and educational use, good base to modify/add to!
