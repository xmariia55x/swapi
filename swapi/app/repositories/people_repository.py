import requests
from requests.exceptions import RequestException, HTTPError, Timeout

class PeopleRepository:
    def __init__(self, api_url: str, logger):
        self.api_url = api_url
        self.logger = logger

    def get_people(self, page: int = 1):
        self.logger.info("Calling Star Wars API to get people")

        try:
            response = requests.get(f'{self.api_url}/people/?page={page}', timeout=10) # Add timeout to avoid waiting infinite time
            response.raise_for_status() # Check if the HTTP status code is 200 OK
        except HTTPError as http_err:
            error_message = f"HTTP error occurred: {http_err}"
            self.logger.error(error_message)
            raise Exception(error_message)
        except Timeout as timeout_err:
            error_message = f"Request timed out: {timeout_err}"
            self.logger.error(error_message)
            raise Exception(error_message)
        except RequestException as req_err:
            error_mesage = f"Error during requests to API: {req_err}"
            self.logger.error(error_message)
            raise Exception(error_message)

        try:
            return response.json()
        except ValueError as json_err:
            error_mesage = f"JSON decoding failed: {json_err}"
            self.logger.error(error_message)
            raise Exception(error_message)