import tkinter as tk

def main():
    #fuentes titulos
    fuente_T= ("Arial", 30)

    ventana= tk.Tk()
    #tamano ventana
    ventana.geometry("1000x650")
    #color
    ventana.configure(bg="lightsteelblue4")

    #botones

    #rastreo
    boton_r= tk.Button(ventana, text= "Rastreo ■", padx=38,pady = 10)
    boton_r.place(x= 90, y =0)
    #envio
    boton_e= tk.Button(ventana, text= "Envio ■", padx=40,pady = 10)
    boton_e.place(x= 240, y =0)
    #agregar paquete
    boton_ap= tk.Button(ventana, text= "Agregar Paquete", padx=30,pady = 10)
    boton_ap.place(x= 560, y =500)
    #iniciar envio
    boton_ie= tk.Button(ventana, text= "Iniciar Envio", padx=40,pady = 10)
    boton_ie.place(x=750, y=500)


    #etiqueta agregar paquete
    etiqueta_ag= tk.Label(ventana, text = "AGREGAR PAQUETE", bg = "lightsteelblue4", font=fuente_T)
    etiqueta_ag.place(x=300, y= 60)

    #blank codigo postal
    texto_cp = tk.Entry(ventana, font = "Helvetica 19")
    texto_cp.place(x=575, y=440)
    #etiqueta codigo postal
    etiqueta_cp = tk.Label(ventana, font = "Arial 15",text="Codigo Postal", bg="lightsteelblue4")
    etiqueta_cp.place(x=575, y=410)

    #blank peso
    texto_peso = tk.Entry(ventana, font = "Helvetica 19")
    texto_peso.place(x=575, y=355)
    #etiqueta peso
    etiqueta_peso = tk.Label(ventana, font = "Arial 15",text="Peso", bg="lightsteelblue4")
    etiqueta_peso.place(x=575, y=325)

    #blank nombre
    texto_name = tk.Entry(ventana, font = "Helvetica 19")
    texto_name.place(x=575, y=270)
    #etiqueta nombre
    etiqueta_cp = tk.Label(ventana, font = "Arial 15",text="Nombre", bg="lightsteelblue4")
    etiqueta_cp.place(x=575, y=240)
    
    #inicio
    ventana.mainloop()
if __name__ == "__main__":
    main()