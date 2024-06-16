from .api import API


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
        percent = (1 - self.planetInfo.health / self.planetInfo.maxHealth) * 100
        regen = (
            self.planetInfo.regenPerSecond * 60 * 60 / self.planetInfo.maxHealth * 100
        )
        msg = ""
        msg += "| ✅ |" if self.finished else "| ❌ |"
        msg += f" {self.planetInfo.name} | "
        msg += "100% | " if self.finished else f"{percent:.5f}% | "
        msg += "0% | " if self.finished else f"{regen:.2f}% | "
        msg += f"{self.planetInfo.statistics.playerCount} |"
        return msg


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
        self.event = self.raw["event"]
        self.statistics = PlanetStatistics(self.raw["statistics"])
        self.attacking = self.raw["attacking"]

    @classmethod
    async def create(cls, index: int):
        raw = await API.GetApiV1Planets(index)
        return cls(raw)


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
