import validators

async def urlValidator (url: str):

    if not (url.startswith(("http://", "https://"))):
        url = "https://" + url
    valid = validators.url(url)

    return valid, url