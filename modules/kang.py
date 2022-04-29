from pyrogram.handlers import MessageHandler

options = lambda: None
options.CHOOSE_SET = "Choose a sticker set"
options.SEND_STICKER = "Alright! Now send me the sticker"
options.SEND_ANIM_STICKER = "Alright! Now send me the animated sticker"
options.SEND_VIDEO_STICKER = "Alright! Now send me the video sticker"
options.EMOJI = "Thanks! Now send me an emoji that corresponds to your first sticker"
options.DONE = "There we go"
options.OVERFLOW = "Whoa! That's probably enough stickers for one set, give it a break"
options.PUBLISH = "Congratulations"
options.CHOOSE_NAME = "Yay! A new sticker set"
options.SET_ICON = "You can set an icon for your sticker set"
options.PROVIDE_NAME = "Please provide a short name for your set"
options.SET_PUBLISHED = "Kaboom! I've just published your sticker set"

def choose_pack(list_of_packs:list ,anim:bool = False):
    temp_list = [item for sublist in list_of_packs for item in sublist if "pronto" in item]
    # return normal webp packs and exlude anim packs
    if not anim:
        return [item for item in temp_list if "anim" not in item]
    
    # if anim is true, return this with ONLY anim packs
    return [item for item in temp_list if "anim" in item]


def kang(client,message):
    try:
        sticker_obj = message.reply_to_message.sticker
        if sticker_obj.is_animated or sticker_obj.is_video:
            message.reply_text("video/animated stickers not supported **YET**",quote=True)
            return
    except:
        message.reply_text("reply to a sticker, dumbass",quote=True)
        return
    
    split = message.text.split(" ",1)
    emojis = "" if len(split) == 1 else split[1]
    number_next = 1
    pack_name = None
    pack_name_suffix = f"a{client.get_me().id}_by_pronto_"

    client.send_message("@stickers","/addsticker")

    def react_on_message(_, bot_message):
        nonlocal number_next
        nonlocal pack_name
        nonlocal kang_handler

        if bot_message.from_user.username == "Stickers":
            match bot_message.text.split(".")[0]:
                case options.CHOOSE_SET:
                    pack_name = choose_pack(bot_message.reply_markup.keyboard)
                    if pack_name == []:
                        bot_message.reply_text("/newpack")
                    else:
                        pack_name = pack_name[-1]
                        number_next = int(pack_name.split("_")[-1])+1
                        bot_message.reply_text(pack_name)
                case options.OVERFLOW:
                    bot_message.reply_text("/newpack")
                case options.CHOOSE_NAME:
                    bot_message.reply_text(f"@{client.get_me().username}'s kang pack vol. {number_next}")
                case options.PUBLISH:
                    bot_message.reply_text("/publish")
                case options.SET_ICON:
                    bot_message.reply_text("/skip")
                case options.PROVIDE_NAME:
                    pack_name = pack_name_suffix+str(number_next)
                    bot_message.reply_text(pack_name)
                case options.SEND_STICKER:
                    bot_message.reply_sticker(sticker_obj.file_id)
                case options.SEND_ANIM_STICKER:
                    bot_message.reply_sticker(sticker_obj.file_id)
                case options.SEND_VIDEO_STICKER:
                    bot_message.reply_sticker(sticker_obj.file_id)
                case options.EMOJI:
                    bot_message.reply_text(sticker_obj.emoji+emojis)
                case options.DONE:
                    bot_message.reply_text("/done")
                    message.reply_text(f"kanged [HERE](https://t.me/addstickers/{pack_name})",quote=True)
                    client.remove_handler(*kang_handler) # remove handler after job is done
                case options.SET_PUBLISHED:
                    message.reply_text(f"kanged [HERE](https://t.me/addstickers/{pack_name})",quote=True)
                    client.remove_handler(*kang_handler) # remove handler after job is done

    kang_handler = client.add_handler(MessageHandler(react_on_message))
    # ^ add handler to react to bot sent messages

help = "`Kang stickers to your own packs, media/animated not supported yet`"