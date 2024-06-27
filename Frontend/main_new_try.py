import tkinter as tk
from tkinter import ttk
import os
from tkinter import filedialog, messagebox
from qsystem import QSystem
from qmodel import QModel
from distribution import Distributions, RandomGenerator

class MainApp(tk.Tk):
    DEFAULT_GEN_NAME = "G"
    DEFAULT_PROC_NAME = "P"
    DEFAULT_A_PARAM = 1
    DEFAULT_B_PARAM = 2
    DEFAULT_SELECTED_RG = "normal"
    DEFAULT_SELECTED_ST = "timed"
    DEFAULT_SELECTED_GEN = ""
    DEFAULT_SELECTED_PROC = ""

    def __init__(self):
        self.qsystem = QSystem()
        self.qmodel = QModel()
        self.model_file_path = None
        self.metamodel_file_path = None

        this_folder = os.path.dirname(__file__)
        self.model_file_path = os.path.join(this_folder, 'program.qs')
        self.metamodel_file_path = os.path.join(this_folder, 'qsystem.tx')

        super().__init__()
        self.title("Main Window")
        self.geometry("800x600")
        self.selected_system_type = tk.StringVar()
        self.selected_generator = tk.StringVar()
        self.selected_system_type.set(MainApp.DEFAULT_SELECTED_ST)
        self.selected_random_generator = tk.StringVar()
        self.selected_random_generator.set(MainApp.DEFAULT_SELECTED_RG)

        self.gen_a = MainApp.DEFAULT_A_PARAM
        self.gen_b = MainApp.DEFAULT_B_PARAM
        self.proc_a = MainApp.DEFAULT_A_PARAM
        self.proc_b = MainApp.DEFAULT_B_PARAM
        self.gen_name = MainApp.DEFAULT_GEN_NAME
        self.proc_name = MainApp.DEFAULT_PROC_NAME
        self.gen_edit_mode = False
        self.start()

    def clear_window(self):
        for widget in self.winfo_children():
            widget.destroy()

    def start(self):
        self.clear_window()

        self.return_button = tk.Button(self, text="Input model parameters", command=self.setup_system_widget)
        self.return_button.pack(pady=20)
        
        self.open_file_button = tk.Button(self, text="Load textX model", command=self.load_model)
        self.open_file_button.pack(pady=20)

        self.use_cached_model_button = tk.Button(self, text="Use saved textX model", command=self.create_simulation_widget)
        self.use_cached_model_button.pack(pady=20)

        if self.model_file_path:
            self.file_path_label = tk.Label(self, text=f"Selected file: {self.model_file_path}")
            self.file_path_label.pack(pady=10)
        if self.metamodel_file_path:
            self.metamodel_path_label = tk.Label(self, text=f"Selected file: {self.metamodel_file_path}")
            self.metamodel_path_label.pack(pady=10)

    def display_system_constraints_entry(self, frame):
        choice = self.selected_system_type.get()
        if choice == 'timed':
            self.time_constraint_entry = tk.Entry(frame)
            self.time_constraint_entry.insert(tk.END, str(self.qsystem.get_time_constraint()))
            self.time_constraint_entry.pack(pady=5)
            self.time_constraint_entry_label = tk.Label(frame, text="System time constraint")
            self.time_constraint_entry_label.pack()
        elif choice == 'requests':
            self.requests_constraint_entry = tk.Entry(frame)
            self.requests_constraint_entry.insert(tk.END, str(self.qsystem.get_requests_constraint()))
            self.requests_constraint_entry.pack(pady=5)
            self.requests_constraint_entry_label = tk.Label(frame, text="System requests number constraint")
            self.requests_constraint_entry_label.pack()
        else:
            self.time_constraint_entry = tk.Entry(frame)
            self.time_constraint_entry.pack(pady=5)
            self.time_constraint_entry_label = tk.Label(frame, text="System time constraint")
            self.time_constraint_entry_label.pack()
        self.delta_constraint_entry = tk.Entry(frame)
        self.delta_constraint_entry.insert(tk.END, str(self.qsystem.get_delta()))
        self.delta_constraint_entry.pack(pady=5)
        self.delta_constraint_label = tk.Label(frame, text="System time delta constraint")
        self.delta_constraint_label.pack()

    def submit_constraints_form(self):
        choice = self.selected_system_type.get()
        self.qsystem.set_delta(self.delta_constraint_entry.get())
        if choice == 'timed':
            self.qsystem.set_time_constraint(self.time_constraint_entry.get())
            self.generators_choice_widget()
        elif choice == 'requests':
            self.qsystem.set_requests_constaint(self.requests_constraint_entry.get())
            self.generators_choice_widget()
        else:
            self.info_box("Input error", "Error")

    def setup_system_widget(self, event=None):
        self.clear_window()

        self.system_widget_header = tk.Label(self, text="Choose system constraints")
        self.system_widget_header.pack()

        options = ['timed', 'requests']
        self.system_type_choice = ttk.Combobox(self, values=options, textvariable=self.selected_system_type)
        self.system_type_choice.pack(pady=20)
        self.system_type_choice.bind("<<ComboboxSelected>>", self.setup_system_widget)

        # Frame to hold the dynamic entry fields
        self.system_entry_frame = tk.Frame(self)
        self.system_entry_frame.pack(pady=20)

        self.display_system_constraints_entry(self.system_entry_frame)
        
        # Create 'Back' and 'Next' buttons
        self.back_button = tk.Button(self, text="Back", command=self.start)
        self.back_button.pack(side=tk.LEFT, padx=20, pady=20)
        
        self.submit_button = tk.Button(self, text="Submit", command=self.submit_constraints_form)
        self.submit_button.pack(side=tk.RIGHT, padx=20, pady=20)

    def save_information_source(self, callback):
        self.qsystem.remove_information_source(self.selected_generator.get())
        distribution_name = self.selected_random_generator.get()
        self.gen_name = self.gen_entry_name.get()
        args = []
        if distribution_name == "normal":
            self.gen_a = self.gen_a_entry.get()
            self.gen_b = self.gen_b_entry.get()
            args.append(self.gen_a)
            args.append(self.gen_b)
        elif distribution_name == "uniform":
            self.gen_a = self.gen_a_entry.get()
            self.gen_b = self.gen_b_entry.get()
            args.append(self.gen_a)
            args.append(self.gen_b)
        elif distribution_name == "increment":
            self.gen_a = self.gen_a_entry.get()
            args.append(self.gen_a)
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
            args.append(self.gen_a)
            args.append(self.gen_b)
        elif distribution_name == "uniform":
            self.gen_a = self.gen_a_entry.get()
            self.gen_b = self.gen_b_entry.get()
            args.append(self.gen_a)
            args.append(self.gen_b)
        elif distribution_name == "increment":
            self.gen_a = self.gen_a_entry.get()
            args.append(self.gen_a)
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

    def display_generator_entry(self, row = 0, col = 0):
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
                    self.selected_random_generator.set(distribution)
                    self.gen_name = generator_name
                    break        
        rg_choice = self.selected_random_generator.get()
        self.gen_entry_name_label = tk.Label(self, text = "Enter information source name: ")
        self.gen_entry_name_label.grid(row = row, column = col)
        col += 1
        self.gen_entry_name = tk.Entry(self)
        self.gen_entry_name.insert(tk.END, self.gen_name)
        self.gen_entry_name.grid(row = row, column = col)
        row += 1
        col = 0
        distribution_label = tk.Label(self, text = "Choose distribution:")
        distribution_label.grid(row = row, column = col)
        col += 1
        options = ['normal', 'uniform', 'increment']
        self.distribution_cbox = ttk.Combobox(self, values=options, textvariable=self.selected_random_generator)
        self.distribution_cbox.bind("<<ComboboxSelected>>", self.generators_choice_widget)
        self.distribution_cbox.grid(row = row, column = col)
        col = 0
        row += 1
        if rg_choice == 'normal':
            self.mu_label = tk.Label(self, text="\u03bc") # mu, mean
            self.mu_label.grid(row = row, column = col)
            col += 1
            self.gen_a_entry = tk.Entry(self)
            self.gen_a_entry.insert(tk.END, str(self.gen_a))
            self.gen_a_entry.grid(row = row, column = col)
            col += 1
            self.sigma_label = tk.Label(self, text="\u03C3") # sigma, standard deviation
            self.sigma_label.grid(row = row, column = col)
            col += 1
            self.gen_b_entry = tk.Entry(self)
            self.gen_b_entry.insert(tk.END, str(self.gen_b))
            self.gen_b_entry.grid(row = row, column = col)
            col = 0
            row += 1
        elif rg_choice == 'uniform':
            self.a_label = tk.Label(self, text="a") # a
            self.a_label.grid(row = row, column = col)
            col += 1
            self.gen_a_entry = tk.Entry(self)
            self.gen_a_entry.insert(tk.END, str(self.gen_a))
            self.gen_a_entry.grid(row = row, column = col)
            col += 1
            self.b_label = tk.Label(self, text="b") # b
            self.b_label.grid(row = row, column = col)
            col += 1
            self.gen_b_entry = tk.Entry(self)
            self.gen_b_entry.insert(tk.END, str(self.gen_b))
            self.gen_b_entry.grid(row = row, column = col)
            col = 0
            row += 1
        elif rg_choice == 'increment':
            self.a_label = tk.Label(self, text="value") # increment
            self.a_label.grid(row = row, column = col)
            col += 1
            self.gen_a_entry = tk.Entry(self)
            self.gen_a_entry.insert(tk.END, str(self.gen_a))
            self.gen_a_entry.grid(row = row, column = col)
            col = 0
            row += 1
        if self.gen_edit_mode:
            self.save_button = tk.Button(self, text = "Save", command = self.save_information_source)
            self.save_button.grid(row = row, column = col, padx=10, pady=10)
        else:
            self.gen_add_button = tk.Button(self, text="Add", command=self.add_information_source)
            self.gen_add_button.grid(row = row, column = col, padx=10, pady=10)
        row += 1
        return row, col

    def choose_generator(self, event):
        if self.generator_choice.get() != '':
            self.gen_edit_mode = True
        self.generators_choice_widget()

    def generators_choice_widget(self, event = None):
        self.clear_window()

        current_row, current_col = 0, 0

        gen_label = tk.Label(self, text="Choose information sources")
        gen_label.grid(row = current_row)
        current_row += 1

        generators = self.qsystem.get_generators()
        options = [x.get_name() for x in generators]
        self.generator_choice = ttk.Combobox(self, values=options, textvariable=self.selected_generator)
        self.generator_choice.grid(row = current_row, column = current_col, padx=10, pady=10)
        current_col += 1
        self.generator_choice.bind("<<ComboboxSelected>>", self.choose_generator)
        
        # Create a Delete button
        self.gen_delete_button = tk.Button(self, text="Delete", command = self.delete_information_source)
        self.gen_delete_button.grid(row = current_row, column = current_col, padx=10, pady=10)
        current_col += 1

        # Create form reset button
        self.gen_new_button = tk.Button(self, text="Clear", command = self.soft_reset_generator_values)
        self.gen_new_button.grid(row = current_row, column = current_col, padx=10, pady=10)
        current_col = 0  
        current_row += 1

        current_row, current_col = self.display_generator_entry(current_row, current_col)

        # Create 'Back' and 'Next' buttons
        self.back_button = tk.Button(self, text="Back", command=self.setup_system_widget)
        self.back_button.grid(row = current_row, column = current_col, padx=20, pady=20)
        current_col += 1
        
        self.submit_button = tk.Button(self, text="Submit")
        self.submit_button.grid(row = current_row, column = current_col, padx=20, pady=20)

    def simulate(self):
        self.qsystem.simulate()

    def create_table(self, table_frame, *args):
        tree = ttk.Treeview(table_frame, columns=(args), show='headings')
        for arg in args:
            tree.heading(arg, text=arg)

        # Add the table to the frame with a vertical scrollbar
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
    
    def create_simulation_widget(self):
        if (self.model_file_path and self.metamodel_file_path and self.model_file_path != '' and self.metamodel_file_path != ''):
            self.clear_window()
            
            self.model = self.qmodel.import_textx_model(self.metamodel_file_path, self.model_file_path)
            self.qsystem.interpret(self.model)

            self.file_path_label = tk.Label(self, text=f"Using textx model: {self.model_file_path}")
            self.file_path_label.pack(pady=10)

            table_frame = tk.Frame(self)
            table_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)

            self.tree = self.create_table(table_frame, "name", "type", "distribution", "distribution args")
            self.populate_modules_table(self.tree)

            # Create 'Back' and 'Next' buttons
            self.back_button = tk.Button(self, text="Back", command=self.start)
            self.back_button.pack(side=tk.LEFT, padx=20, pady=20)
            
            self.next_button = tk.Button(self, text="Simulate", command=self.simulate)
            self.next_button.pack(side=tk.RIGHT, padx=20, pady=20)
        else:
            self.info_box("textX model is not saved", "Error")
            self.start()

    def load_model(self):
        model_path = filedialog.askopenfilename(
            initialdir=os.path.dirname(__file__),
            title="Select .qs File",
            filetypes=[("QS Files", "*.qs")],
            defaultextension=".qs"
        )
        if model_path and model_path != '':
            self.model_file_path = model_path
            metamodel_path = filedialog.askopenfilename(
                initialdir=os.path.dirname(__file__),
                title="Select .tx File",
                filetypes=[("TextX Files", "*.tx")],
                defaultextension=".tx"
            )
            if metamodel_path and metamodel_path != '':
                self.metamodel_file_path = metamodel_path
                # Everything is valid, go to simulation widget
                self.create_simulation_widget()
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