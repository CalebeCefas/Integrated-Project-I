from datetime import time  # Para comparações com horários fixos
import serial  # Comunicação com Arduino via porta serial
import mysql.connector  # Acesso ao banco de dados MySQL
import customtkinter as ctk  # Biblioteca de interface gráfica personalizada baseada em Tkinter
import threading  # Para rodar leitura da serial em segundo plano
from datetime import datetime  # Para manipular datas e horários

# === Função para conectar ao banco de dados MySQL ===
def conectar_banco():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="root",
        database="ru"
    )

# Configurações da porta serial
porta_serial = 'COM3'
baud_rate = 9600
timeout = 1

# === Configuração da Janela Principal ===
janela = ctk.CTk()
janela.title("Avaliação da qualidade dos alimentos")
largura = janela.winfo_screenwidth()
altura = janela.winfo_screenheight()
janela.geometry(f"{800}x{600}")  # Tamanho fixo da janela

# === Criação da Sidebar ===
sidebar = ctk.CTkFrame(janela, width=200, corner_radius=0)
sidebar.pack(side="left", fill="y")

# === Área Principal ===
main_frame = ctk.CTkFrame(janela)
main_frame.pack(side="right", fill="both", expand=True)

# === Elementos da Sidebar ===
ctk.CTkLabel(sidebar, text="Menu", font=("Arial", 20, "bold")).pack(pady=20)

# Escolha de tema (claro ou escuro)
tema = ctk.CTkOptionMenu(sidebar, values=["Light", "Dark"], command=lambda escolha: ctk.set_appearance_mode(escolha))
tema.pack(pady=10)
tema.set("Dark")

# Botões do menu de navegação
ctk.CTkButton(sidebar, text="Votação", command=lambda: mostrar_pagina("Votação")).pack(pady=10, fill="x", padx=10)
ctk.CTkButton(sidebar, text="Pesquisa", command=lambda: mostrar_pagina("Pesquisa")).pack(pady=10, fill="x", padx=10)

# Dicionário para armazenar páginas carregadas
paginas = {}

# Label do horário global (atualizado dinamicamente)
label_horario = None

# === Função que atualiza o horário no canto superior da aba de votação ===
def atualizar_horario():
    agora = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
    label_horario.configure(text="Votação - " + agora)
    janela.after(1000, atualizar_horario)  # Atualiza a cada 1 segundo

# === Sistema de salvamento automático por horário ===
horarios_de_salvamento = ["13:40", "18:40"]
ultima_hora_salva = None  # Para evitar salvamentos duplicados no mesmo minuto

def verificar_horario_para_salvar():
    global ultima_hora_salva

    agora = datetime.now().strftime("%H:%M")

    if agora in horarios_de_salvamento and agora != ultima_hora_salva:
        print(f"[{agora}] Salvando dados no banco...")

        if ultima_linha_recebida:
            salvar_no_banco(ultima_linha_recebida.split(','))
            ultima_hora_salva = agora

    janela.after(60000, verificar_horario_para_salvar)  # Executa novamente em 60 segundos

# === Página de Votação ===
def construir_pagina_votacao(frame):
    global label_horario

    # Label do horário no topo
    label_horario = ctk.CTkLabel(frame, text="", font=("Arial", 18))
    label_horario.pack(pady=10)

    atualizar_horario()  # Começa a atualizar o horário

    # Frame principal onde os votos serão exibidos
    voto = ctk.CTkFrame(frame, width=500, height=400)
    voto.pack(expand=True, anchor="center", pady=20)

    # Textos informativos de cada tipo de refeição
    ctk.CTkLabel(voto, text="Carne \nVermelha:", font=("Arial", 12)).place(x=20, y=50)
    ctk.CTkLabel(voto, text="Carne \nBranca:", font=("Arial", 12)).place(x=20, y=165)
    ctk.CTkLabel(voto, text="Vegetariana:", font=("Arial", 12)).place(x=20, y=300)

    # Criação dos blocos de votos (ótimo, bom, ruim) para cada refeição
    # Segue o padrão: Frame colorido -> Número de votos -> Percentual
    # Frames e labels para cada avaliação e prato (ótimo, bom, ruim)
    # Carne Vermelha
    otimo_carne_vermelha = ctk.CTkFrame(voto, width=100, height=100, fg_color="#28a745")
    otimo_carne_vermelha.place(x=100, y=20)
    txt_otimo_carne_vermelha = ctk.CTkLabel(otimo_carne_vermelha, text="0", font=("Arial", 30, "bold"))
    txt_otimo_carne_vermelha.place(relx=0.5, rely=0.5, anchor="center")
    percentual_otimo_carne_vermelha = ctk.CTkLabel(otimo_carne_vermelha, text="0%", font=("Arial", 15))
    percentual_otimo_carne_vermelha.place(relx=0.5, rely=0.95, anchor="s")

    bom_carne_vermelha = ctk.CTkFrame(voto, width=100, height=100, fg_color="#FFCC00")
    bom_carne_vermelha.place(x=220, y=20)
    txt_bom_carne_vermelha = ctk.CTkLabel(bom_carne_vermelha, text="0", font=("Arial", 30, "bold"))
    txt_bom_carne_vermelha.place(relx=0.5, rely=0.5, anchor="center")
    percentual_bom_carne_vermelha = ctk.CTkLabel(bom_carne_vermelha, text="0%", font=("Arial", 15))
    percentual_bom_carne_vermelha.place(relx=0.5, rely=0.95, anchor="s")

    ruim_carne_vermelha = ctk.CTkFrame(voto, width=100, height=100, fg_color="#CC3333")
    ruim_carne_vermelha.place(x=340, y=20)
    txt_ruim_carne_vermelha = ctk.CTkLabel(ruim_carne_vermelha, text="0", font=("Arial", 30, "bold"))
    txt_ruim_carne_vermelha.place(relx=0.5, rely=0.5, anchor="center")
    percentual_ruim_carne_vermelha = ctk.CTkLabel(ruim_carne_vermelha, text="0%", font=("Arial", 15))
    percentual_ruim_carne_vermelha.place(relx=0.5, rely=0.95, anchor="s")

    # Carne Branca
    otimo_carne_branca = ctk.CTkFrame(voto, width=100, height=100, fg_color="#28a745")
    otimo_carne_branca.place(x=100, y=140)
    txt_otimo_carne_branca = ctk.CTkLabel(otimo_carne_branca, text="0", font=("Arial", 30, "bold"))
    txt_otimo_carne_branca.place(relx=0.5, rely=0.5, anchor="center")
    percentual_otimo_carne_branca = ctk.CTkLabel(otimo_carne_branca, text="0%", font=("Arial", 15))
    percentual_otimo_carne_branca.place(relx=0.5, rely=0.95, anchor="s")

    bom_carne_branca = ctk.CTkFrame(voto, width=100, height=100, fg_color="#FFCC00")
    bom_carne_branca.place(x=220, y=140)
    txt_bom_carne_branca = ctk.CTkLabel(bom_carne_branca, text="0", font=("Arial", 30, "bold"))
    txt_bom_carne_branca.place(relx=0.5, rely=0.5, anchor="center")
    percentual_bom_carne_branca = ctk.CTkLabel(bom_carne_branca, text="0%", font=("Arial", 15))
    percentual_bom_carne_branca.place(relx=0.5, rely=0.95, anchor="s")

    ruim_carne_branca = ctk.CTkFrame(voto, width=100, height=100, fg_color="#CC3333")
    ruim_carne_branca.place(x=340, y=140)
    txt_ruim_carne_branca = ctk.CTkLabel(ruim_carne_branca, text="0", font=("Arial", 30, "bold"))
    txt_ruim_carne_branca.place(relx=0.5, rely=0.5, anchor="center")
    percentual_ruim_carne_branca = ctk.CTkLabel(ruim_carne_branca, text="0%", font=("Arial", 15))
    percentual_ruim_carne_branca.place(relx=0.5, rely=0.95, anchor="s")

    # Vegetariano
    otimo_vegetariano = ctk.CTkFrame(voto, width=100, height=100, fg_color="#28a745")
    otimo_vegetariano.place(x=100, y=260)
    txt_otimo_vegetariano = ctk.CTkLabel(otimo_vegetariano, text="0", font=("Arial", 30, "bold"))
    txt_otimo_vegetariano.place(relx=0.5, rely=0.5, anchor="center")
    percentual_otimo_vegetariano = ctk.CTkLabel(otimo_vegetariano, text="0%", font=("Arial", 15))
    percentual_otimo_vegetariano.place(relx=0.5, rely=0.95, anchor="s")

    bom_vegetariano = ctk.CTkFrame(voto, width=100, height=100, fg_color="#FFCC00")
    bom_vegetariano.place(x=220, y=260)
    txt_bom_vegetariano = ctk.CTkLabel(bom_vegetariano, text="0", font=("Arial", 30, "bold"))
    txt_bom_vegetariano.place(relx=0.5, rely=0.5, anchor="center")
    percentual_bom_vegetariano = ctk.CTkLabel(bom_vegetariano, text="0%", font=("Arial", 15))
    percentual_bom_vegetariano.place(relx=0.5, rely=0.95, anchor="s")

    ruim_vegetariano = ctk.CTkFrame(voto, width=100, height=100, fg_color="#CC3333")
    ruim_vegetariano.place(x=340, y=260)
    txt_ruim_vegetariano = ctk.CTkLabel(ruim_vegetariano, text="0", font=("Arial", 30, "bold"))
    txt_ruim_vegetariano.place(relx=0.5, rely=0.5, anchor="center")
    percentual_ruim_vegetariano = ctk.CTkLabel(ruim_vegetariano, text="0%", font=("Arial", 15))
    percentual_ruim_vegetariano.place(relx=0.5, rely=0.95, anchor="s")

    # Label de total de votos
    label_total = ctk.CTkLabel(voto, text="Total de votos: 0", font=("Arial", 15, "bold"))
    label_total.place(relx=0.60, rely=0.98, anchor="sw")

    # Dicionários para armazenar os labels de contagem e percentual
    labels_qtd = {
        # mapeia os nomes que vêm da serial para os labels de quantidade
    }

    labels_percent = {
        # mapeia os nomes que vêm da serial para os labels de percentual
    }

    # === Processa dados recebidos via porta serial e atualiza os labels ===
    def processar_dados(linha):
        global ultima_linha_recebida
        ultima_linha_recebida = linha
        
        partes = linha.split(',')
        if len(partes) < 28:
            return

        for i in range(0, 27, 3):
            nome = partes[i]
            quantidade = partes[i + 1]
            percentual = partes[i + 2]
            if nome in labels_qtd and nome in labels_percent:
                labels_qtd[nome].configure(text=quantidade)
                labels_percent[nome].configure(text=f"{percentual}%")

        total = partes[-1]
        label_total.configure(text=f"Total de votos: {total}")
        salvar_no_banco(ultima_linha_recebida.split(','))

    # === Lê dados da porta serial em segundo plano ===
    def ler_serial():
        try:
            porta = serial.Serial(porta_serial, baud_rate, timeout=timeout)
            while True:
                linha = porta.readline().decode('utf-8', errors='ignore').strip()
                if linha:
                    processar_dados(linha)
        except serial.SerialException as e:
            print(f"Erro na serial: {e}")

    # Thread da leitura serial
    thread_serial = threading.Thread(target=ler_serial, daemon=True)
    thread_serial.start()

    # === Salva os dados no banco ===
    def salvar_no_banco(partes):
        try:
            conn = conectar_banco()
            cursor = conn.cursor()

            # Inicializa os dados
            dados = {
                "vegetariano_otimo": 0, "vegetariano_bom": 0, "vegetariano_ruim": 0,
                "carne_branca_otimo": 0, "carne_branca_bom": 0, "carne_branca_ruim": 0,
                "carne_vermelha_otimo": 0, "carne_vermelha_bom": 0, "carne_vermelha_ruim": 0,
                "total": 0
            }

            for i in range(0, 27, 3):
                nome = partes[i]
                qtd = int(partes[i + 1])
                if nome in dados:
                    dados[nome] = qtd

            dados["total"] = int(partes[-1])
            agora = datetime.now()

            # Query de insert e update
            query = """
                INSERT INTO avaliacoes 
                (DATA_HORA, VG_OTIMO, VG_BOM, VG_RUIM, CB_OTIMO, CB_BOM, CB_RUIM, CVM_OTIMO, CVM_BOM, CVM_RUIM, TOTAL) 
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            """
            query2 = """
                UPDATE avaliacoes SET
                DATA_HORA=%s, VG_OTIMO=%s, VG_BOM=%s, VG_RUIM=%s, CB_OTIMO=%s, CB_BOM=%s, CB_RUIM=%s, CVM_OTIMO=%s, CVM_BOM=%s, CVM_RUIM=%s, TOTAL=%s
                WHERE ID = %s
            """
            valores = (
                agora,
                dados["vegetariano_otimo"], dados["vegetariano_bom"], dados["vegetariano_ruim"],
                dados["carne_branca_otimo"], dados["carne_branca_bom"], dados["carne_branca_ruim"],
                dados["carne_vermelha_otimo"], dados["carne_vermelha_bom"], dados["carne_vermelha_ruim"],
                dados["total"]
            )

            # Lógica para decidir se deve atualizar ou inserir
            cursor.execute("SELECT DATA_HORA FROM avaliacoes")
            resultados = cursor.fetchall()
            for linha in resultados:
                data_hora = linha[0]
                dataA = data_hora.date()
                horaA = data_hora.time()
                h = datetime.now()
                cursor.execute("SELECT ID FROM avaliacoes WHERE DATA_HORA= %s", (data_hora,))
                resultado_id = cursor.fetchone()
                ID = resultado_id[0] if resultado_id else None

                if dataA == h.date() and time(10, 30) < horaA < time(13, 30):
                    valores_update = valores + (ID,)
                    cursor.execute(query2, valores_update)
                    break
                elif dataA == h.date() and time(15, 30) < horaA < time(18, 30):
                    valores_update = valores + (ID,)
                    cursor.execute(query2, valores_update)
                    break
                else:
                    cursor.execute(query, valores)
                    break

            conn.commit()
            cursor.close()
            conn.close()
            print("Dados salvos no banco.")
        except Exception as e:
            print("Erro ao salvar no banco:", e)

# === Página de Pesquisa de dados salvos ===
def construir_pagina_pesquisa(frame):
    ctk.CTkLabel(frame, text="Pesquisa", font=("Arial", 18)).pack(pady=10)

    frame_pesquisa = ctk.CTkFrame(frame)
    frame_pesquisa.pack(pady=10)

    entrada_data = ctk.CTkEntry(frame_pesquisa, placeholder_text="Data (DD-MM-AAAA)")
    entrada_data.pack(side="left", padx=10)

    botao_pesquisar = ctk.CTkButton(
        frame_pesquisa,
        text="Pesquisar",
        command=lambda: pesquisar_data(entrada_data.get())
    )
    botao_pesquisar.pack(side="left")

    resultado_pesquisa = ctk.CTkTextbox(frame, height=300, width=600)
    resultado_pesquisa.pack(pady=10)

    def pesquisar_data(data):
        try:
            data_convertida = datetime.strptime(data, "%d-%m-%Y").date()  # Converte para datetime.date
            conn = conectar_banco()
            cursor = conn.cursor()

            consulta = "SELECT * FROM avaliacoes WHERE DATE(DATA_HORA) = %s"
            cursor.execute(consulta, (data_convertida,))
            resultados = cursor.fetchall()

            resultado_pesquisa.delete("0.0", "end")

            if resultados:
                # Inicializa totais locais
                veg_otimo = veg_bom = veg_ruim = 0
                carne_branca_otimo = carne_branca_bom = carne_branca_ruim = 0
                carne_vermelha_otimo = carne_vermelha_bom = carne_vermelha_ruim = 0
                total = 0

                for linha in resultados:
                    veg_otimo += linha[2]
                    veg_bom += linha[3]
                    veg_ruim += linha[4]
                    carne_branca_otimo += linha[5]
                    carne_branca_bom += linha[6]
                    carne_branca_ruim += linha[7]
                    carne_vermelha_otimo += linha[8]
                    carne_vermelha_bom += linha[9]
                    carne_vermelha_ruim += linha[10]
                    total += linha[11]

                # Se quiser mostrar os totais finais:
                totais = f"""===== TOTAIS DO DIA =====
Vegetariano - Ótimo: {veg_otimo}, Bom: {veg_bom}, Ruim: {veg_ruim}
Carne Branca - Ótimo: {carne_branca_otimo}, Bom: {carne_branca_bom}, Ruim: {carne_branca_ruim}
Carne Vermelha - Ótimo: {carne_vermelha_otimo}, Bom: {carne_vermelha_bom}, Ruim: {carne_vermelha_ruim}
Total Geral de votos: {total}
======================

                            """
                resultado_pesquisa.insert("end", totais)

            else:
                resultado_pesquisa.insert("end", "Nenhum resultado encontrado.")

            cursor.close()
            conn.close()

        except ValueError:
            resultado_pesquisa.delete("0.0", "end")
            resultado_pesquisa.insert("end", "Data inválida. Use o formato DD-MM-AAAA.")
        except Exception as e:
            resultado_pesquisa.insert("end", f"Erro ao buscar dados: {e}")


# === Função para trocar entre páginas ===
def mostrar_pagina(nome):
    for pagina in paginas.values():
        pagina.pack_forget()

    if nome not in paginas:
        frame = ctk.CTkFrame(main_frame)
        frame.pack(fill="both", expand=True)
        paginas[nome] = frame

        if nome == "Votação":
            construir_pagina_votacao(frame)
        elif nome == "Pesquisa":
            construir_pagina_pesquisa(frame)
    else:
        paginas[nome].pack(fill="both", expand=True)

# === Início da interface ===
mostrar_pagina("Votação")

# salvamento por horário
verificar_horario_para_salvar()

# Roda o loop principal da interface
janela.mainloop()
