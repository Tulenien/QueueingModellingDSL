import tkinter as tk
from tkinter import ttk
import os
from tkinter import filedialog, messagebox
from qsystem import QSystem
from qmodel import QModel

style = ttk.Style()
style.configure("Custom.Treeview", background="#f0f0ff", foreground="black", rowheight=25)

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
        self.configure(bg="#ccddf3")
        self.center_window()
        self.selected_system_type = tk.StringVar()
        self.selected_system_type.set("timed")
        self.start()



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

        self.welcome_label = tk.Label(self, text="QUEUEING MODELLING DSL", bg="#ccddf3", fg="#193d6c",
                         font=('Times', 14, 'bold'))
        self.welcome_label.pack(fill=tk.BOTH, pady=30)  # center label in frame

        self.return_button = tk.Button(self, text="INPUT  MODEL  PARAMETERS", command=self.setup_system_widget, foreground='#F5F5F5',
                       background='#193d6c', relief='raised', font=('Times', 12, 'bold'), width=30)
        self.return_button.pack(pady=15)
        
        self.open_file_button = tk.Button(self, text="LOAD TEXTX MODEL", command=self.load_model, foreground='#F5F5F5',
                       background='#193d6c', relief='raised', font=('Times', 12, 'bold'),  width=30)
        self.open_file_button.pack(pady=15)

        self.use_cached_model_button = tk.Button(self, text="USE SAVED TEXTX MODEL", command=self.create_simulation_widget, foreground='#F5F5F5',
                       background='#193d6c', relief='raised', font=('Times', 12, 'bold'),  width=30)
        self.use_cached_model_button.pack(pady=15)


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
        self.delta_constraint = tk.Entry(self.entry_frame)
        self.delta_constraint.insert(tk.END, str(self.qsystem.get_delta()))
        self.delta_constraint.pack(pady=5)
        self.delta_constraint_label = tk.Label(self.entry_frame, text="System time delta constraint")
        self.delta_constraint_label.pack()

    def submit_form(self):
        choice = self.selected_system_type.get()
        if choice == 'timed':
            pass
        elif choice == 'requests':
            pass
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
        
        self.submit_button = tk.Button(self, text="Submit", command=self.submit_form)
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

            self.file_path_label = tk.Label(self, text=f"Using textx model: {self.model_file_path}", bg="#ccddf3", fg="#193d6c",
                         font=('Times', 10, 'bold'))
            self.file_path_label.pack(fill=tk.BOTH, pady=10)

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
        self.frame_for_selected_files = tk.Frame(self, width=800, height=500, bg="#ccddf3")
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
                self.chosen_file_label = tk.Label(self.frame_for_selected_files, text="Chosen files:", bg="#ccddf3",
                                                  fg="#193d6c",
                                                  font=('Times', 12, 'bold'))
                self.chosen_file_label.pack(fill=tk.BOTH, pady=10)

                self.file_path_label = tk.Label(self.frame_for_selected_files, text=f"Selected model file: {self.model_file_path}", bg="#ccddf3",
                                                  fg="#193d6c",
                                                  font=('Times', 10, 'bold'))
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
                                                         text=f"Selected metamodel file: {self.metamodel_file_path}", bg="#ccddf3",
                                                  fg="#193d6c",
                                                  font=('Times', 10, 'bold'))
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