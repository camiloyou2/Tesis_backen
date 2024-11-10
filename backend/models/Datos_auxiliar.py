# Definir una clase que represente una tabla en la base de datos
from sqlalchemy import Column, String , Integer , Date ,Boolean
from sqlalchemy.orm import registry

# Crear una instancia del registro y la base
mapper_registry = registry()
Base = mapper_registry.generate_base()

class datos_auxiliar(Base):
    __tablename__ = 'datos_auxiliar'
    codigo = Column(String(100), primary_key=True)
    fullnameestudent = Column(String(100))
    ID = Column(Integer)
    nombre = Column(String(100))
    fecha_inicio = Column(Date)
    id_profesor = Column(Integer)
    terminada = Column(Boolean)
    fullnameteacher = Column(String(100))
    
    def to_dict(self):
        return {
            'codigo': self.codigo,
            'fullnameestudent': self.fullnameestudent,
            'ID': self.ID,
            'nombre': self.nombre,
            'fecha_inicio': self.fecha_inicio,
            'id_profesor': self.id_profesor,
            'terminada': self.terminada,
            'fullnameteacher': self.fullnameteacher
           
        }

