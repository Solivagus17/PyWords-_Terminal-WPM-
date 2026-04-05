<div align="center">

<pre>
 ██████╗ ██╗   ██╗    ██╗    ██╗ ██████╗ ██████╗ ██████╗ ███████╗
 ██╔══██╗╚██╗ ██╔╝    ██║    ██║██╔═══██╗██╔══██╗██╔══██╗██╔════╝
 ██████╔╝ ╚████╔╝     ██║ █╗ ██║██║   ██║██████╔╝██║  ██║███████╗
 ██╔═══╝   ╚██╔╝      ██║███╗██║██║   ██║██╔══██╗██║  ██║╚════██║
 ██║        ██║       ╚███╔███╔╝╚██████╔╝██║  ██║██████╔╝███████║
 ╚═╝        ╚═╝        ╚══╝╚══╝  ╚═════╝ ╚═╝  ╚═╝╚═════╝ ╚══════╝
</pre>

### ✦ the cosmic typing benchmark ✦

[![Python](https://img.shields.io/badge/Python-3.7%2B-blue?style=for-the-badge&logo=python&logoColor=white)](https://python.org)
[![Platform](https://img.shields.io/badge/Platform-Linux%20%7C%20macOS%20%7C%20Windows-magenta?style=for-the-badge)](#installation)
[![License](https://img.shields.io/badge/License-MIT-green?style=for-the-badge)](LICENSE)


*A terminal typing benchmark that lives among the stars — measure your speed, sharpen your accuracy, and type through the cosmos.*

</div>

---

## ✦ Preview

<div align="center">

### Main Interface
![PyWords Terminal UI](https://raw.githubusercontent.com/Solivagus17/PyWords-_Terminal-WPM-/main/PyWord_UI_Terminal.png)

### Typing with Random Passages
![Random Passage](https://raw.githubusercontent.com/Solivagus17/PyWords-_Terminal-WPM-/main/PyWords_Random_Para.png)

### Typing with a Book Loaded
![Book Loaded](https://raw.githubusercontent.com/Solivagus17/PyWords-_Terminal-WPM-/main/PyWords_Book_Loaded.png)

### Pride & Prejudice — Custom Book Passage
![Pride and Prejudice Passage](https://raw.githubusercontent.com/Solivagus17/PyWords-_Terminal-WPM-/main/PyWords_Pride%20and%20Prejudice_Para.png)

</div>

---

## ✦ Features

| Feature | Details |
|---|---|
| 📊 **Live WPM Tracking** | Real-time words-per-minute calculated as you type |
| 🎯 **Accuracy Meter** | Tracks correct vs incorrect keystrokes live |
| ⏱️ **Configurable Durations** | 30s, 60s, 90s presets — or any value from 5–300s via CLI |
| 📚 **15 Built-in Passages** | Curated texts from literature, science, philosophy & code |
| 📖 **Custom Book Upload** | Load any `.txt` book and type through its paragraphs |
| 🌌 **Cosmic Starfield** | Animated background stars that drift across your terminal |
| 🐛 **Animated Fireflies** | Glowing fireflies that wander while you type |
| 🐱 **Walking Cats** | Pixel cats that stroll across the bottom of the screen |
| 🎨 **Colour-coded Feedback** | Green for correct, red for errors — instantly visible |
| 🖥️ **Cross-platform** | Linux, macOS, Windows (with `windows-curses`) |

---

## ✦ Installation

### 1 — Clone the Repository

```bash
git clone https://github.com/Solivagus17/PyWords-_Terminal-WPM-.git
cd PyWords-_Terminal-WPM-
```

### 2 — Install Dependencies

PyWords uses Python's built-in `curses` module — no external dependencies on Linux/macOS.

**Linux / macOS**
```bash
# No extra install needed — curses ships with Python
python3 PyWords.py
```

**Windows**
```bash
pip install windows-curses
python PyWords.py
```

> **Requires Python 3.7 or higher.**

---

## ✦ Usage

### Quick Start

```bash
python3 PyWords.py
```

This launches PyWords with the default **60-second** timer and built-in passages.

### Command-line Options

```bash
python3 PyWords.py [--time SECONDS] [--book PATH]
```

| Flag | Short | Default | Description |
|------|-------|---------|-------------|
| `--time` | `-t` | `60` | Test duration in seconds (5–300) |
| `--book` | `-b` | — | Absolute path to a `.txt` file to use as passage source |

**Examples:**

```bash
# 30-second test
python3 PyWords.py --time 30

# 90-second test
python3 PyWords.py -t 90

# Load a book from an absolute path
python3 PyWords.py --book /home/yourname/books/moby_dick.txt

# Combine both
python3 PyWords.py --time 60 --book /Users/yourname/Downloads/pride_and_prejudice.txt
```

---

## ✦ Keyboard Controls

### Splash Screen

| Key | Action |
|-----|--------|
| `Enter` | Start the test |
| `U` | Upload / switch book |
| `T` | Toggle timer duration |
| `←` | Set timer to 30s |
| `→` | Set timer to 60s |
| `↑` | Set timer to 90s |
| `Esc` | Quit |

### During the Test

| Key | Action |
|-----|--------|
| *Any printable key* | Type — timer starts on first keystroke |
| `Backspace` | Delete last character |
| `Esc` | Abort and return to splash |

### Results Screen

| Key | Action |
|-----|--------|
| `R` | Restart with a new passage |
| `Esc` | Return to splash screen |

---

## ✦ Loading a Custom Book

PyWords can turn any plain-text `.txt` book into your typing source. Here's how to do it step by step.

### Step 1 — Get a `.txt` Book

Download a free book from [Project Gutenberg](https://www.gutenberg.org/) as a **Plain Text UTF-8** file.

### Step 2 — Find the Absolute Path

You need the **full absolute path** to the file — not a relative path like `./book.txt`.

**On Linux / macOS:**
```bash
# Navigate to where your book is saved, then run:
pwd
# Example output: /home/yourname/Downloads

# Your full path would be:
/home/yourname/Downloads/pride_and_prejudice.txt
```

Or use `realpath`:
```bash
realpath pride_and_prejudice.txt
# Output: /home/yourname/Downloads/pride_and_prejudice.txt
```

**On Windows:**
1. Open File Explorer and navigate to your book file
2. Hold `Shift` and **right-click** the file
3. Select **"Copy as path"**
4. Paste it — it will look like: `C:\Users\YourName\Downloads\pride_and_prejudice.txt`

> ⚠️ **Windows users:** Replace backslashes `\` with forward slashes `/` when passing the path to the script, or wrap it in quotes.

### Step 3 — Launch with the Book

**Via CLI (recommended):**
```bash
python3 PyWords.py --book /home/yourname/Downloads/pride_and_prejudice.txt
```

**Via the in-app prompt:**

From the splash screen, press `U`. PyWords will display a path input prompt:

![Paste Book Path](https://raw.githubusercontent.com/Solivagus17/PyWords-_Terminal-WPM-/main/PyWords_paste_book_path.png)

Type or paste your **full absolute path** and press `Enter`. PyWords will extract all paragraphs longer than 60 characters and use them as your passage pool.

> **Tip:** On most terminals you can paste with `Ctrl+Shift+V` (Linux), `Cmd+V` (macOS), or right-click → Paste (Windows).

---

## ✦ How Stats Are Calculated

- **WPM** — `(characters typed ÷ 5) ÷ minutes elapsed` — the standard gross WPM formula
- **Accuracy** — percentage of keystrokes that matched the target passage character-for-character
- **Correct Words** — words where every character was typed correctly
- **Errors** — total number of wrong characters typed throughout the test

---

## ✦ Project Structure

```
PyWords-_Terminal-WPM-/
├── PyWords.py                        # The entire application — single file
├── LICENSE                           # MIT License
├── README.md                         # This file
├── PyWord_UI_Terminal.png            # Screenshot — splash screen
├── PyWords_Random_Para.png           # Screenshot — random passage mid-test
├── PyWords_Book_Loaded.png           # Screenshot — book mode mid-test
├── PyWords_Pride and Prejudice_Para.png  # Screenshot — P&P passage
└── PyWords_paste_book_path.png       # Screenshot — book path prompt
```

---

## ✦ Platform Notes

| OS | Status | Notes |
|----|--------|-------|
| Linux | ✅ Full support | `curses` built-in |
| macOS | ✅ Full support | `curses` built-in |
| Windows | ✅ Supported | Requires `pip install windows-curses` |
| WSL (Windows Subsystem for Linux) | ✅ Recommended on Windows | Works natively like Linux |

---

## ✦ License

Released under the [MIT License](LICENSE). Use it, fork it, type faster with it.

---

<div align="center">

✦ *Thanks for using PyWords — keep typing through the cosmos.* ✦

</div>
