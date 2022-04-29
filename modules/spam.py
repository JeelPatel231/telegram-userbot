def spam(client,message):
    chat_id = message.chat.id
    try:
        text = message.text.split(" ",1)[1] # .spam (count text)
        count = int(text.split(" ",1)[0]) # count
    except IndexError:
        message.reply_text("spam text where at?", quote=True);return
    except ValueError:
        message.reply_text("format error", quote=True);return

    if message.reply_to_message is not None:
        text = message.reply_to_message.text
    elif len(text.split(" ")) == 2:
        text = text.split(" ")[1] # text
    else:
        message.reply_text("wrong format, usage : .spam -count- spam",quote=True)
        return
    for _ in range(count):
        client.send_message(chat_id,text)

help = "`Spam messages consecutively for a given count`"