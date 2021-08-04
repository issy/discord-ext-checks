import discord
from discord.ext import commands
from typing import Awaitable, Dict, Union


_ChannelType = Union[discord.abc.GuildChannel, discord.DMChannel]


async def guild_only(cog: commands.Cog, before: discord.Message, after: discord.Message) -> bool:
    return bool(after.guild)


async def dm_only(cog: commands.Cog, before: discord.Message, after: discord.Message) -> bool:
    return not bool(after.guild)


def has_permissions(**perms: bool) -> Awaitable:
    """
    Checks that the author has a certain permission set in this context
    For use in on_message event listeners
    """
    perms: Dict[str, bool]
    if not perms:
        raise TypeError(
            "Must provide at least one keyword argument to has_permissions")

    async def predicate(cog: commands.Cog, before: discord.Message, after: discord.Message) -> bool:
        author: Union[discord.Member, discord.User] = after.author
        channel: _ChannelType = after.channel
        user_permissions = channel.permissions_for(author)

        def check_permission(permission: Dict[str, bool]):
            permission_name, permission_value = permission
            return getattr(user_permissions, permission_name, not permission_value)

        return all(map(check_permission, perms.items()))

    return predicate


def self_has_permissions(**perms: bool) -> Awaitable:
    """
    Checks that the bot has a certain permission set in this context
    For use in on_message event listeners
    """
    perms: Dict[str, bool]
    if not perms:
        raise TypeError(
            "Must provide at least one keyword argument to has_permissions")

    async def predicate(cog: commands.Cog, before: discord.Message, after: discord.Message) -> bool:
        me: Union[discord.Member, discord.User] = getattr(
            after.guild if after.guild else after.channel,
            "me"
        )
        channel: _ChannelType = after.channel
        user_permissions = channel.permissions_for(me)

        def check_permission(permission: Dict[str, bool]):
            permission_name, permission_value = permission
            return getattr(user_permissions, permission_name, not permission_value)

        return all(map(check_permission, perms.items()))

    return predicate


def is_bot(predicate_case: bool = False) -> Awaitable:
    """
    Checks whether the message author is a bot
    """

    async def predicate(cog: commands.Cog, before: discord.Message, after: discord.Message) -> bool:
        return after.author.bot == predicate_case

    return predicate
