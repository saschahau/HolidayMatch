import asyncio

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

async def fetch_recommendations_with_images(travel_agent, destination_recommendations):
    """
    Fetch images for all destination recommendations asynchronously.
    """
    async def fetch_image(recommendation):
        photos = await travel_agent.get_location_photo(recommendation.name)
        if photos and "data" in photos and photos["data"]:
            first_photo = photos["data"][0]
            recommendation.image_url = first_photo["images"]["original"]["url"]
        else:
            recommendation.image_url = None  # Set to None if no image is found

    # Run the image fetch tasks concurrently
    await asyncio.gather(*(fetch_image(recommendation) for recommendation in destination_recommendations))
