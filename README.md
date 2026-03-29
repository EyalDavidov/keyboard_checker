# ⌨ Keyboard Checker

A standalone desktop application for **keyboard testing and hit counting**. Visualises a full keyboard layout on screen and tracks how many times each key has been pressed — useful for testing new keyboards, checking for dead keys, or just satisfying your curiosity.

![Python](https://img.shields.io/badge/Python-3.10%2B-blue?logo=python&logoColor=white)
![Tkinter](https://img.shields.io/badge/UI-Tkinter-green)
![pynput](https://img.shields.io/badge/Input-pynput-orange)

---

## ✨ Features

| Feature | Description |
|---|---|
| **Visual Keyboard** | Canvas-drawn 101/104-key layout with rounded, proportionally-sized keys |
| **Per-Key Counter** | Each key displays its own hit count (bottom-right corner) |
| **Live Flash** | Keys flash red on press for instant visual feedback |
| **Total Counter** | Running total of all key presses shown in the header |
| **Start / Stop** | Toggle global key capture on and off |
| **Reset** | Zero all counters with one click |
| **System Key Capture** | Captures Tab, Space, CapsLock, etc. without losing app focus |
| **Dark Mode** | Modern dark aesthetic with teal/red accent colours |

---

## 🚀 Getting Started

### Prerequisites

- **Python 3.10+**
- **pynput** library

### Installation

```bash
# Clone the repository
git clone https://github.com/EyalDavidov/keyboard_checker.git
cd keyboard_checker

# Install dependencies
pip install pynput
```

### Running

```bash
python keyboard_checker.py
```

---

## 🎮 Usage

1. Click **▶ Start** to begin capturing key presses globally.
2. Press any key — the corresponding visual key flashes and its counter increments.
3. Click **■ Stop** to pause listening.
4. Click **↺ Reset** to zero all counters.
5. Close the window to exit.

> **Note:** While listening is active, `suppress=True` is used to intercept all keyboard input (including system keys like Tab and Alt). Click **Stop** before switching to other applications.

---

## 🖼 Layout

The keyboard is rendered as a Canvas illustration with 6 rows:

| Row | Keys |
|---|---|
| **Function** | Esc · F1–F12 · PrtSc · ScrLk · Pause |
| **Number** | \`~ · 1–0 · -_ · =+ · Backspace · Ins · Home · PgUp |
| **QWERTY** | Tab · Q–P · \[{ · \]} · \\| · Del · End · PgDn |
| **Home** | Caps · A–L · ;: · '" · Enter |
| **Shift** | Shift · Z–M · ,< · .> · /? · Shift · ↑ |
| **Bottom** | Ctrl · Win · Alt · Space · Alt · Win · Mn · Ctrl · ← ↓ → |

---

## 🛠 Tech Stack

- **Python 3** — core language
- **Tkinter** — built-in GUI toolkit (Canvas for key rendering)
- **pynput** — global keyboard event listener

---

## 📄 License

This project is open source and available under the [MIT License](LICENSE).
