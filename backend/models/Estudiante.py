# Definir una clase que represente una tabla en la base de datos
from sqlalchemy import Column, String , Integer , Boolean
from sqlalchemy.orm import registry

# Crear una instancia del registro y la base
mapper_registry = registry()
Base = mapper_registry.generate_base()

class estudiante(Base):
    __tablename__ = 'estudiante' 
    ID = Column(Integer, primary_key=True)   
    Nombre_uno = Column(String(100))
    Nombre_dos = Column(String(100))
    Apellido_uno = Column(String(100))
    Apellido_dos = Column(String(100))
    pasantia_id = Column(Integer)
    monografia_id = Column(Integer)
    auxiliar_id = Column(Integer)
    semestre_avanzado = Column(Boolean)

    def to_dict(self):
        return {
            'id': self.ID,
            'nombre_uno': self.Nombre_uno,
             'nombre_dos': self.Nombre_dos,
             'apellido_uno': self.Apellido_uno,
             'apellido_dos': self.Apellido_dos,
             'pasantia_id': self.pasantia_id,
             'monografia_id': self.monografia_id,
             'auxiliar_id': self.auxiliar_id,
             'termninado': self.semestre_avanzado
        }

