from telegram import ParseMode, Update, Bot
from telegram.ext import CallbackContext, CommandHandler
from bot import dispatcher
from requests import get




def github(bot: Bot, update: Update, context: CallbackContext):
    message = update.effective_message
    text = message.text[len('/git '):]
    usr = get(f'https://api.github.com/users/{text}').json()
    if usr.get('login'):
        reply_text = f"""*Name:* `{usr['name']}`
*👨‍💼Username:* `{usr['login']}`
*🔖Account ID:* `{usr['id']}`
*📝Account type:* `{usr['type']}`
*📍Location:* `{usr['location']}`
*✍️Bio:* `{usr['bio']}`
*➡️Followers:* `{usr['followers']}`
*⬅️Following:* `{usr['following']}`
*🌚Hireable:* `{usr['hireable']}`
*⛵️Public Repos:* `{usr['public_repos']}`
*🚁Public Gists:* `{usr['public_gists']}`
*📨Email:* `{usr['email']}`
*🏢Company:* `{usr['company']}`
*🌍Website:* `{usr['blog']}`
*♻️Last updated:* `{usr['updated_at']}`
*📒Account created at:* `{usr['created_at']}`
"""
    else:
        reply_text = "User not found. Make sure you entered valid username!"
    message.reply_text(reply_text, parse_mode=ParseMode.MARKDOWN)



def repo(bot: Bot, update: Update):
    message = update.effective_message
    text = message.text[len('/repo '):]
    usr = get(f'https://api.github.com/users/{text}/repos?per_page=40').json()
    reply_text = "*Repo*\n"
    for i in range(len(usr)):
        reply_text += f"[{usr[i]['name']}]({usr[i]['html_url']})\n"
    message.reply_text(reply_text, parse_mode=ParseMode.MARKDOWN, disable_web_page_preview=True)



GIT_HANDLER = CommandHandler("git", github)
REPO_HANDLER = CommandHandler("repo", repo)

dispatcher.add_handler(GIT_HANDLER)
dispatcher.add_handler(REPO_HANDLER)

















