
START_SECTION_STRING = """
Hii, I'm {} [✨]({})
_I am an Anime themed group management bot with some awesome features._

➢ *Uptime:* `{}`
➢ `{}` *users, across* `{}` *chats.*

_Make sure to read my_ *ᴀʙᴏᴜᴛ ᴍᴇ* _section to know how you can use me effectively._
Checkout full help menu by sending /help or click help button to know about me, modules, setup and usage.
• A @TeamUltraUnion Project.
"""

ABOUT_SECTION_STRING = """
*『 ᴀʙᴏᴜᴛ ꜱᴇᴄᴛɪᴏɴ: 』*

*{}* - A powerful and modular group management bot built to help your admins and you to manage your group easily.
*Here'ꜱ a shortlist what I can do and about me.*
\n • I can Restrict user.
 • I can greets users with customizable welcome messages and even set a group's rules.
 • I have an advanced anti-flood system.
 • I can warn users until they reach max warns, with each predefined actions such as ban, mute, kick, etc.
 • I have a note keeping system, blacklists, and even pre determined replies on certain keywords.
 • I check for admin's permission before executing any admin-only command and more stuffs.
 • I have more useful and fun modules by which I can help and entertainment you too.
 • I can chat with users by using [Itel AI](https://www.kukiapi.xyz/).
 • [Click here](https://youtube.com/playlist?list=PLR1ul39qY-jfgtjUdzTxV2On8O5OWbgTw) to watch tutorials about my basic modules on [Youtube](https://www.youtube.com).
 • *{}’s* reposiratory is public now on [{}], anyone can fork.
 Click [{}/{}]({}/{}/{}).
 - You can come at our support chat to ask about deploy errors and solutions.
 - Warning - Don't remove developers from Credits section, you'll get gban if you did that..
 - Put "This bot is a fork of [TeamUltraUnion/rajniixrobot](https://github.com/TeamUltraUnion/rajniixrobot.git)" in your bot's start message.
• Reach my support links by opening `ꜱᴜᴘᴘᴏʀᴛ 👨‍✈️` section.

*If you have any Question about me, let our team help you at @{}*.
*Thanks for using me ^_^,* [Click here](https://t.me/{}) *and join to support us*💙"""

DONATE_SECTION_STRING = """
*{}* is hosted on heroku server,
If you want to donate my developers, you can...,
• [Gpay](https://pay.google.com)
*UPI ID* - `dhruv040.04-1@okaxis`.
You can also DM my developers to ask about donation.

*What we do with donations?*
» _Donations can help us to run {} on a paid server by which she can will work faster than before with less downtime!_
» _Donations will help us to improve {} with more useful and fun modules._
» _These donations will also help us to help others, those who really need support._

 *Thanks a lot for thinking about donation❤️*
"""

HELP_SECTION_STRING = """
*『 ʜᴇʟᴘ ꜱᴇᴄᴛɪᴏɴ: 』*

Hey there! My name is *{}*.
ɪ'ᴍ ʜᴇʀᴇ ᴀᴄᴛɪᴠᴇ ᴛᴏ ʜᴇʟᴘ ʏᴏᴜʀ ᴀᴅᴍɪɴꜱ ᴍᴀɴᴀɢᴇ ᴛʜᴇɪʀ ɢʀᴏᴜᴘꜱ ᴡɪᴛʜ ᴍʏ ᴀᴅᴠᴀɴᴄᴇᴅ ᴍᴏᴅᴜʟᴇꜱ!
Have a look at the following for an idea of some of the things I can help you with.
*Main commands available:*
 • `/start` : Starts me, can be used to check I'm alive or no...
 • `/help` : PM's you this message.
 • `/help <module name>` : PM's you info about that module.
 • `/ereport <Feedback or Error report message>` : Report's a Request Appeal or Error Feedback to @{}.

*Need help? head to @{}*
Click on the buttons below to get documentation about specific modules!
 • /settings :
   • In PM: will sends you your settings for all supported modules.
   • In a group: will redirect you to PM, with  all that group's settings.\n\n
All commands can either used with forward slash or exlaimation mark!.
"""

MANUAL_SECTION_STRING = """
*『 ᴍᴀɴᴜᴀʟ ꜱᴇᴄᴛɪᴏɴ: 』*

Here is the help how to use me with my best performance, follow the steps below!
• First add {} to a group...
» Click the “ᴀᴅᴅ ᴍᴇ” button and select a group where you want me to help you and your admins :).
• Promote me with all admin rights to let me get in actions!.
• You can learn about module related helps by help menu, click “ʜᴇʟᴘ” to open, select a module to know about it.
• Now start learning and try to use me with my full strength!"""

ADMIN_SETUP_STRING = """
*｢ ᴀᴅᴍɪɴ ꜱᴇᴛᴜᴘ 」*

• To avoid slowing down, {} caches admin rights for each user.
This cache lasts about 10 minutes; this may change in the future.
This means that if you promote a user manually (without using the /promote command),
{} will only find out 10 minutes later.
• If you want to update them immediately, you can use the `/admincache` command,
that'll force {} to check who the admins are again and their permissions
• If you are getting a message saying:
`You must be this chat administrator to perform this action!`
• This has nothing to do with {}’s rights;
this is all about your permissions as an admin.
{} respects admin permissions;
if you do not have the Ban Users permission as a telegram admin,
you won't be able to ban users with Rajnii.
Similarly, to change {} settings,
you need to have the Change group info permission.
• The message very clearly says that you need these admin rights; {} already have enough."""

ANTISPAM_SETUP_STRING = """
*｢ ᴀɴᴛɪ-ꜱᴘᴀᴍ ꜱᴇᴛᴜᴘ 」*

\n\n*« Anti-Spam »*
• `/antispam <on/off>`: Change antispam security settings in the group, or return your current settings(when no arguments).
This helps protect you and your groups by removing spam flooders as quickly as possible.
• `/gmutespam <on/off>`: As same as antispam, but it mutes the Gmuted user instead of banning. (On Maintainance)

*« Anti-Flood »*
• `/setflood <int/'no'/'off'>`: enables or disables flood control
• `/setfloodmode <ban/kick/mute/tban/tmute> <value>`: Action to perform when user have exceeded flood limit. ban/kick/mute/tmute/tban
Antiflood allows you to take action on users that send more than x messages in a row. Exceeding the set flood will result in restricting that user.

*« Blacklist »*
• `/addblacklist <triggers>`: Add a trigger to the blacklist. Each line is considered one trigger, so using different lines will allow you to add multiple triggers.
• `/blacklistmode <off/del/warn/ban/kick/mute/tban/tmute>`: Action to perform when someone sends blacklisted words.
Blacklists are used to stop certain triggers from being said in a group.
Any time the trigger is mentioned, the message will immediately be deleted.
A good combo is sometimes to pair this up with warn filters!

*« Reports »*
• `/reports <on/off>`: Change report setting, or view current status.
  × If done in pm, toggles your status.
  × If in chat, toggles that chat's status.
If someone in your group thinks someone needs reporting, they now have an easy way to call all admins.

*« Locks »*
• `/lock <type>`: Lock items of a certain type (not available in private)
• `/locktypes`: Lists all possible locktypes
The locks module allows you to lock away some common items in the telegram world; the bot will automatically delete them!

*« Warns »*
• `/addwarn <keyword> <reply message>`: Sets a warning filter on a certain keyword. If you want your keyword to be a sentence, encompass it with quotes, as such: /addwarn "very angry" This is an angry user.
• `/warn <userhandle>`: Warns a user. After 3 warns, the user will be banned from the group. Can also be used as a reply.
• `/strongwarn <on/yes/off/no>`: If set to on, exceeding the warn limit will result in a ban. Else, will just kick.
If you're looking for a way to automatically warn users when they say certain things, use the /addwarn command.

*« Captcha »*
• `/captcha <off/soft/strong>`: All users that join, get muted
A button gets added to the welcome message for them to unmute themselves.
This proves they aren't a bot! soft - restricts users ability to post media for 24 hours.
strong - mutes on join until they prove they're not bots."""

SUPPORT_SECTION_STRING = """
*『 ꜱᴜᴘᴘᴏʀᴛ ꜱᴇᴄᴛɪᴏɴ:』*
*Just click the link below as it's mentioned:*

• Join support chat - @{}.
• Join updates channel - @{}.
"""

CREDITS_SECTION_STRING = """
*『 ᴅᴇᴠᴇʟᴏᴘᴇʀꜱ ꜱᴇᴄᴛɪᴏɴ: 』*

I'm thankful for them as they've given thier too much time in updating me.
• Main Developer   - @{}
• Normal Updates   - @sawada
• New Modules      - @lostdir69_but_flasho
• Update Modules   - @Awesome_RJ_official
• Base Code        - @SonOfLars"""

TANDC_SECTION_STRING = """
*『 ᴛᴇʀᴍꜱ & ᴄᴏɴᴅɪᴛɪᴏɴꜱ ꜱᴇᴄᴛɪᴏɴ: 』*
*The Terms and Conditions are as follows:*

• We respect everyone's privacy & we never collect Sensitive data from groups.
• {} is one of the safest, easiest and Moduler telegram bot.
• Messages between users and {} is End to End Encrypted!
• NSFW content spammers always get Permanent Global Ban in {}\'s Database.
• Be Active on your chats, if someone spamming your group, you can use report feature & you can also report us about that on @{} to appeal a Gban/Fban.
• Make sure antiflood is enabled, so nobody can flood/spam your group.
• Please don't spam bot commands or buttons weather in pm or in groups, it can make {} Slower to respond and
if we blacklist them who spams {}\'s buttons or commands, Hence {} will ignore thier existance.
• Global ban or unban appeals for {}? Read the [criteria](https://t.me/rajniixglobal/15) first.
Appeal Global Actions at [Support chat](https://telegram.me/{}).
• We only stores User ID, Usernames, Name only, which is needed bot to respond to any user.

_Terms & Conditions can be changed anytime, please check once a month._"""


START_GROUP_STRING = "I'm awake already!\n<b>Haven't slept since:</b> <code>{}</code>"
HELP_GROUP_STRING = "Click the button below to get help menu in your inbox!"