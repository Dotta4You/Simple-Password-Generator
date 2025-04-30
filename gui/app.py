import customtkinter as ctk
from generator.password_generator import generate_password
import tkinter as tk
import time

def start_app():
    ctk.set_appearance_mode("dark")
    ctk.set_default_color_theme("blue")

    app = ctk.CTk()
    app.title("Simple Password Generator")
    app.geometry("580x330")
    app.resizable(False, False)

    titel = ctk.CTkLabel(app, text="🔒 Simple Password Generator", font=ctk.CTkFont(size=22, weight="bold"))
    titel.pack(pady=(18, 5))

    last_copy_time = [0]

    ausgabe = ctk.CTkEntry(app, width=400, font=ctk.CTkFont(size=16), justify="center")
    ausgabe.pack(pady=10)
    ausgabe.configure(state="readonly")
    original_fg_color = ausgabe.cget("fg_color")

    def animate_fg_color(widget, start_color, end_color, duration=240, original_fg=None):
        steps = 8
        sleep_time = duration // (2 * steps)
        def hex_to_rgb(c):
            if isinstance(c, (tuple, list)):
                c = c[0]
            if not isinstance(c, str):
                c = str(c)
            c = c.lstrip("#")
            return tuple(int(c[i:i+2], 16) for i in (0, 2, 4))
        def rgb_to_hex(rgb):
            return "#%02x%02x%02x" % rgb

        rgb_start = hex_to_rgb(start_color)
        rgb_end = hex_to_rgb(end_color)
        forw = []
        for i in range(steps):
            now = tuple(int(rgb_start[j] + (rgb_end[j] - rgb_start[j]) * (i+1) / steps) for j in range(3))
            forw.append(rgb_to_hex(now))
        back = forw[::-1]
        sequence = forw + back

        def do_anim(idx=0):
            if idx < len(sequence):
                widget.configure(fg_color=sequence[idx])
                app.after(sleep_time, do_anim, idx+1)
            else:
                widget.configure(fg_color=original_fg if original_fg is not None else start_color)
        do_anim()

    popup_animating = [False]
    def show_popup(message_text):
        if popup_animating[0]:
            return
        popup_animating[0] = True

        popup = ctk.CTkToplevel(app)
        popup.overrideredirect(True)
        popup.attributes("-topmost", True)
        popup.attributes("-alpha", 0.0)

        width, height = 115, 34
        margin_x, margin_y = 14, 14

        app.update_idletasks()
        app_x = app.winfo_x()
        app_y = app.winfo_y()
        app_w = app.winfo_width()
        app_h = app.winfo_height()

        tgt_x = app_x + app_w - width - margin_x
        tgt_y = app_y + app_h - height - margin_y
        start_y = tgt_y + 8

        geo_width = width
        geo_height = height
        geo_x = tgt_x
        geo_start_y = start_y
        geo_tgt_y = tgt_y

        popup.update_idletasks()
        screen_w = popup.winfo_screenwidth()
        screen_h = popup.winfo_screenheight()

        if geo_x + geo_width > screen_w:
            geo_x = screen_w - geo_width - 6
        if geo_x < 0:
            geo_x = 6
        if geo_tgt_y + geo_height > screen_h:
            geo_tgt_y = screen_h - geo_height - 6
            geo_start_y = geo_tgt_y + 8
        if geo_tgt_y < 0:
            geo_tgt_y = 6
            geo_start_y = geo_tgt_y + 8

        popup.geometry(f"{geo_width}x{geo_height}+{geo_x}+{geo_start_y}")

        corner = int(height / 2)
        popup_frame = ctk.CTkFrame(
            popup,
            fg_color="#252e2a",
            corner_radius=corner
        )
        popup_frame.pack(expand=True, fill="both", padx=0, pady=0)
        lbl = ctk.CTkLabel(
            popup_frame,
            text=message_text,
            text_color="#8fffab",
            fg_color="transparent",
            font=ctk.CTkFont(size=13, weight="bold"),
            anchor="center",
            padx=7, pady=6
        )
        lbl.pack(expand=True, fill="both")

        slide_steps = 8
        stay_time = 900

        def slide_fade_in(step=0):
            if step <= slide_steps:
                frac = step / slide_steps
                new_y = int(geo_start_y - (geo_start_y - geo_tgt_y) * frac)
                popup.geometry(f"{geo_width}x{geo_height}+{geo_x}+{new_y}")
                popup.attributes("-alpha", frac)
                popup.after(15, slide_fade_in, step+1)
            else:
                popup.geometry(f"{geo_width}x{geo_height}+{geo_x}+{geo_tgt_y}")
                popup.attributes("-alpha", 1.0)
                popup.after(stay_time, slide_fade_out)

        def slide_fade_out(step=0):
            if step <= slide_steps:
                frac = 1 - (step / slide_steps)
                new_y = int(geo_start_y - (geo_start_y - geo_tgt_y) * frac)
                popup.geometry(f"{geo_width}x{geo_height}+{geo_x}+{new_y}")
                popup.attributes("-alpha", frac)
                popup.after(15, slide_fade_out, step+1)
            else:
                popup.destroy()
                popup_animating[0] = False

        slide_fade_in()


    def kopieren_mit_feedback(event=None):
        now = time.time()
        if now - last_copy_time[0] < 1.0:
            return
        last_copy_time[0] = now

        app.clipboard_clear()
        app.clipboard_append(ausgabe.get())

        orig_fg_color = ausgabe.cget("fg_color")
        ausgabe.configure(fg_color="#35d46e")
        app.after(450, lambda: ausgabe.configure(fg_color=orig_fg_color))
        show_popup("Passwort kopiert!")

    ausgabe.bind("<Button-1>", kopieren_mit_feedback)


    # Einstellungen
    rahmen = ctk.CTkFrame(app)
    rahmen.pack(pady=8, padx=36, fill="x")

    label_laenge = ctk.CTkLabel(rahmen, text="Länge:")
    label_laenge.grid(row=0, column=0, padx=(10, 1), pady=12, sticky="w")

    label_value_var = tk.StringVar(value="12")

    def ersetzen_mit_entry(event):
        label_value.grid_remove()
        entry_value.delete(0, tk.END)
        entry_value.insert(0, label_value_var.get())
        entry_value.grid(row=0, column=2, padx=(9, 4), pady=12, sticky="w")
        entry_value.focus()
        entry_value.select_range(0, tk.END)

    def entry_value_live(event=None):
        val = entry_value.get()
        try:
            val_int = int(val)
        except ValueError:
            return
        if val_int < 6:
            val_int = 6
        if val_int > 100:
            val_int = 100
        slider.set(val_int)
        label_value_var.set(str(val_int))
        neues_passwort()

    def entry_value_confirm(event=None):
        val = entry_value.get()
        try:
            val_int = int(val)
        except ValueError:
            val_int = last_slider_value[0]
        if val_int < 6:
            val_int = 6
        if val_int > 100:
            val_int = 100
        slider.set(val_int)
        label_value_var.set(str(val_int))
        entry_value.grid_remove()
        label_value.configure(text=str(val_int))
        label_value.grid(row=0, column=2, padx=(9, 4), pady=12, sticky="w")

    label_value = ctk.CTkLabel(rahmen, textvariable=label_value_var, width=44, cursor="hand2")
    label_value.grid(row=0, column=2, padx=(9, 4), pady=12, sticky="w")
    label_value.bind("<Button-1>", ersetzen_mit_entry)

    entry_value = ctk.CTkEntry(
        rahmen,
        width=44,
        justify="center"
    )
    entry_value.bind("<Return>", entry_value_confirm)
    entry_value.bind("<FocusOut>", lambda e: entry_value_confirm())
    entry_value.bind("<KeyRelease>", entry_value_live)

    slider = ctk.CTkSlider(
        rahmen,
        from_=6,
        to=100,
        number_of_steps=94,
        width=265,
    )
    slider.set(12)
    slider.grid(row=0, column=1, padx=12, pady=12, sticky="we")

    digits_var = tk.BooleanVar(value=True)
    spez_var = tk.BooleanVar(value=True)
    upper_var = tk.BooleanVar(value=True)

    cb_digits = ctk.CTkCheckBox(rahmen, text="Zahlen", variable=digits_var)
    cb_spez = ctk.CTkCheckBox(rahmen, text="Sonderz.", variable=spez_var)
    cb_upper = ctk.CTkCheckBox(rahmen, text="Großbuchstaben", variable=upper_var)

    cb_digits.grid(row=1, column=0, padx=13, pady=5, sticky="n")
    cb_upper.grid(row=1, column=1, padx=13, pady=5, sticky="n")
    cb_spez.grid(row=1, column=2, padx=13, pady=5, sticky="n")
    rahmen.grid_columnconfigure(0, weight=1)
    rahmen.grid_columnconfigure(1, weight=1)
    rahmen.grid_columnconfigure(2, weight=1)

    last_slider_value = [int(slider.get())]

    def neues_passwort(*args):
        laenge = int(slider.get())
        pw = generate_password(
            length=laenge,
            use_digits=digits_var.get(),
            use_specials=spez_var.get(),
            use_upper=upper_var.get()
        )
        ausgabe.configure(state="normal")
        ausgabe.delete(0, "end")
        ausgabe.insert(0, pw)
        ausgabe.configure(state="readonly")
        label_value_var.set(str(laenge))
        last_slider_value[0] = laenge

    button_gen = ctk.CTkButton(app, text="Generieren", command=neues_passwort, width=140)
    button_gen.pack(pady=(12, 3))
    button_copy = ctk.CTkButton(app, text="Kopieren", command=kopieren_mit_feedback, width=140)
    button_copy.pack(pady=(2, 10))

    def update_slider(value):
        wert = int(float(value))
        if wert != last_slider_value[0]:
            label_value_var.set(str(wert))
            neues_passwort()
        else:
            label_value_var.set(str(wert))

    slider.configure(command=update_slider)
    cb_digits.configure(command=neues_passwort)
    cb_spez.configure(command=neues_passwort)
    cb_upper.configure(command=neues_passwort)

    neues_passwort()
    app.mainloop()