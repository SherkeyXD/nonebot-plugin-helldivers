import pytest

from nonebug import App
from nonebot import logger


@pytest.mark.asyncio
async def test_assignment(app: App):
    from nonebot_plugin_helldivers import Assignment

    logger.debug("正在获取简报...")
    assignment = await Assignment.create()
    print(assignment)
    logger.debug("完成")
