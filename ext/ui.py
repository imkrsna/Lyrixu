import tkinter as tk

class UI:
    def __init__(self):
        self.root = tk.Tk()
        self.initial_window()

    def initial_window(self):
        self.root.title("Lyrixu")
        self.root.geometry("400x400")

        # variables
        project_name_var = tk.StringVar()

        # ui components
        project_frame = tk.Frame(self.root)

        # Project Name
        project_name_frame = tk.Frame(project_frame)
        project_name_label = tk.Label(project_name_frame, text="Project Name:", font=("Consolas", 15, "bold"))
        project_name_label.grid(row=0, column=0)
        project_name_entry = tk.Entry(project_name_frame, font=("Consolas", 15, "bold"))
        project_name_entry.grid(row=0, column=1)
        project_name_frame.pack(pady=5)
        
        # YouTube Url
        project_url_frame = tk.Frame(project_frame)
        project_url_label = tk.Label(project_url_frame, text="Project Url:", font=("Consolas", 15, "bold"))
        project_url_label.grid(row=0, column=0)
        project_url_entry = tk.Entry(project_url_frame, font=("Consolas", 15, "bold"))
        project_url_entry.grid(row=0, column=1)
        project_url_frame.pack(pady=5)

        project_frame.pack(padx=20, pady=20)
        self.root.mainloop()