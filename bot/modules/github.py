import os
from requests import get
from pyrogram import filters
from bot import app, dispatcher



@app.on_message(filters.command(['github']))
def git(_,message):
    replied = message.reply_to_message
    username = message.filtered_input_str
    if replied:
        username = message.text.split(' ')[1]
        return
    url = "https://api.github.com/users/{}".format(username)
    res = requests.get(url)
    if res.status_code == 200:
     await message.reply_text("`fetching github info ...`")
        data = res.json()
        photo = data["avatar_url"]
        if data['bio']:
            data['bio'] = data['bio'].strip()
        repos = []
        sec_res = requests.get(data["repos_url"])
        if sec_res.status_code == 200:
            limit = int(message.flags.get('-l', 5))
            for repo in sec_res.json():
                repos.append(f"[{repo['name']}]({repo['html_url']})")
                limit -= 1
                if limit == 0:
                    break
        template = """
\b👤 **Name** : [{name}]({html_url})
🔧 **Type** : `{type}`
🏢 **Company** : `{company}`
🔭 **Blog** : {blog}
📍 **Location** : `{location}`
📝 **Bio** : __{bio}__
❤️ **Followers** : `{followers}`
👁 **Following** : `{following}`
📊 **Public Repos** : `{public_repos}`
📄 **Public Gists** : `{public_gists}`
🔗 **Profile Created** : `{created_at}`
✏️ **Profile Updated** : `{updated_at}`\n""".format(**data)
        if repos:
            template += "🔍 **Some Repos** : " + ' | '.join(repos)
        await message.reply_photo(chat_id=message.chat.id,
                                        caption=template,
                                        photo=photo,
                                        disable_notification=True)
        await message.delete()
      else:
        await message.reply_text(f"No user found")
    
