import mysql.connector
from credenciales import llaves

class Conexion:
    def __init__(self):
        self.__conexion = None #conecta a db
        self.cursor = None #ejecuta sql y obtiene registros
        
        self.conectar()


#conexion a la base de datos
    def conectar(self):
        try:
            #reemplazar con credenciales
            self.__conexion = mysql.connector.connect(
                host = llaves["host"],
                user = llaves["usuario"],
                password = llaves["contrasena"],
                database = llaves["db"]
    )
            
            if self.__conexion.is_connected():
                print("conectado")
            print(f"cursor: {self.cursor}")
            self.cursor = self.__conexion.cursor()
            print(f"cursor: {self.cursor}")
        except mysql.connector.Error as e:
            print(f"error al conectarse a {e}")

#desconexion a la base de datos                  
    def desconectar(self):
        try:
            print("e1.3.1")
            if self.__conexion and self.__conexion.is_connected():
                self.__conexion.commit()
                print("e1.3.2")
                self.__conexion.close()
                print("e1.3.3")
        except mysql.connector.Error as e:
            print(f"error al desconectarse de {e}")







            