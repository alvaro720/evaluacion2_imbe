#descargar el pip install bcrypt
import bcrypt

class Seguridad:
    @staticmethod
    def encriptar_clave(password: str) -> str:
        salt = bcrypt.gensalt()
        password_bytes = password.encode('utf-8')
        password_hash = bcrypt.hashpw(password_bytes, salt)
        return password_hash.decode('utf-8')

    @staticmethod
    def validar_clave(password_plana: str, password_encriptada: str) -> bool:
        return bcrypt.checkpw(
            password_plana.encode('utf-8'), 
            password_encriptada.encode('utf-8')
        )
    









       # def registrar(self,a:Administrador):
        #self.__conexion.conectar()

        #sql = "INSERT INTO Administrador (id,nombre,rut,correo,contrasena,rol) VALUES (%s,%s,%s,%s,%s,%s)"
        #param = (a.get_id(),a.get_nombre(),a.get_rut(),a.get_correo(),a.get_contrasena(),a.get_rol())
        #self.__conexion.cursor.execute(sql,param)
       ##
        #self.__conexion.desconectar()