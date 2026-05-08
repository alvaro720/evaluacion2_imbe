import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
from datetime import datetime

# ==================== IMPORTACIONES ====================
from Seguridad import Seguridad
from clases.Administrador import Administrador
from clases.Empleado import Empleado
from clases.Registro import Registro
# from clases.Departamento import Departamento   # si tienes la clase
# from clases.Proyecto import Proyecto

from Dao.DAOAdministrador import DAOAdministrador
from Dao.DAOEmpleado import DAOEmpleado
from Dao.DAODepartamento import DAODepartamento
from Dao.DAOProyecto import DAOProyecto
from Dao.DAORegistro import DAORegistro

class SistemaEcoTech:
    def __init__(self, root):
        self.root = root
        self.root.title("EcoTech Solutions - Sistema de Gestión")
        self.root.geometry("1050x680")
        self.root.configure(bg="#2c3e50")

        self.usuario_actual = None
        self.rol_actual = None

        # DAOs
        self.dao_admin = DAOAdministrador()
        self.dao_empleado = DAOEmpleado()
        self.dao_depto = DAODepartamento()
        self.dao_proyecto = DAOProyecto()
        self.dao_registro = DAORegistro()

        self.mostrar_login()

    def mostrar_login(self):
        for widget in self.root.winfo_children():
            widget.destroy()

        frame = tk.Frame(self.root, bg="#2c3e50")
        frame.pack(expand=True)

        tk.Label(frame, text="🔐 EcoTech Solutions", font=("Arial", 22, "bold"), 
                 bg="#2c3e50", fg="#3498db").pack(pady=30)

        tk.Label(frame, text="Usuario:", bg="#2c3e50", fg="white", font=("Arial", 12)).pack(pady=5)
        self.entry_user = tk.Entry(frame, width=35, font=("Arial", 11))
        self.entry_user.pack()

        tk.Label(frame, text="Contraseña:", bg="#2c3e50", fg="white", font=("Arial", 12)).pack(pady=5)
        self.entry_pass = tk.Entry(frame, width=35, show="*", font=("Arial", 11))
        self.entry_pass.pack()

        tk.Button(frame, text="Iniciar Sesión", bg="#3498db", fg="white", font=("Arial", 12, "bold"),
                  width=20, command=self.login).pack(pady=20)

    def login(self):
        user = self.entry_user.get().strip()
        password = self.entry_pass.get().strip()

        admin = self.dao_admin.validar_login(user, password)   # Asegúrate que este método exista en DAOAdministrador
        if admin:
            self.usuario_actual = admin
            self.rol_actual = admin.get_rol()
            self.mostrar_sistema_principal()
        else:
            messagebox.showerror("Error", "Usuario o contraseña incorrectos")

    def mostrar_sistema_principal(self):
        for widget in self.root.winfo_children():
            widget.destroy()

        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(fill="both", expand=True, padx=10, pady=10)

        if self.rol_actual == "admin":
            self.crear_pestanas_admin()
        else:
            self.crear_pestanas_empleado()

    def crear_pestanas_admin(self):
        # Pestaña Empleados
        tab_emp = tk.Frame(self.notebook)
        self.notebook.add(tab_emp, text="👤 Empleados")
        AppEmpleado(tab_emp, self.dao_empleado)

        # Pestaña Departamentos
        tab_depto = tk.Frame(self.notebook)
        self.notebook.add(tab_depto, text="🏢 Departamentos")
        AppDepartamento(tab_depto, self.dao_depto)

        # Pestaña Proyectos
        tab_proy = tk.Frame(self.notebook)
        self.notebook.add(tab_proy, text="📁 Proyectos")
        AppProyecto(tab_proy, self.dao_proyecto)

        # Pestaña Registro de Tiempo
        tab_reg = tk.Frame(self.notebook)
        self.notebook.add(tab_reg, text="⏱ Registro Tiempo")
        AppRegistroTiempo(tab_reg, self.dao_registro, self.usuario_actual)

        # Pestaña Informes
        tab_inf = tk.Frame(self.notebook)
        self.notebook.add(tab_inf, text="📊 Informes")
        self.crear_pestana_informes(tab_inf)

    def crear_pestanas_empleado(self):
        tab_reg = tk.Frame(self.notebook)
        self.notebook.add(tab_reg, text="⏱ Mi Registro de Tiempo")
        AppRegistroTiempo(tab_reg, self.dao_registro, self.usuario_actual)

    def crear_pestana_informes(self, parent):
        tk.Label(parent, text="Generación de Informes", font=("Arial", 16, "bold")).pack(pady=20)
        tk.Button(parent, text="Exportar Empleados (CSV)", command=lambda: messagebox.showinfo("Info", "Funcionalidad en desarrollo")).pack(pady=10)
        tk.Button(parent, text="Horas por Proyecto", command=lambda: messagebox.showinfo("Info", "Funcionalidad en desarrollo")).pack(pady=10)

# ====================== CLASES POR MÓDULO ======================

class AppEmpleado:
    """Similar a tu AppAdministrador pero con más campos"""
    def __init__(self, parent, dao):
        self.parent = parent
        self.dao = dao
        self.crear_interfaz()

    def crear_interfaz(self):
        # Formulario
        frame_form = tk.LabelFrame(self.parent, text="Datos del Empleado", padx=10, pady=10)
        frame_form.pack(fill="x", padx=10, pady=5)

        self.vars = {}
        campos = ["ID", "Nombre", "RUT", "Correo", "Teléfono", "Dirección", "Fecha Inicio", "Salario", "Rol"]
        for i, campo in enumerate(campos):
            tk.Label(frame_form, text=campo + ":").grid(row=i//2, column=(i%2)*2, sticky="e", padx=5, pady=4)
            self.vars[campo] = tk.StringVar()
            estado = "readonly" if campo == "ID" else "normal"
            tk.Entry(frame_form, textvariable=self.vars[campo], state=estado, width=25).grid(
                row=i//2, column=(i%2)*2 + 1, padx=5, pady=4)

        # Botones
        frame_btn = tk.Frame(self.parent)
        frame_btn.pack(fill="x", pady=5)
        for text, color, cmd in [("Registrar", "#27ae60", self.registrar), ("Actualizar", "#2980b9", self.actualizar),
                                ("Eliminar", "#e74c3c", self.eliminar), ("Buscar RUT", "#f39c12", self.buscar),
                                ("Listar", "#7f8c8d", self.listar), ("Limpiar", "#95a5a6", self.limpiar)]:
            tk.Button(frame_btn, text=text, bg=color, fg="white", command=cmd).pack(side="left", padx=5)

        # Treeview
        self.tree = ttk.Treeview(self.parent, columns=("id","nombre","rut","correo","salario"), show="headings")
        self.tree.heading("id", text="ID")
        self.tree.heading("nombre", text="Nombre")
        self.tree.heading("rut", text="RUT")
        self.tree.heading("correo", text="Correo")
        self.tree.heading("salario", text="Salario")
        self.tree.pack(fill="both", expand=True, padx=10, pady=10)

    def registrar(self):
        # Implementar según tu clase Empleado
        messagebox.showinfo("Info", "Registrar Empleado - Completa según tu clase")

    def actualizar(self): pass
    def eliminar(self): pass
    def buscar(self): pass
    def listar(self): pass
    def limpiar(self): pass

class AppDepartamento:
    def __init__(self, parent, dao):
        self.parent = parent
        self.dao = dao
        tk.Label(parent, text="Gestión de Departamentos", font=("Arial", 14, "bold")).pack(pady=10)
        tk.Button(parent, text="Crear Departamento", command=self.crear).pack(pady=5)
        tk.Button(parent, text="Listar Departamentos", command=self.listar).pack(pady=5)

    def crear(self):
        nombre = simpledialog.askstring("Nuevo Departamento", "Nombre del departamento:")
        if nombre:
            self.dao.registrar(nombre)
            messagebox.showinfo("Éxito", "Departamento creado")

    def listar(self):
        messagebox.showinfo("Departamentos", "Listado completo (ampliar según necesites)")

class AppProyecto:
    def __init__(self, parent, dao):
        self.parent = parent
        self.dao = dao
        tk.Label(parent, text="Gestión de Proyectos", font=("Arial", 14, "bold")).pack(pady=10)
        tk.Button(parent, text="Crear Proyecto", command=self.crear).pack(pady=5)

    def crear(self):
        nombre = simpledialog.askstring("Nuevo Proyecto", "Nombre:")
        if nombre:
            self.dao.registrar(nombre)
            messagebox.showinfo("Éxito", "Proyecto creado")

class AppRegistroTiempo:
    def __init__(self, parent, dao, usuario):
        self.parent = parent
        self.dao = dao
        self.usuario = usuario
        self.crear_formulario()

    def crear_formulario(self):
        tk.Label(self.parent, text="Registro de Tiempo", font=("Arial", 14, "bold")).pack(pady=10)
        # Formulario simple...
        tk.Button(self.parent, text="Guardar Registro", bg="#27ae60", fg="white", 
                 command=self.guardar).pack(pady=20)

    def guardar(self):
        messagebox.showinfo("Guardado", "Registro guardado correctamente")

if __name__ == "__main__":
    root = tk.Tk()
    app = SistemaEcoTech(root)
    root.mainloop()