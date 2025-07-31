import customtkinter as ctk
from datetime import datetime, time
from core.db import DB

class Search(ctk.CTkFrame):
    def __init__(self, master, db_manager=None, serial_reader=None):
        super().__init__(master)
        self.db_manager = db_manager

        ctk.CTkLabel(self, text="Pesquisa", font=("Arial", 18)).pack(pady=10)

        # Cria a interface da pesquisa
        self.build_search_ui()

    def build_search_ui(self):
        ctk.CTkLabel(self, text="Pesquisa de Votos por Data", font=("Arial", 18, "bold")).pack(pady=10)

        frame_pesquisa = ctk.CTkFrame(self)
        frame_pesquisa.pack(pady=10)

        self.entrada_data = ctk.CTkEntry(frame_pesquisa, placeholder_text="Data (DD-MM-AAAA)")
        self.entrada_data.pack(side="left", padx=10)

        botao_pesquisar = ctk.CTkButton(frame_pesquisa, text="Pesquisar", command=self.pesquisar_data)
        botao_pesquisar.pack(side="left")

        self.resultado_pesquisa = ctk.CTkTextbox(self, height=300, width=600)
        self.resultado_pesquisa.pack(pady=10)

    def pesquisar_data(self):
        data = self.entrada_data.get()
        try:
            data_convertida = datetime.strptime(data, "%d-%m-%Y").date()

            # Usa a conexão do db_manager, se disponível
            if self.db_manager:
                conn = self.db_manager.connection
                cursor = conn.cursor()

                consulta = "SELECT * FROM avaliacoes WHERE DATE(DATA_HORA) = %s"
                cursor.execute(consulta, (data_convertida,))
                resultados = cursor.fetchall()

                self.resultado_pesquisa.delete("0.0", "end")

                if resultados:
                    almoco_inicio = time(11, 10)
                    almoco_fim = time(13, 20)
                    janta_inicio = time(16, 10)
                    janta_fim = time(19, 20)

                    totais = {
                        "almoço": {"veg": [0, 0, 0], "branca": [0, 0, 0], "vermelha": [0, 0, 0], "total": 0},
                        "janta": {"veg": [0, 0, 0], "branca": [0, 0, 0], "vermelha": [0, 0, 0], "total": 0}
                    }

                    for linha in resultados:
                        hora = linha[1].time()  # DATA_HORA é a coluna 1
                        periodo = None
                        if almoco_inicio <= hora <= almoco_fim:
                            periodo = "almoço"
                        elif janta_inicio <= hora <= janta_fim:
                            periodo = "janta"

                        if periodo:
                            totais[periodo]["veg"][0] += linha[2]
                            totais[periodo]["veg"][1] += linha[3]
                            totais[periodo]["veg"][2] += linha[4]
                            totais[periodo]["branca"][0] += linha[5]
                            totais[periodo]["branca"][1] += linha[6]
                            totais[periodo]["branca"][2] += linha[7]
                            totais[periodo]["vermelha"][0] += linha[8]
                            totais[periodo]["vermelha"][1] += linha[9]
                            totais[periodo]["vermelha"][2] += linha[10]
                            totais[periodo]["total"] += linha[11]

                    texto = ""
                    for periodo in ["almoço", "janta"]:
                        texto += f"===== TOTAIS DO {periodo.upper()} =====\n"
                        texto += f"Vegetariano - Ótimo: {totais[periodo]['veg'][0]}, Bom: {totais[periodo]['veg'][1]}, Ruim: {totais[periodo]['veg'][2]}\n"
                        texto += f"Carne Branca - Ótimo: {totais[periodo]['branca'][0]}, Bom: {totais[periodo]['branca'][1]}, Ruim: {totais[periodo]['branca'][2]}\n"
                        texto += f"Carne Vermelha - Ótimo: {totais[periodo]['vermelha'][0]}, Bom: {totais[periodo]['vermelha'][1]}, Ruim: {totais[periodo]['vermelha'][2]}\n"
                        texto += f"Total Geral de votos: {totais[periodo]['total']}\n"
                        texto += "======================\n\n"

                    self.resultado_pesquisa.insert("end", texto)
                else:
                    self.resultado_pesquisa.insert("end", "Nenhum resultado encontrado.")

                cursor.close()
            else:
                self.resultado_pesquisa.insert("end", "Banco de dados não conectado.")

        except ValueError:
            self.resultado_pesquisa.delete("0.0", "end")
            self.resultado_pesquisa.insert("end", "Data inválida. Use o formato DD-MM-AAAA.")
        except Exception as e:
            self.resultado_pesquisa.insert("end", f"Erro ao buscar dados: {e}")
