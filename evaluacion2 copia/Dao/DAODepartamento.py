from conexiones import Conexion

class DAODepartamento:
    def __init__(self):
        self.__conexion = Conexion()

    def registrar(self, nombre):
        self.__conexion.conectar()
        sql = "INSERT INTO departamento (nombre) VALUES (%s)"
        param = (nombre,)
        self.__conexion.cursor.execute(sql, param)
        self.__conexion.desconectar()

    def obtener_todo(self):
        self.__conexion.conectar()
        sql = "SELECT * FROM departamento"
        self.__conexion.cursor.execute(sql)
        r = self.__conexion.cursor.fetchall()
        self.__conexion.desconectar()
        return r  # Devuelve lista de tuplas

    def eliminar(self, id_departamento):
        self.__conexion.conectar()
        sql = "DELETE FROM departamento WHERE idDepartamento = %s"
        param = (id_departamento,)
        self.__conexion.cursor.execute(sql, param)
        self.__conexion.desconectar()