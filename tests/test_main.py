from fastapi.testclient import TestClient
from main import app
from main import latest_version

client = TestClient(app)

class TestAPIRoot:
    def test_api_root(self):
        response = client.get("/")
        assert response.status_code == 200
        assert response.headers["Version"] == '1.0'
        assert response.json() == {
        "documentation":"/docs",
        "author":"https://github.com/josephxtian/",
        "latest_version":latest_version
        }

class TestCheckAPIStatus:
    def test_check_api_status(self):
        response = client.get("/status/")
        assert response.status_code == 200
        assert response.headers["Version"] == '1.0'
        assert response.json() == {
        "body":"API is online and working",
        "latest_version":latest_version
            }

class TestDoorbot:
# test with no announce name
    def test_doorbot_without_announce_name(self):
        response = client.get("/access/door/fob_id/ff8d0h4749")
        assert response.status_code == 202
        assert response.headers["Version"] == '1.0'
        assert response.json() == {"announce_name": '', "member_id":663}

# test with announce name
    def test_doorbot_with_announce_name(self):
        response = client.get("/access/door/fob_id/ff8d0h4326")
        assert response.status_code == 202
        assert response.json() == {"announce_name": 'canene', "member_id":188}

# test with announce emoji
    def test_doorbot_with_emoji_announce_name(self):
        response = client.get("/access/door/fob_id/088dfh4b")
        assert response.status_code == 202
        assert response.json() == {"announce_name": '♂️', "member_id":930}

# test with incorrect fob_id
    def test_doorbot_with_false_keyfob(self):
        response = client.get("/access/door/fob_id/953ghf3n")
        assert response.headers["Version"] == '1.0'
        assert response.status_code == 403
        assert response.json() == {"detail":"user not on door access list"}

# test with partial fob_id
    def test_doorbot_with_partial_keyfob(self):
        response = client.get("/access/door/fob_id/088d")
        assert response.status_code == 403
        assert response.json() == {"detail":"user not on door access list"}

# test version 1.0 success
    def test_doorbot_v1_0(self):
        response = client.get("/access/door/fob_id/088dfh4b?version=1.0")
        assert response.status_code == 202
        assert response.json() == {"announce_name": '♂️', "member_id":930}

# test version 1.0 forbidden
    def test_doorbot_with_false_keyfob_v1_0(self):
        response = client.get("/access/door/fob_id/953ghf3n?version=1.0")
        assert response.status_code == 403
        assert response.json() == {"detail":"user not on door access list"}

# test non-existant version
    def test_doorbot_v2_0(self):
        response = client.get("/access/door/fob_id/088dfh4b?version=2.0")
        assert response.status_code == 400
        assert response.json() == {"detail":"Invalid API version, refer to API docs"}

class TestToolbot:
    def test_toolbot_no_api_key(self):
        response = client.post("/access/tool/fob_id/fnjlajpx")
        assert response.status_code == 422
        assert response.json() == {'detail': [{'type': 'missing', 'loc': ['body'], 'msg': 'Field required', 'input': None}]}

    def test_toolbot_with_api_key(self):
        response = client.post(
            "/access/tool/fob_id/fnjlajpx",
            json = {"api_key":"U38BJXNe"},
            )
        assert response.status_code == 202
        assert response.json() == {"announce_name": "Bub", "member_id":682}

    def test_toolbot_with_invalid_api_key(self):
        response = client.post(
            "/access/tool/fob_id/fnjlajpx",
            json = {"api_key":"b7jfdghs"},
            )
        assert response.status_code == 401
        assert response.json() == {"detail":"API key not recognised"}

    def test_toolbot_with_uninducted_user(self):
        response = client.post(
           "/access/tool/fob_id/fnjlajpx",
            json = {"api_key":"65ShbT8v"},
            )
        assert response.status_code == 403
        assert response.json() == {"detail":"Forbidden - user not on this tools access list"} 
    
    def test_toolbot_with_false_keyfob_valid_api_key(self):
        response = client.post(
            "/access/tool/fob_id/kgcdwgd",
            json = {"api_key":"U38BJXNe"}
        )
        assert response.status_code == 403
        assert response.json() == {"detail":"Forbidden - user not on this tools access list"}

    def test_version_1_0(self):
        response = client.post(
            "/access/tool/fob_id/fnjlajpx?version=1.0",
            json = {"api_key":"U38BJXNe"},
            )
        assert response.status_code == 202
        assert response.json() == {"announce_name": "Bub", "member_id":682}

    def test_non_existant_version(self):
        response = client.post(
            "/access/tool/fob_id/fnjlajpx?version=1.5",
            json = {"api_key":"U38BJXNe"},
            )
        assert response.status_code == 400
        assert response.json() == {"detail":"Invalid API version, refer to API docs"}