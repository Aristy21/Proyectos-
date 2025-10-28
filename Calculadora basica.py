#calculadora basia 
"""print("Bienvenido a la calculadora\n")
primer_numero = int(input("Ingrese el primer numero: "))
segundo_numero = int(input("Ingrese el segundo numero: "))
operacion = input("Ingrese la operacion: ")
if operacion == "+":
    resultado = primer_numero + segundo_numero
elif operacion == "-":
    resultado = primer_numero - segundo_numero
elif operacion == "*":
    resultado = primer_numero * segundo_numero
elif operacion == "/":
    resultado = primer_numero / segundo_numero
else:
    print("Operacion no valida")
print("El resultado es: ", resultado)"""



print("Bienvenido a la calculadora\n")
def suma(a, b):
    return a + b

def resta(a, b):
    return a - b

def multiplicacion(a, b):
    return a * b

def division(a, b):
    if b == 0:
        return "Error: División por cero"
    return a / b

print("Seleccione la operación que desea realizar:")
print("1. Suma") 
print("2. Resta")
print("3. Multiplicación")
print("4. División")

opcion = input("Ingrese el número de la operación (1-4): ")

try:
    num1 = float(input("Ingrese el primer número: "))
    num2 = float(input("Ingrese el segundo número: "))
except ValueError:
    print("Por favor, ingrese valores numéricos válidos.")
    exit()

if opcion == "1":
    resultado = suma(num1, num2)
    print("El resultado de la suma es:", resultado)
elif opcion == "2":
    resultado = resta(num1, num2)
    print("El resultado de la resta es:", resultado)
elif opcion == "3":
    resultado = multiplicacion(num1, num2)
    print("El resultado de la multiplicación es:", resultado)
elif opcion == "4":
    resultado = division(num1, num2)
    print("El resultado de la división es:", resultado)
else:
    print("Opción no válida, elija 1, 2, 3 o 4.")

