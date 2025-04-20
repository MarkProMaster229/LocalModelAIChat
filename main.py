import tkinter as tk
from ui import ModelDownloadAppUI
from model_handler import ModelHandler
from chat import ChatHandler


class ModelDownloadApp:
    def __init__(self, root):
        self.root = root
        self.model_handler = ModelHandler(self)
        self.chat_handler = ChatHandler(self)
        self.ui = ModelDownloadAppUI(self)

        self.root.title("Загрузчик модели и чат")
        self.root.geometry("600x700")

        self.ui.create_main_ui()


if __name__ == "__main__":
    root = tk.Tk()
    app = ModelDownloadApp(root)
    root.mainloop()