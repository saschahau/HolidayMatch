import asyncio
from datetime import datetime

def run_async_task(task, *args, **kwargs):
    """
    Helper function to run an asynchronous task in a blocking way.
    Args:
        task (coroutine): The asynchronous function to run.
        *args: Positional arguments for the async function.
        **kwargs: Keyword arguments for the async function.
    Returns:
        The result of the async task.
    """
    return asyncio.run(task(*args, **kwargs))

async def fetch_recommendations_with_images_async(travel_agent, destination_recommendations):
    """
    Fetch images for all destination recommendations asynchronously.
    """
    async def fetch_image(recommendation):
        photos = await travel_agent.get_location_photo_async(recommendation.name)
        if photos and "data" in photos and photos["data"]:
            first_photo = photos["data"][0]
            recommendation.image_url = first_photo["images"]["original"]["url"]
        else:
            recommendation.image_url = None  # Set to None if no image is found

    # Run the image fetch tasks concurrently
    await asyncio.gather(*(fetch_image(recommendation) for recommendation in destination_recommendations))

def get_current_plus_two_years():
    """
    Get the current year and the next two years.
    Returns:
        A list of the current year and the next two years.
    """
    # Get current year
    current_year = datetime.now().year

    # Generate list of years from current year to current year + 2
    # e.g. [2024, 2025, 2026]
    return [int(year) for year in range(current_year, current_year + 3)]