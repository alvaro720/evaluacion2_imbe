import tkinter as tk
from tkinter import ttk, messagebox

# ==================== IMPORTACIONES ====================
from clases.Administrador import Administrador
from clases.Empleado import Empleado

from Dao.DAOAdministrador import DAOAdministrador
from Dao.DAOEmpleado import DAOEmpleado
from Dao.DAODepartamento import DAODepartamento
from Dao.DAOProyecto import DAOProyecto
from Dao.DAORegistro import DAORegistro


class SistemaEcoTech:
    def __init__(self, root):
        self.root = root
        self.root.title("EcoTech Solutions - Sistema de Gestión")
        self.root.geometry("1180x740")
        self.root.configure(bg="#2c3e50")

        self.dao_admin = DAOAdministrador()
        self.dao_empleado = DAOEmpleado()
        self.dao_depto = DAODepartamento()
        self.dao_proyecto = DAOProyecto()
        self.dao_registro = DAORegistro()

        self.frame_actual = None

        self.crear_menu_superior()
        self.mostrar_empleados()

    def crear_menu_superior(self):
        menu = tk.Frame(self.root, bg="#34495e", height=65)
        menu.pack(fill="x", pady=5)
        menu.pack_propagate(False)

        botones = [
            ("👨‍💼 Administradores", self.mostrar_administradores),
            ("👤 Empleados", self.mostrar_empleados),
            ("🏢 Departamentos", self.mostrar_departamentos),
            ("📁 Proyectos", self.mostrar_proyectos),
            ("⏱ Registro Tiempo", self.mostrar_registro_tiempo)
        ]

        for texto, comando in botones:
            tk.Button(menu, text=texto, bg="#3498db", fg="white", 
                     font=("Arial", 10, "bold"), command=comando).pack(side="left", padx=12, pady=8)

    def cambiar_contenido(self, nuevo_frame):
        if self.frame_actual:
            self.frame_actual.destroy()
        nuevo_frame.pack(fill="both", expand=True)
        self.frame_actual = nuevo_frame

    # ==================== MÓDULOS ====================
    def mostrar_administradores(self):
        frame = tk.Frame(self.root, bg="#2c3e50")
        AppCRUD(frame, "Administrador", self.dao_admin, Administrador)
        self.cambiar_contenido(frame)

    def mostrar_empleados(self):
        frame = tk.Frame(self.root, bg="#2c3e50")
        AppEmpleado(frame, self.dao_empleado)
        self.cambiar_contenido(frame)

    def mostrar_departamentos(self):
        frame = tk.Frame(self.root, bg="#2c3e50")
        AppDepartamento(frame, self.dao_depto)
        self.cambiar_contenido(frame)

    def mostrar_proyectos(self):
        frame = tk.Frame(self.root, bg="#2c3e50")
        AppProyecto(frame, self.dao_proyecto)
        self.cambiar_contenido(frame)

    def mostrar_registro_tiempo(self):
        frame = tk.Frame(self.root, bg="#2c3e50")
        AppRegistroTiempo(frame, self.dao_registro)
        self.cambiar_contenido(frame)


# ====================== ADMINISTRADOR ======================
class AppCRUD:
    def __init__(self, parent, titulo, dao, Clase):
        self.parent = parent
        self.dao = dao
        self.Clase = Clase
        self.titulo = titulo
        self.crear_interfaz()

    def crear_interfaz(self):
        form = tk.LabelFrame(self.parent, text=f"Datos {self.titulo}", padx=15, pady=15, bg="#34495e", fg="white")
        form.pack(fill="x", padx=15, pady=10)

        self.var_id = tk.StringVar()
        self.var_nombre = tk.StringVar()
        self.var_rut = tk.StringVar()
        self.var_correo = tk.StringVar()
        self.var_contrasena = tk.StringVar()
        self.var_rol = tk.StringVar(value="admin")

        campos = ["ID", "Nombre", "RUT", "Correo", "Contraseña", "Rol"]
        variables = [self.var_id, self.var_nombre, self.var_rut, self.var_correo, self.var_contrasena, self.var_rol]

        for i, (campo, var) in enumerate(zip(campos, variables)):
            tk.Label(form, text=campo+":", bg="#34495e", fg="white").grid(
                row=i//2, column=(i%2)*2, sticky="e", padx=10, pady=8)
            state = "readonly" if campo == "ID" else "normal"
            show = "*" if campo == "Contraseña" else ""
            tk.Entry(form, textvariable=var, state=state, width=40, show=show).grid(
                row=i//2, column=(i%2)*2 + 1, padx=10, pady=8)

        btn_frame = tk.Frame(self.parent, bg="#2c3e50")
        btn_frame.pack(fill="x", pady=10)
        for text, color, cmd in [("Registrar", "#27ae60", self.registrar),
                                ("Actualizar", "#2980b9", self.actualizar),
                                ("Eliminar", "#e74c3c", self.eliminar),
                                ("Buscar RUT", "#f39c12", self.buscar),
                                ("Listar Todos", "#7f8c8d", self.listar),
                                ("Limpiar", "#95a5a6", self.limpiar)]:
            tk.Button(btn_frame, text=text, bg=color, fg="white", command=cmd).pack(side="left", padx=8)

        self.tree = ttk.Treeview(self.parent, columns=("id","nombre","rut","correo","rol"), show="headings")
        for col, h in zip(["id","nombre","rut","correo","rol"], ["ID","Nombre","RUT","Correo","Rol"]):
            self.tree.heading(col, text=h)
        self.tree.pack(fill="both", expand=True, padx=15, pady=10)

    def registrar(self):
        try:
            obj = self.Clase(0, self.var_nombre.get(), self.var_rut.get(), 
                           self.var_correo.get(), self.var_contrasena.get(), self.var_rol.get())
            self.dao.registrar(obj)
            messagebox.showinfo("Éxito", f"{self.titulo} registrado correctamente")
            self.listar()
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def listar(self):
        for item in self.tree.get_children():
            self.tree.delete(item)
        try:
            lista = self.dao.obtener_todo()
            for obj in lista:
                self.tree.insert("", "end", values=(obj.get_id(), obj.get_nombre(), obj.get_rut(),
                                                  obj.get_correo(), obj.get_rol()))
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def buscar(self):
        rut = self.var_rut.get()
        if not rut:
            messagebox.showwarning("Aviso", "Ingrese RUT")
            return
        try:
            obj = self.dao.buscar(rut)
            if obj:
                self.var_id.set(obj.get_id())
                self.var_nombre.set(obj.get_nombre())
                self.var_rut.set(obj.get_rut())
                self.var_correo.set(obj.get_correo())
                self.var_contrasena.set(obj.get_contrasena())
                self.var_rol.set(obj.get_rol())
            else:
                messagebox.showinfo("No encontrado", "No existe ese RUT")
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def actualizar(self): messagebox.showinfo("Info", "Actualizar (pendiente)")
    def eliminar(self): messagebox.showinfo("Info", "Eliminar (pendiente)")
    def limpiar(self): 
        self.var_id.set("")
        self.var_nombre.set("")
        self.var_rut.set("")
        self.var_correo.set("")
        self.var_contrasena.set("")


# ====================== EMPLEADO ======================
class AppEmpleado:
    def __init__(self, parent, dao):
        self.parent = parent
        self.dao = dao
        self.crear_interfaz()

    def crear_interfaz(self):
        form = tk.LabelFrame(self.parent, text="Datos del Empleado", padx=15, pady=15, bg="#34495e", fg="white")
        form.pack(fill="x", padx=15, pady=10)

        self.var_id = tk.StringVar()
        self.var_nombre = tk.StringVar()
        self.var_rut = tk.StringVar()
        self.var_correo = tk.StringVar()
        self.var_telefono = tk.StringVar()
        self.var_salario = tk.StringVar()
        self.var_fecha_inicio = tk.StringVar()
        self.var_departamento = tk.StringVar()

        campos = ["ID", "Nombre", "RUT", "Correo", "Teléfono", "Salario", "Fecha Inicio", "Departamento"]
        variables = [self.var_id, self.var_nombre, self.var_rut, self.var_correo,
                    self.var_telefono, self.var_salario, self.var_fecha_inicio, self.var_departamento]

        for i, (campo, var) in enumerate(zip(campos, variables)):
            tk.Label(form, text=campo+":", bg="#34495e", fg="white").grid(
                row=i//2, column=(i%2)*2, sticky="e", padx=10, pady=8)
            state = "readonly" if campo == "ID" else "normal"
            tk.Entry(form, textvariable=var, state=state, width=40).grid(
                row=i//2, column=(i%2)*2 + 1, padx=10, pady=8)

        btn_frame = tk.Frame(self.parent, bg="#2c3e50")
        btn_frame.pack(fill="x", pady=10)
        for text, color, cmd in [("Registrar", "#27ae60", self.registrar),
                                ("Actualizar", "#2980b9", self.actualizar),
                                ("Eliminar", "#e74c3c", self.eliminar),
                                ("Buscar RUT", "#f39c12", self.buscar),
                                ("Listar Todos", "#7f8c8d", self.listar),
                                ("Limpiar", "#95a5a6", self.limpiar)]:
            tk.Button(btn_frame, text=text, bg=color, fg="white", command=cmd).pack(side="left", padx=8)

        self.tree = ttk.Treeview(self.parent, columns=("id","nombre","rut","correo","salario"), show="headings")
        for col, h in zip(["id","nombre","rut","correo","salario"], ["ID","Nombre","RUT","Correo","Salario"]):
            self.tree.heading(col, text=h)
        self.tree.pack(fill="both", expand=True, padx=15, pady=10)

    def registrar(self):
        try:
            emp = Empleado(0, self.var_nombre.get(), self.var_rut.get(), self.var_correo.get(),
                          "", self.var_telefono.get(), float(self.var_salario.get() or 0),
                          self.var_fecha_inicio.get(), self.var_departamento.get())
            self.dao.registrar(emp)
            messagebox.showinfo("Éxito", "Empleado registrado (ID automático)")
            self.listar()
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def listar(self):
        for item in self.tree.get_children():
            self.tree.delete(item)
        try:
            lista = self.dao.obtener_todo()
            for e in lista:
                self.tree.insert("", "end", values=(e.get_id(), e.get_nombre(), e.get_rut(),
                                                  e.get_correo(), getattr(e, 'get_salario', lambda: "")()))
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def buscar(self): messagebox.showinfo("Info", "Buscar por RUT (pendiente)")
    def actualizar(self): messagebox.showinfo("Info", "Actualizar (pendiente)")
    def eliminar(self): messagebox.showinfo("Info", "Eliminar (pendiente)")
    def limpiar(self): pass


# ====================== DEPARTAMENTO Y PROYECTO (SIMPLIFICADOS) ======================
class AppDepartamento:
    def __init__(self, parent, dao):
        self.parent = parent
        self.dao = dao
        self.crear_interfaz()

    def crear_interfaz(self):
        tk.Label(self.parent, text="Gestión de Departamentos", font=("Arial", 16, "bold"), bg="#2c3e50", fg="white").pack(pady=20)
        tk.Button(self.parent, text="Crear Departamento", bg="#27ae60", fg="white", command=self.crear).pack(pady=5)
        tk.Button(self.parent, text="Listar Departamentos", bg="#7f8c8d", command=self.listar).pack(pady=5)

    def crear(self): 
        nombre = tk.simpledialog.askstring("Nuevo Departamento", "Nombre del departamento:")
        if nombre:
            self.dao.registrar(nombre)
            messagebox.showinfo("Éxito", "Departamento creado")

    def listar(self):
        messagebox.showinfo("Info", "Listar Departamentos (pendiente)")

class AppProyecto:
    def __init__(self, parent, dao):
        self.parent = parent
        self.dao = dao
        self.crear_interfaz()

    def crear_interfaz(self):
        tk.Label(self.parent, text="Gestión de Proyectos", font=("Arial", 16, "bold"), bg="#2c3e50", fg="white").pack(pady=20)
        tk.Button(self.parent, text="Crear Proyecto", bg="#27ae60", fg="white", command=self.crear).pack(pady=5)
        tk.Button(self.parent, text="Listar Proyectos", bg="#7f8c8d", command=self.listar).pack(pady=5)

    def crear(self):
        nombre = tk.simpledialog.askstring("Nuevo Proyecto", "Nombre del proyecto:")
        if nombre:
            self.dao.registrar(nombre)
            messagebox.showinfo("Éxito", "Proyecto creado")

    def listar(self):
        messagebox.showinfo("Info", "Listar Proyectos (pendiente)")


class AppRegistroTiempo:
    def __init__(self, parent, dao):
        self.parent = parent
        self.dao = dao
        tk.Label(parent, text="Registro de Tiempo", font=("Arial", 16, "bold"), bg="#2c3e50", fg="white").pack(pady=40)
        tk.Button(parent, text="Registrar Nuevo Registro", bg="#27ae60", fg="white", 
                 command=lambda: messagebox.showinfo("Info", "Registro de Tiempo - Próximamente")).pack(pady=10)


if __name__ == "__main__":
    root = tk.Tk()
    app = SistemaEcoTech(root)
    root.mainloop()