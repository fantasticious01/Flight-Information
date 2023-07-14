import http.client

import json

conn = http.client.HTTPSConnection("aerodatabox.p.rapidapi.com")

headers = {
    'X-RapidAPI-Key': "93f5488671msh0f9bdb82e4a4714p1562d8jsn85879706bc13",
    'X-RapidAPI-Host': "aerodatabox.p.rapidapi.com"
}

class FlightInfo:
    def __init__(self):
        """Create a new class that provides flight information to the user"""
        self.possible_destination = []
        self.chosen_destination = ""
        self.destination_options = {}
        self.destination_iata = ""

    def find_destination(self):
        """Allows the user to find a destination and the operating airlines. """

                    ### The iata has been preset to CNX (Chiang Mai)!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!

        conn.request("GET", "/airports/iata/cnx/stats/routes/daily", headers=headers)

        res = conn.getresponse()
        data = res.read()
        api_result = data.decode("utf-8")

        self.destination_options = json.loads(api_result)

        # Loop through the dictionary to provide the possible destinations. 
        for index, destination in enumerate(self.destination_options['routes'], 1):
            print(str(index) + '. ' + destination['destination']['name'])
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


    def get_flight_dist_and_time(self):
        """Prints out to the user the distance and flight time to the destination airport."""




if __name__ == '__main__':
    test1 = FlightInfo()
    
    # Testing the find_destination method of the FlightInfo class. 
    test1.find_destination()


    ##test1.provide_operators()

    #Testing get_destination_iata() method to see if the correct destination airport iata is found. 
    test1.get_destination_iata()
    assert(test1.destination_iata == 'DMK')