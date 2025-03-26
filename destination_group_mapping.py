import json
from typing import Dict
from mapping import map_destination

destination_group_mapping = {
    "Mediterranean Sea": 2,
    "Thailand": 3,
    "Far East": 4,
    "South America": 5,
    "Central America": 6,
    "North America": 7,
    "Greek Islands": 8,
    "Western Europe": 10,
    "North Europe": 11,
    "North Africa": 12,
    "South Africa": 13,
    "United Arab Emirats": 15,
    "Islands of Spain": 17,
    "Australia": 19,
    "Persian Gulf": 20,
    "North Italy": 21,
    "North France": 23,
    "North Greece": 24,
    "North Thailand": 25,
    "North America East Coasts": 26,
    "North America West Coasts": 27,
    "Classical Europe": 28,
    "Cyprus": 29,
    "Tropical Islands": 30,
    "Balkan": 31,
    "City trips": 32,
    "Eastern Europe": 52,
    "South Italy": 71,
    "Portugal": 83
}

group_to_destinations = {
    "Australia": [],
    "Balkan": ["Belgrade", "Montenegro"],
    "Central America": ["Cancun"],
    "City trips": [],
    "Classical Europe": ["Amsterdam", "Athens", "Barcelona", "Berlin", "Bologna", "Lisbon", "London", "Madrid", "Milan", "Paris", "Rome", "Venice", "Verona", "Vienna"],
    "Cyprus": ["Ayia Napa", "Larnaca", "Limassol", "Paphos", "Protaras"],
    "Eastern Europe": ["Albanian beaches", "Athens", "Batumi", "Bucharest", "Budapest", "Burgas", "Chisinau", "Krakow", "Lake Balaton", "Montenegro", "Prague", "Riga", "Tbilisi", "Varna", "Warsaw"],
    "Far East": ["Ko Pha Ngan", "Koh Samui", "Phuket"],
    "Greek Islands": ["Athens Beaches", "Chania, Crete ", "Corfu", "Crete", "Halkidiki", "Kos ", "Lefkada", "Mykonos", "Rhodes", "Santorini", "Sitia, Crete", "Skiathos"],
    "Islands of Spain": ["Ibiza", "Palma de Mallorca", "Tenerife"],
    "Mediterranean Sea": ["Athens", "Athens Beaches", "Ayia Napa", "Chania, Crete ", "Corfu", "Crete", "Halkidiki", "Kos ", "Larnaca", "Limassol", "Malta", "Mykonos", "Paphos", "Protaras", "Rhodes", "Santorini", "Sitia, Crete", "Skiathos", "Thessaloniki"],
    "North Africa": [],
    "North America": ["New York"],
    "North America East Coasts": [],
    "North America West Coasts": [],
    "North Europe": [],
    "North France": [],
    "North Greece": [],
    "North Italy": ["Garda Lake", "Milan", "Turin", "Venice", "Verona"],
    "North Thailand": [],
    "Persian Gulf": ["Abu Dhabi", "Dubai"],
    "Portugal": ["Lisbon", "Porto"],
    "South Africa": [],
    "South America": [],
    "South Italy": ["Naples", "Sicily"],
    "Thailand": ["Ko Pha Ngan", "Koh Samui", "Phuket"],
    "Tropical Islands": ["Ko Pha Ngan", "Koh Samui", "Mauritius", "Phuket", "Seychelles", "Zanzibar"],
    "United Arab Emirats": ["Abu Dhabi", "Dubai"],
    "Western Europe": ["Amsterdam", "Barcelona", "Berlin", "Bologna", "French Riviera", "Garda Lake", "Lisbon", "London", "Madrid", "Milan", "Naples", "Nice", "Paris", "Porto", "Rome", "Stockholm", "Tenerife", "Turin", "Venice", "Verona", "Vienna"],
}


def map_destination_group(destination: str) -> int:
    return destination_group_mapping.get(destination, None)

def  get_group_destinations_ids(group: str) -> list[int]:
    destinations = group_to_destinations.get(group, [])
    return [map_destination(destination) for destination in destinations]