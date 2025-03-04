import tkinter as tk
from tkinter import ttk, messagebox
import numpy as np
import json
import pyperclip

class ImprovedEuler(tk.Toplevel):
    def __init__(self, master):
        super().__init__(master)
        
        self.title("Método de Euler Mejorado")
        self.geometry("700x800")
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
        frame = ttk.Frame(self, padding=10, style="TFrame")
        frame.pack(expand=True, fill="both")
        
        ttk.Label(frame, text="Método de Euler Mejorado", font=("Arial", 14, "bold")).pack(pady=10)
        ttk.Label(frame, text="Función f(x, y):").pack(anchor="w")
        self.function_entry = ttk.Entry(frame, width=30)
        self.function_entry.pack(pady=5)
        
        self._create_numeric_input(frame, "Valor Inicial de x (x0):", "x0_entry")
        self._create_numeric_input(frame, "Valor Inicial de y (y0):", "y0_entry")
        self._create_numeric_input(frame, "Tamaño de Paso (h):", "h_entry")
        self._create_numeric_input(frame, "Última Iteración (xf):", "x_target_entry")
        self._create_numeric_input(frame, "Decimales de Precisión:", "precision_entry", default_value="4")
        
        execute_button = ttk.Button(frame, text="Calcular", command=self.calculate)
        execute_button.pack(pady=10)
        
        self.tree = ttk.Treeview(frame, columns=("Iteración", "x", "y_n", "y_n+1", "Error"), show="headings")
        self.tree.heading("Iteración", text="Iteración")
        self.tree.heading("x", text="x")
        self.tree.heading("y_n", text="yₙ")
        self.tree.heading("y_n+1", text="yₙ₊₁")
        self.tree.heading("Error", text="Error")
        self.tree.pack(pady=10, fill="both", expand=True)
        
        control_frame = ttk.Frame(self, style="TFrame")
        control_frame.pack(side="bottom", fill="x", pady=10)
        
        ttk.Button(control_frame, text="Limpiar", command=self.clear_inputs).pack(side="left", padx=5)
        ttk.Button(control_frame, text="Editar", command=self.edit_inputs).pack(side="left", padx=5)
        ttk.Button(control_frame, text="Copiar como JSON", command=self.copy_as_json).pack(side="left", padx=5)
        ttk.Button(control_frame, text="Guía de Uso", command=self.show_guide).pack(side="left", padx=5)
        ttk.Button(control_frame, text="Salir", command=self.destroy).pack(side="right", padx=5)
    
    def _create_numeric_input(self, parent, label_text, attr_name, default_value=""):
        ttk.Label(parent, text=label_text).pack(anchor="w")
        entry = ttk.Entry(parent, width=15, validate="key", font=("Arial", 14), validatecommand=(self.register(self._validate_numeric), "%P"))
        entry.pack(pady=5)
        setattr(self, attr_name, entry)
        if default_value:
            entry.insert(0, default_value)
    
    def _validate_numeric(self, value):
        if value == "" or value.replace(".", "", 1).isdigit():
            return True
        return False
    
    def calculate(self):
        try:
            function_str = self.function_entry.get()
            x0 = float(self.x0_entry.get())
            y0 = float(self.y0_entry.get())
            h = float(self.h_entry.get())
            x_target = float(self.x_target_entry.get())
            precision = int(self.precision_entry.get())
            
            func = lambda x, y: eval(function_str, {"x": x, "y": y, "np": np, "exp": np.exp, "sin": np.sin, "cos": np.cos, "tan": np.tan})
            
            for entry in [self.function_entry, self.x0_entry, self.y0_entry, self.h_entry, self.x_target_entry, self.precision_entry]:
                entry.config(state="disabled")
            
            self.tree.delete(*self.tree.get_children())
            self.results = []
            
            iterations = int(round((x_target - x0) / h)) + 1
            x, y = x0, y0
            for i in range(iterations):
                y_pred = y + h * func(x, y)
                y_corr = y + (h / 2) * (func(x, y) + func(x + h, y_pred))
                error = abs(y_corr - y_pred)  # Cálculo del error absoluto
                
                self.results.append({
                    "Iteración": i,
                    "x": round(x, precision),
                    "y_n": round(y, precision),
                    "y_n+1": round(y_corr, precision),
                    "Error": round(error, precision)
                })
                self.tree.insert("", "end", values=(i, round(x, precision), round(y, precision), round(y_corr, precision), round(error, precision)))
                
                y = y_corr
                x += h
            
            # messagebox.showinfo("Resultado", "Cálculo completado.")
        except Exception as e:
            messagebox.showerror("Error", f"Error: {str(e)}")
    
    def clear_inputs(self):
        for entry in [self.function_entry, self.x0_entry, self.y0_entry, self.h_entry, self.x_target_entry, self.precision_entry]:
            entry.config(state="normal")
            entry.delete(0, "end")
        
        self.precision_entry.insert(0, "4")
        self.tree.delete(*self.tree.get_children())
        self.results = []
    
    def edit_inputs(self):
        for entry in [self.function_entry, self.x0_entry, self.y0_entry, self.h_entry, self.x_target_entry, self.precision_entry]:
            entry.config(state="normal")
    
    def copy_as_json(self):
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
        messagebox.showinfo("Copiado", "Resultados copiados como JSON.")

    def show_guide(self):
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
        
        ttk.Button(guide_window, text="Cerrar", command=guide_window.destroy).pack(pady=10)
        
if __name__ == "__main__":
    root = tk.Tk()
    root.withdraw()  
    app = ImprovedEuler(root)
    app.mainloop()