import customtkinter as ctk
from tkinter import messagebox

from GUI.sidebar import Sidebar
from GUI.votting import Votting
from core.serial_reader import SerialReader
from core.db import DB

class App():
    ctk.set_appearance_mode("Dark")

    def __init__(self):
        self.root=ctk.CTk()
        self.root.title("Avaliação da qualidade dos alimentos do RU - UFC")
        self.root.geometry("800x600")
        
        # --------  CONFIG DB  --------
        self.db_config = {
            'host': 'localhost',
            'user': 'root',
            'password': 'root123',
            'database': 'RU'
            }
        self.db_manager = None

        try:
            self.db_manager = DB(**self.db_config)
            self.db_manager.__enter__()
        except Exception as e:
            messagebox.showerror("Erro de Conexão DB", f"Não foi possível conectar ao banco de dados: {e}")
            self.db_manager = None
        
        # --------  CONFIG SERIAL  --------
        self.serial_config = {
            'port': 'COM3', 
            'baudrate': 9600, 
            'timeout': 1
            }   
        self.serial_reader = None

        try:
            self.serial_reader = SerialReader(**self.serial_config)
            temp_serial_instance = self.serial_reader.__enter__()
            if not temp_serial_instance:
                self.serial_reader = None
                messagebox.showwarning("Conexão Serial", "Não foi possível conectar à porta serial. A leitura do Arduino não funcionará.")
        except Exception as e:
            messagebox.showerror("Erro de Conexão Serial", f"Erro inesperado ao iniciar conexão serial: {e}")
            self.serial_reader = None
        
        # Frame principal onde as páginas serão carregadas
        self.main_frame = ctk.CTkFrame(self.root)
        self.main_frame.pack(side="right", fill="both", expand=True)
        self.current_page = None

        # Sidebar para navegação
        Sidebar(self.root, self.quitting, self.change_page)
        self.Wellcome()

        # self.root.protocol("WM_DELETE_WINDOW", self.quitting)
        self.root.mainloop()

    # Método para mudar de página
    def change_page(self, Page_class):
        if self.current_page:
            self.current_page.destroy()
        self.current_page = Page_class(self.main_frame, self.db_manager, self.serial_reader)
        self.current_page.pack(fill="both", expand=True)

    # Método para fechar a aplicação
    def quitting(self):
        if messagebox.askokcancel("Sair", "Deseja realmente sair?"):
            if self.db_manager:
                self.db_manager.__exit__(None, None, None)
            if self.serial_reader:
                if isinstance(self.current_page, Votting):
                     self.current_page.serial_thread_running = False
                self.serial_reader.__exit__(None, None, None)

            self.root.destroy()
    
    # Método de boas-vindas
    def Wellcome(self):
        if self.current_page:
            self.current_page.destroy()
        self.current_page = ctk.CTkFrame(self.main_frame)
        self.current_page.pack(fill="both", expand=True)

        ctk.CTkLabel(self.current_page, text="Bem-vindo(a) ao sistema de avaliação do RU!",font=("Arial", 30)).pack(expand=True)

if __name__ == "__main__":
    App()