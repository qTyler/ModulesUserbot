# 🔒 Licensed under the GNU GPLv3
# 🌐 https://www.gnu.org/licenses/agpl-3.0.html
# meta developer: @VacuumCleanr

from .. import loader, utils
import datetime
from time import strftime


@loader.tds
class GenUL(loader.Module):
    """Генерация списка пользователей"""

    strings = {'name': 'GenUserList'}
    
    @loader.owner
    async def sglcmd(self, m: Message):
      "<reply> - нужно ответить на сообщение с которого будет начинаться парсинг пользователей"
      reply = await m.get_reply_message()
      if not reply:
        return await m.edit("бля")
      else:
        
