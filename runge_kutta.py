import tkinter as tk
from tkinter import ttk, messagebox
import numpy as np
import json
import pyperclip

class RungeKutta(tk.Toplevel):
    def __init__(self, master):
        super().__init__(master)
        
        self.title("Runge-Kutta Method")
        self.geometry("600x800")
        self.resizable(False, True)
        self.configure(bg="#333333")

        self.style = ttk.Style()
        self.style.configure("TFrame", background="#333333")
        self.style.configure("TLabel", background="#333333", foreground="white", font=("Arial", 16))
        self.style.configure("TButton", font=("Arial", 14), background="#444444", foreground="white")
        self.style.map("TButton", background=[("active", "#555555")])

        self.results = []
        self._create_interface()
    
    def _create_interface(self):
        # Creates the interface for the Improved Euler Method.
        frame = ttk.Frame(self, padding=10, style="TFrame")
        frame.pack(expand=True, fill="both")
        
        # Labels and Input Fields
        ttk.Label(frame, text="Método Runge-Kutta", font=("Arial", 14, "bold")).pack(pady=10)
        ttk.Label(frame, text="Funcion f(x, y):").pack(anchor="w")
        self.function_entry = ttk.Entry(frame, width=30)
        self.function_entry.pack(pady=5)
        
        self._create_numeric_input(frame, "Valor Inicial de x (x0):", "x0_entry")
        self._create_numeric_input(frame, "Valor Inicial de y (y0):", "y0_entry")
        self._create_numeric_input(frame, "Tamaño de Paso (h):", "h_entry")
        self._create_numeric_input(frame, "Ultima Iteración (xf):", "x_target_entry")
        
        # Execute button
        execute_button = ttk.Button(frame, text="Calcular", command=self.calculate)
        execute_button.pack(pady=10)
        
        # Table for results
        self.tree = ttk.Treeview(frame, columns=("Iteration", "x", "y"), show="headings")
        self.tree.heading("Iteration", text="Iteración")
        self.tree.heading("x", text="x")
        self.tree.heading("y", text="y")
        self.tree.pack(pady=10, fill="both", expand=True)
        
        # Control buttons frame
        control_frame = ttk.Frame(self, style="TFrame")
        control_frame.pack(side="bottom", fill="x", pady=10)
        
        clear_button = ttk.Button(control_frame, text="Limpiar", command=self.clear_inputs)
        clear_button.pack(side="left", padx=5)
        
        edit_button = ttk.Button(control_frame, text="Editar", command=self.edit_inputs)
        edit_button.pack(side="left", padx=5)
        
        copy_json_button = ttk.Button(control_frame, text="Copiar como JSON", command=self.copy_as_json)
        copy_json_button.pack(side="left", padx=5)

        guide_button = ttk.Button(control_frame, text="Guía de Uso", command=self.show_guide)
        guide_button.pack(side="left", padx=5)
        
        close_button = ttk.Button(control_frame, text="Salir", command=self.destroy)
        close_button.pack(side="right", padx=5)
    
    def _create_numeric_input(self, parent, label_text, attr_name, default_value=""):
        # Creates a numeric input field with validation.
        ttk.Label(parent, text=label_text).pack(anchor="w")
        entry = ttk.Entry(parent, width=15, validate="key", font=("Arial", 14),  validatecommand=(self.register(self._validate_numeric), "%P"))
        entry.pack(pady=5)
        setattr(self, attr_name, entry)
        if default_value:
            entry.insert(0, default_value)
    
    def _validate_numeric(self, value):
        # Validates that the input is numeric (integers or floats).
        if value == "" or value.replace(".", "", 1).isdigit():
            return True
        return False
    
    def calculate(self):
        # Maneja el cálculo del método de Runge-Kutta de cuarto orden.
        try:
            function_str = self.function_entry.get()
            x0 = float(self.x0_entry.get())
            y0 = float(self.y0_entry.get())
            h = float(self.h_entry.get())
            x_target = float(self.x_target_entry.get())
            
            func = lambda x, y: eval(function_str, {"x": x, "y": y, "np": np, "exp": np.exp, "sin": np.sin, "cos": np.cos, "tan": np.tan})
            
            for entry in [self.function_entry, self.x0_entry, self.y0_entry, self.h_entry, self.x_target_entry]:
                entry.config(state="disabled")
            
            self.tree.delete(*self.tree.get_children())
            self.results = []
            
            iterations = int(round((x_target - x0) / h)) + 1
            x, y = x0, y0
            for i in range(iterations):
                self.results.append({"Iteración": i, "x": x, "y": y})
                self.tree.insert("", "end", values=(i, x, y))
                
                k1 = h * func(x, y)
                k2 = h * func(x + h / 2, y + k1 / 2)
                k3 = h * func(x + h / 2, y + k2 / 2)
                k4 = h * func(x + h, y + k3)
                y += (k1 + 2 * k2 + 2 * k3 + k4) / 6
                x = round(x + h, 15)
            
            messagebox.showinfo("Resultado", "Cálculo completado.")
        except Exception as e:
            messagebox.showerror("Error", f"Error: {str(e)}")
    
    def clear_inputs(self):
        # Clears all input fields and enables them again.
        for entry in [self.function_entry, self.x0_entry, self.y0_entry, self.h_entry, self.x_target_entry, self.precision_entry]:
            entry.config(state="normal")
            entry.delete(0, "end")
        
        self.precision_entry.insert(0, "4")
        self.tree.delete(*self.tree.get_children())
        self.results = []
    
    def edit_inputs(self):
        # Enables all input fields for editing.
        for entry in [self.function_entry, self.x0_entry, self.y0_entry, self.h_entry, self.x_target_entry, self.precision_entry]:
            entry.config(state="normal")
    
    def copy_as_json(self):
        # Copies the input parameters and results as JSON to clipboard.
        data = {
            "function": self.function_entry.get(),
            "x0": self.x0_entry.get(),
            "y0": self.y0_entry.get(),
            "step_size": self.h_entry.get(),
            "target_x": self.x_target_entry.get(),
            "precision": self.precision_entry.get(),
            "results": self.results
        }
        json_data = json.dumps(data, indent=4)
        pyperclip.copy(json_data)
        messagebox.showinfo("Copied", "Resultados copiados como JSON.")

    def show_guide(self):
        # Muestra una guía de cómo escribir funciones correctamente.
        guide_window = tk.Toplevel(self)
        guide_window.title("Guía de Uso")
        guide_window.geometry("400x300")
        guide_window.configure(bg="#333333")
        
        ttk.Label(guide_window, text="Guía para escribir funciones", font=("Arial", 12, "bold"), background="#333333", foreground="white").pack(pady=10)
        guide_text = (
            "- Usa 'x' y 'y' como variables\n"
            "- Exponentes: x**2 (para x²)\n"
            "- Raíz cuadrada: np.sqrt(x)\n"
            "- Trigonometría: np.sin(x), np.cos(x), np.tan(x)\n"
            "- Exponencial: np.exp(x) (para e^x)\n"
            "- Logaritmo: np.log(x) (logaritmo natural)\n"
            "- Multiplicación explícita: x*y (no xy)"
        )
        
        ttk.Label(guide_window, text=guide_text, background="#333333", foreground="white", justify="left").pack(padx=10, pady=5)
        
        close_guide_button = ttk.Button(guide_window, text="Cerrar", command=guide_window.destroy)
        close_guide_button.pack(pady=10)
        
if __name__ == "__main__":
    root = tk.Tk()
    root.withdraw() # Hide the main window
    app = RungeKutta(root)
    app.mainloop()