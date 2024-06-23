import tkinter as tk
from tkinter import ttk

def on_entry_time_to_spend(event, entry, generator_settings, frame_to_focus):
    value = entry.get()
    generator_settings["time_to_spend"] = value
    frame_to_focus.focus()


def make_text_field_time_to_spend(frame, generator_settings):
    label = tk.Label(frame, text="If no law enter time to spend", bg="#ccddf3", fg="#193d6c", font=('Times', 14, 'bold'))
    label.pack(fill=tk.BOTH, expand=True)  # center label in frame

    text_field = tk.Entry(frame, relief="sunken", width=30, font=("Times", 14, 'bold'), bd=2, fg="#193d6c")
    text_field.pack(pady=15)
    text_field.bind("<Return>", lambda event: on_entry_time_to_spend(event, text_field, generator_settings, frame))
    return label, text_field


def on_combobox_select(event, combobox, frame, generator_settings):
    value = combobox.get()
    generator_settings["law"] = value

    if value == "NO LAW":
        make_text_field_time_to_spend(frame, generator_settings)


def make_combobox(frame, generator_settings, options):
    label = tk.Label(frame, text="Choose law", bg="#ccddf3", fg="#193d6c", font=('Times', 14, 'bold'))
    label.pack(fill=tk.BOTH, expand=True)  # center label in frame

    combobox = ttk.Combobox(frame, values=options, width=28, background="#ccddf3", foreground="#193d6c", font=('Times', 14, 'bold'))
    combobox.pack(pady=15)

    combobox.bind("<<ComboboxSelected>>", lambda event: on_combobox_select(event, combobox, frame, generator_settings))


def make_frame(root, generator_settings):
    frame = tk.Frame(root, width=800, height=500, bg="#ccddf3")
    frame.pack(pady=10)  # Adding some padding to push the frame down

    label = tk.Label(frame, text="4. GENERATE GENERATOR SETTINGS", bg="#ccddf3", fg="#193d6c", font = ('Times', 16, 'bold'))
    label.pack(pady=30, fill=tk.BOTH, expand=True) #center label in frame

    frame_for_combobox = tk.Frame(frame, width=800, height=500, bg="#ccddf3")
    frame_for_combobox.pack()  # Adding some padding to push the frame down
    options = ["GAUS", "UNIFORM", "NO LAW"]
    make_combobox(frame_for_combobox, generator_settings, options)
    return frame