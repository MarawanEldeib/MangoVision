import tkinter as tk
import webbrowser

def create_menu(app):
    app.toolbar = tk.Menu(app.root)
    app.root.config(menu=app.toolbar)

    app.language_menu = tk.Menu(app.toolbar, tearoff=0)
    app.toolbar.add_cascade(label=app.get_text("language"), menu=app.language_menu)
    app.language_menu.add_command(label="English", command=lambda: app.switch_language("en"))
    app.language_menu.add_command(label="Malay", command=lambda: app.switch_language("ms"))

    app.model_menu = tk.Menu(app.toolbar, tearoff=0)
    app.toolbar.add_cascade(label=app.get_text("model"), menu=app.model_menu)
    app.model_menu.add_command(label=app.get_text("model_1"), command=lambda: app.switch_model(1))
    app.model_menu.add_command(label=app.get_text("model_2"), command=lambda: app.switch_model(2))

    app.threshold_menu = tk.Menu(app.toolbar, tearoff=0)
    app.toolbar.add_cascade(label=app.get_text("threshold"), menu=app.threshold_menu)
    app.threshold_menu.add_command(label=app.get_text("confidence_threshold"), command=app.set_confidence_threshold)

    app.help_menu = tk.Menu(app.toolbar, tearoff=0)
    app.toolbar.add_cascade(label=app.get_text("contact"), menu=app.help_menu)
    app.help_menu.add_command(label=app.get_text("contact"), command=lambda: webbrowser.open("mailto:Marawandeep13@gmail.com"))
