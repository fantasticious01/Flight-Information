import http.client
from datetime import datetime, timedelta
import json
import time

conn = http.client.HTTPSConnection("aerodatabox.p.rapidapi.com")

headers = {
    'X-RapidAPI-Key': "API-Key",
    'X-RapidAPI-Host': "aerodatabox.p.rapidapi.com"
}

class FlightInfo:
    def __init__(self, iata, local_airport):
        """Create a new class that provides flight information to the user"""
        self.possible_destination = []
        self.chosen_destination = ""
        self.destination_options = {}
        self.destination_iata = ""
        self.current_date = ""
        self.tolocal_dtime = ""
        self.fromlocal_dtime = ""
        self.aircraft_number = ""
        self.local_airport_iata = iata
        self.local_airport = local_airport

    def find_destination(self):
        """Allows the user to find a destination and the operating airlines. """

        conn.request("GET", "/airports/iata/" + self.local_airport_iata + "/stats/routes/daily", headers=headers)

        res = conn.getresponse()
        data = res.read()
        api_result = data.decode("utf-8")

        self.destination_options = json.loads(api_result)

        print("Possible destinations from  the city of " + self.local_airport +" are: \n")

        # Loop through the dictionary to provide the possible destinations. 
        for index, destination in enumerate(self.destination_options['routes'], 1):
            print(str(index) + '. ' + destination['destination']['name'])
            time.sleep(0.2)
            self.possible_destination.append(destination['destination']['name'])
        
        self.chosen_destination = self.select_destination()


    def select_destination(self):
        """Asks the user to choose a destination from the possible destinations."""
        while True:
            choice = input("\nEnter the number of your choice: ")

            try:
                choice = int(choice)
                if 1 <= choice <= len(self.possible_destination):
                    selected_option = self.possible_destination[choice-1]
                    print(f'\nYou have selected: {selected_option}')
                    break
                else:
                    print("Invalid choice!")
            except ValueError:
                print("Invalid input! Please enter a number.")
        
        return selected_option
    
    def get_destination_iata(self):
        """Finds the iata for the destination airport"""
        for airport in self.destination_options['routes']:
            if self.chosen_destination in airport['destination']['name']:
                self.destination_iata = airport['destination']['iata']
                return self.destination_iata

    
    def provide_operators(self):
        """Provides the list of airlines that operate to the user chosen destination"""
        operator = {}
        for destination in self.destination_options['routes']:
            if self.chosen_destination in destination['destination']['name']:
                operator = destination['operators']
        
        print("\nThe following airlines provide flights to your destination.\n")

        for index, airline in enumerate(operator, 1):
            print(str(index) + '. ' + airline['name'])


    def find_flight_dist_and_time(self):
        """Prints out to the user the distance and flight time to the destination airport."""
        conn.request("GET", "/airports/iata/" + self.local_airport_iata + "/distance-time/" + self.destination_iata, headers=headers)
        res = conn.getresponse()
        data = res.read()       
        api_result = data.decode("utf-8")

        distance_time = json.loads(api_result)
        distance = distance_time['greatCircleDistance']['mile']

        time = distance_time['approxFlightTime']

        print("\nThe distance from " + self.local_airport + " to " + self.chosen_destination + " is " + str(distance) 
              + " miles, and time to destination is " + time)
        
    # def set_date_time(self):
    #     """Returns the current date and time. This will be used to find the aircraft number."""
    #     current_datetime = datetime.now()
    #     added_time = current_datetime + timedelta(hours=12)
    #     formatted_datetime_added = added_time.strftime("%Y-%m-%dT%H:%M")
    #     formatted_datetime_curr = current_datetime.strftime("%Y-%m-%dT%H:%M")
    #     self.fromlocal_dtime = formatted_datetime_curr
    #     self.tolocal_dtime = formatted_datetime_added

    # def get_aircraft_number(self):
    #     conn.request("GET", "/flights/airports/iata/" + self.local_airport_iata + 
    #                  "/" + self.fromlocal_dtime + "/" + self.tolocal_dtime + 
    #                  "?withLeg=true&direction=Departure&withCancelled=true&withCodeshared=true&withCargo=true&withPrivate=true&withLocation=false", headers=headers)
    #     res = conn.getresponse()
    #     data = res.read()
    #     api_result = data.decode("utf-8")
    #     aircraft_data  = json.loads(api_result)

    #     for index in aircraft_data['departures']:
    #         print(index['arrival']['airport']['name'])
    #         if index['arrival']['airport']['name'] == self.chosen_destination:
    #             self.aircraft_number = index['number']
    #             return self.aircraft_number
            
    #         return print("No route to your destination!")



if __name__ == '__main__':
    test1 = FlightInfo("CNX", "ICN")
    
    # Testing the find_destination method of the FlightInfo class. 
    test1.find_destination()


    test1.provide_operators()

    #Testing get_destination_iata() method to see if the correct destination airport iata is found. 
    test1.get_destination_iata()
    #assert(test1.destination_iata == 'DMK')

    test1.find_flight_dist_and_time()

    # test1.set_date_time()

    # test1.get_aircraft_number()