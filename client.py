import requests

data = requests.post("http://127.0.0.1:8000/adv/v1",
                     json={"header":"bike",
                           "description":"red",
                           "owner":"Chapaev",
                           "price":20.9}
                     )
print(data.json())
print(data.status_code)


data = requests.get("http://127.0.0.1:8000/adv/v1/2")
print(data.json())
print(data.status_code)

data = requests.patch("http://127.0.0.1:8000/adv/v1/2",
                     json={"header":"bike",
                           "description":"blue",
                           "owner":"Chapaev",
                           "price":50.9}
                     )
print(data.json())
print(data.status_code)



data = requests.get("http://127.0.0.1:8000/adv/search?header=bike")
print(data.json())
print(data.status_code)

data = requests.delete("http://127.0.0.1:8000/adv/v1/1")
print(data.json())
print(data.status_code)
