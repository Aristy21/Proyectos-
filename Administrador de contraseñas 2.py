# ==============================

# ==============================
# Este programa usa la librería Tkinter para crear una interfaz gráfica (GUI)
# y la librería cryptography (Fernet) para encriptar las contraseñas de forma segura.
# Permite agregar, ver y eliminar contraseñas guardadas localmente en un archivo.

import tkinter as tk                     
from tkinter import ttk, messagebox        
from cryptography.fernet import Fernet     
import os                                  



# Nombre de los archivos donde se guarda la clave de encriptación y las contraseñas
KEY_FILE = "key.key"        # Aquí se guarda la clave de encriptación
PASS_FILE = "passwords.txt" # Aquí se guardan las contraseñas cifradas



def cargar_o_generar_clave():
    """
    Esta función revisa si existe un archivo con la clave de encriptación.
    Si existe, la carga. Si no, genera una nueva y la guarda.
    Retorna: un objeto Fernet que permite encriptar y desencriptar datos.
    """
    # Si el archivo de clave NO existe, generamos una nueva
    if not os.path.exists(KEY_FILE):
        key = Fernet.generate_key()  # Genera una clave segura (bytes)
        with open(KEY_FILE, "wb") as f:  
            f.write(key)  # Guardamos la clave en el archivo
    else:
        # Si el archivo SÍ existe, simplemente la cargamos
        with open(KEY_FILE, "rb") as f:
            key = f.read()  # Leemos los bytes de la clave existente

    # Devolvemos un objeto Fernet que usará esa clave para cifrar/descifrar
    return Fernet(key)


# Llamamos la función y guardamos el resultado (un objeto Fernet)
fer = cargar_o_generar_clave()



def agregar_contraseña():
    """
    Toma los valores escritos en los campos de texto (cuenta y contraseña),
    los encripta y los guarda en un archivo.
    """
    cuenta = cuenta_entry.get().strip()      # .get() -> obtiene texto del Entry
    contraseña = pass_entry.get().strip()    # .strip() -> elimina espacios

    # Validamos que ambos campos estén llenos
    if not cuenta or not contraseña:
        messagebox.showerror("Error", "Completa todos los campos.")
        return  # detenemos la función

    try:
        # Encriptamos la contraseña con Fernet
        encriptada = fer.encrypt(contraseña.encode()).decode()
        # encode() -> convierte texto a bytes
        # encrypt() -> cifra esos bytes
        # decode() -> vuelve el resultado a texto para guardarlo fácilmente

        # Guardamos la cuenta y la contraseña encriptada en el archivo
        with open(PASS_FILE, "a", encoding="utf-8") as f:
            # usamos el carácter "|" para separar los datos
            f.write(f"{cuenta}|{encriptada}\n")

        # Mostramos mensaje de éxito
        messagebox.showinfo("Éxito", "Contraseña guardada correctamente.")

        # Actualizamos la tabla y limpiamos los campos
        cargar_contraseñas()
        limpiar_campos()

    except Exception as e:
        # Si algo falla (por ejemplo, error de escritura)
        messagebox.showerror("Error", f"No se pudo guardar: {e}")


def cargar_contraseñas():
    """
    Lee todas las contraseñas del archivo, las desencripta y las muestra
    en la tabla (Treeview) de la interfaz gráfica.
    """
    # Primero limpiamos la tabla actual
    tree.delete(*tree.get_children())

    # Si el archivo no existe todavía, salimos sin error
    if not os.path.exists(PASS_FILE):
        return

    # Abrimos el archivo donde están guardadas las contraseñas
    with open(PASS_FILE, "r", encoding="utf-8") as f:
        for linea in f:
            try:
                # Cada línea está en el formato: cuenta|contraseña_encriptada
                cuenta, encriptada = linea.strip().split("|")

                # Desencriptamos la contraseña para mostrarla en texto plano
                desencriptada = fer.decrypt(encriptada.encode()).decode()

                # Insertamos los datos en la tabla
                tree.insert("", tk.END, values=(cuenta, desencriptada))

            except:
                # Si hay una línea dañada o mal formateada, la ignoramos
                continue


def eliminar_contraseña():
    """
    Elimina del archivo la contraseña seleccionada en la tabla.
    """
    # Obtenemos qué fila está seleccionada en la tabla
    seleccionado = tree.selection()
    if not seleccionado:
        messagebox.showwarning("Atención", "Selecciona una cuenta primero.")
        return

    # Obtenemos el valor de la cuenta seleccionada
    cuenta = tree.item(seleccionado[0])["values"][0]

    # Pedimos confirmación antes de eliminar
    confirmar = messagebox.askyesno("Confirmar", f"¿Eliminar '{cuenta}'?")
    if not confirmar:
        return  # si el usuario dice "No", salimos

    # Leemos todas las líneas del archivo
    with open(PASS_FILE, "r", encoding="utf-8") as f:
        lineas = f.readlines()

    # Reescribimos el archivo, omitiendo la línea que queremos eliminar
    with open(PASS_FILE, "w", encoding="utf-8") as f:
        for linea in lineas:
            if not linea.startswith(cuenta + "|"):  # si la línea no es la seleccionada
                f.write(linea)

    # Recargamos la tabla para reflejar el cambio
    cargar_contraseñas()


def limpiar_campos():
    """
    Limpia los campos de entrada de cuenta y contraseña.
    """
    cuenta_entry.delete(0, tk.END)
    pass_entry.delete(0, tk.END)


def mostrar_ocultar():
    """
    Alterna entre mostrar y ocultar la contraseña (en modo texto o con asteriscos).
    """
    if pass_entry.cget("show") == "*":  # Si actualmente está oculto
        pass_entry.config(show="")      # Mostramos el texto
    else:
        pass_entry.config(show="*")     # Lo ocultamos nuevamente


# ==============================
# INTERFAZ GRÁFICA
# ==============================
# Aquí se construye toda la ventana con sus botones, entradas y tabla.

root = tk.Tk()                     # Creamos la ventana principal
root.title("Gestor de Contraseñas") # Título de la ventana
root.geometry("600x400")            # Tamaño (ancho x alto)

# ---------- FRAME DE ENTRADA ----------
frame_input = ttk.LabelFrame(root, text="Agregar Contraseña", padding=10)
frame_input.pack(fill="x", padx=10, pady=10)  # fill="x" -> ocupa todo el ancho

# Etiqueta y campo de texto para la cuenta
ttk.Label(frame_input, text="Cuenta:").grid(row=0, column=0, sticky="w")
cuenta_entry = ttk.Entry(frame_input, width=40)
cuenta_entry.grid(row=0, column=1, padx=5)

# Etiqueta y campo de texto para la contraseña
ttk.Label(frame_input, text="Contraseña:").grid(row=1, column=0, sticky="w")
pass_entry = ttk.Entry(frame_input, width=40, show="*")  # show="*" -> oculta el texto
pass_entry.grid(row=1, column=1, padx=5)

# Botones de acción
ttk.Button(frame_input, text="Agregar", command=agregar_contraseña).grid(row=2, column=0, pady=5)
ttk.Button(frame_input, text="Limpiar", command=limpiar_campos).grid(row=2, column=1, sticky="w", pady=5)
ttk.Button(frame_input, text="Mostrar/Ocultar", command=mostrar_ocultar).grid(row=2, column=1, sticky="e", pady=5)

# ---------- FRAME DE TABLA ----------
frame_tabla = ttk.LabelFrame(root, text="Contraseñas Guardadas", padding=10)
frame_tabla.pack(fill="both", expand=True, padx=10, pady=10)

# Tabla (Treeview) que mostrará las contraseñas
tree = ttk.Treeview(frame_tabla, columns=("Cuenta", "Contraseña"), show="headings")
tree.heading("Cuenta", text="Cuenta")
tree.heading("Contraseña", text="Contraseña")
tree.pack(fill="both", expand=True)

# Botón para eliminar la cuenta seleccionada
ttk.Button(root, text="Eliminar Seleccionada", command=eliminar_contraseña).pack(pady=5)

# Al iniciar, cargamos las contraseñas guardadas (si las hay)
cargar_contraseñas()

# Ejecutamos el bucle principal de Tkinter (mantiene la ventana abierta)
root.mainloop()
