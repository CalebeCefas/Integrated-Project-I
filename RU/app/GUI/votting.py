import threading
import time
import customtkinter as ctk

class Votting(ctk.CTkFrame):
    collor = {
        'red': '#CC3333',
        'yellow':'#FFCC00',
        'green': '#28a745'
    }

    # Dados que vem do Arduno
    PRATOS = ["carne vermelha", "carne branca", "vegetariano"]
    AVALIACOES =["otimo", "bom", "ruim"]

    # Nomes de exibição na GUI
    PRATOS_DISPLAY=["Carne Vermelha", "Carne Branca", "Vegetariano"]
    AVALIACOES_DISPLAY=['Ótimo', 'Bom', ' Ruim']

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

        self.boxes={}
        self.boxes_frames={}

        # Informativos: Carne Vermelha, Carne ..., Ótimo, Bom, ...
        for j, avaliacao_display in enumerate(self.AVALIACOES_DISPLAY):
            ctk.CTkLabel(self.content_frame, text=avaliacao_display, font=("Arial", 14, "bold")).grid(row=0, column=j + 1, padx=5, pady=5, sticky="s")
        for i, prato_display in enumerate(self.PRATOS_DISPLAY):
            ctk.CTkLabel(self.content_frame, text=prato_display, font=("Arial", 14, "bold")).grid(row=i + 1, column=0, padx=5, pady=5, sticky="e")

        # Criação dos boxes e labels de título
        for i, prato in enumerate(self.PRATOS):
            for j, avaliacao in enumerate(self.AVALIACOES):
                key = f"{prato.replace(' ', '_')}_{avaliacao}"
                color = self.collor['green'] if avaliacao == 'otimo' else \
                        self.collor['yellow'] if avaliacao == 'bom' else \
                        self.collor['red']
            
                self.boxes_frames[(i,j)] = ctk.CTkFrame(self.content_frame, fg_color="transparent")
                self.boxes_frames[(i, j)].grid(row=i + 1, column=j + 1, padx=5, pady=5, sticky="nsew")
                self.boxes[(i, j)] = self._create_score_box(
                    master_frame=self.boxes_frames[(i, j)],
                    color=color
                )
        
        # Inicia a leitura do serial em uma thread separada para não travar a GUI
        self.serial_thread = threading.Thread(target=self._read_serial_data_loop, daemon=True)
        self.serial_thread_running = True
        self.serial_thread.start()

        # Atualiza os scores do DB na inicialização
        ######## self.update_all_score_from_db()

     # Método auxiliar privado para criar as caixas de score
    def _create_score_box(self, master_frame, color, initial_count="0", initial_percent="0%"):
        box_frame = ctk.CTkFrame(master_frame, width=200, height=200, fg_color=color, corner_radius=8)
        box_frame.pack(expand=True, fill="both")

        # Configura a responsividade interna do box_frame
        box_frame.grid_columnconfigure(0, weight=1)
        box_frame.grid_rowconfigure(0, weight=1) # Título
        box_frame.grid_rowconfigure(1, weight=3) # Contagem
        box_frame.grid_rowconfigure(2, weight=1) # Percentual

        count_label = ctk.CTkLabel(box_frame, text=initial_count, font=("Arial", 18, "bold"))
        count_label.grid(row=1, column=0, padx=2, pady=2, sticky="") 

        percent_label = ctk.CTkLabel(box_frame, text=initial_percent, font=("Arial", 10))
        percent_label.grid(row=2, column=0, padx=2, pady=(0,2), sticky="n")
        
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
                    print(f"Dados brutos recebidos do Arduino: {data}")
                    self.process_arduino_data(data)
                time.sleep(0.1)
            else:
                print("Aguardando conexão serial...")
                time.sleep(1)
        print("Thread de leitura serial encerrada.")

    def process_arduino_data(self, data):
        """Processa a string recebida do Arduino e atualiza o DB e a GUI."""
        print("Dados Salvos....")
    
    def update_all_scores_from_db(self):
        pass

    def destroy(self):
        self.serial_thread_running = False
        super().destroy()