import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext, filedialog
from cryptography.fernet import Fernet
import os
import datetime


class PasswordManagerGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Administrador de Contraseñas Seguro")
        self.root.geometry("800x600")
        self.root.resizable(True, True)
        
        # Configurar rutas correctamente
        self.script_dir = os.path.dirname(os.path.abspath(__file__))
        self.key_file = os.path.join(self.script_dir, "key.key")
        self.password_file = os.path.join(self.script_dir, "passwords.txt")
        
        # Inicializar sistema de encriptación
        self.setup_encryption()
        
        # Crear interfaz
        self.create_widgets()
        
        # Cargar contraseñas existentes
        self.load_passwords()
    
    def setup_encryption(self):
        """Configurar sistema de encriptación"""
        try:
            # Intentar cargar clave existente
            with open(self.key_file, "rb") as f:
                self.key = f.read()
        except FileNotFoundError:
            # Generar nueva clave si no existe
            print("Generando nueva clave de encriptación...")
            self.key = Fernet.generate_key()
            with open(self.key_file, "wb") as f:
                f.write(self.key)
            messagebox.showinfo("Clave Generada", "Se ha generado una nueva clave de encriptación.")
        
        self.fer = Fernet(self.key)
    
    def create_widgets(self):
        """Crear la interfaz gráfica"""
        # Frame principal
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Configurar peso de columnas y filas
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        main_frame.columnconfigure(1, weight=1)
        main_frame.rowconfigure(2, weight=1)
        
        # Título
        title_label = ttk.Label(main_frame, text="ADMINISTRADOR DE CONTRASEÑAS SEGURO", 
                               font=("Arial", 14, "bold"))
        title_label.grid(row=0, column=0, columnspan=3, pady=(0, 20))
        
        # Frame para agregar contraseñas
        add_frame = ttk.LabelFrame(main_frame, text="Agregar Nueva Contraseña", padding="10")
        add_frame.grid(row=1, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=(0, 10))
        add_frame.columnconfigure(1, weight=1)
        
        # Campos de entrada
        ttk.Label(add_frame, text="Cuenta:").grid(row=0, column=0, sticky=tk.W, padx=(0, 5))
        self.account_entry = ttk.Entry(add_frame, width=30)
        self.account_entry.grid(row=0, column=1, sticky=(tk.W, tk.E), padx=(0, 10))
        
        ttk.Label(add_frame, text="Contraseña:").grid(row=1, column=0, sticky=tk.W, padx=(0, 5))
        self.password_entry = ttk.Entry(add_frame, width=30, show="*")
        self.password_entry.grid(row=1, column=1, sticky=(tk.W, tk.E), padx=(0, 10))
        
        # Botones
        button_frame = ttk.Frame(add_frame)
        button_frame.grid(row=2, column=0, columnspan=3, pady=(10, 0))
        
        ttk.Button(button_frame, text="Agregar", command=self.add_password).pack(side=tk.LEFT, padx=(0, 5))
        ttk.Button(button_frame, text="Limpiar", command=self.clear_entries).pack(side=tk.LEFT, padx=(0, 5))
        ttk.Button(button_frame, text="Mostrar/Ocultar", command=self.toggle_password_visibility).pack(side=tk.LEFT)
        
        # Frame para mostrar contraseñas
        view_frame = ttk.LabelFrame(main_frame, text="Contraseñas Almacenadas", padding="10")
        view_frame.grid(row=2, column=0, columnspan=3, sticky=(tk.W, tk.E, tk.N, tk.S), pady=(0, 10))
        view_frame.columnconfigure(0, weight=1)
        view_frame.rowconfigure(1, weight=1)
        
        # Treeview para mostrar contraseñas
        columns = ("Cuenta", "Contraseña", "URL")
        self.password_tree = ttk.Treeview(view_frame, columns=columns, show="headings", height=15)
        
        # Configurar columnas
        self.password_tree.heading("Cuenta", text="Cuenta")
        self.password_tree.heading("Contraseña", text="Contraseña")
        self.password_tree.heading("URL", text="URL")
        self.password_tree.column("Cuenta", width=200)
        self.password_tree.column("Contraseña", width=250)
        self.password_tree.column("URL", width=300)
        
        # Scrollbar para treeview
        scrollbar = ttk.Scrollbar(view_frame, orient=tk.VERTICAL, command=self.password_tree.yview)
        self.password_tree.configure(yscrollcommand=scrollbar.set)
        
        self.password_tree.grid(row=1, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        scrollbar.grid(row=1, column=1, sticky=(tk.N, tk.S))
        
        # Botones de gestión
        button_frame2 = ttk.Frame(view_frame)
        button_frame2.grid(row=2, column=0, columnspan=2, pady=(10, 0))
        
        ttk.Button(button_frame2, text="Actualizar", command=self.load_passwords).pack(side=tk.LEFT, padx=(0, 5))
        ttk.Button(button_frame2, text="Eliminar Seleccionada", command=self.delete_password).pack(side=tk.LEFT, padx=(0, 5))
        ttk.Button(button_frame2, text="Exportar a Archivo", command=self.export_passwords).pack(side=tk.LEFT)
        ttk.Button(button_frame2, text="Importar CSV", command=self.import_csv).pack(side=tk.LEFT, padx=(0, 5))
        
        # Barra de estado
        self.status_var = tk.StringVar()
        self.status_var.set("Listo")
        status_bar = ttk.Label(main_frame, textvariable=self.status_var, relief=tk.SUNKEN)
        status_bar.grid(row=3, column=0, columnspan=3, sticky=(tk.W, tk.E))
        
        # Configurar evento para actualizar estado
        self.password_tree.bind("<ButtonRelease-1>", self.on_item_select)
    
    def toggle_password_visibility(self):
        """Alternar visibilidad de la contraseña"""
        if self.password_entry.cget("show") == "*":
            self.password_entry.config(show="")
        else:
            self.password_entry.config(show="*")
    
    def clear_entries(self):
        """Limpiar campos de entrada"""
        self.account_entry.delete(0, tk.END)
        self.password_entry.delete(0, tk.END)
        self.account_entry.focus()
    
    def add_password(self):
        """Agregar nueva contraseña"""
        account = self.account_entry.get().strip()
        password = self.password_entry.get().strip()
        
        if not account or not password:
            messagebox.showerror("Error", "Por favor completa todos los campos.")
            return
        
        try:
            # Encriptar y guardar
            encrypted_password = self.fer.encrypt(password.encode()).decode()
            
            with open(self.password_file, "a", encoding="utf-8") as f:
                f.write(f"{account}|{encrypted_password}\n")
            
            messagebox.showinfo("Éxito", "Contraseña agregada exitosamente.")
            self.clear_entries()
            self.load_passwords()
            
        except Exception as e:
            messagebox.showerror("Error", f"Error al guardar la contraseña: {str(e)}")
    
    def load_passwords(self):
        """Cargar y mostrar contraseñas"""
        # Limpiar treeview
        for item in self.password_tree.get_children():
            self.password_tree.delete(item)
        
        try:
            if os.path.exists(self.password_file):
                with open(self.password_file, "r", encoding="utf-8") as f:
                    for line_num, line in enumerate(f, 1):
                        line = line.strip()
                        if "|" in line:
                            try:
                                # Dividir por | pero manejar casos con URLs y notas
                                parts = line.split("|")
                                account = parts[0]
                                encrypted_password = parts[1]
                                
                                # Desencriptar la contraseña
                                decrypted_password = self.fer.decrypt(encrypted_password.encode()).decode()
                                
                                # Extraer URL si existe
                                url = ""
                                for part in parts[2:]:
                                    if part.startswith("URL: "):
                                        url = part.replace("URL: ", "")
                                        break
                                
                                # Insertar en treeview
                                self.password_tree.insert("", tk.END, values=(account, decrypted_password, url))
                                
                            except Exception as e:
                                # Si hay error de desencriptación, mostrar indicador
                                self.password_tree.insert("", tk.END, values=(f"Error en línea {line_num}", "No se pudo desencriptar", ""))
                                print(f"Error en línea {line_num}: {e}")
            
            # Contar contraseñas cargadas
            count = len(self.password_tree.get_children())
            self.status_var.set(f"Contraseñas cargadas: {count}")
            print(f"Contraseñas cargadas: {count}")
            
        except FileNotFoundError:
            self.status_var.set("No hay contraseñas almacenadas")
            print("No hay contraseñas almacenadas")
        except Exception as e:
            messagebox.showerror("Error", f"Error al cargar contraseñas: {str(e)}")
            self.status_var.set("Error al cargar contraseñas")
            print(f"Error al cargar contraseñas: {e}")
    
    def delete_password(self):
        """Eliminar contraseña seleccionada"""
        selected_item = self.password_tree.selection()
        if not selected_item:
            messagebox.showwarning("Advertencia", "Selecciona una contraseña para eliminar.")
            return
        
        # Confirmar eliminación
        if messagebox.askyesno("Confirmar", "¿Estás seguro de que quieres eliminar esta contraseña?"):
            try:
                # Obtener datos del item seleccionado
                item = self.password_tree.item(selected_item[0])
                account_to_delete = item['values'][0]
                
                # Leer archivo y eliminar línea
                with open(self.password_file, "r", encoding="utf-8") as f:
                    lines = f.readlines()
                
                with open(self.password_file, "w", encoding="utf-8") as f:
                    for line in lines:
                        if not line.startswith(account_to_delete + "|"):
                            f.write(line)
                
                self.load_passwords()
                messagebox.showinfo("Éxito", "Contraseña eliminada exitosamente.")
                
            except Exception as e:
                messagebox.showerror("Error", f"Error al eliminar contraseña: {str(e)}")
    
    def export_passwords(self):
        """Exportar contraseñas a un archivo de texto"""
        try:
            timestamp = datetime.datetime.now().strftime('%Y%m%d_%H%M%S')
            filename = f"contraseñas_exportadas_{timestamp}.txt"
            
            with open(filename, "w", encoding="utf-8") as export_file:
                export_file.write("=== CONTRASEÑAS EXPORTADAS ===\n")
                export_file.write(f"Fecha de exportación: {datetime.datetime.now()}\n\n")
                
                for item in self.password_tree.get_children():
                    values = self.password_tree.item(item)['values']
                    export_file.write(f"Cuenta: {values[0]}\n")
                    export_file.write(f"Contraseña: {values[1]}\n")
                    if len(values) > 2 and values[2]:
                        export_file.write(f"URL: {values[2]}\n")
                    export_file.write("-" * 30 + "\n")
            
            messagebox.showinfo("Éxito", f"Contraseñas exportadas a: {filename}")
            
        except Exception as e:
            messagebox.showerror("Error", f"Error al exportar contraseñas: {str(e)}")
    
    def import_csv(self):
        """Importar contraseñas desde archivo CSV"""
        try:
            filename = filedialog.askopenfilename(
                title="Seleccionar archivo CSV",
                filetypes=[("CSV files", "*.csv"), ("All files", "*.*")]
            )
            
            if filename:
                # Ejecutar el script de importación
                import subprocess
                result = subprocess.run(['python', 'import_csv_passwords.py'], 
                                      capture_output=True, text=True, cwd=self.script_dir)
                
                if result.returncode == 0:
                    messagebox.showinfo("Éxito", "CSV importado exitosamente")
                    self.load_passwords()
                else:
                    messagebox.showerror("Error", f"Error al importar CSV: {result.stderr}")
                    
        except Exception as e:
            messagebox.showerror("Error", f"Error al seleccionar archivo: {str(e)}")
    
    def on_item_select(self, event):
        """Manejar selección de item en treeview"""
        selected_item = self.password_tree.selection()
        if selected_item:
            item = self.password_tree.item(selected_item[0])
            account = item['values'][0]
            self.status_var.set(f"Seleccionada: {account}")


def main():
    """Función principal"""
    root = tk.Tk()
    app = PasswordManagerGUI(root)
    
    # Centrar ventana
    root.update_idletasks()
    x = (root.winfo_screenwidth() - root.winfo_width()) // 2
    y = (root.winfo_screenheight() - root.winfo_height()) // 2
    root.geometry(f"+{x}+{y}")
    
    # Configurar cierre de ventana
    def on_closing():
        if messagebox.askokcancel("Salir", "¿Quieres salir del administrador de contraseñas?"):
            root.destroy()
    
    root.protocol("WM_DELETE_WINDOW", on_closing)
    root.mainloop()


if __name__ == "__main__":
    main()