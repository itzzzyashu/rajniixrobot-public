from telethon import events
from RajniiRobot import arq, telethn, RAJNI_PTB


@telethn.on(events.NewMessage(pattern=r"^/arq(?:\s|$)", incoming=True))
async def arq_stats(event):
    data = await arq.stats()
    if not data.ok:
        return await event.reply(data.result)
    data = data.result
    uptime = data.uptime
    requests = data.requests
    cpu = data.cpu
    server_mem = data.memory.server
    api_mem = data.memory.api
    disk = data.disk
    platform = data.platform
    python_version = data.python
    users = data.users
    statistics = f"""
**>-< System >-<**
**Uptime:** `{uptime}`
**Requests Since Uptime:** `{requests}`
**CPU:** `{cpu}`
**Memory:**
    **Total Used:** `{server_mem}`
    **API:** `{api_mem}`
**Disk:** `{disk}`
**Platform:** `{platform}`
**Python:** `{python_version}`

**ARQ Statistics:**
**Users:** `{users}`

**@RajniiRobot Some Modules Running On ARQ**
"""
    await event.reply(statistics, link_preview=False)