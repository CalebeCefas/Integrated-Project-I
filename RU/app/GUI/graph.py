import customtkinter as ctk

# Importando bibliotecas de gráficos
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.dates as mdates

class Graph(ctk.CTkFrame):
    def __init__(self, master, db_manager, serial_reader=None):
        super().__init__(master)
        self.db_manager = db_manager

        # ---- Estrutura do Gráfico ----
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)

        # Frame para título e o botão
        top_frame = ctk.CTkFrame(self, fg_color="transparent")
        top_frame.grid(row=0, column=0, padx=20, pady=10, sticky="ew")
        
        ctk.CTkLabel(top_frame, text="Gráficos", font=("Arial", 18)).pack(side="left")

        self.reload_button = ctk.CTkButton(top_frame, text="Recarregar")
        self.reload_button.pack(side="right")

        self.graph_frame = ctk.CTkFrame(self)
        self.graph_frame.grid(row=1, column=0, padx=20, pady=10, sticky="nsew")

    def _featch_and_process_data(self):
        pass

    def construir_graficos(self):
        """Função principal que orquestra a limpeza, busca de dados e plotagem dos gráficos."""
        # Limpa o frame de gráficos antes de desenhar
        for widget in self.graph_frame.winfo_children():
            widget.destroy()

        dados_por_dia, datas_eixo_x = self._fetch_and_process_data()

        # Se não houver dados, exibe uma mensagem
        if not dados_por_dia:
            ctk.CTkLabel(self.graph_frame, text="Nenhum dado de votação encontrado nos últimos 7 dias.", font=("Arial", 16)).pack(expand=True)
            return

        # Mapas para legendas, títulos e cores
        pratos_map = {"carne_vermelha": "Carne Vermelha", "carne_branca": "Carne Branca", "vegetariano": "Vegetariano"}
        avaliacoes_map = {"otimo": "Ótimo", "bom": "Bom", "ruim": "Ruim"}

        # Cria um canvas rolável para conter os gráficos
        canvas = ctk.CTkCanvas(self.graph_frame, highlightthickness=0)
        scrollbar = ctk.CTkScrollbar(self.graph_frame, command=canvas.yview)
        frame_interno = ctk.CTkFrame(canvas)

        frame_interno.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
        canvas.create_window((0, 0), window=frame_interno, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
        # Função auxiliar para extrair os dados para plotagem
        def extrair_votos(prato, avaliacao):
            return [dados_por_dia.get(data, {}).get(prato, {}).get(avaliacao, 0) for data in datas_eixo_x]

        # Loop para criar um gráfico para cada tipo de avaliação (Ótimo, Bom, Ruim)
        for avaliacao_key, avaliacao_titulo in avaliacoes_map.items():
            fig, ax = plt.subplots(figsize=(10, 5))
            
            # Para cada prato, desenha uma linha no gráfico
            for prato_key, prato_legenda in pratos_map.items():
                ax.plot(datas_eixo_x, extrair_votos(prato_key, avaliacao_key), label=prato_legenda, marker='o')

            ax.set_title(f"Votos '{avaliacao_titulo}' - Últimos 7 Dias", fontsize=16)
            ax.set_xlabel("Data", fontsize=12)
            ax.set_ylabel("Quantidade de Votos", fontsize=12)
            ax.legend()
            ax.grid(True, linestyle='--', alpha=0.6)
            
            # Formata o eixo X para exibir as datas de forma clara
            ax.xaxis.set_major_formatter(mdates.dates.DateFormatter('%d/%m'))
            ax.xaxis.set_major_locator(mdates.DayLocator())
            fig.autofmt_xdate() # Rotaciona as datas para evitar sobreposição

            # Adiciona o gráfico do Matplotlib ao frame interno do CustomTkinter
            canvas_fig = FigureCanvasTkAgg(fig, master=frame_interno)
            canvas_fig.draw()
            canvas_fig.get_tk_widget().pack(pady=15, padx=10, fill="both", expand=True)

            # É importante fechar a figura para liberar memória
            plt.close(fig)