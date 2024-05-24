import tkinter as tk
from tkinter import ttk

def on_entry_time_to_spend(event, entry, processors_settings):
    value = entry.get()
    processors_settings["time_to_spend"] = value


def make_text_field_time_to_spend(frame, processors_settings):
    label = tk.Label(frame, text="If no law enter time to spend", bg="#ccddf3", fg="#193d6c", font=('Times', 14, 'bold'))
    label.pack(fill=tk.BOTH, expand=True)  # center label in frame

    text_field = tk.Entry(frame, relief="sunken", width=30, font=("Times", 14, 'bold'), bd=2, fg="#193d6c")
    text_field.pack(pady=15)
    text_field.bind("<FocusOut>", lambda event: on_entry_time_to_spend(event, text_field, processors_settings))
    return label, text_field


def on_combobox_select(event, combobox, frame, processors_settings):
    value = combobox.get()
    processors_settings["law"] = value

    if value == "NO LAW":
        make_text_field_time_to_spend(frame, processors_settings)


def make_combobox(frame, processors_settings, options):
    label = tk.Label(frame, text="Choose law", bg="#ccddf3", fg="#193d6c", font=('Times', 14, 'bold'))
    label.pack(fill=tk.BOTH, expand=True)  # center label in frame

    combobox = ttk.Combobox(frame, values=options, width=28, background="#ccddf3", foreground="#193d6c", font=('Times', 14, 'bold'))
    combobox.pack(pady=15)

    combobox.bind("<<ComboboxSelected>>", lambda event: on_combobox_select(event, combobox, frame, processors_settings))


def on_entry_memory_capacity(event, entry, processors_settings):
    value = entry.get()
    processors_settings["memory_capacity"] = value


def make_text_field_memory_capacity(frame, processors_settings):
    label = tk.Label(frame, text="Memory capacity", bg="#ccddf3", fg="#193d6c", font=('Times', 14, 'bold'))
    label.pack(fill=tk.BOTH, expand=True)  # center label in frame

    text_field = tk.Entry(frame, relief="sunken", width=30, font=("Times", 14, 'bold'), bd=2, fg="#193d6c")
    text_field.pack(pady=15)
    text_field.bind("<FocusOut>", lambda event: on_entry_memory_capacity(event, text_field, processors_settings))
    return label, text_field


def connect_generators(frame, options, list_for_values):
    combobox = ttk.Combobox(frame, values=options)
    combobox.pack(pady=10)
    combobox.bind("<<ComboboxSelected>>", lambda event: on_combobox_select(event, combobox, list_for_values))

def make_combobox(frame, options, list_for_values):
    label = tk.Label(frame, text="Choose law", bg="#ccddf3", fg="#193d6c", font=('Times', 14, 'bold'))
    label.pack(fill=tk.BOTH, expand=True)  # center label in frame

    combobox = ttk.Combobox(frame, values=options, width=28, background="#ccddf3", foreground="#193d6c", font=('Times', 14, 'bold'))
    combobox.pack(pady=10)
    combobox.bind("<<ComboboxSelected>>", lambda event: on_combobox_select(event, combobox, frame, list_for_values))


def on_generator_combobox_select(event, combobox, processors_settings):
    value = combobox.get()
    processors_settings["generators"].append(value)


def make_generators_combobox(frame, all_generators, list_for_values):
    label = tk.Label(frame, text="Choose generator", bg="#ccddf3", fg="#193d6c", font=('Times', 14, 'bold'))
    label.pack(fill=tk.BOTH, expand=True)  # center label in frame

    combobox = ttk.Combobox(frame, values=all_generators,  width=28, background="#ccddf3", foreground="#193d6c", font=('Times', 14, 'bold'))
    combobox.pack(pady=10)
    combobox.bind("<<ComboboxSelected>>", lambda event: on_generator_combobox_select(event, combobox, list_for_values))


def make_frame(root, all_generators, processors_settings):
    frame = tk.Frame(root, width=800, height=500, bg="#ccddf3")
    frame.pack(pady=10)  # Adding some padding to push the frame down

    label = tk.Label(frame, text="5. GENERATE PROCESSORS SETTINGS", bg="#ccddf3", fg="#193d6c", font = ('Times', 16, 'bold'))
    label.pack(pady=30, fill=tk.BOTH, expand=True) #center label in frame

    frame_for_combobox = tk.Frame(frame, width=800, height=500, bg="#ccddf3")
    frame_for_combobox.pack()  # Adding some padding to push the frame down
    options = ["GAUS", "UNIFORM", "NO LAW"]
    make_combobox(frame_for_combobox, options, processors_settings)

    #memory capacity
    make_text_field_memory_capacity(frame, processors_settings)

    #connected generators
    frame_for_generator_combobox = tk.Frame(frame, width=800, height=500, bg="#ccddf3")
    frame_for_generator_combobox.pack()  # Adding some padding to push the frame down

    make_generators_combobox(frame_for_generator_combobox, all_generators, processors_settings)

    button = tk.Button(frame, text="ADD NEXT GENERATOR", foreground='#193d6c', background='#b7c6da', relief='raised',
                       font=('Times', 12, 'bold'),
                       command=lambda: make_generators_combobox(frame_for_generator_combobox, all_generators, processors_settings))
    button.pack(pady=20)

    return frame