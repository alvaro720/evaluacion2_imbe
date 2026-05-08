import mysql.connector

from conexiones import Conexion
from Seguridad import Seguridad 
from clases.Administrador import Administrador

class DAOAdministrador:
    def __init__(self):
        self.__conexion = Conexion()

    def registrar(self,a:Administrador):
        self.__conexion.conectar()

        sql = "INSERT INTO Administrador (nombre,rut,correo,contrasena,rol) VALUES (%s,%s,%s,%s,%s)"
        param = (a.get_nombre(),a.get_rut(),a.get_correo(),a.get_contrasena(),a.get_rol())
        self.__conexion.cursor.execute(sql,param)
       ##
        self.__conexion.desconectar()

    def actualizar(self,a:Administrador):
        self.__conexion.conectar()
        sql = "UPDATE Administrador SET nombre = %s, correo = %s, contrasena = %s, rol =%s WHERE rut = %s"
        param = (a.get_nombre(),a.get_correo(),a.get_contrasena(),a.get_rol(),a.get_rut())
        self.__conexion.cursor.execute(sql,param)
       ##
        self.__conexion.desconectar()

    def eliminar(self,a:Administrador):
        self.__conexion.conectar()
        sql = "DELETE FROM Administrador WHERE rut = %s"
        param = (a.get_rut(),)
        self.__conexion.cursor.execute(sql,param)
       ##
        self.__conexion.desconectar()

    def buscar(self,rut):
        self.__conexion.conectar()
        sql = "SELECT * FROM Administrador WHERE rut = %s"
        param = (rut,)
        self.__conexion.cursor.execute(sql,param)
        r = self.__conexion.cursor.fetchone()
       ##
        self.__conexion.desconectar()
        if r != None:
            a = Administrador(r[0],r[1],r[2],r[3],r[4],r[5])
            return a

    def obtener_todo(self):
        print("e1.1")
        self.__conexion.conectar()
        print("e1.2")
        sql = "SELECT * FROM Administrador"
        self.__conexion.cursor.execute(sql)
        r = self.__conexion.cursor.fetchall()
        
        
        print("e1.4")
        self.__conexion.desconectar()
        print("e1.5")
        Administradores = [] 

        for a in r:
            #Creo una Administrador con los datos de la tupla
            admin = Administrador(a[0],a[1],a[2],a[3],a[4],a[5])
            #Agrego al listado
            
            Administradores.append(admin)
        return Administradores



