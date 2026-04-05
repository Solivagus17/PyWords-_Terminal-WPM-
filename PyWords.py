#!/usr/bin/env python3
"""
PyWords.py — Cosmic Terminal Typing Benchmark
A feature-rich WPM counter with a cosmic UI, animated fireflies & cats,
book-upload support, and 15 built-in passages.
On Windows, requires: pip install windows-curses
"""


import time
import curses
import random
import argparse
import sys
import os
import math
import re
from typing import List, Optional, Tuple

# Directory that contains this script — book files are resolved relative to this
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))

# ─────────────────────────────────────────────────────────────────────────────
#  ASCII LOGO  (cosmic style)
# ─────────────────────────────────────────────────────────────────────────────
LOGO_LINES = [
    r" ██████╗ ██╗   ██╗    ██╗    ██╗ ██████╗ ██████╗ ██████╗ ███████╗",
    r" ██╔══██╗╚██╗ ██╔╝    ██║    ██║██╔═══██╗██╔══██╗██╔══██╗██╔════╝",
    r" ██████╔╝ ╚████╔╝     ██║ █╗ ██║██║   ██║██████╔╝██║  ██║███████╗",
    r" ██╔═══╝   ╚██╔╝      ██║███╗██║██║   ██║██╔══██╗██║  ██║╚════██║",
    r" ██║        ██║       ╚███╔███╔╝╚██████╔╝██║  ██║██████╔╝███████║",
    r" ╚═╝        ╚═╝        ╚══╝╚══╝  ╚═════╝ ╚═╝  ╚═╝╚═════╝ ╚══════╝",
]

TAGLINE    = "✦  the cosmic typing benchmark by PyWords  ✦"
SPLASH_A   = "[ ENTER ] Start   [ U ] Upload Book   [ ESC ] Quit"
SPLASH_B   = "[ T ] Time: {t}s   [ ← ] 30s   [ → ] 60s   [ ↑ ] 90s"

# ─────────────────────────────────────────────────────────────────────────────
#  BUILT-IN PASSAGE POOL  (15 passages)
# ─────────────────────────────────────────────────────────────────────────────
PASSAGES = [
    (
        "The quick brown fox jumps over the lazy dog. A wizard's job is to vex chumps "
        "quickly in fog. Pack my box with five dozen liquor jugs. How vexingly quick daft "
        "zebras jump. The five boxing wizards jump quickly through the misty valley."
    ),
    (
        "Space is not empty. It is full of wonder — vast clouds of gas and dust, the remnants "
        "of ancient supernovae, quietly sculpting the next generation of stars. Every atom in "
        "your body was forged in the heart of a dying star millions of years before Earth was born."
    ),
    (
        "In the beginning God created the heavens and the earth. Now the earth was formless "
        "and empty, darkness was over the surface of the deep, and the Spirit of God was "
        "hovering over the waters. And God said, Let there be light, and there was light."
    ),
    (
        "It was a bright cold day in April and the clocks were striking thirteen. Winston "
        "Smith, his chin nuzzled into his breast in an effort to escape the vile wind, "
        "slipped quickly through the glass doors of Victory Mansions, though not quickly "
        "enough to prevent a swirl of gritty dust from entering along with him."
    ),
    (
        "Two roads diverged in a yellow wood, and sorry I could not travel both and be one "
        "traveler, long I stood and looked down one as far as I could to where it bent in "
        "the undergrowth; then took the other, as just as fair, and having perhaps the better "
        "claim, because it was grassy and wanted wear."
    ),
    (
        "The art of programming is the art of organizing complexity, of mastering multitude "
        "and avoiding its bastard chaos as effectively as possible. Simplicity is prerequisite "
        "for reliability. Testing shows the presence, not the absence of bugs. Elegance is "
        "not a dispensable luxury but a quality that decides between success and failure."
    ),
    (
        "To be, or not to be, that is the question: whether tis nobler in the mind to suffer "
        "the slings and arrows of outrageous fortune, or to take arms against a sea of "
        "troubles and by opposing end them. To die, to sleep, no more; and by a sleep to say "
        "we end the heartache and the thousand natural shocks that flesh is heir to."
    ),
    (
        "The cosmos is all that is or ever was or ever will be. Our feeblest contemplations "
        "of the cosmos stir us — there is a tingling in the spine, a catch in the voice, "
        "a faint sensation as if a distant memory of falling from a great height. We know we "
        "are approaching the grandest of mysteries. — Carl Sagan"
    ),
    (
        "Machine learning is not magic, it is statistics applied at scale. Neural networks "
        "learn by adjusting millions of numerical weights until their predictions match the "
        "training data as closely as possible. Backpropagation carries error gradients layer "
        "by layer until every synapse in the artificial brain has been nudged toward the truth."
    ),
    (
        "The night sky is a time machine. When you gaze at the Andromeda galaxy you are seeing "
        "light that left it two and a half million years ago. The stars you see with the naked "
        "eye are windows into the past, some of them already dead by the time their ancient "
        "photons finally reach your retina."
    ),
    (
        "Rivers know this: there is no hurry. We shall get there some day. The smallest "
        "stream, trickling through a mossy bank, knows nothing of impatience. It winds, "
        "meanders, pools in quiet eddies, and in its own time, always reaches the ocean "
        "where all waters are one and all journeys end."
    ),
    (
        "Quantum mechanics describes a universe far stranger than science fiction. Particles "
        "can be in two places at once until observed. Distant particles can share quantum "
        "states instantaneously across any distance. The act of measurement itself changes "
        "reality, as if the universe refuses to commit until someone is watching."
    ),
    (
        "A ship in harbor is safe, but that is not what ships are for. Bold experimentation "
        "is the engine of discovery. Every great breakthrough began as a heresy, an idea so "
        "radical that the establishment recoiled. The scientists who changed history were not "
        "the most careful — they were the most daring."
    ),
    (
        "The terminal blinks, patient as a monk. You place your fingers on the keys and the "
        "universe waits. Every keystroke is a small act of creation, a photon of meaning "
        "launched into the void of the screen. Code is poetry written for two audiences: "
        "the machine that executes it and the human who must someday understand it."
    ),
    (
        "Somewhere, something incredible is waiting to be known. Science moves at the speed "
        "of curiosity multiplied by collaboration. Every experiment is a question posed to "
        "nature, and nature always answers — sometimes with the answer you expected, and "
        "sometimes with a secret so astonishing it reshapes everything you thought you knew."
    ),
]

# ─────────────────────────────────────────────────────────────────────────────
#  COLOR PAIR IDs
# ─────────────────────────────────────────────────────────────────────────────
CP_CORRECT   = 1   # green
CP_ERROR     = 2   # red
CP_UNTYPED   = 3   # white dim
CP_HEADER    = 4   # cyan
CP_LOGO1     = 5   # bright magenta (cosmic)
CP_LOGO2     = 6   # blue
CP_TAGLINE   = 7   # white dim
CP_RESULT_HI = 8   # bright green
CP_TIMER_LOW = 9   # red
CP_STAR      = 10  # dark blue/cyan star
CP_FIREFLY   = 11  # bright yellow
CP_CAT       = 12  # white
CP_BORDER    = 13  # magenta border
CP_PROMPT    = 14  # bright cyan bold
CP_SPECIAL   = 15  # yellow accent

def init_colors():
    curses.start_color()
    curses.use_default_colors()
    curses.init_pair(CP_CORRECT,   curses.COLOR_GREEN,   -1)
    curses.init_pair(CP_ERROR,     curses.COLOR_RED,     -1)
    curses.init_pair(CP_UNTYPED,   curses.COLOR_WHITE,   -1)
    curses.init_pair(CP_HEADER,    curses.COLOR_CYAN,    -1)
    curses.init_pair(CP_LOGO1,     curses.COLOR_MAGENTA, -1)
    curses.init_pair(CP_LOGO2,     curses.COLOR_BLUE,    -1)
    curses.init_pair(CP_TAGLINE,   curses.COLOR_WHITE,   -1)
    curses.init_pair(CP_RESULT_HI, curses.COLOR_GREEN,   -1)
    curses.init_pair(CP_TIMER_LOW, curses.COLOR_RED,     -1)
    curses.init_pair(CP_STAR,      curses.COLOR_CYAN,    -1)
    curses.init_pair(CP_FIREFLY,   curses.COLOR_YELLOW,  -1)
    curses.init_pair(CP_CAT,       curses.COLOR_WHITE,   -1)
    curses.init_pair(CP_BORDER,    curses.COLOR_MAGENTA, -1)
    curses.init_pair(CP_PROMPT,    curses.COLOR_CYAN,    -1)
    curses.init_pair(CP_SPECIAL,   curses.COLOR_YELLOW,  -1)

# ─────────────────────────────────────────────────────────────────────────────
#  SAFE DRAW HELPERS
# ─────────────────────────────────────────────────────────────────────────────
def safe_addstr(win, y, x, text, attr=0):
    try:
        max_y, max_x = win.getmaxyx()
        if y < 0 or y >= max_y or x < 0:
            return
        available = max_x - x
        if available <= 0:
            return
        win.addstr(y, x, text[:available], attr)
    except curses.error:
        pass

def safe_addch(win, y, x, ch, attr=0):
    try:
        max_y, max_x = win.getmaxyx()
        if y < 0 or y >= max_y or x < 0 or x >= max_x:
            return
        win.addch(y, x, ch, attr)
    except curses.error:
        pass

# ─────────────────────────────────────────────────────────────────────────────
#  COSMIC BACKGROUND — stars
# ─────────────────────────────────────────────────────────────────────────────
STAR_CHARS = [".", "·", "*", "✦", "+", "°", "★"]

class StarField:
    def __init__(self, h: int, w: int, density: float = 0.025):
        self.stars: List[Tuple[int, int, str, float]] = []
        self._build(h, w, density)

    def _build(self, h: int, w: int, density: float):
        self.stars = []
        count = int(h * w * density)
        for _ in range(count):
            r = random.randint(0, max(0, h - 1))
            c = random.randint(0, max(0, w - 1))
            ch = random.choice(STAR_CHARS)
            brightness = random.random()
            self.stars.append((r, c, ch, brightness))

    def rebuild(self, h: int, w: int):
        self._build(h, w, 0.025)

    def draw(self, win, t: float):
        for (r, c, ch, phase) in self.stars:
            # Slow twinkle — sin wave per star
            intensity = (math.sin(t * 0.7 + phase * 6.28) + 1) / 2
            if intensity > 0.6:
                attr = curses.color_pair(CP_STAR) | curses.A_BOLD
            elif intensity > 0.3:
                attr = curses.color_pair(CP_STAR)
            else:
                attr = curses.color_pair(CP_STAR) | curses.A_DIM
            safe_addch(win, r, c, ch, attr)

# ─────────────────────────────────────────────────────────────────────────────
#  FIREFLIES
# ─────────────────────────────────────────────────────────────────────────────
FIREFLY_CHAR = "✦"

class Firefly:
    def __init__(self, h: int, w: int):
        self.h = h
        self.w = w
        self.reset()

    def reset(self):
        self.y = random.uniform(1, max(2, self.h - 2))
        self.x = random.uniform(1, max(2, self.w - 2))
        self.vy = random.uniform(-0.3, 0.3)
        self.vx = random.uniform(-0.5, 0.5)
        self.phase = random.uniform(0, 6.28)
        self.speed = random.uniform(0.5, 2.0)

    def update(self, dt: float):
        self.y += self.vy * dt * self.speed
        self.x += self.vx * dt * self.speed
        # Wander
        self.vy += random.uniform(-0.05, 0.05)
        self.vx += random.uniform(-0.05, 0.05)
        self.vy = max(-0.8, min(0.8, self.vy))
        self.vx = max(-1.0, min(1.0, self.vx))
        # Wrap / bounce edges
        if self.y < 1:
            self.y = 1; self.vy = abs(self.vy)
        if self.y >= self.h - 1:
            self.y = self.h - 2; self.vy = -abs(self.vy)
        if self.x < 1:
            self.x = 1; self.vx = abs(self.vx)
        if self.x >= self.w - 1:
            self.x = self.w - 2; self.vx = -abs(self.vx)

    def draw(self, win, t: float):
        glow = (math.sin(t * 3.0 + self.phase) + 1) / 2
        if glow > 0.5:
            attr = curses.color_pair(CP_FIREFLY) | curses.A_BOLD
        else:
            attr = curses.color_pair(CP_FIREFLY) | curses.A_DIM
        safe_addch(win, int(self.y), int(self.x), FIREFLY_CHAR, attr)

# ─────────────────────────────────────────────────────────────────────────────
#  CATS  (roaming ASCII cats)
# ─────────────────────────────────────────────────────────────────────────────
# Each cat is a list of strings (multi-line sprite).
# We have left-facing and right-facing variants.
CAT_RIGHT = [r"/\^/\  ", r"(=^_^=)", r" (___) "]
CAT_LEFT  = [r"  /\^/\ ", r"(=^_^=)", r"  (___) "]
CAT_SIT   = [r" /\./\ ", r"(= ‥ =)", r"  UwU  "]

class Cat:
    SPRITES = [CAT_RIGHT, CAT_LEFT, CAT_SIT]

    def __init__(self, h: int, w: int):
        self.h = h
        self.w = w
        self.reset()

    def reset(self):
        self.y    = float(random.randint(2, max(3, self.h - 5)))
        self.x    = float(random.randint(0, max(0, self.w - 10)))
        self.vx   = random.choice([-0.4, 0.4])
        self.sit_timer = 0.0
        self.sit_dur   = 0.0
        self.sitting   = False
        self._pick_sprite()

    def _pick_sprite(self):
        if self.sitting:
            self.sprite = CAT_SIT
        elif self.vx > 0:
            self.sprite = CAT_RIGHT
        else:
            self.sprite = CAT_LEFT

    def update(self, dt: float):
        if self.sitting:
            self.sit_timer += dt
            if self.sit_timer >= self.sit_dur:
                self.sitting = False
                self.vx = random.choice([-0.4, 0.4])
                self._pick_sprite()
        else:
            self.x += self.vx
            # Random sit
            if random.random() < 0.002:
                self.sitting = True
                self.sit_timer = 0.0
                self.sit_dur   = random.uniform(1.5, 4.0)
                self._pick_sprite()
            # Bounce at edges
            if self.x < 1:
                self.x = 1; self.vx = abs(self.vx); self._pick_sprite()
            if self.x > self.w - 10:
                self.x = self.w - 10; self.vx = -abs(self.vx); self._pick_sprite()

    def draw(self, win, t: float):
        attr = curses.color_pair(CP_CAT) | curses.A_BOLD
        ix = int(self.x)
        iy = int(self.y)
        for li, line in enumerate(self.sprite):
            safe_addstr(win, iy + li, ix, line, attr)

# ─────────────────────────────────────────────────────────────────────────────
#  COSMIC BORDER
# ─────────────────────────────────────────────────────────────────────────────
def draw_cosmic_border(win, t: float):
    h, w = win.getmaxyx()
    phase = t * 0.5
    for col in range(w):
        glow = (math.sin(col * 0.15 + phase) + 1) / 2
        if glow > 0.6:
            attr = curses.color_pair(CP_BORDER) | curses.A_BOLD
        else:
            attr = curses.color_pair(CP_BORDER) | curses.A_DIM
        safe_addch(win, 0, col, "═", attr)
        safe_addch(win, h - 1, col, "═", attr)
    for row in range(h):
        glow = (math.sin(row * 0.2 + phase + 1.0) + 1) / 2
        if glow > 0.6:
            attr = curses.color_pair(CP_BORDER) | curses.A_BOLD
        else:
            attr = curses.color_pair(CP_BORDER) | curses.A_DIM
        safe_addch(win, row, 0, "║", attr)
        safe_addch(win, row, w - 1, "║", attr)
    # Corners
    c_attr = curses.color_pair(CP_BORDER) | curses.A_BOLD
    safe_addch(win, 0,     0,     "╔", c_attr)
    safe_addch(win, 0,     w - 1, "╗", c_attr)
    safe_addch(win, h - 1, 0,     "╚", c_attr)
    safe_addch(win, h - 1, w - 1, "╝", c_attr)

# ─────────────────────────────────────────────────────────────────────────────
#  STATS CALCULATION
# ─────────────────────────────────────────────────────────────────────────────
def calc_stats(typed: str, passage: str, elapsed: float):
    minutes = elapsed / 60.0 if elapsed > 0 else 0.0001
    errors = 0
    correct = 0
    for i, ch in enumerate(typed):
        if i < len(passage):
            if ch == passage[i]:
                correct += 1
            else:
                errors += 1
        else:
            errors += 1
    keystrokes = len(typed)
    raw_wpm  = (keystrokes / 5.0) / minutes
    wpm      = (correct / 5.0) / minutes
    accuracy = (correct / keystrokes * 100.0) if keystrokes > 0 else 100.0
    return {
        "wpm":        round(wpm, 1),
        "raw_wpm":    round(raw_wpm, 1),
        "accuracy":   round(accuracy, 1),
        "keystrokes": keystrokes,
        "errors":     errors,
        "correct":    correct,
    }

# ─────────────────────────────────────────────────────────────────────────────
#  BOOK UPLOAD / PARAGRAPH EXTRACTION
# ─────────────────────────────────────────────────────────────────────────────
def resolve_book_path(name: str) -> Optional[str]:
    """
    Only accept absolute paths to ensure portability across different systems.
    """
    if os.path.isabs(name):
        return name
    return None

def extract_paragraphs_from_file(path: str) -> List[str]:
    """
    Read a plain text file and extract typing-sized passages (60-380 chars).
    Works for prose, plays (Hamlet-style), poetry, and Project Gutenberg books.

    Strategy 1: split on double blank lines (classic prose paragraphs).
    Strategy 2: split on single blank lines (many play/poetry formats).
    Strategy 3: sliding window over all non-empty lines joined together
                (catches books with no consistent blank lines at all).
    The first strategy that yields >= 5 passages wins; otherwise all are merged.
    Relative filenames are resolved against the folder containing PyWords.py.
    """
    resolved = resolve_book_path(path)
    try:
        with open(resolved, "r", encoding="utf-8", errors="replace") as f:
            raw = f.read()
    except OSError:
        return []

    # Normalise line endings
    raw = raw.replace("\r\n", "\n").replace("\r", "\n")

    # Skip Project Gutenberg header/footer boilerplate
    gutenberg_start = re.search(
        r"\*\*\* ?START OF (THE|THIS) PROJECT GUTENBERG", raw, re.IGNORECASE
    )
    gutenberg_end = re.search(
        r"\*\*\* ?END OF (THE|THIS) PROJECT GUTENBERG", raw, re.IGNORECASE
    )
    if gutenberg_start:
        raw = raw[gutenberg_start.end():]
    if gutenberg_end:
        end_pos = gutenberg_end.start()
        if end_pos > 0:
            raw = raw[:end_pos]

    def clean_chunk(chunk: str) -> str:
        """Collapse a block of lines into a single clean string."""
        return " ".join(chunk.split())

    def is_heading(text: str) -> bool:
        """Heuristic: short ALL-CAPS or stage-direction lines are skipped."""
        stripped = text.strip()
        if len(stripped) < 3 or len(stripped) > 60:
            return False
        # If >60% chars are uppercase and it's short, treat as heading
        alpha = [c for c in stripped if c.isalpha()]
        if not alpha:
            return True
        return sum(1 for c in alpha if c.isupper()) / len(alpha) > 0.6

    def filter_passages(texts: List[str]) -> List[str]:
        result = []
        for t in texts:
            t = clean_chunk(t)
            if 60 <= len(t) <= 380 and not is_heading(t):
                result.append(t)
        return result

    # ── Strategy 1: double blank lines ──────────────────────────────────────
    chunks1 = re.split(r"\n[ \t]*\n[ \t]*\n", raw)
    passages1 = filter_passages(chunks1)
    if len(passages1) >= 5:
        return passages1

    # ── Strategy 2: single blank lines ──────────────────────────────────────
    chunks2 = re.split(r"\n[ \t]*\n", raw)
    passages2 = filter_passages(chunks2)
    if len(passages2) >= 5:
        return passages2

    # ── Strategy 3: sliding window over non-empty lines ──────────────────────
    # Join every non-empty, non-heading line, then cut into 60-350-char chunks
    lines = [l.strip() for l in raw.split("\n") if l.strip() and not is_heading(l.strip())]
    combined = " ".join(lines)
    passages3: List[str] = []
    i = 0
    while i < len(combined):
        # Find a nice word boundary around the target length (~200 chars)
        end = min(i + 250, len(combined))
        # Extend to next sentence end if possible
        for punct in (".", "!", "?"):
            pos = combined.find(punct, min(i + 100, end - 1), end + 60)
            if pos != -1:
                end = pos + 1
                break
        chunk = combined[i:end].strip()
        if len(chunk) >= 60:
            passages3.append(chunk)
        i = end

    passages3 = [p for p in passages3 if 60 <= len(p) <= 400]
    return passages3 if passages3 else []

def prompt_book_upload(stdscr) -> Optional[str]:
    """
    Show a prompt asking the user to type the full path to a .txt file.
    Returns the input string or None on ESC/cancel.
    """
    h, w = stdscr.getmaxyx()
    curses.curs_set(1)
    stdscr.nodelay(False)

    prompt_text = "Enter the full path to the .txt file (e.g., C:\\path\\to\\file.txt):"
    input_buf: List[str] = []
    error_msg = ""

    while True:
        stdscr.erase()
        # re-draw stars
        t = time.time() % 100
        draw_cosmic_border(stdscr, t)
        py = h // 2 - 2
        px = max(1, (w - len(prompt_text)) // 2)
        safe_addstr(stdscr, py, px, prompt_text,
                    curses.color_pair(CP_PROMPT) | curses.A_BOLD)

        inp = "".join(input_buf)
        ix = max(1, (w - min(w - 4, 60)) // 2)
        # Draw input box
        box_w = min(w - 4, 60)
        safe_addstr(stdscr, py + 2, ix - 1, "┌" + "─" * box_w + "┐",
                    curses.color_pair(CP_BORDER))
        safe_addstr(stdscr, py + 3, ix - 1, "│" + inp[-box_w:].ljust(box_w) + "│",
                    curses.color_pair(CP_HEADER) | curses.A_BOLD)
        safe_addstr(stdscr, py + 4, ix - 1, "└" + "─" * box_w + "┘",
                    curses.color_pair(CP_BORDER))

        if error_msg:
            safe_addstr(stdscr, py + 5, max(1, (w - len(error_msg)) // 2), error_msg,
                        curses.color_pair(CP_ERROR) | curses.A_BOLD)

        hint = "Press ENTER to load  |  ESC to cancel"
        safe_addstr(stdscr, py + 7, max(1, (w - len(hint)) // 2), hint,
                    curses.color_pair(CP_TAGLINE) | curses.A_DIM)
        stdscr.refresh()

        key = stdscr.getch()
        if key == 27:
            curses.curs_set(0)
            return None
        elif key in (curses.KEY_ENTER, ord("\n"), ord("\r")):
            inp = "".join(input_buf).strip()
            if not inp:
                continue
            if not os.path.isabs(inp):
                error_msg = "Error: Please enter the full absolute path."
                input_buf = []  # Clear input
                continue
            curses.curs_set(0)
            return inp
        elif key in (curses.KEY_BACKSPACE, 127, 8):
            if input_buf:
                input_buf.pop()
            error_msg = ""  # Clear error on edit
        elif 32 <= key <= 126:
            input_buf.append(chr(key))
            error_msg = ""  # Clear error on edit
        elif key == curses.KEY_RESIZE:
            h, w = stdscr.getmaxyx()

# ─────────────────────────────────────────────────────────────────────────────
#  SPLASH SCREEN
# ─────────────────────────────────────────────────────────────────────────────
def draw_splash(stdscr, total_time: int,
                book_passages: Optional[List[str]]) -> Tuple[str, int, Optional[List[str]]]:
    """
    Animated splash screen with stars, fireflies, and cats.
    Returns (action, total_time, book_passages).
    action: 'start', 'quit'
    """
    curses.curs_set(0)
    stdscr.nodelay(True)

    h, w = stdscr.getmaxyx()
    stars = StarField(h, w)
    fireflies = [Firefly(h, w) for _ in range(8)]
    cats = [Cat(h, w) for _ in range(2)]

    t_start = time.time()
    prev_frame = t_start

    while True:
        now    = time.time()
        t      = now - t_start
        dt     = now - prev_frame
        prev_frame = now

        # Update creatures
        for ff in fireflies:
            ff.update(dt)
        for cat in cats:
            cat.update(dt)

        stdscr.erase()

        # Stars
        stars.draw(stdscr, t)

        # Fireflies and cats
        for ff in fireflies:
            ff.draw(stdscr, t)
        for cat in cats:
            cat.draw(stdscr, t)

        # Cosmic border
        draw_cosmic_border(stdscr, t)

        # Logo  — pulsing color blend: alternate magenta / blue
        logo_w = max(len(l) for l in LOGO_LINES)
        logo_h = len(LOGO_LINES)
        total_block = logo_h + 2 + 1 + 2 + 1 + 2
        start_y = max(1, (h - total_block) // 2)

        for i, line in enumerate(LOGO_LINES):
            lx = max(1, (w - logo_w) // 2)
            pulse = (math.sin(t * 1.2 + i * 0.5) + 1) / 2
            if pulse > 0.5:
                attr = curses.color_pair(CP_LOGO1) | curses.A_BOLD
            else:
                attr = curses.color_pair(CP_LOGO2) | curses.A_BOLD
            safe_addstr(stdscr, start_y + i, lx, line, attr)

        # Tagline
        ty = start_y + logo_h + 1
        pulse2 = (math.sin(t * 0.8) + 1) / 2
        tag_attr = curses.color_pair(CP_SPECIAL) | curses.A_BOLD if pulse2 > 0.5 else \
                   curses.color_pair(CP_TAGLINE) | curses.A_DIM
        safe_addstr(stdscr, ty, max(1, (w - len(TAGLINE)) // 2), TAGLINE, tag_attr)

        # Book indicator
        book_line = ""
        if book_passages:
            book_line = f"✦ Book loaded: {len(book_passages)} passages ✦"
        elif book_passages == []:
            book_line = "✦ Book loaded (no valid paragraphs found — using built-ins) ✦"
        if book_line:
            safe_addstr(stdscr, ty + 1, max(1, (w - len(book_line)) // 2),
                        book_line, curses.color_pair(CP_RESULT_HI) | curses.A_BOLD)

        # Controls
        prompt_a = SPLASH_A
        prompt_b = SPLASH_B.format(t=total_time)
        row_a = ty + 2
        row_b = ty + 3
        safe_addstr(stdscr, row_a, max(1, (w - len(prompt_a)) // 2), prompt_a,
                    curses.color_pair(CP_PROMPT) | curses.A_BOLD)
        safe_addstr(stdscr, row_b, max(1, (w - len(prompt_b)) // 2), prompt_b,
                    curses.color_pair(CP_TAGLINE) | curses.A_DIM)

        stdscr.refresh()
        time.sleep(0.03)  # ~33 fps

        key = stdscr.getch()
        if key == curses.KEY_RESIZE:
            h, w = stdscr.getmaxyx()
            stars.rebuild(h, w)
            fireflies = [Firefly(h, w) for _ in range(8)]
            cats = [Cat(h, w) for _ in range(2)]
        elif key in (curses.KEY_ENTER, ord("\n"), ord("\r")):
            return "start", total_time, book_passages
        elif key == 27:
            return "quit", total_time, book_passages
        elif key in (ord("u"), ord("U")):
            stdscr.nodelay(False)
            path = prompt_book_upload(stdscr)
            stdscr.nodelay(True)
            if path:
                paras = extract_paragraphs_from_file(path)
                book_passages = paras  # may be empty list
            h, w = stdscr.getmaxyx()
            stars.rebuild(h, w)
        elif key == curses.KEY_LEFT:
            total_time = max(15, total_time - 30)
        elif key == curses.KEY_RIGHT:
            total_time = min(300, total_time + 30)
        elif key == curses.KEY_UP:
            total_time = 90
        elif key in (ord("t"), ord("T")):
            total_time = 60  # reset to default

# ─────────────────────────────────────────────────────────────────────────────
#  TYPING UI
# ─────────────────────────────────────────────────────────────────────────────
def draw_typing_ui(stdscr, passage: str, typed: str,
                   time_left: float, total_time: int, stats: dict,
                   stars: StarField, fireflies: List[Firefly],
                   cats: List[Cat], t: float):
    stdscr.erase()
    h, w = stdscr.getmaxyx()

    # Stars (muted during typing)
    for (r, c, ch, phase) in stars.stars:
        intensity = (math.sin(t * 0.4 + phase * 6.28) + 1) / 2
        if intensity > 0.8:
            safe_addch(stdscr, r, c, ch,
                       curses.color_pair(CP_STAR) | curses.A_DIM)

    # Fireflies
    for ff in fireflies:
        ff.draw(stdscr, t)

    # Cats roam below the text area
    for cat in cats:
        cat.draw(stdscr, t)

    # Cosmic border
    draw_cosmic_border(stdscr, t)

    # ── Header bar (row 1) ──────────────────────────────────────────────────
    header_label = " ✦ PyWords "
    timer_str = f" {int(time_left):3d}s "
    wpm_str   = f" WPM:{stats['wpm']:5.1f} "
    acc_str   = f" Acc:{stats['accuracy']:5.1f}% "
    progress  = len(typed) / max(1, len(passage))
    bar_w     = min(20, w - 40)
    filled    = int(bar_w * progress)
    bar       = "▓" * filled + "░" * (bar_w - filled)
    bar_str   = f" [{bar}] "

    timer_attr = (curses.color_pair(CP_TIMER_LOW) | curses.A_BOLD
                  if time_left <= 10
                  else curses.color_pair(CP_HEADER) | curses.A_BOLD)

    safe_addstr(stdscr, 1, 1, header_label,
                curses.color_pair(CP_LOGO1) | curses.A_BOLD)
    safe_addstr(stdscr, 1, 1 + len(header_label), bar_str,
                curses.color_pair(CP_SPECIAL) | curses.A_BOLD)

    right = wpm_str + acc_str + timer_str
    safe_addstr(stdscr, 1, max(2, w - len(right) - 1), right, timer_attr)

    # ── Separator (row 2) ──────────────────────────────────────────────────
    sep = "─" * (w - 2)
    safe_addstr(stdscr, 2, 1, sep, curses.color_pair(CP_BORDER) | curses.A_DIM)

    # ── Passage (word-wrapped) ─────────────────────────────────────────────
    pad   = 4
    text_w = max(10, w - pad * 2)
    words  = passage.split(" ")
    lines: List[str] = []
    cur_line = ""
    for word in words:
        trial = cur_line + (" " if cur_line else "") + word
        if len(trial) <= text_w:
            cur_line = trial
        else:
            if cur_line:
                lines.append(cur_line)
            cur_line = word
    if cur_line:
        lines.append(cur_line)

    passage_start_row = 4
    available_rows    = h - passage_start_row - 4
    char_idx          = 0
    cursor_drawn      = False

    for li, line_text in enumerate(lines):
        if li >= available_rows:
            break
        row = passage_start_row + li
        for ci, ch in enumerate(line_text):
            col  = pad + ci
            flat = char_idx
            if flat < len(typed):
                if typed[flat] == ch:
                    attr = curses.color_pair(CP_CORRECT) | curses.A_BOLD
                else:
                    attr = curses.color_pair(CP_ERROR) | curses.A_BOLD | curses.A_UNDERLINE
            elif flat == len(typed):
                attr  = curses.color_pair(CP_HEADER) | curses.A_REVERSE | curses.A_BOLD
                cursor_drawn = True
            else:
                attr = curses.color_pair(CP_UNTYPED) | curses.A_DIM
            safe_addch(stdscr, row, col, ch, attr)
            char_idx += 1

    # ── Hint bar (bottom) ─────────────────────────────────────────────────
    hint = "  ✦  ESC quit   |   R restart   |   U upload book  ✦  "
    hint_row = h - 2
    safe_addstr(stdscr, hint_row, max(1, (w - len(hint)) // 2), hint,
                curses.color_pair(CP_TAGLINE) | curses.A_DIM)

    stdscr.refresh()

# ─────────────────────────────────────────────────────────────────────────────
#  RESULTS SCREEN
# ─────────────────────────────────────────────────────────────────────────────
RESULT_CATS = [
    r"  /\  /\  ",
    r" (ᵕ‿‿ᵕ) ",
    r"  ‿‿‿‿  ",
]

def draw_results(stdscr, stats: dict, stars: StarField) -> str:
    curses.curs_set(0)
    stdscr.nodelay(False)

    h, w = stdscr.getmaxyx()
    t_start = time.time()

    result_lines = [
        ("", None),
        (f"  ✦  Final WPM     :  {stats['wpm']}",   CP_RESULT_HI),
        (f"  ✦  Raw WPM       :  {stats['raw_wpm']}", CP_HEADER),
        (f"  ✦  Accuracy      :  {stats['accuracy']}%", CP_RESULT_HI),
        (f"  ✦  Keystrokes    :  {stats['keystrokes']}", CP_HEADER),
        (f"  ✦  Errors        :  {stats['errors']}",
         CP_ERROR if stats["errors"] > 0 else CP_CORRECT),
        ("", None),
        ("  [ R ] Try Again     [ ESC ] Quit  ", CP_PROMPT),
    ]

    logo_w = max(len(l) for l in LOGO_LINES)
    logo_h = len(LOGO_LINES)
    total_block = logo_h + len(result_lines) + 3
    start_y = max(1, (h - total_block) // 2)

    # Draw logo
    stdscr.erase()
    t0 = time.time()
    stars.draw(stdscr, t0)
    draw_cosmic_border(stdscr, t0 - t_start)

    for i, line in enumerate(LOGO_LINES):
        lx = max(1, (w - logo_w) // 2)
        safe_addstr(stdscr, start_y + i, lx, line,
                    curses.color_pair(CP_LOGO1) | curses.A_BOLD)

    # Victory cat
    cat_x = max(1, w - 14)
    for li, cl in enumerate(RESULT_CATS):
        safe_addstr(stdscr, start_y + li, cat_x, cl,
                    curses.color_pair(CP_CAT) | curses.A_BOLD)

    stdscr.refresh()

    result_start = start_y + logo_h + 1
    for idx, (text, color_id) in enumerate(result_lines):
        time.sleep(0.12)
        row = result_start + idx
        if not text:
            continue
        lx = max(1, (w - len(text)) // 2 - 6)
        if color_id == CP_RESULT_HI:
            attr = curses.color_pair(CP_RESULT_HI) | curses.A_BOLD
        elif color_id == CP_HEADER:
            attr = curses.color_pair(CP_HEADER) | curses.A_BOLD
        elif color_id == CP_ERROR:
            attr = curses.color_pair(CP_ERROR) | curses.A_BOLD
        elif color_id == CP_CORRECT:
            attr = curses.color_pair(CP_CORRECT) | curses.A_BOLD
        elif color_id == CP_PROMPT:
            attr = curses.color_pair(CP_PROMPT) | curses.A_BOLD
        else:
            attr = curses.color_pair(CP_TAGLINE) | curses.A_DIM
        safe_addstr(stdscr, row, lx, text, attr)
        stdscr.refresh()

    while True:
        key = stdscr.getch()
        if key == 27:
            return "quit"
        elif key in (ord("r"), ord("R")):
            return "restart"
        elif key == curses.KEY_RESIZE:
            return "restart"

# ─────────────────────────────────────────────────────────────────────────────
#  MAIN TEST LOOP
# ─────────────────────────────────────────────────────────────────────────────
def run_test(stdscr, total_time: int,
             book_passages: Optional[List[str]]) -> Tuple[str, Optional[List[str]]]:
    pool = book_passages if book_passages else PASSAGES
    passage = random.choice(pool)

    typed: List[str] = []
    start_time: Optional[float] = None

    h, w = stdscr.getmaxyx()
    stars     = StarField(h, w, density=0.018)
    fireflies = [Firefly(h, w) for _ in range(6)]
    cats      = [Cat(h, w) for _ in range(2)]
    # Push cats down so they don't overlap text
    for cat in cats:
        cat.y = max(h - 6, 2)

    curses.curs_set(0)
    stdscr.nodelay(True)
    t_start   = time.time()
    prev_frame = t_start

    while True:
        now = time.time()
        t   = now - t_start
        dt  = now - prev_frame
        prev_frame = now

        # Update creatures
        for ff in fireflies:
            ff.update(dt)
        for cat in cats:
            cat.update(dt)

        if start_time is None:
            elapsed   = 0.0
            time_left = float(total_time)
        else:
            elapsed   = now - start_time
            time_left = max(0.0, total_time - elapsed)

        stats = calc_stats("".join(typed), passage, elapsed if elapsed > 0 else 0.001)

        try:
            draw_typing_ui(stdscr, passage, "".join(typed),
                           time_left, total_time, stats,
                           stars, fireflies, cats, t)
        except curses.error:
            pass

        typed_str = "".join(typed)
        if len(typed_str) >= len(passage):
            # Append a new passage to continue the test
            next_passage = random.choice(pool)
            passage += " " + next_passage
        if time_left <= 0 and start_time is not None:
            final_stats = calc_stats(typed_str, passage, elapsed if elapsed > 0 else 0.001)
            action = draw_results(stdscr, final_stats, stars)
            return action, book_passages

        key = stdscr.getch()
        if key == curses.KEY_RESIZE:
            h, w = stdscr.getmaxyx()
            stars = StarField(h, w, density=0.018)
            fireflies = [Firefly(h, w) for _ in range(6)]
            cats = [Cat(h, w) for _ in range(2)]
            for cat in cats:
                cat.y = max(h - 6, 2)
            continue
        if key == -1:
            time.sleep(0.016)
            continue

        if start_time is None and 32 <= key <= 126:
            start_time = time.time()

        if key == 27:
            return "quit", book_passages

        # Shortcuts disabled during typing to prevent interference

        if key in (curses.KEY_BACKSPACE, 127, 8):
            if typed:
                typed.pop()
        elif 32 <= key <= 126:
            typed.append(chr(key))

        time.sleep(0.005)

# ─────────────────────────────────────────────────────────────────────────────
#  CURSES MAIN
# ─────────────────────────────────────────────────────────────────────────────
def main(stdscr, total_time: int, initial_book: Optional[List[str]]):
    init_colors()
    curses.curs_set(0)
    book_passages = initial_book

    while True:
        action, total_time, book_passages = draw_splash(stdscr, total_time, book_passages)
        if action == "quit":
            break

        while True:
            result, book_passages = run_test(stdscr, total_time, book_passages)
            if result == "quit":
                return
            elif result in ("restart", "done"):
                break

# ─────────────────────────────────────────────────────────────────────────────
#  ENTRY POINT
# ─────────────────────────────────────────────────────────────────────────────
if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        prog="PyWords",
        description="PyWords — the cosmic terminal typing benchmark",
    )
    parser.add_argument(
        "--time", "-t",
        type=int, default=60, metavar="SECONDS",
        help="Duration of the typing test in seconds (default: 60)",
    )
    parser.add_argument(
        "--book", "-b",
        type=str, default=None, metavar="FILE",
        help="Path to a .txt book file to use as passage source",
    )
    args = parser.parse_args()

    if args.time < 5 or args.time > 300:
        print("Error: --time must be between 5 and 300 seconds.", file=sys.stderr)
        sys.exit(1)

    initial_book = None
    if args.book:
        resolved = resolve_book_path(args.book)
        if resolved is None:
            print(f"Error: --book must be an absolute path. Got: {args.book}", file=sys.stderr)
            sys.exit(1)
        paras = extract_paragraphs_from_file(resolved)
        if paras:
            print(f"[PyWords] Loaded {len(paras)} paragraphs from '{resolved}'.")
            initial_book = paras
        else:
            print(f"[PyWords] Warning: no valid paragraphs found in '{resolved}'. Using built-ins.")
            initial_book = []

    try:
        curses.wrapper(main, args.time, initial_book)
    except KeyboardInterrupt:
        pass
    finally:
        print("\n✦ Thanks for using PyWords — keep typing through the cosmos! ✦")
