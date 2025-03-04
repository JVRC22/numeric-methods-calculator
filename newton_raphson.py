import tkinter as tk
from tkinter import ttk, messagebox
import numpy as np
import json
import pyperclip
import sympy as sp

class NewtonRaphson(tk.Toplevel):
    def __init__(self, master):
        super().__init__(master)

        self.title("Método de Newton-Raphson")
        self.geometry("600x650")
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

        ttk.Label(frame, text="Método de Newton-Raphson", font=("Arial", 14, "bold")).pack(pady=10)
        ttk.Label(frame, text="Función f(x):").pack(anchor="w")

        self.function_entry = ttk.Entry(frame, width=30)
        self.function_entry.pack(pady=5)
        self.function_entry.bind("<KeyRelease>", self.update_derivative)

        ttk.Label(frame, text="Derivada f'(x):").pack(anchor="w")
        self.derivative_entry = ttk.Entry(frame, width=30, state="readonly")
        self.derivative_entry.pack(pady=5)

        self._create_numeric_input(frame, "Valor Inicial (x0):", "x0_entry")
        self._create_numeric_input(frame, "Decimales de Precisión:", "precision_entry", default_value="4")

        execute_button = ttk.Button(frame, text="Calcular", command=self.calculate)
        execute_button.pack(pady=10)

        self.tree = ttk.Treeview(frame, columns=("Iteración", "x", "Xn+1"), show="headings")
        self.tree.heading("Iteración", text="Iteración")
        self.tree.heading("x", text="Xn")
        self.tree.heading("Xn+1", text="Xn+1")
        self.tree.pack(pady=10, fill="both", expand=True)

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
        ttk.Label(parent, text=label_text).pack(anchor="w")
        entry = ttk.Entry(parent, width=15, validate="key", font=("Arial", 14),
                          validatecommand=(self.register(self._validate_numeric), "%P"))
        entry.pack(pady=5)
        setattr(self, attr_name, entry)
        if default_value:
            entry.insert(0, default_value)

    def _validate_numeric(self, value):
        return value == "" or value.replace(".", "", 1).isdigit()

    def update_derivative(self, event=None):
        try:
            function_str = self.function_entry.get()
            if function_str.strip() == "":
                self.derivative_entry.config(state="normal")
                self.derivative_entry.delete(0, "end")
                self.derivative_entry.config(state="readonly")
                return

            x = sp.symbols("x")
            function_expr = sp.sympify(function_str, locals={"np": np})
            derivative_expr = sp.diff(function_expr, x)

            self.derivative_entry.config(state="normal")
            self.derivative_entry.delete(0, "end")
            self.derivative_entry.insert(0, str(derivative_expr))
            self.derivative_entry.config(state="readonly")
        except Exception:
            pass

    def calculate(self):
        try:
            function_str = self.function_entry.get()
            derivative_str = self.derivative_entry.get()
            x0 = float(self.x0_entry.get())
            precision = int(self.precision_entry.get())

            if not function_str or not derivative_str:
                messagebox.showerror("Error", "Debes ingresar una función válida.")
                return

            func = lambda x: eval(function_str, {"x": x, "np": np})
            dfunc = lambda x: eval(derivative_str, {"x": x, "np": np})

            for entry in [self.function_entry, self.derivative_entry, self.x0_entry, self.precision_entry]:
                entry.config(state="disabled")

            self.tree.delete(*self.tree.get_children())
            self.results = []

            x = x0
            i = 0
            MAX_LIMIT = 1e100  # Límite de valores permitidos para evitar errores

            while True:
                try:
                    fx = func(x)
                    dfx = dfunc(x)

                    if dfx == 0:
                        # messagebox.showerror("Error", "Derivada igual a cero. No se puede continuar.")
                        break

                    x_new = x - fx / dfx

                    # Verificar si el nuevo valor es demasiado grande
                    if abs(x_new) > MAX_LIMIT:
                        # messagebox.showwarning("Advertencia", "Valor demasiado grande. Se detiene el cálculo.")
                        break

                    rounded_x = round(x_new, precision)

                    self.results.append({"Iteración": i, "x": round(x, precision), "Xn+1": rounded_x})
                    self.tree.insert("", "end", values=(i, round(x, precision), rounded_x))

                    # Condición de parada: Si el valor de Xn redondeado no cambia, detener iteraciones
                    if round(x, precision) == rounded_x:
                        break

                    x = x_new
                    i += 1

                except OverflowError:
                    # messagebox.showwarning("Advertencia", "Cálculo fuera de rango. Se detiene el proceso.")
                    break

            # messagebox.showinfo("Resultado", "Cálculo completado.")
        except Exception as e:
            messagebox.showerror("Error", f"Error: {str(e)}")

    def clear_inputs(self):
        for entry in [self.function_entry, self.derivative_entry, self.x0_entry, self.precision_entry]:
            entry.config(state="normal")
            entry.delete(0, "end")
        self.tree.delete(*self.tree.get_children())
        self.results = []

    def edit_inputs(self):
        for entry in [self.function_entry, self.derivative_entry, self.x0_entry, self.precision_entry]:
            entry.config(state="normal")

    def copy_as_json(self):
        data = {
            "function": self.function_entry.get(),
            "derivative": self.derivative_entry.get(),
            "x0": self.x0_entry.get(),
            "precision": self.precision_entry.get(),
            "results": self.results
        }
        pyperclip.copy(json.dumps(data, indent=4))
        messagebox.showinfo("Copiado", "Resultados copiados como JSON.")

    def show_guide(self):
        guide_window = tk.Toplevel(self)
        guide_window.title("Guía de Uso")
        guide_window.geometry("400x200")
        guide_window.configure(bg="#333333")

        ttk.Label(guide_window, text="Guía para escribir funciones", font=("Arial", 12, "bold"),
                  background="#333333", foreground="white").pack(pady=10)
        guide_text = (
            "- Usa 'x' como variable\n"
            "- Exponentes: x**2 (para x²)\n"
            "- Raíz cuadrada: np.sqrt(x)\n"
            "- Trigonometría: np.sin(x), np.cos(x), np.tan(x)\n"
            "- Exponencial: np.exp(x)\n"
            "- Logaritmo: np.log(x)\n"
        )
        ttk.Label(guide_window, text=guide_text, background="#333333", foreground="white",
                  justify="left").pack(padx=10, pady=5)
        ttk.Button(guide_window, text="Cerrar", command=guide_window.destroy).pack(pady=10)

if __name__ == "__main__":
    root = tk.Tk()
    root.withdraw()
    app = NewtonRaphson(root)
    app.mainloop()