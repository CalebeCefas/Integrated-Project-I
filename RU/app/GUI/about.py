import customtkinter as ctk
import webbrowser

class About(ctk.CTkFrame):
    def __init__(self, master, db_manager=None, serial_reader=None):
        super().__init__(master)

        # Frame central para conter todo o conteúdo centralizado
        content_frame = ctk.CTkFrame(self, fg_color="transparent")
        content_frame.pack(expand=True)  # Centraliza verticalmente e horizontalmente

        # Título
        ctk.CTkLabel(
            content_frame,
            text="Sobre o Projeto",
            font=("Arial", 28, "bold")
        ).pack(pady=(0, 20))

        # Descrição
        descricao = (
        "Este sistema de votação foi desenvolvido para o restaurante universitário, "
        "com o objetivo de modernizar e agilizar a coleta de feedback dos alunos "
        "sobre as refeições. Anteriormente, as avaliações eram feitas de forma manual, "
        "utilizando papéis coloridos em uma caixa. Agora, os alunos podem avaliar três "
        "tipos de proteínas (carne vermelha, carne branca e vegetariano) com três níveis "
        "de satisfação (ótimo, bom e ruim) de maneira digital e em tempo real. "
        "Essa automação traz mais eficiência, precisão e facilidade na análise dos dados, "
        "contribuindo para a melhoria contínua da qualidade das refeições."
        )

        ctk.CTkLabel(
        content_frame,
        text=descricao,
        font=("Arial", 18),
        justify="left",
        anchor="center",  
        wraplength=700 
        ).pack(pady=10)

        # Texto antes do link
        ctk.CTkLabel(
            content_frame,
            text="Acesse o repositório no GitHub para mais informações:",
            font=("Arial", 15, "bold")
        ).pack(pady=(20, 5))

        # Link clicável
        self.link = "https://github.com/CalebeCefas/Integrated-Project-I"

        ctk.CTkButton(
            content_frame,
            text=self.link,
            font=("Arial", 14, "underline"),
            fg_color="transparent",
            text_color="blue",
            hover=False,
            command=self.abrir_link
        ).pack()

    def abrir_link(self):
        webbrowser.open_new(self.link)
