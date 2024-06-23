import pytest

from nonebug import App
from nonebot import logger


@pytest.mark.asyncio
async def test_assignment(app: App):
    from nonebot_plugin_helldivers.info import EventsAll
    logger.debug("正在获取全部星球的事件...")
    all_events = await EventsAll.create()
    str(all_events)
    logger.debug("完成")
