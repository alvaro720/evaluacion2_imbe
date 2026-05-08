import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
from datetime import datetime

# ==================== IMPORTACIONES ====================
from clases.Registro import Registro
from Dao.DAORegistro import DAORegistro
from Dao.DAOProyecto import DAOProyecto


class PortalEmpleado:
    def __init__(self, root):
        self.root = root
        self.root.title("EcoTech Solutions - Portal Empleado")
        self.root.geometry("1150x720")
        self.root.configure(bg="#2c3e50")

        # DAOs
        self.dao_registro = DAORegistro()
        self.dao_proyecto = DAOProyecto()

        # Datos del empleado (puedes cambiarlos o cargarlos después)
        self.usuario_actual = {
            "id": 1,
            "nombre": "Juan Pérez",
            "rut": "12.345.678-9"
        }

        self.crear_menu_superior()
        self.mostrar_registrar_tiempo()  # Empieza en Registrar Tiempo

    def crear_menu_superior(self):
        menu = tk.Frame(self.root, bg="#34495e", height=70)
        menu.pack(fill="x", pady=5)
        menu.pack_propagate(False)

        tk.Label(menu, text=f"👤 {self.usuario_actual['nombre']}", 
                bg="#34495e", fg="white", font=("Arial", 12, "bold")).pack(side="left", padx=20)

        tk.Button(menu, text="📁 Mis Proyectos", bg="#3498db", fg="white", 
                 font=("Arial", 10, "bold"), command=self.mostrar_mis_proyectos).pack(side="left", padx=10)
        
        tk.Button(menu, text="⏱ Registrar Tiempo", bg="#27ae60", fg="white", 
                 font=("Arial", 10, "bold"), command=self.mostrar_registrar_tiempo).pack(side="left", padx=10)

        tk.Button(menu, text="Salir", bg="#e74c3c", fg="white", 
                 command=self.root.quit).pack(side="right", padx=20)

    # ====================== MIS PROYECTOS ======================
    def mostrar_mis_proyectos(self):
        for widget in self.root.winfo_children():
            if isinstance(widget, tk.Frame) and widget != self.root.winfo_children()[0]:
                widget.destroy()

        frame = tk.Frame(self.root, bg="#2c3e50")
        frame.pack(fill="both", expand=True)

        tk.Label(frame, text="📁 Mis Proyectos Asignados", font=("Arial", 18, "bold"), 
                bg="#2c3e50", fg="white").pack(pady=30)

        # Treeview de ejemplo
        tree = ttk.Treeview(frame, columns=("id", "nombre", "descripcion"), show="headings")
        tree.heading("id", text="ID")
        tree.heading("nombre", text="Proyecto")
        tree.heading("descripcion", text="Descripción")
        tree.pack(fill="both", expand=True, padx=20, pady=10)

        # Datos de ejemplo
        proyectos_ejemplo = [(1, "Energía Solar", "Instalación paneles"), 
                            (2, "Reciclaje Inteligente", "Sistema de clasificación")]
        for p in proyectos_ejemplo:
            tree.insert("", "end", values=p)

    # ====================== REGISTRAR TIEMPO ======================
    def mostrar_registrar_tiempo(self):
        for widget in self.root.winfo_children():
            if isinstance(widget, tk.Frame) and widget != self.root.winfo_children()[0]:
                widget.destroy()

        frame = tk.Frame(self.root, bg="#2c3e50")
        frame.pack(fill="both", expand=True)

        tk.Label(frame, text="⏱ Registrar Tiempo Trabajado", font=("Arial", 18, "bold"), 
                bg="#2c3e50", fg="white").pack(pady=20)

        form = tk.Frame(frame, bg="#2c3e50")
        form.pack(pady=10)

        self.var_fecha = tk.StringVar(value=datetime.now().strftime("%Y-%m-%d"))
        self.var_horas = tk.StringVar()
        self.var_proyecto = tk.StringVar()
        self.var_descripcion = tk.StringVar()

        tk.Label(form, text="Fecha:", bg="#2c3e50", fg="white").grid(row=0, column=0, padx=15, pady=10, sticky="e")
        tk.Entry(form, textvariable=self.var_fecha, width=30).grid(row=0, column=1, padx=10, pady=10)

        tk.Label(form, text="Horas trabajadas:", bg="#2c3e50", fg="white").grid(row=1, column=0, padx=15, pady=10, sticky="e")
        tk.Entry(form, textvariable=self.var_horas, width=30).grid(row=1, column=1, padx=10, pady=10)

        tk.Label(form, text="ID Proyecto:", bg="#2c3e50", fg="white").grid(row=2, column=0, padx=15, pady=10, sticky="e")
        tk.Entry(form, textvariable=self.var_proyecto, width=30).grid(row=2, column=1, padx=10, pady=10)

        tk.Label(form, text="Descripción:", bg="#2c3e50", fg="white").grid(row=3, column=0, padx=15, pady=10, sticky="e")
        tk.Entry(form, textvariable=self.var_descripcion, width=55).grid(row=3, column=1, padx=10, pady=10)

        tk.Button(frame, text="💾 Guardar Registro", bg="#27ae60", fg="white", font=("Arial", 12, "bold"),
                  command=self.guardar_registro).pack(pady=25)

    def guardar_registro(self):
        try:
            reg = Registro(
                id_registro=0,
                fecha=self.var_fecha.get(),
                hora=self.var_horas.get(),
                descripcion=self.var_descripcion.get(),
                empleado=self.usuario_actual["id"],
                proyecto=int(self.var_proyecto.get() or 0)
            )

            self.dao_registro.registrar(reg)
            messagebox.showinfo("Éxito", "Registro de tiempo guardado correctamente")

            # Limpiar campos
            self.var_horas.set("")
            self.var_descripcion.set("")
            self.var_proyecto.set("")
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo guardar el registro:\n{str(e)}")


if __name__ == "__main__":
    root = tk.Tk()
    app = PortalEmpleado(root)
    root.mainloop()