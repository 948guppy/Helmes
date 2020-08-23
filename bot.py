#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from discord.ext import commands
import discord
import traceback

import config
from cogs.utils.errors import *


class Helmes(commands.Bot):
    def __init__(self, **kwargs):
        super().__init__(command_prefix=commands.when_mentioned_or('h/'), **kwargs)
        for cog in config.cogs:
            try:
                self.load_extension(cog)
            except Exception as exc:
                print('Could not load extension {0} due to {1.__class__.__name__}: {1}'.format(cog, exc))

    async def on_ready(self):
        print('Logged on as {0} (ID: {0.id})'.format(self.user))

    async def on_command_error(self, ctx, exception):
        if isinstance(exception, commands.CheckFailure):
            return

        if isinstance(exception, PermissionNotFound):
            await ctx.send('コマンドを実行する権限がありません')
            return

        if isinstance(exception, NotGuildChannel):
            await ctx.send('サーバー内でのみ実行できるコマンドです')
            return

        if isinstance(exception, NotDMChannel):
            await ctx.send('DM内でのみ実行できるコマンドです')
            return

        if isinstance(exception, IncompletePreparing):
            await ctx.send('現在大会準備モードではありません')
            return

        if isinstance(exception, InvalidArgument):
            await ctx.send("引数が間違っている可能性があります")

        orig_error = getattr(exception, "original", exception)
        error_msg = ''.join(traceback.TracebackException.from_exception(orig_error).format())
        error_msg = "```py\n" + error_msg + "\n```"
        await ctx.send(error_msg)


bot = Helmes()

bot.run(config.token)
