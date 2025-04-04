import tkinter as tk
from tkinter import ttk, messagebox
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import numpy as np
from sympy import symbols, lambdify, sympify, diff

# Función para graficar con diseño actualizado
def graficar_funcion(f, a, b, c, metodo):
    fig = plt.Figure(figsize=(6, 4), dpi=100)
    ax = fig.add_subplot(111)
    
    # Determinar los límites del gráfico
    if metodo == "Newton-Raphson":
        x_vals = np.linspace(c - 3, c + 3, 200)  # Centrado en punto inicial
    else:
        x_vals = np.linspace(a - 1, b + 1, 200)
    
    y_vals = [f(x) for x in x_vals]
    ax.plot(x_vals, y_vals, 'b-', label='f(x)', linewidth=2)
    
    # Marcar puntos según el método
    if metodo == "Bisección" or metodo == "Falsa Posición":
        ax.plot(a, f(a), 'ro', label='a', markersize=8)
        ax.plot(b, f(b), 'go', label='b', markersize=8)
    
    ax.plot(c, f(c), 'mo', label='raíz', markersize=8)
    
    # Elementos gráficos
    ax.axhline(y=0, color='black', linestyle='--', alpha=0.5)
    ax.axvline(x=0, color='black', linestyle='--', alpha=0.5)
    ax.grid(True, linestyle=':', alpha=0.7)
    ax.legend(loc='best', frameon=False)
    ax.set_title(f'Método de {metodo}', fontsize=14, color='darkblue')
    ax.set_xlabel('x', fontsize=12)
    ax.set_ylabel('f(x)', fontsize=12)
    ax.set_facecolor('whitesmoke')
    
    return fig

# Método de Bisección
def calcular_biseccion(f, a, b, crit, max_iter, tabla_tree):
    if f(a) * f(b) >= 0:
        return None, "La función no tiene una raíz en el intervalo o tiene un número par de raíces."
    
    i, ea, x_anterior = 0, 1, 0
    tabla_tree.delete(*tabla_tree.get_children())
    
    while ea > crit and i < max_iter:
        c = (a + b) / 2
        fc = f(c)
        ea = abs((c - x_anterior) / c) if c != 0 else 0
        
        # Actualizar tabla
        if i % 2 == 0:
            tabla_tree.insert("", "end", values=(i, round(a, 6), round(b, 6), round(c, 6), round(fc, 9)), tags=('evenrow',))
        else:
            tabla_tree.insert("", "end", values=(i, round(a, 6), round(b, 6), round(c, 6), round(fc, 9)), tags=('oddrow',))
        
        # Actualizar intervalo
        if f(c) * f(a) < 0:
            b = c
        else:
            a = c
            
        x_anterior = c
        i += 1
        
    return c, f"El valor de x es {round(c, 9)} con un f(c) de {round(f(c), 9)}"

# Método de Falsa Posición
def calcular_falsa_posicion(f, a, b, crit, max_iter, tabla_tree):
    if f(a) * f(b) >= 0:
        return None, "La función no tiene una raíz en el intervalo o tiene un número par de raíces."
    
    i, ea, x_anterior = 0, 1, 0
    tabla_tree.delete(*tabla_tree.get_children())
    
    while ea > crit and i < max_iter:
        fa = f(a)
        fb = f(b)
        
        # Cálculo del punto c usando la regla de falsa posición
        c = b - fb * (b - a) / (fb - fa)
        fc = f(c)
        
        ea = abs((c - x_anterior) / c) if c != 0 else 0
        
        # Actualizar tabla
        if i % 2 == 0:
            tabla_tree.insert("", "end", values=(i, round(a, 6), round(b, 6), round(c, 6), round(fc, 9)), tags=('evenrow',))
        else:
            tabla_tree.insert("", "end", values=(i, round(a, 6), round(b, 6), round(c, 6), round(fc, 9)), tags=('oddrow',))
        
        # Actualizar intervalo
        if fc * fa < 0:
            b = c
        else:
            a = c
            
        x_anterior = c
        i += 1
        
    return c, f"El valor de x es {round(c, 9)} con un f(c) de {round(f(c), 9)}"

# Método de Newton-Raphson
def calcular_newton_raphson(f, df, x0, crit, max_iter, tabla_tree):
    i, ea = 0, 1
    tabla_tree.delete(*tabla_tree.get_children())
    
    x_anterior = x0
    
    while ea > crit and i < max_iter:
        try:
            fx = f(x_anterior)
            dfx = df(x_anterior)
            
            if abs(dfx) < 1e-10:  # Evitar división por cero
                return None, "El valor de la derivada es cercano a cero. Cambie el punto inicial."
            
            x_nuevo = x_anterior - fx / dfx
            ea = abs((x_nuevo - x_anterior) / x_nuevo) if x_nuevo != 0 else 0
            
            # Actualizar tabla (adaptada para Newton-Raphson)
            if i % 2 == 0:
                tabla_tree.insert("", "end", values=(i, round(x_anterior, 6), round(fx, 6), round(dfx, 6), round(x_nuevo, 9)), tags=('evenrow',))
            else:
                tabla_tree.insert("", "end", values=(i, round(x_anterior, 6), round(fx, 6), round(dfx, 6), round(x_nuevo, 9)), tags=('oddrow',))
            
            x_anterior = x_nuevo
            i += 1
            
        except Exception as e:
            return None, f"Error en cálculo: {e}"
    
    return x_anterior, f"El valor de x es {round(x_anterior, 9)} con un f(x) de {round(f(x_anterior), 9)}"

# Función principal
def calcular():
    try:
        # Limpiar gráfica previa
        for widget in frame_grafica.winfo_children():
            widget.destroy()
        
        # Obtener la función y crear callable
        fn = sympify(funcion_entry.get())
        f = lambdify(x, fn)
        
        # Calcular derivada para Newton-Raphson
        dfn = diff(fn, x)
        df = lambdify(x, dfn)
        
        # Obtener parámetros comunes
        crit = float(crit_entry.get())
        max_iter = int(iter_entry.get())
        metodo = metodo_combo.get()
        
        # Configurar columnas de tabla según método
        tabla_tree.delete(*tabla_tree.get_children())
        
        if metodo == "Newton-Raphson":
            for col in tabla_tree["columns"]:
                tabla_tree.heading(col, text="")
            tabla_tree.heading("i", text="i")
            tabla_tree.heading("a", text="xᵢ")
            tabla_tree.heading("b", text="f(xᵢ)")
            tabla_tree.heading("c", text="f'(xᵢ)")
            tabla_tree.heading("f(c)", text="xᵢ₊₁")
            
            # Obtener punto inicial para Newton-Raphson
            x0 = float(x0_entry.get())
            c, mensaje = calcular_newton_raphson(f, df, x0, crit, max_iter, tabla_tree)
            
            if c is not None:  
                fig = graficar_funcion(f, None, None, c, metodo)
                canvas = FigureCanvasTkAgg(fig, frame_grafica)
                canvas.draw()
                canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)
                accion.configure(text="** Cálculo Terminado! **")
            else:
                accion.configure(text="** Error en el cálculo **")
                
        else:  # Bisección o Falsa Posición
            for col in tabla_tree["columns"]:
                tabla_tree.heading(col, text="")
            tabla_tree.heading("i", text="i")
            tabla_tree.heading("a", text="a")
            tabla_tree.heading("b", text="b")
            tabla_tree.heading("c", text="c")
            tabla_tree.heading("f(c)", text="f(c)")
            
            # Obtener intervalo
            a = float(a_entry.get())
            b = float(b_entry.get())
            
            if metodo == "Bisección":
                c, mensaje = calcular_biseccion(f, a, b, crit, max_iter, tabla_tree)
            else:  # Falsa Posición
                c, mensaje = calcular_falsa_posicion(f, a, b, crit, max_iter, tabla_tree)
                
            if c is not None:
                fig = graficar_funcion(f, a, b, c, metodo)
                canvas = FigureCanvasTkAgg(fig, frame_grafica)
                canvas.draw()
                canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)
                accion.configure(text="** Cálculo Terminado! **")
            else:
                accion.configure(text="** Error en el intervalo **")
        
        resultado_label.config(text=mensaje)
        
    except Exception as e:
        resultado_label.config(text=f"Error: {e}")
        accion.configure(text="** Error en la función o datos **")
        messagebox.showerror("Error", f"Se produjo un error: {e}")

# Función para actualizar los campos según el método seleccionado
def actualizar_campos(*args):
    metodo = metodo_combo.get()
    
    # Ocultar todos los campos
    a_label.grid_remove()
    a_entry.grid_remove()
    b_label.grid_remove()
    b_entry.grid_remove()
    x0_label.grid_remove()
    x0_entry.grid_remove()
    
    if metodo == "Newton-Raphson":
        # Mostrar solo campo para punto inicial
        x0_label.grid(row=2, column=0, padx=5, pady=5)
        x0_entry.grid(row=2, column=1, padx=5, pady=5)
        frame_titulo.config(text="Método de Newton-Raphson")
    else:
        # Mostrar campos para intervalo [a,b]
        a_label.grid(row=2, column=0, padx=5, pady=5)
        a_entry.grid(row=2, column=1, padx=5, pady=5)
        b_label.grid(row=3, column=0, padx=5, pady=5)
        b_entry.grid(row=3, column=1, padx=5, pady=5)
        
        if metodo == "Bisección":
            frame_titulo.config(text="Método de Bisección")
        else:
            frame_titulo.config(text="Método de Falsa Posición")

# Configuración de la interfaz
ventana = tk.Tk()
ventana.title("CALCULADORA DE RAÍCES DE ECUACIONES")
ventana.configure(bg='#f0e1d2')

# Estilo para la interfaz
style = ttk.Style()
style.configure("TFrame", background="#f0e1d2")
style.configure("TLabel", background="#f0e1d2", foreground="darkred", font=("Helvetica", 10))
style.configure("TButton", background="#ff6666", foreground="black", font=("Helvetica", 10, "bold"))
style.map("TButton", 
          background=[("active", "#ff3333")],
          foreground=[("active", "white")])
style.configure("TEntry", fieldbackground="#fff2e6", relief="solid", borderwidth=2)
style.configure("TCombobox", fieldbackground="#fff2e6")
style.configure("Datos.TLabelframe", background="#f0e1d2", borderwidth=3, relief="ridge")
style.configure("Datos.TLabelframe.Label", foreground="darkred", background="#f0e1d2", font=("Helvetica", 11, "bold"))
style.configure("Excel.Treeview", 
                background="white", 
                foreground="black", 
                rowheight=25, 
                fieldbackground="white",
                font=("Arial", 9))
style.configure("Excel.Treeview.Heading", 
                background="#d9e1f2", 
                foreground="#000000", 
                relief="flat", 
                font=("Arial", 10, "bold"),
                borderwidth=1)
style.map("Excel.Treeview", 
          background=[("selected", "#b8cce4")],
          foreground=[("selected", "black")])
style.layout("Excel.Treeview", [
    ('Excel.Treeview.treearea', {'sticky': 'nswe'})
])

# Marco principal
marco_principal = ttk.Frame(ventana)
marco_principal.grid(row=0, column=0, padx=10, pady=10)
marco_principal.configure(style="TFrame")

# Marco de entrada de datos
frame_titulo = ttk.LabelFrame(marco_principal, text="Método de Bisección", padding="10", width=350, style="Datos.TLabelframe")
frame_titulo.grid(row=0, column=0, padx=10, pady=10)

x = symbols("x")

# Campos de entrada
ttk.Label(frame_titulo, text="Función (en términos de x):", foreground="#990000").grid(row=0, column=0, padx=5, pady=5)
funcion_entry = ttk.Entry(frame_titulo, width=30)
funcion_entry.grid(row=0, column=1, padx=5, pady=5)

ttk.Label(frame_titulo, text="Método:", foreground="#990000").grid(row=1, column=0, padx=5, pady=5)
metodo_combo = ttk.Combobox(frame_titulo, width=28, state="readonly")
metodo_combo['values'] = ('Bisección', 'Falsa Posición', 'Newton-Raphson')
metodo_combo.current(0)  # Por defecto, seleccionamos Bisección
metodo_combo.grid(row=1, column=1, padx=5, pady=5)
metodo_combo.bind("<<ComboboxSelected>>", actualizar_campos)

# Campos para intervalos [a,b]
a_label = ttk.Label(frame_titulo, text="Valor inicial a:", foreground="#990000")
a_label.grid(row=2, column=0, padx=5, pady=5)
a_entry = ttk.Entry(frame_titulo, width=30)
a_entry.grid(row=2, column=1, padx=5, pady=5)

b_label = ttk.Label(frame_titulo, text="Valor inicial b:", foreground="#990000")
b_label.grid(row=3, column=0, padx=5, pady=5)
b_entry = ttk.Entry(frame_titulo, width=30)
b_entry.grid(row=3, column=1, padx=5, pady=5)

# Campo para punto inicial Newton-Raphson (inicialmente oculto)
x0_label = ttk.Label(frame_titulo, text="Punto inicial x₀:", foreground="#990000")
x0_entry = ttk.Entry(frame_titulo, width=30)
x0_label.grid_remove()  # Inicialmente oculto
x0_entry.grid_remove()  # Inicialmente oculto

# Criterios de parada comunes
ttk.Label(frame_titulo, text="Criterio de tolerancia:", foreground="#990000").grid(row=4, column=0, padx=5, pady=5)
crit_entry = ttk.Entry(frame_titulo, width=30)
crit_entry.grid(row=4, column=1, padx=5, pady=5)
crit_entry.insert(0, "0.0001")  # Valor por defecto

ttk.Label(frame_titulo, text="Máximo de iteraciones:", foreground="#990000").grid(row=5, column=0, padx=5, pady=5)
iter_entry = ttk.Entry(frame_titulo, width=30)
iter_entry.grid(row=5, column=1, padx=5, pady=5)
iter_entry.insert(0, "100")  # Valor por defecto

# Botón calcular
accion = ttk.Button(frame_titulo, text="Calcular", command=calcular, style="TButton")
accion.grid(row=6, column=0, columnspan=2, pady=10)

# Marco para gráfica
frame_grafica = ttk.Frame(marco_principal)
frame_grafica.grid(row=0, column=1, padx=5, pady=5)

# Marco para tabla de resultados
frame_tabla_container = ttk.LabelFrame(ventana, text="Resultados del Método", style="Datos.TLabelframe")
frame_tabla_container.grid(row=6, column=0, columnspan=2, padx=10, pady=10, sticky="nsew")

frame_tabla = ttk.Frame(frame_tabla_container)
frame_tabla.pack(fill="both", expand=True, padx=5, pady=5)

# Tabla de resultados
columns = ("i", "a", "b", "c", "f(c)")
tabla_tree = ttk.Treeview(frame_tabla, columns=columns, show="headings", style="Excel.Treeview")

# Configuración de columnas
for col in columns:
    tabla_tree.heading(col, text=col)
    tabla_tree.column(col, width=100, anchor="center")

tabla_tree.tag_configure('evenrow', background='#ffffff')
tabla_tree.tag_configure('oddrow', background='#f0f0f0')

# Scrollbars
scroll_y = ttk.Scrollbar(frame_tabla, orient="vertical", command=tabla_tree.yview)
scroll_x = ttk.Scrollbar(frame_tabla, orient="horizontal", command=tabla_tree.xview)
tabla_tree.configure(yscrollcommand=scroll_y.set, xscrollcommand=scroll_x.set)
scroll_y.pack(side="right", fill="y")
scroll_x.pack(side="bottom", fill="x")
tabla_tree.pack(fill="both", expand=True)

# Etiqueta para mostrar resultado final
resultado_label = ttk.Label(ventana, text="", font=("Arial", 10, "bold"), foreground="#990000")
resultado_label.grid(row=7, column=0, columnspan=2, pady=5)

# Menú
menubar = tk.Menu(ventana)
filemenu = tk.Menu(menubar, tearoff=0)
filemenu.add_command(label="Salir", command=ventana.quit)
menubar.add_cascade(label="Archivo", menu=filemenu)
ventana.config(menu=menubar)

# Establecer enfoque inicial y lanzar
funcion_entry.focus()
ventana.mainloop()