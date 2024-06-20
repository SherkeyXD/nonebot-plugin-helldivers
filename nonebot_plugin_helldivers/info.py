from .api import API

from datetime import datetime, timezone


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
        tasks = [
            await Task.create(task, raw["progress"][index])
            for index, task in enumerate(raw["setting"]["tasks"])
        ]
        reward = [Reward(reward) for reward in raw["setting"]["rewards"]]
        return cls(raw, tasks, reward)

    def get_remaining_time(self) -> str:
        msg = ""
        if self.due > 60 * 60 * 24:
            msg += f"{self.due // (60*60*24)} 天 "
            self.due %= 60 * 60 * 24
        if self.due > 60 * 60:
            msg += f"{self.due // (60*60)} 小时 "
            self.due %= 60 * 60
        if self.due > 60:
            msg += f"{self.due // 60} 分钟 "
            self.due %= 60
        if self.due > 0:
            msg += f"{self.due} 秒 "
        return msg.strip()

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
    async def create(cls, info: dict, finished: bool = False):
        instance = cls(info, finished)
        planet_index = instance.values[-1]
        instance.planetInfo = await Planet.create(planet_index)
        return instance

    def __str__(self) -> str:
        event = self.planetInfo.event
        finished = self.finished
        if event:
            percent = (1 - event.health / event.maxHealth) * 100
            regen = f"{event.get_percentage():.2f}%"
            sign = "🛡️"
        elif finished:
            percent, regen, sign = 100, "None", "✅"
        else:
            percent = (1 - self.planetInfo.health / self.planetInfo.maxHealth) * 100
            regen = f"{(self.planetInfo.regenPerSecond * 60 * 60 / self.planetInfo.maxHealth * 100):.2f}%"
            sign = "❌"
        percentage = f"{percent:.5f}%" if not finished else "100.00%"
        return f"| {sign} | {self.planetInfo.name} | {percentage} | {regen} | {self.planetInfo.statistics.playerCount} |"


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


class Event:
    table = {1: "保卫"}

    def __init__(self, info: dict) -> None:
        self.id = info["id"]
        self.eventType = info["eventType"]
        self.faction = info["faction"]
        self.health = info["health"]
        self.maxHealth = info["maxHealth"]
        self.startTime = self.to_timestamp(info["startTime"])
        self.endTime = self.to_timestamp(info["endTime"])
        self.campaignId = info["campaignId"]
        self.jointOperationIds = info["jointOperationIds"]

    @classmethod
    def create(cls, info: dict):
        if info is None:
            return None
        return cls(info)

    @staticmethod
    def to_timestamp(string: str) -> float:
        date_part, frac_seconds_with_z = string.split(".")
        frac_seconds = frac_seconds_with_z[:-1]
        frac_seconds_truncated = frac_seconds[:6]
        adjusted_timestamp = f"{date_part}.{frac_seconds_truncated}Z"
        dt = datetime.strptime(adjusted_timestamp, "%Y-%m-%dT%H:%M:%S.%fZ")
        dt = dt.replace(tzinfo=timezone.utc)
        return dt.timestamp()

    def get_percentage(self) -> float:
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
