# https://www.geeksforgeeks.org/get-post-requests-using-python/


# importing the requests library
import requests

  
# api-endpoint
URL = "http://localhost:5000/register"

r = requests.post(url = URL)

print(r.text)