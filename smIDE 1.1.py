import os
import tkinter as tk
from tkinter import ttk, scrolledtext, filedialog, messagebox, simpledialog
from pygments import highlight
from pygments.lexers import get_lexer_by_name
from pygments.formatters import get_formatter_by_name

class smIDE:

    def __init__(self, root):
        self.root = root
        self.root.title("smIDE 1.0")
        self.root.geometry("1250x1250")
        self.root.option_add('*Font', 'helvetica 11')

        self.create_menu()
        self.create_notebook()
        self.create_toolbar()
        self.create_file_explorer()

        # Dictionary to keep track of tab counts
        self.tab_counts = {}
        # Variable to keep track of the currently active tab
        self.current_extension = ""
        self.current_tab = None

    def create_menu(self):
        menu_bar = tk.Menu(self.root)

        file_menu = tk.Menu(menu_bar, tearoff=0)
        file_menu.add_command(label="New", command=self.new_file)
        file_menu.add_command(label="Open", command=self.open_file)
        file_menu.add_command(label="Save", command=self.save_file)
        file_menu.add_command(label="Save As", command=self.save_file_as)
        file_menu.add_separator()
        file_menu.add_command(label="Exit", command=self.root.destroy)

        menu_bar.add_cascade(label="File", menu=file_menu)

        self.root.config(menu=menu_bar)

    def create_notebook(self):
        self.notebook = ttk.Notebook(self.root)

        languages = ["HTML", "CSS", "SCSS", "JavaScript", "Python"]
        self.text_widgets = {}

        for lang in languages:
            text_widget = scrolledtext.ScrolledText(self.notebook,
                                                    wrap=tk.WORD,
                                                    bg='#282c34',
                                                    fg='white',
                                                    insertbackground='white',
                                                    insertwidth=4,
                                                    padx=10,
                                                    pady=10)
            text_widget.config(font=('helvetica', 12))
            self.notebook.add(text_widget, text=lang)
            self.text_widgets[lang] = text_widget

        self.notebook.pack(side=tk.LEFT, expand=1, fill="both")
        self.notebook.bind("<ButtonRelease-1>",
                           self.on_tab_selected)  # Bind event to tab selection

    def create_file_explorer(self):
        frame = ttk.Frame(self.root)
        frame.pack(side=tk.LEFT, fill="y")

        up_button = ttk.Button(frame, text="Up", command=self.go_up_directory)
        up_button.pack(pady=10)

        label = ttk.Label(frame, text="File Explorer", font=('helvetica', 12))
        label.pack(pady=10)

        self.file_listbox = tk.Listbox(frame,
                                       selectmode=tk.SINGLE,
                                       bg='#282c34',
                                       fg='white',
                                       selectbackground='#61dafb',
                                       font=('helvetica', 11))
        self.file_listbox.pack(expand=1, fill="both")

        # Bind double-click event to open file or change directory
        self.file_listbox.bind('<Double-Button-1>', self.on_file_list_double_click)

        self.update_file_list()

    def create_toolbar(self):
        toolbar = ttk.Frame(self.root)

        new_button = ttk.Button(toolbar, text="New", command=self.new_file)
        open_button = ttk.Button(toolbar, text="Open", command=self.open_file)
        save_button = ttk.Button(toolbar, text="Save", command=self.save_file)
        plus_button = ttk.Button(toolbar, text="+ add Tab +", command=self.create_new_tab)

        new_button.pack(side=tk.LEFT, padx=5)
        open_button.pack(side=tk.LEFT, padx=5)
        save_button.pack(side=tk.LEFT, padx=5)
        plus_button.pack(side=tk.LEFT, padx=5)

        toolbar.pack(side=tk.TOP, fill=tk.X)

    def update_file_list(self):
        self.file_listbox.delete(0, tk.END)
        current_directory = os.getcwd()
        for file_name in os.listdir(current_directory):
            file_path = os.path.join(current_directory, file_name)
            if os.path.isdir(file_path):
                self.file_listbox.insert(tk.END, file_name)

    def go_up_directory(self):
        current_directory = os.getcwd()
        parent_directory = os.path.dirname(current_directory)
        os.chdir(parent_directory)
        self.update_file_list()

    def on_file_list_double_click(self, event):
        selected_index = self.file_listbox.curselection()
        if selected_index:
            selected_item = self.file_listbox.get(selected_index)
            current_directory = os.getcwd()
            new_directory = os.path.join(current_directory, selected_item)
            if os.path.isdir(new_directory):
                os.chdir(new_directory)
                self.update_file_list()

    def on_tab_selected(self, event):
        # Update the currently active tab
        active_tab = self.notebook.tab(self.notebook.select(), "text")
        self.current_tab = active_tab
        extension_mapping = {
            "HTML": "html",
            "CSS": "css",
            "SCSS": "scss",
            "JavaScript": "js",
            "Python": "py"
        }
        self.current_extension = extension_mapping.get(active_tab, "")

    def open_selected_file(self, event):
        selected_index = self.file_listbox.curselection()
        if selected_index:
            selected_item = self.file_listbox.get(selected_index)
            current_directory = os.getcwd()
            file_path = os.path.join(current_directory, selected_item)
            if os.path.isfile(file_path):
                # Display the count next to the tab name
                count = self.update_tab_count(self.current_tab)
                with open(file_path, "r") as file:
                    content = file.read()
                    # Use Pygments for syntax highlighting
                    lexer = get_lexer_by_name(self.current_extension.lower())
                    formatter = get_formatter_by_name("html",
                                                      linenos=True,
                                                      cssclass="source")
                    highlighted_content = highlight(content, lexer, formatter)
                    text_widget = self.text_widgets[self.current_tab]
                    text_widget.delete(1.0, tk.END)
                    text_widget.insert(tk.END, highlighted_content)
                    self.notebook.tab(text_widget, text=f"{self.current_tab} x{count}")

    def open_file(self):
        file_path = filedialog.askopenfilename(
            filetypes=[("Text files", "*.txt"), ("All files", "*.*")])
        if file_path:
            with open(file_path, "r") as file:
                content = file.read()
                # Open the file only in the currently active tab
                if self.current_tab:
                    text_widget = self.text_widgets[self.current_tab]
                    text_widget.delete(1.0, tk.END)
                    text_widget.insert(tk.END, content)

    def save_file(self):
        if self.current_tab:
            file_path = filedialog.asksaveasfilename(
                defaultextension=f".{self.current_extension}" if self.current_extension else "",
                filetypes=[(f"{self.current_extension.upper()} files",
                            f"*.{self.current_extension}") if self.current_extension else ("All files", "*.*")])
            if file_path:
                with open(file_path, "w") as file:
                    text_widget = self.text_widgets[self.current_tab]
                    content = text_widget.get(1.0, tk.END)
                    file.write(content)
                self.update_file_list()  # Update file list after saving
        else:
            messagebox.showwarning("Save Error", "Please select a tab to save.")

    def save_file_as(self):
        if self.current_tab:
            file_path = filedialog.asksaveasfilename(
                defaultextension=f".{self.current_extension}" if self.current_extension else "",
                filetypes=[(f"{self.current_extension.upper()} files",
                            f"*.{self.current_extension}") if self.current_extension else ("All files", "*.*")])
            if file_path:
                with open(file_path, "w") as file:
                    text_widget = self.text_widgets[self.current_tab]
                    content = text_widget.get(1.0, tk.END)
                    file.write(content)
                self.update_file_list()  # Update file list after saving
        else:
            messagebox.showwarning("Save Error", "Please select a tab to save.")

    def create_new_tab(self):
        # Prompt user to enter the name of the new tab
        new_tab_name = simpledialog.askstring("New Tab",
                                              "Enter the name for the new tab:",
                                              parent=self.root)
        if new_tab_name:
            # Prompt user to select a language for the new tab
            language_options = [
                "Python", "HTML", "CSS", "SCSS", "JavaScript", "Undefined"
            ]
            selected_language = simpledialog.askstring(
                "New Tab",
                "Select a language for the new tab:",
                parent=self.root,
                initialvalue="Undefined")

            # Validate the selected_language to ensure correct display
            if selected_language is not None:
                selected_language = selected_language.lower()
                if selected_language not in map(lambda x: x.lower(), language_options):
                    selected_language = ""

            if selected_language:
                if selected_language.lower() == "undefined":
                    selected_language = ""  # Set to an empty string for an undefined language
                # Create a new tab with the specified language
                text_widget = scrolledtext.ScrolledText(self.notebook,
                                                        wrap=tk.WORD,
                                                        bg='#282c34',
                                                        fg='white',
                                                        insertbackground='white',
                                                        insertwidth=4,
                                                        padx=10,
                                                        pady=10)
                text_widget.config(font=('helvetica', 12))
                tab_name = f"{new_tab_name} ({selected_language})"
                self.notebook.add(text_widget, text=tab_name)
                self.text_widgets[tab_name] = text_widget
                self.notebook.select(len(self.text_widgets) - 1)  # Select the last tab

                # Set the current_tab and current_extension attributes
                self.current_tab = tab_name
                extension_mapping = {
                    "HTML": "html",
                    "CSS": "css",
                    "SCSS": "scss",
                    "JavaScript": "js",
                    "Python": "py"
                }
                self.current_extension = extension_mapping.get(selected_language, "")

                self.update_tab_count(tab_name)  # Update tab count

    def update_tab_count(self, selected_tab):
        # Update the count and return the updated count
        count = self.tab_counts.get(selected_tab, 0) + 1
        self.tab_counts[selected_tab] = count
        return count

    def new_file(self):
        # Add your implementation for creating a new file here
        pass

if __name__ == "__main__":
    root = tk.Tk()
    SMIDE = smIDE(root)
    root.mainloop()