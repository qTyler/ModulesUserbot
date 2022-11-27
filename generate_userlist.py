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
    async def sglcmd(self, m):
        "<reply> - нужно ответить на сообщение с которого будет начинаться парсинг пользователей"
        max_users = 30 #default
        symbols_add = [
            '+',
            'plus',
            'плюс',
            '➕',
            '👍'
        ]
        if not m.chat:
            return await m.edit("<b>Это не чат</b>")

        usrlist = ''
        reply = await m.get_reply_message()
        if not reply:
            return await m.edit("бля")
        else:
            c = 0
            for msg in m.client.get_messages(m.chat.id, offset_id = reply.id, reverse=True, limit = 400):
                if max_users == c: break
                c += 1
                try:
                    if msg.text[0:1] in symbols_add:
                        user = utils.get_display_name(msg.sender)
                        if msg.sender == None:
                            user = msg.post_author
                            #uid = 0
                        else:
                            uid = msg.sender.id
                        if not user: user = m.chat.title
                except TypeError: continue
                except NameError: user = '* Аноним без должности'
                userlist += '{}. {}\n'.format(c, user)
        await message.edit(userlist)     
                    
