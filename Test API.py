

import http.client
import re

conn = http.client.HTTPSConnection("aerodatabox.p.rapidapi.com")

headers = {
    'X-RapidAPI-Key': "93f5488671msh0f9bdb82e4a4714p1562d8jsn85879706bc13",
    'X-RapidAPI-Host': "aerodatabox.p.rapidapi.com"
}

conn.request("GET", "/airports/search/term?q=grand%20rapids&limit=10", headers=headers)

res = conn.getresponse()
data = res.read()


pattern = r'Grand Rapids'

matches = re.findall(pattern, data.decode("utf-8"))

print(matches)

# name = "Daniel Park"
# if " " in name:
#     name_split = name.split(" ")
#     res = "nono".join(name_split)
# print(res)