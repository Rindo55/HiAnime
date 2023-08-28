from pyrogram import Client, idle, filters, enums
import time
from SafoneAPI import SafoneAPI
import os
import asyncio
from html_telegraph_poster.upload_images import upload_image
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery, InputMediaPhoto
from jikanpy import Jikan
import signal
from io import BytesIO
import sys
import random
import base64
import aiohttp
import requests
from html_telegraph_poster import TelegraphPoster
api_id = 3845818
api_hash = "95937bcf6bc0938f263fc7ad96959c6d"
bot_token = "6428443845:AAF9usGZRMRPPMuOfcjClNypt3N_p2_gUZc"
app = Client("anime_bot", api_id=api_id, api_hash=api_hash, bot_token=bot_token)

async def timeout_message(chat_id):
    await asyncio.sleep(300)
    await app.send_message(chat_id, "Beep Boop! 5 minutes up, no response has been received. Your appeal has timed out. If you'd like to submit the appeal, please click [here](https://t.me/aniwatchappealbot?start=appeal).")

async def timeoutz_message(chat_id):
    await asyncio.sleep(500)
    await app.send_message(chat_id, "Beep Boop! 5 minutes up, no response has been received. Your appeal has timed out. If you'd like to submit the appeal, please click [here](https://t.me/aniwatchappealbot?start=appeal).")
@app.on_message(filters.command('start'))
def start(bot, update):
    user_id = update.from_user.id
    user_states[user_id] = 'waiting_name'
    bot.send_message(user_id, "Hi! Please send me your name.")

# Define a function to handle user messages
@app.on_message(filters.text)
def handle_message(bot, update):
    user_id = update.from_user.id
    if user_id in user_states:
        state = user_states[user_id]

        if state == 'waiting_name':
            bot.send_message(user_id, "You got a good name.")
            user_states[user_id] = 'waiting_dob'
            bot.send_message(user_id, "Now, please send me your date of birth (DOB).")

        elif state == 'waiting_dob':
            bot.send_message(user_id, "Good!")
 
@app.on_message(filters.regex("fd") & filters.private)
async def handle_message(client, message):
    user=message.from_user
    user=user.id
    profile = await app.send_message(message.chat.id, text="Reply to this message with your profile link.")
    if message.reply_to_message.text == "Reply to this message with your profile link.":
        app.send_message(
            chat_id=message.chat.id,
            text="**Reply to this message with date of your punishment.**"
        )
    elif message.reply_to_message.text == "Reply to this message with date of your punishment.":
        name = message.text
        app.send_message(
            chat_id=message.chat.id,
            text="**Reply to this message with your appeal.\n`[Warning]: This question has a lower limit of 301 characters. Any answer that won't fall within the accepted number of characters will be ignored.**"
        )
    elif message.reply_to_message.text == "**Reply to this message with your appeal.\n`[Warning]: This question has a lower limit of 301 characters. Any answer that won't fall within the accepted number of characters will be ignored.**":
        name = message.text
        app.send_message(
            chat_id=message.chat.id,
            text="**Your appeal had been received and is now under review."
        )
    else:
        pass
def get_anime_info(anime_title):
    url = f"https://api.jikan.moe/v4/anime?q={anime_title}"
    response = requests.get(url)
    data = response.json()

    if data and "data" in data and len(data["data"]) > 0:
        anime = data["data"][0]
        anime_info = f"**Title: {anime['title']}**\n"
        anime_info += f"- Type: {anime['type']}\n\n"
        anime_info += f"- Score: {anime['score']}\n\n"
        anime_info += f"- Episodes: {anime['episodes']}\n\n"
        anime_info += f"- Status: {anime['status']}\n\n"
    
        air = [aire['from'] and aire['to'] for aire in anime['aired']]
        aired = air.replace("T00:00:00+00:00", "")
        anime_info += f"Aired: {', '.join(aire)}\n\n"
        
        
        anime_info += f"- Premiered: {anime['season']} {anime['year']} \n\n"
        
        producers = [producer['name'] for producer in anime['producers']]
        anime_info += f"- Producers: {', '.join(producers)}\n\n"
        licensors = [licensor['name'] for licensor in anime['licensors']]
        anime_info += f"Licensors: {', '.join(licensors)}\n\n"
        studios = [studio['name'] for studio in anime['studios']]
        anime_info += f"Studio: {', '.join(studios)}\n\n"        
        anime_info += f"- Source: {anime['source']}\n\n"
        themes = [theme['name'] for theme in anime['themes']]
        anime_info += f"Themes: {', '.join(themes)}\n"
        anime_info += f"- Duration: {anime['duration']}\n\n"
        anime_info += f"- Rating: {anime['rating']}\n\n"



        return anime_info
    else:
        return "Anime not found."

@app.on_message(filters.command("anime"))
def handle_message(client, message):
    anime_title = " ".join(message.command[1:])
    anime_info = get_anime_info(anime_title)
    client.send_message(message.chat.id, anime_info)

ANIME_QUERY = """
query ($id: Int, $idMal:Int, $search: String) {
  Media (id: $id, idMal: $idMal, search: $search, type: ANIME) {
    id
    idMal
    title {
      romaji
      english
      native
    }
    format
    status
    episodes
    duration
    countryOfOrigin
    source (version: 2)
    trailer {
      id
      site
    }
    genres
    tags {
      name
    }
    studios {
    nodes {
        name
    }
    }
    averageScore
    relations {
      edges {
        node {
          title {
            romaji
            english
          }
          id
        }
        relationType
      }
    }
    nextAiringEpisode {
      timeUntilAiring
      episode
    }
    isAdult
    isFavourite
    mediaListEntry {
      status
      score
      id
    }
    siteUrl
  }
}
"""
ANIME_DB = {}

async def return_json_senpai(query: str, vars_: dict):
    url = "https://graphql.anilist.co"
    anime = vars_["search"]
    db = ANIME_DB.get(anime)

    if db:
      return db
    data = requests.post(url, json={"query": query, "variables": vars_}).json()
    ANIME_DB[anime] = data

    return data

temp = []

async def get_anime(vars_,less):
    if 1 == 1:
        result = await return_json_senpai(ANIME_QUERY, vars_)

        error = result.get("errors")
        if error:
            error_sts = error[0].get("message")
            print([f"[{error_sts}]"])
            print(vars_)
            data = temp[0]
            temp.pop(0)
        else:
          data = result["data"]["Media"]   
          temp.append(data)
        idm = data.get("id")
        title = data.get("title")
        tit = title.get("english")
        if tit == None:
            tit = title.get("romaji")

        title_img = f"https://img.anili.st/media/{idm}"
        
        if less == True:
          return idm, title_img, tit

        return data
def synopsis_desu(synopsis):
    
    # Initialize TelegraphPoster
    client = TelegraphPoster(use_api=True)
    client.create_api_token("golumpa")
    
    # Get the first name and username of the bot
    
    # Create a telegraph page
    page = client.post(
        title="Synopsis",
        author="MAL",
        author_url="https://myanimelist.net",
        text=out,
    )
    return page["url"]

async def info(title):
    process = subprocess.Popen(
        ["mediainfo", file, "--Output=HTML"],
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
    )
    stdout, stderr = process.communicate()
    out = stdout.decode()
    client = TelegraphPoster(use_api=True)
    client.create_api_token("synpsis")
    page = client.post(
        title="Synopsis",
        author="Natsu",
        author_url=f"https://t.me/animearchivex",
        text=synopsi,
    )
    return page["url"]
async def get_anime_img(query):
    vars_ = {"search": query}
    idm, title_img, title = await get_anime(vars_,less=True)

    #title = format_text(title)
    return idm, title_img, title
    
def get_anime_name(title):
    x = title.split(" - ")[-1]
    title = title.replace(x,"").strip()
    title = title[:-2].strip()

    x = title.split(" ")[-1].strip()
    if str(x[-1]) in digits and str(x[0]) == "S" and str(x[1]) in digits:
      if "S" in x:
        y = x.replace("S","S")
        title = title.replace(x,y)
    return title

atext = """
📺 **{}**
      **({})**
━━━━━━━━━━━━━━━━━━━━━━
- Type: {}

- Score: 🌟{}

- Episodes: {}

- Status: {}

- Aired: {}

- Premiered: {}

- Producers: {}

- Licensors: {}

- Studio: {}

- Source: {}

- Genre: #{}

- Theme: {}

- Duration: {} mins/Ep

- Rating: {}

- Tags: {}

- Rank: {} | Popularity: {}
"""
async def get_anilist_data(title):
    malurl = f"https://api.jikan.moe/v4/anime?q={title}"
    malresponse = requests.get(malurl)
    maldata = malresponse.json()
    vars_ = {"search": title}
    data = await get_anime(vars_,less=False)
    id_ = data.get("id")
    title = data.get("title")
    form = data.get("format")
    source = data.get("source")
    status = data.get("status")
    episodes = data.get("episodes")
    duration = data.get("duration")
    trailer = data.get("trailer")
    genres = data.get("genres")
    averageScore = data.get("averageScore")
    img = f"https://img.anili.st/media/{id_}"

    # title
    title1 = title.get("english")
    title2 = title.get("romaji")

    if title2 == None:
      title2 = title.get("native")

    if title1 == None:
      title1 = title2   

    # genre

    genre = ""

    for i in genres:
      genre += i + ", #"

    genre = genre[:-3]
    genre = genre.replace("#Slice of Life", "#Slice_of_Life")
    genre = genre.replace("#Mahou Shoujo", "#Mahou_Shoujo")    
    genre = genre.replace("#Sci-Fi", "#SciFi")
    studiox = data['studios']['nodes'][0]['name']
    tags = []
    for i in data['tags']:
        tags.append(i["name"])
    tagsx = "#" + f"{', #'.join(tags)}"
    tagsx = tagsx.replace("#Age Gap", "#Age_Gap")
    tagsx = tagsx.replace("#Anti-hero", "#Antihero")
    tagsx = tagsx.replace("#Artificial Intelligence", "#Artificial_Intelligence")
    tagsx = tagsx.replace("#Augmented Reality", "#Augmented_Reality")
    tagsx = tagsx.replace("#Battle Royale", "#Battle_Royale")
    tagsx = tagsx.replace("#Body Horror", "#Body_Horror")
    tagsx = tagsx.replace("#Boys' Love", "#Boys_Love")
    tagsx = tagsx.replace("#Card Battle", "#Card_Battle")
    tagsx = tagsx.replace("#Coming of Age", "#Coming_of_Age")
    tagsx = tagsx.replace("#Cosmic Horror", "#Cosmic_Horror")
    tagsx = tagsx.replace("#Cute Boys Doing Cute Things", "#Cute_Boys_Doing_Cute_Things")
    tagsx = tagsx.replace("#Cute Girls Doing Cute Things", "#Cute_Girls_Doing_Cute_Things")
    tagsx = tagsx.replace("#Ensemble Cast", "#Ensemble_Cast")
    tagsx = tagsx.replace("#Fairy Tale", "#Fairy_Tale")
    tagsx = tagsx.replace("#Family Life", "#Family_Life")
    tagsx = tagsx.replace("#Female Harem", "#Female_Harem")
    tagsx = tagsx.replace("#Female Protagonist", "#Female_Protagonist")
    tagsx = tagsx.replace("#Full CGI", "#Full_CGI")
    tagsx = tagsx.replace("#Full Color", "#Full_Color")
    tagsx = tagsx.replace("#Found Family", "#Found_Family")
    tagsx = tagsx.replace("#Gender Bending", "#Gender_Bending")
    tagsx = tagsx.replace("#Ice Skating", "#Ice_Skating")
    tagsx = tagsx.replace("#Language Barrier", "#Language_Barrier")
    tagsx = tagsx.replace("#Lost Civilization", "#LostCivilization")
    tagsx = tagsx.replace("#Love Triangle", "#Love_Triangle")
    tagsx = tagsx.replace("#Male Protagonist", "#Male_Protagonist")
    tagsx = tagsx.replace("#Martial Arts", "#Martial_Arts")
    tagsx = tagsx.replace("#Memory Manipulation", "#Memory_Manipulation")
    tagsx = tagsx.replace("#Monster Boy", "#Monster_Boy")
    tagsx = tagsx.replace("#Monster Girl", "#Monster_Girl")
    tagsx = tagsx.replace("#Non-fiction", "#Nonfiction")
    tagsx = tagsx.replace("#Office Lady", "#Office_Lady")
    tagsx = tagsx.replace("#Ojou-sama", "#Ojousama")
    tagsx = tagsx.replace("#Otaku Culture", "#Otaku_Culture")
    tagsx = tagsx.replace("#Post-Apocalyptic", "#Post_Apocalyptic")
    tagsx = tagsx.replace("#Primarily Adult Cast", "#Primarily_Adult_Cast")
    tagsx = tagsx.replace("#Primarily Child Cast", "#Primarily_Child_Cast")
    tagsx = tagsx.replace("#Primarily Female Cast", "#Primarily_Female_Cast")
    tagsx = tagsx.replace("#Primarily Male Cast", "#Primarily_Male_Cast")
    tagsx = tagsx.replace("#Primarily Teen Cast", "#Primarily_Teen_Cast")
    tagsx = tagsx.replace("#School Club", "#School_Club")
    tagsx = tagsx.replace("#Real Robot", "#Real_Robot")
    tagsx = tagsx.replace("#Ero Guro", "#Ero_Guro")
    tagsx = tagsx.replace("#Software Development", "#Software_Development")
    tagsx = tagsx.replace("#Time Manipulation", "#Time_Manipulation")
    tagsx = tagsx.replace("#Surreal Comedy", "#Surreal_Comedy")
    tagsx = tagsx.replace("#Teens' Love", "#Teens_Love")
    tagsx = tagsx.replace("#Urban Fantasy", "#Urban_Fantasy")
    tagsx = tagsx.replace("#Super Power", "#Super_Power")
    tagsx = tagsx.replace("#Super Robot", "#Super_Robot")
    tagsx = tagsx.replace("#Video Games", "#Video Games")
    tagsx = tagsx.replace("#Virtual World", "#Virtual_World")
    tagsx = tagsx.replace("#Shrine Maiden", "#Shrine_Maiden")
    tagsx = tagsx.replace("#Lost Civilization", "#Lost_Civilization")
    tagsx = tagsx.replace("#Dissociative Identities", "#Dissociative_Identities")
    tagsx = tagsx.replace("#Achronological Order", "#Achronological Order")
    tagsx = tagsx.replace("#Time Skip", "#Time_Skip")
    tagsx = tagsx.replace("#Age Regression", "#Age_Regression")
    tagsx = tagsx.replace("#Human Pet", "#Human_Pet")
    tagsx = tagsx.replace("#Achronoligical Order", "#Achronoligical_Order")
    tagsx = tagsx.replace("#Family Life", "#Family_Life")
    tagsx = tagsx.replace("#Body Swapping", "#Body_Swapping")
    tagsx = tagsx.replace("#Large Breasts", "Large_Breasts")
    tagsx = tagsx.replace("#Classic Literature", "#Classic_Literature")
    tagsx = tagsx.replace("#Tanned Skin", "#Tanned_Skin")
    tagsx = tagsx.replace("#Video Games", "#Video_Games")
    tagsx = tagsx.replace("#Alternate Universe", "#Alternate_Universe")
    tagsx = tagsx.replace("#Anti-Hero", "#AntiHero")
    if data and "data" in maldata and len(maldata["data"]) > 0:
      mal = maldata["data"][0]
      producer = []
      for i in mal['producers']:
        producer.append(i["name"])
      producer = ", ".join(producer)
      licensor = []
      for i in mal['licensors']:
        licensor.append(i["name"])
      licensor = ", ".join(licensor)
      if licensor=="":
          licensor=licensor.replace("", "Unknown")
        
      theme = []
      for i in mal['themes']:
          theme.append(i["name"])
      theme = ", ".join(theme)
      season = f"{mal['season']} {mal['year']}"
      rating = mal['rating']
      aired = mal['aired']['string']
      malink = mal['url']
      malrank = mal['rank']
      malpopularity = mal['popularity']
      synopsi = mal['synopsis']
      synopsi = synopsi.replace("[Written by MAL Rewrite]", "")
    client = TelegraphPoster(use_api=True)
    client.create_api_token("synpsis")
    page = client.post(
        title=title1,
        author="MAL",
        author_url=f"https://myanimelist.net",
        text=f"<h4>Synopsis</h4>\n{synopsi}",             
    )
    syn = page["url"]
    caption = atext.format(
      title2,
      title1,
      form,
      averageScore,
      episodes,
      status,
      aired,
      season,
      producer,
      licensor,
      studiox,
      source,   
      genre,
      theme,
      duration,
      rating,
      tagsx,
      malrank,
      malpopularity,
    )


    if trailer != None:
      ytid = trailer.get("id")
      site = trailer.get("site")
    else:
      site = None

    if site == "youtube":
      caption += f"\n - [Synopsis]({syn})  |  [Trailer](https://www.youtube.com/watch?v={ytid})\n\n- More Info: [AniList](https://anilist.co/anime/{id_})  |  [MAL]({malink})\n━━━━━━━━━━━━━━━━━━━━━━\n@AnimeArchiveX"
    else:
      caption += f"\n - [Synopsis]({syn})\n\n- More Info: [AniList](https://anilist.co/anime/{id_})  |  [MAL]({malink})\n━━━━━━━━━━━━━━━━━━━━━━\n@AnimeArchiveX"

    return img, caption
                                
@app.on_message(filters.command("anilist"))
async def handle_message(client, message):
    name = " ".join(message.command[1:])
    result = await get_anilist_data(name)
    img, caption = result
    return await client.send_photo(message.chat.id,photo=img,caption=caption)
    
command_queue = asyncio.Queue()
processing = False  # Flag to indicate if a process is ongoing

@app.on_message(filters.command("imagine"))
async def handle_message(client, message):
    topy = message.reply_to_message_id
    if topy==4:
        global processing
        if processing:
            tk = await message.reply_text("Your request is in queue.")
            await command_queue.put(message)
            await asyncio.sleep(10)
            await tk.delete()
        else:
            await command_queue.put(message)
            await process_queue()

async def process_queue():
    global processing
    
    while not command_queue.empty():
        processing = True
        sam_id = -1001911678094
        next_command = await command_queue.get()
        topicy_id=4
        taku = await app.send_message(
            chat_id=sam_id,
            text="Imagining...",
            reply_to_message_id=topicy_id
        )
        bing = " ".join(next_command.command[1:])
        sux = f"https://api.safone.me/imagine?text={bing}&version=3"
        responsep = requests.get(sux)
        print(responsep)
        fuk = responsep.json()

        if 'error' in fuk:
            await app.send_message(
                chat_id=sam_id,
                text=fuk['error'],
                reply_to_message_id=topicy_id
            )
            processing = False
        else:
            pho_list = fuk['image']  # Get the list of images directly
            media_group = []
            temp_files = []  # To keep track of temporary files
            for idx, pho in enumerate(pho_list):
                sdf = ''.join(pho)
                b64dec = base64.b64decode(sdf)
                temp_filename = f"image{idx}.jpg"
                temp_files.append(temp_filename)
                with open(temp_filename, 'wb') as file:
                    file.write(b64dec)
                media_group.append(InputMediaPhoto(media=temp_filename, caption=f"image {idx + 1}"))
            await app.send_media_group(
                chat_id=sam_id,
                media=media_group,
                reply_to_message_id=topicy_id
            )
            for temp_file in temp_files:
                os.remove(temp_file)
            await taku.delete()
            processing = False

@app.on_message(filters.private)
async def handle_private_message(client, message):
    await process_queue()
            
@app.on_message(filters.chat(-1001911678094))
async def handle_message(client, message):
    user = message.from_user
    userid = user.id
    topz = message.reply_to_message_id
    KAYO_ID=-1001911678094
    if topz==3:
        topic_id=topz
        ta = await app.send_message(
            chat_id=KAYO_ID,
            text="Typing...",
            reply_to_message_id=topic_id
        )
        API_URLX = "https://api.safone.me/bard"
        payloadx = {
            "message": message.text,
        }
        headersx = {
            "accept": "application/json",
            "Content-Type": "application/json"
        }
        responsex = requests.post(API_URLX, json=payloadx, headers=headersx)
        if responsex.status_code == 200:
            datax = responsex.json()
            if "choices" in datax and len(datax["choices"]) > 0:
                assistant_responsex = datax["choices"][0]["content"][0]
                print("Assistant:", assistant_responsex)
            else:
                print("No response from assistant.")
        else:
            print("Error:", responsex.status_code)

        await ta.edit(assistant_responsex)
    elif topz==2:
        topi_id=topz
        tak = await app.send_message(
            chat_id=KAYO_ID,
            text="Typing...",
            reply_to_message_id=topi_id
        )
        API_URLz = "https://api.safone.me/chatgpt"
        boom = message.text
        payloadz = {
            "message": boom,
            "version": 3,
            "chat_mode": "assistant",
            "dialog_messages": f'[{{"bot":"","user":"{userid}"}}]'
        }
        headersz = {
            "accept": "application/json",
            "Content-Type": "application/json"
        }
        responsez = requests.post(API_URLz, json=payloadz, headers=headersz)
        if responsez.status_code == 200:
            dataz = responsez.json()
            if "choices" in dataz and len(dataz["choices"]) > 0:
                assistant_responsez = dataz["choices"][0]["message"]["content"]
                print("Assistant:", assistant_responsez)
            else:
                print("No response from assistant.")
        else:
            print("Error:", responsez.status_code)
        topicz_id=topz
        await tak.edit(assistant_responsez)
    else:
        pass 
        


    
    


async def get_anime_info(anime_name):
    query = '''
    query ($anime_name: String) {
        Media (search: $anime_name, type: ANIME) {
            title {
                romaji
                english
            }
            type
            averageScore
            source
            duration
            episodes
            genres
            tags {
                name
            }
            status
            studios {
                nodes {
                    name
                }
            }
            startDate {
                year
                month
                day
            }
            endDate {
                year
                month
                day
            }
            licensors {
                nodes {
                    name
                }
            }
            season
            producers {
                nodes {
                    name
                }
            }
        }
    }
    '''

    variables = {
        "anime_name": anime_name
    }
    ANILIST_API = "https://graphql.anilist.co"
    response = requests.post(ANILIST_API, json={"query": query, "variables": variables})
    data = response.json()

    return data["data"]["Media"]


# Handler for /anime command
@app.on_message(filters.command("ani"))
async def anime_command_handler(client, message):
    # Get the anime name from the command arguments
    title = " ".join(message.command[1:])

    # Get anime info from AniList
    img, caption = await get_anilist_data(title)
    main = await app.reply_photo(photo=img,caption=caption)

    # Format the anime info into a string
    info_string = f"Title: {anime_info['title']['romaji']}\n"
    info_string += f"English Title: {anime_info['title']['english']}\n"
    info_string += f"Type: {anime_info['type']}\n"
    info_string += f"Score: {anime_info['averageScore']}\n"
    info_string += f"Source: {anime_info['source']}\n"
    info_string += f"Duration: {anime_info['duration']}\n"
    info_string += f"Episodes: {anime_info['episodes']}\n"
    info_string += f"Genres: {', '.join(anime_info['genres'])}\n"
    info_string += f"Tags: {', '.join(tag['name'] for tag in anime_info['tags'])}\n"
    info_string += f"Status: {anime_info['status']}\n"
    info_string += f"Studio: {anime_info['studios']['nodes'][0]['name']}\n"
    info_string += f"Start Date: {anime_info['startDate']['year']}-{anime_info['startDate']['month']}-{anime_info['startDate']['day']}\n"
    info_string += f"End Date: {anime_info['endDate']['year']}-{anime_info['endDate']['month']}-{anime_info['endDate']['day']}\n"
    info_string += f"Licensors: {', '.join(licensor['name'] for licensor in anime_info['licensors']['nodes'])}\n"
    info_string += f"Season: {anime_info['season']}\n"
    info_string += f"Producers: {', '.join(producer['name'] for producer in anime_info['producers']['nodes'])}\n"

    # Send the anime info as a reply

app.start()
print("Powered by @animxt")
idle()

