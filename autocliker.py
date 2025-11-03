import threading
import time
import sys
import tkinter as tk
from tkinter import ttk
import pygetwindow as gw
import pyautogui

IS_MAC = sys.platform == "darwin"

class AutoRefresher:
    def __init__(self, root):
        self.root = root
        self.root.title("Auto Refresher")
        self.running = False

        # Enter one or more comma-separated substrings, e.g.:
        #   " - Opera GX, - Opera"
        # or a site title that appears in both browsers.
        self.title_var = tk.StringVar(value="")     # e.g., "- Opera GX, - Opera"
        self.interval_var = tk.IntVar(value=60)     # seconds

        self.create_widgets()
        self.thread = None

    def create_widgets(self):
        frm = ttk.Frame(self.root, padding=10)
        frm.grid()

        ttk.Label(frm, text="Window titles contain (comma-separated):").grid(column=0, row=0, sticky='w')
        ttk.Entry(frm, textvariable=self.title_var, width=40).grid(column=1, row=0, padx=(6,0))

        ttk.Label(frm, text="Interval (sec):").grid(column=0, row=1, sticky='w', pady=(8,0))
        ttk.Entry(frm, textvariable=self.interval_var, width=10).grid(column=1, row=1, sticky='w', padx=(6,0), pady=(8,0))

        self.btn = ttk.Button(frm, text="🔄 Start", command=self.toggle)
        self.btn.grid(column=0, row=2, columnspan=2, pady=12, sticky='ew')

        ttk.Label(frm, text="Tip: try filters like '- Opera GX, - Opera' to hit both.").grid(column=0, row=3, columnspan=2, sticky='w')

    def toggle(self):
        if not self.running:
            titles = [t.strip() for t in self.title_var.get().split(",") if t.strip()]
            interval = self.interval_var.get()
            if not titles or interval <= 0:
                return
            self.running = True
            self.btn.config(text="■ Stop")
            self.thread = threading.Thread(target=self.run, daemon=True)
            self.thread.start()
        else:
            self.running = False
            self.btn.config(text="🔄 Start")

    def _refresh_active_window(self):
        # Use platform-appropriate refresh shortcut
        if IS_MAC:
            pyautogui.hotkey('command', 'r')
        else:
            # F5 works too, but Ctrl+R is more universal across Chromium browsers
            pyautogui.hotkey('ctrl', 'r')

    def run(self):
        while self.running:
            titles = [t.strip() for t in self.title_var.get().split(",") if t.strip()]
            seen = set()  # avoid refreshing the same window twice if it matches multiple filters

            for t in titles:
                try:
                    matches = gw.getWindowsWithTitle(t)
                except Exception:
                    matches = []

                for w in matches:
                    # Deduplicate by window handle (Windows) or title/coords fallback
                    key = getattr(w, "hwnd", None) or (w.title, w.left, w.top, w.width, w.height)
                    if key in seen:
                        continue
                    seen.add(key)

                    try:
                        # Bring window to foreground and refresh
                        if w.isMinimized:
                            w.restore()
                        w.activate()       # focus
                        time.sleep(0.25)   # very short settle time
                        self._refresh_active_window()
                        time.sleep(0.15)   # brief gap between windows
                    except Exception:
                        # Ignore windows we can’t activate (OS permissions, etc.)
                        pass

            # Wait until next cycle
            time.sleep(max(1, self.interval_var.get()))

if __name__ == "__main__":
    # pip install pygetwindow pyautogui
    root = tk.Tk()
    app = AutoRefresher(root)
    root.mainloop()
