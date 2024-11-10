from sqlalchemy import create_engine, Column, Integer, String, ForeignKey, Date
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker

Base = declarative_base()

class Proyecto(Base):
    __tablename__ = 'Proyectos'
    ProyectoID = Column(Integer, primary_key=True, autoincrement=True)
    TituloEspecializacion = Column(String(255))
    Estado = Column(String(50))

class Estudiante(Base):
    __tablename__ = 'Estudiantes'
    EstudianteID = Column(Integer, primary_key=True, autoincrement=True)
    Nombre = Column(String(100))

class Director(Base):
    __tablename__ = 'Directores'
    DirectorID = Column(Integer, primary_key=True, autoincrement=True)
    Nombre = Column(String(100))

class Modalidad(Base):
    __tablename__ = 'Modalidades'
    ModalidadID = Column(Integer, primary_key=True, autoincrement=True)
    Nombre = Column(String(50))

class Periodo(Base):
    __tablename__ = 'Periodos'
    PeriodoID = Column(Integer, primary_key=True, autoincrement=True)
    Periodo = Column(String(10))
    Ano = Column(Integer)

class Acta(Base):
    __tablename__ = 'Actas'
    ActaID = Column(Integer, primary_key=True , autoincrement=True)
    NumeroActa = Column(Integer)
    FechaAprobacion = Column(Date)
    FechaSustentacion = Column(Date)

class ProyectoEstudiante(Base):
    __tablename__ = 'ProyectosEstudiantes'
    ProyectoID = Column(Integer, primary_key=True)
    EstudianteID = Column(Integer  )
    DirectorID = Column(Integer )
  
    ModalidadID = Column(Integer)
    PeriodoID = Column(Integer)
    ActaID = Column(Integer)


class Graduados(Base):
    __tablename__ = 'graduados'
    id = Column(Integer, primary_key=True, autoincrement=True)
    anio = Column(Integer  )
    periodo = Column(Integer )
  
    genero = Column(String(1))
    nombre = Column(String(100))
    opcion = Column(String(100))
    titulo = Column(String(100))
    fecha_ingreso = Column(Date)
    fecha_registro= Column(Date)
    cc = Column(String(11))

   
   
