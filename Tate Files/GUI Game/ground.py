import customtkinter as ctk

ctk.set_appearance_mode("system")  # or "dark"/"light"
ctk.set_default_color_theme("blue")

def tabviewer(parent):
    # Create the tabview
    tabs = ctk.CTkTabview(parent, corner_radius=0, border_width=0)
    tabs.pack(fill="both", expand=True, padx=0, pady=0)

    # Move tabs to the top-left corner
    tabs._segmented_button._canvas.configure(highlightthickness=0)
    tabs._segmented_button.grid(sticky="w", padx=4, pady=(2, 0))

    # Visual Studio style colors
    mode = ctk.get_appearance_mode()
    if mode == "Dark":
        bg = "#1E1E1E"
        active = "#252526"
        text = "#FFFFFF"
        inactive_text = "#AAAAAA"
    else:
        bg = "#F3F3F3"
        active = "#E7E7E7"
        text = "#000000"
        inactive_text = "#555555"

    # Configure tabview appearance
    tabs.configure(fg_color=bg, segmented_button_fg_color=bg)
    tabs._segmented_button.configure(
        fg_color=bg,
        selected_color=active,
        selected_hover_color=active,
        unselected_color=bg,
        unselected_hover_color=active,
        text_color=text,
        text_color_disabled=inactive_text,
        corner_radius=0,
    )

    return tabs

def tab(parent, label):
    return parent.add(label)


# --- Example usage ---
if __name__ == "__main__":
    root = ctk.CTk()
    root.geometry("700x400")
    root.title("CTk Tabviewer - Visual Studio Style")

    viewer = tabviewer(root)
    t1 = tab(viewer, "Explorer")
    t2 = tab(viewer, "Output")
    t3 = tab(viewer, "Terminal")

    ctk.CTkLabel(t1, text="📂 Project Files").pack(pady=20)
    ctk.CTkLabel(t2, text="📜 Build Output").pack(pady=20)
    ctk.CTkLabel(t3, text="💻 Command Line").pack(pady=20)

    root.mainloop()
