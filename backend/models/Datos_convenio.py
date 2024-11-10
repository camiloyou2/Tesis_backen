# Definir una clase que represente una tabla en la base de datos
from sqlalchemy import Column, String , Integer , Date ,Boolean
from sqlalchemy.orm import registry

# Crear una instancia del registro y la base
mapper_registry = registry()
Base = mapper_registry.generate_base()

class datos_convenio(Base):
    __tablename__ = 'datos_convenios'
    nombre = Column(String(100), primary_key=True)
    nit = Column(Integer)
    direccion = Column(String(50))
    fecha_inicio = Column(Date)
    fecha_fin = Column(Date)
    estado = Column(Boolean)
    

    def to_dict(self):
        return {
            'nombre': self.nombre,
            'nit': self.nit,
            'direccion': self.direccion,
            'fecha_inicio': self.fecha_inicio,
            'fecha_inicio': self.fecha_inicio,
            'fecha_fin': self.fecha_fin,
            'estado': self.estado
           
        }

