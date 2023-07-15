import FindAirport
import FlightInfo

user_airport = FindAirport.FindAirport()
user_airport.user_location()
local_airport = user_airport.find_airport()
local_iata = user_airport.get_iata()
user_airport.airport_time()

user_flight = FlightInfo.FlightInfo(iata = local_iata, local_airport = local_airport)
user_flight.find_destination()
user_flight.provide_operators()
user_flight.find_flight_dist_and_time()


