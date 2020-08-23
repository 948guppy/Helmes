import discord
from discord.ext import commands
import asyncio
import psycopg2
import os

DATABASE_URL = os.environ["DATABASE_URL"]

conn = psycopg2.connect(DATABASE_URL, sslmode='require')
c = conn.cursor()


class Setup(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def setup(self, ctx):
        """サーバーに対しセットアップを行います。これ以降の処理はこれで作成される専用チャンネルでのみ使用可能です。"""

        def check_guild(GUILD_ID):
            t = (GUILD_ID,)
            c.execute('SELECT category_id FROM guild_data WHERE guild_id=%s', t)
            result = len(c.fetchall())
            conn.commit()
            if result == 0:
                return True
            return False

        def save_guild(GUILD_ID, CATEGORY_ID, CHANNEL_ID):
            save = (GUILD_ID, CATEGORY_ID, CHANNEL_ID,)
            c.execute(
                "INSERT INTO guild_data (guild_id, category_id, channel_id) values (%s,%s,%s)", save)
            conn.commit()

        if check_guild(ctx.guild.id):
            category = await ctx.guild.create_category_channel(name="🐺人狼ツール")
            channel = await category.create_text_channel(name="🔧｜メンテナンス")
            save_guild(ctx.guild.id, category.id, channel.id)
            await ctx.send(f"セットアップが完了しました。これ以降は{channel.mention}で操作してください。")
            return
        await ctx.send("既にセットアップが完了しています")

    @commands.command()
    async def restore(self, ctx):
        """t/setupコマンドで作成されたチャンネルを修復します。"""

        def check_guild(GUILD_ID):
            t = (GUILD_ID,)
            c.execute('SELECT category_id FROM guild_data WHERE guild_id=%s', t)
            result = len(c.fetchall())
            conn.commit()
            if result == 0:
                return False
            return True

        def reload_guild(GUILD_ID):
            t = (GUILD_ID,)
            c.execute('SELECT category_id FROM guild_data WHERE guild_id=%s', t)
            category_channel = c.fetchone()
            c.execute('SELECT channel_id FROM guild_data WHERE guild_id=%s', t)
            text_channel = c.fetchone()
            conn.commit()
            return category_channel[0], text_channel[0]

        def delete_guild_data(GUILD_ID):
            t = (GUILD_ID,)
            c.execute('delete FROM guild_data WHERE guild_id=%s', t)
            conn.commit()

        def save_guild(GUILD_ID, CATEGORY_ID, CHANNEL_ID):
            save = (GUILD_ID, CATEGORY_ID, CHANNEL_ID,)
            c.execute(
                "INSERT INTO guild_data (guild_id, category_id, channel_id) values (%s,%s,%s)", save)
            conn.commit()

        delete_channels = []

        if check_guild(ctx.guild.id) is False:
            await ctx.send("セットアップが完了していません")
            return
        try:
            delete_channels.append(await self.bot.fetch_channel(reload_guild(ctx.guild.id)[0]))
            delete_channels.append(await self.bot.fetch_channel(reload_guild(ctx.guild.id)[1]))
            await ctx.send("修復の必要はありません")
        except discord.NotFound:
            delete_guild_data(ctx.guild.id)
            await ctx.send(f"修復中...", delete_after=2)
            for channel in delete_channels:
                await channel.delete()
            category = await ctx.guild.create_category_channel(name="🔧トーナメントツール")
            channel = await category.create_text_channel(name="トーナメントを作成")
            save_guild(ctx.guild.id, category.id, channel.id)
            await asyncio.sleep(2)
            await ctx.send(f"修復が完了しました。これ以降は{channel.mention}で操作してください。")
            return


def setup(bot):
    bot.add_cog(Setup(bot))
