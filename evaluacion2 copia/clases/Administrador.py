from clases.Usuario import Usuario

class Administrador(Usuario):
    def __init__(self,id,nombre,rut,correo,contrasena,rol):
        super().__init__(id,nombre,rut,correo,contrasena,rol)

        