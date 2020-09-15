import pytz
from datetime import datetime

timezone = pytz.timezone("America/Bogota")

class Peticion:
    def __init__(self, cedula, peticion, fecha_atencion,estado = "Creada"):
        self.cedula = cedula
        self.peticion = peticion
        self.fecha_atencion = timezone.localize(datetime.strptime(fecha_atencion, '%d/%m/%y %H:%M:%S'))
        self.fecha_creacion = timezone.localize(datetime.now())
        self.estado = estado


    def to_dict(self):
        return dict((key, value) for (key, value) in self.__dict__.items())