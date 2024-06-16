<div align="center">

# nonebot-plugin-helldivers

<img src="https://socialify.git.ci/SherkeyXD/nonebot-plugin-helldivers/image?font=Jost&logo=https%3A%2F%2Fstatic.wikia.nocookie.net%2Fhelldivers_gamepedia%2Fimages%2F8%2F8d%2FSuper_earth.png&name=1&owner=1&pattern=Diagonal%20Stripes&theme=Dark" alt="nonebot-plugin-helldivers" width="640" height="320" />

## For SuperEarth!

</div>

## 这是什么？

[NoneBot2](https://github.com/nonebot/nonebot2) 侧的 Helldivers 2 插件

目前的功能列表：

- 简报：发送当前的最高指令，包括任务的具体内容

## 安装插件

在 Bot 目录下运行如下指令

### 使用 nb-cli 安装（推荐）

```shell
nb plugin install nonebot-plugin-helldivers
```

### 使用包管理器安装

```shell
# pip
pip install nonebot-plugin-helldivers
# poetry
poetry add nonebot-plugin-helldivers
```

然后检查 `pyproject.toml` 文件中 `[tool.nonebot]` 下的 `plugins` 是否包含 `nonebot_plugin_helldivers`，如果没有则手动添加

## 配置插件

本插件无需配置

## TODO

- [ ] 使用游戏内的指令风格绘制图片，以及进度条显示
- [ ] 星系地图绘制，包括补给线以及各个星球战况
- [ ] 各个星球的环境以及条件（等待 API 支持）
