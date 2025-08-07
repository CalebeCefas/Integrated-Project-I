from datetime import datetime
import threading
import time
from tkinter import messagebox
import customtkinter as ctk

class Votting(ctk.CTkFrame):
    color = {
        'red': '#DC3545',
        'yellow':'#FFC107',
        'green': '#28a745'
    }

    # Usando as abreviações para padronizar com os dados do banco de dados
    PRATOS_ABBR = ["CVM", "CB", "VG"]
    AVALIACOES = ["otimo", "bom", "ruim"]

    # Nomes de exibição na GUI
    PRATOS_DISPLAY = ["Carne Vermelha", "Carne Branca", "Vegetariano"]
    AVALIACOES_DISPLAY = ['Ótimo', 'Bom', 'Ruim']

    def __init__(self, master, db_manager, serial_reader):
        super().__init__(master)
        self.db_manager = db_manager
        self.serial_reader = serial_reader
        
        # Título da tela de votação
        ctk.CTkLabel(self, text="Votação", font=("Arial", 18)).pack(pady=10)

        # Frame para o conteúdo da votação
        self.content_frame = ctk.CTkFrame(self, corner_radius=10)
        self.content_frame.pack(padx=20, pady=20, fill="both", expand=True)

        for i in range(len(self.AVALIACOES_DISPLAY)+1):
            self.content_frame.grid_columnconfigure(i, weight=1)
        for i in range(len(self.PRATOS_DISPLAY)+1):
            self.content_frame.grid_rowconfigure(i, weight=1)

        # Centralizar as Boxes na tela
        self.content_frame.grid_columnconfigure(0, weight=0)
        self.content_frame.grid_rowconfigure(0, weight=0)

        self.boxes = {}
        self.boxes_frames = {}

        # Informativos: Carne Vermelha, Carne ..., Ótimo, Bom, ...
        for j, avaliacao_display in enumerate(self.AVALIACOES_DISPLAY):
            ctk.CTkLabel(self.content_frame, text=avaliacao_display, font=("Arial", 14, "bold")).grid(row=0, column=j + 1, padx=5, pady=5, sticky="s")
        for i, prato_display in enumerate(self.PRATOS_DISPLAY):
            ctk.CTkLabel(self.content_frame, text=prato_display, font=("Arial", 14, "bold")).grid(row=i + 1, column=0, padx=5, pady=5, sticky="e")

        # Criação dos boxes e labels de título
        for i, prato_abbr in enumerate(self.PRATOS_ABBR):
            for j, avaliacao in enumerate(self.AVALIACOES):
                # Chave padronizada para busca e atualização
                key = (prato_abbr, avaliacao)
                color = self.color['green'] if avaliacao == 'otimo' else \
                        self.color['yellow'] if avaliacao == 'bom' else \
                        self.color['red']
            
                self.boxes_frames[(i, j)] = ctk.CTkFrame(self.content_frame, fg_color="transparent")
                self.boxes_frames[(i, j)].grid(row=i + 1, column=j + 1, padx=5, pady=5, sticky="nsew")
                self.boxes[key] = self._create_score_box(
                    master_frame=self.boxes_frames[(i, j)],
                    color=color
                )
        
        # Inicia a leitura do serial em uma thread separada para não travar a GUI
        self.serial_thread_running = True
        self.serial_thread = threading.Thread(target=self._read_serial_data_loop, daemon=True)
        self.serial_thread.start()

        # Atualiza os scores do DB na inicialização
        self.update_all_scores_from_db()

    # Método auxiliar privado para criar as caixas de score
    def _create_score_box(self, master_frame, color, initial_count="0", initial_percent="0%"):
        box_frame = ctk.CTkFrame(master_frame, width=200, height=200, fg_color=color, corner_radius=8)
        box_frame.pack(expand=True, fill="both")

        # Configura a responsividade interna do box_frame
        box_frame.grid_columnconfigure(0, weight=1)
        box_frame.grid_rowconfigure(0, weight=1) # Título
        box_frame.grid_rowconfigure(1, weight=3) # Contagem
        box_frame.grid_rowconfigure(2, weight=1) # Percentual

        count_label = ctk.CTkLabel(box_frame, text=initial_count, font=("Arial", 32, "bold"), anchor='center', text_color='black')
        count_label.grid(row=1, column=0, padx=2, pady=2, sticky="") 

        percent_label = ctk.CTkLabel(box_frame, text=initial_percent, font=("Arial", 15), text_color='black')
        percent_label.grid(row=2, column=0, padx=2, pady=(0, 2), sticky="n")
        
        return {
            'frame': box_frame,
            'count_label': count_label,
            'percent_label': percent_label
        }
    
    def _read_serial_data_loop(self):
        while self.serial_thread_running:
            if self.serial_reader and self.serial_reader.serial_connection and self.serial_reader.serial_connection.is_open:
                data = self.serial_reader.read_data()
                if data:
                    #print(f"Dados brutos recebidos do Arduino: {data}")
                    self.process_arduino_data(data)
                time.sleep(0.1)
            else:
                if self.serial_thread_running:
                    print("Aguardando conexão serial...")
                time.sleep(1)
        #print("Thread de leitura serial encerrada.")

    # votting.py
    def process_arduino_data(self, data):
        """Processa a string 'prato,avaliacao' recebida do Arduino."""
        if not self.db_manager or not self.db_manager.connection:
            #print("Voto não registrado: Banco de dados não conectado.")
            return

        try:
            prato, avaliacao = data.split(',')
            prato = prato.strip().upper()
            avaliacao = avaliacao.strip().lower()

            # Corrigido o nome da lista para validação
            if prato in self.PRATOS_ABBR and avaliacao in self.AVALIACOES:
                query = """
                    INSERT INTO registro (data, hora, ID_PRATO) 
                    VALUES (%s, %s, (SELECT ID FROM pratos WHERE prato = %s AND avaliacao = %s))
                """
                current_time = datetime.now()
                data_db = (current_time.date(), current_time.strftime('%H:%M:%S'), prato, avaliacao)
                
                if self.db_manager.execute_query(query, data_db):
                    #print(f"Voto '{prato}' - '{avaliacao}' registrado com sucesso.")
                    self.update_all_scores_from_db() # Atualiza a GUI
                else:
                    print("Falha ao registrar voto no DB.")
            else:
                print(f"Dados inválidos recebidos: {data}")
        except (ValueError, IndexError) as e:
            print(f"Erro ao analisar dados do Arduino: {e}. Dados recebidos: {data}")
        except Exception as e:
            print(f"Erro inesperado ao processar dados do Arduino: {e}")
    
    def update_all_scores_from_db(self):
        if not self.db_manager or not self.db_manager.connection:
            #print("Erro: Gerenciador do banco de dados não conectado.")
            return

        try:
            total_votos_query = """
                SELECT COUNT(ID) 
                FROM registro 
                WHERE data = CURDATE()
            """
            total_votos_hoje = self.db_manager.fetch_data(total_votos_query)
            total_votos_hoje = total_votos_hoje[0][0] if total_votos_hoje else 0

            votos_query = """
                SELECT p.prato, p.avaliacao, COUNT(r.ID) as quantidade
                FROM registro r
                JOIN pratos p ON r.ID_PRATO = p.ID
                WHERE r.data = CURDATE()
                GROUP BY p.prato, p.avaliacao;
            """
            votos_hoje = self.db_manager.fetch_data(votos_query)
            
            # Limpa todos os scores antes de atualizar
            for key in self.boxes:
                self.boxes[key]['count_label'].configure(text="0")
                self.boxes[key]['percent_label'].configure(text="0%")

            if votos_hoje:
                for prato, avaliacao, quantidade in votos_hoje:
                    # Chave padronizada para busca e atualização
                    key = (prato.strip().upper(), avaliacao.strip().lower())
                    if key in self.boxes:
                        self.boxes[key]['count_label'].configure(text=str(quantidade))
                        if total_votos_hoje > 0:
                            percent = (quantidade / total_votos_hoje) * 100
                            self.boxes[key]['percent_label'].configure(text=f"{percent:.1f}%")

        except Exception as e:
            messagebox.showerror("Erro de Banco de Dados", f"Erro ao atualizar scores: {e}")

    def stop_serial_thread(self):
        self.serial_thread_running = False
        #print("Sinal para encerrar a thread serial enviado.")

    def destroy(self):
        self.stop_serial_thread()
        super().destroy()