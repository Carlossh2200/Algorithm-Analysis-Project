import tkinter as tk
from tkinter import messagebox

class VentanaPrincipal(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title("Ventana Principal")
        self.geometry("1000x650")
        self.configure(bg="lightsteelblue4")

        self.numero_paquete = 1  # Inicializar contador de paquetes

        # Blank nombre
        self.texto_name = tk.Entry(self, font="Helvetica 19")
        self.texto_name.place(x=575, y=270)

        # Blank peso
        self.texto_peso = tk.Entry(self, font="Helvetica 19")
        self.texto_peso.place(x=575, y=355)

        # Blank codigo postal
        self.texto_cp = tk.Entry(self, font="Helvetica 19")
        self.texto_cp.place(x=575, y=440)

        # Título "Agregar paquetes"
        titulo_agregar_paquetes = tk.Label(self, font="Arial 30 bold", text="Agregar Paquetes", bg="lightsteelblue4", fg="white")
        titulo_agregar_paquetes.place(x=575, y=130)

        # Etiqueta nombre
        etiqueta_nombre = tk.Label(self, font="Arial 15", text="Nombre", bg="lightsteelblue4")
        etiqueta_nombre.place(x=575, y=240)

        # Etiqueta peso
        etiqueta_peso = tk.Label(self, font="Arial 15", text="Peso", bg="lightsteelblue4")
        etiqueta_peso.place(x=575, y=325)

        # Etiqueta codigo postal
        etiqueta_cp = tk.Label(self, font="Arial 15", text="Codigo Postal", bg="lightsteelblue4")
        etiqueta_cp.place(x=575, y=410)

        # Boton agregar paquete
        boton_ap = tk.Button(self, text="Agregar Paquete", padx=30, pady=10, command=self.obtener_datos)
        boton_ap.place(x=560, y=500)

        # Imagen en la parte superior derecha
        imagen_superior_derecha = tk.PhotoImage(file=r"C:\Users\fabia\Pictures\logo.png")  # Cambia la ruta según tu ubicación
        label_superior_derecha = tk.Label(self, image=imagen_superior_derecha, bg="lightsteelblue4")
        label_superior_derecha.image = imagen_superior_derecha  # Referencia para evitar que la imagen sea eliminada por el recolector de basura
        label_superior_derecha.place(relx=1, rely=0, anchor="ne")  # Utiliza relx y rely para posicionar en relación al tamaño de la ventana

        # Imagen en la parte inferior izquierda
        imagen_inferior_izquierda = tk.PhotoImage(file=r'C:\Users\fabia\Downloads\image-removebg-preview (1).png')
        label_inferior_izquierda = tk.Label(self, image=imagen_inferior_izquierda, bg="lightsteelblue4")
        label_inferior_izquierda.image = imagen_inferior_izquierda  # Referencia para evitar que la imagen sea eliminada por el recolector de basura
        label_inferior_izquierda.place(relx=0, rely=1, anchor="sw")  # Utiliza relx y rely para posicionar en relación al tamaño de la ventana

        # Imagen en la parte media izquierda
        imagen_izquierda = tk.PhotoImage(file=r'C:\Users\fabia\Pictures\Screenshots\Captura de pantalla 2023-11-15 125953.png')
        label_izquierda = tk.Label(self, image=imagen_izquierda, bg="lightsteelblue4")
        label_izquierda.image = imagen_izquierda
        label_izquierda.place(x=130, rely=0.5, anchor="w")  # Coloca en el lado izquierdo de la ventana


    def obtener_datos(self):
        nombre = self.texto_name.get()
        peso = self.texto_peso.get()
        codigo_postal = self.texto_cp.get()

        # Validar que todos los campos estén completos
        if nombre == '' or peso == '' or codigo_postal == '':
            messagebox.showwarning("Advertencia", "Completa todos los datos")
            return

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

def main():
    app = VentanaPrincipal()
    app.mainloop()

if __name__ == "__main__":
    main()
