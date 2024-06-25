import tkinter as tk
from tkinter import ttk
from distribution import Distributions
from qsystem import QSystem

distribution_name = "NOLAW"

def on_entry_focus_out(event, entry, list_for_values, frame_to_focus):
    value = entry.get()
    list_for_values.append(value) #TODO ADD INTO LIST OF VALUES WHICH QSYTEM ADD PROCESSORS
    frame_to_focus.focus()

def make_text_field(frame, width, padding, list_for_values):
    text_field = tk.Entry(frame, relief="sunken", width=width, font=("Times", 14, 'bold'), bd=2, fg="#193d6c")
    text_field.pack(pady=padding)
    text_field.bind("<Return>", lambda event: on_entry_focus_out(event, text_field, list_for_values, frame))


def make_frame(root, list_for_values):
    frame = tk.Frame(root, width=800, height=500, bg="#ccddf3")
    frame.pack(pady=10)  # Adding some padding to push the frame down

    # firstly you make frame --COMMENT FOR TIM
    frame_for_combobox_info = tk.Frame(frame, width=800, height=500, bg="#ccddf3")
    frame_for_combobox_info.pack(pady=10)  # Adding some padding to push the frame down

    choices = [key for key in Distributions.distribution_dict]
    label = tk.Label(frame_for_combobox_info, text="1. CHOOSE DISTRIBUTION LAW", bg="#ccddf3", fg="#193d6c",
                     font=('Times', 14, 'bold'))
    label.pack(fill=tk.BOTH, expand=True)  # center label in frame

    combobox = ttk.Combobox(frame_for_combobox_info, values=choices, width=28, background="#ccddf3",
                            foreground="#193d6c", font=('Times', 14, 'bold'))
    combobox.pack(pady=15)

    combobox.bind("<<ComboboxSelected>>", lambda event: on_combobox_select(event, combobox, frame, generator_settings))

    label = tk.Label(frame, text="2. NAME PROCESSORS", bg="#ccddf3", fg="#193d6c", font = ('Times', 16, 'bold'))
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

    list_for_parameters = []

    if value == "uniform":
        label = tk.Label(frame, text="ENTER PARAMETER A", bg="#ccddf3", fg="#193d6c", font=('Times', 12, 'bold'))
        label.pack(pady=5, fill=tk.BOTH, expand=True)  # center label in frame
        make_text_field_for_parameter(frame, 30, 5, list_for_parameters)

        label = tk.Label(frame, text="ENTER PARAMETER B", bg="#ccddf3", fg="#193d6c", font=('Times', 12, 'bold'))
        label.pack(pady=5, fill=tk.BOTH, expand=True)  # center label in frame
        make_text_field_for_parameter(frame, 30, 5, list_for_parameters)
    elif value == "normal":
        label = tk.Label(frame, text="ENTER PARAMETER A", bg="#ccddf3", fg="#193d6c", font=('Times', 12, 'bold'))
        label.pack(pady=5, fill=tk.BOTH, expand=True)  # center label in frame
        make_text_field_for_parameter(frame, 30, 5, list_for_parameters)

        label = tk.Label(frame, text="ENTER PARAMETER B", bg="#ccddf3", fg="#193d6c", font=('Times', 12, 'bold'))
        label.pack(pady=5, fill=tk.BOTH, expand=True)  # center label in frame
        make_text_field_for_parameter(frame, 30, 5, list_for_parameters)
    elif value == "increment":
        label = tk.Label(frame, text="ENTER VALUE", bg="#ccddf3", fg="#193d6c", font=('Times', 12, 'bold'))
        label.pack(pady=5, fill=tk.BOTH, expand=True)  # center label in frame
        make_text_field_for_parameter(frame, 30, 5, list_for_parameters)
    else:
        print("default case")

    #generator_settings["law"] = value

    #if value == "NO LAW":
    #    make_text_field_time_to_spend(frame, generator_settings)

def return_parameter(event, entry, list_for_values, frame_to_focus):
    #HERE ADD SOME CODE, this function is called when someone enter something in text field for parameter
    frame_to_focus.focus()

def make_text_field_for_parameter(frame, width, padding, list_for_values):
    text_field = tk.Entry(frame, relief="sunken", width=width, font=("Times", 14, 'bold'), bd=2, fg="#193d6c")
    text_field.pack(pady=padding)
    text_field.bind("<Return>", lambda event: return_parameter(event, text_field, list_for_values, frame))