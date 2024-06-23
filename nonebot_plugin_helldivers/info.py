from .api import API
from .utils import timestamp_to_describe_str, strptime_to_timestamp


from datetime import datetime
import asyncio


class Assignment:
    def __init__(self, raw, tasks, reward) -> None:
        self.raw = raw
        self.id = self.raw["id32"]
        self.progress = self.raw["progress"]
        self.due = self.raw["expiresIn"]  # in seconds
        self.type = self.raw["setting"]["type"]
        self.title = self.raw["setting"]["overrideTitle"]
        self.brief = self.raw["setting"]["overrideBrief"]
        self.description = self.raw["setting"]["taskDescription"]
        self.tasks = tasks
        self.reward = reward
        self.flags = self.raw["setting"]["flags"]

    @classmethod
    async def create(cls):
        raw = await API.GetRawApiV2AssignmentWar()
        raw = raw[0]
        all_planets_info = await API.GetApiV1PlanetsAll()
        all_planets_info_with_index = {
            planet["index"]: planet for planet in all_planets_info
        }
        tasks_coroutines = [
            Task.create(
                info=task,
                finished=raw["progress"][index],
                planet_info=all_planets_info_with_index.get(task["values"][-1], None),
            )
            for index, task in enumerate(raw["setting"]["tasks"])
        ]
        tasks = await asyncio.gather(*tasks_coroutines)
        reward = [Reward(reward) for reward in raw["setting"]["rewards"]]
        return cls(raw, tasks, reward)

    def get_remaining_time(self) -> str:
        return timestamp_to_describe_str(self.due, lang="zh")

    def __str__(self) -> str:
        if self.type == 4:
            return self.planets_attack_info()
        return ""

    def planets_attack_info(self):
        info = ""
        info += "# 重要指令\n\n"
        info += f"{self.brief}\n\n"
        info += "## 指令简报\n\n"
        info += f"{self.description}\n\n"
        info += "## 剩余时间\n\n"
        info += f"{self.get_remaining_time()}\n\n"
        info += "## 任务进度\n\n"
        info += "| 状况 | 星球 | 解放度 | 反攻度 | 人数 |\n"
        info += "| --- | --- | --- | --- | --- |\n"
        for task in self.tasks:
            info += f"{task}\n"
        info += "\n## 任务奖励\n\n"
        for reward in self.reward:
            info += f"- {reward.name} x{reward.amount}\n"
        return info


class Task:
    def __init__(self, info: dict, finished: bool = False) -> None:
        self.info = info
        self.type = info["type"]
        self.values = info["values"]
        self.valueTypes = info["valueTypes"]
        self.finished = finished

    @classmethod
    async def create(cls, info: dict, finished: bool = False, planet_info: dict = None):
        instance = cls(info, finished)
        planet_index = instance.values[-1]
        instance.planetInfo = (
            Planet(planet_info) if planet_info else await Planet.create(planet_index)
        )
        return instance

    def __str__(self) -> str:
        event = self.planetInfo.event
        finished = self.finished
        if event:
            percent = f"{event.get_regen():.2f}%"
            regen = f"{event.get_regen():.2f}%"
            sign = "🛡️"
        elif finished:
            percent, regen, sign = "已解放", "None", "✅"
        else:
            percent = f"{self.planetInfo.get_liberation():.5f}%"
            regen = f"{self.planetInfo.get_regen():.2f}%"
            sign = "❌"
        return f"| {sign} | {self.planetInfo.name} | {percent} | {regen} | {self.planetInfo.statistics.playerCount} |"


class Planet:
    def __init__(self, raw):
        self.raw = raw
        self.index = self.raw["index"]
        self.name = self.raw["name"]
        self.sector = self.raw["sector"]
        self.biome = Biome(self.raw["biome"])
        self.hazards = [Hazard(hazard) for hazard in self.raw["hazards"]]
        self.hash = self.raw["hash"]
        self.position = (self.raw["position"]["x"], self.raw["position"]["y"])
        self.waypoints = self.raw["waypoints"]
        self.maxHealth = self.raw["maxHealth"]
        self.health = self.raw["health"]
        self.disabled = self.raw["disabled"]
        self.initialOwner = self.raw["initialOwner"]
        self.currentOwner = self.raw["currentOwner"]
        self.regenPerSecond = self.raw["regenPerSecond"]
        self.event = Event.create(self.raw["event"])
        self.statistics = PlanetStatistics(self.raw["statistics"])
        self.attacking = self.raw["attacking"]

    @classmethod
    async def create(cls, index: int):
        raw = await API.GetApiV1Planets(index)
        return cls(raw)

    def get_liberation(self) -> float:
        return (1 - self.health / self.maxHealth) * 100

    def get_regen(self) -> float:
        return self.regenPerSecond * 60 * 60 / self.maxHealth * 100


class EventsAll:
    def __init__(self, raw) -> None:
        self.raw = raw
        self.planets = [Planet(planet) for planet in self.raw]

    @classmethod
    async def create(cls):
        info = await API.GetApiV1PlanetEvents()
        return cls(info)

    def __str__(self) -> str:
        info = ""
        events = {event_type: [planet for planet in self.planets if planet.event.eventType == event_type] for event_type in set(planet.event.eventType for planet in self.planets)}
        for event_type in events:
            info += f"## {Event.table[event_type]}任务\n\n"
            if event_type == 1:
                info += "| 星球 | 我方进度 | 敌人进度 | 剩余时间 | 人数 |\n"
                info += "| --- | --- | --- | --- | --- |\n"
                for planet in events[event_type]:
                    event = planet.event
                    info += f"| {planet.name} | {event.get_liberation():.2f}% | {event.get_regen():.2f}% | {event.get_remaining_time()} | {planet.statistics.playerCount} |\n"
        print(info)
        return ""

class Event:
    table = {1: "保卫"}

    def __init__(self, info: dict) -> None:
        self.id = info["id"]
        self.eventType = info["eventType"]
        self.faction = info["faction"]
        self.health = info["health"]
        self.maxHealth = info["maxHealth"]
        self.startTime = strptime_to_timestamp(info["startTime"])
        self.endTime = strptime_to_timestamp(info["endTime"])
        self.campaignId = info["campaignId"]
        self.jointOperationIds = info["jointOperationIds"]

    @classmethod
    def create(cls, info: dict):
        if info is None:
            return None
        return cls(info)

    def get_remaining_time(self) -> str:
        return timestamp_to_describe_str(self.endTime - datetime.now().timestamp(), lang="en")

    def get_liberation(self) -> float:
        return (1 - self.health / self.maxHealth) * 100

    def get_regen(self) -> float:
        now = datetime.now().timestamp()
        return (now - self.startTime) / (self.endTime - self.startTime) * 100


class Reward:
    table = {
        897894480: "奖章",
    }

    def __init__(self, info: dict) -> None:
        self.type = info["type"]
        self.id = info["id32"]
        self.name = self.table.get(self.id, "未知奖励")
        self.amount = info["amount"]


class PlanetStatistics:
    def __init__(self, info: dict) -> None:
        self.missionsWon = info["missionsWon"]
        self.missionsLost = info["missionsLost"]
        self.missionTime = info["missionTime"]
        self.terminidKills = info["terminidKills"]
        self.automatonKills = info["automatonKills"]
        self.illuminateKills = info["illuminateKills"]
        self.bulletsFired = info["bulletsFired"]
        self.bulletsHit = info["bulletsHit"]
        self.timePlayed = info["timePlayed"]
        self.deaths = info["deaths"]
        self.revives = info["revives"]
        self.friendlies = info["friendlies"]
        self.missionSuccessRate = info["missionSuccessRate"]
        self.accuracy = info["accuracy"]
        self.playerCount = info["playerCount"]


class Biome:
    def __init__(self, info: dict) -> None:
        self.name = info["name"]
        self.description = info["description"]


class Hazard:
    def __init__(self, info: dict) -> None:
        self.name = info["name"]
        self.description = info["description"]
