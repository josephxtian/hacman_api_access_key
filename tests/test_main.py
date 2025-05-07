from fastapi.testclient import TestClient
from main import app
from main import latest_version

client = TestClient(app)

class TestCheckAPIStatus:
    def test_check_api_status(self):
        response = client.get("/status/")
        assert response.status_code == 200
        assert response.json() == {
        "body":"API is online and working",
        "latest_version":latest_version
            }

class TestDoorbot:
# test with no announce name
    def test_doorbot_without_announce_name(self):
        response = client.get("/access/door/fob_id/ff8d0h4749")
        assert response.status_code == 202
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
        assert response.status_code == 403
        assert response.json() == {"detail":"user not on door access list"}

# test with partial fob_id
    def test_doorbot_with_false_keyfob(self):
        response = client.get("/access/door/fob_id/088d")
        assert response.status_code == 403
        assert response.json() == {"detail":"user not on door access list"}

# test version 1.0 success
    def test_doorbot_v1_0(self):
        response = client.get("/access/door/fob_id/088dfh4b?version=1.0")
        assert response.status_code == 202
        assert response.json() == {"announce_name": '♂️', "member_id":930}

# test version 1.0 forbidden
    def test_doorbot_with_false_keyfob(self):
        response = client.get("/access/door/fob_id/953ghf3n?version=1.0")
        assert response.status_code == 403
        assert response.json() == {"detail":"user not on door access list"}
