"""
Keyboard Checker – Canvas-drawn keyboard illustration with per-key hit counters.
Tech: Python 3 · Tkinter · pynput
"""

import tkinter as tk
from tkinter import font as tkfont
from pynput import keyboard
import sys

# ─────────────────────────── colour palette ─────────────────────────── #
BG_MAIN       = "#111119"
BG_CANVAS     = "#1b1b2f"
BG_KEY        = "#252540"
BG_KEY_FLASH  = "#e94560"
OUTLINE_KEY   = "#3a3a5c"
FG_KEY        = "#c8c8da"
FG_COUNT      = "#0ff0b8"
FG_COUNT_ZERO = "#555570"
HEADER_FG     = "#e94560"
BTN_START_BG  = "#0cc0a0"
BTN_STOP_BG   = "#e94560"
BTN_RESET_BG  = "#f0a030"
BTN_FG        = "#ffffff"
STATUS_ON     = "#0cc0a0"
STATUS_OFF    = "#e94560"
FG_LABEL      = "#888899"

# ──────────────────────── keyboard layout data ──────────────────────── #
# (id, display_text, width_units)   1 unit = 50 px

ROWS = [
    # Row 0 — Function keys
    [
        ("escape",       "Esc",   1.0), None,
        ("f1","F1",1), ("f2","F2",1), ("f3","F3",1), ("f4","F4",1), None,
        ("f5","F5",1), ("f6","F6",1), ("f7","F7",1), ("f8","F8",1), None,
        ("f9","F9",1), ("f10","F10",1), ("f11","F11",1), ("f12","F12",1), None,
        ("print_screen","PrtSc",1), ("scroll_lock","ScrLk",1), ("pause","Pause",1),
    ],
    # Row 1 — Number row
    [
        ("`","`~",1), ("1","1!",1), ("2","2@",1), ("3","3#",1), ("4","4$",1),
        ("5","5%",1), ("6","6^",1), ("7","7&",1), ("8","8*",1), ("9","9(",1),
        ("0","0)",1), ("-","-_",1), ("=","=+",1), ("backspace","Backspace",2.0), None,
        ("insert","Ins",1), ("home","Home",1), ("page_up","PgUp",1),
    ],
    # Row 2 — QWERTY
    [
        ("tab","Tab",1.5),
        ("q","Q",1), ("w","W",1), ("e","E",1), ("r","R",1), ("t","T",1),
        ("y","Y",1), ("u","U",1), ("i","I",1), ("o","O",1), ("p","P",1),
        ("[","[{",1), ("]","]}",1), ("\\","\\|",1.5), None,
        ("delete","Del",1), ("end","End",1), ("page_down","PgDn",1),
    ],
    # Row 3 — Home row
    [
        ("caps_lock","Caps",1.75),
        ("a","A",1), ("s","S",1), ("d","D",1), ("f","F",1), ("g","G",1),
        ("h","H",1), ("j","J",1), ("k","K",1), ("l","L",1),
        (";",";:",1), ("'","'\"",1), ("enter","Enter",2.25),
    ],
    # Row 4 — Shift row
    [
        ("shift_l","Shift",2.25),
        ("z","Z",1), ("x","X",1), ("c","C",1), ("v","V",1), ("b","B",1),
        ("n","N",1), ("m","M",1), (",",",<",1), (".",".>",1), ("/","/?",1),
        ("shift_r","Shift",2.75), None,
        ("up","↑",1),
    ],
    # Row 5 — Bottom row
    [
        ("ctrl_l","Ctrl",1.25), ("win_l","Win",1.25), ("alt_l","Alt",1.25),
        ("space","",6.25),
        ("alt_r","Alt",1.25), ("win_r","Win",1.25), ("menu","Mn",1.25), ("ctrl_r","Ctrl",1.25), None,
        ("left","←",1), ("down","↓",1), ("right","→",1),
    ],
]

# Spacer widths (the None gaps) per row
GAP_PX = 12  # extra gap where None appears

# ───── pynput key → internal id mapping ───── #
SPECIAL_MAP = {
    keyboard.Key.esc: "escape",
    keyboard.Key.f1: "f1", keyboard.Key.f2: "f2", keyboard.Key.f3: "f3", keyboard.Key.f4: "f4",
    keyboard.Key.f5: "f5", keyboard.Key.f6: "f6", keyboard.Key.f7: "f7", keyboard.Key.f8: "f8",
    keyboard.Key.f9: "f9", keyboard.Key.f10: "f10", keyboard.Key.f11: "f11", keyboard.Key.f12: "f12",
    keyboard.Key.print_screen: "print_screen", keyboard.Key.scroll_lock: "scroll_lock",
    keyboard.Key.pause: "pause", keyboard.Key.backspace: "backspace",
    keyboard.Key.insert: "insert", keyboard.Key.home: "home", keyboard.Key.page_up: "page_up",
    keyboard.Key.tab: "tab", keyboard.Key.delete: "delete", keyboard.Key.end: "end",
    keyboard.Key.page_down: "page_down", keyboard.Key.caps_lock: "caps_lock",
    keyboard.Key.enter: "enter",
    keyboard.Key.shift_l: "shift_l", keyboard.Key.shift_r: "shift_r",
    keyboard.Key.shift: "shift_l",
    keyboard.Key.up: "up",
    keyboard.Key.ctrl_l: "ctrl_l", keyboard.Key.ctrl_r: "ctrl_r", keyboard.Key.ctrl: "ctrl_l",
    keyboard.Key.cmd_l: "win_l", keyboard.Key.cmd_r: "win_r", keyboard.Key.cmd: "win_l",
    keyboard.Key.alt_l: "alt_l", keyboard.Key.alt_r: "alt_r", keyboard.Key.alt: "alt_l",
    keyboard.Key.alt_gr: "alt_r",
    keyboard.Key.space: "space", keyboard.Key.menu: "menu",
    keyboard.Key.left: "left", keyboard.Key.down: "down", keyboard.Key.right: "right",
}

CHAR_TO_ID = {
    '`': '`', '~': '`', '1': '1', '!': '1', '2': '2', '@': '2', '3': '3', '#': '3',
    '4': '4', '$': '4', '5': '5', '%': '5', '6': '6', '^': '6', '7': '7', '&': '7',
    '8': '8', '*': '8', '9': '9', '(': '9', '0': '0', ')': '0', '-': '-', '_': '-',
    '=': '=', '+': '=', '[': '[', '{': '[', ']': ']', '}': ']', '\\': '\\', '|': '\\',
    ';': ';', ':': ';', "'": "'", '"': "'", ',': ',', '<': ',', '.': '.', '>': '.',
    '/': '/', '?': '/', ' ': 'space',
}


# ═══════════════════════════ Application ═══════════════════════════ #

class KeyboardChecker:
    UNIT     = 50        # px per 1-unit key width
    KEY_H    = 42        # key height
    GAP      = 4         # gap between keys
    RAD      = 6         # corner radius for rounded rects
    FLASH_MS = 200       # flash duration

    def __init__(self, root: tk.Tk):
        self.root = root
        self.root.title("Keyboard Checker")
        self.root.configure(bg=BG_MAIN)
        self.root.resizable(False, False)

        # Fonts
        self.fn_key   = tkfont.Font(family="Segoe UI", size=8)
        self.fn_count = tkfont.Font(family="Consolas",  size=8, weight="bold")
        self.fn_hdr   = tkfont.Font(family="Segoe UI", size=14, weight="bold")
        self.fn_btn   = tkfont.Font(family="Segoe UI", size=10, weight="bold")
        self.fn_stat  = tkfont.Font(family="Segoe UI", size=10)

        # Data
        self.counters: dict[str, int] = {}
        self.key_rects: dict[str, int]  = {}   # id -> canvas rect id
        self.key_texts: dict[str, int]  = {}   # id -> canvas text id (label)
        self.cnt_texts: dict[str, int]  = {}   # id -> canvas text id (counter)
        self.listening = False
        self.listener = None
        self.total = 0

        self._build_header()
        self._build_keyboard()
        self._build_controls()

    # ────────────── rounded rectangle helper ────────────── #
    def _round_rect(self, canvas, x1, y1, x2, y2, r, **kw):
        pts = [
            x1+r, y1,   x2-r, y1,
            x2,   y1,   x2,   y1+r,
            x2,   y2-r, x2,   y2,
            x2-r, y2,   x1+r, y2,
            x1,   y2,   x1,   y2-r,
            x1,   y1+r, x1,   y1,
        ]
        return canvas.create_polygon(pts, smooth=True, **kw)

    # ────────────── header ────────────── #
    def _build_header(self):
        f = tk.Frame(self.root, bg=BG_MAIN)
        f.pack(fill="x", padx=20, pady=(14, 6))

        tk.Label(f, text="⌨  Keyboard Checker", font=self.fn_hdr,
                 fg=HEADER_FG, bg=BG_MAIN).pack(side="left")

        # status
        self.lbl_dot = tk.Label(f, text="●", font=self.fn_stat, fg=STATUS_OFF, bg=BG_MAIN)
        self.lbl_dot.pack(side="right", padx=(0,4))
        self.lbl_status = tk.Label(f, text="Idle", font=self.fn_stat, fg=FG_LABEL, bg=BG_MAIN)
        self.lbl_status.pack(side="right")

        self.lbl_total = tk.Label(f, text="Total: 0", font=self.fn_stat,
                                  fg=FG_COUNT, bg=BG_MAIN)
        self.lbl_total.pack(side="right", padx=(0,24))

    # ────────────── keyboard canvas ────────────── #
    def _build_keyboard(self):
        # Calculate canvas size from layout
        max_w = 0
        for row in ROWS:
            w = 0
            for item in row:
                if item is None:
                    w += GAP_PX
                else:
                    _, _, wu = item
                    w += wu * self.UNIT + self.GAP
            if w > max_w:
                max_w = w

        canvas_w = int(max_w) + 20
        canvas_h = len(ROWS) * (self.KEY_H + self.GAP) + 16

        self.canvas = tk.Canvas(self.root, width=canvas_w, height=canvas_h,
                                bg=BG_CANVAS, bd=0, highlightthickness=0)
        self.canvas.pack(padx=16, pady=(4, 6))

        y = 8
        for row in ROWS:
            x = 10
            for item in row:
                if item is None:
                    x += GAP_PX
                    continue
                kid, disp, wu = item
                kw = int(wu * self.UNIT) - self.GAP
                self._draw_key(x, y, kw, self.KEY_H, kid, disp)
                x += kw + self.GAP
            y += self.KEY_H + self.GAP

    def _draw_key(self, x, y, w, h, kid, disp):
        self.counters[kid] = 0

        rect = self._round_rect(self.canvas, x, y, x + w, y + h,
                                 self.RAD, fill=BG_KEY, outline=OUTLINE_KEY, width=1)

        # Key label — top-left area
        txt = self.canvas.create_text(
            x + 6, y + 5, text=disp, anchor="nw",
            fill=FG_KEY, font=self.fn_key
        )

        # Counter — bottom-right area
        cnt = self.canvas.create_text(
            x + w - 6, y + h - 5, text="0", anchor="se",
            fill=FG_COUNT_ZERO, font=self.fn_count
        )

        self.key_rects[kid] = rect
        self.key_texts[kid] = txt
        self.cnt_texts[kid] = cnt

    # ────────────── controls ────────────── #
    def _build_controls(self):
        f = tk.Frame(self.root, bg=BG_MAIN)
        f.pack(pady=(4, 14))

        self.btn_start = self._btn(f, "▶  Start", BTN_START_BG, self._start)
        self.btn_stop  = self._btn(f, "■  Stop",  BTN_STOP_BG,  self._stop)
        self.btn_reset = self._btn(f, "↺  Reset", BTN_RESET_BG, self._reset)
        self.btn_stop.config(state="disabled")

    def _btn(self, parent, text, bg, cmd):
        b = tk.Button(parent, text=text, font=self.fn_btn,
                      bg=bg, fg=BTN_FG, activebackground=bg,
                      activeforeground=BTN_FG, bd=0,
                      padx=18, pady=5, cursor="hand2", command=cmd)
        b.pack(side="left", padx=8)
        return b

    # ────────────── flash / update ────────────── #
    def _flash(self, kid):
        if kid not in self.key_rects:
            return
        self.canvas.itemconfigure(self.key_rects[kid], fill=BG_KEY_FLASH, outline=BG_KEY_FLASH)
        self.canvas.itemconfigure(self.key_texts[kid], fill="#ffffff")
        self.canvas.itemconfigure(self.cnt_texts[kid], fill="#ffffff")
        self.root.after(self.FLASH_MS, self._unflash, kid)

    def _unflash(self, kid):
        if kid not in self.key_rects:
            return
        self.canvas.itemconfigure(self.key_rects[kid], fill=BG_KEY, outline=OUTLINE_KEY)
        self.canvas.itemconfigure(self.key_texts[kid], fill=FG_KEY)
        count = self.counters.get(kid, 0)
        self.canvas.itemconfigure(self.cnt_texts[kid],
                                  fill=FG_COUNT if count > 0 else FG_COUNT_ZERO)

    def _increment(self, kid):
        if kid not in self.counters:
            return
        self.counters[kid] += 1
        self.canvas.itemconfigure(self.cnt_texts[kid], text=str(self.counters[kid]))
        self.total += 1
        self.lbl_total.config(text=f"Total: {self.total}")

    # ────────────── pynput resolve ────────────── #
    def _resolve(self, key):
        if isinstance(key, keyboard.Key):
            return SPECIAL_MAP.get(key)
        if hasattr(key, "char") and key.char is not None:
            ch = key.char
            if ch in CHAR_TO_ID:
                return CHAR_TO_ID[ch]
            if ch.lower().isalpha():
                return ch.lower()
        if hasattr(key, "vk") and key.vk is not None:
            vk = key.vk
            if 65 <= vk <= 90:
                return chr(vk).lower()
            if 48 <= vk <= 57:
                return chr(vk)
        return None

    def _on_press(self, key):
        if not self.listening:
            return
        kid = self._resolve(key)
        if kid is None:
            return
        self.root.after(0, self._increment, kid)
        self.root.after(0, self._flash, kid)

    # ────────────── button callbacks ────────────── #
    def _start(self):
        if self.listening:
            return
        self.listening = True
        self.lbl_status.config(text="Listening")
        self.lbl_dot.config(fg=STATUS_ON)
        self.btn_start.config(state="disabled")
        self.btn_stop.config(state="normal")

        self.listener = keyboard.Listener(on_press=self._on_press, suppress=True)
        self.listener.daemon = True
        self.listener.start()

    def _stop(self):
        if not self.listening:
            return
        self.listening = False
        self.lbl_status.config(text="Idle")
        self.lbl_dot.config(fg=STATUS_OFF)
        self.btn_start.config(state="normal")
        self.btn_stop.config(state="disabled")
        if self.listener:
            self.listener.stop()
            self.listener = None

    def _reset(self):
        for kid in self.counters:
            self.counters[kid] = 0
            self.canvas.itemconfigure(self.cnt_texts[kid], text="0", fill=FG_COUNT_ZERO)
        self.total = 0
        self.lbl_total.config(text="Total: 0")

    def on_close(self):
        self._stop()
        self.root.destroy()


# ═════════════════════════════ main ═════════════════════════════ #
def main():
    root = tk.Tk()
    try:
        root.iconbitmap(default="")
    except tk.TclError:
        pass

    app = KeyboardChecker(root)
    root.protocol("WM_DELETE_WINDOW", app.on_close)
    root.mainloop()


if __name__ == "__main__":
    main()
