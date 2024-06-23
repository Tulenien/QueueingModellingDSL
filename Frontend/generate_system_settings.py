import tkinter as tk
from tkinter import ttk

# {
#     options: [], of delta and events
#     chosen_delta:true/false
#     chosen_event: true/false
#     small_number_in_ms: int if chosen delta
#     time: int if chosen delta
#     number_of_event: int if chosen_event
#     with_return: true / false
# }


def destroy_text_field_and_label(frame, frame_path, system_settings):
    system_settings["delta"] = ""
    system_settings["event"] = ""
    system_settings["small_number_in_ms"] = -1
    system_settings["number_of_event"] = -1
    system_settings["time"] = -1

    target = frame.nametowidget(frame_path)
    target.pack_forget()
    frame.unbind("<Destroy>")

def on_entry_focus_out_small_number(event, entry, system_settings, frame_to_focus):
    value = entry.get()
    system_settings["small_number_in_ms"] = value
    frame_to_focus.focus()

def make_text_field_to_input_small_number(frame, system_settings):
    label = tk.Label(frame, text="Input small number", bg="#ccddf3", fg="#193d6c", font=('Times', 14, 'bold'))
    label.pack(fill=tk.BOTH, expand=True)  # center label in frame

    text_field = tk.Entry(frame, relief="sunken", width=30, font=("Times", 14, 'bold'), bd=2, fg="#193d6c")
    text_field.pack(pady=15)
    text_field.bind("<Return>", lambda event: on_entry_focus_out_small_number(event, text_field, system_settings, frame))
    return label, text_field

def on_entry_focus_out_time(event, entry, system_settings, frame_to_focus):
    value = entry.get()
    system_settings["time"] = value
    frame_to_focus.focus()

def make_text_field_to_input_time(frame, system_settings):
    label = tk.Label(frame, text="Input time", bg="#ccddf3", fg="#193d6c", font=('Times', 14, 'bold'))
    label.pack(fill=tk.BOTH, expand=True)  # center label in frame

    text_field = tk.Entry(frame, relief="sunken", width=30, font=("Times", 14, 'bold'), bd=2, fg="#193d6c")
    text_field.pack(pady=15)
    text_field.bind("<Return>", lambda event: on_entry_focus_out_time(event, text_field, system_settings, frame))
    return label, text_field


def on_entry_focus_out_number_of_events(event, entry, system_settings, frame_to_focus):
    value = entry.get()
    system_settings["number_of_event"] = value
    frame_to_focus.focus()

def make_text_field_to_input_number_of_events(frame, system_settings):
    label = tk.Label(frame, text="Input number of events", bg="#ccddf3", fg="#193d6c", font=('Times', 14, 'bold'))
    label.pack(fill=tk.BOTH, expand=True)  # center label in frame

    text_field = tk.Entry(frame, relief="sunken", width=30, font=("Times", 14, 'bold'), bd=2, fg="#193d6c")
    text_field.pack(pady=15)
    text_field.bind("<Return>", lambda event: on_entry_focus_out_number_of_events(event, text_field, system_settings, frame))
    return label, text_field



def on_combobox_select(event, combobox, parent_frame, system_settings):
    #firstly destroj previous additional frame
    if len(parent_frame.winfo_children()) > 2:
        destroy_text_field_and_label(parent_frame, parent_frame.winfo_children()[2], system_settings)

    additional_frame = tk.Frame(parent_frame, width=800, height=500, bg="#ccddf3")
    additional_frame.pack()
    value = combobox.get()

    #TODO: kako znati da je delta
    if value == "delta":
        system_settings["chosen_delta"] = True
        system_settings["chosen_event"] = False
        make_text_field_to_input_small_number(additional_frame, system_settings)
        make_text_field_to_input_time(additional_frame, system_settings)

    else:
        system_settings["chosen_event"] = True
        system_settings["chosen_delta"] = False
        make_text_field_to_input_number_of_events(additional_frame, system_settings)



def make_combobox(frame, system_settings):
    label = tk.Label(frame, text="Choose delta or event", bg="#ccddf3", fg="#193d6c", font=('Times', 14, 'bold'))
    label.pack(fill=tk.BOTH, expand=True)  # center label in frame

    combobox = ttk.Combobox(frame, values=system_settings["options"], width=28, background="#ccddf3", foreground="#193d6c", font=('Times', 14, 'bold'))
    combobox.pack(pady=15)

    combobox.bind("<<ComboboxSelected>>", lambda event: on_combobox_select(event, combobox, frame, system_settings))


def on_checkbox_click(system_settings):
    system_settings["with_return"] = checkbox_var.get()

def make_frame(root, system_settings):
    frame = tk.Frame(root, width=800, height=500, bg="#ccddf3")
    frame.pack(pady=10)  # Adding some padding to push the frame down

    label = tk.Label(frame, text="3. GENERATE SYSTEM SETTINGS", bg="#ccddf3", fg="#193d6c", font = ('Times', 16, 'bold'))
    label.pack(pady=30, fill=tk.BOTH, expand=True) #center label in frame

    frame_for_combobox = tk.Frame(frame, width=800, height=500, bg="#ccddf3")
    frame_for_combobox.pack()  # Adding some padding to push the frame down
    make_combobox(frame_for_combobox, system_settings)

    #polje za return
    global checkbox_var
    checkbox_var = tk.BooleanVar()
    checkbox = tk.Checkbutton(frame, text="With return", variable=checkbox_var, width=30, bg="#ccddf3", fg="#193d6c", font=('Times', 14, 'bold'), command=lambda: on_checkbox_click(system_settings))
    checkbox.pack(padx=20, pady=20)

    return frame