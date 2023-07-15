import http.client
import time
import json

conn = http.client.HTTPSConnection("aerodatabox.p.rapidapi.com")

headers = {
    # User will need an api key
    'X-RapidAPI-Key': "API-KEY",
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

        print("\n\nAvailable airports in the city of " + self.airport_data['searchBy'] +" are: \n")
        time.sleep(0.5)
        # Loops through the dictionary to find available airports in the city. 
        for index, airport in enumerate(self.airport_data['items'], 1):
            print(str(index) + '. ' + airport['name'])
            self.available_airports.append(airport['name'])
            time.sleep(0.3)

        self.user_airport = self.choose_airport()
        return self.user_airport
        

    def choose_airport(self):
        """From the available airports, makes the user to choose an airport"""
        while True:
            choice = input("\nEnter the number of your choice: ")

            try:
                choice = int(choice)
                if 1 <= choice <= len(self.available_airports):
                    selected_option = self.available_airports[choice-1]
                    print(f'\nYou have selected: {selected_option}')
                    time.sleep(0.5)
                    break
                else:
                    print("Invalid choice!")
            except ValueError:
                print("Invalid input! Please enter a number.")
        
        return selected_option
    
    def get_iata(self):
        """Gets the iata of the user chosen airport."""
        for airport in self.airport_data['items']:
            if self.user_airport in airport['name']:
                self.airport_iata = airport['iata']
                return self.airport_iata
            
    def airport_time(self):
        """The method provides the current local day and time at the airport."""

        conn.request("GET", "/airports/iata/" + self.airport_iata + "/time/local", headers=headers)
        res = conn.getresponse()
        data = res.read()
        api_result = data.decode("utf-8")
        time_data = json.loads(api_result)
        current_day_and_time = time_data['time']['local']
        time_zone = time_data['timeZoneId']
        print(f"\nThe local day and time at the airport is {current_day_and_time} in timezone {time_zone}.\n\n")
        time.sleep(1)
        
        





 

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

    # Testing airport_time() method to see if it prints out the expected information. 
    test1.airport_time()




