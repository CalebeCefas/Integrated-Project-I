import customtkinter as ctk
#Criação de janela 
janela = ctk.CTk()
janela.title("Avaliação da qualidade dos alimentos")
janela.geometry("700x600")
janela.minsize(width=700,height=600)
x=0.15

#Tema
tema = ctk.CTkOptionMenu(janela, values=["Light","Dark"],command=lambda escolha: ctk.set_appearance_mode(escolha))
tema.place(x=1,y=1)
tema.set("Dark")

#Votação 
vot= ctk.CTkFrame(janela, width= 500,height=400)
vot.pack(expand=True, anchor="center")

txt1= ctk.CTkLabel(vot,text="Carne \nvermelha:",font=("Arial",12))
txt1.place(x=20,y=50)
txt2= ctk.CTkLabel(vot,text="Carne \nbranca:",font=("Arial",12))
txt2.place(x=20,y=165)
txt3= ctk.CTkLabel(vot,text="Vegetariana:",font=("Arial",12))
txt3.place(x=20,y=300)
txt22= ctk.CTkLabel(vot,text=f"Total de votos: {x}",font=("Arial",15))
txt22.place(relx=0.65, rely=0.98, anchor="sw")

otimo1= ctk.CTkFrame(vot, width= 100,height=100,fg_color="#28a745",)
otimo1.place(x=100,y=20,)
#subistituir X
txt4= ctk.CTkLabel(otimo1,text=f"{x}",font=("Arial",30,"bold"))
txt4.place(relx=0.5, rely=0.5, anchor="center")
txt5= ctk.CTkLabel(otimo1,text=f"{x}%",font=("Arial",15))
txt5.place(relx=0.5, rely=0.95, anchor="s")

otimo2= ctk.CTkFrame(vot, width= 100,height=100,fg_color="#28a745")
otimo2.place(x=100,y=140)
txt6= ctk.CTkLabel(otimo2,text=f"{x}",font=("Arial",30,"bold"))
txt6.place(relx=0.5, rely=0.5, anchor="center")
txt7= ctk.CTkLabel(otimo2,text=f"{x}%",font=("Arial",15))
txt7.place(relx=0.5, rely=0.95, anchor="s")

otimo3= ctk.CTkFrame(vot, width= 100,height=100,fg_color="#28a745")
otimo3.place(x=100,y=260)
txt8= ctk.CTkLabel(otimo3,text=f"{x}",font=("Arial",30,"bold"))
txt8.place(relx=0.5, rely=0.5, anchor="center")
txt9= ctk.CTkLabel(otimo3,text=f"{x}%",font=("Arial",15))
txt9.place(relx=0.5, rely=0.95, anchor="s")

bom1= ctk.CTkFrame(vot, width= 100,height=100,fg_color="#FFCC00")
bom1.place(x=220,y=20)
txt10= ctk.CTkLabel(bom1,text=f"{x}",font=("Arial",30,"bold"))
txt10.place(relx=0.5, rely=0.5, anchor="center")
txt11= ctk.CTkLabel(bom1,text=f"{x}%",font=("Arial",15))
txt11.place(relx=0.5, rely=0.95, anchor="s")


bom2= ctk.CTkFrame(vot, width= 100,height=100,fg_color="#FFCC00")
bom2.place(x=220,y=140)
txt12= ctk.CTkLabel(bom2,text=f"{x}",font=("Arial",30,"bold"))
txt12.place(relx=0.5, rely=0.5, anchor="center")
txt13= ctk.CTkLabel(bom2,text=f"{x}%",font=("Arial",15))
txt13.place(relx=0.5, rely=0.95, anchor="s")

bom3= ctk.CTkFrame(vot, width= 100,height=100,fg_color="#FFCC00")
bom3.place(x=220,y=260)
txt14= ctk.CTkLabel(bom3,text=f"{x}",font=("Arial",30,"bold"))
txt14.place(relx=0.5, rely=0.5, anchor="center")
txt15= ctk.CTkLabel(bom3,text=f"{x}%",font=("Arial",15))
txt15.place(relx=0.5, rely=0.95, anchor="s")

Ruim1= ctk.CTkFrame(vot, width= 100,height=100,fg_color="#CC3333")
Ruim1.place(x=340,y=20)
txt16= ctk.CTkLabel(Ruim1,text=f"{x}",font=("Arial",30,"bold"))
txt16.place(relx=0.5, rely=0.5, anchor="center")
txt17= ctk.CTkLabel(Ruim1,text=f"{x}%",font=("Arial",15))
txt17.place(relx=0.5, rely=0.95, anchor="s")

Ruim2= ctk.CTkFrame(vot, width= 100,height=100,fg_color="#CC3333")
Ruim2.place(x=340,y=140)
txt18= ctk.CTkLabel(Ruim2,text=f"{x}",font=("Arial",30,"bold"))
txt18.place(relx=0.5, rely=0.5, anchor="center")
txt19= ctk.CTkLabel(Ruim2,text=f"{x}%",font=("Arial",15))
txt19.place(relx=0.5, rely=0.95, anchor="s")

Ruim3= ctk.CTkFrame(vot, width= 100,height=100,fg_color="#CC3333")
Ruim3.place(x=340,y=260)
txt20= ctk.CTkLabel(Ruim3,text=f"{x}",font=("Arial",30,"bold"))
txt20.place(relx=0.5, rely=0.5, anchor="center")
txt21= ctk.CTkLabel(Ruim3,text=f"{x}%",font=("Arial",15))
txt21.place(relx=0.5, rely=0.95, anchor="s")

janela.mainloop()