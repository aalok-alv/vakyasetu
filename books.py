import customtkinter as ctk

# ------------------ CONFIG ------------------
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("dark-blue")

ACCENT = "#3b82f6"
BG_MAIN = "#111827"
BG_SIDEBAR = "#0f172a"

class BooksApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("VakyaSetu - Books")
        self.attributes("-fullscreen", True)
        self.configure(fg_color=BG_MAIN)

        # Exit back to main menu
        self.bind("<Escape>", lambda e: self.destroy())

        # ---------------- LAYOUT ----------------
        # Sidebar
        self.sidebar = ctk.CTkFrame(self, width=250, fg_color=BG_SIDEBAR, corner_radius=0)
        self.sidebar.pack(side="left", fill="y")
        self.sidebar.pack_propagate(False)

        ctk.CTkLabel(self.sidebar, text="Library", font=ctk.CTkFont(size=32, weight="bold")).pack(pady=(40, 30))

        # Categories
        categories = ["All Books", "Manhwa", "Audiobooks", "Favorites"]
        for cat in categories:
            btn = ctk.CTkButton(
                self.sidebar, text=cat, fg_color="transparent", 
                text_color="#e5e7eb", hover_color="#1f2937", 
                anchor="w", font=ctk.CTkFont(size=20)
            )
            btn.pack(fill="x", padx=20, pady=10)

        # Main Content Area
        self.main_content = ctk.CTkFrame(self, fg_color="transparent")
        self.main_content.pack(side="right", fill="both", expand=True, padx=40, pady=40)

        ctk.CTkLabel(self.main_content, text="Recent Reads", font=ctk.CTkFont(size=36, weight="bold")).pack(anchor="w", pady=(0, 20))

        # Placeholder for Book Grid
        self.grid_frame = ctk.CTkFrame(self.main_content, fg_color="transparent")
        self.grid_frame.pack(fill="both", expand=True)

        self.create_book_placeholder("The Alchemist", "Paulo Coelho", 0, 0)
        self.create_book_placeholder("Solo Leveling", "Chugong", 0, 1)
        self.create_book_placeholder("Atomic Habits", "James Clear", 0, 2)

    def create_book_placeholder(self, title, author, row, col):
        card = ctk.CTkFrame(self.grid_frame, width=200, height=300, corner_radius=15, fg_color="#1f2937")
        card.grid(row=row, column=col, padx=20, pady=20)
        card.pack_propagate(False)

        # Placeholder Cover
        cover = ctk.CTkFrame(card, width=160, height=200, fg_color="#374151", corner_radius=10)
        cover.pack(pady=(20, 10))
        ctk.CTkLabel(cover, text="📖", font=ctk.CTkFont(size=50)).place(relx=0.5, rely=0.5, anchor="center")

        ctk.CTkLabel(card, text=title, font=ctk.CTkFont(size=18, weight="bold")).pack()
        ctk.CTkLabel(card, text=author, font=ctk.CTkFont(size=14), text_color="#9ca3af").pack()

def main():
    app = BooksApp()
    app.mainloop()

if __name__ == "__main__":
    main()