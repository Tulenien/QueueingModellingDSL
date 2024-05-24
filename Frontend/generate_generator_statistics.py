import tkinter as tk
from tkinter import ttk

def on_combobox_select(event, combobox, list_for_values):
    value = combobox.get()
    list_for_values.append(value)

def make_combobox(frame, options, list_for_values):
    combobox = ttk.Combobox(frame, values=options, width=28, background="#ccddf3", foreground="#193d6c", font=('Times', 14, 'bold'))
    combobox.pack(pady=10)
    combobox.bind("<<ComboboxSelected>>", lambda event: on_combobox_select(event, combobox, list_for_values))


def make_frame(root, options, list_for_values):
    frame = tk.Frame(root, width=800, height=500, bg="#ccddf3")
    frame.pack(pady=10)  # Adding some padding to push the frame down

    label = tk.Label(frame, text="6. GENERATE STATISTICS FOR GENERATORS", bg="#ccddf3", fg="#193d6c", font = ('Times', 16, 'bold'))
    label.pack(pady=20, fill=tk.BOTH, expand=True) #center label in frame

    label = tk.Label(frame, text="CHOOSE GENERATORS", bg="#ccddf3", fg="#193d6c",
                     font=('Times', 14, 'bold'))
    label.pack(fill=tk.BOTH, expand=True)  # center label in frame

    frame_for_combobox = tk.Frame(frame, width=800, height=500, bg="#ccddf3")
    frame_for_combobox.pack()  # Adding some padding to push the frame down
    make_combobox(frame_for_combobox, options, list_for_values)

    button = tk.Button(frame, text="ADD NEXT", foreground='#193d6c', background='#b7c6da', relief='raised', font=('Times', 12, 'bold'),  command=lambda:make_combobox(frame_for_combobox, options, list_for_values))
    button.pack(pady=20)

    return frame