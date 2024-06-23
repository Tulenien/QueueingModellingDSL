import tkinter as tk
import stylization
import generate_generators
import generate_processors
import generate_system_settings
import generate_generators_settings
import generate_processors_settings
import generate_generator_statistics
import generate_processor_statistics
from qsystem import QSystem

qsystem = QSystem()

all_generators = [] #used for the first page to collect names of generators
all_processors = [] #used for the second page to collect names of processors

#add current option, delete delta, event, choosen things
system_settings = {
    "options": ["delta", "event1", "event2"],
    "chosen_delta": False,
    "delta": "",
    "chosen_event": False,
    "event": "",
    "small_number_in_ms": -1,
    "time": -1,
    "number_of_event": -1,
    "with_return": False
}
generator_settings = {
    "law": "",
    "time_to_spend": ""
}

processors_settings = {
    "law": "",
    "time_to_spend": "",
    "memory_capacity": "",
    "generators": []
}

generators_statistics = {
    "generators_from_backend": [], #get all generators from backend
    "chosen_generators": []
}

processors_statistics = {
    "processors_from_backend": [], #get all processors from backend
    "chosen_processors": []
}

def destroy_generate_generators_frame(frame, root):
    frame.pack_forget()
    call_second_page(root)



def call_second_page(root):
    gp_frame = generate_processors.make_frame(root, qsystem) #all_processors
    button = tk.Button(gp_frame, text="NEXT PAGE",
                       command=lambda: destroy_generate_processors_frame(gp_frame, root), foreground='#b7c6da',
                       background='#193d6c', relief='raised', font=('Times', 12, 'bold'))
    button.pack(pady=20)

def destroy_generate_processors_frame(frame, root):
    frame.pack_forget()
    call_third_page(root)



def call_third_page(root):
    ss_frame = generate_system_settings.make_frame(root, system_settings)
    button = tk.Button(ss_frame, text="NEXT PAGE",
                       command=lambda: destroy_system_settings(ss_frame, root), foreground='#b7c6da',
                       background='#193d6c', relief='raised', font=('Times', 12, 'bold'))
    button.pack(pady=20)

def destroy_system_settings(frame, root):
    frame.pack_forget()
    call_forth_page(root)

def call_forth_page(root):
    gs_frame = generate_generators_settings.make_frame(root, generator_settings)
    button = tk.Button(gs_frame, text="NEXT PAGE",
                       command=lambda: destroy_generate_generators_settings(gs_frame, root), foreground='#b7c6da',
                       background='#193d6c', relief='raised', font=('Times', 12, 'bold'))
    button.pack(pady=20)

def destroy_generate_generators_settings(frame, root):
    frame.pack_forget()
    call_fifth_page(root)


def call_fifth_page(root):
    gs_frame = generate_processors_settings.make_frame(root, all_generators, processors_settings)
    button = tk.Button(gs_frame, text="NEXT PAGE",
                       command=lambda: destroy_generate_processor_settings(gs_frame, root), foreground='#b7c6da',
                       background='#193d6c', relief='raised', font=('Times', 12, 'bold'))
    button.pack(pady=20)

def destroy_generate_processor_settings(frame, root):
    frame.pack_forget()
    call_sixth_page(root)

def call_sixth_page(root):
    #TODO: GET FROM BACKEND GENERATORS IN USE. I ADDED THESE JUST TO TRY FRONT
    generators_statistics["generators_from_backend"] = ["GEN1", "GEN2", "gEN3"]
    ggs_frame = generate_generator_statistics.make_frame(root, generators_statistics["generators_from_backend"], generators_statistics["chosen_generators"])
    button = tk.Button(ggs_frame, text="NEXT PAGE",
                       command=lambda: destroy_generate_generators_statistics_frame(ggs_frame, root), foreground='#b7c6da',
                       background='#193d6c', relief='raised', font=('Times', 12, 'bold'))
    button.pack(pady=20)


def destroy_generate_generators_statistics_frame(frame, root):
    frame.pack_forget()
    call_seventh_page(root)


def call_seventh_page(root):
    # TODO: GET FROM BACKEND PROCESSORS IN USE. I ADDED THESE JUST TO TRY FRONT
    processors_statistics["processors_from_backend"] = ["PROC1", "PROC2", "PROC3"]
    gps_frame = generate_processor_statistics.make_frame(root, processors_statistics["processors_from_backend"],
                                                         processors_statistics["chosen_processors"])
    button = tk.Button(gps_frame, text="FINISH",
                       command=lambda: destroy_generate_processors_statistics_frame(gps_frame, root),
                       foreground='#b7c6da',
                       background='#193d6c', relief='raised', font=('Times', 12, 'bold'))
    button.pack(pady=20)


def destroy_generate_processors_statistics_frame(frame, root):
    frame.pack_forget()

    label = tk.Label(root, text="THANK YOU FOR YOUR INPUT!  HAVE A NICE DAY! :)", bg="#ccddf3", fg="#193d6c",
                     font=('Times', 14, 'bold'))
    label.pack(pady=10, fill=tk.BOTH, expand=True)  # center label in frame

    on_window_close(root)

def on_window_close(root):
    print(all_generators)
    print(all_processors)
    print(system_settings)
    print(generator_settings)
    print(processors_settings)
    print(generators_statistics)
    print(processors_statistics)
    root.unbind("<Destroy>")




if __name__ == "__main__":
    # root window
    root = tk.Tk()
    stylization.default_window(root, "TNT", "800x800", "#ccddf3")
    stylization.center_window(root)
    root.resizable(False, False)

    #first window - generate generators
    gg_frame = generate_generators.make_frame(root, qsystem) #all_generators TODO: qsystem
    button = tk.Button(gg_frame, text="NEXT PAGE",
                       command=lambda: destroy_generate_generators_frame(gg_frame, root), foreground='#b7c6da',
                       background='#193d6c', relief='raised', font=('Times', 12, 'bold'))
    button.pack(pady=20)

    root.bind("<Destroy>", lambda event: on_window_close(root))
    root.mainloop()