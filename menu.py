import tkinter as tk
from tkinter import ttk, messagebox
import improved_euler
import newton_raphson
import runge_kutta

class Menu(tk.Tk):
    # Function to initialize the calculator.
    def __init__(self):
        super().__init__()

        # Sets the title, size, and background color of the calculator.
        self.title("Numerical Methods Calculator")
        self.geometry("450x500")
        self.resizable(False, False)
        self.configure(bg="#333333")

        self.style = ttk.Style()
        self.style.configure("TFrame", background="#333333")
        self.style.configure("TLabel", background="#333333", foreground="white", font=("Arial", 16))
        self.style.configure("TButton", font=("Arial", 14), background="#444444", foreground="white")
        self.style.configure("TRadiobutton", background="#333333", foreground="white", font=("Arial", 14))
        self.style.map("TButton", background=[("active", "#555555")])

        # Variable to store the selected method.
        self.current_method = tk.IntVar(value=1)

        # Creates the interface for the calculator.
        self._create_interface()

    # Function to create the interface for the calculator.
    def _create_interface(self):
        # Main container with padding
        frame = ttk.Frame(self, padding=10, style="TFrame")
        frame.pack(expand=True, fill="both")

        # Labels
        ttk.Label(frame, text="Proyecto: Calculadora de Métodos Numéricos").pack(anchor="w", pady=3)
        ttk.Label(frame, text="Materia: Matemáticas para Ingeniería II").pack(anchor="w", pady=3)
        ttk.Label(frame, text="Nombre: Javier Resendiz Carpio").pack(anchor="w", pady=3)
        ttk.Label(frame, text="Grado y Sección: 8vo C").pack(anchor="w", pady=3)
        
        # Method selection label
        ttk.Label(frame, text="Seleccione un método:", font=("Arial", 12, "bold")).pack(pady=10)
        
        # Centered method selection radio buttons
        method_frame = ttk.Frame(frame, style="TFrame")
        method_frame.pack()
        self._create_check_option(method_frame, "Euler Mejorado", 1)
        self._create_check_option(method_frame, "Runge-Kutta", 2)
        self._create_check_option(method_frame, "Newton-Raphson", 3)
        
        # Centered execute button
        execute_button = ttk.Button(frame, text="Ejecutar", command=self.execute_selected_method)
        execute_button.pack(pady=10)
        
        # Close button at the bottom right
        close_button_frame = ttk.Frame(self, style="TFrame")
        close_button_frame.pack(side="bottom", fill="x", pady=10)
        close_button = ttk.Button(close_button_frame, text="Salir", command=self.close)
        close_button.pack(side="right", padx=10)

    # Creates a check option for method selection.
    def _create_check_option(self, parent, text, value):
        radio = ttk.Radiobutton(parent, text=text, variable=self.current_method, value=value, style="TRadiobutton")
        radio.pack(anchor="w", padx=10, pady=2)

    def execute_selected_method(self):
        # Executes the selected numerical method.
        method = self.current_method.get()
        
        match method:
            case 1:
                improved_euler.ImprovedEuler(self)
            case 2:
                runge_kutta.RungeKutta(self)
            case 3:
                newton_raphson.NewtonRaphson(self)
            case _:
                messagebox.showerror("Error", "Please select a valid method.")

    def close(self):
        # Closes the application with a farewell message.
        # messagebox.showinfo("Exit", "Hasta luego!!!")
        self.destroy()

if __name__ == "__main__":
    app = Menu()
    app.mainloop()
