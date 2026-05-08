import tkinter as tk
from tkinter import ttk, messagebox

# Importaciones necesarias (ajusta 'dao_administrador' al nombre real de tu archivo DAO)
try:
    from clases.Administrador import Administrador
    from Dao.DAOAdministrador import DAOAdministrador 
except ImportError as e:
    print(f"Advertencia: Revisa tus importaciones. Error: {e}")

class AppAdministrador:
    def __init__(self, root):
        self.root = root
        self.root.title("Prueba DAO Administrador")
        self.root.geometry("800x500")
        
        try:
            self.dao = DAOAdministrador()
        except Exception as e:
            self.dao = None
            
        self.var_id = tk.StringVar()
        self.var_nombre = tk.StringVar()
        self.var_rut = tk.StringVar()
        self.var_correo = tk.StringVar()
        self.var_contrasena = tk.StringVar()
        self.var_rol = tk.StringVar()

        self.crear_interfaz()
        
    def crear_interfaz(self):
        frame_form = tk.LabelFrame(self.root, text="Datos del Administrador", padx=10, pady=10)
        frame_form.pack(fill="x", padx=10, pady=10)

        # ID ahora es 'readonly' para que no se pueda escribir, pero sí mostrar
        tk.Label(frame_form, text="ID:").grid(row=0, column=0, sticky="e", padx=5, pady=5)
        tk.Entry(frame_form, textvariable=self.var_id, state="readonly").grid(row=0, column=1, padx=5, pady=5)

        tk.Label(frame_form, text="Nombre:").grid(row=0, column=2, sticky="e", padx=5, pady=5)
        tk.Entry(frame_form, textvariable=self.var_nombre).grid(row=0, column=3, padx=5, pady=5)

        tk.Label(frame_form, text="RUT:").grid(row=1, column=0, sticky="e", padx=5, pady=5)
        tk.Entry(frame_form, textvariable=self.var_rut).grid(row=1, column=1, padx=5, pady=5)

        tk.Label(frame_form, text="Correo:").grid(row=1, column=2, sticky="e", padx=5, pady=5)
        tk.Entry(frame_form, textvariable=self.var_correo).grid(row=1, column=3, padx=5, pady=5)

        tk.Label(frame_form, text="Contraseña:").grid(row=2, column=0, sticky="e", padx=5, pady=5)
        tk.Entry(frame_form, textvariable=self.var_contrasena, show="*").grid(row=2, column=1, padx=5, pady=5)

        tk.Label(frame_form, text="Rol:").grid(row=2, column=2, sticky="e", padx=5, pady=5)
        tk.Entry(frame_form, textvariable=self.var_rol).grid(row=2, column=3, padx=5, pady=5)

        frame_btn = tk.Frame(self.root)
        frame_btn.pack(fill="x", padx=10, pady=5)

        tk.Button(frame_btn, text="Registrar", bg="#4CAF50", fg="white", command=self.registrar).pack(side="left", padx=5)
        tk.Button(frame_btn, text="Actualizar", bg="#2196F3", fg="white", command=self.actualizar).pack(side="left", padx=5)
        tk.Button(frame_btn, text="Eliminar", bg="#f44336", fg="white", command=self.eliminar).pack(side="left", padx=5)
        tk.Button(frame_btn, text="Buscar por RUT", bg="#FF9800", command=self.buscar).pack(side="left", padx=5)
        tk.Button(frame_btn, text="Listar Todos", bg="#9E9E9E", command=self.listar).pack(side="left", padx=5)
        tk.Button(frame_btn, text="Limpiar", command=self.limpiar).pack(side="left", padx=5)

        frame_tabla = tk.Frame(self.root)
        frame_tabla.pack(fill="both", expand=True, padx=10, pady=10)

        columnas = ("id", "nombre", "rut", "correo", "rol")
        self.tree = ttk.Treeview(frame_tabla, columns=columnas, show="headings")
        self.tree.heading("id", text="ID")
        self.tree.heading("nombre", text="Nombre")
        self.tree.heading("rut", text="RUT")
        self.tree.heading("correo", text="Correo")
        self.tree.heading("rol", text="Rol")
        self.tree.column("id", width=50)
        self.tree.pack(fill="both", expand=True, side="left")
        
        scrollbar = ttk.Scrollbar(frame_tabla, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscroll=scrollbar.set)
        scrollbar.pack(side="right", fill="y")

    def _crear_administrador(self, es_registro=False):
        try:
            # Si es registro, el ID se ignora (None) para que la DB lo auto-incremente
            val_id = None if es_registro else (int(self.var_id.get()) if self.var_id.get() else 0)
            
            admin = Administrador(
                val_id, 
                self.var_nombre.get(), 
                self.var_rut.get(), 
                self.var_correo.get(), 
                self.var_contrasena.get(), 
                self.var_rol.get()
            )
            return admin
        except Exception as e:
            messagebox.showerror("Error", f"Datos inválidos: {e}")
            return None

    def registrar(self):
        if not self.dao: return
        admin = self._crear_administrador(es_registro=True)
        if admin:
            try:
                self.dao.registrar(admin)
                messagebox.showinfo("Éxito", "Registrado (ID auto-generado).")
                self.listar()
            except Exception as e:
                print(str(e))

    def actualizar(self):
        if not self.dao: return
        admin = self._crear_administrador()
        if admin:
            try:
                self.dao.actualizar(admin)
                messagebox.showinfo("Éxito", "Actualizado correctamente.")
                self.listar()
            except Exception as e:
                print(str(e))

    def eliminar(self):
        if not self.dao: return
        admin = self._crear_administrador()
        if admin:
            try:
                self.dao.eliminar(admin)
                messagebox.showinfo("Éxito", "Eliminado correctamente.")
                self.listar()
            except Exception as e:
                print(str(e))

    def buscar(self):
        if not self.dao: return
        rut = self.var_rut.get()
        if not rut:
            messagebox.showwarning("Falta RUT", "Ingresa el RUT para buscar.")
            return
        try:
            admin = self.dao.buscar(rut)
            if admin:
                self.limpiar()
                self.var_id.set(admin.get_id())
                self.var_nombre.set(admin.get_nombre())
                self.var_rut.set(admin.get_rut())
                self.var_correo.set(admin.get_correo())
                self.var_contrasena.set(admin.get_contrasena())
                self.var_rol.set(admin.get_rol())
            else:
                messagebox.showinfo("No encontrado", "No existe ese RUT.")
        except Exception as e:
            print(str(e))

    def listar(self):
        print("e1")
        if not self.dao: return
        for item in self.tree.get_children(): self.tree.delete(item)
        try:
            listado = self.dao.obtener_todo()
            print(listado)
            for a in listado:
                self.tree.insert("", "end", values=(a.get_id(), a.get_nombre(), a.get_rut(), a.get_correo(), a.get_rol()))
                print("e2")
        except Exception as e:
            print(e)

    def limpiar(self):
        self.var_id.set("")
        self.var_nombre.set("")
        self.var_rut.set("")
        self.var_correo.set("")
        self.var_contrasena.set("")
        self.var_rol.set("")

if __name__ == "__main__":
    root = tk.Tk()
    app = AppAdministrador(root)
    root.mainloop()



