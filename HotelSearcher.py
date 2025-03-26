import json
import logging
import requests

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def make_search(search_params: str) -> str:
    logger.info(f"Making search with params: {search_params}")
    # Extract relevant parameters for API call
    api_params = {
        "destinationIds": search_params.get("destinationIds", []),
        "rating": search_params.get("rating", []),
        "amenities": search_params.get("amenities", []),
        "preferences": search_params.get("preferences", [])
    }

    # Construct API URL with parameters
    base_url = "https://holidayfinder-co-il-len-cri-live.travelyo-qa.stagewearemove.com/api_no_auth/holiday_finder/offers-v2/"
    query_params = f"?data={json.dumps(api_params)}"
    url = base_url + query_params

    logger.info(f"Making API request to: {url}")

    
    
    try:
        response = requests.get(url)
        response.raise_for_status()  # Raise an exception for bad status codes
        return response.json()
    except requests.RequestException as e:
        logger.error(f"API request failed: {str(e)}")
        raise Exception(f"Failed to fetch holiday offers: {str(e)}")
    # Here you would make the actual curl request using requests library
    # For now just return the constructed URL
    return url