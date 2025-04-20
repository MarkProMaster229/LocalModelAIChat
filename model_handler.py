import os
import threading
import time
import tkinter as tk
from tkinter import messagebox, filedialog
from transformers import AutoModelForCausalLM, AutoTokenizer
from huggingface_hub import snapshot_download
import humanize

class ModelHandler:
    def __init__(self, app):
        self.app = app
        self.folder_path = ""
        self.is_downloading = False
        self.models = {}
        self.start_time = None
        self.total_size = None

    def select_folder(self):
        self.folder_path = filedialog.askdirectory()
        if self.folder_path:
            messagebox.showinfo("Успех", f"Выбрана папка: {self.folder_path}")
            self.check_existing_models()
        else:
            messagebox.showerror("Ошибка", "Пожалуйста, выберите папку.")

    def check_existing_models(self):
        self.models.clear()
        self.app.ui.model_listbox.delete(0, tk.END)
        for folder in os.listdir(self.folder_path):
            model_path = os.path.join(self.folder_path, folder)
            if os.path.isdir(model_path) and os.path.exists(os.path.join(model_path, "config.json")):
                try:
                    model = AutoModelForCausalLM.from_pretrained(model_path)
                    tokenizer = AutoTokenizer.from_pretrained(model_path)
                    self.models[folder] = (model, tokenizer)
                    self.app.ui.model_listbox.insert(tk.END, folder)
                except Exception as e:
                    print(f"Не удалось загрузить модель {folder}: {e}")

    def download_model(self):
        if self.is_downloading:
            messagebox.showwarning("Предупреждение", "Загрузка уже выполняется!")
            return

        model_name = self.app.ui.model_name.get().strip()
        if not model_name:
            messagebox.showerror("Ошибка", "Пожалуйста, введите название модели.")
            return
        if not self.folder_path:
            messagebox.showerror("Ошибка", "Пожалуйста, выберите папку для установки.")
            return

        self.is_downloading = True
        self.app.ui.download_button.config(state="disabled")
        self.app.ui.progress['value'] = 0
        self.app.ui.time_label.config(text="Оставшееся время: расчет...")
        messagebox.showinfo("Информация", f"Начинается загрузка модели '{model_name}'...")

        model_save_path = os.path.join(self.folder_path, model_name.replace("/", "_"))
        thread = threading.Thread(target=self._download_model_thread, args=(model_name, model_save_path))
        thread.daemon = True
        thread.start()

    def _download_model_thread(self, model_name, model_save_path):
        try:
            self.start_time = time.time()
            snapshot_download(
                repo_id=model_name,
                local_dir=model_save_path,
                local_dir_use_symlinks=False,
                cache_dir=model_save_path,
            )

            model = AutoModelForCausalLM.from_pretrained(model_save_path)
            tokenizer = AutoTokenizer.from_pretrained(model_save_path)

            self.app.root.after(0, lambda: self._finalize_download(model_name, model, tokenizer))
        except Exception as e:
            self.app.root.after(0, lambda err=e: self._handle_download_error(err))
        finally:
            self.app.root.after(0, self._reset_download_state)

    def _finalize_download(self, model_name, model, tokenizer):
        self.models[model_name.replace("/", "_")] = (model, tokenizer)
        self.update_model_list()
        messagebox.showinfo("Успех", f"Модель '{model_name}' загружена и готова к использованию.")

    def _handle_download_error(self, error):
        messagebox.showerror("Ошибка", f"Ошибка при загрузке модели: {error}")
        print(f"Ошибка: {error}")

    def _reset_download_state(self):
        self.is_downloading = False
        self.app.ui.download_button.config(state="normal")
        self.app.ui.time_label.config(text="Оставшееся время: неизвестно")

    def update_model_list(self):
        self.app.ui.model_listbox.delete(0, tk.END)
        for model_name in self.models:
            self.app.ui.model_listbox.insert(tk.END, model_name)

    def show_progress(self, value, total_size=None):
        self.app.ui.progress['value'] = value
        if total_size:
            self.total_size = total_size
        if value > 0 and self.total_size:
            elapsed_time = time.time() - self.start_time
            speed = (value / 100) * self.total_size / elapsed_time
            remaining_bytes = (1 - value / 100) * self.total_size
            remaining_time = remaining_bytes / speed if speed > 0 else 0
            self.app.ui.time_label.config(text=f"Оставшееся время: {humanize.naturaldelta(remaining_time)}")
        self.app.root.update_idletasks()