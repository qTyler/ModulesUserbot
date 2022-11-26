#          ▄▀█ █▀▄▀█ █▀█ █▀█ █▀▀
#          █▀█ █░▀░█ █▄█ █▀▄ ██▄
#
#             © Copyright 2022
#
#          https://t.me/amorescam
#
# 🔒 Licensed under the GNU GPLv3
# 🌐 https://www.gnu.org/licenses/agpl-3.0.html
# meta developer: @amoremods
# meta banner: https://raw.githubusercontent.com/AmoreForever/assets/master/Nytimer.jpg

from .. import loader, utils
import datetime
from time import strftime


@loader.tds
class NYMod(loader.Module):
    """Узнай, сколько осталось до нового года"""

    strings = {'name': 'NewYearTimer'}

    async def nycmd(self, message):
        """Check date"""
        now = datetime.datetime.today()
        ng = datetime.datetime(int(strftime('%Y')) + 1, 1, 1)
        d = ng - now
        mm, ss = divmod(d.seconds, 60)
        hh, mm = divmod(mm, 60)
        soon = '<b><emoji document_id=6334530007968253960>☃️</emoji> До <u>Нового года</u>: {} д. {} ч. {} м. {} s.</b>\n<b><emoji document_id=5393226077520798225>🥰</emoji> Встретить новый год вместе <u>семьей</u> или <u>друзьями</u>!</b>'.format(d.days, hh, mm, ss)
        await utils.answer(message, soon)
