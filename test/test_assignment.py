import pytest
import aiohttp
import asyncio

from nonebug import App
from nonebot import logger


async def get_assignment_with_retry(retries : int = 3):
    from nonebot_plugin_helldivers import Assignment
    for retry in range(1, retries+1):
        try:
            assignment = await Assignment.create()
            print()
            print(assignment)
            break
        except aiohttp.client_exceptions.ClientConnectorError:
            logger.opt(colors=True).debug(f"网络连接错误，正在进行第 {retry} 次重试...")
            await asyncio.sleep(1)
        except Exception as e:
            raise e
    else:
        logger.error("全部尝试失败，放弃重试")
        raise aiohttp.client_exceptions.ClientConnectorError


@pytest.mark.asyncio
async def test_assignment(app: App):
    logger.debug("正在获取简报...")
    await get_assignment_with_retry()
    logger.debug("完成")
