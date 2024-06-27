import tkinter as tk
from tkinter import ttk
import os
from tkinter import filedialog, messagebox
from qsystem import QSystem
from qmodel import QModel

class MainApp(tk.Tk):
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
        self.selected_system_type.set("timed")
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

    def display_system_constraints_entry(self):
        choice = self.selected_system_type.get()
        if choice == 'timed':
            self.time_constraint_entry = tk.Entry(self.entry_frame)
            self.time_constraint_entry.insert(tk.END, str(self.qsystem.get_time_constraint()))
            self.time_constraint_entry.pack(pady=5)
            self.time_constraint_entry_label = tk.Label(self.entry_frame, text="System time constraint")
            self.time_constraint_entry_label.pack()
        elif choice == 'requests':
            self.requests_constraint_entry = tk.Entry(self.entry_frame)
            self.requests_constraint_entry.insert(tk.END, str(self.qsystem.get_requests_constraint()))
            self.requests_constraint_entry.pack(pady=5)
            self.requests_constraint_entry_label = tk.Label(self.entry_frame, text="System requests number constraint")
            self.requests_constraint_entry_label.pack()
        else:
            self.time_constraint_entry = tk.Entry(self.entry_frame)
            self.time_constraint_entry.pack(pady=5)
            self.time_constraint_entry_label = tk.Label(self.entry_frame, text="System time constraint")
            self.time_constraint_entry_label.pack()
        self.delta_constraint_entry = tk.Entry(self.entry_frame)
        self.delta_constraint_entry.insert(tk.END, str(self.qsystem.get_delta()))
        self.delta_constraint_entry.pack(pady=5)
        self.delta_constraint_label = tk.Label(self.entry_frame, text="System time delta constraint")
        self.delta_constraint_label.pack()

    def submit_constraints_form(self):
        choice = self.selected_system_type.get()
        self.qsystem.set_delta(self.delta_constraint_entry.get())
        if choice == 'timed':
            self.qsystem.set_time_constraint(self.time_constraint_entry.get())
        elif choice == 'requests':
            self.qsystem.set_requests_constaint(self.requests_constraint_entry.get())
        else:
            pass

    def setup_system_widget(self, event=None):
        self.clear_window()

        self.system_widget_header = tk.Label(self, text="Choose system constraints")
        self.system_widget_header.pack()

        options = ['timed', 'requests']
        self.system_type_choice = ttk.Combobox(self, values=options, textvariable=self.selected_system_type)
        self.system_type_choice.pack(pady=20)
        self.system_type_choice.bind("<<ComboboxSelected>>", self.setup_system_widget)

        # Frame to hold the dynamic entry fields
        self.entry_frame = tk.Frame(self)
        self.entry_frame.pack(pady=20)

        self.display_system_constraints_entry()
        
        # Create 'Back' and 'Next' buttons
        self.back_button = tk.Button(self, text="Back", command=self.start)
        self.back_button.pack(side=tk.LEFT, padx=20, pady=20)
        
        self.submit_button = tk.Button(self, text="Submit", command=self.submit_constraints_form)
        self.submit_button.pack(side=tk.RIGHT, padx=20, pady=20)

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