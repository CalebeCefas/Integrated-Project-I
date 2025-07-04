import customtkinter as ctk

#Criação de janela 
janela =  ctk.CTk()
janela.title("Avaliação da qualidade dos alimentos")
janela.geometry("700x600")
janela.minsize(width = 700, height = 600)

x = 0.15

#Tema
tema = ctk.CTkOptionMenu(janela, values = ["Light", "Dark"], command = lambda escolha: ctk.set_appearance_mode(escolha))
tema.place(x = 20, y = 10)
tema.set("Dark")

#frame da Votação 
voto = ctk.CTkFrame(janela, width = 500, height = 400)
voto.pack(expand = True, anchor = "center")

#Textos Informativos
ctk.CTkLabel(voto, text = "Carne \nVermelha:", font = ("Arial", 12)).place(x = 20, y = 50)
ctk.CTkLabel(voto, text = "Carne \nBranca:", font = ("Arial", 12)).place(x = 20, y = 165)
ctk.CTkLabel(voto, text = "Vegetariana:", font = ("Arial", 12)).place(x = 20, y = 300)
ctk.CTkLabel(voto, text = f"Total de votos: {x}", font = ("Arial", 15)).place(relx = 0.60, rely = 0.98, anchor = "sw")

#votos otimos de carne vermelha com percentual
otimo_carne_vermelha = ctk.CTkFrame(voto, width = 100, height = 100, fg_color = "#28a745", )
otimo_carne_vermelha.place(x = 100, y = 20, )
#subistituir X
txt_otimo_carne_vermelha = ctk.CTkLabel(otimo_carne_vermelha, text = f"{x}", font = ("Arial", 30, "bold"))
txt_otimo_carne_vermelha.place(relx = 0.5, rely = 0.5, anchor = "center")
percentual_otimo_carne_vermelha = ctk.CTkLabel(otimo_carne_vermelha, text = f"{x}%", font = ("Arial", 15))
percentual_otimo_carne_vermelha.place(relx = 0.5, rely = 0.95, anchor = "s")

#votos otimos de carne branca com percentual
otimo_carne_branca = ctk.CTkFrame(voto, width = 100, height = 100, fg_color = "#28a745")
otimo_carne_branca.place(x = 100, y = 140)
txt_otimo_carne_branca = ctk.CTkLabel(otimo_carne_branca, text = f"{x}", font = ("Arial", 30, "bold"))
txt_otimo_carne_branca.place(relx = 0.5, rely = 0.5, anchor = "center")
percentual_otimo_carne_branca = ctk.CTkLabel(otimo_carne_branca, text = f"{x}%", font = ("Arial", 15))
percentual_otimo_carne_branca.place(relx = 0.5, rely = 0.95, anchor = "s")

#votos otimos de vegetariano com percentual
otimo_vegetariano = ctk.CTkFrame(voto, width = 100, height = 100, fg_color = "#28a745")
otimo_vegetariano.place(x = 100, y = 260)
txt_otimo_vegetariano = ctk.CTkLabel(otimo_vegetariano, text = f"{x}", font = ("Arial", 30, "bold"))
txt_otimo_vegetariano.place(relx = 0.5, rely = 0.5, anchor = "center")
percentual_otimo_vegetariano = ctk.CTkLabel(otimo_vegetariano, text = f"{x}%", font = ("Arial", 15))
percentual_otimo_vegetariano.place(relx = 0.5, rely = 0.95, anchor = "s")

#votos bom de carne vermelha com percentual
bom_carne_vermelha = ctk.CTkFrame(voto, width = 100, height = 100, fg_color = "#FFCC00")
bom_carne_vermelha.place(x = 220, y = 20)
txt_bom_carne_vermelha = ctk.CTkLabel(bom_carne_vermelha, text = f"{x}", font = ("Arial", 30, "bold"))
txt_bom_carne_vermelha.place(relx = 0.5, rely = 0.5, anchor = "center")
percentual_bom_carne_vermelha = ctk.CTkLabel(bom_carne_vermelha, text = f"{x}%", font = ("Arial", 15))
percentual_bom_carne_vermelha.place(relx = 0.5, rely = 0.95, anchor = "s")

#votos bom de carne branca com percentual
bom_carne_branca = ctk.CTkFrame(voto, width = 100, height = 100, fg_color = "#FFCC00")
bom_carne_branca.place(x = 220, y = 140)
txt_bom_carne_branca = ctk.CTkLabel(bom_carne_branca, text = f"{x}", font = ("Arial", 30, "bold"))
txt_bom_carne_branca.place(relx = 0.5, rely = 0.5, anchor = "center")
percentual_bom_carne_branca = ctk.CTkLabel(bom_carne_branca, text = f"{x}%", font = ("Arial", 15))
percentual_bom_carne_branca.place(relx = 0.5, rely = 0.95, anchor = "s")

#votos bom de vegetariano com percentual
bom_vegetariano = ctk.CTkFrame(voto, width = 100, height = 100, fg_color = "#FFCC00")
bom_vegetariano.place(x = 220, y = 260)
txt_otimo_vegetariano = ctk.CTkLabel(bom_vegetariano, text = f"{x}", font = ("Arial", 30, "bold"))
txt_otimo_vegetariano.place(relx = 0.5, rely = 0.5, anchor = "center")
percentual_bom_vegetariano = ctk.CTkLabel(bom_vegetariano, text = f"{x}%", font = ("Arial", 15))
percentual_bom_vegetariano.place(relx = 0.5, rely = 0.95, anchor = "s")

#votos ruim de carne vermelha com percentual
ruim_carne_vermelha = ctk.CTkFrame(voto, width = 100, height = 100, fg_color = "#CC3333")
ruim_carne_vermelha.place(x = 340, y = 20)
txt_ruim_carne_vermelha = ctk.CTkLabel(ruim_carne_vermelha, text = f"{x}", font = ("Arial", 30, "bold"))
txt_ruim_carne_vermelha.place(relx = 0.5, rely = 0.5, anchor = "center")
percentual_ruim_carne_vermelha = ctk.CTkLabel(ruim_carne_vermelha, text = f"{x}%", font = ("Arial", 15))
percentual_ruim_carne_vermelha.place(relx = 0.5, rely = 0.95, anchor = "s")

#votos ruim de carne branca com percentual
ruim_carne_branca = ctk.CTkFrame(voto, width = 100, height = 100, fg_color = "#CC3333")
ruim_carne_branca.place(x = 340, y = 140)
txt_ruim_carne_branca = ctk.CTkLabel(ruim_carne_branca, text = f"{x}", font = ("Arial", 30, "bold"))
txt_ruim_carne_branca.place(relx = 0.5, rely = 0.5, anchor = "center")
percentual_ruim_carne_branca = ctk.CTkLabel(ruim_carne_branca, text = f"{x}%", font = ("Arial", 15))
percentual_ruim_carne_branca.place(relx = 0.5, rely = 0.95, anchor = "s")

#votos ruim de vegetariano com percentual
ruim_vegetariano = ctk.CTkFrame(voto, width = 100, height = 100, fg_color = "#CC3333")
ruim_vegetariano.place(x = 340, y = 260)
txt_ruim_vegetariano = ctk.CTkLabel(ruim_vegetariano, text = f"{x}", font = ("Arial", 30, "bold"))
txt_ruim_vegetariano.place(relx = 0.5, rely = 0.5, anchor = "center")
percentual_ruim_vegetariano = ctk.CTkLabel(ruim_vegetariano, text = f"{x}%", font = ("Arial", 15))
percentual_ruim_vegetariano.place(relx = 0.5, rely = 0.95, anchor = "s")

janela.mainloop()