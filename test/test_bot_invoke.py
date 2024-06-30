import random

import pytest

import nonebot
from nonebug import App
from nonebot.adapters.onebot.v11 import Adapter, Bot, Message


def make_event(message: str, group=False):
    from nonebot.adapters.onebot.v11.event import Sender
    from nonebot.adapters.onebot.v11 import PrivateMessageEvent, GroupMessageEvent

    msg = Message(message)
    if not group:
        return PrivateMessageEvent(
            time=1122,
            self_id=2233,
            post_type="message",
            sub_type="",
            user_id=2233,
            message_type="private",
            message_id=random.randrange(0, 10000),
            message=msg,
            original_message=msg,
            raw_message=message,
            font=1,
            sender=Sender(user_id=2233),
            to_me=False,
        )
    else:
        return GroupMessageEvent(
            time=1122,
            self_id=2233,
            group_id=3344,
            post_type="message",
            sub_type="",
            user_id=2233,
            message_type="group",
            message_id=random.randrange(0, 10000),
            message=msg,
            original_message=msg,
            raw_message=str(message),
            font=1,
            sender=Sender(user_id=2233),
            to_me=False,
        )


async def simple_test(
    test_func: callable,
    app: App,
    message: str,
):
    async with app.test_matcher(test_func) as ctx:
        adapter = nonebot.get_adapter(Adapter)
        bot = ctx.create_bot(base=Bot, adapter=adapter)
        event = make_event(message=message, group=True)
        ctx.receive_event(bot, event)
        ctx.should_finished(test_func)


@pytest.mark.asyncio
async def test_main_order(app: App):
    from nonebot_plugin_helldivers import main_order
    from nonebot_plugin_helldivers.info import Assignment

    md = str(await Assignment.create())
    print(md)
    # await simple_test(main_order, app, "简报")


@pytest.mark.asyncio
async def test_active_events(app: App):
    from nonebot_plugin_helldivers import active_events
    from nonebot_plugin_helldivers.info import ActiveEvents

    md = str(await ActiveEvents.create())
    print(md)
    # await simple_test(active_events, app, "事件")
