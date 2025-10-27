import tkinter as tk
from tkinter import messagebox, ttk
import random
import time

class Barco:
    """Clase para representar un barco"""
    def __init__(self, nombre, tamaño): #definimos un objeto 
        self.nombre = nombre
        self.tamaño = tamaño
        self.posiciones = []  # Lista de tuplas (fila, columna)
        self.hits = 0  # Número de golpes recibidos
        
    def hundido(self):
        """Verifica si el barco está hundido"""
        return self.hits >= self.tamaño
    
    def agregar_posicion(self, fila, columna):
        """Agrega una posición al barco"""
        self.posiciones.append((fila, columna))
    
    def recibir_golpe(self):
        """Incrementa el contador de golpes"""
        self.hits += 1

class Tablero:
    """Clase para manejar el tablero de juego"""
    def __init__(self, tamaño=10):
        self.tamaño = tamaño
        self.tablero = [['~' for _ in range(tamaño)] for _ in range(tamaño)]
        self.barcos = []
        self.disparos_realizados = set()
    
    def mostrar_tablero(self, mostrar_barcos=False):
        """Muestra el tablero en consola (para debug)"""
        print("  " + " ".join([str(i) for i in range(self.tamaño)]))
        for i, fila in enumerate(self.tablero):
            print(f"{i} " + " ".join(fila))
    
    def colocar_barco(self, barco, fila_inicio, columna_inicio, direccion):
        """Coloca un barco en el tablero"""
        fila, columna = fila_inicio, columna_inicio
        
        # Verificar si el barco cabe en esa posición
        if direccion == 'horizontal':
            if columna + barco.tamaño > self.tamaño:
                return False
            for i in range(barco.tamaño):
                if self.tablero[fila][columna + i] != '~':
                    return False
        else:  # vertical
            if fila + barco.tamaño > self.tamaño:
                return False
            for i in range(barco.tamaño):
                if self.tablero[fila + i][columna] != '~':
                    return False
        
        # Colocar el barco
        if direccion == 'horizontal':
            for i in range(barco.tamaño):
                self.tablero[fila][columna + i] = 'B'
                barco.agregar_posicion(fila, columna + i)
        else:
            for i in range(barco.tamaño):
                self.tablero[fila + i][columna] = 'B'
                barco.agregar_posicion(fila + i, columna)
        
        self.barcos.append(barco)
        return True
    
    def disparar(self, fila, columna):
        """Realiza un disparo en la posición especificada"""
        if (fila, columna) in self.disparos_realizados:
            return "Ya disparaste aquí"
        
        self.disparos_realizados.add((fila, columna))
        
        if self.tablero[fila][columna] == 'B':
            self.tablero[fila][columna] = 'X'
            # Encontrar qué barco fue golpeado
            for barco in self.barcos:
                if (fila, columna) in barco.posiciones:
                    barco.recibir_golpe()
                    if barco.hundido():
                        return f"¡Hundiste el {barco.nombre}!"
                    else:
                        return "¡Impacto!"
        else:
            self.tablero[fila][columna] = 'O'
            return "Agua"
    
    def todos_barcos_hundidos(self):
        """Verifica si todos los barcos están hundidos"""
        return all(barco.hundido() for barco in self.barcos)

class BatallaNaval:
    """Clase principal del juego"""
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Batalla Naval")
        self.root.geometry("800x600")
        self.root.configure(bg='#1e3a8a')
        
        # Tableros
        self.tablero_jugador = Tablero()
        self.tablero_maquina = Tablero()
        
        # Estado del juego
        self.fase = "colocacion"  # colocacion, juego, terminado
        self.barcos_por_colocar = [
            Barco("Submarino", 2),
            Barco("Lancha", 3),
            Barco("Portaaviones", 4)
        ]
        self.barco_actual = 0
        self.posiciones_temporales = []
        self.turno_jugador = True
        
        self.crear_interfaz()
    
    def crear_interfaz(self):
        """Crea la interfaz gráfica del juego"""
        # Título
        titulo = tk.Label(
            self.root,
            text="🚢 BATALLA NAVAL 🚢",
            font=("Arial", 24, "bold"),
            fg="white",
            bg="#1e3a8a"
        )
        titulo.pack(pady=20)
        
        # Frame principal
        self.frame_principal = tk.Frame(self.root, bg="#1e3a8a")
        self.frame_principal.pack(expand=True, fill="both", padx=20, pady=20)
        
        # Frame de información
        self.frame_info = tk.Frame(self.frame_principal, bg="#1e3a8a")
        self.frame_info.pack(fill="x", pady=(0, 20))
        
        self.label_estado = tk.Label(
            self.frame_info,
            text="¡Bienvenido! Coloca tus barcos en el tablero",
            font=("Arial", 14),
            fg="white",
            bg="#1e3a8a"
        )
        self.label_estado.pack()
        
        # Frame de tableros
        self.frame_tableros = tk.Frame(self.frame_principal, bg="#1e3a8a")
        self.frame_tableros.pack(expand=True, fill="both")
        
        # Tablero del jugador
        self.frame_tablero_jugador = tk.Frame(self.frame_tableros, bg="#1e3a8a")
        self.frame_tablero_jugador.pack(side="left", expand=True, fill="both", padx=(0, 10))
        
        tk.Label(
            self.frame_tablero_jugador,
            text="TU TABLERO",
            font=("Arial", 12, "bold"),
            fg="white",
            bg="#1e3a8a"
        ).pack()
        
        self.canvas_jugador = tk.Canvas(
            self.frame_tablero_jugador,
            width=300,
            height=300,
            bg="#0f172a",
            highlightthickness=2,
            highlightbackground="white"
        )
        self.canvas_jugador.pack(pady=10)
        
        # Tablero de la máquina
        self.frame_tablero_maquina = tk.Frame(self.frame_tableros, bg="#1e3a8a")
        self.frame_tablero_maquina.pack(side="right", expand=True, fill="both", padx=(10, 0))
        
        tk.Label(
            self.frame_tablero_maquina,
            text="TABLERO ENEMIGO",
            font=("Arial", 12, "bold"),
            fg="white",
            bg="#1e3a8a"
        ).pack()
        
        self.canvas_maquina = tk.Canvas(
            self.frame_tablero_maquina,
            width=300,
            height=300,
            bg="#0f172a",
            highlightthickness=2,
            highlightbackground="white"
        )
        self.canvas_maquina.pack(pady=10)
        
        # Frame de controles
        self.frame_controles = tk.Frame(self.frame_principal, bg="#1e3a8a")
        self.frame_controles.pack(fill="x", pady=(20, 0))
        
        self.boton_direccion = tk.Button(
            self.frame_controles,
            text="Dirección: Horizontal",
            command=self.cambiar_direccion,
            font=("Arial", 10),
            bg="#3b82f6",
            fg="white",
            relief="raised"
        )
        self.boton_direccion.pack(side="left", padx=(0, 10))
        
        self.boton_confirmar = tk.Button(
            self.frame_controles,
            text="Confirmar Barco",
            command=self.confirmar_barco,
            font=("Arial", 10),
            bg="#10b981",
            fg="white",
            relief="raised"
        )
        self.boton_confirmar.pack(side="left", padx=(0, 10))
        
        self.boton_empezar = tk.Button(
            self.frame_controles,
            text="Empezar Juego",
            command=self.empezar_juego,
            font=("Arial", 10),
            bg="#f59e0b",
            fg="white",
            relief="raised",
            state="disabled"
        )
        self.boton_empezar.pack(side="left")
        
        self.direccion_horizontal = True
        self.dibujar_tableros()
        self.canvas_jugador.bind("<Button-1>", self.click_tablero_jugador)
        self.canvas_maquina.bind("<Button-1>", self.click_tablero_maquina)
    
    def cambiar_direccion(self):
        """Cambia la dirección de colocación del barco"""
        self.direccion_horizontal = not self.direccion_horizontal
        texto = "Dirección: Horizontal" if self.direccion_horizontal else "Dirección: Vertical"
        self.boton_direccion.config(text=texto)
    
    def dibujar_tableros(self):
        """Dibuja ambos tableros en los canvas"""
        self.dibujar_tablero(self.canvas_jugador, self.tablero_jugador, True)
        self.dibujar_tablero(self.canvas_maquina, self.tablero_maquina, False)
    
    def dibujar_tablero(self, canvas, tablero, mostrar_barcos):
        """Dibuja un tablero específico"""
        canvas.delete("all")
        
        tamaño_celda = 30
        margen = 10
        
        # Dibujar cuadrícula
        for i in range(tablero.tamaño):
            for j in range(tablero.tamaño):
                x1 = margen + j * tamaño_celda
                y1 = margen + i * tamaño_celda
                x2 = x1 + tamaño_celda
                y2 = y1 + tamaño_celda
                
                # Color de fondo
                color = "#1e40af"  # Azul marino
                
                # Determinar el color según el estado de la celda
                if mostrar_barcos:
                    if tablero.tablero[i][j] == 'B':
                        color = "#374151"  # Gris para barcos
                    elif tablero.tablero[i][j] == 'X':
                        color = "#dc2626"  # Rojo para impactos
                    elif tablero.tablero[i][j] == 'O':
                        color = "#6b7280"  # Gris claro para agua
                else:
                    if tablero.tablero[i][j] == 'X':
                        color = "#dc2626"  # Rojo para impactos
                    elif tablero.tablero[i][j] == 'O':
                        color = "#6b7280"  # Gris claro para agua
                
                canvas.create_rectangle(x1, y1, x2, y2, fill=color, outline="white", width=1)
        
        # Dibujar números y letras
        for i in range(tablero.tamaño):
            # Números verticales
            canvas.create_text(
                margen - 5, margen + i * tamaño_celda + tamaño_celda // 2,
                text=str(i), fill="white", font=("Arial", 8)
            )
            # Números horizontales
            canvas.create_text(
                margen + i * tamaño_celda + tamaño_celda // 2, margen - 5,
                text=str(i), fill="white", font=("Arial", 8)
            )
    
    def click_tablero_jugador(self, event):
        """Maneja los clics en el tablero del jugador"""
        if self.fase == "colocacion":
            self.colocar_barco_jugador(event)
        elif self.fase == "juego" and self.turno_jugador:
            self.disparar_jugador(event)
    
    def click_tablero_maquina(self, event):
        """Maneja los clics en el tablero de la máquina"""
        if self.fase == "juego" and self.turno_jugador:
            self.disparar_jugador(event)
    
    def colocar_barco_jugador(self, event):
        """Coloca un barco en el tablero del jugador"""
        if self.barco_actual >= len(self.barcos_por_colocar):
            return
        
        canvas = self.canvas_jugador
        tamaño_celda = 30
        margen = 10
        
        # Calcular posición
        columna = (event.x - margen) // tamaño_celda
        fila = (event.y - margen) // tamaño_celda
        
        if 0 <= fila < self.tablero_jugador.tamaño and 0 <= columna < self.tablero_jugador.tamaño:
            barco = self.barcos_por_colocar[self.barco_actual]
            
            # Limpiar posiciones temporales anteriores
            self.posiciones_temporales = []
            
            # Calcular posiciones del barco
            if self.direccion_horizontal:
                if columna + barco.tamaño <= self.tablero_jugador.tamaño:
                    for i in range(barco.tamaño):
                        self.posiciones_temporales.append((fila, columna + i))
            else:
                if fila + barco.tamaño <= self.tablero_jugador.tamaño:
                    for i in range(barco.tamaño):
                        self.posiciones_temporales.append((fila + i, columna))
            
            # Mostrar preview del barco
            self.mostrar_preview_barco()
    
    def mostrar_preview_barco(self):
        """Muestra un preview del barco antes de confirmarlo"""
        self.dibujar_tablero(self.canvas_jugador, self.tablero_jugador, True)
        
        tamaño_celda = 30
        margen = 10
        
        for fila, columna in self.posiciones_temporales:
            x1 = margen + columna * tamaño_celda
            y1 = margen + fila * tamaño_celda
            x2 = x1 + tamaño_celda
            y2 = y1 + tamaño_celda
            
            # Dibujar preview en amarillo
            self.canvas_jugador.create_rectangle(
                x1, y1, x2, y2, fill="#fbbf24", outline="white", width=2
            )
    
    def confirmar_barco(self):
        """Confirma la colocación del barco actual"""
        if not self.posiciones_temporales:
            messagebox.showwarning("Advertencia", "Selecciona una posición para el barco")
            return
        
        barco = self.barcos_por_colocar[self.barco_actual]
        fila_inicio, columna_inicio = self.posiciones_temporales[0]
        
        if self.tablero_jugador.colocar_barco(barco, fila_inicio, columna_inicio, 
                                           "horizontal" if self.direccion_horizontal else "vertical"):
            self.barco_actual += 1
            self.posiciones_temporales = []
            
            if self.barco_actual >= len(self.barcos_por_colocar):
                self.label_estado.config(text="¡Todos los barcos colocados! Presiona 'Empezar Juego'")
                self.boton_empezar.config(state="normal")
                self.boton_confirmar.config(state="disabled")
            else:
                siguiente_barco = self.barcos_por_colocar[self.barco_actual]
                self.label_estado.config(text=f"Coloca el {siguiente_barco.nombre} (tamaño: {siguiente_barco.tamaño})")
            
            self.dibujar_tableros()
        else:
            messagebox.showerror("Error", "No se puede colocar el barco en esa posición")
    
    def empezar_juego(self):
        """Inicia el juego colocando los barcos de la máquina"""
        self.fase = "juego"
        self.colocar_barcos_maquina()
        self.label_estado.config(text="¡Juego iniciado! Es tu turno. Haz clic en el tablero enemigo para disparar")
        self.boton_confirmar.config(state="disabled")
        self.boton_direccion.config(state="disabled")
        self.boton_empezar.config(state="disabled")
        self.dibujar_tableros()
    
    def colocar_barcos_maquina(self):
        """Coloca automáticamente los barcos de la máquina"""
        barcos_maquina = [
            Barco("Submarino", 2),
            Barco("Lancha", 3),
            Barco("Portaaviones", 4)
        ]
        
        for barco in barcos_maquina:
            colocado = False
            intentos = 0
            
            while not colocado and intentos < 100:
                fila = random.randint(0, self.tablero_maquina.tamaño - 1)
                columna = random.randint(0, self.tablero_maquina.tamaño - 1)
                direccion = random.choice(['horizontal', 'vertical'])
                
                colocado = self.tablero_maquina.colocar_barco(barco, fila, columna, direccion)
                intentos += 1
    
    def disparar_jugador(self, event):
        """Maneja el disparo del jugador"""
        if not self.turno_jugador:
            return
        
        canvas = self.canvas_maquina
        tamaño_celda = 30
        margen = 10
        
        columna = (event.x - margen) // tamaño_celda
        fila = (event.y - margen) // tamaño_celda
        
        if 0 <= fila < self.tablero_maquina.tamaño and 0 <= columna < self.tablero_maquina.tamaño:
            resultado = self.tablero_maquina.disparar(fila, columna)
            self.label_estado.config(text=f"Tu disparo: {resultado}")
            
            if self.tablero_maquina.todos_barcos_hundidos():
                self.fin_juego("¡Felicidades! ¡Has ganado!")
                return
            
            self.turno_jugador = False
            self.root.after(1000, self.disparo_maquina)
            
            self.dibujar_tableros()
    
    def disparo_maquina(self):
        """Realiza el disparo de la máquina"""
        if self.turno_jugador:
            return
        
        # Disparo aleatorio inteligente
        fila, columna = self.obtener_disparo_inteligente()
        resultado = self.tablero_jugador.disparar(fila, columna)
        
        self.label_estado.config(text=f"Disparo enemigo en ({fila}, {columna}): {resultado}")
        
        if self.tablero_jugador.todos_barcos_hundidos():
            self.fin_juego("¡La máquina ha ganado!")
            return
        
        self.turno_jugador = True
        self.label_estado.config(text="Es tu turno. Haz clic en el tablero enemigo para disparar")
        
        self.dibujar_tableros()
    
    def obtener_disparo_inteligente(self):
        """Obtiene una posición inteligente para el disparo de la máquina"""
        # Buscar posiciones no disparadas
        posiciones_disponibles = []
        for i in range(self.tablero_jugador.tamaño):
            for j in range(self.tablero_jugador.tamaño):
                if (i, j) not in self.tablero_jugador.disparos_realizados:
                    posiciones_disponibles.append((i, j))
        
        if posiciones_disponibles:
            return random.choice(posiciones_disponibles)
        else:
            return (0, 0)  # Fallback
    
    def fin_juego(self, mensaje):
        """Termina el juego"""
        self.fase = "terminado"
        messagebox.showinfo("¡Juego Terminado!", mensaje)
        self.label_estado.config(text=mensaje)
    
    def ejecutar(self):
        """Ejecuta el juego"""
        self.root.mainloop()

if __name__ == "__main__":
    juego = BatallaNaval()
    juego.ejecutar()
