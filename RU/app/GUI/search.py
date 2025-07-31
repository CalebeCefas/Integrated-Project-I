import customtkinter as ctk

class Search(ctk.CTkFrame):
    def __init__(self, master, db_manager=None, serial_reader=None):
        super().__init__(master)
        
        ctk.CTkLabel(self, text="Pesquisa", font=("Arial", 18)).pack(pady=10)
