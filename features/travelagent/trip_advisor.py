import httpx

class TripAdvisor:
    def __init__(self, api_key):
        self.__api_key = api_key
        self.__base_url = "https://api.content.tripadvisor.com/api/v1"

    async def location_search_async(self, search_query, category):
        """

        :param search_query:
        :param category:
        :return:
        """
        url = f"{self.__base_url}/location/search?searchQuery={search_query}&category={category}&language=en&key={self.__api_key}"
        headers = {
            "Referer": "holidaymatch.streamlit.app",
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
        """
        url = f"{self.__base_url}/location/{location_id}/photos?language=en&key={self.__api_key}"
        headers = {
            "Referer": "holidaymatch.streamlit.app",
            "accept": "application/json"
        }
        async with httpx.AsyncClient() as client:
            response = httpx.get(url, headers=headers)
            return response.json()

    async def location_details_async(self, location_id: int):
        url = f"{self.__base_url}/location/{location_id}/details?language=en&currency=CHF&key={self.__api_key}"
        headers = {
            "Referer": "holidaymatch.streamlit.app",
            "accept": "application/json"
        }
        async with httpx.AsyncClient() as client:
            response = httpx.get(url, headers=headers)
            return response.json()