import validators

async def urlValidator (url: str):
    valid = validators.url(url)

    return valid