from pydantic import BaseModel


class paginar_info (BaseModel):
    
    poscion : str 
    siguiente: str
    anterior :str