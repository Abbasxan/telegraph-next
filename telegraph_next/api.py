import asyncio
import logging
from json import dumps
from typing import List, IO

import aiofiles
import aiohttp
from aiohttp import ContentTypeError
from pydantic import TypeAdapter


from .exceptions import MethodIsNotAllowed, TelegraphError, FileIsNotPresented, InvalidFileExtension
from .html_transform import html2nodes
from .models import Account, Page
from .models import Node
from .models.page import PagesList
from .models.uploaded_file import UploadedFile
from .utils import normalize_locals, serialize_nodes


class APIEndpoints:
    """Class with endpoints of telegraph api"""

    base_uri = "https://149.154.164.13"
    CREATE_ACCOUNT = f"{base_uri}/createAccount"
    CREATE_PAGE = f"{base_uri}/createPage"
    EDIT_ACCOUNT_INFO = f"{base_uri}/editAccountInfo"
    GET_ACCOUNT_INFO = f"{base_uri}/getAccountInfo"
    GET_PAGE_LIST = f"{base_uri}/getPageList"
    REVOKE_ACCESS_TOKEN = f"{base_uri}/revokeAccessToken"
    UPLOAD = f"https://149.154.164.13/upload"

    @staticmethod
    def edit_page(page_name: str):
        return f"{APIEndpoints.base_uri}/editPage/{page_name}"

    @staticmethod
    def get_page(page_name: str):
        return f"{APIEndpoints.base_uri}/getPage/{page_name}"

    @staticmethod
    def get_views(page_name: str):
        return f"{APIEndpoints.base_uri}/getViews/{page_name}"


class Telegraph:
    """Telegraph API class"""

    def __init__(self, access_token=None, proxy=None):
        """
        Constructor of Class

        :param access_token: Access token. If not specified, limited quanity of methods will be availible, until you create account
        :param proxy: Proxy URL (e.g. http://proxy:port)
        """
        self.access_token = access_token
        self.proxy = proxy
        self.logger = logging.getLogger("Telegraph")

    async def create_account(self, short_name: str, author_name: str = None, author_url: str = None,
                             renew_token: bool = True):
        """
        Method for Creating new Account.

        :param short_name: Account name, helps users with several accounts remember which they are currently using
        :param author_name: Default author name used when creating new articles.
        :param author_url: Profile link, opened when users click on the author's name below the title.
        :param renew_token: Specifies, should be Telegraph object token renewed on method execution
        :return: Account object with access_token field
        """
        account: Account = await self.make_request(APIEndpoints.CREATE_ACCOUNT,
                                                   normalize_locals(locals(), "renew_token"),
                                                   model=Account)
        if renew_token:
            self.logger.debug(f"Token changed from {self.access_token} to {account.access_token}")
            self.access_token = account.access_token
        return account

    async def create_page(self, title: str, content: List[Node] = None, author_name: str = None, author_url: str = None,
                          return_content: bool = False, content_html: str = None) -> Page:
        """
        Create new telegraph page

        :param title: Page title
        :param content: Content of the page
        :param author_name: Author name, displayed below the article's title
        :param author_url: Profile link, opened when users click on the author's name below the title
        :param return_content: If true, content will be returned in content field
        :param content_html: Html Content, that will be converted into list of nodes
        :return: Page object, contains content if return_content is set to True
        """
        if content_html:
            content_json = serialize_nodes(html2nodes(content_html))
        elif not content:
            content_json = [""]
        else:
            content_json = serialize_nodes(content)

        params = normalize_locals(locals(), "content", "content_html", "content_json")
        params["content"] = dumps(content_json)
        page: Page = await self.make_request(APIEndpoints.CREATE_PAGE, json=params, method="post", model=Page)
        return page

    async def edit_page(self, path: str, title: str, content: List[Node] = None, content_html: str = None,
                        author_name: str = None, author_url: str = None, return_content: bool = False) -> Page:
        """
        Edit existing telegraph page

        :param path: Path to page
        :param title: Page title
        :param content: Content of the page
        :param author_name: Author name, displayed below the article's title
        :param author_url: Profile link, opened when users click on the author's name below the title
        :param return_content: If true, content will be returned in content field
        :param content_html: Html Content, that will be converted into list of nodes
        :return: Page object, contains content if return_content is set to True
        """
        if content_html:
            content_json = serialize_nodes(html2nodes(content_html))
        elif not content:
            content_json = [""]
        else:
            content_json = serialize_nodes(content)
        params = normalize_locals(locals(), "content", "content_html", "path")
        params["content"] = dumps(content_json)
        page: Page = await self.make_request(APIEndpoints.edit_page(path), json=params, method="post", model=Page)
        return page

    async def get_account_info(self, fields: List[str] = None):
        """
        Use this method to get information about a Telegraph account

        :param fields: List of account fields to return. Available fields: short_name, author_name, author_url, auth_url, page_count
        :return: an Account object
        """
        account_info = await self.make_request(APIEndpoints.GET_ACCOUNT_INFO, normalize_locals(locals()))
        return account_info

    async def revoke_access_token(self) -> dict:
        """
        Use this method to revoke access_token and generate a new one. Sets new access_token

        :return: Account object with access token field
        """
        account: dict = await self.make_request(APIEndpoints.REVOKE_ACCESS_TOKEN)
        self.logger.debug(f"Token changed from {self.access_token} to {account['access_token']}")
        self.access_token = account["access_token"]
        return account

    async def get_page(self, path: str, return_content: bool = False) -> Page:
        """
        Use this method to revoke access_token and generate a new one

        :param path: Path to the Telegraph page
        :param return_content: If true, content field will be returned
        :return: Page object
        """
        page: Page = await self.make_request(APIEndpoints.get_page(path), params=normalize_locals(locals(), "path"),
                                             model=Page)
        return page

    async def get_page_list(self, limit: int = 50, offset: int = 0) -> PagesList:
        """
        Use this method to get a list of pages belonging to a Telegraph account

        :param limit: Limits the number of pages to be retrieved
        :param offset: Sequential number of the first page to be returned
        :return: list of pages, sorted by most recently created pages first
        """
        pages: PagesList = await self.make_request(APIEndpoints.GET_PAGE_LIST, params=normalize_locals(locals()),
                                                   model=PagesList)
        return pages

    async def get_views(self, path: str, year: int = None, month: int = None, day: int = None, hour: int = None) -> int:
        """
        Use this method to get the number of views for a Telegraph article.

        :param path: Path to the Telegraph page
        :param year: Required if month is passed. If passed, the number of page views for the requested year will be returned.
        :param month: Required if day is passed. If passed, the number of page views for the requested month will be returned.
        :param day: Required if hour is passed. If passed, the number of page views for the requested day will be returned.
        :param hour: If passed, the number of page views for the requested hour will be returned.
        :return: By default, the total number of page views will be returned.
        """
        views_dict = await self.make_request(APIEndpoints.get_views(path), params=normalize_locals(locals(), "path"))
        return views_dict["views"]

    async def edit_account_info(self, short_name: str = None, author_name: str = None,
                                author_url: str = None) -> Account:
        """
        Use this method to update information about a Telegraph account.

        :param short_name: New account name
        :param author_name: New default author name used when creating new articles
        :param author_url: New default profile link, opened when users click on the author's name below the title
        :return: an Account object with the default fields
        """
        account = await self.make_request(APIEndpoints.EDIT_ACCOUNT_INFO, params=normalize_locals(locals()))
        return account

    async def upload_file(self, file_path: str = None, file_stream: IO = None, retries: int = 3):
        """
        Uploads a file to Catbox.moe (reliable fallback since telegra.ph/upload is globally unstable).
        Automatically retries up to `retries` times on transient errors.

        :param file_path: Path to file in local filesystem
        :param file_stream: IO object (e.g. from open())
        :param retries: Number of retry attempts on failure (default: 3)
        :return: UploadedFile object with full Catbox URL in .src
        :raises FileIsNotPresented: If no files were passed
        :raises Exception: If all retry attempts are exhausted
        """
        if not file_path and not file_stream:
            raise FileIsNotPresented

        last_error = None
        for attempt in range(1, retries + 1):
            try:
                data = aiohttp.FormData()
                data.add_field('reqtype', 'fileupload')

                if file_path:
                    # Async file read — non-blocking, safe under high load
                    async with aiofiles.open(file_path, "rb") as f:
                        file_bytes = await f.read()
                    data.add_field('fileToUpload', file_bytes, filename=file_path.split("/")[-1].split("\\")[-1])
                else:
                    data.add_field('fileToUpload', file_stream)

                self.logger.debug(f"Uploading file to Catbox (attempt {attempt}/{retries}).")
                async with aiohttp.ClientSession() as session:
                    async with session.post(
                        'https://catbox.moe/user/api.php',
                        data=data,
                        timeout=aiohttp.ClientTimeout(total=30)
                    ) as response:
                        media_url = (await response.text()).strip()

                if not media_url.startswith("http"):
                    raise Exception(f"Catbox rejected upload: {media_url}")

                return TypeAdapter(UploadedFile).validate_python({"src": media_url})

            except Exception as e:
                last_error = e
                self.logger.warning(f"Upload attempt {attempt}/{retries} failed: {e}")
                if attempt < retries:
                    await asyncio.sleep(1)

        raise Exception(f"Upload failed after {retries} attempts: {last_error}")

    async def make_request(self, endpoint: str, params: dict = None, method: str = "get", model=None,
                           use_token: bool = True, json=None, **extra_params):
        """
        Function for making requests to API

        :param endpoint: Telegraph API endpoints
        :param params: Params for request queries
        :param method: Request Method. Only "get" or "post" are allowed
        :param model: PyDantic model for after request transformation
        :param use_token: Specifies, should token be passed in params, or not
        :param extra_params: Extra options, that will be passed into request function (e.g. file)
        :return: json dict, if model is not set, else BaseModel object
        :raises: MethodIsNotAllowed: if method param is invalid
        """
        # OMG this looks so scary, I think it should be fixed
        if params is None:
            params = {}

        if self.access_token and use_token:
            if json is not None:
                json["access_token"] = self.access_token
            else:
                params["access_token"] = self.access_token

        if self.proxy:
            extra_params.setdefault("proxy", self.proxy)

        if method == "get":
            result = await self.get(endpoint, params=params, **extra_params)
        elif method == "post":
            result = await self.post(endpoint, params=params, json=json, **extra_params)
        else:
            raise MethodIsNotAllowed

        if not result["ok"]:
            raise TelegraphError(result["error"])

        data = result["result"]
        if model:
            return TypeAdapter(model).validate_python(data)
        return data

    @staticmethod
    async def get(url: str, params: dict = None, raw=False, encoding="utf-8", **extra_params):
        """
        Make asynchronus GET request

        :param url: Request URL
        :param params: Query Params
        :param raw: Specifies should function return raw string, or use json parser
        :param encoding: (if raw is set to True) Specifies string encoding
        :param extra_params: Extra request params, passed into session.get function
        :return: Dict or Str, depending on raw flag
        """
        headers = extra_params.pop("headers", {})
        if "149.154.164.13" in url:
            headers["Host"] = "telegra.ph" if url.endswith("/upload") else "api.telegra.ph"
            extra_params["ssl"] = False
            
        async with aiohttp.request("get", url, params=params, headers=headers, **extra_params) as response:
            if raw:
                return (await response.read()).decode(encoding=encoding)
            else:
                return await response.json()

    @staticmethod
    async def post(url: str, params: dict, raw=False, encoding="utf-8", **extra_params):
        """
        Make asynchronus POST request

        :param url: Request URL
        :param params: Query Params
        :param raw: Specifies should function return raw string, or use json parser
        :param encoding: (if raw is set to True) Specifies string encoding
        :param extra_params: Extra request params, passed into session.get function
        :return: Dict or Str, depending on raw flag
        """
        headers = extra_params.pop("headers", {})
        if "149.154.164.13" in url:
            headers["Host"] = "telegra.ph" if url.endswith("/upload") else "api.telegra.ph"
            extra_params["ssl"] = False
            
        async with aiohttp.request("post", url, params=params, headers=headers, **extra_params) as response:
            if raw:
                return (await response.read()).decode(encoding=encoding)
            else:
                return await response.json()
