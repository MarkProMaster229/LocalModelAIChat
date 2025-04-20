import tkinter as tk
from tkinter import messagebox, filedialog, ttk

class ModelDownloadAppUI:
    def __init__(self, app):
        self.app = app
        self.root = app.root
        self.model_name = tk.StringVar()

    def create_main_ui(self):
        self.model_label = tk.Label(self.root, text="Введите название модели (например, 'gpt2'):")
        self.model_label.pack(pady=10)

        self.model_entry = tk.Entry(self.root, textvariable=self.model_name, width=50)
        self.model_entry.pack(pady=10)

        self.select_button = tk.Button(self.root, text="Выберите папку для установки",
                                    command=self.app.model_handler.select_folder)
        self.select_button.pack(pady=10)

        self.download_button = tk.Button(self.root, text="Скачать модель",
                                      command=self.app.model_handler.download_model)
        self.download_button.pack(pady=10)

        self.progress = ttk.Progressbar(self.root, length=400, mode="determinate", maximum=100)
        self.progress.pack(pady=10)

        self.time_label = tk.Label(self.root, text="Оставшееся время: неизвестно")
        self.time_label.pack(pady=5)

        self.model_listbox = tk.Listbox(self.root, height=5, width=50)
        self.model_listbox.pack(pady=10)

        self.chat_button = tk.Button(self.root, text="Начать чат с моделью",
                                   command=self.app.chat_handler.start_chat)
        self.chat_button.pack(pady=10)

    def create_chat_ui(self):
        for widget in self.root.winfo_children():
            widget.destroy()

        self.root.title("Чат с моделью")
        self.chat_frame = tk.Frame(self.root)
        self.chat_frame.pack(pady=10, padx=10, fill="both", expand=True)

        self.chat_display = tk.Text(self.chat_frame, height=20, width=50, state="disabled", wrap="word")
        self.chat_display.pack(pady=10, fill="both", expand=True)

        scrollbar = tk.Scrollbar(self.chat_frame, command=self.chat_display.yview)
        scrollbar.pack(side="right", fill="y")
        self.chat_display.config(yscrollcommand=scrollbar.set)

        self.input_frame = tk.Frame(self.root)
        self.input_frame.pack(pady=10, fill="x")

        self.message_entry = tk.Entry(self.input_frame, width=40)
        self.message_entry.pack(side="left", padx=5)
        self.message_entry.bind("<Return>", self.app.chat_handler.send_message)

        self.send_button = tk.Button(self.input_frame, text="Отправить",
                                  command=self.app.chat_handler.send_message)
        self.send_button.pack(side="left")

        self.back_button = tk.Button(self.root, text="Вернуться",
                                   command=self.app.chat_handler.return_to_main)
        self.back_button.pack(pady=5)