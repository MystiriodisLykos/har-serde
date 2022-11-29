from functools import partial

from .harf import *


def harf_cata(a: Callable[[HarF[A]], A], h: FHar) -> A:
    def inner_cata(e: HarF) -> A:
        return harf_cata(a, e)

    fs = [inner_cata] * len(getattr(h, "__parameters__", []))
    if hasattr(h, "nmap"):
        subs = h.nmap(*fs)
    else:
        subs = h
    try:
        return a(subs)
    except Exception as e:
        raise RuntimeError(f"Error applying algebra to type: {type(subs)}") from e


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
