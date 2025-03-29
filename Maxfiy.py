import telebot
import sqlite3
from telebot import types

# Telegram bot token
bot = telebot.TeleBot("7643121260:AAHJ_3Nj3d9uSchcQtYXOBJMBOBop_iDIvQ")

# SQLite3 baza bilan bog'lanish
conn = sqlite3.connect("1412.db", check_same_thread=False)  # Baza fayli mavjud bo'lmasa, uni yaratadi
cursor = conn.cursor()

# Foydalanuvchilar jadvalini yaratish
cursor.execute("""
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER,
    name TEXT,
    phone TEXT
)
""")
conn.commit()



# Telefon raqamini so'rash
@bot.message_handler(commands=['start'])
def startpg(message):
    user_id = message.chat.id
    contact_menu = types.ReplyKeyboardMarkup(True,False)
    contact_button = types.KeyboardButton("📱 Telefon raqamni ulashish", request_contact=True)
    contact_menu.add(contact_button)
    bot.send_message(
        message.chat.id,
        "Botdan foydalanish uchun telefon raqamingizni ulashing 👇",
        reply_markup=contact_menu
    )
    log_user_action(user_id, 'Bot ishga tushdi')

# Telefon raqamini qayta ishlash
@bot.message_handler(content_types=['contact'])
def handle_contact(message):
    user_id = message.chat.id
    user_name = message.chat.first_name or "Ismi ko'rsatilmagan"
    user_phone = message.contact.phone_number
    
    cursor.execute("INSERT INTO users (user_id, name, phone) VALUES (?, ?, ?)", (user_id, user_name, user_phone))
    conn.commit()
    
    admin_id = "7961099561"  # Admin ID
    bot.send_message(
        admin_id,
        f"Yangi foydalanuvchi:\nID: {user_id}\nIsmi: {user_name}\nTelefon raqami: +{user_phone}"
    )

    # Foydalanuvchiga asosiy menyu berish
    main_menu = types.ReplyKeyboardMarkup(resize_keyboard=True)
    main_menu.row('🥞Ovqatlanish🍯', '🏃‍♀️Fitnes modellari🏃')
    main_menu.row('🏋️‍♀️Mashg‘ulotlar🏋️', '✅Foydali maslahatlar✅')
    bot.send_message(
        user_id,
        "Rahmat! Telefon raqamingiz qabul qilindi. Endi botdan foydalanishingiz mumkin.",
        reply_markup=main_menu
    )

# Bosh sahifa
def sahifa(message):
    main_menu = types.ReplyKeyboardMarkup(resize_keyboard=True)
    main_menu.row('🥞Ovqatlanish🍯', '🏃‍♀️Fitnes modellari🏃')
    main_menu.row('🏋️‍♀️Mashg‘ulotlar🏋️', '✅Foydali maslahatlar✅')
    bot.send_message(message.chat.id, "Tegishli bo'limni tanlang", reply_markup=main_menu)

# Matnli xabarlar uchun ishlov berish
@bot.message_handler(content_types=['text'])
def handle_text(message):
    user_id = message.chat.id
    if message.text == 'Bosh sahifa▶️':
        sahifa(message)
        log_user_action(user_id, "Bosh sahifa")
    elif message.text == '🥞Ovqatlanish🍯':
        pitani = types.ReplyKeyboardMarkup(resize_keyboard=True)
        pitani.row('🥚Dietalar🥗', '🥕Vitaminlar🥝')
        pitani.row('🛢Sport qo‘shimchalari🥛', '💎Minerallar⛏️')
        pitani.row('💊Anabolik steroidlar💉', 'Bosh sahifa▶️')
        bot.send_message(message.chat.id, "Tanlovni bajaring:", reply_markup=pitani)
        log_user_action(user_id, "Ovqatlanish menyusi")
    elif message.text == '🔙 Orqaga':
        baza = types.ReplyKeyboardMarkup(True, False)
        baza.row('👥 Foydalanuvchilar roʻyxati')
        baza.row('🗑 Foydalanuvchilarni oʻchirish')
        baza.row('Bosh sahifa▶️')
        bot.send_message(message.chat.id, "Ma'lumotlar bazasi bo'limi", reply_markup=baza)
        
    elif message.text == '🥚Dietalar🥗':
        dieta_menu = types.ReplyKeyboardMarkup(resize_keyboard=True)
        dieta_menu.row('💪🏻Mushak massasi orttirish🍖')
        dieta_menu.row('🏃🏻Ozish va quritish🏃🏻‍♀️')
        dieta_menu.row('Bosh sahifa▶️')
        bot.send_message(
            message.chat.id,
            "Bu yerda dietalar tamoyillari keltirilgan. Mahsulotlarni BZhU jadvallaridan tanlashingiz mumkin.",
            reply_markup=dieta_menu
        )
        log_user_action(user_id, "Dietalar menyusi")

    elif message.text == '💪🏻Mushak massasi orttirish🍖':
        bot.send_message(message.chat.id, 'http://telegra.ph/Nabor-Myshechnoj-Massy-09-23')
        log_user_action(user_id, "Mushak massasi orttirish dietasi")

    elif message.text == '🏃🏻Ozish va quritish🏃🏻‍♀️':
        bot.send_message(message.chat.id, 'http://telegra.ph/SUSHKA-teladlya-MUZHCHIN-i-ZHENSHCHIN-09-23')
        log_user_action(user_id, "Ozish va quritish dietasi")


    elif message.text == '🥕Vitaminlar🥝':
        vitamin1 = types.ReplyKeyboardMarkup(True, False)
        vitamin1.row('🍓Umumiy🍎')
        vitamin1.row('Bosh sahifa▶️')
        bot.send_message(message.chat.id, "Kerakli bo‘limni tanlang", reply_markup=vitamin1)
        log_user_action(user_id, "Vitaminlar menyusi")

    elif message.text == '🍓Umumiy🍎':
        bot.send_message(message.chat.id, 'https://uz.wikipedia.org/wiki/Vitaminlar')
        log_user_action(user_id, "Vitaminlar bo‘limi: Umumiy")

    
    elif message.text == '🛢Sport qo‘shimchalari🥛':
        dobavki23 = types.ReplyKeyboardMarkup(True, False)
        dobavki23.row('🥚Protein🥛', '🛢Geyner🍯')
        dobavki23.row('❇️Amino kislotalar⚱️', '☑️BCAA✳️')
        dobavki23.row('💊L-Arginin🎈', '💊Tribulus👌🏻')
        dobavki23.row('Bosh sahifa▶️')
        bot.send_message(message.chat.id, "Tanlang:", reply_markup=dobavki23)
        log_user_action(user_id, "Sport qo‘shimchalari menyusi")

    elif message.text == '🥚Protein🥛':
        bot.send_message(message.chat.id, 'http://telegra.ph/Protein-09-23')
        log_user_action(user_id, "Protein haqida ma'lumot")

    elif message.text == '🛢Geyner🍯':
        bot.send_message(message.chat.id, 'http://telegra.ph/CHto-takoe-gejner-09-23')
        log_user_action(user_id, "Geyner haqida ma'lumot")

    elif message.text == '❇️Amino kislotalar⚱️':
        bot.send_message(message.chat.id, 'http://telegra.ph/Aminokisloty-09-23')
        log_user_action(user_id, "Amino kislotalar haqida ma'lumot")

    elif message.text == '☑️BCAA✳️':
        bot.send_message(message.chat.id, 'http://telegra.ph/BCAA-09-23')
        log_user_action(user_id, "BCAA haqida ma'lumot")

    elif message.text == '💊L-Arginin🎈':
        bot.send_message(message.chat.id, 'http://telegra.ph/L-Arginin---donator-azota-09-23')
        log_user_action(user_id, "L-Arginin haqida ma'lumot")

    elif message.text == '💊Tribulus👌🏻':
        bot.send_message(message.chat.id, 'http://telegra.ph/Tribulus-Terestris-09-23')
        log_user_action(user_id, "Tribulus haqida ma'lumot")

    # Minerallar
    elif message.text == '💎Minerallar⛏️':
        mineral1 = types.ReplyKeyboardMarkup(True, False)
        mineral1.row('Rux', 'Magniy', 'Kalsiy')
        mineral1.row('Kaliy', 'Brom', 'Yod')
        mineral1.row('Temir', 'Ftor', 'Mis')
        mineral1.row('Bosh sahifa▶️')
        bot.send_message(message.chat.id, "Kerakli mineralni tanlang:", reply_markup=mineral1)
        log_user_action(user_id, "Minerallar menyusi")

    elif message.text == 'Rux':
        bot.send_message(message.chat.id, 
                         "Rux organizmda 200 dan ortiq fermentlar sintezida ishtirok etadi. "
                         "Bu o‘sish, jinsiy yetilish va qon hosil qilish jarayonlariga ta'sir ko‘rsatadi.")
        bot.send_message(message.chat.id, 
                         "Manbalar: go‘sht, baliq, dengiz mahsulotlari, dukkaklilar, don mahsulotlari.")
        # bot.send_photo(message.chat.id, const.PHOTOVITAMIN1)
        log_user_action(user_id, "Mineral: Rux")

    elif message.text == 'Magniy':
        bot.send_message(message.chat.id, "Magniy haqida batafsil ma'lumot")
        bot.send_message(message.chat.id, "Magniy (Magnesium), Mg — Mendeleyev davriy sistemasining II guruhiga mansub kimyoviy element; ishkoriy - yer metallarga kiradi. Tartib raqami 12, atom massasi 24,305. Tabiiy Magniy 3 ta barqaror izotopdan iborat. 24Mg (78,60%), 25Mg (10,11%), 26Mg (11,29%).")
        # bot.send_photo(message.chat.id, const.PHOTOVITAMIN2)
        log_user_action(user_id, "Mineral: Magniy")

    elif message.text == 'Kalsiy':
        bot.send_message(message.chat.id, "Kalsiy haqida batafsil ma'lumot")
        bot.send_message(message.chat.id, "Kalsiy kalsiy metali va uning tuzlarini olishda, gaz va suyuqliklarni quritishda, betonning qotish jarayonini tezlashtirishda, tibbiyotda asabni tinchlantiruvchi, qon toʻxtatuvchi dori sifatida, allergik kasalliklarni davolashda qoʻllanadi")
        # bot.send_photo(message.chat.id, const.PHOTOVITAMIN3)
        log_user_action(user_id, "Mineral: Kalsiy")
    elif message.text == 'Kaliy':
        bot.send_message(message.chat.id, "Kaliy haqida batafsil ma'lumot")
        bot.send_message(message.chat.id, "Kaliy — Mendeleyev davriy sistemasining I guruhiga mansub kimyoviy element. Ishqoriy metall, tartib raqami 19, atom massasi 39,0983. Ikkita barqaror izotop — 3'K(93,259 %), 4|K(6,729 %), shuningdek, radioaktiv izotop 40K(T|/2= 1,32- 10-yil)dan iborat.")
        # bot.send_photo(message.chat.id, const.PHOTOVITAMIN3)
        log_user_action(user_id, "Mineral: Kaliy")
    elif message.text == 'Brom':
        bot.send_message(message.chat.id, "Brom haqida batafsil ma'lumot")
        bot.send_message(message.chat.id, "Brom (lotincha Bromum, yun. bromos), Brom— Mendeleyev davriy sistemasining VII guruhi kimyoviy elementi, galogenlardan biri; tartib raqami 35, atom massasi 79,904; odatdagi sharoitda yoqimsiz hidli, qizgʻish-qoʻngʻir suyuqlik. Suyuqlanish temperaturasi — 7,25°, qaynash temperaturasi 59,2°.")
        # bot.send_photo(message.chat.id, const.PHOTOVITAMIN3)
        log_user_action(user_id, "Mineral: Brom")
    elif message.text == 'Yod':
        bot.send_message(message.chat.id, "Yod haqida batafsil ma'lumot")
        bot.send_message(message.chat.id, "iodis — binafsha rangli), I — Mendeleyev davriy sistemasining VII guruhiga mansub kimyoviy element, galogenlarga kiradi. Tartib raqami —53, atom massasi 126,9045. 1811 yilda fransuz kimyogari Yod Kurtua tomonidan kashf etilgan. Tabiiy Yod atom massasi 127 ga teng boʻlgan bitta barqaror izotopdan iborat")
        # bot.send_photo(message.chat.id, const.PHOTOVITAMIN3)
        log_user_action(user_id, "Mineral: Yod")
    elif message.text == 'Temir':
        bot.send_message(message.chat.id, "Temir haqida batafsil ma'lumot")
        bot.send_message(message.chat.id, "Temir (lotincha: Ferrum), Fe — Mendeleyev davriy sistemasining VIII guruxiga mansub kimyoviy element. Tartib raqami 26; atom massasi 55,847. Temir 4 ta barqaror izotop: 54Fe(5,84%), 56Fe(91,68%), 57Fe(2,17%) va 58Fe(0,31%) dan iborat. Temir qadimdan ishlatib kelingan")
        # bot.send_photo(message.chat.id, const.PHOTOVITAMIN3)
        log_user_action(user_id, "Mineral: Temir")
    elif message.text == 'Ftor':
        bot.send_message(message.chat.id, "Ftor haqida batafsil ma'lumot")
        bot.send_message(message.chat.id, "Ftor (yunoncha: phthoros — oʻlim, buzilish), F — Mendeleyev davriy sistemasining VII mansub guruhiga kimyoviy element; galogenlarga kiradi. Tartib raqami 9, atom massasi 18.998403. Ftor bir izotop |9Gʻ dan iborat. Shuning uchun Ftor 'sof element' hisoblanadi")
        # bot.send_photo(message.chat.id, const.PHOTOVITAMIN3)  
        log_user_action(user_id, "Mineral: Ftor")
    elif message.text == 'Mis':
        bot.send_message(message.chat.id, "Mis haqida batafsil ma'lumot")
        bot.send_message(message.chat.id, "Mis (lotincha: cuprum — Kipr o. nomidan olingan), Cu — Mendeleyev davriy sistemasining 1 guruhiga mansub kimyoviy element. Tartib raqami 29,atom massasi 63,546. Tabiiy Mis ikkita barkaror izotop 63Cu(69,1%) va 65Cu(30,9%)dan iborat. Sunʼiy radioaktiv izotoplardan 61Cu, MCu muhim")
        # bot.send_photo(message.chat.id, const.PHOTOVITAMIN3)
        log_user_action(user_id, "Mineral: Mis")
    

    # Shu kabi qolgan minerallar ham ishlanadi...

    # Anabolik steroidlar
    elif message.text == '💊Anabolik steroidlar💉':
        anabol1 = types.ReplyKeyboardMarkup(True, False)
        anabol1.row('💉Inyeksiya💉')
        anabol1.row('💊Og‘zaki preparatlar💊')
        anabol1.row('💉Kursdan keyingi terapiya💊')
        anabol1.row('Bosh sahifa▶️')
        bot.send_message(message.chat.id, "Kerakli bo‘limni tanlang:", reply_markup=anabol1)
        log_user_action(user_id, "Anabolik steroidlar menyusi")

    elif message.text == '💉Inyeksiya💉':
        inekc1 = types.ReplyKeyboardMarkup(True, False)
        inekc1.row('💉Andropen275💉', '💉Jintropin💉')
        inekc1.row('💉Anapolon💉', '💉Klomid💉')
        inekc1.row('💉Drostanolon💉', '💉Sustamed💉')
        inekc1.row('Bosh sahifa▶️')
        bot.send_message(message.chat.id, "Kerakli inyeksiyani tanlang:", reply_markup=inekc1)
        log_user_action(user_id, "Anabolik inyeksiya bo‘limi")

    elif message.text == '💉Andropen275💉':
        bot.send_message(message.chat.id, 'http://telegra.ph/Andropen-275-09-24')
        log_user_action(user_id, "Andropen275 haqida ma'lumot")

    elif message.text == '💉Jintropin💉':
        bot.send_message(message.chat.id, 'http://telegra.ph/Dzhintropin-09-24')
        log_user_action(user_id, "Jintropin haqida ma'lumot")
        
    elif message.text == '💉Anapolon💉':
        bot.send_message(message.chat.id, 'https://images.app.goo.gl/5YQTkRcmKLVWQmAF8')
        log_user_action(user_id, "Anapolon haqida ma'lumot")

    elif message.text == '💉Klomid💉':
        bot.send_message(message.chat.id, 'https://www.rlsnet.ru/drugs/klomid-1671')
        log_user_action(user_id, "Klomid haqida ma'lumot")

    elif message.text == '💉Drostanolon💉':
        bot.send_message(message.chat.id, 'https://en.wikipedia.org/wiki/Drostanolone')
        log_user_action(user_id, "Drostanolon haqida ma'lumot")

    elif message.text == '💉Sustamed💉':
        bot.send_message(message.chat.id, 'https://images.app.goo.gl/Um6zj1BL2KLSkuGS9')
        bot.send_message(message.chat.id, 'https://images.app.goo.gl/VcfCfAPWbKSodTKA7')
        log_user_action(user_id, "Sustamed haqida ma'lumot")

    # Qolgan inyeksi
    
# Og‘zaki preparatlar
    elif message.text == '💊Og‘zaki preparatlar💊':
        oral1 = types.ReplyKeyboardMarkup(True, False)
        oral1.row('💊Methandrostenolone💊', '💊Stanozolol💊')
        oral1.row('💊Turinabol💊', '💊Oksandrolon💊')
        oral1.row('💊Anadrol💊')
        oral1.row('Bosh sahifa▶️')
        bot.send_message(message.chat.id, "Kerakli preparatni tanlang:", reply_markup=oral1)
        log_user_action(user_id, "Og‘zaki steroidlar menyusi")

    elif message.text == '💊Methandrostenolone💊':
        bot.send_message(message.chat.id, 'https://www.sciencedirect.com/topics/neuroscience/methandrostenolone')
        log_user_action(user_id, "Methandrostenolone haqida ma'lumot")

    elif message.text == '💊Stanozolol💊':
        bot.send_message(message.chat.id, 'https://ru.wikipedia.org/wiki/Станозолол')
        log_user_action(user_id, "Stanozolol haqida ma'lumot")

    elif message.text == '💊Turinabol💊':
        bot.send_message(message.chat.id, 'https://www.youtube.com/watch?v=jboGdyoVvJA')
        log_user_action(user_id, "Turinabol haqida ma'lumot")

    elif message.text == '💊Oksandrolon💊':
        bot.send_message(message.chat.id, 'https://ru.wikipedia.org/wiki/Оксандролон')
        log_user_action(user_id, "Oksandrolon haqida ma'lumot")

    elif message.text == '💊Anadrol💊':
        bot.send_message(message.chat.id, 'https://www.rxlist.com/anadrol-50-drug.htm')
        log_user_action(user_id, "Anadrol haqida ma'lumot")

    # Kursdan keyingi terapiya
    elif message.text == '💉Kursdan keyingi terapiya💊':
        pct1 = types.ReplyKeyboardMarkup(True, False)
        pct1.row('💊Tamoksifen💊', '💊Klomid💊')
        pct1.row('💊Anastrozol💊', '💊Letrozol💊')
        pct1.row('Bosh sahifa▶️')
        bot.send_message(message.chat.id, "Kursdan keyingi terapiya preparatini tanlang:", reply_markup=pct1)
        log_user_action(user_id, "Kursdan keyingi terapiya menyusi")

    elif message.text == '💊Tamoksifen💊':
        bot.send_message(message.chat.id, 'https://apteka.uz/uz/product/tamoksifen')
        log_user_action(user_id, "Tamoksifen haqida ma'lumot")

    elif message.text == '💊Klomid💊':
        bot.send_message(message.chat.id, 'http://telegra.ph/Klomid-v-bodibildinge-09-24')
        log_user_action(user_id, "Klomid haqida ma'lumot")

    elif message.text == '💊Anastrozol💊':
        bot.send_message(message.chat.id, 'https://med24.uz/uz/product/anastrozol-tabletki')
        log_user_action(user_id, "Anastrozol haqida ma'lumot")

    elif message.text == '💊Letrozol💊':
        bot.send_message(message.chat.id, 'https://apteka.uz/uz/product/letrozol')
        log_user_action(user_id, "Letrozol haqida ma'lumot")
    
    # Bosh sahifaga qaytish
    elif message.text == 'Bosh sahifa▶️':
        startpg(message)
        log_user_action(user_id, "Bosh sahifaga qaytish")


    elif message.text == '🏃‍♀️Fitnes modellari🏃':
        bot.send_message( message.chat.id,'https://www.google.com/search?sca_esv=5eec4df861aac159&biw=1872&bih=964&q=fitnes+modellari+haqida+malumot&udm=7&fbs=AEQNm0ATtbC49U4Qw-vyWIJ8ecjuFu7-jruAR185CCdeYYCOxw_MBAu7hhjYG_sDoXl3o_uCMetJDjMk04_KOq0RLSIhgwNIUgSCGKtp_8jUS5GOb90uYb9BpSZVCwYISeDGyGnOQ_CtdTNRdGe2QGVvlq15KPEYnX2FQIIlpJdRtrVkUulHWb4&sa=X&ved=2ahUKEwi4xujS_OqKAxUQKRAIHT2KNv4QtKgLegQIEBAB#ip=1')
        bot.send_message(message.chat.id, '👆🏻Fitnes haqida malomot👆🏻🫴🏻')
        log_user_action(user_id, "Fitnes modellari")

    elif message.text == '🏋️‍♀️Mashg‘ulotlar🏋️':
        bot.send_message( message.chat.id,'https://cyberleninka.ru/article/n/sport-turlarida-mashg-ulotlarni-tashkil-etish-va-sifat-darajasini-oshirish-vositalari')
        bot.send_message(message.chat.id, '👆🏻Mashg‘ulotlar haqida malumotlarni shu joydan topasiz👆🏻🫴🏻')
        log_user_action(user_id, "Fitnes modellari")
        
    elif message.text == '✅Foydali maslahatlar✅':
        bot.send_message( message.chat.id,'https://daryo.uz/2020/10/06/erta-tongda-sport-bilan-shugullanishning-organizmga-7-foydasi')
        bot.send_message(message.chat.id, '👆🏻Foydali maslahatlarni shu joydan topasiz👆🏻🫴🏻')
        log_user_action(user_id, "✅Foydali maslahatlar✅")
    elif message.text == '/admin':
    # Foydalanuvchidan telefon raqamini so'rash
        contact_menu = types.ReplyKeyboardMarkup(resize_keyboard=True)
        contact_button = types.KeyboardButton("📱 Telefon raqamni ulashish", request_contact=True)
        contact_menu.add(contact_button)
        bot.send_message(
            message.chat.id,
            "Admin menyusiga kirish uchun telefon raqamingizni ulashing 👇",
            reply_markup=contact_menu
        )
        bot.register_next_step_handler(message, handle_admin_contact)  # Telefon raqamini qayta ishlash funksiyasiga o'tish
    elif message.text == '0831':
        bot.register_next_step_handler(message,check_admin_password)
    elif message.text == '👥 Foydalanuvchilar roʻyxati':
        cursor.execute("SELECT rowid, name, phone FROM users")
        users = cursor.fetchall()
        if users:
            msg = "\n".join([f"Qator:{rowid} , Ismi: {name}, Telefon: +{phone}" for rowid, name, phone in users])
        else:
            msg = "Hozircha hech qanday foydalanuvchi yo'q."
        bot.send_message(message.chat.id, msg)
        
    elif message.text == '🗑 Foydalanuvchilarni oʻchirish':
        
        user_id = message.chat.id
        log_user_action(user_id,'🗑 Foydalanuvchilarni oʻchirish tugmasini bosdi ! ')
        button = types.ReplyKeyboardMarkup(True,False)
        button.row('❌ Barchasini o‘chirish')
        button.row('❌Qator bo‘yicha oʻchirish')
        button.row('🔙 Orqaga')
        button.row('Bosh sahifa▶️')
        bot.send_message(message.chat.id,'Malumotlarni oʻchirish boʻlimi',reply_markup=button)
    elif message.text == '❌ Barchasini o‘chirish':
        cursor.execute("DELETE FROM users")  # Barcha foydalanuvchilarni o'chirish
        cursor.execute("DELETE FROM sqlite_sequence WHERE name='users'")  # ID qiymatini ham tozalash
        conn.commit()
        bot.send_message(message.chat.id, "Barcha foydalanuvchilar muvaffaqiyatli o'chirildi va ID tiklandi.")
    elif message.text == '❌Qator bo‘yicha oʻchirish':
        msg = bot.send_message(message.chat.id, 'O‘chirish uchun foydalanuvchi qatorini kiriting:')
        bot.register_next_step_handler(msg, delete_user)
    elif message.text == '/malumot':
        bot.send_message(message.chat.id,f"🛠 Admin haqida ma'lumot \n👤 Ismi: [ASLIDDIN]\n📞 Aloqa: [+998889791008]\nTelgram user: [@aslidd1nake_o1]📍\nJoylashuv: [Qashqadaryo - Qamashi]")
#	elif message.text == '🔙 Orqaga':
 #        baza = types.ReplyKeyboardMarkup(True, False)
#         baza.row('👥 Foydalanuvchilar roʻyxati')
#         baza.row('🗑 Foydalanuvchilarni oʻchirish')
#         baza.row('Bosh sahifa▶️')
#l 		bot.send_message(message.chat.id, "Ma'lumotlar bazasi bo'limi", reply_markup=baza)


user_attempts = {}

def handle_admin_contact(message):
    if message.contact:
        user_id = message.chat.id
        user_phone = message.contact.phone_number

        # Admin ID-siga foydalanuvchi ID va telefon raqamini yuborish
        admin_id = 7961099561  # Adminning haqiqiy Telegram ID-sini kiriting
        bot.send_message(
            admin_id,
            f"Admin menyusiga kirishga uringan foydalanuvchi:\n"
            f"Foydalanuvchi ID: {user_id}\n"
            f"Telefon raqami: +{user_phone}"
        )

        # Foydalanuvchiga parol so'rash
        user_attempts[user_id] = 0  # Har bir foydalanuvchi uchun urinishlarni boshlash
        msg = bot.send_message(message.chat.id, "Parolni kiriting:")
        bot.register_next_step_handler(msg, check_admin_password)
    else:
        bot.send_message(message.chat.id, "Telefon raqami ulashilmadi. Iltimos, qaytadan urinib ko'ring.")

def check_admin_password(message):
    user_id = message.chat.id
    correct_password = '0831'
    
    # Foydalanuvchi parolni to'g'ri kiritgan bo'lsa
    if message.text == correct_password:
        bot.send_message(message.chat.id, "Parol to'g'ri!")
        log_user_action(user_id, 'Adminlik menyusiga muvaffaqiyatli kirildi')

        # Adminlik menyusini ko'rsatish
        baza = types.ReplyKeyboardMarkup(True, False)
        baza.row('👥 Foydalanuvchilar roʻyxati')
        baza.row('🗑 Foydalanuvchilarni oʻchirish') 
        baza.row('Bosh sahifa▶️')
        bot.send_message(message.chat.id, "Ma'lumotlar bazasi bo'limi", reply_markup=baza)

    # Noto'g'ri parol bo'lsa
    else:
        user_attempts[user_id] += 1  # Urinishni hisoblash
        if user_attempts[user_id] >= 3:
            bot.send_message(message.chat.id, "Siz 3 martadan ko'proq urindiz, kirish rad etildi.")
            log_user_action(user_id, "Adminlik menyusiga kirishga 3 marta muvaffaqiyatsiz urinish")
        else:
            msg = bot.send_message(
                message.chat.id,
                f"Noto'g'ri parol. Qayta urinib ko'ring ({3 - user_attempts[user_id]} urinish qoldi):"
            )
            bot.register_next_step_handler(msg, check_admin_password)     
        
def delete_user(message):
    try:
        row_number = int(message.text)
        
        # Tekshirish: Qator mavjudligini aniqlash
        cursor.execute("SELECT COUNT(*) FROM users WHERE rowid = ?", (row_number,))
        if cursor.fetchone()[0] == 0:
            bot.send_message(message.chat.id, f"Qator {row_number} mavjud emas.")
            return
        
        # Qatorni o'chirish
        cursor.execute("DELETE FROM users WHERE rowid = ?", (row_number,))
        conn.commit()
        
        bot.send_message(message.chat.id, f"Foydalanuvchi qator {row_number} muvaffaqiyatli o'chirildi.")
    except ValueError:
        bot.send_message(message.chat.id, "Iltimos, faqat sonli qator raqamini kiriting.")
    except Exception as e:
        bot.send_message(message.chat.id, f"Xato yuz berdi: {str(e)}")
# def delete_user(message):
#     row_number = int(message.text)
#     cursor.execute("DELETE FROM users WHERE rowid = ?", (row_number,))
#     conn.commit()
#     bot.send_message(message.chat.id, f"Foydalanuvchi qator {row_number} muvaffaqiyatli o'chirildi.")

    
        
        
        # baza = types.ReplyKeyboardMarkup(True,False)
        # baza.row('🗂 Ma\'lumotlar bazasi')
        # baza.row()

def log_user_action(user_id, action):
    
    """
    Foydalanuvchi harakatlarini loglash va adminga yuborish funksiyasi
    """
    admin_id = 7961099561
    log_message = f"Foydalanuvchi ID: {user_id} - Amal: {action}"
    bot.send_message(admin_id, log_message)


# Botni ishlatishni boshlash
bot.infinity_polling()
#1
