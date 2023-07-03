import os

from core.base import CustomClient


def load_extensions(bot: CustomClient):
    """Automatically load all extension in the ./extensions folder"""

    bot.logger.info("Loading Extensions...")

    # go through all folders in the directory and load the extensions from all files
    # Note: files must end in .py
    for root, dirs, files in os.walk("extensions"):
        for file in files:
            if file.endswith(".py") and not file.startswith("__init__"):
                file = file.removesuffix(".py")
                path = os.path.join(root, file)
                python_import_path = path.replace("/", ".").replace("\\", ".")

                # load the extension
                bot.load_extension(python_import_path)

    bot.logger.info(
        f"< {len(bot.interactions.get(0, []))} > Global Interactions Loaded")
