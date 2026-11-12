import datetime
import re
import time
import urllib.request
import requests
import aiohttp

from datetime import datetime
from typing import List
from bs4 import BeautifulSoup
from countryinfo import CountryInfo
from faker import Faker
from faker.providers import internet
from PyDictionary import PyDictionary
from telethon import events, Button
from telethon import errors
from search_engine_parser import GoogleSearch
from tswift import Song
from youtubesearchpython import VideosSearch

from RajniiRobot.utils.inlinehelper import *
from RajniiRobot.utils.pluginhelpers import fetch, json_prettify
from RajniiRobot import telethn, OPENWEATHERMAP_ID, TIME_API_KEY, SUPPORT_CHAT, RAJNI_PTB

dictionary = PyDictionary()


class AioHttp:

    @staticmethod
    async def get_json(link):
        async with aiohttp.ClientSession() as session, session.get(
                link) as resp:
            return await resp.json()

    @staticmethod
    async def get_text(link):
        async with aiohttp.ClientSession() as session, session.get(
                link) as resp:
            return await resp.text()

    @staticmethod
    async def get_raw(link):
        async with aiohttp.ClientSession() as session, session.get(
                link) as resp:
            return await resp.read()


__mod_name__ = "Inline"
__help__ = """
INLINE BOT SERVICE OF @RajniiRobot
I'm more efficient when added as group admin. By the way these commands can be used by anyone in a group via inline.
──「 Syntax 」──
   @RajniiRobot [command] [query]
──「 Commands Available 」──
➛ alive - Check Bot's Stats.
➛ yt [query] - Youtube Search.
➛ tr [LANGUAGE_CODE] [QUERY]** - Translate Text.
➛ modapk [name] - Give you direct link of mod apk.
➛ ud [QUERY] - Urban Dictionary Query
➛ google [QUERY] - Google Search.
➛ webss [URL] - Take Screenshot Of A Website.
➛ bitly [URL] - Shorten A Link.
➛ wall [Query] - Find Wallpapers.
➛ pic [Query] - Find pictures.
➛ saavn [SONG_NAME] - Get Songs From Saavn.
➛ deezer [SONG_NAME] - Get Songs From Deezer.
➛ torrent [QUERY] - Torrent Search.
➛ reddit [QUERY] - Get memes from reddit.
➛ imdb [QUERY] - Search movies on imdb.
➛ spaminfo [ID] - Get spam info of the user.
➛ lyrics [QUERY] - Get lyrics of the song.
➛ paste [TEXT] - Paste text on pastebin.
➛ define [WORD] - Get definition from Dictionary.
➛ synonyms [WORD] - Get synonyms from Dictionary.
➛ antonyms [WORD] - Get antonyms from Dictionary.
➛ country [QUERY] - Get Information about given country.
➛ cs - Gathers Cricket info (Globally).
➛ covid [COUNTRY] - Get covid updates of given country.
➛ fakegen - Gathers fake information.
➛ weather [QUERY] - Get weather information.
➛ datetime [QUERY] - Get Date & time information of given country/region.
➛ app [QUERY] - Search for apps in playstore.
➛ gh [QUERY] - Search github.
➛ so [QUERY] - Search stack overflow.
➛ wiki [QUERY] - Search wikipedia.
➛ ping - Check ping rate.
➛ pokedex [TEXT]: Pokemon Search
"""

__MODULE__ = "Inline"
__HELP__ = """
 ==>> **INLINE BOT SERVICE OF @RajniiRobot** <<==
`I'm more efficient when added as group admin. By the way these commands can be used by anyone in a group via inline.`
   >> Syntax <<
@RajniiRobot [command] [query]
   >> Commands Available <<
- **alive** - __Check Bot's Stats.__
- **yt [query]** - __Youtube Search.__
- **tr [LANGUAGE_CODE] [QUERY]** - __Translate Text.__
- **ud [QUERY]** - __Urban Dictionary Query.__
- **google [QUERY]** - __Google Search.__
- **modapk [name]** - __Give you direct link of mod apk__
- **webss [URL]** - __Take Screenshot Of A Website.__
- **bitly [URL]** - __Shorten A Link.__
- **wall [Query]** - __Find Wallpapers.__
- **pic [Query]** - __Find pictures.__
- **saavn [SONG_NAME]** - __Get Songs From Saavn.__
- **deezer [SONG_NAME]** - __Get Songs From Deezer.__
- **torrent [QUERY]** - __Torrent Search.__
- **reddit [QUERY]** - __Get memes from redit.__
- **imdb [QUERY]** - __Search movies on imdb.__
- **spaminfo [id]** - __Get spam info of the user.__
- **lyrics [QUERY]** - __Get lyrics of given song.__
- **paste [TEXT]** - __Paste text on pastebin.__
- **define [WORD]** - __Get definition from Dictionary.__
- **synonyms [WORD]** - __Get synonyms from Dictionary.__
- **antonyms [WORD]** - __Get antonyms from Dictionary.__
- **country [QUERY]** - __Get Information about given country.__
- **cs** - __Gathers Cricket info (Globally).__
- **covid [COUNTRY]** - __Get covid updates of given country.__
- **fakegen** - __Gathers fake information.__
- **weather [QUERY]** - __Get weather information.__
- **datetime [QUERY]** - __Get Date & time information of given country/region.__
- **app [QUERY]** - __Search for apps on playstore.
- **gh [QUERY]** - __Search github.__
- **so [QUERY]** - __Search stack overfolw.__
- **wiki [QUERY]** - __Search wikipedia.__
- **ping** - __Check ping rate.__
- **pokedex [TEXT]** - __Pokemon Search.__
"""


@telethn.on(events.NewMessage(pattern=r"^[/.\?-]inline$", incoming=True))
async def inline_help(event):
    await event.reply(text=__HELP__)


@telethn.on(events.InlineQuery())
async def inline_query_handler(query):
    try:
        text = query.text.lower()
        answers = []
        if text.strip() == "":
            answerss = await inline_help_func(__HELP__)
            # Convert python dictionaries/objects to Telethon inline builder results if needed, or wrap appropriately
            await query.answer(answerss, cache_time=10)
            return
            
        cmd = text.split()[0]
        if cmd == "alive":
            answerss = await alive_function(answers)
            await query.answer(answerss, cache_time=10)
        elif cmd == "tr":
            lang = text.split()[1]
            tex = text.split(None, 2)[2]
            answerss = await translate_func(answers, lang, tex)
            await query.answer(answerss, cache_time=10)
        elif cmd == "ud":
            tex = text.split(None, 1)[1]
            answerss = await urban_func(answers, tex)
            await query.answer(answerss, cache_time=10)
        elif cmd == "google":
            tex = text.split(None, 1)[1]
            answerss = await google_search_func(answers, tex)
            await query.answer(answerss, cache_time=10)
        elif cmd == "webss":
            tex = text.split(None, 1)[1]
            answerss = await webss(tex)
            await query.answer(answerss, cache_time=2)
        elif cmd == "bitly":
            tex = text.split(None, 1)[1]
            answerss = await shortify(tex)
            await query.answer(answerss, cache_time=2)
        elif cmd == "wiki":
            if len(text.split()) < 2:
                await query.answer(
                    results=[],
                    switch_pm=(
                        "Wikipedia | wiki [QUERY]",
                        "inline",
                    ),
                )
                return
            tex = text.split(None, 1)[1].strip()
            answerss = await wiki_func(answers, tex)
            await query.answer(answerss, cache_time=2)

        elif cmd == "ping":
            answerss = await ping_func(answers)
            await query.answer(answerss, cache_time=2)
            return

        elif cmd == "yt":
            answers = []
            search_query = query.text.lower().strip().rstrip()
            if len(text.split()) > 1:
                search_query = text.split(None, 1)[1]

            if search_query == "":
                await query.answer(
                    results=[],
                    switch_pm=(
                        "Type a YouTube video name...",
                        "help",
                    ),
                    cache_time=0,
                )
            else:
                search = VideosSearch(search_query, limit=50)

                for result in search.result()["result"]:
                    answers.append(
                        query.builder.article(
                            title=result["title"],
                            description="{}, {} views.".format(
                                result["duration"],
                                result["viewCount"]["short"]),
                            text="https://www.youtube.com/watch?v={}".format(
                                result["id"]),
                            thumb=result["thumbnails"][0]["url"],
                        )
                    )

                try:
                    await query.answer(answers, cache_time=0)
                except Exception:
                    await query.answer(
                        results=[],
                        cache_time=0,
                        switch_pm=(
                            "Error: Search timed out",
                            "",
                        ),
                    )

        elif cmd == "wall" or cmd == "pic":
            tex = text.split(None, 1)[1]
            answerss = await wall_func(answers, tex)
            await query.answer(answerss)

        elif cmd == "saavn":
            tex = text.split(None, 1)[1]
            answerss = await saavn_func(answers, tex)
            await query.answer(answerss)

        elif cmd == "deezer":
            tex = text.split(None, 1)[1]
            answerss = await deezer_func(answers, tex)
            await query.answer(answerss)

        elif cmd == "torrent":
            tex = text.split(None, 1)[1]
            answerss = await torrent_func(answers, tex)
            await query.answer(answerss, cache_time=10)
            
        elif cmd == "modapk":
            sgname = text.split(None, 1)[1]
            PabloEscobar = (
                f"https://an1.com/tags/MOD/?story={sgname}&do=search&subaction=search"
            )
            r = requests.get(PabloEscobar)
            results = []
            soup = BeautifulSoup(r.content, "html5lib")
            mydivs = soup.find_all("div", {"class": "search-results"})
            Pop = soup.find_all("div", {"class": "title"})
            cnte = len(mydivs)
            for cnt in range(cnte):
                sucker = mydivs[cnt]
                pH9 = sucker.find("a").contents[0]
                file_name = pH9
                pH = sucker.findAll("img")
                imme = pH[0]["src"]
                Pablo = Pop[0].a["href"]
                ro = requests.get(Pablo)
                soupe = BeautifulSoup(ro.content, "html5lib")
                myopo = soupe.find_all("div", {"class": "item"})
                capt = f"**{file_name}** \n** {myopo[0].text}**\n**{myopo[1].text}**\n**{myopo[2].text}**\n**{myopo[3].text}**"
                mydis0 = soupe.find_all("a", {"class": "get-product"})
                Lol9 = mydis0[0]
                lemk = "https://an1.com" + Lol9["href"]
                rr = requests.get(lemk)
                soup = BeautifulSoup(rr.content, "html5lib")
                script = soup.find("script", type="text/javascript")
                leek = re.search(r'href=[\'"]?([^\'" >]+)',
                                 script.text).group()
                dl_link = leek[5:]

                buttons = [
                    [Button.url("Download Link", lemk)],
                    [Button.url("Direct Download Link", dl_link)]
                ]
                results.append(
                    query.builder.photo(
                        imme,
                        title=file_name,
                        text=capt,
                        buttons=buttons,
                    )
                )

            await query.answer(results, cache_time=0)
            
        elif cmd == "reddit":
            subreddit = text.split(None, 1)[1]
            results = []
            reddit = await arq.reddit(subreddit)
            sreddit = reddit.subreddit
            title = reddit.title
            image = reddit.url
            link = reddit.postLink
            caption = f"""**Title:** `{title}`
                    Subreddit: `{sreddit}`"""
            results.append(
                query.builder.photo(
                    image,
                    title="Meme Search",
                    text=caption,
                    buttons=[[Button.url("PostLink", link)]],
                )
            )
            await query.answer(results, cache_time=0)

        elif cmd == "imdb":
            movie_name = text.split(None, 1)[1]
            results = []
            remove_space = movie_name.split(" ")
            final_name = "+".join(remove_space)
            page = requests.get("https://www.imdb.com/find?ref_=nv_sr_fn&q=" +
                                final_name + "&s=all")
            soup = BeautifulSoup(page.content, "lxml")
            odds = soup.findAll("tr", "odd")
            mov_title = odds[0].findNext("td").findNext("td").text
            mov_link = ("http://www.imdb.com/" +
                        odds[0].findNext("td").findNext("td").a["href"])
            page1 = requests.get(mov_link)
            soup = BeautifulSoup(page1.content, "lxml")
            poster = soup.find("div", "poster").img["src"] if soup.find("div", "poster") else ""
            mov_details = re.sub(r"\s+", " ", soup.find("div", "title_wrapper").findNext("div").text) if soup.find("div", "title_wrapper") else ""
            credits = soup.findAll("div", "credit_summary_item")
            director = credits[0].a.text
            if len(credits) == 1:
                writer = "Not available"
                stars = "Not available"
            elif len(credits) > 2:
                writer = credits[1].a.text
                actors = [x.text for x in credits[2].findAll("a")]
                actors.pop()
                stars = actors[0] + "," + actors[1] + "," + actors[2]
            else:
                writer = "Not available"
                actors = [x.text for x in credits[1].findAll("a")]
                actors.pop()
                stars = actors[0] + "," + actors[1] + "," + actors[2]
            story_line = soup.find("div", "inline canwrap").findAll("p")[0].text if soup.find("div", "inline canwrap") else "Not available"
            
            mov_country, mov_language = [], []
            info = soup.findAll("div", "txt-block")
            if info:
                for node in info:
                    for i in node.findAll("a"):
                        if "country_of_origin" in i["href"]:
                            mov_country.append(i.text)
                        elif "primary_language" in i["href"]:
                            mov_language.append(i.text)
                            
            mov_rating = r.strong["title"] if (r := soup.findAll("div", "ratingValue")) else "Not available"
            lol = f"Movie - {mov_title}\n Click to see more"
            msg = ("<a href=" + poster + ">&#8203;</a>"
                   "<b>Title : </b><code>" + mov_title + "</code>\n<code>" +
                   mov_details + "</code>\n<b>Rating : </b><code>" +
                   mov_rating + "</code>\n<b>Country : </b><code>" +
                   (mov_country[0] if mov_country else "") + "</code>\n<b>Language : </b><code>" +
                   (mov_language[0] if mov_language else "") + "</code>\n<b>Director : </b><code>" +
                   director + "</code>\n<b>Writer : </b><code>" + writer +
                   "</code>\n<b>Stars : </b><code>" + stars +
                   "</code>\n<b>IMDB Url : </b>" + mov_link +
                   "\n<b>Story Line : </b>" + story_line)
            results.append(
                query.builder.article(
                    title="Imdb Search",
                    description=lol,
                    text=msg,
                    parse_mode="html",
                )
            )
            await query.answer(results, cache_time=0)
            
        elif cmd == "spaminfo":
            cmd_arg = text.split(None, 1)[1]
            results = []
            url = f"https://api.intellivoid.net/spamprotection/v1/lookup?query={cmd_arg}"
            a = await AioHttp().get_json(url)
            response = a["success"]
            if response is True:
                date = a["results"]["last_updated"]
                stats = "**◢ Intellivoid• SpamProtection Info**:\n"
                stats += f' ➛ **Updated on**: `{datetime.fromtimestamp(date).strftime("%Y-%m-%d %I:%M:%S %p")}`\n'
                stats += f" ➛ **Chat Info**: [Link](https://telegram.dog/SpamProtectionBot/?start=00_{cmd_arg})\n"

                if a["results"]["attributes"]["is_potential_spammer"] is True:
                    stats += " ➛ **User**: `USERxSPAM`\n"
                elif a["results"]["attributes"]["is_operator"] is True:
                    stats += " ➛ **User**: `USERxOPERATOR`\n"
                elif a["results"]["attributes"]["is_agent"] is True:
                    stats += " ➛ **User**: `USERxAGENT`\n"
                elif a["results"]["attributes"]["is_whitelisted"] is True:
                    stats += " ➛ **User**: `USERxWHITELISTED`\n"

                stats += f' ➛ **Type**: `{a["results"]["entity_type"]}`\n'
                stats += f' ➛ **Language**: `{a["results"]["language_prediction"]["language"]}`\n'
                stats += f' ➛ **Language Probability**: `{a["results"]["language_prediction"]["probability"]}`\n'
                stats += "**Spam Prediction**:\n"
                stats += f' ➛ **Ham Prediction**: `{a["results"]["spam_prediction"]["ham_prediction"]}`\n'
                stats += f' ➛ **Spam Prediction**: `{a["results"]["spam_prediction"]["spam_prediction"]}`\n'
                stats += f'**Blacklisted**: `{a["results"]["attributes"]["is_blacklisted"]}`\n'
                if a["results"]["attributes"]["is_blacklisted"] is True:
                    stats += f' ➛ **Reason**: `{a["results"]["attributes"]["blacklist_reason"]}`\n'
                    stats += f' ➛ **Flag**: `{a["results"]["attributes"]["blacklist_flag"]}`\n'
                stats += f'**PTID**:\n`{a["results"]["private_telegram_id"]}`\n'
                results.append(
                    query.builder.article(
                        title="Spam Info",
                        description="Search Users spam info",
                        text=stats,
                    )
                )
                await query.answer(results, cache_time=0)
                
        elif cmd == "lyrics":
            cmd_arg = text.split(None, 1)[1]
            results = []
            song = Song.find_song(cmd_arg)
            if song and song.lyrics:
                reply = song.format()
            else:
                reply = "Couldn't find any lyrics for that song!"

            if len(reply) > 4095:
                reply = "lyrics too big, Try using /lyrics"

            results.append(
                query.builder.article(
                    title="Song Lyrics",
                    description="Click here to see lyrics",
                    text=reply,
                )
            )
            await query.answer(results, cache_time=0)
            
        elif cmd == "pokedex":
            if len(text.split()) < 2:
                await query.answer(
                    results=[],
                    switch_pm=(
                        "Pokemon [text]",
                        "pokedex",
                    ),
                )
                return
            pokedex = text.split(None, 1)[1].strip()
            Pokedex = await pokedexinfo(answers, pokedex)
            await query.answer(Pokedex, cache_time=2)
            
        elif cmd == "paste":
            tex = text.split(None, 1)[1]
            answerss = await paste_func(answers, tex)
            await query.answer(answerss, cache_time=2)

        elif cmd == "covid":
            lel = text.split(None, 1)[1]
            results = []
            country = lel.replace(" ", "")
            data = await fetch(
                f"https://corona.lmao.ninja/v2/countries/{country}")
            data = await json_prettify(data)
            results.append(
                query.builder.article(
                    title="Covid Info Gathered succesfully",
                    description=data,
                    text=data,
                )
            )
            await query.answer(results, cache_time=2)
            
        elif cmd == "country":
            lel = text.split(None, 1)[1]
            results = []
            country = CountryInfo(lel)
            try:
                a = country.info()
            except:
                a = {}
            name = a.get("name", "Unknown")
            bb = a.get("altSpellings", [])
            hu = ", ".join(bb)

            area = a.get("area", "")
            hell = a.get("borders", [])
            borders = ", ".join(hell)

            call = " ".join(a.get("callingCodes", []))
            capital = a.get("capital", "")
            currencies = ", ".join(a.get("currencies", []))

            HmM = a.get("demonym", "")
            geo = a.get("geoJSON", {})
            pablo = geo.get("features", [{}])
            EsCoBaR = pablo[0].get("geometry", {}).get("type", "") if pablo else ""
            iSo = a.get("ISO", {})
            iso = ", ".join([v for v in iSo.values()])

            lMAO = ", ".join(a.get("languages", []))
            nonive = a.get("nativeName", "")
            waste = a.get("population", "")
            reg = a.get("region", "")
            sub = a.get("subregion", "")
            tom = ", ".join(a.get("timezones", []))
            lanester = ", ".join(a.get("tld", []))
            wiki = a.get("wiki", "")

            caption = f"""<b><u>Information Gathered Successfully</b></u>
                <b>
                Country Name:- {name}
                Alternative Spellings:- {hu}
                Country Area:- {area} square kilometers
                Borders:- {borders}
                Calling Codes:- {call}
                Country's Capital:- {capital}
                Country's currency:- {currencies}
                Demonym:- {HmM}
                Country Type:- {EsCoBaR}
                ISO Names:- {iso}
                Languages:- {lMAO}
                Native Name:- {nonive}
                population:- {waste}
                Region:- {reg}
                Sub Region:- {sub}
                Time Zones:- {tom}
                Top Level Domain:- {lanester}
                wikipedia:- {wiki}</b>
                Gathered By @RajniiRobot.</b>
                """
            results.append(
                query.builder.article(
                    title=f"Infomation of {name}",
                    description=f"Country Name:- {name}\nCapital:- {capital}\nTouch for more info",
                    text=caption,
                    parse_mode="html",
                )
            )
            await query.answer(results, cache_time=2)

        elif cmd == "fakegen":
            results = []
            fake = Faker()
            name = str(fake.name())
            fake.add_provider(internet)
            address = str(fake.address())
            ip = fake.ipv4_private()
            cc = fake.credit_card_full()
            email = fake.ascii_free_email()
            job = fake.job()
            android = fake.android_platform_token()
            pc = fake.chrome()
            res = f"<b><u> Fake Information Generated</b></u>\n<b>Name :-</b><code>{name}</code>\n\n<b>Address:-</b><code>{address}</code>\n\n<b>IP ADDRESS:-</b><code>{ip}</code>\n\n<b>credit card:-</b><code>{cc}</code>\n\n<b>Email Id:-</b><code>{email}</code>\n\n<b>Job:-</b><code>{job}</code>\n\n<b>android user agent:-</b><code>{android}</code>\n\n<b>Pc user agent:-</b><code>{pc}</code>"
            results.append(
                query.builder.article(
                    title="Fake infomation gathered",
                    description="Click here to see them",
                    text=res,
                    parse_mode="html",
                )
            )
            await query.answer(results, cache_time=0)

        elif cmd == "cs":
            results = []
            score_page = "http://static.cricinfo.com/rss/livescores.xml"
            page = urllib.request.urlopen(score_page)
            soup = BeautifulSoup(page, "html.parser")
            result = soup.find_all("description")
            Sed = "".join([match.get_text() + "\n\n" for match in result])
            res = f"<b><u>Match information gathered successful</b></u>\n\n\n<code>{Sed}</code>"
            results.append(
                query.builder.article(
                    title="Match information gathered",
                    description="Click here to see them",
                    text=res,
                    parse_mode="html",
                )
            )
            await query.answer(results, cache_time=0)

        elif cmd in ("antonyms", "synonyms", "define"):
            results = []
            lel = text.split(None, 1)[1]
            if cmd == "antonyms":
                let = dictionary.antonym(lel)
            elif cmd == "synonyms":
                let = dictionary.synonym(lel)
            else:
                let = dictionary.meaning(lel)
            got = str(let).replace("{", "").replace("}", "").replace("'", "")
            results.append(
                query.builder.article(
                    title=f"{cmd.capitalize()} for {lel}",
                    description=got,
                    text=got,
                )
            )
            await query.answer(results, cache_time=0)

        elif cmd == "weather":
            results = []
            sample_url = "https://api.openweathermap.org/data/2.5/weather?q={}&APPID={}&units=metric"
            input_str = text.split(None, 1)[1]
            async with aiohttp.ClientSession() as session:
                async with session.get(sample_url.format(input_str, OPENWEATHERMAP_ID)) as resp:
                    response_api = await resp.json()
            if response_api.get("cod") == 200:
                country_code = response_api["sys"]["country"]
                country_time_zone = int(response_api["timezone"])
                sun_rise_time = int(response_api["sys"]["sunrise"]) + country_time_zone
                sun_set_time = int(response_api["sys"]["sunset"]) + country_time_zone
                lol = """ 
                WEATHER INFO GATHERED
                Location: {}
                Temperature ☀️: {}°С
                Humidity 🌤: {}%
                Wind 💨: {}m/s
                Clouds ☁️: {}hpa
                Sunrise 🌤: {} {}
                Sunset 🌝: {} {}""".format(
                    input_str,
                    response_api["main"]["temp"],
                    response_api["main"]["humidity"],
                    response_api["wind"]["speed"],
                    response_api["clouds"]["all"],
                    time.strftime("%Y-%m-%d %H:%M:%S", time.gmtime(sun_rise_time)),
                    country_code,
                    time.strftime("%Y-%m-%d %H:%M:%S", time.gmtime(sun_set_time)),
                    country_code,
                )
                results.append(
                    query.builder.article(
                        title="Weather Information",
                        description=lol,
                        text=lol,
                    )
                )
                await query.answer(results, cache_time=0)

        elif cmd == "datetime":
            results = []
            gay = text.split(None, 1)[1]
            query_timezone = gay.lower()
            if len(query_timezone) == 2:
                result = generate_time(query_timezone, ["countryCode"])
            else:
                result = generate_time(query_timezone, ["zoneName", "countryName"])

            if not result:
                result = f"Timezone info not available for <b>{gay}</b>"

            results.append(
                query.builder.article(
                    title=f"Date & Time info of {gay}",
                    description=result,
                    text=result,
                    parse_mode="html",
                )
            )
            await query.answer(results, cache_time=0)

        elif cmd == "app":
            rip = []
            app_name = text.split(None, 1)[1]
            remove_space = app_name.split(" ")
            final_name = "+".join(remove_space)
            page = requests.get("https://play.google.com/store/search?q=" + final_name + "&c=apps")
            soup = BeautifulSoup(page.content, "lxml", from_encoding="utf-8")
            results = soup.findAll("div", "ZmHEEd")
            if results:
                app_name_str = results[0].findNext("div", "Vpfmgd").findNext("div", "WsMG1c nnK0zc").text
                app_dev = results[0].findNext("div", "Vpfmgd").findNext("div", "KoLSrc").text
                app_dev_link = "https://play.google.com" + results[0].findNext("div", "Vpfmgd").findNext("a", "mnKHRc")["href"]
                app_rating = results[0].findNext("div", "Vpfmgd").findNext("div", "pf5lIe").find("div")["aria-label"]
                app_link = "https://play.google.com" + results[0].findNext("div", "Vpfmgd").findNext("div", "vU6FJ p63iDd").a["href"]
                app_icon = results[0].findNext("div", "Vpfmgd").findNext("div", "uzcko").img["data-src"]
                
                app_details = "<a href='" + app_icon + "'>📲&#8203;</a>"
                app_details += " <b>" + app_name_str + "</b>"
                app_details += ("\n\n<code>Developer :</code> <a href='" + app_dev_link + "'>" + app_dev + "</a>")
                app_details += "\n<code>Rating :</code> " + app_rating.replace("Rated ", "⭐ ").replace(" out of ", "/").replace(" stars", "", 1).replace(" stars", "⭐ ").replace("five", "5")
                app_details += ("\n<code>Features :</code> <a href='" + app_link + "'>View in Play Store</a>")
                app_details += f"\n\n===> @{SUPPORT_CHAT} <==="
                
                rip.append(
                    query.builder.article(
                        title=f"Details of {app_name_str}",
                        description=app_details,
                        text=app_details,
                        parse_mode="html",
                    )
                )
            await query.answer(rip, cache_time=0)

        elif cmd in ("gh", "so"):
            results = []
            gett = text.split(None, 1)[1]
            site_query = ' "site:github.com"' if cmd == "gh" else ' "site:stackoverflow.com"'
            gresults = await GoogleSearch().async_search(gett + site_query, 1)
            result = ""
            title = ""
            for i in range(4):
                try:
                    title = gresults["titles"][i].replace("\n", " ")
                    source = gresults["links"][i]
                    description = gresults["descriptions"][i]
                    result += f"[{title}]({source})\n"
                    result += f"`{description}`\n\n"
                except IndexError:
                    pass
            results.append(
                query.builder.article(
                    title=f"Results for {gett}",
                    description=f"Info search\nTouch to read",
                    text=result,
                )
            )
            await query.answer(results, cache_time=0)

    except (IndexError, TypeError, KeyError, ValueError):
        return


def generate_time(to_find: str, findtype: List[str]) -> str:
    data = requests.get(
        f"http://api.timezonedb.com/v2.1/list-time-zone"
        f"?key={TIME_API_KEY}"
        f"&format=json"
        f"&fields=countryCode,countryName,zoneName,gmtOffset,timestamp,dst"
    ).json()

    for zone in data.get("zones", []):
        for eachtype in findtype:
            if to_find in zone.get(eachtype, "").lower():
                country_name = zone["countryName"]
                country_zone = zone["zoneName"]
                country_code = zone["countryCode"]

                daylight_saving = "Yes" if zone["dst"] == 1 else "No"

                date_fmt = r"%d-%m-%Y"
                time_fmt = r"%H:%M:%S"
                day_fmt = r"%A"
                gmt_offset = zone["gmtOffset"]
                timestamp = datetime.now(
                    datetime.timezone.utc) + datetime.timedelta(
                        seconds=gmt_offset)
                current_date = timestamp.strftime(date_fmt)
                current_time = timestamp.strftime(time_fmt)
                current_day = timestamp.strftime(day_fmt)
                break
        else:
            continue
        break

    try:
        result = (f" DATE AND TIME OF COUNTRY\n"
                  f"🌍 Country : {country_name}\n"
                  f"⏳ Zone Name : {country_zone}\n"
                  f"🗺 Country Code: {country_code}\n"
                  f"🌞 Daylight saving : {daylight_saving}\n"
                  f"🌅 Day : {current_day}\n"
                  f"⌚ Current Time : {current_time}\n"
                  f"📆 Current Date : {current_date}")
    except BaseException:
        result = None

    return result