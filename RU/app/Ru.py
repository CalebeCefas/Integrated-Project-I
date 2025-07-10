import serial
import mysql.connector
import customtkinter as ctk
import threading
from datetime import datetime

def conectar_banco():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="root",
        database="ru"
    )

porta_serial = 'COM3'
baud_rate = 9600
timeout = 1

# === Configuração da janela ===
janela = ctk.CTk()
janela.title("Avaliação da qualidade dos alimentos")
largura = janela.winfo_screenwidth()
altura = janela.winfo_screenheight()
janela.geometry(f"{largura}x{altura}")

# Tema
tema = ctk.CTkOptionMenu(janela, values=["Light", "Dark"], command=lambda escolha: ctk.set_appearance_mode(escolha))
tema.place(x=20, y=10)
tema.set("Dark")

# Frame da sidebar
sidebar = ctk.CTkFrame(janela, width=200, corner_radius=0)
sidebar.pack(side="left", fill="y")

# Área principal
main_frame = ctk.CTkFrame(janela)
main_frame.pack(side="right", fill="both", expand=True)

ctk.CTkLabel(sidebar, text="Menu", font=("Arial", 20, "bold")).pack(pady=20)

ctk.CTkButton(sidebar, text="Votação", command=lambda: mostrar_pagina("Votação")).pack(pady=10, fill="x", padx=10)
ctk.CTkButton(sidebar, text="Gráficos", command=lambda: mostrar_pagina("Gráficos")).pack(pady=10, fill="x", padx=10)
ctk.CTkButton(sidebar, text="Relatórios", command=lambda: mostrar_pagina("Relatórios")).pack(pady=10, fill="x", padx=10)

paginas = {}

label_horario = None

def atualizar_horario():
    agora = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
    label_horario.configure(text="Votação - " + agora)
    janela.after(1000, atualizar_horario)

def construir_pagina_votacao(frame):
    global label_horario

    label_horario = ctk.CTkLabel(frame, text="", font=("Arial", 18))
    label_horario.pack(pady=10)

    atualizar_horario()
    
    voto = ctk.CTkFrame(frame, width=500, height=400)
    voto.pack(expand=True, anchor="center", pady=20)

    # Textos informativos
    ctk.CTkLabel(voto, text="Carne \nVermelha:", font=("Arial", 12)).place(x=20, y=50)
    ctk.CTkLabel(voto, text="Carne \nBranca:", font=("Arial", 12)).place(x=20, y=165)
    ctk.CTkLabel(voto, text="Vegetariana:", font=("Arial", 12)).place(x=20, y=300)

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

    # Label total de votos
    label_total = ctk.CTkLabel(voto, text="Total de votos: 0", font=("Arial", 15, "bold"))
    label_total.place(relx=0.60, rely=0.98, anchor="sw")

    # Mapear labels para facilitar atualização
    labels_qtd = {
        "carne_vermelha_otimo": txt_otimo_carne_vermelha,
        "carne_vermelha_bom": txt_bom_carne_vermelha,
        "carne_vermelha_ruim": txt_ruim_carne_vermelha,
        "carne_branca_otimo": txt_otimo_carne_branca,
        "carne_branca_bom": txt_bom_carne_branca,
        "carne_branca_ruim": txt_ruim_carne_branca,
        "vegetariano_otimo": txt_otimo_vegetariano,
        "vegetariano_bom": txt_bom_vegetariano,
        "vegetariano_ruim": txt_ruim_vegetariano,
    }

    labels_percent = {
        "carne_vermelha_otimo": percentual_otimo_carne_vermelha,
        "carne_vermelha_bom": percentual_bom_carne_vermelha,
        "carne_vermelha_ruim": percentual_ruim_carne_vermelha,
        "carne_branca_otimo": percentual_otimo_carne_branca,
        "carne_branca_bom": percentual_bom_carne_branca,
        "carne_branca_ruim": percentual_ruim_carne_branca,
        "vegetariano_otimo": percentual_otimo_vegetariano,
        "vegetariano_bom": percentual_bom_vegetariano,
        "vegetariano_ruim": percentual_ruim_vegetariano,
    }

    # Função para processar os dados recebidos do Arduino e atualizar labels
    def processar_dados(linha):
        partes = linha.split(',')
        if len(partes) < 28:  # 9 votos * 3 partes + 1 total
            return
        
        # Atualiza os labels com os dados
        for i in range(0, 27, 3):
            nome = partes[i]
            quantidade = partes[i + 1]
            percentual = partes[i + 2]

            if nome in labels_qtd and nome in labels_percent:
                labels_qtd[nome].configure(text=quantidade)
                labels_percent[nome].configure(text=f"{percentual}%")

        # Atualiza total de votos
        total = partes[-1]
        label_total.configure(text=f"Total de votos: {total}")

    # Função que roda em thread para ler a porta serial
    def ler_serial():
        try:
            porta = serial.Serial(porta_serial, baud_rate, timeout=timeout)
            while True:
                linha = porta.readline().decode('utf-8', errors='ignore').strip()
                if linha:
                    processar_dados(linha)
        except serial.SerialException as e:
            print(f"Erro na serial: {e}")

    # Iniciar thread da serial como daemon para não travar a interface
    thread_serial = threading.Thread(target=ler_serial, daemon=True)
    thread_serial.start()


    def salvar_no_banco(partes):
        try:
            conn = conectar_banco()
            cursor = conn.cursor()

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

            query = """
                INSERT INTO avaliacoes 
                (DATA_HORA, VG_OTIMO, VG_BOM, VG_RUIM, CB_OTIMO, CB_BOM, CB_RUIM, CVM_OTIMO, CVM_BOM, CVM_RUIM, TOTAL) 
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            """

            valores = (
                agora,
                dados["vegetariano_otimo"], dados["vegetariano_bom"], dados["vegetariano_ruim"],
                dados["carne_branca_otimo"], dados["carne_branca_bom"], dados["carne_branca_ruim"],
                dados["carne_vermelha_otimo"], dados["carne_vermelha_bom"], dados["carne_vermelha_ruim"],
                dados["total"]
            )

            cursor.execute(query, valores)
            conn.commit()
            cursor.close()
            conn.close()
            print("Dados salvos no banco.")
        except Exception as e:
            print("Erro ao salvar no banco:", e)



        # Função que roda em thread para ler a porta serial
        def ler_serial():
            try:
                porta = serial.Serial(porta_serial, baud_rate, timeout=timeout)
                while True:
                    linha = porta.readline().decode('utf-8', errors='ignore').strip()
                    if linha:
                        processar_dados(linha)
            except serial.SerialException as e:
                print(f"Erro na serial: {e}")

        # Iniciar thread da serial como daemon para não travar a interface
        thread_serial = threading.Thread(target=ler_serial, daemon=True)
        thread_serial.start()

        salvar_no_banco(partes)

def construir_pagina_graficos(frame):
    ctk.CTkLabel(frame, text="Gráficos", font=("Arial", 18)).pack(pady=10)

def construir_pagina_relatorios(frame):
    ctk.CTkLabel(frame, text="Relatórios", font=("Arial", 18)).pack(pady=10)

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
            # Converter de DD-MM-AAAA para AAAA-MM-DD
            data_convertida = datetime.strptime(data, "%d-%m-%Y").strftime("%Y-%m-%d")

            conn = conectar_banco()
            cursor = conn.cursor()

            consulta = """
                SELECT * FROM avaliacoes
                WHERE DATE(DATA_HORA) = %s
            """
            cursor.execute(consulta, (data_convertida,))
            resultados = cursor.fetchall()

            resultado_pesquisa.delete("0.0", "end")  # limpa o texto

            if resultados:
                for linha in resultados:
                    texto = f"""
    ID: {linha[0]}
    Data/Hora: {linha[1]}
    Vegetariano - Ótimo: {linha[2]}, Bom: {linha[4]}, Ruim: {linha[3]}
    Carne Branca - Ótimo: {linha[5]}, Bom: {linha[7]}, Ruim: {linha[6]}
    Carne Vermelha - Ótimo: {linha[8]}, Bom: {linha[10]}, Ruim: {linha[9]}
    Total de votos: {linha[11]}
    -------------------------
    """
                    resultado_pesquisa.insert("end", texto)
            else:
                resultado_pesquisa.insert("end", "Nenhum resultado encontrado.")
            
            cursor.close()
            conn.close()

        except ValueError:
            resultado_pesquisa.delete("0.0", "end")
            resultado_pesquisa.insert("end", "Data inválida. Use o formato DD-MM-AAAA.")
        except Exception as e:
            resultado_pesquisa.insert("end", f"Erro ao buscar dados: {e}")

# Funções de navegação
def mostrar_pagina(nome):
    for pagina in paginas.values():
        pagina.pack_forget()

    if nome not in paginas:
        frame = ctk.CTkFrame(main_frame)
        frame.pack(fill="both", expand=True)
        paginas[nome] = frame

        if nome == "Votação":
            construir_pagina_votacao(frame)
        elif nome == "Gráficos":
            construir_pagina_graficos(frame)
        elif nome == "Relatórios":
            construir_pagina_relatorios(frame)
    else:
        paginas[nome].pack(fill="both", expand=True)

mostrar_pagina("Votação")

janela.mainloop()
