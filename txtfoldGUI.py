import tkinter as tk
from tkinter import filedialog, messagebox, ttk
import threading
from converter import FolderToTextConverter

class FolderToTextConverterGUI:
    def __init__(self, master):
        self.master = master
        master.title("Folder to Text Converter")
        master.geometry("800x600")

        # Create a custom theme
        self.create_custom_theme()

        # Input folder
        input_frame = ttk.Frame(master, padding=10)
        input_frame.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")
        self.input_folder_label = ttk.Label(input_frame, text="Input Folder:", font=("Arial", 12))
        self.input_folder_label.pack(side="left", padx=5)
        self.input_folder_entry = ttk.Entry(input_frame, width=40, font=("Arial", 12))
        self.input_folder_entry.pack(side="left", padx=5)
        self.input_folder_button = ttk.Button(input_frame, text="Browse", command=self.browse_input_folder)
        self.input_folder_button.pack(side="left", padx=5)

        # Output folder/file
        output_frame = ttk.Frame(master, padding=10)
        output_frame.grid(row=1, column=0, padx=10, pady=10, sticky="nsew")
        self.output_label = ttk.Label(output_frame, text="Output:", font=("Arial", 12))
        self.output_label.pack(side="left", padx=5)
        self.output_entry = ttk.Entry(output_frame, width=40, font=("Arial", 12))
        self.output_entry.pack(side="left", padx=5)
        self.output_button = ttk.Button(output_frame, text="Browse", command=self.browse_output)
        self.output_button.pack(side="left", padx=5)

        # File types
        file_types_frame = ttk.Frame(master, padding=10)
        file_types_frame.grid(row=2, column=0, padx=10, pady=10, sticky="nsew")
        self.file_types_label = ttk.Label(file_types_frame, text="File Types (comma separated):", font=("Arial", 12))
        self.file_types_label.pack(side="left", padx=5)
        self.file_types_entry = ttk.Entry(file_types_frame, width=40, font=("Arial", 12))
        self.file_types_entry.pack(side="left", padx=5)

        # Output type
        output_type_frame = ttk.Frame(master, padding=10)
        output_type_frame.grid(row=3, column=0, padx=10, pady=10, sticky="nsew")
        self.output_type_label = ttk.Label(output_type_frame, text="Output Type:", font=("Arial", 12))
        self.output_type_label.pack(side="left", padx=5)
        self.output_type_var = tk.StringVar()
        self.output_type_var.set("single_file")
        self.single_file_radio = ttk.Radiobutton(output_type_frame, text="Single File", variable=self.output_type_var, value="single_file", style="TRadiobutton")
        self.single_file_radio.pack(side="left", padx=5)
        self.individual_files_radio = ttk.Radiobutton(output_type_frame, text="Individual Files", variable=self.output_type_var, value="individual_files", style="TRadiobutton")
        self.individual_files_radio.pack(side="left", padx=5)

        # URL input
        url_frame = ttk.Frame(master, padding=10)
        url_frame.grid(row=4, column=0, padx=10, pady=10, sticky="nsew")
        self.url_label = ttk.Label(url_frame, text="URL:", font=("Arial", 12))
        self.url_label.pack(side="left", padx=5)
        self.url_entry = ttk.Entry(url_frame, width=40, font=("Arial", 12))
        self.url_entry.pack(side="left", padx=5)

        # Convert button
        self.convert_button = ttk.Button(master, text="Convert", command=self.start_conversion, style="TButton")
        self.convert_button.grid(row=5, column=0, padx=10, pady=10)

        # Progress bar
        self.progress_bar = ttk.Progressbar(master, mode="determinate", style="TProgressbar")
        self.progress_bar.grid(row=6, column=0, padx=10, pady=10, sticky="ew")

        # Log window
        log_frame = ttk.Frame(master, padding=10)
        log_frame.grid(row=7, column=0, padx=10, pady=10, sticky="nsew")
        self.log_text = tk.Text(log_frame, height=10, width=80, font=("Courier", 10))
        self.log_text.pack(side="left", fill="both", expand=True)
        log_scrollbar = ttk.Scrollbar(log_frame, command=self.log_text.yview)
        log_scrollbar.pack(side="right", fill="y")
        self.log_text.config(yscrollcommand=log_scrollbar.set)

        # File progress bar
        file_progress_frame = ttk.Frame(master, padding=10)
        file_progress_frame.grid(row=8, column=0, padx=10, pady=10, sticky="ew")
        self.file_progress_label = ttk.Label(file_progress_frame, text="", font=("Arial", 10))
        self.file_progress_label.pack(side="left", padx=5)
        self.file_progress_bar = ttk.Progressbar(file_progress_frame, mode="determinate", length=400)
        self.file_progress_bar.pack(side="left", padx=5, fill="x", expand=True)

        # Status label
        self.status_label = ttk.Label(master, text="", font=("Arial", 12), foreground="#4CAF50")
        self.status_label.grid(row=9, column=0, padx=10, pady=10)

        # Configure grid weights
        master.rowconfigure(0, weight=1)
        master.rowconfigure(1, weight=1)
        master.rowconfigure(2, weight=1)
        master.rowconfigure(3, weight=1)
        master.rowconfigure(4, weight=1)
        master.rowconfigure(5, weight=1)
        master.rowconfigure(6, weight=1)
        master.rowconfigure(7, weight=1)
        master.rowconfigure(8, weight=1)
        master.rowconfigure(9, weight=1)
        master.columnconfigure(0, weight=1)

        self.converter = FolderToTextConverter()
        self.conversion_thread = None

    def create_custom_theme(self):
        style = ttk.Style()
        style.theme_create("CustomTheme", parent="clam", settings={
            "TFrame": {"configure": {"background": "#1E1E1E"}},
            "TLabel": {"configure": {"background": "#1E1E1E", "foreground": "#FFFFFF", "font": ("Arial", 12)}},
            "TButton": {"configure": {"background": "#4CAF50", "foreground": "#FFFFFF", "font": ("Arial", 12)}},
            "TEntry": {"configure": {"fieldbackground": "#2C2C2C", "foreground": "#FFFFFF", "font": ("Arial", 12)}},
            "TRadiobutton": {"configure": {"background": "#1E1E1E", "foreground": "#FFFFFF", "font": ("Arial", 12)}},
            "TProgressbar": {"configure": {"background": "#4CAF50", "troughcolor": "#2C2C2C", "bordercolor": "#1E1E1E", "lightcolor": "#4CAF50", "darkcolor": "#4CAF50"}},
        })
        style.theme_use("CustomTheme")

    def browse_input_folder(self):
        input_folder = filedialog.askdirectory()
        if input_folder:
            self.input_folder_entry.delete(0, tk.END)
            self.input_folder_entry.insert(0, input_folder)

    def browse_output(self):
        output_type = self.output_type_var.get()
        if output_type == "single_file":
            output_path = filedialog.asksaveasfilename(defaultextension=".txt")
        else:
            output_path = filedialog.askdirectory()

        if output_path:
            self.output_entry.delete(0, tk.END)
            self.output_entry.insert(0, output_path)

    def start_conversion(self):
        if self.conversion_thread and self.conversion_thread.is_alive():
            messagebox.showerror("Error", "A conversion is already in progress.")
            return

        input_folder = self.input_folder_entry.get()
        output_path = self.output_entry.get()
        file_types = [ext.strip() for ext in self.file_types_entry.get().split(",") if ext.strip()]
        output_type = self.output_type_var.get()
        url = self.url_entry.get()

        self.conversion_thread = threading.Thread(target=self.run_conversion, args=(input_folder, output_path, file_types, output_type, url))
        self.conversion_thread.start()

    def run_conversion(self, input_folder, output_path, file_types, output_type, url):
        try:
            self.converter.convert_folder_to_text(input_folder, output_path, file_types, output_type, url)
            self.update_status("Conversion completed successfully.", "#4CAF50")
        except ValueError as e:
            self.update_status(str(e), "#FF0000")
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def update_status(self, message, color):
        self.status_label.config(text=message, foreground=color)
        self.status_label.update_idletasks()

    def update_log(self, message):
        self.log_text.insert(tk.END, message + "\n")
        self.log_text.see(tk.END)
        self.log_text.update_idletasks()

    def update_progress(self):
        self.progress_bar.update_idletasks()

    def update_file_progress(self, filename, progress):
        self.file_progress_label.config(text=f"Processing: {filename}")
        self.file_progress_bar["value"] = progress
        self.file_progress_bar.update_idletasks()

root = tk.Tk()
converter_gui = FolderToTextConverterGUI(root)
root.mainloop()