from typing import Union

from .harf import (
    TimingsF,
    BeforeAfterRequestF,
    CacheF,
    ContentF,
    ResponseF,
    ParamF,
    PostDataF,
    PostDataTextF,
    PostDataParamF,
    QueryStringF,
    HeaderF,
    CookieF,
    RequestF,
    EntryF,
    PageTimingsF,
    PageF,
    BrowserF,
    CreatorF,
    LogF,
    TopF,
)


Timings = TimingsF
BeforeAfterRequest = BeforeAfterRequestF
Cache = CacheF[BeforeAfterRequest, BeforeAfterRequest]
Content = ContentF
Header = HeaderF
Cookie = CookieF
Response = ResponseF[Cookie, Header, Content]
Param = ParamF
PostDataText = PostDataTextF
PostDataParam = PostDataParamF[Param]
PostData = Union[PostDataText, PostDataParam]
QueryString = QueryStringF
QueryParam = QueryString
Request = RequestF[Cookie, Header, QueryString, PostData]
Entry = EntryF[Request, Response, Cache, Timings]
PageTimings = PageTimingsF
Page = PageF[PageTimings]
Browser = BrowserF
Creator = CreatorF
Log = LogF[Creator, Entry, Browser, Page]
Har = TopF[Log]
