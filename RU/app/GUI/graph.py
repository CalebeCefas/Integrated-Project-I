import customtkinter as ctk
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.dates as mdates
from datetime import datetime, timedelta

class Graph(ctk.CTkFrame):
    def __init__(self, master, db_manager, serial_reader=None):
        super().__init__(master)
        self.db_manager = db_manager

        # ---- Estrutura da UI ----
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)

        top_frame = ctk.CTkFrame(self, fg_color="transparent")
        top_frame.grid(row=0, column=0, padx=20, pady=10, sticky="ew")
        
        ctk.CTkLabel(top_frame, text="Gráficos de Votos (Últimos 7 Dias)", font=("Arial", 18, "bold")).pack(side="left")

        self.reload_button = ctk.CTkButton(top_frame, text="Recarregar", command=self.construir_graficos)
        self.reload_button.pack(side="right")

        self.graph_frame = ctk.CTkFrame(self)
        self.graph_frame.grid(row=1, column=0, padx=20, pady=10, sticky="nsew")

        # Chama a construção dos gráficos na inicialização
        self.construir_graficos()

    def _fetch_and_process_data(self):
        """
        Busca os dados dos últimos 7 dias no banco e os processa
        para o formato necessário para os gráficos.
        """
        if not self.db_manager or not self.db_manager.connection:
            #print("Gráficos: Banco de dados não conectado.")
            return {}, []

        dados_por_dia = {}
        # Gera a lista dos últimos 7 dias para o eixo X do gráfico
        datas_eixo_x = [(datetime.now() - timedelta(days=i)).date() for i in range(6, -1, -1)]
        
        try:
            cursor = self.db_manager.connection.cursor()
            
            # Query para buscar os dados agrupados por dia, prato e avaliação
            query = """
                SELECT 
                    r.data,
                    p.prato,
                    p.avaliacao,
                    COUNT(r.ID) AS quantidade
                FROM 
                    registro AS r
                JOIN 
                    pratos AS p ON r.ID_PRATO = p.ID
                WHERE 
                    r.data >= %s
                GROUP BY 
                    r.data, p.prato, p.avaliacao
                ORDER BY 
                    r.data;
            """
            data_inicio = (datetime.now() - timedelta(days=6)).date()
            cursor.execute(query, (data_inicio,))
            resultados = cursor.fetchall()
            
            # Organiza os resultados em um dicionário para fácil acesso
            for data, prato, avaliacao, quantidade in resultados:
                if data not in dados_por_dia:
                    dados_por_dia[data] = {}
                if prato not in dados_por_dia[data]:
                    dados_por_dia[data][prato] = {}
                dados_por_dia[data][prato][avaliacao.lower()] = quantidade
            
            cursor.close()
            return dados_por_dia, datas_eixo_x
            
        except Exception as e:
            #print(f"Erro ao buscar dados para os gráficos: {e}")
            return {}, []

    def construir_graficos(self):
        """Função principal que orquestra a limpeza, busca e plotagem dos gráficos."""
        # Limpa o frame de gráficos antes de redesenhar
        for widget in self.graph_frame.winfo_children():
            widget.destroy()

        dados_por_dia, datas_eixo_x = self._fetch_and_process_data()

        if not dados_por_dia:
            ctk.CTkLabel(self.graph_frame, text="Nenhum dado de votação encontrado nos últimos 7 dias.", font=("Arial", 16)).pack(expand=True)
            return

        # Mapas para legendas e títulos
        pratos_map = {"CVM": "C. Vermelha", "CB": "C. Branca", "VG": "Vegetariano"}
        avaliacoes_map = {"otimo": "Ótimo", "bom": "Bom", "ruim": "Ruim"}

        # Cria um canvas rolável
        canvas = ctk.CTkScrollableFrame(self.graph_frame, label_text="Resultados")
        canvas.pack(side="left", fill="both", expand=True)

        # Função auxiliar para extrair os dados para plotagem
        def extrair_votos(prato, avaliacao):
            return [dados_por_dia.get(data, {}).get(prato, {}).get(avaliacao, 0) for data in datas_eixo_x]

        # Loop para criar um gráfico para cada tipo de avaliação (Ótimo, Bom, Ruim)
        for avaliacao_key, avaliacao_titulo in avaliacoes_map.items():
            fig, ax = plt.subplots(figsize=(10, 4))
            
            for prato_key, prato_legenda in pratos_map.items():
                ax.plot(datas_eixo_x, extrair_votos(prato_key, avaliacao_key), label=prato_legenda, marker='o')

            ax.set_title(f"Votos '{avaliacao_titulo}' - Últimos 7 Dias", fontsize=14)
            ax.set_ylabel("Quantidade de Votos", fontsize=10)
            ax.legend()
            ax.grid(True, linestyle='--', alpha=0.6)
            
            ax.xaxis.set_major_formatter(mdates.DateFormatter('%d/%m'))
            ax.xaxis.set_major_locator(mdates.DayLocator())
            plt.setp(ax.get_xticklabels(), rotation=30, ha='right')
            fig.tight_layout()

            # Adiciona o gráfico ao frame rolável
            canvas_fig = FigureCanvasTkAgg(fig, master=canvas)
            canvas_fig.draw()
            canvas_fig.get_tk_widget().pack(pady=10, padx=10, fill="x", expand=True)
            plt.close(fig)