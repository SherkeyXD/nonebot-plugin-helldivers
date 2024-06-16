import asyncio

from nonebot import on_command
from nonebot.adapters.onebot.v11 import MessageEvent, MessageSegment
from nonebot.plugin import PluginMetadata

from nonebot import require

from .info import Assignment
from .config import Config

require("nonebot_plugin_htmlrender")
from nonebot_plugin_htmlrender import (  # noqa: E402
    md_to_pic,
)

__plugin_meta__ = PluginMetadata(
    homepage="https://github.com/SherkeyXD/nonebot-plugin-helldivers",
    name="绝地潜兵信息查询小助手",
    description="为了超级地球！",
    usage="简报：获取星系战争简要概况",
    type="application",
    supported_adapters={"~onebot.v11"},
    config=Config,
    extra={},
)


async def send_wait_message(
    send: callable, flag: asyncio.Event, time: int = 3, message: str = ""
):
    await asyncio.sleep(time)
    if not flag.is_set():
        await send(message)


short = on_command("简报", aliases={"hd简报"})


@short.handle()
async def get_war_info(event: MessageEvent):
    reply = MessageSegment.reply(id_=event.message_id)
    finished_flag = asyncio.Event()
    timer_task = asyncio.create_task(
        send_wait_message(
            lambda message: short.send(message),
            flag=finished_flag,
            time=3,
            message="正在与超级地球最高司令部进行通信，请民主地等待",
        )
    )
    try:
        info = await Assignment.create()
        finished_flag.set()
        timer_task.cancel()
        pic = await md_to_pic(str(info))
        await short.finish(reply + MessageSegment.image(pic))
    except IndexError:  # 目前没有任务
        await short.finish(
            reply + MessageSegment.text("等待超级地球最高司令部的进一步指令")
        )
