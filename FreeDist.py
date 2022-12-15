from .. import loader, utils
from telethon.tl.types import Message
from telethon.utils import get_display_name
import datetime, requests, random
from time import strftime

@loader.tds
class FreeDistribution(loader.Module):
"""Программа беплатной раздачи ништяков"""

    strings = {
        "name": "FreeDistribution",
        "btnName": "🎁 Забрать халяву!",
        "":"",
        "error_store_empty", "Склад пуст раздавать нечего. Пополните склад!",
        
    }
  
    def __init__(self):
      self.config = loader.ModuleConfig(
            loader.ConfigValue(
                "DisTime",
                3,
                doc=lambda: "Время проведение раздачи в часах. Значение по умолчанию",
                validator=loader.validators.Integer()
            ),
            loader.ConfigValue(
                "LinkFrequency",
                2,
                doc=lambda: "Частота появление ссылки в час. Значение по умолчанию",
                validator=loader.validators.Integer()
            ),    
            loader.ConfigValue(
                "LinkLifetime",
                3,
                doc=lambda: "Время жизни ссылки в секундах. Значение по умолчанию",
                validator=loader.validators.Integer()
            ),         
            loader.ConfigValue( 
                "Store",
                [ ],
                doc=lambda: "Укажите ссылку на стафф (ключи, софт и т.д.), пример: https://privnote.com/QmPkpRR5#2NmQ0dOBG",
                validator=loader.validators.Series(validator=loader.validators.Url())
            ),
        )
    
    def _get_mark(self):
        url = self.config['Store'][random.randint(0, len(self.config['Store']))]
        return (
            {
                "text": self.config["btnName"],
                "url": url,
            }
        )
    
    @loader.unrestricted
    async def infocmd(self, message: Message):
        """Send userbot info"""

        if self.config["custom_button"]:
            await self.inline.form(
                message=message,
                text=self._render_info(True),
                reply_markup=self._get_mark(),
                **(
                    {"photo": self.config["banner_url"]}
                    if self.config["banner_url"]
                    else {}
                ),
            )
        else:
            try:
                await self._client.send_file(
                    message.peer_id,
                    self.config["banner_url"],
                    caption=self._render_info(False),
                )
            except Exception:
                await utils.answer(message, self._render_info(False))
            else:
                if message.out:
                    await message.delete()
    
    @loader.owner
    async def fdstrbcmd(self, m: Message):
        """ <время проведение раздачи> <частота появление ссылки в час> <время жизни ссылки> 
        Запускает раздачу ништяков!
        """
        reply = await m.get_reply_message()
        userid = reply.sender_id
        
        if args:
            try: 
                if len(args) == 1: self.config["DisTime"] = int(args[0])
                if len(args) == 2: self.config["LinkFrequency"] = int(args[1])
                if len(args) == 3: self.config["LinkLifetime"]  = int(args[2])
            except ValueError: pass
            
        if len(self.config['Store']) > 0:
          return await m.edit(self.strings("error_store_empty"))
        
        
