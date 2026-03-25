import customtkinter as ctk
import math


# ------------------ SAFE IMPORTS ------------------
def safe_import(module_name):
    try:
        return __import__(module_name)
    except ImportError:
        return None

text_to_speech_ENG = safe_import("text_to_speech_ENG")
text_to_speech_HIN = safe_import("text_to_speech_HIN")
chat_ENG = safe_import("chat_ENG")
chat_HIN = safe_import("chat_HIN")

# ------------------ UI CONFIG ------------------
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("dark-blue")

ACCENT = "#3b82f6"
BG_CARD = "#111827"
BG_MAIN = "#030712"  # Solid background to prevent animation ghosting
TEXT_BRIGHT = "#ffffff"
TEXT_DIM = "#9ca3af"
TEXT_DARK = "#4b5563"

# ------------------ TRANSLATIONS ------------------
STRINGS = {
    "English": {
        "title": "VakyaSetu",
        "lang_tag": "ENG",
        "cards": [
            ("🎤", "Talk"), 
            ("💬", "Chat"), 
            ("📰", "News"), 
            ("📖", "Books"), 
            ("📷", "Photos")
        ]
    },
    "Hindi": {
        "title": "वाक्यसेतु",
        "lang_tag": "HI",
        "cards": [
            ("🎤", "बातचीत"), 
            ("💬", "ऑनलाइन चैट"), 
            ("📰", "समाचार"), 
            ("📖", "किताबें"), 
            ("📷", "तस्वीरें")
        ]
    }
}

class VakyaSetuApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.attributes("-fullscreen", True)
        self.bind("<Escape>", lambda e: self.destroy())
        
        # ROOT FRAME: Solid color prevents transparent redraw stacking
        self.root_frame = ctk.CTkFrame(self, fg_color=BG_MAIN)
        self.root_frame.pack(fill="both", expand=True)

        self.is_animating = False
        self.toast_frame = None

        self.show_language_selection()

    def clear_screen(self):
        for widget in self.root_frame.winfo_children():
            widget.destroy()

    # ---------------- UI: IN-APP NOTIFICATIONS ----------------
    def show_toast(self, message, duration=3000):
        if self.toast_frame:
            self.toast_frame.destroy()
            
        self.toast_frame = ctk.CTkFrame(self.root_frame, fg_color="#ef4444", corner_radius=15)
        self.toast_frame.place(relx=0.5, rely=0.9, anchor="center")
        
        ctk.CTkLabel(self.toast_frame, text=message, font=ctk.CTkFont(size=16, weight="bold"), text_color="white").pack(padx=30, pady=10)
        self.after(duration, self.toast_frame.destroy)

    # ---------------- UI: LANGUAGE SCREEN ----------------
    def show_language_selection(self):
        self.clear_screen()
        container = ctk.CTkFrame(self.root_frame, fg_color="transparent")
        container.place(relx=0.5, rely=0.5, anchor="center")

        ctk.CTkLabel(container, text="VakyaSetu / वाक्यसेतु", font=ctk.CTkFont(size=54, weight="bold")).pack(pady=30)
        
        combo = ctk.CTkComboBox(container, values=["English", "Hindi"], state="readonly", width=320, height=55, font=ctk.CTkFont(size=22))
        combo.set("English")
        combo.pack(pady=15)

        ctk.CTkButton(
            container, text="Start / शुरू करें", cursor="hand2",
            command=lambda: self.setup_main_ui(combo.get()),
            width=320, height=55, fg_color=ACCENT, font=ctk.CTkFont(size=22, weight="bold")
        ).pack(pady=20)

    # ---------------- UI: MAIN WHEEL SCREEN ----------------
    def setup_main_ui(self, lang):
        self.clear_screen()
        self.current_lang = lang
        data = STRINGS[lang]

        # Header
        header = ctk.CTkFrame(self.root_frame, height=80, fg_color="#0f172a")
        header.pack(fill="x")
        
        ctk.CTkButton(header, text="← Language", width=100, fg_color="#374151", hover_color="#4b5563", cursor="hand2", command=self.show_language_selection).pack(side="left", padx=20)
        ctk.CTkLabel(header, text=data["title"], font=ctk.CTkFont(size=36, weight="bold")).pack(side="left", padx=10, pady=20)
        ctk.CTkLabel(header, text=data["lang_tag"], font=ctk.CTkFont(size=20)).pack(side="right", padx=30, pady=20)

        # Content Zone: Solid background fix
        self.wheel_frame = ctk.CTkFrame(self.root_frame, fg_color=BG_MAIN)
        self.wheel_frame.pack(fill="both", expand=True)

        # Keyboard Navigation
        self.bind("<Right>", lambda e: self.move_carousel(1))
        self.bind("<Delete>", lambda e: self.move_carousel(1)) 
        self.bind("<Left>", lambda e: self.move_carousel(-1))
        self.bind("<Return>", lambda e: self.activate(self.current_index))

        self.cards = []
        for icon, text in data["cards"]:
            self.cards.append(self.create_card(icon, text))

        self.current_index = 0
        self.is_animating = False
        self.update_focus(animate=False) 

    def create_card(self, icon, text):
        card = ctk.CTkFrame(self.wheel_frame, corner_radius=35, fg_color=BG_CARD, cursor="hand2")
        card.pack_propagate(False)

        card.icon_label = ctk.CTkLabel(card, text=icon, cursor="hand2")
        card.icon_label.pack(pady=(40, 10))
        
        card.text_label = ctk.CTkLabel(card, text=text, cursor="hand2")
        card.text_label.pack()

        for w in (card, card.icon_label, card.text_label):
            w.bind("<Button-1>", lambda e, c=card: self.card_click(c))
            
        return card

    # ---------------- 3D ANIMATION ENGINE ----------------
    def get_layout_data(self):
        """
        Defines the 5 positions.
        Cards are spaced to prevent rectangular bounding box overlap, 
        which fixes the Tkinter 'black corner' clipping issue.
        """
        return {
            # CENTER: Slightly narrowed width to make room
            0: {"x": 0.50, "y": 0.45, "w": 460, "h": 320, "fi": 90, "ft": 36, "bc": ACCENT, "tc": TEXT_BRIGHT, "bw": 4},
            
            # RIGHT & LEFT: Pushed slightly further to the sides
            1: {"x": 0.83, "y": 0.55, "w": 240, "h": 180, "fi": 45,  "ft": 20, "bc": "#1f2937", "tc": TEXT_DIM, "bw": 2},
            4: {"x": 0.17, "y": 0.55, "w": 240, "h": 180, "fi": 45,  "ft": 20, "bc": "#1f2937", "tc": TEXT_DIM, "bw": 2},
            
            # FAR RIGHT & FAR LEFT: Tucked cleanly into the edges
            2: {"x": 0.96, "y": 0.65, "w": 100, "h": 80,  "fi": 24,  "ft": 12, "bc": "#111827", "tc": TEXT_DARK, "bw": 1},
            3: {"x": 0.04, "y": 0.65, "w": 100, "h": 80,  "fi": 24,  "ft": 12, "bc": "#111827", "tc": TEXT_DARK, "bw": 1},
        }

    def update_focus(self, animate=True):
        if self.is_animating and animate:
            return
            
        total_cards = len(self.cards)
        layout = self.get_layout_data()

        for rel_val in [2, 3, 1, 4, 0]: 
            idx = (self.current_index + rel_val) % total_cards
            self.cards[idx].lift()

        if not animate:
            for i, card in enumerate(self.cards):
                rel = (i - self.current_index) % total_cards
                t = layout[rel]
                card.place(relx=t["x"], rely=t["y"], anchor="center")
                card.configure(width=t["w"], height=t["h"], border_color=t["bc"], border_width=t["bw"])
                card.icon_label.configure(font=ctk.CTkFont(size=t["fi"]), text_color=t["tc"])
                card.text_label.configure(font=ctk.CTkFont(size=t["ft"], weight="bold"), text_color=t["tc"])
            return

        self.is_animating = True
        targets = []

        for i, card in enumerate(self.cards):
            rel = (i - self.current_index) % total_cards
            t = layout[rel]
            
            info = card.place_info()
            cx = float(info.get('relx', t['x'])) if info else t['x']
            cy = float(info.get('rely', t['y'])) if info else t['y']
            cw = card._desired_width
            ch = card._desired_height

            targets.append({"card": card, "start": {"x": cx, "y": cy, "w": cw, "h": ch}, "end": t})

        # Changed to 14 frames for a faster, cleaner snap
        self.animate_step(targets, step=1, max_steps=14) 

    def animate_step(self, targets, step, max_steps):
        if step > max_steps:
            self.is_animating = False
            return

        # Smooth easing formula
        p = step / max_steps
        ease = 4 * p * p * p if p < 0.5 else 1 - math.pow(-2 * p + 2, 3) / 2

        for t in targets:
            c = t["card"]
            s = t["start"]
            e = t["end"]

            # 1. SLIDE ONLY: We only animate the X and Y positions smoothly
            nx = s["x"] + (e["x"] - s["x"]) * ease
            ny = s["y"] + (e["y"] - s["y"]) * ease
            
            c.place(relx=nx, rely=ny, anchor="center")

            # 2. INSTANT SNAP: Change the size and fonts exactly halfway through.
            # This stops the engine from choking on resizing rounded corners!
            if step == max_steps // 2:
                c.configure(width=e["w"], height=e["h"], border_color=e["bc"], border_width=e["bw"])
                c.icon_label.configure(font=ctk.CTkFont(size=e["fi"]), text_color=e["tc"])
                c.text_label.configure(font=ctk.CTkFont(size=e["ft"], weight="bold"), text_color=e["tc"])

        # Force clean up 
        self.update_idletasks()

        # Reduced to 12 frames for a lightning-fast, clean swipe
        self.after(16, self.animate_step, targets, step + 1, 36)


    # ---------------- INTERACTION & ROUTING ----------------
    def move_carousel(self, direction):
        self.current_index = (self.current_index + direction) % len(self.cards)
        self.update_focus()

    def card_click(self, card):
        idx = self.cards.index(card)
        if idx == self.current_index:
            self.activate(idx)
        else:
            diff = (idx - self.current_index) % len(self.cards)
            direction = 1 if diff <= len(self.cards)//2 else -1
            self.move_carousel(direction)

    def activate(self, index):
        if index == 0: 
            top = ctk.CTkToplevel(self)
            if self.current_lang == "English" and text_to_speech_ENG: 
                text_to_speech_ENG.AlphabetLocator(top)
            elif self.current_lang == "Hindi" and text_to_speech_HIN: 
                text_to_speech_HIN.AlphabetLocatorHindi(top)
            else: 
                self.show_toast(f"Talk module missing for {self.current_lang}!")
                top.destroy()
        elif index == 1: 
            if self.current_lang == "English" and chat_ENG: 
                chat_ENG.main()
            elif self.current_lang == "Hindi" and chat_HIN: 
                chat_HIN.main()
            else: 
                self.show_toast(f"Chat module missing for {self.current_lang}!")

            
        
if __name__ == "__main__":
    app = VakyaSetuApp()
    app.mainloop()