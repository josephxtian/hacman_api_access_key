import csv
from fastapi import FastAPI, status, HTTPException, Response, Header
from pydantic import BaseModel

env = "dev_"
latest_version = 1.0

app = FastAPI()

class AccessOutput(BaseModel):
    announce_name: str
    member_id: int

# API root
@app.get("/",status_code=status.HTTP_200_OK)
def api_home(response:Response):
    response.headers["Version"] = '1.0'
    return {
        "documentation":"/docs",
        "author":"https://github.com/josephxtian/",
        "latest_version":latest_version
        }

# API check status
@app.get("/status/",status_code=status.HTTP_200_OK)
def check_api_status(response:Response):
    response.headers["Version"] = '1.0'
    return {
        "body":"API is online and working",
        "latest_version":latest_version
            }


# Doorbot v1.0
@app.get(
        "/access/door/fob_id/{fob_id}", status_code = status.HTTP_202_ACCEPTED, response_model=AccessOutput)
def doorbot_request(fob_id: str, response:Response, version: float = latest_version):
    response.headers["Version"] = '1.0'
    if version == 1.0:
        with open(f'{env}door_information.csv','r',) as file:
            door_list = csv.reader(file)
            for row in door_list:
                if fob_id == row[0]:
                    return {"announce_name": row[1], "member_id":row[2]}
                
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                                detail ="user not on door access list")
            # 403 Forbidden
            # The client does not have access rights to the content,
            # the server is refusing to give the requested resource.
            # Unlike 401, the client's identity is known to the server.


# toolbot DRAFT
@app.get("/access/tool/{tool}/fob_id/{fob_id}", status_code = status.HTTP_202_ACCEPTED, response_model=AccessOutput)
def toolbot_request(fob_id: str, response:Response, version: float = latest_version):
    response.headers["Version"] = '1.0'
    if version == 1.0:
        with open(f'{env}tool_information.csv','r',) as file:
            tool_access_list = csv.reader(file)
            for row in tool_access_list:
                if fob_id == row[0]:
                    return {"announce_name": row[1], "member_id":row[2]}
                
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                                detail ="user not on tool access list")
            # 403 Forbidden
            # The client does not have access rights to the content,
            # the server is refusing to give the requested resource.
            # Unlike 401, the client's identity is known to the server.
