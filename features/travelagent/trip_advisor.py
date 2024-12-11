# References: 
# - HTTPX. (n.d.). HTTPX: A next-generation HTTP client for Python. HTTPX. https://www.python-httpx.org/
# - TripAdvisor LLC. (n.d.). API Reference. https://tripadvisor-content-api.readme.io/reference/overview
import httpx

class TripAdvisor:
    """ Class to interact with the TripAdvisor API """
    def __init__(self, api_key):
        self.__api_key = api_key
        self.__base_url = "https://api.content.tripadvisor.com/api/v1"

    async def location_search_async(self, search_query, category):
        """ 
        The Location Search request returns a list of locations that match the search query. 

        :param search_query: The search query to search for locations.
        :param category: The category of the location to search for.

        :return: The location search results (JSON).

        For more information, visit: https://tripadvisor-content-api.readme.io/reference/searchforlocations
        """
        url = f"{self.__base_url}/location/search?searchQuery={search_query}&category={category}&language=en&key={self.__api_key}"
        headers = {
            "Referer": "https://streamlit.app",
            "accept": "application/json"
        }
        async with httpx.AsyncClient() as client:
            response = httpx.get(url, headers=headers)
            return response.json()

    async def location_photos_async(self, location_id: int):
        """
        The Location Photos request returns up to 5 high-quality photos for a specific location.

        Sizes (height x width) for each photo type are as follows:
            Thumbnail: Fixed 50x50px, cropped, resized, and optimized by Tripadvisor
            Small: Fixed 150x150px, cropped, resized, and optimized by Tripadvisor
            Medium: Max dimension 250px (can be height or width, depending on photo orientation), the other dimension is resized to maintain the aspect ratio
            Large: Max dimension 550px (same rules as Medium, resized to maintain aspect ratio)
            Original: This is the photo in its original resolution and aspect ratio as provided by the user who submitted it.

        :param location_id:
        :return:

        For more information, visit: https://tripadvisor-content-api.readme.io/reference/getlocationphotos
        """
        url = f"{self.__base_url}/location/{location_id}/photos?language=en&key={self.__api_key}"
        headers = {
            "Referer": "https://streamlit.app",
            "accept": "application/json"
        }
        async with httpx.AsyncClient() as client:
            response = httpx.get(url, headers=headers)
            return response.json()

    async def location_details_async(self, location_id: int):
        """ 
        The Location Details request returns detailed information about a specific location.

        :param location_id: The location ID to get the details for.
        :return: Detailed information about the location (JSON).

        For more information, visit: https://tripadvisor-content-api.readme.io/reference/getlocationdetails
        """
        url = f"{self.__base_url}/location/{location_id}/details?language=en&currency=CHF&key={self.__api_key}"
        headers = {
            "Referer": "https://streamlit.app",
            "accept": "application/json"
        }
        async with httpx.AsyncClient() as client:
            response = httpx.get(url, headers=headers)
            return response.json()