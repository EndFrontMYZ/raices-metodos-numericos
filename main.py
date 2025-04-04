import tkinter as tk
from tkinter import messagebox

# Definición de los métodos numéricos (Ejemplo de Bisección)
def biseccion(func, a, b, tol):
    if func(a) * func(b) >= 0:
        return None  # No se puede aplicar el método
    c = a
    while (b - a) >= tol:
        c = (a + b) / 2
        if func(c) == 0.0:
            break
        elif func(c) * func(a) < 0:
            b = c
        else:
            a = c
    return c

# Función para crear la interfaz gráfica
def crear_interfaz():
    ventana = tk.Tk()
    ventana.title("Métodos Numéricos - Raíces de Ecuaciones")

    # Aquí agregas los widgets como botones, entradas, etiquetas, etc.
    
    ventana.mainloop()

# Llamar a la función para mostrar la interfaz
if __name__ == "__main__":
    crear_interfaz()
