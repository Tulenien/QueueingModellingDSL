import tkinter as tk
from tkinter import ttk
import os
from tkinter import filedialog, messagebox
from backend.qsystem import QSystem
from backend.qmodel import QModel
from backend.distribution import Distributions, RandomGenerator

class MainApp(tk.Tk):
    # QModelling Defaults
    DEFAULT_GEN_NAME = "G"
    DEFAULT_PROC_NAME = "P"
    DEFAULT_A_PARAM = 1
    DEFAULT_B_PARAM = 2
    DEFAULT_SELECTED_RG = "normal"
    DEFAULT_SELECTED_ST = "timed"
    DEFAULT_SELECTED_GEN = ""
    DEFAULT_SELECTED_PROC = ""

    # GUI Defaults
    BACKGROUND_LABEL_COLOR = "#CCDDF3"
    FOREGROUND_LABEL_COLOR = "#193D6C"
    FOREGROUND_BUTTON_COLOR = "#F5F5F5"
    BACKGROND_BUTTON_COLOR = "#193D6C"
    
    FONT_ENTRIES = ("Times", 14, "bold")
    FONT_REGULAR = ("Times", 12, "bold")
    FONT_LABEL = ("Times", 10, "bold")

    def __init__(self):
        self.qsystem = QSystem()
        self.qmodel = QModel()
        self.model_file_path = None
        self.metamodel_file_path = None
        self.requests = []

        this_folder = os.path.dirname(__file__)
        self.model_file_path = os.path.join(this_folder, 'models/program.qs')
        self.metamodel_file_path = os.path.join(this_folder, 'models/qsystem.tx')

        super().__init__()
        self.title("Main Window")
        self.geometry("800x600")
        self.configure(bg=MainApp.BACKGROUND_LABEL_COLOR)
        self.center_window()
        self.selected_system_type = tk.StringVar()
        self.selected_generator = tk.StringVar()
        self.selected_processor = tk.StringVar()
        self.selected_random_generator = tk.StringVar()
        self.selected_system_type.set(MainApp.DEFAULT_SELECTED_ST)
        self.selected_processor.set(MainApp.DEFAULT_SELECTED_PROC)
        self.selected_random_generator.set(MainApp.DEFAULT_SELECTED_RG)

        self.gen_a = MainApp.DEFAULT_A_PARAM
        self.gen_b = MainApp.DEFAULT_B_PARAM
        self.proc_a = MainApp.DEFAULT_A_PARAM
        self.proc_b = MainApp.DEFAULT_B_PARAM
        self.gen_name = MainApp.DEFAULT_GEN_NAME
        self.proc_name = MainApp.DEFAULT_PROC_NAME
        self.gen_edit_mode = False
        self.proc_edit_mode = False
        self.start()

    def check_parameters(self, func, *args):
        flag = True
        for arg in args:
            flag &= func(arg)
            if not flag:
                break
        return flag

    def check_int_parameters(self, value):
        if type(value) == "int":
            return True
        return False

    def check_float_parameters(self, value):
        if type(value) == "float":
            return True
        return False

    def center_window(self):
        self.update_idletasks()
        width = self.winfo_width()
        height = self.winfo_height()
        x_offset = (self.winfo_screenwidth() - width) // 2
        y_offset = (self.winfo_screenheight() - height) // 2
        self.geometry('{}x{}+{}+{}'.format(width, height, x_offset, y_offset))

    def clear_window(self):
        for widget in self.winfo_children():
            widget.destroy()

    def start(self):
        self.clear_window()

        self.welcome_label = tk.Label(self, text="QUEUEING MODELLING DSL", bg=MainApp.BACKGROUND_LABEL_COLOR, fg=MainApp.FOREGROUND_LABEL_COLOR,
                         font=MainApp.FONT_ENTRIES)
        self.welcome_label.pack(fill=tk.BOTH, pady=30)  # center label in frame

        self.return_button = tk.Button(self, text="INPUT  MODEL  PARAMETERS", command=self.setup_system_widget, foreground=MainApp.FOREGROUND_BUTTON_COLOR,
                       background=MainApp.BACKGROND_BUTTON_COLOR, relief='raised', font=MainApp.FONT_REGULAR, width=30)
        self.return_button.pack(pady=15)

        self.open_file_button = tk.Button(self, text="LOAD TEXTX MODEL", command=self.load_model, foreground=MainApp.FOREGROUND_BUTTON_COLOR,
                       background=MainApp.BACKGROND_BUTTON_COLOR, relief='raised', font=MainApp.FONT_REGULAR,  width=30)
        self.open_file_button.pack(pady=15)

        self.use_cached_model_button = tk.Button(self, text="USE SAVED TEXTX MODEL", command=self.create_simulation_widget, foreground=MainApp.FOREGROUND_BUTTON_COLOR,
                       background=MainApp.BACKGROND_BUTTON_COLOR, relief='raised', font=MainApp.FONT_REGULAR,  width=30)
        self.use_cached_model_button.pack(pady=15)


        if self.model_file_path:
            self.file_path_label = tk.Label(self, text=f"Selected model file: {self.model_file_path}", bg=MainApp.BACKGROUND_LABEL_COLOR, fg=MainApp.FOREGROUND_LABEL_COLOR,
                         font=MainApp.FONT_LABEL)
            self.file_path_label.pack(pady=15)
        if self.metamodel_file_path:
            self.metamodel_path_label = tk.Label(self, text=f"Selected metamodel file: {self.metamodel_file_path}", bg=MainApp.BACKGROUND_LABEL_COLOR, fg=MainApp.FOREGROUND_LABEL_COLOR,
                         font=MainApp.FONT_LABEL)
            self.metamodel_path_label.pack()


    def display_system_constraints_entry(self, frame):
        choice = self.selected_system_type.get()
        if choice == 'timed':
            self.time_constraint_entry_label = tk.Label(frame, text="2. SYSTEM TIME CONSTRAINT", bg=MainApp.BACKGROUND_LABEL_COLOR,
                                                        fg=MainApp.FOREGROUND_LABEL_COLOR,
                                                        font=MainApp.FONT_REGULAR)
            self.time_constraint_entry_label.pack()

            self.time_constraint_entry = tk.Entry(frame, relief="sunken", width=20, font=MainApp.FONT_ENTRIES, bd=2, fg=MainApp.FOREGROUND_LABEL_COLOR)
            self.time_constraint_entry.insert(tk.END, str(self.qsystem.get_time_constraint()))
            self.time_constraint_entry.pack(pady=15)

        elif choice == 'requests':
            self.requests_constraint_entry_label = tk.Label(frame, text="2. SYSTEM REQUESTS NUMBER CONSTRAINT",
                                                            bg=MainApp.BACKGROUND_LABEL_COLOR, fg=MainApp.FOREGROUND_LABEL_COLOR,
                                                            font=MainApp.FONT_REGULAR)
            self.requests_constraint_entry_label.pack()
            self.requests_constraint_entry = tk.Entry(frame, relief="sunken", width=20, font=MainApp.FONT_ENTRIES, bd=2, fg=MainApp.FOREGROUND_LABEL_COLOR)
            self.requests_constraint_entry.insert(tk.END, str(self.qsystem.get_requests_constraint()))
            self.requests_constraint_entry.pack(pady=15)

        else:
            self.time_constraint_entry_label = tk.Label(frame, text="2. SYSTEM TIME CONSTRAINT", bg=MainApp.BACKGROUND_LABEL_COLOR,
                                                        fg=MainApp.FOREGROUND_LABEL_COLOR,
                                                        font=MainApp.FONT_REGULAR)
            self.time_constraint_entry_label.pack()
            self.time_constraint_entry = tk.Entry(frame, relief="sunken", width=20, font=MainApp.FONT_ENTRIES, bd=2, fg=MainApp.FOREGROUND_LABEL_COLOR)
            self.time_constraint_entry.pack(pady=15)

        self.delta_constraint_label = tk.Label(frame, text="3. SYSTEM TIME DELTA CONSTRAINT", bg=MainApp.BACKGROUND_LABEL_COLOR, fg=MainApp.FOREGROUND_LABEL_COLOR,
                                               font=MainApp.FONT_REGULAR)
        self.delta_constraint_label.pack()
        self.delta_constraint_entry = tk.Entry(frame, relief="sunken", width=20, font=MainApp.FONT_ENTRIES, bd=2, fg=MainApp.FOREGROUND_LABEL_COLOR)
        self.delta_constraint_entry.insert(tk.END, str(self.qsystem.get_delta()))
        self.delta_constraint_entry.pack(pady=10)


    def submit_constraints_form(self):
        choice = self.selected_system_type.get()
        self.qsystem.set_delta(float(self.delta_constraint_entry.get()))
        if choice == 'timed':
            self.qsystem.set_time_constraint(int(self.time_constraint_entry.get()))
            self.generators_choice_widget()
        elif choice == 'requests':
            self.qsystem.set_requests_constaint(int(self.requests_constraint_entry.get()))
            self.generators_choice_widget()
        else:
            self.info_box("Input error", "Error")

    def setup_system_widget(self, event=None):
        self.clear_window()

        self.system_widget_header = tk.Label(self, text="SYSTEM SETUP", bg=MainApp.BACKGROUND_LABEL_COLOR, fg=MainApp.FOREGROUND_LABEL_COLOR,
                                             font=MainApp.FONT_ENTRIES)
        self.system_widget_header.pack(pady=30)

        self.system_widget_header = tk.Label(self, text="1. CHOOSE SYSTEM CONSTRAINTS",  bg=MainApp.BACKGROUND_LABEL_COLOR, fg=MainApp.FOREGROUND_LABEL_COLOR,
                         font=MainApp.FONT_REGULAR)
        self.system_widget_header.pack()

        options = ['timed', 'requests']
        self.system_type_choice = ttk.Combobox(self, values=options, textvariable=self.selected_system_type, width=20, background=MainApp.BACKGROUND_LABEL_COLOR, foreground=MainApp.FOREGROUND_LABEL_COLOR, font=('Times', 13, 'bold'))
        self.system_type_choice.pack(pady=10)
        self.system_type_choice.bind("<<ComboboxSelected>>", self.setup_system_widget)

        # Frame to hold the dynamic entry fields
        self.system_entry_frame = tk.Frame(self, bg=MainApp.BACKGROUND_LABEL_COLOR)
        self.system_entry_frame.pack(pady=20)

        self.display_system_constraints_entry(self.system_entry_frame)

        # Create 'Back' and 'Next' buttons
        self.back_button = tk.Button(self, text="BACK", command=self.start, foreground=MainApp.FOREGROUND_BUTTON_COLOR,
                       background=MainApp.BACKGROND_BUTTON_COLOR, relief='raised', font=MainApp.FONT_REGULAR)
        self.back_button.pack(side=tk.LEFT, padx=20, pady=20)

        self.submit_button = tk.Button(self, text="SUBMIT", command=self.submit_constraints_form, foreground=MainApp.FOREGROUND_BUTTON_COLOR,
                       background=MainApp.BACKGROND_BUTTON_COLOR, relief='raised', font=MainApp.FONT_REGULAR)
        self.submit_button.pack(side=tk.RIGHT, padx=20, pady=20)

    def save_information_source(self):
        self.qsystem.remove_information_source(self.selected_generator.get())
        distribution_name = self.selected_random_generator.get()
        self.gen_name = self.gen_entry_name.get()
        args = []
        flag = True
        if distribution_name == "normal":
            self.gen_a = self.gen_a_entry.get()
            self.gen_b = self.gen_b_entry.get()
            flag = self.check_parameters(self.check_float_parameters, self.gen_a, self.gen_b)
            if flag:
                args.append(float(self.gen_a))
                args.append(float(self.gen_b))
            else:
                self.info_box("Input has to be float", "WARNING")
                self.generators_choice_widget()
        elif distribution_name == "uniform":
            self.gen_a = self.gen_a_entry.get()
            self.gen_b = self.gen_b_entry.get()
            flag = self.check_parameters(self.check_int_parameters, self.gen_a, self.gen_b)
            if flag:
                args.append(int(self.gen_a))
                args.append(int(self.gen_b))
            else:
                # TODO: Make sure that args are not stored after invalid input!!!
                # args.append(self.gen_a)
                # args.append(self.gen_b)
                self.info_box("Input has to be integer", "WARNING")
                self.generators_choice_widget()
        elif distribution_name == "increment":
            self.gen_a = self.gen_a_entry.get()
            flag = self.check_parameters(self.check_float_parameters, self.gen_a)
            if flag:
                args.append(float(self.gen_a))
            else:
                self.info_box("Input has to be float", "WARNING")
                self.generators_choice_widget()
        function = Distributions.get_distribution(distribution_name)
        generator = RandomGenerator(function, args, distribution_name)
        self.qsystem.add_information_source(generator, self.gen_name)
        self.soft_reset_generator_values()

    def delete_information_source(self):
        self.qsystem.remove_information_source(self.selected_generator.get())
        self.soft_reset_generator_values()

    def add_information_source(self):
        distribution_name = self.selected_random_generator.get()
        self.gen_name = self.gen_entry_name.get()
        args = []
        if distribution_name == "normal":
            self.gen_a = self.gen_a_entry.get()
            self.gen_b = self.gen_b_entry.get()
            args.append(float(self.gen_a))
            args.append(float(self.gen_b))
        elif distribution_name == "uniform":
            self.gen_a = self.gen_a_entry.get()
            self.gen_b = self.gen_b_entry.get()
            args.append(int(self.gen_a))
            args.append(int(self.gen_b))
        elif distribution_name == "increment":
            self.gen_a = self.gen_a_entry.get()
            args.append(float(self.gen_a))
        function = Distributions.get_distribution(distribution_name)
        generator = RandomGenerator(function, args, distribution_name)
        self.qsystem.add_information_source(generator, self.gen_name)
        self.soft_reset_generator_values()

    def soft_reset_generator_values(self):
        self.gen_name = MainApp.DEFAULT_GEN_NAME
        self.selected_generator.set(MainApp.DEFAULT_SELECTED_GEN)
        self.gen_a = MainApp.DEFAULT_A_PARAM
        self.gen_b = MainApp.DEFAULT_B_PARAM
        self.gen_edit_mode = False
        self.generators_choice_widget()

    def display_generator_entry(self):
        if self.gen_edit_mode == True:
            generator_name = self.selected_generator.get()
            generators = self.qsystem.get_generators()
            for gen in generators:
                if gen.get_name() == generator_name:
                    rg = gen.get_random_generator()
                    distribution = rg.get_distribution()
                    if distribution == "normal" or distribution == "uniform":
                        self.gen_a = rg.get_distribution_args()[0]
                        self.gen_b = rg.get_distribution_args()[1]
                    elif distribution == "increment":
                        self.gen_a = rg.get_distribution_args()[0]
                    self.gen_name = generator_name
                    break
        rg_choice = self.selected_random_generator.get()

        second_frame = tk.Frame(self, bg=MainApp.BACKGROUND_LABEL_COLOR)
        second_frame.pack(pady=10)


        self.gen_entry_name_label = tk.Label(second_frame, text = "Enter information source name: ",  bg=MainApp.BACKGROUND_LABEL_COLOR, fg=MainApp.FOREGROUND_LABEL_COLOR,
                         font=MainApp.FONT_ENTRIES)
        self.gen_entry_name_label.grid(row=0, column=0)

        self.gen_entry_name = tk.Entry(second_frame, relief="sunken", width=20, font=MainApp.FONT_ENTRIES, bd=2, fg=MainApp.FOREGROUND_LABEL_COLOR)
        self.gen_entry_name.insert(tk.END, self.gen_name)
        self.gen_entry_name.grid(row=0, column=1)

        third_frame = tk.Frame(self, bg=MainApp.BACKGROUND_LABEL_COLOR)
        third_frame.pack(pady=10)


        distribution_label = tk.Label(third_frame, text = "Choose distribution:",  bg=MainApp.BACKGROUND_LABEL_COLOR, fg=MainApp.FOREGROUND_LABEL_COLOR,
                         font=MainApp.FONT_ENTRIES)
        distribution_label.grid(row=0, column=0, padx=10)

        options = ['normal', 'uniform', 'increment']
        self.distribution_cbox = ttk.Combobox(third_frame, values=options, textvariable=self.selected_random_generator, width=28, background=MainApp.BACKGROUND_LABEL_COLOR, foreground=MainApp.FOREGROUND_LABEL_COLOR, font=MainApp.FONT_ENTRIES)
        self.distribution_cbox.bind("<<ComboboxSelected>>", self.generators_choice_widget)
        self.distribution_cbox.grid(row=0, column=1)

        fourth_frame = tk.Frame(self, bg=MainApp.BACKGROUND_LABEL_COLOR)
        fourth_frame.pack(pady=10)

        if rg_choice == 'normal':
            self.mu_label = tk.Label(fourth_frame, text="\u03bc",  bg=MainApp.BACKGROUND_LABEL_COLOR, fg=MainApp.FOREGROUND_LABEL_COLOR,
                         font=MainApp.FONT_ENTRIES) # mu, mean
            self.mu_label.grid(row=0, column =0, padx=5)

            self.gen_a_entry = tk.Entry(fourth_frame, relief="sunken", width=15, font=MainApp.FONT_ENTRIES, bd=2, fg=MainApp.FOREGROUND_LABEL_COLOR)
            self.gen_a_entry.insert(tk.END, str(self.gen_a))
            self.gen_a_entry.grid(row=0, column=1, padx=5)

            self.sigma_label = tk.Label(fourth_frame, text="\u03C3",  bg=MainApp.BACKGROUND_LABEL_COLOR, fg=MainApp.FOREGROUND_LABEL_COLOR,
                         font=MainApp.FONT_ENTRIES) # sigma, standard deviation
            self.sigma_label.grid(row = 0, column = 2, padx=5)

            self.gen_b_entry = tk.Entry(fourth_frame, relief="sunken", width=15, font=MainApp.FONT_ENTRIES, bd=2, fg=MainApp.FOREGROUND_LABEL_COLOR)
            self.gen_b_entry.insert(tk.END, str(self.gen_b))
            self.gen_b_entry.grid(row = 0, column = 3)

        elif rg_choice == 'uniform':
            self.a_label = tk.Label(fourth_frame, text="a",  bg=MainApp.BACKGROUND_LABEL_COLOR, fg=MainApp.FOREGROUND_LABEL_COLOR,
                         font=MainApp.FONT_ENTRIES) # a
            self.a_label.grid(row = 0, column = 0, padx=10)
            self.gen_a_entry = tk.Entry(fourth_frame, relief="sunken", width=15, font=MainApp.FONT_ENTRIES, bd=2, fg=MainApp.FOREGROUND_LABEL_COLOR)
            self.gen_a_entry.insert(tk.END, str(self.gen_a))
            self.gen_a_entry.grid(row = 0, column = 1, padx=5)

            self.b_label = tk.Label(fourth_frame, text="b",  bg=MainApp.BACKGROUND_LABEL_COLOR, fg=MainApp.FOREGROUND_LABEL_COLOR,
                         font=MainApp.FONT_ENTRIES) # b
            self.b_label.grid(row= 0, column = 2, padx=10)

            self.gen_b_entry = tk.Entry(fourth_frame, relief="sunken", width=15, font=MainApp.FONT_ENTRIES, bd=2, fg=MainApp.FOREGROUND_LABEL_COLOR)
            self.gen_b_entry.insert(tk.END, str(self.gen_b))
            self.gen_b_entry.grid(row = 0, column = 3,)

        elif rg_choice == 'increment':
            self.a_label = tk.Label(fourth_frame, text="value", bg=MainApp.BACKGROUND_LABEL_COLOR, fg=MainApp.FOREGROUND_LABEL_COLOR,
                         font=MainApp.FONT_ENTRIES) # increment
            self.a_label.grid(row = 0, column = 0, padx=10)

            self.gen_a_entry = tk.Entry(fourth_frame, relief="sunken", width=15, font=MainApp.FONT_ENTRIES, bd=2, fg=MainApp.FOREGROUND_LABEL_COLOR)
            self.gen_a_entry.insert(tk.END, str(self.gen_a))
            self.gen_a_entry.grid(row = 0, column = 1)

        fifth_frame = tk.Frame(self, bg=MainApp.BACKGROUND_LABEL_COLOR)
        fifth_frame.pack(pady=10)
        if self.gen_edit_mode:

            self.save_button = tk.Button(fifth_frame, text = "SAVE", command = self.save_information_source, foreground=MainApp.FOREGROUND_BUTTON_COLOR,
                       background=MainApp.BACKGROND_BUTTON_COLOR, relief='raised', font=MainApp.FONT_REGULAR)
            self.save_button.grid(row = 0, column = 0, padx=10, pady=10)
        else:
            self.gen_add_button = tk.Button(fifth_frame, text="ADD", command=self.add_information_source, foreground=MainApp.FOREGROUND_BUTTON_COLOR,
                       background=MainApp.BACKGROND_BUTTON_COLOR, relief='raised', font=MainApp.FONT_REGULAR)
            self.gen_add_button.grid(row = 0, column = 1, padx=10, pady=10)


    def choose_generator(self, event):
        if self.generator_choice.get() != '':
            self.gen_edit_mode = True
        self.generators_choice_widget()

    def generators_choice_widget(self, event = None):
        self.clear_window()

        gen_title_label = tk.Label(self, text="GENERATE GENERATORS AND GENERATOR'S SETTINGS", bg=MainApp.BACKGROUND_LABEL_COLOR, fg=MainApp.FOREGROUND_LABEL_COLOR,
                             font=MainApp.FONT_ENTRIES)
        gen_title_label.pack(pady=30)


        first_frame = tk.Frame(self, bg=MainApp.BACKGROUND_LABEL_COLOR)
        first_frame.pack(pady=20)


        gen_label = tk.Label(first_frame, text="Choose information sources", bg=MainApp.BACKGROUND_LABEL_COLOR, fg=MainApp.FOREGROUND_LABEL_COLOR,
                             font=MainApp.FONT_ENTRIES)
        gen_label.grid(row=0, column=0)

        #Create a generator combobox
        generators = self.qsystem.get_generators()
        options = [x.get_name() for x in generators]
        self.generator_choice = ttk.Combobox(first_frame, values=options, textvariable=self.selected_generator, width=28, background=MainApp.BACKGROUND_LABEL_COLOR, foreground=MainApp.FOREGROUND_LABEL_COLOR, font=MainApp.FONT_ENTRIES)
        self.generator_choice.grid(row=0, column=1, padx=10, pady=10)
        self.generator_choice.bind("<<ComboboxSelected>>", self.choose_generator)

        # Create a Delete button
        self.gen_delete_button = tk.Button(first_frame, text="DELETE", command=self.delete_information_source,
                                           foreground=MainApp.FOREGROUND_BUTTON_COLOR,
                                           background=MainApp.BACKGROND_BUTTON_COLOR, relief='raised', font=MainApp.FONT_REGULAR)
        self.gen_delete_button.grid(row=1, column=0, padx=10, pady=10)

        # Create form reset button
        self.gen_new_button = tk.Button(first_frame, text="CLEAR", command=self.soft_reset_generator_values,
                                        foreground=MainApp.FOREGROUND_BUTTON_COLOR,
                                        background=MainApp.BACKGROND_BUTTON_COLOR, relief='raised', font=MainApp.FONT_REGULAR)
        self.gen_new_button.grid(row=1, column=1, padx=10, pady=10)


        self.display_generator_entry()

        button_frame = tk.Frame(self, bg=MainApp.BACKGROUND_LABEL_COLOR)
        button_frame.pack(pady=10)

        # Create 'Back' and 'Next' buttons
        self.back_button = tk.Button(button_frame, text="BACK", command=self.setup_system_widget, foreground=MainApp.FOREGROUND_BUTTON_COLOR,
                                     background=MainApp.BACKGROND_BUTTON_COLOR, relief='raised', font=MainApp.FONT_REGULAR)
        self.back_button.grid(row=0, column=0, padx=20, pady=20)

        self.submit_button = tk.Button(button_frame, text="SUBMIT", command=self.processors_choice_widget, foreground=MainApp.FOREGROUND_BUTTON_COLOR,
                                       background=MainApp.BACKGROND_BUTTON_COLOR, relief='raised', font=MainApp.FONT_REGULAR)
        self.submit_button.grid(row=0, column=1, padx=20, pady=20)


    def save_processing_unit(self):
        self.qsystem.remove_processing_unit(self.selected_processor.get())
        distribution_name = self.selected_random_generator.get()
        self.proc_name = self.proc_entry_name.get()
        args = []
        flag = True
        if distribution_name == "normal":
            self.proc_a = self.proc_a_entry.get()
            self.proc_b = self.proc_b_entry.get()
            flag = self.check_parameters(self.check_float_parameters, self.proc_a, self.proc_b)
            if flag:
                args.append(float(self.proc_a))
                args.append(float(self.proc_b))
            else:
                self.info_box("Input has to be float", "WARNING")
                self.processors_choice_widget()
        elif distribution_name == "uniform":
            self.proc_a = self.proc_a_entry.get()
            self.proc_b = self.proc_b_entry.get()
            flag = self.check_parameters(self.check_int_parameters, self.proc_a, self.proc_b)
            if flag:
                args.append(int(self.proc_a))
                args.append(int(self.proc_b))
            else:
                self.info_box("Input has to be int", "WARNING")
                self.processors_choice_widget()
        elif distribution_name == "increment":
            self.proc_a = self.proc_a_entry.get()
            flag = self.check_parameters(self.check_float_parameters, self.proc_a)
            if flag:
                args.append(float(self.proc_a))
            else:
                self.info_box("Input has to be float", "WARNING")
                self.processors_choice_widget()
        function = Distributions.get_distribution(distribution_name)
        generator = RandomGenerator(function, args, distribution_name)
        self.qsystem.add_processing_unit(generator, self.proc_name)
        self.soft_reset_processor_values()

    def delete_processing_unit(self):
        self.qsystem.remove_processing_unit(self.selected_processor.get())
        self.soft_reset_processor_values()

    def add_processing_unit(self):
        distribution_name = self.selected_random_generator.get()
        self.proc_name = self.proc_entry_name.get()
        args = []
        if distribution_name == "normal":
            self.proc_a = self.proc_a_entry.get()
            self.proc_b = self.proc_b_entry.get()
            args.append(float(self.proc_a))
            args.append(float(self.proc_b))
        elif distribution_name == "uniform":
            self.proc_a = self.proc_a_entry.get()
            self.proc_b = self.proc_b_entry.get()
            args.append(int(self.proc_a))
            args.append(int(self.proc_b))
        elif distribution_name == "increment":
            self.proc_a = self.proc_a_entry.get()
            args.append(float(self.proc_a))
        function = Distributions.get_distribution(distribution_name)
        generator = RandomGenerator(function, args, distribution_name)
        self.qsystem.add_processing_unit(generator, self.proc_name)
        self.soft_reset_processor_values()

    def soft_reset_processor_values(self):
        self.proc_name = MainApp.DEFAULT_PROC_NAME
        self.selected_processor.set(MainApp.DEFAULT_SELECTED_PROC)
        self.proc_a = MainApp.DEFAULT_A_PARAM
        self.proc_b = MainApp.DEFAULT_B_PARAM
        self.proc_edit_mode = False
        self.processors_choice_widget()

    def display_processor_entry(self):
        if self.proc_edit_mode == True:
            processor_name = self.selected_processor.get()
            processors = self.qsystem.get_processors()
            for proc in processors:
                if proc.get_name() == processor_name:
                    rg = proc.get_random_generator()
                    distribution = rg.get_distribution()
                    if distribution == "normal" or distribution == "uniform":
                        self.proc_a = rg.get_distribution_args()[0]
                        self.proc_b = rg.get_distribution_args()[1]
                    elif distribution == "increment":
                        self.proc_a = rg.get_distribution_args()[0]
                    self.proc_name = processor_name
                    break

        second_frame = tk.Frame(self, bg=MainApp.BACKGROUND_LABEL_COLOR)
        second_frame.pack(pady=10)

        rg_choice = self.selected_random_generator.get()
        self.proc_entry_name_label = tk.Label(second_frame, text = "Enter processor unit name: ",  bg=MainApp.BACKGROUND_LABEL_COLOR, fg=MainApp.FOREGROUND_LABEL_COLOR,
                         font=MainApp.FONT_ENTRIES)
        self.proc_entry_name_label.grid(row=0, column=0)

        self.proc_entry_name = tk.Entry(second_frame, relief="sunken", width=20, font=MainApp.FONT_ENTRIES,
                                                   bd=2, fg=MainApp.FOREGROUND_LABEL_COLOR)
        self.proc_entry_name.insert(tk.END, self.proc_name)
        self.proc_entry_name.grid(row=0, column=1)

        third_frame = tk.Frame(self, bg=MainApp.BACKGROUND_LABEL_COLOR)
        third_frame.pack(pady=10)


        distribution_label = tk.Label(third_frame, text = "Choose distribution:",  bg=MainApp.BACKGROUND_LABEL_COLOR, fg=MainApp.FOREGROUND_LABEL_COLOR,
                         font=MainApp.FONT_ENTRIES)
        distribution_label.grid(row=0, column=0, padx=10)

        options = ['normal', 'uniform', 'increment']
        self.distribution_cbox = ttk.Combobox(third_frame, values=options, textvariable=self.selected_random_generator,  width=28,
                                                          background=MainApp.BACKGROUND_LABEL_COLOR, foreground=MainApp.FOREGROUND_LABEL_COLOR,
                                                          font=MainApp.FONT_ENTRIES)
        self.distribution_cbox.bind("<<ComboboxSelected>>", self.processors_choice_widget)
        self.distribution_cbox.grid(row=0, column=1)

        fourth_frame = tk.Frame(self, bg=MainApp.BACKGROUND_LABEL_COLOR)
        fourth_frame.pack(pady=10)


        if rg_choice == 'normal':
            self.mu_label = tk.Label(fourth_frame, text="\u03bc",  bg=MainApp.BACKGROUND_LABEL_COLOR, fg=MainApp.FOREGROUND_LABEL_COLOR,
                         font=MainApp.FONT_ENTRIES) # mu, mean
            self.mu_label.grid(row=0, column =0, padx=5)

            self.proc_a_entry = tk.Entry(fourth_frame, relief="sunken", width=20, font=MainApp.FONT_ENTRIES,
                                                   bd=2, fg=MainApp.FOREGROUND_LABEL_COLOR)
            self.proc_a_entry.insert(tk.END, str(self.proc_a))
            self.proc_a_entry.grid(row = 0, column = 1)

            self.sigma_label = tk.Label(fourth_frame, text="\u03C3",  bg=MainApp.BACKGROUND_LABEL_COLOR, fg=MainApp.FOREGROUND_LABEL_COLOR,
                         font=MainApp.FONT_ENTRIES) # sigma, standard deviation
            self.sigma_label.grid(row=0, column=2, padx=5)

            self.proc_b_entry = tk.Entry(fourth_frame, relief="sunken", width=20, font=MainApp.FONT_ENTRIES,
                                                   bd=2, fg=MainApp.FOREGROUND_LABEL_COLOR)
            self.proc_b_entry.insert(tk.END, str(self.proc_b))
            self.proc_b_entry.grid(row=0, column=3)

        elif rg_choice == 'uniform':
            self.a_label = tk.Label(fourth_frame, text="a",  bg=MainApp.BACKGROUND_LABEL_COLOR, fg=MainApp.FOREGROUND_LABEL_COLOR,
                         font=MainApp.FONT_ENTRIES) # a
            self.a_label.grid(row = 0, column = 0, padx=10)
            self.proc_a_entry = tk.Entry(fourth_frame, relief="sunken", width=20, font=MainApp.FONT_ENTRIES,
                                                   bd=2, fg=MainApp.FOREGROUND_LABEL_COLOR)
            self.proc_a_entry.insert(tk.END, str(self.proc_a))
            self.proc_a_entry.grid(row = 0, column = 1, padx=40)
            self.b_label = tk.Label(fourth_frame, text="b",  bg=MainApp.BACKGROUND_LABEL_COLOR, fg=MainApp.FOREGROUND_LABEL_COLOR,
                         font=MainApp.FONT_ENTRIES) # b
            self.b_label.grid(row = 0, column = 2, padx=10)
            self.proc_b_entry = tk.Entry(fourth_frame, relief="sunken", width=20, font=MainApp.FONT_ENTRIES,
                                                   bd=2, fg=MainApp.FOREGROUND_LABEL_COLOR)
            self.proc_b_entry.insert(tk.END, str(self.proc_b))
            self.proc_b_entry.grid(row = 0, column = 3)

        elif rg_choice == 'increment':
            self.a_label = tk.Label(fourth_frame, text="value",  bg=MainApp.BACKGROUND_LABEL_COLOR, fg=MainApp.FOREGROUND_LABEL_COLOR,
                         font=MainApp.FONT_ENTRIES) # increment
            self.a_label.grid(row = 0, column = 0, padx=10)

            self.proc_a_entry = tk.Entry(fourth_frame, relief="sunken", width=20, font=MainApp.FONT_ENTRIES,
                                                   bd=2, fg=MainApp.FOREGROUND_LABEL_COLOR)
            self.proc_a_entry.insert(tk.END, str(self.proc_a))
            self.proc_a_entry.grid(row = 0, column = 1)

        fifth_frame = tk.Frame(self, bg=MainApp.BACKGROUND_LABEL_COLOR)
        fifth_frame.pack(pady=10)

        if self.proc_edit_mode:
            self.save_button = tk.Button(fifth_frame, text = "SAVE", command = self.save_processing_unit, foreground=MainApp.FOREGROUND_BUTTON_COLOR,
                       background=MainApp.BACKGROND_BUTTON_COLOR, relief='raised', font=MainApp.FONT_REGULAR)
            self.save_button.grid(row=0, column=0, padx=10, pady=10)
        else:
            self.proc_add_button = tk.Button(fifth_frame, text="ADD", command=self.add_processing_unit, foreground=MainApp.FOREGROUND_BUTTON_COLOR,
                       background=MainApp.BACKGROND_BUTTON_COLOR, relief='raised', font=MainApp.FONT_REGULAR)
            self.proc_add_button.grid(row=0, column=1, padx=10, pady=10)



    def choose_processor(self, event):
        if self.processor_choice.get() != '':
            self.proc_edit_mode = True
        self.processors_choice_widget()

    def processors_choice_widget(self, event = None):
        self.clear_window()

        proc_title_label = tk.Label(self, text="GENERATE PROCESSORS AND PROCESSOR'S SETTINGS", bg=MainApp.BACKGROUND_LABEL_COLOR,
                                   fg=MainApp.FOREGROUND_LABEL_COLOR,
                                   font=MainApp.FONT_ENTRIES)
        proc_title_label.pack(pady=30)

        first_frame = tk.Frame(self, bg=MainApp.BACKGROUND_LABEL_COLOR)
        first_frame.pack(pady=20)

        proc_label = tk.Label(first_frame, text="Choose processing units", bg=MainApp.BACKGROUND_LABEL_COLOR, fg=MainApp.FOREGROUND_LABEL_COLOR,
                              font=MainApp.FONT_ENTRIES)
        proc_label.grid(row=0, column=0)


        processors = self.qsystem.get_processors()
        options = [x.get_name() for x in processors]
        self.processor_choice = ttk.Combobox(first_frame, values=options, textvariable=self.selected_processor,  width=28, background=MainApp.BACKGROUND_LABEL_COLOR, foreground=MainApp.FOREGROUND_LABEL_COLOR,
                                             font=MainApp.FONT_ENTRIES)
        self.processor_choice.grid(row=0, column=1, padx=10, pady=10)
        self.processor_choice.bind("<<ComboboxSelected>>", self.choose_processor)

        # Create a Delete button
        self.proc_delete_button = tk.Button(first_frame, text="DELETE", command = self.delete_processing_unit, foreground=MainApp.FOREGROUND_BUTTON_COLOR,
                       background=MainApp.BACKGROND_BUTTON_COLOR, relief='raised', font=MainApp.FONT_REGULAR)
        self.proc_delete_button.grid(row=1, column=0, padx=10, pady=10)

        # Create form reset button
        self.proc_new_button = tk.Button(first_frame, text="CLEAR", command = self.soft_reset_processor_values, foreground=MainApp.FOREGROUND_BUTTON_COLOR,
                       background=MainApp.BACKGROND_BUTTON_COLOR, relief='raised', font=MainApp.FONT_REGULAR)
        self.proc_new_button.grid(row=1, column=1, padx=10, pady=10)


        self.display_processor_entry()


        button_frame = tk.Frame(self, bg=MainApp.BACKGROUND_LABEL_COLOR)
        button_frame.pack(pady=10)


        # Create 'Back' and 'Next' buttons
        self.back_button = tk.Button(button_frame, text="BACK", command=self.generators_choice_widget, foreground=MainApp.FOREGROUND_BUTTON_COLOR,
                       background=MainApp.BACKGROND_BUTTON_COLOR, relief='raised', font=MainApp.FONT_REGULAR)
        self.back_button.grid(row=0, column=0, padx=20, pady=20)

        self.submit_button = tk.Button(button_frame, text="SUBMIT", command = lambda: self.create_simulation_widget(isMetamodel=False), foreground=MainApp.FOREGROUND_BUTTON_COLOR,
                       background=MainApp.BACKGROND_BUTTON_COLOR, relief='raised', font=MainApp.FONT_REGULAR)
        self.submit_button.grid(row=0, column=1, padx=20, pady=20)

    def simulate(self):
        self.requests = self.qsystem.simulate()
        self.qsystem.log_requests(self.requests)
        self.create_results_widget()

    def create_table(self, table_frame, *args):
        tree = ttk.Treeview(table_frame, columns=(args), show='headings')
        for arg in args:
            tree.heading(arg, text=arg)

        #Add the table to the frame with a vertical scrollbar
        vsb = ttk.Scrollbar(table_frame, orient="vertical", command=tree.yview)
        tree.configure(yscrollcommand=vsb.set)
        vsb.pack(side='right', fill='y')
        tree.pack(fill=tk.BOTH, expand=True)
        return tree

    def populate_modules_table(self, table):
        generators = self.qsystem.get_generators()
        processors = self.qsystem.get_processors()
        for gen in generators:
            rg = gen.get_random_generator()
            table.insert('', tk.END, values=(gen.get_name(), "Generator", rg.get_distribution(), rg.get_distribution_args()))

        for proc in processors:
            rg = proc.get_random_generator()
            table.insert('', tk.END, values=(proc.get_name(), "Processor", rg.get_distribution(), rg.get_distribution_args()))

    def create_simulation_widget(self, isMetamodel=True):
        self.clear_window()
        if (isMetamodel and self.model_file_path and self.metamodel_file_path and self.model_file_path != '' and self.metamodel_file_path != ''):
            self.model = self.qmodel.import_textx_model(self.metamodel_file_path, self.model_file_path)
            self.qsystem.interpret(self.model)

            self.file_path_label = tk.Label(self, text=f"Using textx model: {self.model_file_path}", bg=MainApp.BACKGROUND_LABEL_COLOR, fg=MainApp.FOREGROUND_LABEL_COLOR,
                         font=MainApp.FONT_LABEL)
            self.file_path_label.pack(fill=tk.BOTH, pady=10)

            table_frame = tk.Frame(self, height=50)
            table_frame.pack(expand=True, padx=20)

            self.tree = self.create_table(table_frame, "name", "type", "distribution", "distribution args")

            self.populate_modules_table(self.tree)

            # Create 'Back' and 'Next' buttons
            self.back_button = tk.Button(self, text="BACK", command=self.start, foreground=MainApp.FOREGROUND_BUTTON_COLOR,
                       background=MainApp.BACKGROND_BUTTON_COLOR, relief='raised', font=MainApp.FONT_REGULAR)
            self.back_button.pack(side=tk.LEFT, padx=20, pady=20)

            self.next_button = tk.Button(self, text="SIMULATE", command=self.simulate, foreground=MainApp.FOREGROUND_BUTTON_COLOR,
                       background=MainApp.BACKGROND_BUTTON_COLOR, relief='raised', font=MainApp.FONT_REGULAR)
            self.next_button.pack(side=tk.RIGHT, padx=20, pady=20)
        else:
            table_frame = tk.Frame(self, height=300)
            table_frame.pack( expand=True, padx=20)

            self.tree = self.create_table(table_frame, "name", "type", "distribution", "distribution args")
            self.populate_modules_table(self.tree)

            # Create 'Back' and 'Next' buttons
            self.back_button = tk.Button(self, text="BACK", command = self.processors_choice_widget, foreground=MainApp.FOREGROUND_BUTTON_COLOR,
                       background=MainApp.BACKGROND_BUTTON_COLOR, relief='raised', font=MainApp.FONT_REGULAR)
            self.back_button.pack(side=tk.LEFT, padx=20, pady=20)

            self.next_button = tk.Button(self, text="SIMULATE", command=self.simulate, foreground=MainApp.FOREGROUND_BUTTON_COLOR,
                       background=MainApp.BACKGROND_BUTTON_COLOR, relief='raised', font=MainApp.FONT_REGULAR)
            self.next_button.pack(side=tk.RIGHT, padx=20, pady=20)

    def create_results_widget(self):
        self.clear_window()

        table_frame = tk.Frame(self, height=50)
        table_frame.pack(expand=True, padx=20)

        self.tree = self.create_table(table_frame, "name", "gen_time", "proc_time")
        self.populate_results_table(self.tree)
        # Create 'Back' and 'Next' buttons
        self.back_button = tk.Button(self, text="BACK", command=self.create_simulation_widget, foreground=MainApp.FOREGROUND_BUTTON_COLOR,
                                     background=MainApp.BACKGROND_BUTTON_COLOR, relief='raised', font=MainApp.FONT_REGULAR)
        self.back_button.pack(side=tk.LEFT, padx=20, pady=20)
        self.next_button = tk.Button(self, text="MAIN MENU", command=self.start, foreground=MainApp.FOREGROUND_BUTTON_COLOR,
                                     background=MainApp.BACKGROND_BUTTON_COLOR, relief='raised', font=MainApp.FONT_REGULAR)
        self.next_button.pack(side=tk.RIGHT, padx=20, pady=20)

    def populate_results_table(self,table):
        for r in self.requests:
            proc_time = str(round(r.get_finish_processing_time() - r.get_start_processing_time(), 5))
            gen_time_rounded = str(round(r.get_generation_time(),5))
            table.insert('', tk.END,
                         values=(r.get_name(),gen_time_rounded , proc_time))

    def load_model(self):
        self.frame_for_selected_files = tk.Frame(self, width=800, height=500, bg=MainApp.BACKGROUND_LABEL_COLOR)
        self.frame_for_selected_files.pack(pady=10)

        model_path = filedialog.askopenfilename(
            initialdir=os.path.dirname(__file__),
            title="Select .qs File",
            filetypes=[("QS Files", "*.qs")],
            defaultextension=".qs"
        )
        if model_path and model_path != '':
            self.model_file_path = model_path

            if self.model_file_path:
                self.chosen_file_label = tk.Label(self.frame_for_selected_files, text="Chosen files:", bg=MainApp.BACKGROUND_LABEL_COLOR,
                                                  fg=MainApp.FOREGROUND_LABEL_COLOR,
                                                  font=MainApp.FONT_REGULAR)
                self.chosen_file_label.pack(fill=tk.BOTH, pady=10)

                self.file_path_label = tk.Label(self.frame_for_selected_files, text=f"Selected model file: {self.model_file_path}", bg=MainApp.BACKGROUND_LABEL_COLOR,
                                                  fg=MainApp.FOREGROUND_LABEL_COLOR,
                                                  font=MainApp.FONT_LABEL)
                self.file_path_label.pack(pady=5)


            metamodel_path = filedialog.askopenfilename(
                initialdir=os.path.dirname(__file__),
                title="Select .tx File",
                filetypes=[("TextX Files", "*.tx")],
                defaultextension=".tx"
            )
            if metamodel_path and metamodel_path != '':
                self.metamodel_file_path = metamodel_path

                if self.metamodel_file_path:
                    self.metamodel_path_label = tk.Label(self.frame_for_selected_files,
                                                         text=f"Selected metamodel file: {self.metamodel_file_path}", bg=MainApp.BACKGROUND_LABEL_COLOR,
                                                  fg=MainApp.FOREGROUND_LABEL_COLOR,
                                                  font=MainApp.FONT_LABEL)
                    self.metamodel_path_label.pack(pady=5)
                    self.update()
                    self.after(2000, self.create_simulation_widget())
            else:
                self.start()
        else:
            self.start()


    def handle_file_path(self, file_path):
        # Handle the file path as needed
        print(f"File path selected: {file_path}")

    def info_box(self, text, title="Info"):
        # Implement the action for the 'Next' button
        messagebox.showinfo(title, text)

if __name__ == "__main__":
    app = MainApp()
    app.mainloop()