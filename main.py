import http.client
import re

conn = http.client.HTTPSConnection("aerodatabox.p.rapidapi.com")

headers = {
    'X-RapidAPI-Key': "93f5488671msh0f9bdb82e4a4714p1562d8jsn85879706bc13",
    'X-RapidAPI-Host': "aerodatabox.p.rapidapi.com"
}


class FindAirport:
    def __init__(self):
        """Create a new class that finds the airport around the user's location"""
        self.current_location = ""
        self.user_airport = ""

    def user_location(self):
        """Asks the user for a location"""
        user_loc = input("In which city are you currently located?")
        if " " in user_loc:
            split = user_loc.split(" ")
            join = "20%".join(split)
            self.current_location = join.lower()
        else:
            self.current_location = user_loc.lower()

    def find_airport(self):
        """Using the user's current location, provides the list of airports around"""
        api_request = "/airports/search/term?q=" + self.current_location + "&limit=10"
        conn.request("GET", api_request, headers=headers)
        res = conn.getresponse()
        data = res.read()
        api_result = data.decode("utf-8")

        print("Available airports in the city of " + self.current_location +" are: ")
        # Using regular expressions to get the names of the airports. 
        # re_pattern = r'(?<=\"name\" ).*(?= \"shortName\")
        re_pattern = r'.*'
        matches = re.findall(re_pattern, api_result)
        print(matches)




# Testing the class
if __name__ == '__main__':
    test1 = FindAirport()

    # Testing to see if the white space is correctly replaced with "20%"
    assert test1.current_location == ""
    test1.user_location()
    # assert test1.current_location == "chiang20%mai"

    test1.find_airport()


