import requests
import urllib

session = requests.Session()
session.max_redirects = 10000
request = session.get("http://localhost")

chars = ""
for response in request.history:
    chars += urllib.parse.unquote(response.url.split("=")[-1])

print(chars)

# Take base64 and decode it for the flag
