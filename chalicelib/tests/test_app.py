

def test_index(client):
    response = client.http.get('/')
    assert response.body == b'there is no root'
    assert response.status_code == 404

# def test_send_current(client):
#     response = client.http.get('/sendcurrent')
#     print(response.body)