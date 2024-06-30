import asyncio

from nonebot import on_command
from nonebot.plugin import PluginMetadata
from nonebot.plugin import inherit_supported_adapters

from nonebot import require

from .info import Assignment, ActiveEvents
from .config import Config

require("nonebot_plugin_htmlrender")
from nonebot_plugin_htmlrender import (  # noqa: E402
    md_to_pic,
)

require("nonebot_plugin_saa")
from nonebot_plugin_saa import (  # noqa: E402
    MessageFactory,
    Image,
    Text,
)


__plugin_meta__ = PluginMetadata(
    homepage="https://github.com/SherkeyXD/nonebot-plugin-helldivers",
    name="绝地潜兵信息查询小助手",
    description="为了超级地球！",
    usage="简报：获取星系战争简要概况",
    type="application",
    supported_adapters=inherit_supported_adapters("nonebot_plugin_saa"),
    config=Config,
    extra={},
)


async def handle_communication(task_creator):
    finished_flag = asyncio.Event()

    async def send_wait_message():
        await asyncio.sleep(3)
        if not finished_flag.is_set():
            await MessageFactory(
                Text("正在与超级地球最高司令部进行通信，请民主地等待")
            ).send(reply=False, at_sender=False)

    timer_task = asyncio.create_task(send_wait_message())

    try:
        info = await task_creator()
        finished_flag.set()
        timer_task.cancel()
        pic = await md_to_pic(str(info))
        await MessageFactory(Image(pic)).send(reply=True, at_sender=False)
    except IndexError as e:  # 目前没有任务
        await MessageFactory(Text(str(e))).send(reply=True, at_sender=False)
    except Exception as e:
        await MessageFactory(Text(f"发生错误：\n{str(e)}")).send(reply=True, at_sender=False)


main_order = on_command("简报", aliases={"hd简报"})
@main_order.handle()
async def get_main_order():
    await handle_communication(Assignment.create)
    await main_order.finish()


active_events = on_command("事件", aliases={"hd事件"})
@active_events.handle()
async def get_all_events():
    await handle_communication(ActiveEvents.create)
    await active_events.finish()
