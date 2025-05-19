import csv
from fastapi import FastAPI, status, HTTPException, Response, Header, Body
from pydantic import BaseModel

env = "dev"
latest_version = 1.0

doorbot_filename = "_doorbot_lines.csv"
toolbot_filename = "_toolbot_lines.csv"
toolbot_id_api_filname = "_tool_api_keys.csv"

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


# Doorbot Get Request v1.0
@app.get(
        "/access/door/fob_id/{fob_id}", status_code = status.HTTP_202_ACCEPTED, response_model=AccessOutput)
def doorbot_request(fob_id: str, response:Response, version: float = latest_version):
    response.headers["Version"] = '1.0'
    if version == 1.0:
        with open(f'{env}{doorbot_filename}','r',) as file:
            door_list = csv.reader(file)
            for row in door_list:
                if fob_id == row[0]:
                    return {"announce_name": row[1], "member_id":row[2]}
                
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                                detail ="user not on door access list",headers={"Version":"1.0"})
            # 403 Forbidden
            # The client does not have access rights to the content,
            # the server is refusing to give the requested resource.
            # Unlike 401, the client's identity is known to the server.
    else:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail = "Invalid API version, refer to API docs",headers={"Version":"1.0"})


# toolbot Post Request v1.0
@app.post("/access/tool/fob_id/{fob_id}", status_code = status.HTTP_202_ACCEPTED, response_model=AccessOutput)
def toolbot_request(fob_id: str, response:Response, api_key:str = Body(embed=True), version: float = latest_version):
    response.headers["Version"] = '1.0'
    if version == 1.0:
        # check if API key is valid and match to tool ID
        with open(f'{env}{toolbot_id_api_filname}','r',) as tool_api_keys:
            tool_ids = csv.reader(tool_api_keys)
            for row in tool_ids:
                if api_key in row[1]:
                    tool_id = row[0]
                    break
            else:
                raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail="API key not recognised",headers={"Version":"1.0"})
        # check if user can use tool
        with open(f'{env}{toolbot_filename}','r',) as tool_info:
            tool_access_list = csv.reader(tool_info)
            for row in tool_access_list:
                if fob_id == row[0] and tool_id == row[1]:
                    return {"announce_name": row[2], "member_id":row[3]}
                
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                                detail ="Forbidden - user not on this tools access list",
                                headers={"Version":"1.0"})
    # if version number is not valid
    else:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail = "Invalid API version, refer to API docs",
                            headers={"Version":"1.0"})