from dataclasses import dataclass, replace
from functools import partial
from typing import TypeVar, Generic, Callable, List, Union, Any, Optional, Type

from serde import serde, SerdeSkip, field, to_dict

A = TypeVar("A")
B = TypeVar("B")
C = TypeVar("C")
D = TypeVar("D")

W = TypeVar("W")
X = TypeVar("X")
Y = TypeVar("Y")
Z = TypeVar("Z")

Func = Callable[[A], B]


skip_if_none = lambda: field(default=None, skip_if=lambda v: v is None)


@serde
class MISSING:
    """Sentinel value to use where a missing attribute is syntactically different from being set to None.

    For example, `Cache.afterRequest=MISSING` means the cache entry after the request is unavailable
    but, `Cache.afterRequest=None` means there is no cache entry after the request.
    """

    pass


def skip_if_missing() -> MISSING:
    return field(default=MISSING(), serializer=to_dict)


Missable = Union[MISSING, None, A]


@serde
@dataclass
class TimingsF:
    send: int
    wait: int
    receive: int
    blocked: Optional[int] = skip_if_none()
    dns: Optional[int] = skip_if_none()
    connect: Optional[int] = skip_if_none()
    ssl: Optional[int] = skip_if_none()
    comment: Optional[str] = skip_if_none()

    def nmap(self: "TimingsF") -> "TimingsF":
        return self


@serde
@dataclass
class BeforeAfterRequestF:
    lastAccess: str
    eTag: str
    hitCount: int
    expires: Optional[int] = skip_if_none()
    comment: Optional[str] = skip_if_none()

    def nmap(self: "BeforeAfterRequestF") -> "BeforeAfterRequestF":
        return self


@serde
@dataclass
class CacheF(Generic[A, B]):
    beforeRequest: Missable[A] = skip_if_missing()
    afterRequest: Missable[B] = skip_if_missing()
    comment: Optional[str] = skip_if_none()

    def nmap(self: "CacheF[A, B]", f: Func[A, W], g: Func[B, X]) -> "CacheF[W, X]":
        beforeRequest = self.beforeRequest
        afterRequest = self.afterRequest
        return CacheF(
            f(beforeRequest) if beforeRequest not in {MISSING, None} else beforeRequest,
            g(afterRequest) if afterRequest not in {MISSING, None} else afterRequest,
        )


@serde
@dataclass
class ContentF:
    size: int
    mimeType: str
    compression: Optional[int] = skip_if_none()
    text: Optional[str] = skip_if_none()
    encoding: Optional[str] = skip_if_none()
    comment: Optional[str] = skip_if_none()

    def nmap(self: "ContentF") -> "ContentF":
        return self


@serde
@dataclass
class ResponseF(Generic[A, B, C]):
    status: int
    statusText: str
    httpVersion: str
    cookies: List[A]
    headers: List[B]
    content: C
    redirectURL: str
    headersSize: int = -1
    bodySize: int = -1
    comment: Optional[int] = skip_if_none()

    def nmap(
        self: "ResponseF[A, B, C]",
        f: Func[A, W],
        g: Func[B, X],
        h: Func[C, Y],
    ) -> "ResponseF[W, X, Y]":
        return replace(
            self,  # type: ignore[arg-type]
            cookies=list(map(f, self.cookies)),
            headers=list(map(g, self.headers)),
            content=h(self.content),
        )


@serde
@dataclass
class ParamF:
    name: str
    value: Missable[str] = skip_if_missing()
    fileName: Optional[str] = skip_if_none()
    contentType: Optional[str] = skip_if_none()
    comment: Optional[str] = skip_if_none()

    def nmap(self: "ParamF") -> "ParamF":
        return self


@serde
@dataclass
class PostDataParamF(Generic[A]):
    mimeType: str
    params: List[A]
    comment: Optional[str] = skip_if_none()

    def nmap(self: "PostDataParamF[A]", f: Func[A, W]) -> "PostDataParamF[W]":
        return replace(
            self,  # type: ignore[arg-type]
            params=list(map(f, self.params)),
        )


@serde
@dataclass
class PostDataTextF:
    mimeType: str
    text: str
    comment: Optional[str] = skip_if_none()

    def nmap(self: "PostDataTextF") -> "PostDataTextF":
        return self


PostDataF = Union[PostDataTextF, PostDataParamF[A]]


@serde
@dataclass
class QueryStringF:
    name: str
    value: str
    comment: Optional[str] = skip_if_none()

    def nmap(self: "QueryStringF") -> "QueryStringF":
        return self


@serde
@dataclass
class HeaderF:
    name: str
    value: str
    comment: Optional[str] = skip_if_none()

    def nmap(self: "HeaderF") -> "HeaderF":
        return self


@serde
@dataclass
class CookieF:
    name: str
    value: str
    path: Optional[str] = skip_if_none()
    domain: Optional[str] = skip_if_none()
    expired: Optional[str] = skip_if_none()
    httpOnly: Optional[bool] = skip_if_none()
    secure: Optional[bool] = skip_if_none()
    comment: Optional[str] = skip_if_none()

    def nmap(self: "CookieF") -> "CookieF":
        return self


@serde
@dataclass
class RequestF(Generic[A, B, C, D]):
    method: str
    url: str
    httpVersion: str
    cookies: List[A]
    headers: List[B]
    queryString: List[C]
    headersSize: int = -1
    bodySize: int = -1
    postData: Optional[D] = skip_if_none()
    comment: Optional[str] = skip_if_none()

    def nmap(
        self: "RequestF[A, B, C, D]",
        f: Func[A, W],
        g: Func[B, X],
        h: Func[C, Y],
        i: Func[D, Z],
    ) -> "RequestF[W, X, Y, Z]":
        post_data = self.postData
        if post_data is not None:
            new_post_data: Optional[Z] = i(post_data)
        else:
            new_post_data = post_data
        return replace(
            self,  # type: ignore[arg-type]
            cookies=list(map(f, self.cookies)),
            headers=list(map(g, self.headers)),
            queryString=list(map(h, self.queryString)),
            postData=new_post_data,
        )


@serde
@dataclass
class EntryF(Generic[A, B, C, D]):
    startedDateTime: str
    time: int
    request: A
    response: B
    cache: C
    timings: D
    serverIPAddress: Optional[str] = skip_if_none()
    connection: Optional[str] = skip_if_none()
    pageref: Optional[str] = skip_if_none()
    comment: Optional[str] = skip_if_none()

    def nmap(
        self: "EntryF[A, B, C, D]",
        f: Func[A, W],
        g: Func[B, X],
        h: Func[C, Y],
        i: Func[D, Z],
    ) -> "EntryF[W, X, Y, Z]":
        return replace(
            self,  # type: ignore[arg-type]
            request=f(self.request),
            response=g(self.response),
            cache=h(self.cache),
            timings=i(self.timings),
        )


@serde
@dataclass
class PageTimingsF:
    onContentLoad: Optional[int] = -1
    onLoad: Optional[int] = -1
    comment: Optional[str] = skip_if_none()

    def nmap(self: "PageTimingsF") -> "PageTimingsF":
        return self


@serde
@dataclass
class PageF(Generic[A]):
    startedDateTime: str
    id: str
    title: str
    pageTimings: A
    comment: Optional[str] = skip_if_none()

    def nmap(self: "PageF[A]", f: Func[A, W]) -> "PageF[W]":
        return replace(
            self,  # type: ignore[arg-type]
            pageTimings=f(self.pageTimings),
        )


@serde
@dataclass
class BrowserF:
    name: str
    version: str
    comment: Optional[str] = skip_if_none()

    def nmap(self: "BrowserF") -> "BrowserF":
        return self


@serde
@dataclass
class CreatorF:
    name: str
    version: str
    comment: Optional[str] = skip_if_none()

    def nmap(self: "CreatorF") -> "CreatorF":
        return self


@serde
@dataclass
class LogF(Generic[A, B, C, D]):
    creator: A
    entries: List[B]
    pages: List[D] = field(default_factory=list)
    version: str = "1.2"
    browser: Optional[C] = None
    comment: Optional[str] = skip_if_none()

    def nmap(
        self: "LogF[A, B, C, D]",
        f: Func[A, W],
        g: Func[B, X],
        h: Func[C, Y],
        i: Func[D, Z],
    ) -> "LogF[W, X, Y, Z]":
        browser = self.browser
        if browser is None:
            new_browser: Optional[Y] = browser
        else:
            new_browser = h(browser)
        return replace(
            self,  # type: ignore[arg-type]
            creator=f(self.creator),
            entries=list(map(g, self.entries)),
            browser=new_browser,
            pages=list(map(i, self.pages)),
        )


@serde
@dataclass
class TopF(Generic[A]):
    log: A

    def nmap(self: "TopF[A]", f: Func[A, W]) -> "TopF[W]":
        return TopF(f(self.log))


HarF = Union[
    TimingsF,
    BeforeAfterRequestF,
    CacheF[A, A],
    ContentF,
    ResponseF[A, A, A],
    ParamF,
    PostDataF[A],
    QueryStringF,
    HeaderF,
    CookieF,
    RequestF[A, A, A, A],
    EntryF[A, A, A, A],
    PageTimingsF,
    PageF[A],
    BrowserF,
    CreatorF,
    LogF[A, A, A, A],
    TopF,
]

FHar = HarF["FHar"]  # type: ignore[misc]


def harf_cata(a: Callable[[HarF[A]], A], h: FHar) -> A:
    def inner_cata(e: HarF) -> A:
        return harf_cata(a, e)

    fs = [inner_cata] * len(getattr(h, "__parameters__", []))
    if hasattr(h, "nmap"):
        subs = h.nmap(*fs)
    else:
        subs = h
    return a(subs)


def harf(
    default: A,
    timing: Callable[[TimingsF], A] = None,
    before_after_request: Callable[[BeforeAfterRequestF], A] = None,
    cache: Callable[[CacheF], A] = None,
    content: Callable[[ContentF], A] = None,
    response: Callable[[ResponseF[A, A, A]], A] = None,
    param: Callable[[ParamF], A] = None,
    post_data: Callable[[PostDataF[A]], A] = None,
    querystring: Callable[[QueryStringF], A] = None,
    header: Callable[[HeaderF], A] = None,
    cookie: Callable[[CookieF], A] = None,
    request: Callable[[RequestF[A, A, A, A]], A] = None,
    entry: Callable[[EntryF[A, A, A, A]], A] = None,
    page_timing: Callable[[PageTimingsF], A] = None,
    page: Callable[[PageF[A]], A] = None,
    browser: Callable[[BrowserF], A] = None,
    creator: Callable[[CreatorF], A] = None,
    log: Callable[[LogF[A, A, A, A]], A] = None,
) -> Callable[[FHar], A]:
    def alg(h: HarF[A]) -> A:
        if isinstance(h, TimingsF):
            return timing(h) if timing else default
        if isinstance(h, BeforeAfterRequestF):
            return before_after_request(h) if before_after_request else default
        if isinstance(h, CacheF):
            return cache(h) if cache else default
        if isinstance(h, ContentF):
            return content(h) if content else default
        if isinstance(h, ResponseF):
            return response(h) if response else default
        if isinstance(h, ParamF):
            return param(h) if param else default
        if isinstance(h, PostDataTextF) or isinstance(h, PostDataParamF):
            return post_data(h) if post_data else default
        if isinstance(h, QueryStringF):
            return querystring(h) if querystring else default
        if isinstance(h, HeaderF):
            return header(h) if header else default
        if isinstance(h, CookieF):
            return cookie(h) if cookie else default
        if isinstance(h, RequestF):
            return request(h) if request else default
        if isinstance(h, EntryF):
            return entry(h) if entry else default
        if isinstance(h, PageTimingsF):
            return page_timing(h) if page_timing else default
        if isinstance(h, PageF):
            return page(h) if page else default
        if isinstance(h, BrowserF):
            return browser(h) if browser else default
        if isinstance(h, CreatorF):
            return creator(h) if creator else default
        if isinstance(h, LogF):
            return log(h) if log else default
        if isinstance(h, TopF):
            return h.log
        return default

    return partial(harf_cata, alg)


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
Request = RequestF[Cookie, Header, QueryString, PostData]
Entry = EntryF[Request, Response, Cache, Timings]
PageTimings = PageTimingsF
Page = PageF[PageTimings]
Browser = BrowserF
Creator = CreatorF
Log = LogF[Creator, Entry, Browser, Page]
Har = TopF[Log]
