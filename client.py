import requests
#
# data = requests.post("http://127.0.0.1:8000/adv/v1/user",
#                      json={"name":"Masha", "password":"12345",})
# print(data.status_code)
# print(data.json())

data = requests.get("http://127.0.0.1:8000/adv/v1/user/1")
print(data.json())
print(data.status_code)
#

#
#
data = requests.post("http://127.0.0.1:8000/adv/v1/login",
                     json={"name":"Sasha", "password":"12345"})

print(data.status_code)
print(data.json())
token = data.json()["token"]
# #
# # #
# data = requests.patch("http://127.0.0.1:8000/adv/v1/user/3",
#                      json={"name":"Dasha"},
#                       headers={"x-token":token}
#                      )
# print(data.json())
# print(data.status_code)
# # #
# # #
# data = requests.delete("http://127.0.0.1:8000/adv/v1/user/3", headers={"x-token":token})
# print(data.json())
# print(data.status_code)


# # #########################################################################



# data = requests.post("http://127.0.0.1:8000/adv/v1",
#                      json={"header":"guitar",
#                            "description":"red",
#                            "owner":"Sasha",
#                            "price":100,},
#                      headers={"x-token":token},
# #
#                      )
# print(data.json())
# print(data.status_code)
# #


#
# data = requests.get("http://127.0.0.1:8000/adv/v1/1")
# print(data.json())
# print(data.status_code)
# # # # #



# data = requests.patch("http://127.0.0.1:8000/adv/v1/1",
#                      json={"header":"guitar",
#                            "description":"blue",
#                            "owner":"Sasha",
#                            "price":50.9}, headers={"x-token":token}
#                      )
# print(data.json())
# print(data.status_code)




# params = {
#     "header": "guitar"
# }
#
# data = requests.get("http://127.0.0.1:8000/adv/search/", params=params)
# print(data.json())
# print(data.status_code)



#
# data = requests.delete("http://127.0.0.1:8000/adv/v1/1",headers={"x-token":token})
# print(data.json())
# print(data.status_code)
