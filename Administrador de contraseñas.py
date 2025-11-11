from cryptography.fernet import Fernet
import os


def write_key():
    """Generar una nueva clave y guardarla en un archivo"""
    key = Fernet.generate_key()
    with open("key.key", "wb") as key_file:
        key_file.write(key)
    print("Nueva clave generada y guardada en key.key")
    return key


def load_key():
    """Cargar la clave desde el archivo"""
    try:
        file = open("key.key", "rb")
        key = file.read()
        file.close()
        return key
    except FileNotFoundError:
        print("Archivo de clave no encontrado. Generando nueva clave...")
        return write_key()


def view():
    """Ver todas las contraseñas almacenadas"""
    try:
        with open('passwords.txt', 'r') as f:
            for line in f.readlines():
                data = line.rstrip()
                if "|" in data:
                    user, passw = data.split("|", 1)  # Usar split con límite
                    try:
                        decrypted_password = fer.decrypt(passw.encode()).decode()
                        print("Usuario:", user, "| Contraseña:", decrypted_password)
                    except Exception as e:
                        print(f"Error al desencriptar la contraseña para {user}: {e}")
                else:
                    print("Formato de línea inválido:", data)
    except FileNotFoundError:
        print("No se encontró el archivo de contraseñas. Agrega una contraseña primero.")


def add():
    """Agregar una nueva contraseña"""
    name = input('Nombre de la cuenta: ')
    pwd = input("Contraseña: ")
    
    try:
        with open('passwords.txt', 'a') as f:
            f.write(name + "|" + fer.encrypt(pwd.encode()).decode() + "\n")
        print("Contraseña agregada exitosamente.")
    except Exception as e:
        print(f"Error al guardar la contraseña: {e}")


def main():
    """Función principal del administrador de contraseñas"""
    print("=== ADMINISTRADOR DE CONTRASEÑAS ===")
    print("Bienvenido al administrador de contraseñas seguro.")
    
    while True:
        mode = input(
            "\n¿Qué te gustaría hacer?\n- Agregar nueva contraseña (add)\n- Ver contraseñas existentes (view)\n- Salir (q)\nOpción: ").lower()
        
        if mode == "q":
            print("¡Hasta luego! Tus contraseñas están seguras.")
            break
        elif mode == "view":
            print("\n=== CONTRASEÑAS ALMACENADAS ===")
            view()
        elif mode == "add":
            print("\n=== AGREGAR NUEVA CONTRASEÑA ===")
            add()
        else:
            print("Opción inválida. Por favor elige: add, view, o q.")


if __name__ == "__main__":
    # Inicializar el sistema de encriptación
    key = load_key()
    fer = Fernet(key)
    
    # Ejecutar el programa principal
    main()