# Definir una clase que represente una tabla en la base de datos
from sqlalchemy import Column, String , Integer , Boolean
from sqlalchemy.orm import registry

# Crear una instancia del registro y la base
mapper_registry = registry()
Base = mapper_registry.generate_base()

class profesor(Base):
    __tablename__ = 'profesores' 
    ID = Column(Integer, primary_key=True)   
    Nombre_uno = Column(String(100))
    Nombre_dos = Column(String(100))
    Apellido_uno = Column(String(100))
    Apellido_dos = Column(String(100))
   

    def to_dict(self):
        return {
            'id': self.ID,
            'nombre_uno': self.Nombre_uno,
             'nombre_dos': self.Nombre_dos,
             'apellido_uno': self.Apellido_uno,
             'apellido_dos': self.Apellido_dos,
             
        }
