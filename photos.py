import customtkinter as ctk

# ------------------ CONFIG ------------------
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("dark-blue")

BG_MAIN = "#111827"
BG_CARD = "#1f2937"

class PhotosApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("VakyaSetu - Photos")
        self.attributes("-fullscreen", True)
        self.configure(fg_color=BG_MAIN)

        # Exit back to main menu
        self.bind("<Escape>", lambda e: self.destroy())

        # Header
        self.header = ctk.CTkFrame(self, height=100, fg_color="transparent")
        self.header.pack(fill="x", padx=40, pady=(40, 0))
        
        ctk.CTkLabel(self.header, text="📷 Gallery", font=ctk.CTkFont(size=42, weight="bold")).pack(side="left")
        
        ctk.CTkButton(self.header, text="+ Upload", fg_color="#3b82f6", font=ctk.CTkFont(size=18, weight="bold")).pack(side="right")

        # Scrollable Gallery Area
        self.gallery = ctk.CTkScrollableFrame(self, fg_color="transparent")
        self.gallery.pack(fill="both", expand=True, padx=40, pady=20)

        # Setup a clean 3-column grid for the feed
        self.gallery.grid_columnconfigure((0, 1, 2), weight=1)

        # Add Placeholder Photos
        self.add_photo_card("Friends Trip", "August 2025", 0, 0)
        self.add_photo_card("Design Ideas", "Saved", 0, 1)
        self.add_photo_card("College Fest", "February 2026", 0, 2)
        self.add_photo_card("Camera Roll", "Recent", 1, 0)

    def add_photo_card(self, title, subtitle, row, col):
        card = ctk.CTkFrame(self.gallery, height=350, corner_radius=20, fg_color=BG_CARD)
        card.grid(row=row, column=col, padx=15, pady=15, sticky="nsew")
        card.pack_propagate(False)

        # Placeholder Image Area
        img_placeholder = ctk.CTkFrame(card, fg_color="#374151", corner_radius=15)
        img_placeholder.pack(fill="both", expand=True, padx=15, pady=(15, 5))
        
        ctk.CTkLabel(img_placeholder, text="Image", text_color="#9ca3af").place(relx=0.5, rely=0.5, anchor="center")

        # Text Area
        text_frame = ctk.CTkFrame(card, height=60, fg_color="transparent")
        text_frame.pack(fill="x", padx=20, pady=(5, 15))
        
        ctk.CTkLabel(text_frame, text=title, font=ctk.CTkFont(size=20, weight="bold")).pack(anchor="w")
        ctk.CTkLabel(text_frame, text=subtitle, font=ctk.CTkFont(size=14), text_color="#9ca3af").pack(anchor="w")

def main():
    app = PhotosApp()
    app.mainloop()

if __name__ == "__main__":
    main()