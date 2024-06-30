import pytest
import nonebot
from nonebug import NONEBOT_INIT_KWARGS
from nonebot.adapters.onebot.v11 import Adapter as OnebotV11Adapter

def pytest_configure(config: pytest.Config) -> None:
    config.stash[NONEBOT_INIT_KWARGS] = {
        "command_start": {""},
        "log_level": "DEBUG",
    }

@pytest.fixture(scope="session", autouse=True)
def load_adapters(nonebug_init: None):  # noqa: PT004
    driver = nonebot.get_driver()
    driver.register_adapter(OnebotV11Adapter)