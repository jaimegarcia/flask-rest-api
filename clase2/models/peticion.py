class Peticion:
    def __init__(self, cedula, peticion, fecha_creacion, fecha_atencion):
        self.cedula = cedula
        self.peticion = peticion
        self.fecha_creacion = fecha_creacion
        self.fecha_atencion = fecha_atencion

    def to_dict(self):
        return dict((key, value) for (key, value) in self.__dict__.items())