import json
import requests
from typing import List, Optional
from datetime import datetime
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def load_offers() -> Optional[dict]:

    BASE_URL = "https://www.holidayheroes.de/api_no_auth/holiday_finder/offers/"

    try:
        # Construct request payload
        payload = {
            "locale": "de",
            "currency": "EUR",
            "fromwhere": ['BER'],
            "engine": {
                "market": 1,
                "where": [162],  # Default location ID
                "when": {
                    "months": {
                        "periods": [],
                        "min": None,
                        "max": None,
                        "nights": []
                    }
                },
                "who": {
                    "adult": 2,
                    "child": 0,
                    "room": 1,
                    "childAges": []
                },
                "what": [],
                "whereTxt": ["Paris"],
                "whatTxt": [],
                "destinationGroups": []
            },
            "filters": {
                "rating": [],
                "stops": [],
                "refundable": False,
                "board": [],
                "amenities": [],
                "amenitiesTxt": [],
                "luggage": {
                    "canAddTrolley": False,
                    "canAddCib": False
                },
                "flex": False
            },
            "sort": {"best": -1},
            "limit": 100,
            "offset": 0,
            "searchUserProfile": 0
        }

        results = {}

        timestamp = int(datetime.now().timestamp() * 1000)
        params = {
                "data": json.dumps(payload),
                "muid": "77cb4fd097a64e27fa65d827fcc76b34",
                "t": timestamp
            }
        
        logger.info(f"Making API request to: {BASE_URL} with params: {params}")
        response = requests.get(BASE_URL, params=params)
        response.raise_for_status()
        #logger.info(f"Response: {response.json()}")
        
        return results
        
    except requests.exceptions.RequestException as e:
        print(f"Error loading offers: {str(e)}")
        return None
    except json.JSONDecodeError as e:
        print(f"Error parsing response: {str(e)}")
        return None
