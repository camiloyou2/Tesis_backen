from fastapi.responses import JSONResponse
from jwt import decode, encode
from datetime import datetime, timedelta
from os import getenv

def expire_date(days: int):
    """
    Calcula una fecha de expiración.

    Args:
        days (int): Número de días a partir de la fecha actual para calcular la fecha de expiración.

    Returns:
        datetime: La nueva fecha de expiración.
    """
    data = datetime.now()
    new_date = data + timedelta(days=days)
    return new_date

def expire_minutes(minutes: int) -> datetime:
    """
    Calcula una fecha de expiración en minutos.

    Args:
        minutes (int): Número de minutos a partir de la fecha actual para calcular la fecha de expiración.

    Returns:
        datetime: La nueva fecha de expiración.
    """
    data = datetime.now()
    new_date = data + timedelta(minutes=minutes)
    return new_date


def write_token(data: dict):
    """
    Genera un token JWT.

    Args:
        data (dict): Datos que se incluirán en el payload del token.

    Returns:
        str: Token JWT generado.
    """
   
    print(data)
    token = encode(payload={**data, "exp": expire_date(1)}, key=getenv("SECRET"), algorithm="HS256")
    return  JSONResponse(content={"token": token}, status_code=200)

def validar_token(token: str, output: bool = False):
    """
    Valida un token JWT.

    Args:
        token (str): Token JWT a validar.
        output (bool): Si es True, devuelve el payload decodificado del token. Por defecto es False.

    Returns:
        dict or JSONResponse: Payload decodificado del token si es válido, de lo contrario, una respuesta JSON con un mensaje de error y un código de estado 401.
    """
    try:
        print(token + "----------------------")
        decoded_token = decode(token, key=getenv("SECRET"), algorithms=["HS256"])
        print(decoded_token)
        if output:
            return True
        return False
    except Exception:
        return   False
