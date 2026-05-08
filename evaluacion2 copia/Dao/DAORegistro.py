from conexiones import Conexion
from clases.Registro import Registro

class DAORegistro:
    def __init__(self):
        self.__conexion = Conexion()

    def registrar(self, r: Registro):
        self.__conexion.conectar()
        sql = """
            INSERT INTO registro (fecha, hora, descripcion, empleado, proyecto) 
            VALUES (%s, %s, %s, %s, %s)
        """
        param = (r.get_fecha(), r.get_hora(), r.get_descripcion(), 
                r.get_empleado(), r.get_proyecto())
        self.__conexion.cursor.execute(sql, param)
        self.__conexion.desconectar()

    def obtener_por_empleado(self, id_empleado):
        self.__conexion.conectar()
        sql = "SELECT * FROM registro WHERE empleado = %s"
        param = (id_empleado,)
        self.__conexion.cursor.execute(sql, param)
        r = self.__conexion.cursor.fetchall()
        self.__conexion.desconectar()

        registros = []
        for reg in r:
            registro = Registro(reg[0], reg[1], reg[2], reg[3], reg[4], reg[5])
            registros.append(registro)
        return registros

    def obtener_todo(self):
        self.__conexion.conectar()
        sql = "SELECT * FROM registro"
        self.__conexion.cursor.execute(sql)
        r = self.__conexion.cursor.fetchall()
        self.__conexion.desconectar()

        registros = []
        for reg in r:
            registro = Registro(reg[0], reg[1], reg[2], reg[3], reg[4], reg[5])
            registros.append(registro)
        return registros