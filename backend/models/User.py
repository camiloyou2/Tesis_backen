# Definir una clase que represente una tabla en la base de datos
from sqlalchemy import Column, String
from sqlalchemy.orm import registry

# Crear una instancia del registro y la base
mapper_registry = registry()
Base = mapper_registry.generate_base()

class user(Base):
    __tablename__ = 'user'
    user = Column(String(12), primary_key=True)
    password = Column(String(50))

    def to_dict(self):
        return {
            'user': self.username,
            'password': self.password
        }
