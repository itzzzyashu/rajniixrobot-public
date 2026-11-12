import github

from telethon import events
from RajniiRobot import telethn


@telethn.on(events.NewMessage(pattern=r"^[/.\?-]repo$", incoming=True))
async def give_repo(event):
    g = github.Github()
    repo = g.get_repo("TeamUltraUnion/rajniirobot")
    list_of_users = "".join(
        f"*{count}.* [{i.login}](https://github.com/{i.login})\n"
        for count, i in enumerate(repo.get_contributors(), start=1)
    )

    text = f"""[Github](https://github.com/TeamUltraUnion/rajniixrobot.git) | [Support Chat](https://t.me/rajniixsupport)