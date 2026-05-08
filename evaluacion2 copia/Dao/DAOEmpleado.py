import mysql.connector
from conexiones import Conexion
from clases.Empleado import Empleado

class DAOEmpleado:
    def __init__(self):
        self.__conexion = Conexion()

    def registrar(self, e: Empleado):
        self.__conexion.conectar()
        sql = "INSERT INTO empleado (nombre, rut, correo, contrasena, rol) VALUES (%s, %s, %s, %s, %s)"
        param = (e.get_nombre(), e.get_rut(), e.get_correo(), e.get_contrasena(), e.get_rol())
        self.__conexion.cursor.execute(sql, param)
        self.__conexion.desconectar()

    def actualizar(self, e: Empleado):
        self.__conexion.conectar()
        sql = "UPDATE empleado SET nombre = %s, correo = %s, contrasena = %s, rol = %s WHERE rut = %s"
        param = (e.get_nombre(), e.get_correo(), e.get_contrasena(), e.get_rol(), e.get_rut())
        self.__conexion.cursor.execute(sql, param)
        self.__conexion.desconectar()

    def eliminar(self, rut):
        self.__conexion.conectar()
        sql = "DELETE FROM empleado WHERE rut = %s"
        param = (rut,)
        self.__conexion.cursor.execute(sql, param)
        self.__conexion.desconectar()

    def buscar(self, rut):
        self.__conexion.conectar()
        sql = "SELECT * FROM empleado WHERE rut = %s"
        param = (rut,)
        self.__conexion.cursor.execute(sql, param)
        r = self.__conexion.cursor.fetchone()
        self.__conexion.desconectar()

        if r is not None:
            return Empleado(r[0], r[1], r[2], r[3], r[4], r[5])
        return None

    def obtener_todo(self):
        self.__conexion.conectar()
        sql = "SELECT * FROM empleado"
        self.__conexion.cursor.execute(sql)
        r = self.__conexion.cursor.fetchall()
        self.__conexion.desconectar()

        empleados = []
        for a in r:
            emp = Empleado(a[0], a[1], a[2], a[3], a[4], a[5])
            empleados.append(emp)
        return empleados