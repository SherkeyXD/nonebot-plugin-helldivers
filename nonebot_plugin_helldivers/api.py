import aiohttp
import asyncio

import uuid


class API:
    api_root = "https://api.helldivers2.dev"
    headers = {
        "Accept": "application/json",
        "Accept-Language": "zh-Hans",
        "X-Super-Client": f"nonebot-plugin-helldivers/{uuid.uuid4()}",
    }

    @staticmethod
    async def __makeRequest(url: str, max_retry: int = 5):
        async with aiohttp.ClientSession() as session:
            for attempt in range(max_retry):
                async with session.get(url, headers=API.headers) as res:
                    if res.status == 200:
                        # rate_limit_remaining = int(res.headers.get('X-RateLimit-Remaining', 1))
                        # if rate_limit_remaining <= 1:
                        #    await asyncio.sleep(10)
                        return await res.json()
                    elif res.status == 429:
                        retry_after = int(res.headers.get("Retry-After", 1))
                        await asyncio.sleep(retry_after)
                    else:
                        await asyncio.sleep(2**attempt)
        return None

    @staticmethod
    async def GetRawApiWarSeasonCurrentWarID() -> dict:
        """
        Returns the currently active war season ID.
        """
        info = await API.__makeRequest(
            API.api_root + "/raw/api/WarSeason/current/WarID"
        )
        return info

    @staticmethod
    async def GetRawApiWarSeasonStatus(WarID: int = 801) -> dict:
        """
        Get a snapshot of the current war status.
        """
        info = await API.__makeRequest(
            API.api_root + f"/raw/api/WarSeason/{WarID}/Status"
        )
        return info

    @staticmethod
    async def GetRawApiWarSeasonWarInfo(WarID: int = 801) -> dict:
        """
        Gets the current war info (planets position info included).
        """
        info = await API.__makeRequest(
            API.api_root + f"/raw/api/WarSeason/{WarID}/WarInfo"
        )
        return info

    @staticmethod
    async def GetRawApiStatsWarSummary(WarID: int = 801) -> dict:
        """
        Gets the current war summary and stats.
        """
        info = await API.__makeRequest(
            API.api_root + f"/raw/api/Stats/war/{WarID}/summary"
        )
        return info

    @staticmethod
    async def GetRawApiNewsFeed(WarID: int = 801) -> dict:
        """
        Retrieves a list of news messages from Super Earth.
        """
        info = await API.__makeRequest(API.api_root + f"/raw/api/NewsFeed/{WarID}")
        return info

    @staticmethod
    async def GetRawApiV2AssignmentWar(WarID: int = 801) -> dict:
        """
        Retrieves a list of currently active assignments (like Major Orders).
        """
        info = await API.__makeRequest(
            API.api_root + f"/raw/api/v2/Assignment/War/{WarID}"
        )
        return info

    @staticmethod
    async def GetApiV1War() -> dict:
        """
        Gets the current War state.
        """
        info = await API.__makeRequest(API.api_root + "/api/v1/war")
        return info

    @staticmethod
    async def GetApiV1AssignmentsAll() -> dict:
        """
        Fetches a list of all available Assignment information available.
        """
        info = await API.__makeRequest(API.api_root + "/api/v1/assignments")
        return info

    @staticmethod
    async def GetApiV1Assignments(index: int) -> dict:
        """
        Fetches a specific Assignment identified by index.
        """
        info = await API.__makeRequest(API.api_root + f"/api/v1/assignments/{index}")
        return info

    @staticmethod
    async def GetApiV1CampaignsAll() -> dict:
        """
        Fetches a list of all available Campaign information available.
        """
        info = await API.__makeRequest(API.api_root + "/api/v1/campaigns")
        return info

    @staticmethod
    async def GetApiV1Campaigns(index: int) -> dict:
        """
        Fetches a specific Campaign identified by index.
        """
        info = await API.__makeRequest(API.api_root + f"/api/v1/campaigns/{index}")
        return info

    @staticmethod
    async def GetApiV1DispatchesAll() -> dict:
        """
        Fetches a list of all available Dispatch information available.
        """
        info = await API.__makeRequest(API.api_root + "/api/v1/dispatches")
        return info

    @staticmethod
    async def GetApiV1Dispatches(index: int) -> dict:
        """
        Fetches a specific Dispatch identified by index.
        """
        info = await API.__makeRequest(API.api_root + f"/api/v1/dispatches/{index}")
        return info

    @staticmethod
    async def GetApiV1PlanetsAll() -> dict:
        """
        Fetches a list of all available Planet information available.
        """
        info = await API.__makeRequest(API.api_root + "/api/v1/planets")
        return info

    @staticmethod
    async def GetApiV1Planets(index: int) -> dict:
        """
        Fetches a specific Planet identified by index.
        """
        info = await API.__makeRequest(API.api_root + f"/api/v1/planets/{index}")
        return info

    @staticmethod
    async def GetApiV1PlanetEvents() -> dict:
        """
        Fetches all planets with an active Event.
        """
        info = await API.__makeRequest(API.api_root + "/api/v1/planet-events")
        return info

    @staticmethod
    async def GetApiV1Steam() -> dict:
        """
        Fetches the Steam newsfeed for Helldivers 2.
        """
        info = await API.__makeRequest(API.api_root + "/api/v1/steam")
        return info

    @staticmethod
    async def GetApiV1Steam2(gid: int) -> dict:
        """
        Fetches a specific newsfeed item from the Helldivers 2 Steam newsfeed.
        """
        info = await API.__makeRequest(API.api_root + f"/api/v1/steam/{gid}")
        return info
