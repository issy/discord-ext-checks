from setuptools import setup

setup(
    name="discord-ext-checks",
    author="Issy",
    url="https://github.com/issy/discordpy-event-checks",
    version="0.0.1b",
    packages=["discord.ext.checks"],
    license="MIT",
    description="An extension module to add simple check decorators to event listeners in discord.py",
    install_requires=["discord.py>=1.4"],
    python_requires=">=3.5.3",
)
