# Definir una clase que represente una tabla en la base de datos
from sqlalchemy import Column, LargeBinary, String , Integer , Date ,Boolean
from sqlalchemy.orm import registry

# Crear una instancia del registro y la base
mapper_registry = registry()
Base = mapper_registry.generate_base()

# Define the model
class UploadPasantia(Base):
    __tablename__ = "pasantia"

    ID = Column(Integer, primary_key=True, index=True, autoincrement=True)
    id_profesor = Column(Integer)
    nombre = Column(String(25))
    anteproyecto = Column(LargeBinary)
    acta_de_satisfaccion = Column(LargeBinary)
    certificado_laboral = Column(LargeBinary)
    certificado_arl = Column(LargeBinary)
    horario_del_pasante = Column(LargeBinary)
    fecha_inicio = Column(String)
    terminada = Column(Boolean)


