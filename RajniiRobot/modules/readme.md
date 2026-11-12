# RajniiRobot Example plugin format

```

## Advanced: Telethon
```python3
from RajniiRobot import telethn
from RajniiRobot.events import register

@register(pattern="^/hi$")
async def _(event):
    j = "Namaste"
    await event.reply(j)
    
__mod_name__ = "Hi"
__help__ = """
*Hi*
- /hi: Namaste
"""
```