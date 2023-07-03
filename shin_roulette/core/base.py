import logging
import os

from interactions import Client, listen, logger_name


class CustomClient(Client):
    """Subclass of interactions.Client with our own logger and on_startup event"""

    # you can use that logger in all your extensions
    logger = logging.getLogger(logger_name)

    @listen()
    async def on_startup(self):
        self.logger.info(f'Logged in as {self.user} (ID: {self.user.id})')
