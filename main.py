import http.client

import json

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
        self.available_airports = []
        self.airport_data = {}
        self.airport_iata = ""

    def user_location(self):
        """Asks the user for a location"""
        user_loc = input("In which city are you currently located?")
        if " " in user_loc:
            split = user_loc.split(" ")
            join = "%20".join(split)
            self.current_location = join.lower()
        else:
            self.current_location = user_loc.lower()

    def find_airport(self):
        """Using the user's current location, provides the list of airports around. 
           Calls choose_airport() method to have the user select and airport"""
        api_request = "/airports/search/term?q=" + self.current_location + "&limit=10"
        conn.request("GET", api_request, headers=headers)
        res = conn.getresponse()
        data = res.read()
        api_result = data.decode("utf-8")

        self.airport_data = json.loads(api_result)

        print("Available airports in the city of " + self.airport_data['searchBy'] +" are: ")

        for index, airport in enumerate(self.airport_data['items'], 1):
            print(str(index) + '. ' + airport['name'])
            self.available_airports.append(airport['name'])

        self.user_airport = self.choose_airport()
        

    def choose_airport(self):
        """From the available airports, makes the user to choose an airport"""
        while True:
            choice = input("Enter the number of your choice: ")

            try:
                choice = int(choice)
                if 1 <= choice <= len(self.available_airports):
                    selected_option = self.available_airports[choice-1]
                    print(f'You have selected: {selected_option}')
                    break
                else:
                    print("Invalid choice!")
            except ValueError:
                print("Invalid input! Please enter a number.")
        
        return selected_option
    
    def get_iata(self):
        """Gets the iata of the airport, which will be used in different parts of the code."""
        for airport in self.airport_data['items']:
            if self.user_airport in airport['name']:
                self.airport_iata = airport['iata']
                return self.airport_iata


 

# Testing the class
if __name__ == '__main__':
    test1 = FindAirport()

    # Testing to see if the white space is correctly replaced with "%20" when Chiang Mai is chosen as city. 
    assert test1.current_location == ""
    test1.user_location()
    ## assert test1.current_location == "chiang%20mai"

    test1.find_airport()
    test1.get_iata()
    # When the airport has been chosen as John F Kennedy in New York City
    ##assert test1.airport_iata == "JFK"


