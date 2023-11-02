# Shin Roulette

A [discord.py](https://github.com/Rapptz/discord.py) bot to do FFXIV content.

Shin Roulette picks a random 8-man raid and assigns each player a random role and job.

Invite the bot here: https://discord.com/api/oauth2/authorize?client_id=1125704521251823667&permissions=2147493888&scope=bot

## Hosting the Bot

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
