import tkinter as tk
from tkinter import messagebox
import torch

class ChatHandler:
    def __init__(self, app):
        self.app = app
        self.selected_model = None
        self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        self.chat_history = []  # Список для хранения истории диалога
        print(f"Using device: {self.device}")

    def start_chat(self):
        if not self.app.model_handler.models:
            messagebox.showerror("Ошибка", "Нет доступных моделей. Пожалуйста, загрузите модель.")
            return

        selected_index = self.app.ui.model_listbox.curselection()
        if not selected_index:
            messagebox.showerror("Ошибка", "Пожалуйста, выберите модель для общения.")
            return

        self.selected_model = list(self.app.model_handler.models.values())[selected_index[0]]
        self.chat_history = []  # Очищаем историю при старте нового чата
        self.app.ui.create_chat_ui()

    def send_message(self, event=None):
        user_input = self.app.ui.message_entry.get().strip()
        if not user_input:
            return

        model, tokenizer = self.selected_model
        self.display_message(f"Вы: {user_input}", "user")
        self.app.ui.message_entry.delete(0, tk.END)

        try:
            if tokenizer.pad_token is None:
                tokenizer.pad_token = tokenizer.eos_token

            # Добавляем сообщение пользователя в историю
            self.chat_history.append({"role": "user", "content": user_input})

            # Формируем полный текст для модели (включая историю)
            conversation = ""
            for message in self.chat_history:
                if message["role"] == "user":
                    conversation += f"User: {message['content']}\n"
                else:
                    conversation += f"Bot: {message['content']}\n"

            # Токенизируем весь текст (включая историю)
            inputs = tokenizer(conversation, return_tensors="pt", padding=True, truncation=True)

            # Перенос модели и данных на устройство
            model = model.to(self.device)
            inputs = {key: val.to(self.device) for key, val in inputs.items()}

            # Генерация ответа
            outputs = model.generate(
                input_ids=inputs['input_ids'],
                attention_mask=inputs['attention_mask'],
                max_length=150,
                num_return_sequences=1,
                pad_token_id=tokenizer.eos_token_id,
                temperature=0.1,
                top_k=50,
                top_p=0.9,
                repetition_penalty=1.2
            )

            # Декодируем ответ
            response = tokenizer.decode(outputs[0], skip_special_tokens=True)

            # Удаляем входной текст из ответа, если он там есть
            if response.startswith(conversation):
                response = response[len(conversation):].strip()

            # Добавляем ответ модели в историю
            self.chat_history.append({"role": "bot", "content": response})

            # Отображаем ответ
            self.display_message(f"Бот: {response}", "bot")

        except Exception as e:
            self.display_message(f"Ошибка: {e}", "error")

    def display_message(self, message, tag):
        self.app.ui.chat_display.config(state="normal")
        self.app.ui.chat_display.insert(tk.END, message + "\n\n")
        self.app.ui.chat_display.tag_add(tag, "end-2l", "end-1l")
        if tag == "user":
            self.app.ui.chat_display.tag_config("user", foreground="blue", font=("Arial", 10, "bold"))
        elif tag == "bot":
            self.app.ui.chat_display.tag_config("bot", foreground="green")
        else:
            self.app.ui.chat_display.tag_config("error", foreground="red")
        self.app.ui.chat_display.config(state="disabled")
        self.app.ui.chat_display.see(tk.END)

    def return_to_main(self):
        for widget in self.app.root.winfo_children():
            widget.destroy()
        self.app.ui.create_main_ui()
        self.app.model_handler.update_model_list()