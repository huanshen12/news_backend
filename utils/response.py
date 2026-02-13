from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder



def success_response(data = None,message:str = "success"):
    response =  {
        "code":200,
        "message":message,
        "data":data
    }
    return JSONResponse(content=jsonable_encoder(response))
