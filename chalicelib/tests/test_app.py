

def test_index(client):
    response = client.http.get('/')
    assert response.body == b'there is no root'
    assert response.status_code == 404

# def test_send_current(client):
#     # response = client.http.get('/sendcurrent?withtime=800')
#     response = client.http.get('/sendcurrent')
#     print(response.json_body)

def test_info(client):
    response = client.http.get('/info')
    print(response.json_body)
    assert response.status_code == 200


# def test_ticked(client):
#     a = 600
#     z = 3000
#     t = 30
#     counter = 0
#     for i in range(int(a/t), int(z/t)):
#         response = client.http.get(f'/sendcurrent?withtime={str(i*t)}')
#         print(response.json_body)
#         counter+=1      
#     print('counter:', counter)


    
# def test_ticked(client):
#     a = 798
#     z = 798 + 100
#     t = 1
#     counter = 0
#     for i in range(int(a/t), int(z/t)):
#         response = client.http.get(f'/sendcurrent?withtime={str(i*t)}')
#         counter+=1      
#     print('counter:', counter)


# def test_many_times(client):
#     # a = 600
#     # z = 3000
#     # t = 30
#     a = 800
#     z = 1800
#     t = 3
#     counter = 0
#     for i in range(int(a/t), int(z/t)):
#         response = client.http.get(f'/manytime/{str(i*t)}')
#         # print(response.json_body)
#         counter+=1      
#     print('counter:', counter)