import time
import aiohttp
import requests
from typing import overload, Literal

from .enums import AnnouncementId, API_URL
from .objects import News, PageInfo

class Client:
    def __init__(self):
        self._session: requests.Session | None = None
        self._update_time: float | None = None

    @property
    def session(self) -> requests.Session | None:
        return self._session

    @property
    def closed(self) -> bool:
        return self._session is None

    @property
    def update_time(self) -> float | None:
        return self._update_time

    @overload
    def get_news(self, uid: AnnouncementId, page: int=0, max_rows: int=30, keyword: str="", pageinfo: Literal[True]=True) -> tuple[list[News], PageInfo]: ...

    @overload
    def get_news(self, uid: AnnouncementId, page: int=0, max_rows: int=30, keyword: str="", pageinfo: Literal[False, None]=None) -> list[News]: ...

    def _init(self, *, force: bool=False) -> None:
        if self._session and not force:
            return
        if self._session:
            self.close()
        self._session = requests.Session()
        self._update_time = time.time()

    def _cleanup(self) -> None:
        self._session = None
        self._update_time = None

    def close(self) -> None:
        if self._session:
            self._session.close()
        self._cleanup()

    def _get_news(self, uid: AnnouncementId, page: int=0, max_rows: int=30, keyword: str=""):
        data = {
            "field": "time",
            "order": "DESC",
            "pageNum": page,
            "maxRows": max_rows,
            "keyword": keyword,
            "uid": uid.value,
            "tf": "1",
            "auth_type": "user",
        }

        resp = self.session.post(API_URL, data=data)
        return resp.json()

    def get_news(self, uid: AnnouncementId, page: int=0, max_rows: int=30, keyword: str="", pageinfo: bool | None=None) -> list[News] | tuple[list[News], PageInfo]:
        self._init()
        data = self._get_news(uid, page, max_rows, keyword)

        results = []
        for news in data[1:]:
            results.append(
                News(
                    title=news["title"],
                    unitname=news["unit_name"],
                    clicks=news["clicks"],
                    time=news["time"],
                    id=news["newsId"]
                )
            )

        if pageinfo:
            info = data[0]
            page = PageInfo(
                num=info["pageNum"],
                rows=info["maxRows"],
                total=info["totalPages"]
            )
            return results, page

        return results
    
class AsyncClient:
    def __init__(self, cache: bool=False):
        self._session: aiohttp.ClientSession | None=None
        self._update_time: float | None = None

    @property
    def session(self) -> aiohttp.ClientSession | None:
        return self._session

    @property
    def closed(self) -> bool:
        return True if not isinstance(self._session, aiohttp.ClientSession) else self._session.closed

    @property
    def update_time(self) -> float | None:
        return self._update_time

    @overload
    async def get_news(self, uid: AnnouncementId, page: int=0, max_rows: int=30, keyword: str="", pageinfo: Literal[True]=True) -> tuple[list[News], PageInfo]: ...

    @overload
    async def get_news(self, uid: AnnouncementId, page: int=0, max_rows: int=30, keyword: str="", pageinfo: Literal[False, None]=None) -> list[News]: ...

    async def _init(self, *, force: bool=False) -> None:
        if self._session and not self._session.closed and not force:
            return
        if self._session:
            await self.close()
        self._session = aiohttp.ClientSession()
        self._update_time = time.time()

    def _cleanup(self) -> None:
        self._session = None
        self._update_time = None

    async def close(self) -> None:
        if self._session and not self._session.closed:
            await self._session.close()

        self._cleanup()

    async def _get_news(self, uid: AnnouncementId, page: int=0, max_rows: int=30, keyword: str=""):
        data = {
            "field": "time",
            "order": "DESC",
            "pageNum": page,
            "maxRows": max_rows,
            "keyword": keyword,
            "uid": uid.value,
            "tf": "1",
            "auth_type": "user",
        }
        print(uid.value)
        async with self.session.post(API_URL, data=data) as resp:
            # text = await resp.text()
            # print(text)
            return await resp.json(content_type=None)

    async def get_news(self, uid: AnnouncementId, page: int=0, max_rows: int=30, keyword: str="", pageinfo: bool | None = None) -> list[News] | tuple[list[News], PageInfo]:
        await self._init()
        data = await self._get_news(uid, page, max_rows, keyword)

        # print("current:", info["pageNum"])
        # print("max:", info["maxRows"])
        # print("total:", info["totalPages"])

        results = []
        for news in data[1:]:
            results.append(
                News(
                    title=news["title"],
                    unitname=news["unit_name"],
                    clicks=news["clicks"],
                    time=news["time"],
                    id=news["newsId"]
                )
            )
        if pageinfo:
            info = data[0]

            page = PageInfo(
                num=info["pageNum"],
                rows=info["maxRows"],
                total=info["totalPages"]
            )
            return results, page

        return results