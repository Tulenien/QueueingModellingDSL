import tkinter as tk

def on_entry_focus_out(event, entry, list_for_values, frame_to_focus):
    value = entry.get()
    list_for_values.add_information_source() #TODO: add generators into list_for_values which is qsytem
    frame_to_focus.focus()

def make_text_field(frame, width, padding, list_for_values):
    text_field = tk.Entry(frame, relief="sunken", width=width, font=("Times", 14, 'bold'), bd=2, fg="#193d6c")
    text_field.pack(pady=padding)
    text_field.bind("<Return>", lambda event: on_entry_focus_out(event, text_field, list_for_values, frame))


def make_frame(root, list_for_values): #list_for_values is qsystem
    frame = tk.Frame(root, width=800, height=500, bg="#ccddf3")
    frame.pack(pady=10)  # Adding some padding to push the frame down

    label = tk.Label(frame, text="1. NAME GENERATORS", bg="#ccddf3", fg="#193d6c", font = ('Times', 16, 'bold'))
    label.pack(pady=20, fill=tk.BOTH, expand=True) #center label in frame

    frame_for_text_fields = tk.Frame(frame, width=800, height=500, bg="#ccddf3")
    frame_for_text_fields.pack()  # Adding some padding to push the frame down
    make_text_field(frame_for_text_fields, 30, 10, list_for_values)

    button = tk.Button(frame, text="ADD NEXT", foreground='#193d6c', background='#b7c6da', relief='raised', font=('Times', 12, 'bold'),  command=lambda:make_text_field(frame_for_text_fields, 30, 10, list_for_values))
    button.pack(pady=20)

    return frame

