# 🔒 Licensed under the GNU GPLv3
# 🌐 https://www.gnu.org/licenses/agpl-3.0.html
# meta developer: @VacuumCleanr

from .. import loader, utils
from telethon.tl.types import Message
from telethon.utils import get_display_name
import datetime, requests
from time import strftime

@loader.tds
class RaffAss(loader.Module):
    """Модуль-помощник в проведении розыгрышей и рулеток"""

    strings = {
        "name": "RaffleAssistant",
        "error_no_pm": "<b>[UserBot]</b> Это не чат",
        "errr_no_reply": "<b>[UserBot]</b> Не тупи, никакой это не ответ :)",
        "no_rank": "Аноним без должности",
        "_list_begin":" ╭︎ 🗂 <b>Список участников:</b>\n",
        "_list_body" : "├︎ <b>{}</b>. {}\n", 
        "_list_footer":"╰︎ <b>{}</b>. {}\n",
    }
    
    def __init__(self):
        self.config = loader.ModuleConfig(
            loader.ConfigValue( # self.config["max_users"]
                "max_users",
                100,
                doc=lambda: "Максимальное количество участников. Значение по умолчанию",
                validator=loader.validators.Integer()
            ),
            loader.ConfigValue( # self.config["ignored_users"]
                "ignored_users",
                [ ],
                doc=lambda: "Список пользователей которым запрещено учавствовать в отборе на рулетку",
                validator=loader.validators.Series(validator=loader.validators.String())
            ),                 
            loader.ConfigValue( # self.config["trigger_symbols"]
                "trigger_symbols",
                ['+', 'plus', 'плюс', '➕', '👍', '✔️', '✅', '☑️'],
                doc=lambda: "Список триггеров для участия в отборе на рулетку",
                validator=loader.validators.Series(validator=loader.validators.String()) # 
            ),
            
            loader.ConfigValue( # self.config["theme_template"]
                "theme_template",
                " ╭︎ 🗂 <b>Список участников:</b>\n├︎ <b>{}</b>. {}\n╰︎ <b>{}</b>. {}\n",
                doc=lambda: "Шаблон/оформление отображаемого списка",
                validator=loader.validators.String() # 
            ),           
    )
        
    async def load_theme(self,):
        lines = self.config["theme_template"].split('\n')
        if len(lines) == 3: 
            return lines
        else: 
            return " ╭︎ 🗂 <b>Список участников:</b>\n├︎ <b>{}</b>. {}\n╰︎ <b>{}</b>. {}\n".split('\n')
        
    async def listview(self, list):
        i = 0
        cusers = len(list)
        listview = self.strings("_list_begin")
        for user in list:
           i += 1
           if cusers == i: listview += self.strings("_list_footer").format(i, user)
           else: listview += self.strings("_list_body").format(i, user)
        return listview   

    @loader.unrestricted
    async def uliucmd(self, m: Message):
        """ - Список идентификаторов пользователей которым запрещено участвие в отборе
        0 - запрет анонимным пользователям
        """
        pass
    
    @loader.unrestricted
    async def ulcmd(self, m: Message):
        """ <*reply> [max_users:int] - Gенерация списка участников для рулетки
           Пример генерации списка на 25 чел: .ul 25 
        """
        
        args = utils.get_args(m)
        chatid = utils.get_chat_id(m)
        max_users = self.config["max_users"]
        
        if args:
            try: max_users = int(args[0])
            except ValueError: pass
          
        if not m.chat:
            return await m.edit(self.string("error_no_pm"))

        reply = await m.get_reply_message()
        if not reply: return await m.edit(self.string("errr_no_reply"))
        else:
            c = 0
            usrlist = [ ]
            async for msg in m.client.iter_messages(chatid, offset_id = reply.id, reverse=True, limit = 400):
                if max_users == c: break
                useradd = ''
                try:
                    if str(msg.text).lower() in self.config["trigger_symbols"]: #self.symbols_add:
                        user = get_display_name(msg.sender)
                        if msg.sender == None:
                            user = msg.post_author
                            uid = 0
                        else:
                            uid = msg.sender.id
                        if not user: user = m.chat.title
                        if not user in usrlist:
                            c += 1
                            useradd = user
                            #self.usrlist.append(user)
                            
                except AttributeError: continue
                except TypeError: continue
                except NameError:
                    c += 1
                    useradd = self.strings("no_rank")
                    
                if useradd:
                    if uid in self.config["ignored_users"]: continue
                    else: usrlist.append(useradd)
                
        await utils.answer(m, await self.listview(usrlist))
