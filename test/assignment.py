from nonebot_plugin_helldivers.info import Assignment

import asyncio


async def get_assignment():
    assignment = await Assignment.create()
    print(assignment)


asyncio.run(get_assignment())
