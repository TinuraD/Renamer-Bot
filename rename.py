"""
MIT License

Copyright (c) 2022 Tinura Dinith

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
"""

from os import getenv, path, remove, rename
from pyrogram import Client, filters, enums
from pyrogram.types import Message

bot = Client("Renamerbot", 
                bot_token=getenv("BOT_TOKEN"), 
                api_id=getenv("API_ID"), 
                api_hash=getenv("API_HASH"))

@bot.on_message(filters.command(["start","help"]))
async def startmsg(_, msg):
    await msg.reply_text("""
Hello, I'm renamer bot 👋
I can rename any file with custom thumbnail support.

- `/rename` - Reply to file to rename it.
- Sent image to use as custom thumbnail.
- `/delthumb` - Delete custom thumbnail.
- `/showthumb` - To view current thumbnail.
    
**__Bot by Tinura Dinith__**    
    """, quote=False)

@bot.on_message(filters.photo)
async def savethumb(_, msg):
    location = f"./thumbs/{msg.from_user.id}.jpg"
    if path.exists(location): remove(location)
    await bot.download_media(
        message=msg, file_name=location)
    await msg.reply_text("Thumbnail saved successfully ✅")    

@bot.on_message(filters.command("delthumb"))
async def deletethumb(_, msg):
    location = f"./thumbs/{msg.from_user.id}.jpg"
    if path.exists(location): 
        remove(location)
        await msg.reply_text("Thumbnail deleted successfully ✅")
    else : await msg.reply_text("You haven't set thumbnails yet. ❌")

@bot.on_message(filters.command("showthumb"))
async def showthumb(_, msg):
    location = f"./thumbs/{msg.from_user.id}.jpg"
    if path.exists(location): await msg.reply_photo(location, caption="Here is your thumbnail.")
    else : await msg.reply_text("You haven't set thumbnails yet. ❌")  

@bot.on_message(filters.command("rename"))
async def rename(_, msg:Message):
    location = f"./media/{msg.from_user.id}/"
    if not msg.reply_to_message : return await msg.reply_text("Please reply to a file to change thumbnail.")
    if msg.reply_to_message and not msg.reply_to_message.document:
        return await msg.reply_text("Please reply to a document type file to change thumbnail.")
    await bot.download_media(msg.reply_to_message, location)
    mg = await msg.reply_text("Downloading...")
    filename = msg.reply_to_message.document.file_name
    gettheext = filename.split(".")
    file_ext=(gettheext[-1])
    if len(msg.command) < 2:
        newname = filename
    if len(msg.command) > 1:
        newname = msg.text.split(None, 1)[1]+"."+file_ext
        rename(location+filename, location+newname)
    await mg.edit("Uploading...")
    await bot.send_chat_action(msg.chat.id, enums.ChatAction.UPLOAD_DOCUMENT)
    if path.exists(f"./thumbs/{msg.from_user.id}.jpg"):
        await msg.reply_document(location+newname, thumb=f"./thumbs/{msg.from_user.id}.jpg")
    else:
        await msg.reply_document(location+newname)   
    await mg.delete()
    await bot.send_chat_action(msg.chat.id, enums.ChatAction.CANCEL)    
    if path.exists(location+newname):remove(location+newname)           
        
print("Bot started")
bot.run()        
