from fastapi import APIRouter, File, Form, HTTPException, Query, Request, UploadFile
from pydantic import BaseModel

from configdatabase.configdbs import Database


grants_user_routes = APIRouter()

@grants_user_routes.get("/get_all_convenios")
def get_rows_info   (
                  
                    ):
    db = Database()
 
    return(db.get_all_convenios())
@grants_user_routes.get("/get_all_profesores")
def get_all_profesores   (
                  
                    ):
    db = Database()
 
    return(db.get_all_profesores())

@grants_user_routes.get("/get_rows_estudents")
def get_rows_info   (
                    previo: bool = Query(False, description="Parametro previo"),
                    next: bool = Query(False, description="Parametro next"),
                    poscion: int = Query(1, description="Parametro poscion")
                    ):
    db = Database()
    if previo == True and poscion!= 1:
        poscion = poscion -1
    return(db.get_all_estudents(poscion))


@grants_user_routes.get("/get_datos_pasantia")
def get_datos_pasantia   (
                    previo: bool = Query(False, description="Parametro previo"),
                    next: bool = Query(False, description="Parametro next"),
                    poscion: int = Query(1, description="Parametro poscion")
                    ):
    db = Database()
    if previo == True and poscion!= 1:
        poscion = poscion -1
    return(db.get_datos_pasantia(poscion))


@grants_user_routes.get("/get_con_opciones")
def get_con_opciones   (
        previo: bool = Query(False, description="Parametro previo"),
                    next: bool = Query(False, description="Parametro next"),
                    poscion: int = Query(1, description="Parametro poscion")
                  ):
    db = Database()
    if previo == True and poscion!= 1:
        poscion = poscion -1
    return(db.get_datos_xx(poscion))



@grants_user_routes.get("/get_sin_opciones")
def get_sin_opciones   (
        previo: bool = Query(False, description="Parametro previo"),
                    next: bool = Query(False, description="Parametro next"),
                    poscion: int = Query(1, description="Parametro poscion")
                  ):
    db = Database()
    if previo == True and poscion!= 1:
        poscion = poscion -1
    return(db.get_datos_monografia(poscion))



@grants_user_routes.get("/get_datos_auxiliar")
def get_datos_auxiliar   (
                    previo: bool = Query(False, description="Parametro previo"),
                    next: bool = Query(False, description="Parametro next"),
                    poscion: int = Query(1, description="Parametro poscion")
                    ):
    db = Database()
    if previo == True and poscion!= 1:
        poscion = poscion -1
    return(db.get_datos_auxiliar(poscion))

@grants_user_routes.get("/get_datos_convenio")
def get_datos_convenio   (
                    previo: bool = Query(False, description="Parametro previo"),
                    next: bool = Query(False, description="Parametro next"),
                    poscion: int = Query(1, description="Parametro poscion")
                    ):
    db = Database()
    if previo == True and poscion!= 1:
        poscion = poscion -1
    return(db.get_datos_convenio(poscion))


@grants_user_routes.get("/get_datos_pasantia_individual")
def get_datos_pasantia_individual   (
                  
                    id_pasantia: int = Query(1, description="id_pasantia")
                    ):
    db = Database()
    return(db.get_datos_pasantia_individual(id_pasantia))


@grants_user_routes.get("/get_datos_auxiliar_individual")
def get_datos_auxiliar_individual   (
                  
                    id_auxiliar: int = Query(1, description="id_auxiliar")
                    ):
    db = Database()
    return(db.get_datos_auxiliar_individual(id_auxiliar))


@grants_user_routes.get("/get_datos_monografia_individual")
async def get_datos_monografia_individual   ( request: Request ):
    data = await  request.json()
    id = data.get("id")
    db = Database()
    return(db.get_datos_monografia_individual(id))


@grants_user_routes.get("/docente")
async  def get_docente( 
                    previo: bool = Query(False, description="Parametro previo"),
                    next: bool = Query(False, description="Parametro next"),
                    poscion: int = Query(1, description="Parametro poscion")
                    ):
    db = Database()
    if previo == True and poscion!= 1:
        poscion = poscion -1
    return(db.get_docente(poscion))

@grants_user_routes.get("/get_all_Estado")
async  def get_all_Estado__():
  
    db = Database()
    return(db.get_all_Estado())

@grants_user_routes.get("/get_all_tipo_documento")
async  def get_all_tipo_documento__():
  
    db = Database()
    return(db.get_all_tipo_documento())


@grants_user_routes.get("/get_all_opciones_de_grado")
async  def get_all_opciones_de_grado__():
  
    db = Database()
    return(db.get_all_opciones_de_grado())


# las url o endponts por post 


@grants_user_routes.post("/get_datos_convenio_concreto")
async def get_datos_convenio_concreto   (request: Request
                  
                  
                    ):
   
    data = await  request.json()
    id = data.get("id")
    print(id)
    db = Database()
  
    return(db.get_datos_convenio_concreto(id))



@grants_user_routes.post("/get_datos_monografia_individual")
async def get_datos_monografia_individual   (
                  request: Request
               
                    ):
    data = await  request.json()
    numero_documento = data.get("numero_documento")
   
    db = Database()
    return(db.get_datos_monografia_individual(numero_documento))


@grants_user_routes.post("/get_pages_number")
async def get_pages_number( request: Request):
    data = await  request.json()
    tabla_nombre = data.get("tabla_nombre")
    db = Database()
    return(db.get_pages(tabla_nombre))


@grants_user_routes.post("/enviar_formulario")
async def enviar_formulario(datos: Request):
    # Lógica para procesar los datos recibidos
    data = await  datos.json()
    db = Database()
    print(data)
    nuevos_datos = {
        "numero_documento": data.get("numero_documento"),
        "nombre": data.get("nombre_completo"),           # Renombrado de nombre_completo a nombre
        "codigo": data.get("codigo"),
        "semestre": data.get("estado"),                 # Renombrado de estado a id_estado
        "creditos": data.get("creditos"),
        "solicitudes_sis": data.get("solicitudes_sis"),
        "id_documento": data.get("tipo_documento"),
        "id_estado": data.get("estado_descripcion"),
        "id_opcion": data.get("opcion_grado")
    }
    print(nuevos_datos)

    db.actualizar_usuario( data.get("numero_documento"), nuevos_datos)

    return {"message": "Usuario actualizado exitosamente"}
    
    #return {"message": "Formulario recibido exitosamente", "datos": datos}



@grants_user_routes.post("/pasantia_especifica")
async  def pasantia_especifica(request: Request):
    data = await  request.json()
    id = data.get("id")
    print(id)
    db = Database()
    return(db.get_datos_pasantia_individual(id))


@grants_user_routes.post("/docente_pasantia")
async  def post_docente_pasantia(request: Request):
    data = await  request.json()
    id = data.get("id")
    print(id)
    db = Database()
    return(db.post_docente_pasantia(id))


@grants_user_routes.post("/docente_monografia")
async  def post_docente_monografia(request: Request):
    data = await  request.json()
    id = data.get("id")
    print(id)
    db = Database()
    return(db.get_datos_pasantia_individual(id))


@grants_user_routes.post("/docente_auxiliar")
async  def post_docente_auxiliar (request: Request):
    data = await  request.json()
    id = data.get("id")
    print(id)
    db = Database()
    return(db.get_datos_pasantia_individual(id))

@grants_user_routes.post("/upload")
async def upload_file(
id_convenio : str = Form(...),
  id_profesor: str = Form(...),
    nombre: str = Form(...),
    anteproyecto: UploadFile = File(None),
    acta_de_satisfaccion: UploadFile = File(None),
    certificado_laboral: UploadFile = File(None),
    certificado_arl: UploadFile = File(None),
    horario_del_pasante: UploadFile = File(None),
    fecha_inicio: str = Form(...),  # Assuming the date is sent as a string
    terminada: bool = Form(...)
):
    # Process text fields
    print(f"ID Profesor: {id_profesor}")
    print(f"Nombre: {nombre}")
    print(f"fecha_inicio: {fecha_inicio}")
    print(f"terminada: {terminada}")
    print(f"terminada: {id_convenio}")
    
    anteproyecto_content = await anteproyecto.read() if anteproyecto else None
    acta_content = await acta_de_satisfaccion.read() if acta_de_satisfaccion else None
    certificado_laboral_content = await certificado_laboral.read() if certificado_laboral else None
    certificado_arl_content = await certificado_arl.read() if certificado_arl else None
    horario_del_pasante_content = await horario_del_pasante.read() if horario_del_pasante else None
    print(type(anteproyecto_content))
   # db = Database()
    #db.ceate_pasantia(id_profesor,nombre,anteproyecto_content,acta_content
                   #   ,certificado_laboral_content, certificado_arl_content , 
                     # horario_del_pasante_content, fecha_inicio, terminada)

    # Return response
    return {"status": "Success", "message": "Files and form data received"}



@grants_user_routes.post("/uploadmonografia")
async def upload_filemonografia(
  id_profesor: str = Form(...),
    nombre: str = Form(...),
    anteproyecto: UploadFile = File(None),
    documento_final: UploadFile = File(None),
    fecha_inicio: str = Form(...),  # Assuming the date is sent as a string
    terminada: bool = Form(...)
):
    # Process text fields
    print(f"ID Profesor: {id_profesor}")
    print(f"Nombre: {nombre}")
    print(f"fecha_inicio: {fecha_inicio}")
    print(f"terminada: {terminada}")

    
    anteproyecto_content = await anteproyecto.read() if anteproyecto else None
    acta_cdocumento_final = await documento_final.read() if documento_final else None

   
    db = Database()
  
    # Return response
    return {"status": "Success", "message": "Files and form data received"}



@grants_user_routes.post("/uploadauxiliar")
async def upload_fileauxiliar(
  id_profesor: str = Form(...),
    nombre: str = Form(...),
    anteproyecto: UploadFile = File(None),
    fecha_inicio: str = Form(...),  # Assuming the date is sent as a string
    terminada: bool = Form(...)
):
    # Process text fields
    print(f"ID Profesor: {id_profesor}")
    print(f"Nombre: {nombre}")
    print(f"fecha_inicio: {fecha_inicio}")
    print(f"terminada: {terminada}")

    
    anteproyecto_content = await anteproyecto.read() if anteproyecto else None
    print(anteproyecto_content)
   
    db = Database()
  
    # Return response
    return {"status": "Success", "message": "Files and form data received"}


@grants_user_routes.post("/uploaddocente")
async def upload_docente(
  
    nombre: str = Form(...),
    
    apellido: str = Form(...)
):
    # Process text fields
    print(f"ID Profesor: {apellido}")
    print(f"Nombre: {nombre}")

    
    
    db = Database()
  
    # Return response
    return {"status": "Success", "message": "Files and form data received"}


