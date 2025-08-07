import customtkinter as ctk
from GUI.graph import Graph
from GUI.search import Search
from GUI.votting import Votting
from GUI.about import About

class Sidebar(ctk.CTkFrame):
    def __init__(self, root, quitting, change_page):
        super().__init__(root, corner_radius=0)
        self.pack(side="left", fill="y")
        self.quitting = quitting
        self.change_page = change_page

        ctk.CTkLabel(self, text="Menu", font=("Arial", 20, "bold")).pack(padx=20, pady=10)

        theme = ctk.CTkOptionMenu(self, values=["Light", "Dark"], command=self.theme_mode)
        theme.pack(padx=10, pady=10, fill='x')
        theme.set("Dark")

        # Frame superior para os botões principais
        self.frame_top = ctk.CTkFrame(self, fg_color="transparent")
        self.frame_top.pack(padx=10, pady=(10, 0), fill="both", expand=True)

        self.button('Votação', Votting, parent=self.frame_top)
        self.button('Gráficos', Graph, parent=self.frame_top)
        self.button('Pesquisa', Search, parent=self.frame_top)

        # Frame inferior para o botão Sobre e Sair
        self.frame_bottom = ctk.CTkFrame(self, fg_color="transparent")
        self.frame_bottom.pack(side="bottom", fill="x", padx=10, pady=10)

        self.button('Sobre', About, parent=self.frame_bottom)

        ctk.CTkButton(self.frame_bottom, text="Sair", command=quitting).pack(pady=(10, 0), fill="x")

    def theme_mode(self, choice):
        ctk.set_appearance_mode(choice)

    def button(self, text, frame_class, parent=None):
        if parent is None:
            parent = self
        ctk.CTkButton(parent, text=text, command=lambda: self.change_page(frame_class)).pack(pady=3, fill="x")
