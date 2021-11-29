

def test_index(client):
    response = client.http.get('/')
    assert response.body == b'there is no root'
    assert response.status_code == 404

def test_info(client):
    response = client.http.get('/info')
    print(response.json_body)
    assert response.status_code == 200