'''import http.client

conn = http.client.HTTPSConnection("aerodatabox.p.rapidapi.com")

headers = {
    'X-RapidAPI-Key': "93f5488671msh0f9bdb82e4a4714p1562d8jsn85879706bc13",
    'X-RapidAPI-Host': "aerodatabox.p.rapidapi.com"
}

# Things change from here

# This requests for the flight dates of a specific flight between given dates.
conn.request("GET", "/flights/number/KE037/dates/2023-07-07/2023-07-15", headers=headers)

res = conn.getresponse()
data = res.read()

print(data.decode("utf-8"))'''

import http.client

conn = http.client.HTTPSConnection("aerodatabox.p.rapidapi.com")

headers = {
    'X-RapidAPI-Key': "93f5488671msh0f9bdb82e4a4714p1562d8jsn85879706bc13",
    'X-RapidAPI-Host': "aerodatabox.p.rapidapi.com"
}

conn.request("GET", "/airports/search/term?q=grand%20rapids&limit=10", headers=headers)

res = conn.getresponse()
data = res.read()

print(data.decode("utf-8"))