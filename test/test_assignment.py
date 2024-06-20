import pytest
import nonebot
from nonebug import App


@pytest.mark.asyncio
async def test_assignment(app: App):
    nonebot.load_from_toml("pyproject.toml")
    from nonebot_plugin_helldivers import Assignment
    assignment = await Assignment.create()
    print(assignment)

    
