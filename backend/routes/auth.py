from fastapi import APIRouter , Header ,HTTPException, Query, Request
from fastapi.responses import JSONResponse
from  pydantic import BaseModel , EmailStr
from configdatabase.configdbs import Database
from jwtconfig.functions_jwt import  write_token , validar_token
from configdatabase.configdbs import Database
from models.modelos_estradada_api import User

auth_routes = APIRouter()

@auth_routes.post("/login")
async  def login(request: Request):

    
    data = await  request.json()
    
    
    username = data.get("username")
    password = data.get("password")
    print(username + password )
    db = Database()

    if db.find_user_by_username(username,password)!= None:
        user = User(**data)

        return  write_token(user.__dict__)
    else:
        return JSONResponse(content={"message":"User not found"})

@auth_routes.post("/verificar/token")
async def verificar_token(request: Request):
    data = await  request.json()
    token = data.get("token")
   
    
    return(validar_token(token, True))


@auth_routes.post("/hello")
async  def hello(request: Request):

    
    data = await  request.json()
    
    
    username = data.get("username")
    password = data.get("password")
    print(username + password )
   
    return JSONResponse(content={"message":"User not found"})

