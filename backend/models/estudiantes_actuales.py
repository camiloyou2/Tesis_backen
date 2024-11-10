from sqlalchemy import create_engine, Column, Integer, String, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship


# Base para definir los modelos
Base = declarative_base()

# Definir las tablas como modelos de SQLAlchemy
class TipoDocumento(Base):
    __tablename__ = 'Tipo_Documento'
    
    id = Column(Integer, primary_key=True)
    descripcion = Column(String(10), nullable=False)

class OpcionesGrado(Base):
    __tablename__ = 'Opciones_Grado'
    
    id = Column(Integer, primary_key=True)
    descripcion = Column(String(50), nullable=False)

class Estado(Base):
    __tablename__ = 'Estado'
    
    id = Column(Integer, primary_key=True)
    descripcion = Column(String(50), nullable=False)

class EstudiantesResignificados(Base):
    __tablename__ = 'Estudiantes_resignificados'
    
    numero_documento = Column(String(20), primary_key=True)
    nombre = Column(String(40), nullable=False)
    codigo = Column(String(30))
    semestre = Column(String(2))
    creditos = Column(String(3))
    id_opcion = Column(Integer, ForeignKey('Opciones_Grado.id'))
    id_documento = Column(Integer, ForeignKey('Tipo_Documento.id'))
    id_estado = Column(Integer, ForeignKey('Estado.id'))
    solicitudes_sis = Column(String(100))

    # Relaciones (opcional si deseas acceder a los detalles de los IDs)
    tipo_documento = relationship('TipoDocumento')
    opcion_grado = relationship('OpcionesGrado')
    estado = relationship('Estado')

