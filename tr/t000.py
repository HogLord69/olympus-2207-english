# -*- coding: utf-8 -*-
# Olympus 2207 -- the strings with no English anywhere in the older build.
#
# Everything else in this project is a port. These 98 are content the Fixed
# Edition added, so they were translated rather than sourced.
#
# Keyed by russian text, so one entry resolves every occurrence across every
# file -- the three identical "Ааааа..." death cries share one key.
#
# Register follows the English already in each file: Fallout's own body-part
# and skill names, "You see a ..." for look-descriptions, and the terse
# idiomatic voice the ported dialogue uses.

T = {

# --- unfinished-content placeholders, kept as placeholders -------------------
# Foxx marks unwritten look-descriptions this way. Translating the marker
# rather than inventing descriptions keeps his "not written yet" visible.
"::описание::": "::description::",
"Описание": "Description",

# --- Mark, Newton ------------------------------------------------------------
"Спасибо, рад помочь, Марк, ты же знаешь. Расскажешь еще о жителях?":
    "Thanks. Glad to help, Mark, you know that. Will you tell me more about the locals?",
"Спасибо, Марк. А теперь давай лучше вернемся к вопросам о городе.":
    "Thanks, Mark. Now let's get back to my questions about the town.",
"Спасибо, Марк. Кстати, мне пора идти. Я еще заскочу.":
    "Thanks, Mark. I should get going, though. I'll stop by again.",

# --- Seth --------------------------------------------------------------------
"Так ты хочешь, чтобы я помог тебе, или нет? Я ведь могу выполнить поручение Мэта.":
    "So do you want my help or not? I could just as easily do Mat's job instead.",

# --- the sleeping farmers (both the male and female variants) ----------------
"::хр-р-р-р-пиу-у-у...::": "::snnnnrk-pheeeew...::",
"::м-м-м-а-а-м-м...::": "::mmm-aaa-mmm...::",
"::м-у-у-а-а-а-м-м-м...::": "::mooo-aaaa-mmmm...::",
"::а-а-р-р-х-х-р-р-р-ю-у...::": "::aaa-rrrh-hrrr-yoooo...::",
"::вздох::": "::sigh::",

# --- Doctor Moreau -----------------------------------------------------------
"Не стоит продолжать врать, когда тебя поймали на лжи. [Моро нажал тревожную кнопку на компьютере]. Сейчас о тебе позаботятся...":
    "There's no sense lying once you've been caught at it. [Moreau presses the alarm button on his computer.] Someone will be along to see to you shortly...",
"[начать бой]": "[start combat]",
"[сделать подсечку доктору]": "[sweep the doctor's legs out from under him]",
"[ударить доктора с правой прямо в нос]": "[right hook, straight to the doctor's nose]",

# --- Beloch ------------------------------------------------------------------
"Тьфу, упрашивать еще вас, твари... Толку никакого...":
    "Pfah. Beg you lot for anything... Waste of breath...",

# --- Osvald ------------------------------------------------------------------
"Вот твоя награда. Если найдешь Слюгер - заходи. [он отдал положенную Вам награду а сам углубился в изучение пистолета. В этот момент его высокомерная физиономия стала простой и задумчивой. В его глазах был интерес, а не презрение. Кажется, он не намерен продолжать с Вами разговор]":
    "Here's your reward. If you ever turn up a Slugger, come see me. [He hands over what he owes and goes back to studying the pistol. For a moment that arrogant face of his turns plain and thoughtful, and there's interest in his eyes instead of contempt. He doesn't look inclined to keep talking.]",
"Эй, Освальд, у меня есть пара вопросов.": "Hey, Osvald, I've got a couple of questions.",
"[конец диалога]": "[end of dialogue]",

# --- Ursul's weapon training -------------------------------------------------
# Skill names follow Fallout's own: Small Guns, Melee Weapons, Unarmed.
"Слушай, а ты можешь меня чему-нибудь обучить?": "Listen - could you teach me something?",
"За 500 батареек, могу рукопашке, легкому или холодному оружию обучить. Но только один раз, времени заниматься этим у меня нету. Так, что сразу определись.":
    "For 500 batteries I can teach you Unarmed, Small Guns or Melee Weapons. Once only, mind - I haven't the time for more. So make your mind up now.",
"Легкому оружию.": "Small Guns.",
"Холодному оружию.": "Melee Weapons.",
"Рукопашному бою.": "Unarmed.",
"Надо подумать.": "I'll think about it.",
"Ну, приступим.": "Right then, let's get to it.",
"Давай 500 батареек.": "Hand over the 500 batteries.",
"У меня столько нет.": "I don't have that much.",
"Держи.": "Here you go.",
"Можешь идти и опробывать новые навыки.": "Off you go. Try out your new skills.",
"Урсул научил вас, как обращаться с легким оружием.":
    "Ursul taught you how to handle small guns.",
"Урсул научил вас, как обращаться с холодным оружием.":
    "Ursul taught you how to handle melee weapons.",
"Урсул научил вас рукопашному бою.": "Ursul taught you unarmed combat.",

# --- aimed-shot targets ------------------------------------------------------
# Fallout's own targeting list reads torso, not chest.
"грудь": "torso",
"руку с пушкой": "gun arm",

# --- combat barks ------------------------------------------------------------
"ААААААА!": "AAAAAAA!",
"Аа-а-а-а-а!!": "Aaa-a-a-a-a!!",
"О-о-о-о-о!": "O-o-o-o-o!",
"Делай ноги!!": "Leg it!!",
"Бег полезен!!!": "Running's good for you!!!",
"Бегом отсюда!": "Run for it!",
"Я больше сюда не ходок!": "I'm never setting foot here again!",
"Быстрее, быстрее!": "Faster, faster!",
"Мне не хватило немного ярости.": "I was a little short on rage.",
"Неееет, я не сдамся ни живым, ни мертвым!":
    "Nooooo, you'll not have me alive or dead!",
"Не догонишь меня!!!": "You'll never catch me!!!",
"Ааааа! Ааааа!": "Aaaaa! Aaaaa!",
"Ааааа!!!": "Aaaaa!!!",
"::аааоооууу::": "::aaaoooouuu::",
"Ааааа...": "Aaaaa...",
"Ахах! Где моя клюка?!": "Ahah! Where's my walking stick?!",

# --- perks -------------------------------------------------------------------
# Phrasing mirrors the existing "lowered slightly by repeated drunkeness".
"Ваши очки жизни немного увеличились в результате продолжительного использования Авто-Дока.":
    "Your hit points have been raised slightly by prolonged use of the Auto-Doc.",
"Ваши очки жизни еще немного увеличились в результате продолжительного использования Авто-Дока.":
    "Your hit points have been raised a little further by prolonged use of the Auto-Doc.",
"Ваши очки жизни немного уменьшились в результате продолжительного использования Авто-Дока.":
    "Your hit points have been lowered slightly by prolonged use of the Auto-Doc.",
"Ваши очки жизни еще немного уменьшились в результате продолжительного использования Авто-Дока.":
    "Your hit points have been lowered a little further by prolonged use of the Auto-Doc.",

# --- character sheet ---------------------------------------------------------
"Здесь указано число убитых вами за время путешествий и приключений человеческих особей мужского пола.":
    "This line shows the number of male humans you have killed in your travels and adventures.",

# --- items -------------------------------------------------------------------
"Карта доступа Х2": "X2 Access Card",

# --- screen settings ---------------------------------------------------------
"Авто": "Auto",
"FPS Лимит": "FPS Limit",
"Панель игрока": "Player Panel",
"Уровень яркости": "Brightness",
"Установлено %d нодов.": "%d nodes set.",
"Сглаживание": "Antialiasing",
"Задает уровень яркости картинки игры в режиме DirectX 9.":
    "Sets the brightness of the game image in DirectX 9 mode.",
"Задает ширину информационного дисплей для сообщений на главной игровой панели игрока.":
    "Sets the width of the message display on the main player panel.",
"Ограничивает частоту кадров в игре до 100-150 FPS. Лишние кадры отбрасываются.":
    "Caps the frame rate at 100-150 FPS. Extra frames are dropped.",
"Включает принудительное сглаживание картинки игры при масштабировании окна в DirectX 9.":
    "Forces antialiasing when the game window is scaled in DirectX 9.",

# --- companion skill-use lines ----------------------------------------------
"Давай я помогу.": "Let me help.",
"Я могу это сделать.": "I can do that.",
"Я получил это.": "I got it.",
"Рад помочь.": "Glad to help.",
"Окей.": "Okay.",
"Я попробую.": "I'll give it a try.",
"Если будут проблемы, дай мне знать.": "Let me know if you run into trouble.",
"Вы получили это?": "Did you get it?",
"Если это то что вы хотели.": "If that's what you were after.",
"Действуй, пробуй!": "Go on, give it a go!",
"Иди вперед.": "Go ahead.",
}
