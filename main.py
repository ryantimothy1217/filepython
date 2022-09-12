import telebot
import json
from datetime import datetime
import time
import psycopg2

bot = telebot.TeleBot('5430244780:AAHj9xAa2joLUFDUYr_isr54jF8PlMzoIJc')
lastdatelog = "2022/07/30-02:05:56.949327"

hostname = 'localhost'
database = 'cobaskripsi'
username = 'postgres'
pwd = '123456'
port_id = 5432
# conn = None
# cur = None

conn = psycopg2.connect(
    host=hostname,
    dbname=database,
    user=username,
    password=pwd,
    port=port_id)
cur = conn.cursor()


def generateTableIfNotExists():
    # Create Table
    create_script = ''' CREATE TABLE IF NOT EXISTS datastore (
                                id      int PRIMARY KEY,
                                jenis_serang varchar(50) NOT NULL,
                                ip_penyerang varchar(15),
                                ip_diserang varchar(15),
                                port_penyerang varchar(15),
                                port_diserang varchar(15),
                                tanggal_serang varchar(15),
                                waktu_serang varchar(15))'''

    cur.execute(create_script)
    conn.commit()

    # Create Sequence for Auto Increment ID
    seq_script = '''
        CREATE SEQUENCE public.autoinc
        INCREMENT 1
        START 1
        MINVALUE 1; 
    '''
    cur.execute(seq_script)
    conn.commit()

    # Alter table and add sequence
    alter_script = "ALTER TABLE ONLY datastore ALTER COLUMN id SET DEFAULT nextval('autoinc'::regclass);"
    cur.execute(alter_script)
    conn.commit()


# @bot.message_handler(commands=['start'])
# def welcome(message):
#     # membalas pesan
#     # createjson(message)
#     bot.reply_to(message, 'Halo bro, ada apa?')
#

@bot.message_handler(commands=['logging'])
def logging(message):
    while True:
        try:
            time.sleep(10)
            print("send log")
            createjson(message)
        except:
            pass

def createjson(message):
    global lastdatelog
    # Opening JSON file
    f = open('alert_json.txt')
    pecah = f.read().split("}")

    json_format = "["

    for index, i in enumerate(pecah):
        json_format += i
        if index >= len(pecah) - 2:
            pass
        else:
            json_format += "}, "

    json_format += "}]"

    # print(json_format)
    # returns JSON object as
    # a dictionary
    data = json.loads(json_format)
    # json.x
    # data = json.dumps(json_format, sort_keys=True, indent=2, separators=(',', ': '))

    # Iterating through the json
    # list
    for i in data:
        # log_timestamp = i['timestamp'] + " 2022"
        # if 'msgs' in i:
        #     print('testt')
        # else:
        #     print('x')

        # log_timestamp = "2022/" + i['timestamp']
        log_timestamp = ("2022/" + i['timestamp']) if 'timestamp' in i else None

        # print(i['dst_port'])
        # print(i['src_port'])
        # print(f"Port: {data['dst_port']}")
        # print(log_timestamp)
        jenis = i['msg'] if 'msg' in i else None
        port1 = str(i['src_port']) if 'src_port' in i else None
        port2 = str(i['dst_port']) if 'dst_port' in i else None
        ip1 = i['src_addr'] if 'src_addr' in i else None
        ip2 = i['dst_addr'] if 'dst_addr' in i else None
        # print(port1)
        # print(port2)
        # converted_port = str(port)

        # print(log_timestamp)

        last_datetime = datetime.strptime(lastdatelog, "%Y/%m/%d-%H:%M:%S.%f")
        log_datetime = datetime.strptime(log_timestamp, "%Y/%m/%d-%H:%M:%S.%f")
        # print(log_datetime)
        tanggal = last_datetime.strftime("%Y-%m-%d")
        waktu = last_datetime.strftime("%H:%M:%S")

        # print(tanggal)
        # print(waktu)
        # cetak_waktu = datetime.strptime(log_timestamp, "%H:%M:%S")
        #
        # print(last_datetime.date())
        # print(log_datetime.date())
        #
        # difference = log_datetime - last_datetime
        # print(difference)
        # print(difference.)
        #
        if log_datetime > last_datetime:
            # print("log_datetime > last_datetime:")
            # bot.reply_to(message, i['src_addr'])
            textMessage = ""

            if jenis is not None:
                textMessage += "Jenis Serangan : " + jenis
            if ip1 is not None:
                textMessage += "\nIP Penyerang : " + ip1
            if ip2 is not None:
                textMessage += "\nIP Diserang : " + ip2
            if port1 is not None:
                textMessage += "\nPort Penyerang : " + port1
            if port2 is not None:
                textMessage += "\nPort Diserang : " + port2
            if tanggal is not None:
                textMessage += "\nTanggal Serang : " + tanggal
            if waktu is not None:
                textMessage += "\nWaktu Serang : " + waktu

            chatid = message.chat.id
            bot.send_message(chatid, textMessage)
            # print(jenis, ip1, ip2, port1, port2, tanggal, waktu)

            insertToDB(jenis, ip1, ip2, port1, port2, tanggal, waktu)

            # bot.send_message(chatid, "IP Serangan : " + i['src_addr'])

            lastdatelog = log_timestamp

            # Closing file
            f.close()


def insertToDB(jenis, ipp, ips, pp, ps, tanggal, waktu):
    insert_script = '''
                        INSERT INTO datastore 
                        (jenis_serang, ip_penyerang, ip_diserang, port_penyerang, port_diserang, 
                        tanggal_serang, waktu_serang) 
                        VALUES ( %s, %s, %s, %s, %s, %s, %s)'''
    insert_values = (jenis, ipp, ips, pp, ps, tanggal, waktu)
    # print(jenis, ipp, ips, pp, ps, tanggal, waktu)

    cur.execute(insert_script, insert_values)
    conn.commit()


while True:
    try:
        bot.polling()
    except:
        pass

# except Exception as error:
#      print(error)
#     finally:
#         if cur is not None:
#             cur.close()
#         if conn is not None:
#             conn.close()
# createjson()
# generateTableIfNotExists()
# depa