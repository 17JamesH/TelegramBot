import json
import requests
import time
import urllib
import datetime

# Bot token used to access this bot
TOKEN = "680853535:AAGIca5YDCLScY-gx0q8eGYOAEuTjtwLorY"
# Telegram Bot API URL
URL = "https://api.telegram.org/bot{}/".format(TOKEN)


# Gets string from specified url with contents in UTF-8
def check_url(url):
    response = requests.get(url)
    content = response.content.decode("utf8")
    return content


# Returns url contents as json object
def check_url_json(url):
    content = check_url(url)
    js = json.loads(content)
    return js


# Sends a message to a Telegram chat
def send_message(text, chat_id):
    text = urllib.parse.quote_plus(text)
    url = URL + "sendMessage?text={}&chat_id={}".format(text, chat_id)
    check_url(url)


# Deletes message with id message_id
def delete_message(message_id, chat_id):
    url = URL + "deleteMessage?message_id={}&chat_id={}".format(message_id, chat_id)
    check_url(url)


# Gets Updates from Telegram API for this bot
def get_updates(offset=None):
    url = URL + "getUpdates?timeout=100"
    if offset:
        url += "&offset={}".format(offset)
    js = check_url_json(url)
    return js


# Gets the id of the most recent update
def get_last_update_id(updates):
    update_ids = []
    for update in updates["result"]:
        update_ids.append(int(update["update_id"]))
    return max(update_ids)


# Deletes all messages in an update segment muahahaha
def delete_all(updates):
    for update in updates["result"]:
        try:
            message_id = update["message"]["message_id"]
            chat = update["message"]["chat"]["id"]
            delete_message(message_id, chat)
        except Exception as e:
            print(e)


# Repeats all messages in an update segment
def echo_all(updates):
    for update in updates["result"]:
        try:
            text = update["message"]["text"]
            chat = update["message"]["chat"]["id"]
            # Hardcoded to respond only to me
            if update["message"]["from"]["id"] == 422110754:
                send_message(text, chat)
        except Exception as e:
            print(e)


# Main loop
def main():
    last_update_id = None
    while True:
        # Putting most recent updates into JSON object
        updates = get_updates(last_update_id)
        if len(updates["result"]) > 0:
            # Sets next update to check for to the one after the most recently checked
            last_update_id = get_last_update_id(updates) + 1
            # Do Action
            echo_all(updates)
            delete_all(updates)
        time.sleep(0.5)


if __name__ == '__main__':
    main()
