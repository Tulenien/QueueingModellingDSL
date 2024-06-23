import tkinter as tk
from tkinter import ttk
from distribution import Distributions
from qsystem import QSystem

distribution_name = "NOLAW"

def on_entry_focus_out(event, entry, list_for_values, frame_to_focus):
    value = entry.get()
    function = Distributions.get_distribution(distribution_name)
    # Need a field for args depending on the law chosen
    generator = RandomGenerator(function, args)
    list_for_values.add_information_source(generator, name)
    frame_to_focus.focus()

def make_text_field(frame, width, padding, list_for_values):
    text_field = tk.Entry(frame, relief="sunken", width=width, font=("Times", 14, 'bold'), bd=2, fg="#193d6c")
    text_field.pack(pady=padding)
    text_field.bind("<Return>", lambda event: on_entry_focus_out(event, text_field, list_for_values, frame))


def make_frame(root, list_for_values): #list_for_values is qsystem
    frame = tk.Frame(root, width=800, height=500, bg="#ccddf3")
    frame.pack(pady=10)  # Adding some padding to push the frame down

    choices = [key for key in Distributions.distribution_dict]
    label = tk.Label(frame, text="1. CHOOSE DISTRIBUTION LAW", bg="#ccddf3", fg="#193d6c", font=('Times', 14, 'bold'))
    label.pack(fill=tk.BOTH, expand=True)  # center label in frame

    combobox = ttk.Combobox(frame, values=choices, width=28, background="#ccddf3", foreground="#193d6c", font=('Times', 14, 'bold'))
    combobox.pack(pady=15)

    combobox.bind("<<ComboboxSelected>>", lambda event: on_combobox_select(event, combobox, frame, generator_settings))

    label = tk.Label(frame, text="NAME GENERATORS", bg="#ccddf3", fg="#193d6c", font = ('Times', 14, 'bold'))
    label.pack(pady=20, fill=tk.BOTH, expand=True) #center label in frame

    frame_for_text_fields = tk.Frame(frame, width=800, height=500, bg="#ccddf3")
    frame_for_text_fields.pack()  # Adding some padding to push the frame down
    make_text_field(frame_for_text_fields, 30, 10, list_for_values)

    button = tk.Button(frame, text="ADD NEXT", foreground='#193d6c', background='#b7c6da', relief='raised', font=('Times', 12, 'bold'),  command=lambda:make_text_field(frame_for_text_fields, 30, 10, list_for_values))
    button.pack(pady=20)

    return frame


def on_combobox_select(event, combobox, frame, generator_settings):
    value = combobox.get()
    distribution_name = value

    match value:
        case "uniform":
        # TODO: make as much fields as we have parameters in the function:
        # def uniform(a, b)
        # def normal(a, b):
        # def increment(value):
            pass
        case _: #default case
            pass

    #generator_settings["law"] = value

    #if value == "NO LAW":
    #    make_text_field_time_to_spend(frame, generator_settings)

