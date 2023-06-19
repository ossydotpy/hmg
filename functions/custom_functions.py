import aiohttp

async def send_api_request(apiurl, headers=None, params = None):
    async with aiohttp.ClientSession() as session:
      async with session.get(apiurl, headers=headers) as response:
        data = await response.json()
        return data, response.status