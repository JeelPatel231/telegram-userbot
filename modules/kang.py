from pyrogram.handlers import MessageHandler
from pyffmpeg import FFmpeg
import os

ffm = FFmpeg()

options = lambda: None
options.CHOOSE_SET = "Choose a sticker"
options.SEND_STICKER = "Alright! Now send"
options.EMOJI = "Thanks! Now send"
options.DONE = "There we go"
options.OVERFLOW = "Whoa! That's probably"
options.ASK_PUBLISH = "Choose the sticker"
options.PUBLISH = "Congratulations"
options.CHOOSE_NAME = "Yay! A new"
options.SET_ICON = "You can set"
options.PROVIDE_NAME = "Please provide a"
options.SET_PUBLISHED = "Kaboom! I've just"

conversion_map = {
    "tgz" : None,
    "webp" : None,
    "webm" : None,
    "png" : "webp",
    "jpg" : "webp",
    "mp4" : "webm"
}

def getFirst3Spaces(str):
    spc = 3
    lst = str.split(None,spc)[:spc]
    return " ".join(lst)

def choose_pack(list_of_packs:list ,anim:bool = False,video:bool = False):
    rep_list = [item for sublist in list_of_packs for item in sublist if "pronto" in item]
    # return animated packs
    if anim: return [item for item in rep_list if "anim" in item]
    # return video packs
    if video: return [item for item in rep_list if "video" in item]
    # return normal webp packs and exlude anim packs
    if not anim and not video:
        return [item for item in rep_list if "video" not in item and "anim" not in item]

def kang(client,message):
    file_path = client.download_media(message.reply_to_message)
    og_ext = file_path.rsplit(".",1)[1]
    try:
        final_ext = conversion_map[og_ext]
    except KeyError:
        message.reply_text("`unsupported sexuality, most likely...`")
        return

    is_animated = final_ext == "tgz" or og_ext == "tgz"
    is_video = final_ext == "webm" or og_ext == "webm"
    if final_ext is not None:
        params = "-vf scale=w=512:h=512:force_original_aspect_ratio=decrease"
        if final_ext == "webm" : params += " -ss 00:00:00 -to 00:00:03"
        ffm.options(f"-i {os.path.relpath(file_path)} {params} downloads/output.{final_ext}")
        os.remove(file_path)
        file_path = os.path.abspath(f'downloads/output.{final_ext}')

    split = message.text.split(" ",1)
    emojis = "🤔" if len(split) == 1 else split[1]
    number_next = 1
    pack_name = None
    pack_name_suffix = f"a{client.get_me().id}_by_pronto_"

    client.send_message("@stickers","/addsticker")

    def react_on_message(_, bot_message):
        nonlocal number_next
        nonlocal pack_name
        nonlocal kang_handler
        nonlocal is_animated
        nonlocal is_video

        if bot_message.from_user.username == "Stickers":
            match getFirst3Spaces(bot_message.text.split(".")[0]):
                case options.CHOOSE_SET:
                    pack_name = choose_pack(bot_message.reply_markup.keyboard,is_animated,is_video)
                    if pack_name == []:
                        t = "/newpack"
                        if is_animated: t = "/newanimated"
                        if is_video: t = "/newvideo"
                        bot_message.reply_text(t)
                    else:
                        pack_name = pack_name[-1]
                        number_next = int(pack_name.split("_")[-1])+1
                        bot_message.reply_text(pack_name)
                case options.OVERFLOW:
                    t = "/newpack"
                    if is_animated: t = "/newanimated"
                    if is_video: t = "/newvideo"
                    bot_message.reply_text(t)
                case options.CHOOSE_NAME:
                    if is_animated: pack_type = "animated"
                    elif is_video: pack_type = "video"
                    else: pack_type = "kang"
                    bot_message.reply_text(f"@{client.get_me().username}'s {pack_type} pack vol. {number_next}")
                case options.PUBLISH:
                    bot_message.reply_text("/publish")
                case options.SET_ICON:
                    bot_message.reply_text("/skip")
                case options.PROVIDE_NAME:
                    if is_animated: pack_type = "animated"
                    elif is_video: pack_type = "video"
                    else: pack_type = "kang"
                    pack_name = f"{pack_name_suffix}{pack_type}_{str(number_next)}"
                    bot_message.reply_text(pack_name)
                case options.SEND_STICKER:
                    bot_message.reply_document(file_path)
                case options.EMOJI:
                    bot_message.reply_text(emojis)
                case options.ASK_PUBLISH:
                    bot_message.reply_text(bot_message.reply_markup.keyboard[0][0])
                case options.DONE:
                    bot_message.reply_text("/done")
                    message.reply_text(f"kanged [HERE](https://t.me/addstickers/{pack_name})",quote=True)
                    os.remove(file_path)
                    client.remove_handler(*kang_handler) # remove handler after job is done
                case options.SET_PUBLISHED:
                    message.reply_text(f"kanged [HERE](https://t.me/addstickers/{pack_name})",quote=True)
                    os.remove(file_path)
                    client.remove_handler(*kang_handler) # remove handler after job is done

    kang_handler = client.add_handler(MessageHandler(react_on_message))
    # ^ add handler to react to bot sent messages

help = "`Kang stickers to your own packs, media/animated not supported yet`"