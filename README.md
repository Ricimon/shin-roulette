# Shin-Roulette

A [discord.py](https://github.com/Rapptz/discord.py) bot to do FFXIV content.

## Getting Started

### Dependencies

- [Poetry](https://python-poetry.org/docs/)
- Python3.10+

### Running

A `.env` file needs to be created with the following contents:

```
DISCORD_TOKEN=<your discord bot token>
TEST_GUILD_ID=<guild id for quick slash command syncing> # optional
```

Perform a one-time install of python dependencies:

```bash
poetry install
```

To start the bot:

```bash
poetry run python shin_roulette/main.py
```

### Docker

This bot can be run in production environments by adding the `.env` file and
running through Docker:

```bash
docker-compose up -d
```
