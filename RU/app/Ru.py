import serial

porta_serial = 'COM3'
baud_rate = 9600
timeout = 1

try:
    ser = serial.Serial(porta_serial, baud_rate, timeout=timeout)
    
    while True:
        linha = ser.readline().decode('utf-8', errors='ignore').strip()
        if linha:
            print("Arduino disse:", linha)

except serial.SerialException as e:
    print(f"Erro ao abrir a porta serial: {e}")

import customtkinter as ctk
import serial
import threading

# === Configuração da janela ===
janela = ctk.CTk()
janela.title("Avaliação da qualidade dos alimentos")
janela.geometry("700x600")
janela.minsize(width=700, height=600)

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

# Funções de navegação
def mostrar_pagina(nome):
    for widget in main_frame.winfo_children():
        widget.destroy()
    
    if nome == "Votação":
        # Cria o frame da votação DENTRO do main_frame
        voto = ctk.CTkFrame(main_frame, width=500, height=400)
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
                porta = serial.Serial('COM3', 9600, timeout=1)
                while True:
                    linha = porta.readline().decode('utf-8', errors='ignore').strip()
                    if linha:
                        processar_dados(linha)
            except serial.SerialException as e:
                print(f"Erro na serial: {e}")

        # Iniciar thread da serial como daemon para não travar a interface
        thread_serial = threading.Thread(target=ler_serial, daemon=True)
        thread_serial.start()

    elif nome == "Gráficos":
        ctk.CTkLabel(main_frame, text="Gráficos", font=("Arial", 18)).pack(pady=20)
    elif nome == "Relatórios":
        ctk.CTkLabel(main_frame, text="Relatórios", font=("Arial", 18)).pack(pady=20)


janela.mainloop()
