import customtkinter as ctk
from datetime import datetime
from tkinter import messagebox

class Search(ctk.CTkFrame):
    def __init__(self, master, db_manager=None, serial_reader=None):
        super().__init__(master)
        self.db_manager = db_manager
        self.current_page = 0
        self.items_per_page = 15 # Aumentado para mostrar mais resumos

        ctk.CTkLabel(self, text="Resumo de Votos", font=("Arial", 18, "bold")).pack(pady=10)

        self.build_search_ui()
        self.load_data()

    def build_search_ui(self):
        # Frame para a barra de pesquisa
        frame_pesquisa = ctk.CTkFrame(self, fg_color="transparent")
        frame_pesquisa.pack(pady=10, padx=20, fill="x")

        self.entrada_data = ctk.CTkEntry(frame_pesquisa, placeholder_text="Filtrar por data (DD-MM-AAAA)")
        self.entrada_data.pack(side="left", padx=(0, 10), fill="x", expand=True)

        botao_pesquisar = ctk.CTkButton(frame_pesquisa, text="Filtrar", command=self.pesquisar_data)
        botao_pesquisar.pack(side="left")

        botao_limpar = ctk.CTkButton(frame_pesquisa, text="Limpar Filtro", command=self.limpar_pesquisa)
        botao_limpar.pack(side="left", padx=10)

        # Frame para exibir os resultados
        self.resultado_frame = ctk.CTkFrame(self)
        self.resultado_frame.pack(pady=10, padx=20, fill="both", expand=True)
        
        self.resultado_textbox = ctk.CTkTextbox(self.resultado_frame, height=300, width=600, font=("Courier New", 12))
        self.resultado_textbox.pack(pady=(0,10), fill="both", expand=True)

        # Frame para os botões de paginação
        pagination_frame = ctk.CTkFrame(self, fg_color="transparent")
        pagination_frame.pack(pady=10, padx=20, fill="x", side="bottom")

        self.prev_button = ctk.CTkButton(pagination_frame, text="Anterior", command=self.prev_page)
        self.prev_button.pack(side="left")
        
        self.page_label = ctk.CTkLabel(pagination_frame, text=f"Página {self.current_page + 1}")
        self.page_label.pack(side="left", padx=20)

        self.next_button = ctk.CTkButton(pagination_frame, text="Próximo", command=self.next_page)
        self.next_button.pack(side="left")

    def load_data(self, data_filtro=None):
        if not self.db_manager or not self.db_manager.connection:
            self.resultado_textbox.delete("1.0", "end")
            self.resultado_textbox.insert("end", "Banco de dados não conectado.")
            return

        try:
            cursor = self.db_manager.connection.cursor()
            
            # Query para agrupar e contar os votos
            query = """
                SELECT 
                    r.data AS dia,
                    CASE 
                        WHEN r.hora BETWEEN '11:00:00' AND '13:30:00' THEN 'Almoço'
                        ELSE 'Janta'
                    END AS periodo,
                    p.prato,
                    p.avaliacao,
                    COUNT(r.ID) AS quantidade
                FROM 
                    registro AS r
                JOIN 
                    pratos AS p ON r.ID_PRATO = p.ID
            """
            params = []
            
            if data_filtro:
                query += " WHERE r.data = %s"
                params.append(data_filtro)

            query += """
                GROUP BY dia, periodo, p.prato, p.avaliacao
                ORDER BY dia DESC, periodo DESC, p.prato, p.avaliacao
                LIMIT %s OFFSET %s
            """
            offset = self.current_page * self.items_per_page
            params.extend([self.items_per_page, offset])
            
            cursor.execute(query, tuple(params))
            resultados = cursor.fetchall()
            
            self.resultado_textbox.delete("1.0", "end")
            if not resultados:
                self.resultado_textbox.insert("end", "Nenhum resultado encontrado para o filtro aplicado.")
                self.next_button.configure(state="disabled")
            else:
                # Cabeçalho da tabela
                header = f"{'Data':<12}{'Período':<10}{'Prato':<15}{'Avaliação':<10}{'Votos'}\n"
                header += "="*55 + "\n"
                self.resultado_textbox.insert("end", header)
                
                # Mapa para nomes mais amigáveis
                prato_map = {'CVM': 'C. Vermelha', 'CB': 'C. Branca', 'VG': 'Vegetariano'}
                
                # Exibição dos dados
                for dia, periodo, prato, avaliacao, quantidade in resultados:
                    prato_formatado = prato_map.get(prato, prato)
                    linha = f"{str(dia):<12}{periodo:<10}{prato_formatado:<15}{avaliacao:<10}{quantidade}\n"
                    self.resultado_textbox.insert("end", linha)
                
                self.next_button.configure(state="normal")

            self.prev_button.configure(state="normal" if self.current_page > 0 else "disabled")
            self.page_label.configure(text=f"Página {self.current_page + 1}")
            
            cursor.close()

        except Exception as e:
            messagebox.showerror("Erro de Banco de Dados", f"Erro ao buscar dados: {e}")

    def pesquisar_data(self):
        data_str = self.entrada_data.get()
        if not data_str:
            self.limpar_pesquisa()
            return
            
        try:
            data_convertida = datetime.strptime(data_str, "%d-%m-%Y").date()
            self.current_page = 0
            self.load_data(data_filtro=data_convertida)
        except ValueError:
            messagebox.showerror("Formato Inválido", "Data inválida. Use o formato DD-MM-AAAA.")

    def limpar_pesquisa(self):
        self.entrada_data.delete(0, 'end')
        self.current_page = 0
        self.load_data()

    def next_page(self):
        self.current_page += 1
        self.load_data(data_filtro=self._get_filtro_data())

    def prev_page(self):
        if self.current_page > 0:
            self.current_page -= 1
            self.load_data(data_filtro=self._get_filtro_data())
            
    def _get_filtro_data(self):
        data_str = self.entrada_data.get()
        if not data_str:
            return None
        try:
            return datetime.strptime(data_str, "%d-%m-%Y").date()
        except ValueError:
            return None