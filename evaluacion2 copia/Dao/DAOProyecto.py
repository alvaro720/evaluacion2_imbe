from conexiones import Conexion

class DAOProyecto:
    def __init__(self):
        self.__conexion = Conexion()

    def registrar(self, nombre):
        self.__conexion.conectar()
        sql = "INSERT INTO proyecto (nombre) VALUES (%s)"
        param = (nombre,)
        self.__conexion.cursor.execute(sql, param)
        self.__conexion.desconectar()

    def obtener_todo(self):
        self.__conexion.conectar()
        sql = "SELECT * FROM proyecto"
        self.__conexion.cursor.execute(sql)
        r = self.__conexion.cursor.fetchall()
        self.__conexion.desconectar()
        return r

    def eliminar(self, id_proyecto):
        self.__conexion.conectar()
        sql = "DELETE FROM proyecto WHERE idProyecto = %s"
        param = (id_proyecto,)
        self.__conexion.cursor.execute(sql, param)
        self.__conexion.desconectar()