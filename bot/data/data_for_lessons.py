active_users = {}

data_dct = {
    'greeting': 'Hello {0.first_name} from skyeng! Choose below what you want to practice ;)',
    'welcome': '''Hey {0.first_name}! 👋🏼 \nI see you are eager to start a lesson!🚀\nGreat Idea!\nChoose a lesson you want to start with\n
                     ⏰ click <b>/time</b> for time lesson \n 📧 click <b>/email</b> for email lesson''',
    'time_messages': {
        'part_1': '''Telling a time? Perfect! Let 's hit the road!🤟🏼''',
        'part_2': '''Read more information about this topic in''' + '<a href="https://magazine.skyeng.ru/kak-na-samom-dele-pravilno-nazyvat-vremja-na-anglijskom/"> <b>the article in Skyeng Magazine</b></a>',
        'part_yt_1': '''Look the best explanation of the topic''' + '<a href="https://www.youtube.com/watch?v=AyAQfTxGyqI/"> <b>on YouTube channel attentively!</b></a>',
        'part_yt_2': '''❗️Watch the video on youtube!\nAnd come back here, complete tasks for new knowledge ''',
        'part_3': '''🔥 Now let's practise!\n<b>Listen and repeat after me</b>''',
        'practice_mes_1': '''12:00 — It's twelve o'clock''',
        'voice_mess_1': '''It's twelve o'clock''',
        'part_6': '''Record your voice message to show how you repeat 🎙'''
    },

    'email_messages': {
        'message_1': '''How to say "@"? Perfect! Let 's hit the road!🤟🏼''',
        'message_2':  '''
            🗯 Word: "@" — at
            🔹Transcription: [æt]
            🔹Meaning: (computing) the symbol (@) used in email addresses 
            🔹Translation: -
            ⚡️Level: A1''',
        'message_3': 'at',
        'message_4': '''Listen how to pronounce <b>"@"</b>\n<b>Repeat after me 🤟🏼</b>'''
    },

    'voice_proccesing_messages': {
        'at_0_at': '''Let's have some practice! Record voice, say email below: \n<b>sky@gmail.com </b> 🎙''',
        'at_1_sky': {
            'part_1': '''✅''',
            'part_2': ''' Next task 🔥:\n<b>What's your email? 🖌 Write it using "@", please</b>''',
            'part_3': '''❌'''
        },
        'at_3_text_email': {
            'part_1': 'Please write your email, in this task you need to write exactly, not recording'
        },
        'at_4_own_email_voice': {
            'part_1': '''Please, listen again''',
            'part_2': '''What number of the right e-mail? Write 1, 2 or 3? 👇🏻\n 1. bootcampatgmail.com\n 2. bootcamp.at@gmail.com\n 3. bootcamp@gmail.com''',
            'part_3': '''Well done! Let's check how you got it😏\nChoose what e-mail I will say: '''
        },
        'time_0': {
            'part_1': ''' Next task 🔥\nRecord voice, say: <b>12:05 — It's five past twelve 🎙</b>''',
            'part_2': '''❌\nRecord your message once again'''
        },
        'time_1': {
            'part_1': '''💣''',
            'part_2': ''' Next\n<b>12:30 - It's half past twelve 🎙</b>''',
        },
        'time_2': {
            'part_1': ''' Next\n<b>12:31 - It's twenty-nine to one</b>\nRecord your voice message to show how you repeat 🎙''',
        },
        'time_3': {
            'part_1': ['🎙👉🏻 11:00', '🎙👉🏻 14:00', '🎙👉🏻 23:00', '🎙👉🏻 04:00', '🎙👉🏻 12:00', '🎙👉🏻 22:00', '🎙👉🏻 13:00',
                            '🎙👉🏻 15:00', '🎙👉🏻 04:00', '🎙👉🏻 19:00', '🎙👉🏻 18:00', '🎙👉🏻 20:00', '🎙👉🏻 21:00', '🎙👉🏻 16:00',
                            '🎙👉🏻 17:00']
        },
        'time_4': {
            'part_1': ['🎙👉🏻 11:00', '🎙👉🏻 14:00', '🎙👉🏻 23:00', '🎙👉🏻 04:00', '🎙👉🏻 12:00', '🎙👉🏻 22:00', '🎙👉🏻 13:00',
                            '🎙👉🏻 15:00', '🎙👉🏻 04:00', '🎙👉🏻 19:00', '🎙👉🏻 18:00', '🎙👉🏻 20:00', '🎙👉🏻 21:00', '🎙👉🏻 16:00',
                            '🎙👉🏻 17:00']
        },
        'time_5': {
            'part_1': '''Please, repeat the theory!\nRecord your message once again''',
            'part_2': ["01:01", "01:02", "01:03", "01:04", "01:05", "01:06", "01:07", "01:08",
                             "01:09", "01:10", "01:11", "01:12", "01:13", "01:14", "01:15", "01:16",
                             "01:17", "01:18", "01:19", "01:20", "01:21", "19:19", "19:20", "19:21",
                             "19:22", "19:23", "19:24", "19:25", "19:26", "19:27", "19:28", "19:29",
                             "23:11", "23:12", "23:13", "23:14", "23:15", "23:16", "23:17", "23:18",
                             "23:19", "23:20"]
        },
        'time_6': {
            'part_1': ["01:01", "01:02", "01:03", "01:04", "01:05", "01:06", "01:07", "01:08",
                               "01:09", "01:10", "01:11", "01:12", "01:13", "01:14", "01:15", "01:16",
                               "01:17", "01:18", "01:19", "01:20", "01:21", "19:19", "19:20", "19:21",
                               "19:22", "19:23", "19:24", "19:25", "19:26", "19:27", "19:28", "19:29",
                               "23:11", "23:12", "23:13", "23:14", "23:15", "23:16", "23:17", "23:18",
                               "23:19", "23:20"],
            'part_2': '''Oops, it seems to me you missheard some important information.\nPlease, revise it again and try to record the voice message again.!'''
        },
        'time_7': {
            'part_1': ["01:30", "02:30", "03:30", "04:30", "05:30", "06:30", "07:30", "08:30", "09:30",
                              "10:30", "11:30", "12:30", "16:30", "17:30", "18:30", "19:30", "20:30", "21:30", "22:30",
                              "23:30", "24:30"],
            'part_2': '''Please, repeat the theory!'''
        },
        'time_8': {
            'part_1': '''you try very hard! let's practice some more, but you're already a great fellow 🔥❤️''',
            'part_2': ["01:31", "02:31", "03:31", "04:31", "05:31", "06:31", "07:31", "08:31", "09:31",
                              "10:31", "11:31", "12:31", "16:31", "17:31", "18:31", "19:31", "20:31", "21:31", "22:31",
                              "23:31", "24:31"]
        },
        'time_9': {
            'part_1': '''Next:''',
            'part_2': ["01:31", "02:31", "03:31", "04:31", "05:31", "06:31", "07:31", "08:31", "09:31",
                              "10:31", "11:31", "12:31", "16:31", "17:31", "18:31", "19:31", "20:31", "21:31", "22:31",
                              "23:31", "24:31"]
        },
        'time_10': {
            'part_1': '''🎉Amazing!\n💙Topics learnt\n❤️You are awesome\nChoose next lesson from menu'''
        }
    }
}