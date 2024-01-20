import tkinter as tk
from tkinter import scrolledtext
from tkinter import filedialog


class smIDE:

  def __init__(self, root):
    self.root = root
    self.root.title("smIDE DevBeta ver0.0.1")
    self.text_area = scrolledtext.ScrolledText(root,
                                               wrap=tk.WORD,
                                               width=40,
                                               height=10)
    self.text_area.pack(expand=True, fill='both')

    # Menu Bar
    self.menu_bar = tk.Menu(root)
    self.root.config(menu=self.menu_bar)

    # File Menu
    self.file_menu = tk.Menu(self.menu_bar, tearoff=0)
    self.menu_bar.add_cascade(label="File", menu=self.file_menu)
    self.file_menu.add_command(label="New", command=self.new_file)
    self.file_menu.add_command(label="Open", command=self.open_file)
    self.file_menu.add_command(label="Save", command=self.save_file)
    self.file_menu.add_separator()
    self.file_menu.add_command(label="Exit", command=self.root.destroy)

  def new_file(self):
    self.text_area.delete(1.0, tk.END)

  def open_file(self):
    file_path = filedialog.askopenfilename(defaultextension=".py",
                                           filetypes=[("Python", "*.py"),
                                                      ("All files", "*.*")])
    if file_path:
      with open(file_path, 'r') as file:
        content = file.read()
        self.text_area.delete(1.0, tk.END)
        self.text_area.insert(tk.END, content)

  def save_file(self):
    file_path = filedialog.asksaveasfilename(defaultextension=".py",
                                             filetypes=[("Python", "*.py"),
                                                        ("All files", "*.*")])
    if file_path:
      with open(file_path, 'w') as file:
        content = self.text_area.get(1.0, tk.END)
        file.write(content)


if __name__ == "__main__":
  root = tk.Tk()
  SMIDE = smIDE(root)
  root.mainloop()

