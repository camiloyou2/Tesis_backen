from datetime import date, datetime
import json
from os import getenv
from dotenv import load_dotenv
from fastapi.encoders import jsonable_encoder
from requests import Session
from sqlalchemy import Column, Integer, String, create_engine, select , text, update
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm import registry
from models.Datos_docente import profesor
from models.Estudiante import estudiante
from models.Pasantia import UploadPasantia
from models.User import user
from models.Datos_pasantia import datos_pasantia
from models.Datos_monografia import datos_monografia
from models.Datos_auxiliar import datos_auxiliar
from models.Datos_convenio import datos_convenio
from unidecode import unidecode
from models.estudiantes_actuales import Estado, EstudiantesResignificados, OpcionesGrado, TipoDocumento
from models.models_power import Acta, Director, Estudiante, Graduados, Modalidad, Periodo, Proyecto, ProyectoEstudiante
class Database:
    def __init__(self):
        # Crear una instancia de Engine
        self.engine = create_engine(
            f'mysql+pymysql://{getenv("USERDB")}:{getenv("PASSWORD")}@localhost/{getenv("DATABASE")}'
        )

        # Crear una clase Base para la definición de la tabla
        self.mapper_registry = registry()
        self.Base = self.mapper_registry.generate_base()

        # Crear una fábrica de sesiones
        self.Session = sessionmaker(bind=self.engine)
        self.session = self.Session()

        # Definir el modelo User
        self.User = self.define_user_model()
        self.Estudiante = estudiante
        self.pasantia= UploadPasantia
        self.datos_pasantia = datos_pasantia
        self.datos_monografia = datos_monografia
        self.datos_auxiliar = datos_auxiliar
        self.datos_convenio = datos_convenio
        self.datos_docente = profesor
        self.documentos = TipoDocumento
        self.opcines_grdao = OpcionesGrado
        
        # Crear todas las tablas en la base de datos (si no existen)
        self.Base.metadata.create_all(self.engine)

    def define_user_model(self):
      
        return user

    def create_user(self, username, password):
        # Crear una instancia de User
        new_user = self.User(username=username, password=password)

        # Agregar la instancia a la sesión
        self.session.add(new_user)

        # Confirmar la transacción
        self.session.commit()
    def get_tipo_documento (self, descripcion):
         # Obtener el ID del tipo de documento por descripción
        tipo_doc = self.session.query(self.documentos).filter_by(descripcion=descripcion).first()
        return tipo_doc.id if tipo_doc else None
    
    def get_tipo_opciones_de_grado(self, descripcion):
         # Obtener el ID del tipo de documento por descripción
        tipo_opcion = self.session.query(OpcionesGrado).filter_by(descripcion=descripcion).first()
        return tipo_opcion.id if tipo_opcion else None
    
    def get_tipo_Estado(self, descripcion):
         # Obtener el ID del tipo de documento por descripción
        tipo_Estado = self.session.query(Estado).filter_by(descripcion=descripcion).first()
        return tipo_Estado.id if tipo_Estado else None
    
    def get_all_opciones_de_grado(self):
        # Asumiendo que OpcionesGrado es el modelo de la tabla Opciones_Grado
        opciones = self.session.query(OpcionesGrado).all()
        return opciones 
   
    def actualizar_usuario(self, numero_documento: str, nuevos_datos: dict):
        # Construimos la sentencia de actualización
        stmt = (
            update(EstudiantesResignificados)
            .where(EstudiantesResignificados.numero_documento == numero_documento)
            .values(**nuevos_datos)  # Se descompone el diccionario de datos en pares clave-valor
        )
        # Ejecutamos la sentencia de actualización
        self.session.execute(stmt)
        self.session.commit()  # Confirmamos los cambios en la base de datos
   
    def get_all_tipo_documento(self):
        # Asumiendo que OpcionesGrado es el modelo de la tabla Opciones_Grado
        opciones = self.session.query(self.documentos).all()
        return opciones 
    
    def get_all_Estado(self):
        # Asumiendo que OpcionesGrado es el modelo de la tabla Opciones_Grado
        opciones = self.session.query(Estado).all()
        return opciones 

    def create_estudiante(self,numero_documento,nombre,codigo,semestre,creditos,id_opcion,id_documento,id_estado,solicitudes_sis):
        # Asumiendo que OpcionesGrado es el modelo de la tabla Opciones_Grado
                # Add a new user to Estudiantes_resignificados
        new_student = EstudiantesResignificados(
            numero_documento=numero_documento,
            nombre=nombre,
            codigo=codigo,
            semestre=semestre,
            creditos=creditos,
            id_opcion=id_opcion,       # Replace with actual id from Opciones_Grado
            id_documento=id_documento,    # Replace with actual id from Tipo_Documento
            id_estado=id_estado,       # Replace with actual id from Estado
            solicitudes_sis=solicitudes_sis
        )

        # Add and commit the new user
        self.session.add(new_student)
        self.session.commit()

    def ceate_pasantia(self, id_profesor, nombre,anteproyecto_content,
                       acta_content,certificado_laboral_content,certificado_arl_content,
                     horario_del_pasante_content,fecha_inicio ,terminada ):
        # Crear una instancia de User
        
        print("-----------------  " + fecha_inicio )
        new_pasantia = self.pasantia(
             id_profesor=int(id_profesor),
        nombre=nombre,
        anteproyecto=anteproyecto_content,
        acta_de_satisfaccion=acta_content,
        certificado_laboral=certificado_laboral_content,
        certificado_arl=certificado_arl_content,
        horario_del_pasante=horario_del_pasante_content,
        fecha_inicio=fecha_inicio,  # Convert the string to a date object
        terminada=terminada
        )

        # Agregar la instancia a la sesión
        self.session.add(new_pasantia)

        # Confirmar la transacción
        self.session.commit()
        
    def paginate(self,query, page, per_page):
        # first all users second page that wanna see divicions users
        total_items = query.count()
        total_pages = (total_items + per_page - 1) // per_page  # Calcula el total de páginas
        items = query.limit(per_page).offset((page - 1) * per_page).all()
        return {
            'items': items,
            'total_items': total_items,
            'total_pages': total_pages,
            'current_page': page,
            'per_page': per_page
        }
        
    def get_all_convenios(self):
          
        # Definir la consulta SQL
        query = text("""
SELECT nombre, id, 
       CASE
           WHEN CURDATE() BETWEEN fecha_inicio AND fecha_fin THEN TRUE
           ELSE FALSE
       END AS estado
FROM convenio
-- Utilizamos la subconsulta para filtrar con el alias 'estado'
WHERE CURDATE() BETWEEN fecha_inicio AND fecha_fin;

""")

        # Ejecutar la consulta
        result = self.session.execute(query)
        rows = result.fetchall()
        
        print (rows[0][0])
        # Obtener los resultados
        

        return  [{"nombre": item.nombre,
                       "id": item.id
                     
                     
                      } for item in rows]
        # Convertir la lista de diccionarios a JSON

    def get_all_profesores(self):
          
        # Definir la consulta SQL
        query = text("""
SELECT id,concat(Nombre_uno, " ",Nombre_dos," ",Apellido_uno," ", Apellido_dos)  as fullname
FROM profesores

""")

        # Ejecutar la consulta
        result = self.session.execute(query)
        rows = result.fetchall()
        
        print (rows[0][0])
        # Obtener los resultados
        

        return  [{"fullname": item.fullname,
                       "id": item.id,
                    
                     
                      } for item in rows]
        # Convertir la lista de diccionarios a JSON

    def get_all_estudents(self ,poscion ):
      #  print(self.session.query(self.User).count())
       # users = self.session.query(self.User).all()
        page = poscion
        per_page = 2
        query = self.session.query(self.Estudiante)
        # first all users second page that wanna see divicions users
        result = self.paginate(query, page, per_page)
       
       
        # Obtener solo los items
        items = result['items']
        # Crear una lista de diccionarios a partir de los atributos de los items
        user_list = [{"nombre_uno": item.Nombre_uno,
                       "nombre_dos": item.Nombre_dos,
                      "apellido_uno": item.Apellido_uno,
                      "apellido_dos": item.Apellido_dos,
                      } for item in items]

        # Convertir la lista de diccionarios a una cadena JSON con formato
        json_str = json.dumps(user_list, indent=4)
        print(json_str)
       
        return(json_str)
        # Convertir la lista de diccionarios a JSON
    #SELECT * FROM prueba.datos_pasantia;
    def get_datos_pasantia (self ,poscion ):
       #  print(self.session.query(self.User).count())
       # users = self.session.query(self.User).all()
        page = poscion
        per_page = 3
        query = self.session.query(self.datos_pasantia)
        # first all users second page that wanna see divicions users
        result = self.paginate(query, page, per_page)
       
       
        # Obtener solo los items
        items = result['items']
        # Crear una lista de diccionarios a partir de los atributos de los items
        user_list = [{

           'codigo': item.codigo,
            'fullnameestudent': item.fullnameestudent,
            'ID': item.ID,
            'nombre': item.nombre,
            'fecha_inicio': item.fecha_inicio,
            'id_profesor': item.id_profesor,
            'terminada': item.terminada,
            'fullnameteacher': item.fullnameteacher,
            'id_convenio': item.id_convenio,

                      } for item in items]

        # Convertir la lista de diccionarios a una cadena JSON con formato
        #json_str = json.dumps(user_list, indent=4)
        print(user_list)
       
        return(user_list)
        # Convertir la lista de diccionarios a JSON

    def get_datos_monografia (self ,poscion ):
       #  print(self.session.query(self.User).count())
       # users = self.session.query(self.User).all()
       # Aliasing the tables for clarity (optional)
        # Construcción de la consulta

        # Construcción de la consulta con campos específicos
        page = poscion
        per_page = 100
        
       


        consulta = (
    self.session.query(
        EstudiantesResignificados.numero_documento,
        EstudiantesResignificados.nombre,
        EstudiantesResignificados.codigo,
        EstudiantesResignificados.semestre,
        EstudiantesResignificados.creditos,
        EstudiantesResignificados.id_opcion,
        EstudiantesResignificados.id_documento,
        EstudiantesResignificados.id_estado,
        EstudiantesResignificados.solicitudes_sis
    )
    .outerjoin(Estado, EstudiantesResignificados.id_estado == Estado.id)  # LEFT JOIN con Estado
    .filter(EstudiantesResignificados.id_estado.is_(None))  # Filtro donde id_estado es NULL
    .order_by(EstudiantesResignificados.nombre)  # Ordenar por nombre en orden ascendente
)
        result = self.paginate(consulta, page, per_page)
        items = result['items']
        
        user_list = [{

          "numero_documento": x.numero_documento,
                "nombre": x.nombre,
                "codigo": x.codigo,
                "semestre": x.semestre,
                "creditos": x.creditos,
                "id_opcion": x.id_opcion,
                "id_documento": x.id_documento,
                "id_estado": x.id_estado,
                "solicitudes_sis": x.solicitudes_sis

                      } for x in items]
       
    
        return(user_list)
        # Convertir la lista de diccionarios a JSON

    def get_datos_xx (self ,poscion ):
        page = poscion
        per_page = 100
        consulta = (
    self.session.query(
        EstudiantesResignificados.numero_documento,
        EstudiantesResignificados.nombre,
        EstudiantesResignificados.codigo,
        EstudiantesResignificados.semestre,
        EstudiantesResignificados.creditos,
        EstudiantesResignificados.id_opcion,
        EstudiantesResignificados.id_documento,
        EstudiantesResignificados.id_estado,
        EstudiantesResignificados.solicitudes_sis,
        Estado.id,
        Estado.descripcion
    )
    .outerjoin(Estado, EstudiantesResignificados.id_estado == Estado.id)  # LEFT JOIN on Estado
    .filter(EstudiantesResignificados.id_estado.isnot(None))  # Filter where id_estado is not null
    .order_by(EstudiantesResignificados.nombre)  # Order by nombre in ascending order
)
        result = self.paginate(consulta, page, per_page)
        items = result['items']
        
        user_list = [{

          "numero_documento": x.numero_documento,
                "nombre": x.nombre,
                "codigo": x.codigo,
                "semestre": x.semestre,
                "creditos": x.creditos,
                "id_opcion": x.id_opcion,
                "id_documento": x.id_documento,
                "id_estado": x.id_estado,
                "solicitudes_sis": x.solicitudes_sis

                      } for x in items]
       
    
        return(user_list)
    
    def get_datos_auxiliar (self ,poscion ):
        #  print(self.session.query(self.User).count())
        # users = self.session.query(self.User).all()
            page = poscion
            per_page = 3
            query = self.session.query(self.datos_auxiliar)
            # first all users second page that wanna see divicions users
            result = self.paginate(query, page, per_page)
        
        
            # Obtener solo los items
            items = result['items']
            # Crear una lista de diccionarios a partir de los atributos de los items
            user_list = [{

            'codigo': item.codigo,
                'fullnameestudent': item.fullnameestudent,
                'ID': item.ID,
                'nombre': item.nombre,
                'fecha_inicio': item.fecha_inicio,
                'id_profesor': item.id_profesor,
                'terminada': item.terminada,
                'fullnameteacher': item.fullnameteacher

                        } for item in items]

            # Convertir la lista de diccionarios a una cadena JSON con formato
            #json_str = json.dumps(user_list, indent=4)
            print(user_list)
        
            return(user_list)
            # Convertir la lista de diccionarios a JSON

    def get_datos_convenio (self ,poscion ):
                
            #  print(self.session.query(self.User).count())
            # users = self.session.query(self.User).all()
                page = poscion
                per_page = 10
                query = self.session.query(self.datos_convenio)
                # first all users second page that wanna see divicions users
                result = self.paginate(query, page, per_page)
            
            
                # Obtener solo los items
                items = result['items']
                # Crear una lista de diccionarios a partir de los atributos de los items
                user_list = [{
 'nombre': item.nombre,
            'nit': item.nit,
            'direccion': item.direccion,
            'fecha_inicio': item.fecha_inicio,
            'fecha_inicio': item.fecha_inicio,
            'fecha_fin': item.fecha_fin,
            'estado': item.estado


                            } for item in items]

                # Convertir la lista de diccionarios a una cadena JSON con formato
                #json_str = json.dumps(user_list, indent=4)
                print(user_list)
            
                return(user_list)
                # Convertir la lista de diccionarios a JSON
    
    def get_pages(self ,tabla_nombre):
        print(tabla_nombre + "  -------------------------------------")
        if (tabla_nombre == "auxiliar"):
             query = self.session.query(self.datos_auxiliar)
        if (tabla_nombre == "monografia"):
             query = self.session.query(self.datos_monografia)
        if (tabla_nombre == "pasantia"):
             query = self.session.query(self.datos_pasantia)
        
        total_items = query.count()
        total_pages = (total_items + 3 - 1) // 3  # Calcula el total de páginas
        return {    
            'total_pages': total_pages,
        }
     
    def get_datos_convenio_concreto( self, id_convenio):
          
        # Definir la consulta SQL
        query = text("""
    SELECT nombre, nit, direccion, fecha_inicio, fecha_fin,
           CASE 
               WHEN CURDATE() BETWEEN fecha_inicio AND fecha_fin THEN TRUE
               ELSE FALSE
           END AS estado
    FROM convenio 
    WHERE id = :id
""")

        # Ejecutar la consulta
        result = self.session.execute(query, {'id': id_convenio})
        rows = result.fetchall()
        
        print (rows[0][0])
        # Obtener los resultados
        return  [{
            'nombre': rows[0][0],
            'nit': rows[0][1],
            'direccion':  rows[0][2],
            'fecha_inicio':  rows[0][3],
            'fecha_fin':  rows[0][4],
            'estado':  rows[0][5]
                            } ]
    
    def get_datos_pasantia_individual( self, id_pasantia ):
          
        # Definir la consulta SQL
        query = text("""
   select 
anteproyecto ,  acta_de_satisfaccion  ,certificado_laboral  ,certificado_arl  ,
horario_del_pasante  ,terminada 
from pasantia  where id = :id  
""")

        # Ejecutar la consulta
        result = self.session.execute(query, {'id': id_pasantia})
        rows = result.fetchall()
        
        
        # Obtener los resultados
        return  [{
            'anteproyecto': rows[0][0],
            'acta_de_satisfaccion': rows[0][1],
            'certificado_laboral':  rows[0][2],
            'certificado_arl':  rows[0][3],
            'horario_del_pasante':  rows[0][4],
            'terminada':  rows[0][5]
                            } ]
    
    def get_datos_monografia_individual( self, id):
          
        # Definir la consulta SQL
        query = text("""
             
         SELECT 
    numero_documento, 
    nombre, 
    codigo, 
    semestre, 
    creditos, 
    solicitudes_sis, 
    tipo_documento.descripcion AS tipo_documento_descripcion, 
    estado.descripcion AS estado_descripcion, 
    opciones_grado.descripcion AS opciones_grado_descripcion
FROM 
    estudiantes_resignificados
INNER JOIN 
    tipo_documento ON estudiantes_resignificados.id_documento = tipo_documento.id
LEFT JOIN 
    estado ON estado.id = estudiantes_resignificados.id_estado
LEFT JOIN 
    opciones_grado ON opciones_grado.id = estudiantes_resignificados.id_opcion
WHERE 
    estudiantes_resignificados.numero_documento =   :id

UNION

SELECT 
    numero_documento, 
    nombre, 
    codigo, 
    semestre, 
    creditos, 
    solicitudes_sis, 
    tipo_documento.descripcion AS tipo_documento_descripcion, 
    estado.descripcion AS estado_descripcion, 
    opciones_grado.descripcion AS opciones_grado_descripcion
FROM 
    estudiantes_resignificados
INNER JOIN 
    tipo_documento ON estudiantes_resignificados.id_documento = tipo_documento.id
RIGHT JOIN 
    estado ON estado.id = estudiantes_resignificados.id_estado
LEFT JOIN 
    opciones_grado ON opciones_grado.id = estudiantes_resignificados.id_opcion
WHERE 
    estudiantes_resignificados.numero_documento =  :id

UNION

SELECT 
    numero_documento, 
    nombre, 
    codigo, 
    semestre, 
    creditos, 
    solicitudes_sis, 
    tipo_documento.descripcion AS tipo_documento_descripcion, 
    estado.descripcion AS estado_descripcion, 
    opciones_grado.descripcion AS opciones_grado_descripcion
FROM 
    estudiantes_resignificados
INNER JOIN 
    tipo_documento ON estudiantes_resignificados.id_documento = tipo_documento.id
RIGHT JOIN 
    opciones_grado ON opciones_grado.id = estudiantes_resignificados.id_opcion
LEFT JOIN 
    estado ON estado.id = estudiantes_resignificados.id_estado
WHERE 
    estudiantes_resignificados.numero_documento =  :id;



""")

        # Ejecutar la consulta
        result = self.session.execute(query, {'id': id})
        rows = result.fetchall()
        print(rows)
        keys = ["numero_documento", "nombre_completo", "codigo", "estado", "creditos", "solicitudes_sis", "tipo_documento", "estado_descripcion", "opcion_grado"]

        # Convertir cada tupla en un diccionario
        rows_as_dict = [dict(zip(keys, row)) for row in rows]

        # Convertir la lista de diccionarios a JSON
        json_result = json.dumps(rows_as_dict, default=str)

       
        # Devolver el JSON como respuesta
        return(json_result)
    
    def get_datos_auxiliar_individual( self, id_pasantia):
          
        # Definir la consulta SQL
        query = text("""
   select 
anteproyecto  , terminada 
from auxiliar_de_investigacion  where id = :id  
""")

        # Ejecutar la consulta
        result = self.session.execute(query, {'id': id_pasantia})
        rows = result.fetchall()
        
        print (rows[0][0])
        # Obtener los resultados
        return  [{
            'anteproyecto': rows[0][0],
            'terminada': rows[0][1]
            
                            } ]
       
    def find_user_by_username(self, username, password):
        print(username)
        # Usar el método select para buscar un usuario específico
        stmt = select(self.User).where(self.User.user == username ,self.User.password ==  password)

        # Ejecutar la consulta y obtener el primer resultado
        some_user = self.session.scalars(stmt).first()

        return some_user
    
    def get_docente (self ,poscion ):
        #  print(self.session.query(self.User).count())
        # users = self.session.query(self.User).all()
            page = poscion
            per_page = 3
            query = self.session.query(self.datos_docente)
            # first all users second page that wanna see divicions users
            result = self.paginate(query, page, per_page)
        
        
            # Obtener solo los items
            items = result['items']
            # Crear una lista de diccionarios a partir de los atributos de los items
            user_list = [{

            'ID': item.ID,
                'full_name': item.Nombre_uno+ " "+ item.Nombre_dos+" "+item.Apellido_uno + " "+ item.Apellido_dos
                        } for item in items]

            # Convertir la lista de diccionarios a una cadena JSON con formato
            #json_str = json.dumps(user_list, indent=4)
            print(user_list)
        
            return(user_list)
            # Convertir la lista de diccionarios a JSON

    def post_docente_pasantia( self, id):
            
            # Definir la consulta SQL
            query = text("""
    select 
    anteproyecto  , terminada ,nombre 
    from pasantia  where id_profesor = :id  
    """)

            # Ejecutar la consulta
            result = self.session.execute(query, {'id': id})
            rows = result.fetchall()
            # Obtener los resultados
            return    [{
 'nombre': row.nombre,
            'anteproyecto': row.anteproyecto,
            'terminada': row.terminada

                            } for row in rows]
    
    def insertar_dato( self, x,y,z,a, e,f,g,h,i,j):
                # Insert the project
        
        proyecto = Proyecto(TituloEspecializacion=procesar_texto(x), Estado=procesar_texto(y))

        self.session.add(proyecto)
        self.session.commit()  # Commit to get the ProyectoID
        # Insert the student
        estudiante = Estudiante(Nombre=procesar_texto(z))
        self.session.add(estudiante)
        self.session.commit()  # Commit to get the EstudianteID

        # Insert the director
        director = Director(Nombre=procesar_texto(a))
        self.session.add(director)
        self.session.commit()  # Commit to get the DirectorID

         # Insert the Modalidad
        modalidad = Modalidad(Nombre=identificar_modalidad(procesar_texto(e)))
        self.session.add(modalidad)
        self.session.commit()  # Commit to get the DirectorID


         # Insert the Periodo
        periodo = Periodo(Periodo=f , Ano=g)
        self.session.add(periodo)
        self.session.commit()  # Commit to get the DirectorID


         # Insert the Acta
        if  isinstance(i, datetime)  :
            i = i.date() 
        if  isinstance(j, datetime) :
            
            j = j.date()  # Asegúrate de que j sea un objeto datetime antes de llamar a .date()

 
        acta = Acta(NumeroActa=h ,FechaAprobacion=i, FechaSustentacion=j)
        self.session.add(acta)
        self.session.commit()  # Commit to get the DirectorID

        proyecto_estudiante = ProyectoEstudiante(
        ProyectoID=proyecto.ProyectoID,
        EstudianteID=estudiante.EstudianteID,
        DirectorID=director.DirectorID,
        ModalidadID=modalidad.ModalidadID,  # Replace with the actual ModalidadID
        PeriodoID=periodo.PeriodoID,  # Replace with the actual PeriodoID
        ActaID=acta.ActaID # Replace with the actual ActaID
        )
        self.session.add(proyecto_estudiante)
        self.session.commit()

    def insertar_graduados( self, a,b,c,d,e,f,g,h, i):
                # Insert the project
        if  g:
            g= datetime.strptime(g, "%d-%m-%Y")
        if h:    
            h= datetime.strptime(h, "%d-%m-%Y")
        if  isinstance(g, datetime)  :
            g = g.date() 
        if  isinstance(h, datetime) :
            
            h= h.date()  # Asegúrate de que j sea un objeto datetime antes de llamar a .date()

        graduado = Graduados(anio=procesar_texto(a), periodo=procesar_texto(b), genero=procesar_texto(c), nombre=procesar_texto(d), 
                             opcion=procesar_texto(e),titulo=procesar_texto(f),fecha_ingreso=g,fecha_registro=h, cc =i)

        self.session.add(graduado)
        self.session.commit()  # Commit to get the ProyectoID
        
def procesar_texto (texto: str):
     if texto!= None:
        texto = texto.lower()
        texto = ' '.join(texto.split())
        texto= unidecode(texto)
     return texto

def identificar_modalidad(texto:str):
     if texto!= None:
        if  texto.startswith("monogr"):
             return "monografia"
        if  texto.startswith("auxiliar"):
             return "auxiliar de investigacion"
     return texto
     
                        
          
    
    

