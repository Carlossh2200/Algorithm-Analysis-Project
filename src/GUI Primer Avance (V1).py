import tkinter as tk
from tkinter import messagebox

class VentanaPrincipal(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title("Ventana Principal")
        self.geometry("1500x650")
        self.configure(bg="lightsteelblue4")

        self.numero_paquete = 1  # Inicializar contador de paquetes

        # Blank nombre
        self.texto_name = tk.Entry(self, font="Helvetica 19")
        self.texto_name.place(x=850, y=270)

        # Blank peso
        self.texto_peso = tk.Entry(self, font="Helvetica 19")
        self.texto_peso.place(x=850, y=355)

        # Blank codigo postal
        self.texto_cp = tk.Entry(self, font="Helvetica 19")
        self.texto_cp.place(x=850, y=449)

        # Título "Agregar paquetes"
        titulo_agregar_paquetes = tk.Label(self, font="Arial 40 bold", text="Agregar Paquetes", bg="lightsteelblue4", fg="white")
        titulo_agregar_paquetes.place(x=780, y=130)

        # Etiqueta nombre
        etiqueta_nombre = tk.Label(self, font="Arial 20", text="Nombre", bg="lightsteelblue4")
        etiqueta_nombre.place(x=940, y=230)

        # Etiqueta peso
        etiqueta_peso = tk.Label(self, font="Arial 20", text="Peso", bg="lightsteelblue4")
        etiqueta_peso.place(x=955, y=315)

        # Etiqueta codigo postal
        etiqueta_cp = tk.Label(self, font="Arial 20", text="Codigo Postal", bg="lightsteelblue4")
        etiqueta_cp.place(x=905, y=405)

        # Boton agregar paquete
        boton_ap = tk.Button(self, text="Agregar Paquete", padx=394, pady=5, command=self.obtener_datos, bg="light green", fg="black")
        boton_ap.place(x=575, y=500)

        # Boton eliminar paquete
        boton_eliminar = tk.Button(self, text="Eliminar Paquete", padx=16, pady=5, command=self.abrir_ventana_eliminar, bg="orange", fg="black")
        boton_eliminar.place(x=1330, y=545)

        # Boton salir
        boton_salir = tk.Button(self, text="Salir del Pograma", padx=15, pady=5, command=self.salir_programa, bg="red", fg="white")
        boton_salir.place(x=1330, y=590)

        # Recuadro para mostrar datos
        self.recuadro_datos = tk.Text(self, width=30, height=12.5, wrap=tk.WORD, state=tk.DISABLED)
        self.recuadro_datos.place(x=575, y=270)

        # Imagen en la parte superior derecha
        imagen_superior_derecha = tk.PhotoImage(file=r"C:\Users\fabia\Pictures\Screenshots\Logo Camino.png")  # Cambia la ruta según tu ubicación
        label_superior_derecha = tk.Label(self, image=imagen_superior_derecha, bg="lightsteelblue4")
        label_superior_derecha.image = imagen_superior_derecha  # Referencia para evitar que la imagen sea eliminada por el recolector de basura
        label_superior_derecha.place(relx=1, rely=0, anchor="ne")  # Utiliza relx y rely para posicionar en relación al tamaño de la ventana

        # Imagen en la parte inferior izquierda
        imagen_inferior_izquierda = tk.PhotoImage(file=r"C:\Users\fabia\Downloads\Logo Repartidor.png")
        label_inferior_izquierda = tk.Label(self, image=imagen_inferior_izquierda, bg="lightsteelblue4")
        label_inferior_izquierda.image = imagen_inferior_izquierda  # Referencia para evitar que la imagen sea eliminada por el recolector de basura
        label_inferior_izquierda.place(relx=0, rely=1, anchor="sw")  # Utiliza relx y rely para posicionar en relación al tamaño de la ventana

        # Imagen en la parte media izquierda
        imagen_izquierda = tk.PhotoImage(file=r'C:\Users\fabia\Pictures\Screenshots\Mapa.png')
        label_izquierda = tk.Label(self, image=imagen_izquierda, bg="lightsteelblue4")
        label_izquierda.image = imagen_izquierda
        label_izquierda.place(x=130, rely=0.5, anchor="w")  # Coloca en el lado izquierdo de la ventana

        # Configurar vinculación de la tecla "Enter"
        self.bind("<Return>", lambda event=None: self.obtener_datos())


    def obtener_datos(self):
        nombre = self.texto_name.get()
        peso = self.texto_peso.get()
        codigo_postal = self.texto_cp.get()

        # Validar que todos los campos estén completos
        if nombre == '' or peso == '' or codigo_postal == '':
            messagebox.showwarning("Advertencia", "Completa todos los datos")
            return
        
        # Validar que el nombre solo contiene letras y espacios
        if not nombre.replace(' ', '').isalpha():
            messagebox.showwarning("Advertencia", "El nombre solo puede contener letras y espacios")
            return

        # Validar que el peso solo contienen números
        if not peso.isdigit() or int(peso) < 0 or int(peso) > 15:
            messagebox.showwarning("Advertencia", "El peso debe contener solo números entre 1 y 15")
            return

         # Validar que el código postal solo contienen números y está en el rango permitido
        if not codigo_postal.isdigit() or int(codigo_postal) < 0 or int(codigo_postal) > 16:
            messagebox.showwarning("Advertencia", "El código postal debe contener solo números y estar en el rango de 0 a 16")
            return
        
       # Agregar datos al recuadro
        datos_a_mostrar = f"-----Paquete {self.numero_paquete}-----\n"
        datos_a_mostrar += f"Nombre: {nombre}\n"
        datos_a_mostrar += f"Peso: {peso}\n"
        datos_a_mostrar += f"Codigo Postal: {codigo_postal}\n\n"

        self.recuadro_datos.config(state=tk.NORMAL)  # Habilitar la escritura temporalmente
        self.recuadro_datos.insert(tk.END, datos_a_mostrar)
        self.recuadro_datos.config(state=tk.DISABLED)  # Volver a deshabilitar la escritura


        # Imprimir número de paquete
        print(f"-----Paquete {self.numero_paquete}-----")
        self.numero_paquete += 1  # Incrementar el contador

        #Variables
        print("Nombre:", nombre)
        print("Peso:", peso)
        print("Codigo Postal:", codigo_postal)

        # Limpiar campos después de obtener datos
        self.texto_name.delete(0, tk.END)
        self.texto_peso.delete(0, tk.END)
        self.texto_cp.delete(0, tk.END)

        # Mostrar mensaje de "Paquete agregado"
        messagebox.showinfo("Mensaje", "Paquete agregado")

    def salir_programa(self):
        self.destroy()  # Cierra la ventana principal y finaliza el programa

    def abrir_ventana_eliminar(self):
        ventana_eliminar = VentanaEliminar(self)

    def verificar_existencia_paquete(self, numero_paquete):
        # Verifica si el número de paquete existe en el recuadro de datos
        texto_recuadro = self.recuadro_datos.get("1.0", tk.END)
        return f"-----Paquete {numero_paquete}-----" in texto_recuadro

class VentanaEliminar(tk.Toplevel):
    def __init__(self, ventana_principal):
        super().__init__()

        self.title("Eliminar Paquete")
        self.geometry("300x150")
        self.configure(bg="lightsteelblue4")

        self.ventana_principal = ventana_principal

        # Etiqueta y entrada para el número de paquete a eliminar
        etiqueta_numero_paquete = tk.Label(self, font="Arial 12", text="Número de Paquete:", bg="lightsteelblue4")
        etiqueta_numero_paquete.place(x=20, y=30)

        self.entry_numero_paquete = tk.Entry(self, font="Helvetica 12", width=10)
        self.entry_numero_paquete.place(x=180, y=30)

        # Botón para eliminar paquete
        boton_eliminar_paquete = tk.Button(self, text="Eliminar", padx=10, pady=5, command=self.eliminar_paquete, bg="red", fg="white")
        boton_eliminar_paquete.place(x=120, y=80)

        # Vincular la tecla "Enter" al botón eliminar paquete
        self.bind("<Return>", lambda event=None: boton_eliminar_paquete.invoke())

    def eliminar_paquete(self):
        numero_paquete_a_eliminar = self.entry_numero_paquete.get()

        # Validar que se haya ingresado un número
        if not numero_paquete_a_eliminar.isdigit():
            messagebox.showwarning("Advertencia", "Ingrese un número de paquete válido")
            return

        numero_paquete_a_eliminar = int(numero_paquete_a_eliminar)

        # Verificar si el número de paquete existe antes de eliminar
        if not self.ventana_principal.verificar_existencia_paquete(numero_paquete_a_eliminar):
            messagebox.showwarning("Advertencia", f"El paquete {numero_paquete_a_eliminar} no existe")
            return

        # Eliminar paquete del recuadro de datos
        self.ventana_principal.recuadro_datos.config(state=tk.NORMAL)
        self.ventana_principal.recuadro_datos.delete(f"1.0", f"end-1c")  # Limpiar todo el contenido del recuadro
        self.ventana_principal.recuadro_datos.config(state=tk.DISABLED)

        messagebox.showinfo("Mensaje", f"Paquete {numero_paquete_a_eliminar} eliminado")

        # Cerrar la ventana de eliminar
        self.destroy()


def main():
    app = VentanaPrincipal()
    app.mainloop()

if __name__ == "__main__":
    main()
