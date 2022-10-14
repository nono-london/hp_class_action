import asyncio
import sys

from requests_helpers.aiohttp_libs.aiohttp_proxy_request import AioHttpWithProxy


async def get_url(url: str, proxy_universe_size: int = 50):
    aiottp_class = AioHttpWithProxy(proxy_universe_size=proxy_universe_size,
                                    timeout=20, )
    response = await aiottp_class.get_url_with_attack(url=url,
                                                      max_proxies=5000,
                                                      update_proxy=True)
    print(type(response))
    return response


if __name__ == '__main__':
    if sys.platform == "win32" and sys.version_info.minor >= 8:
        asyncio.set_event_loop_policy(
            asyncio.WindowsSelectorEventLoopPolicy()  # pylint: disable=no-member
        )

    event_loop = asyncio.get_event_loop()

    event_loop.run_until_complete(get_url(url='https://www.avendrealouer.fr/',
                                          proxy_universe_size=500))
