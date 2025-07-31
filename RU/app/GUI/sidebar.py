import customtkinter as ctk

from GUI.graph import Graph
from GUI.search import Search
from GUI.votting import Votting

class Sidebar(ctk.CTkFrame):

    def __init__(self, root, quiting, change_page):
        super().__init__(root, corner_radius=0)
        self.pack(side="left", fill="y")
        self.quiting = quiting
        self.change_page = change_page

        # texto e butões do sidebar
        ctk.CTkLabel(self, text="Menu", font=("Arial", 20, "bold")).pack(padx=20, pady=10)

        # Opção de tema
        theme = ctk.CTkOptionMenu(self, values=["Light", "Dark"], command=self.theme_mode)
        theme.pack(padx=10, pady=10, fill='x')
        theme.set("Dark")

        # Botões para mudar de página
        self.button('Votação', Votting)
        self.button('Gráficos', Graph)
        self.button('Pesquisa', Search)

        ctk.CTkButton(self, text="Sair", command=quiting).pack(side="bottom", padx=10, pady=20, fill="x")
      
    # Método para mudar o tema
    def theme_mode(self, choice):
        ctk.set_appearance_mode(choice)

    def button(self, text, frame_class):
        ctk.CTkButton(self, text=text, command=lambda: self.change_page(frame_class)).pack(padx=10, pady=3, fill="x")