from fastapi import FastAPI
from fastapi import status

app = FastAPI()

#API check status
@app.get("/v1/status/",status_code=status.HTTP_200_OK)
def root():
    return "API is online and working"


# #doorbot
# @app.get("/v1/access/door/fob_id/{fob_id}")
# async def root():
#     return {"message": "Hello World"}


# #toolbot
# @app.get("/v1/access/tool/fob_id/{fob_id}")
# async def root():
#     return {"message": "Hello World"}