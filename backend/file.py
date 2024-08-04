import sys
import os
import psutil
import datetime
import shutil
import logging
from mysql.connector import connect, Error
import pandas as pd
import smpplib.gsm
import smpplib.client
import smpplib.consts
import time
import configparser
from threading import Thread

platforms = {
    "linux": "Linux",
    "linux1": "Linux",
    "darwin": "OS x",
    "win32": "Windows",
    "win64": "Windows"
}

fname = ""
use_method = 0

class sms_generator:
    ip = ""
    port = 0
    username = ""
    passwd = ""    
    files = []
    repeat = False
    amount, amount_per_sec = "", ""

    def __init__(self, ip="", port="", user="", password="yasser1234", files=[], repeat=False, amount=0, amount_per_sec=0):
        self.ip = ip
        self.port = port
        self.username = user
        self.passwd = password
        self.files = files
        self.repeat = repeat
        self.amount = amount
        self.amount_per_sec = amount_per_sec

    def connect_db(self):
        try:
            connection = connect(
                host="db",
                user="root",
                password="yasser1234",
                database="templates"
            )
            return connection
        except Error as e:
            print(f"Error: {e}")
            return None

        


    def create_tables(self):
        connection = self.connect_db()
        if connection:
            try:
                cursor = connection.cursor()
                cursor.execute("""
                    CREATE TABLE IF NOT EXISTS generator (
                        id INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
                        ip VARCHAR(255),
                        file VARCHAR(255),
                        SMS INT,ex
                        total VARCHAR(255),
                        repeaat VARCHAR(255)
                    );
                """)
                connection.commit()
            except Error as e:
                print(f"Error creating table: {e}")
            finally:
                connection.close()

    def checked(self, name):
        connection = self.connect_db()
        if connection:
            try:
                cursor = connection.cursor()
                cursor.execute("SELECT COUNT(*) FROM {}".format(name))
                count = cursor.fetchone()[0]
                return count
            except Error as e:
                print(f"Error checking table: {e}")
                return 0
            finally:
                connection.close()

    def Generator(self):
        self.create_tables()
        connection = self.connect_db()
        if connection:
            try:
                cursor = connection.cursor()
                s = '''
                CREATE TABLE IF NOT EXISTS generator_''' + (self.files[0].split("/")[-1]).split(".")[0] + '''(
                               id INT PRIMARY KEY AUTO_INCREMENT,
                               ip   VARCHAR(255),
                               port VARCHAR(255),
                               user VARCHAR(255), 
                               password VARCHAR(255), 
                               file VARCHAR(255), 
                               repeaat VARCHAR(255), 
                               amount VARCHAR(255), 
                               amount_per_sec VARCHAR(255)
                );
                '''
                cursor.execute(s)
                file = ",".join(self.files)
                s = "INSERT INTO generator(ip,file,SMS,total,repeaat) values('{}','{}',0,'{}','{}')".format(
                    str(self.ip) + ":" + str(self.port), file, str(self.amount), self.repeat)
                cursor.execute(s)
                s = """INSERT INTO generator_""" + (self.files[0].split("/")[-1]).split(".")[0] + """(ip, port, user, password, file, repeaat, amount,
                amount_per_sec) VALUES ('{}', '{}', '{}', '{}', '{}','{}', '{}', '{}')""".format(self.ip,
                self.port, self.username, self.passwd, file, self.repeat, self.amount, self.amount_per_sec)
                cursor.execute(s)
                connection.commit()
            except Error as e:
                print(f"Error in Generator method: {e}")
            finally:
                connection.close()

    def get_last_id(self):
        connection = self.connect_db()
        if connection:
            try:
                cursor = connection.cursor()
                cursor.execute("SELECT MAX(id) FROM generator;")
                last_id = cursor.fetchone()[0]
                return last_id
            except Error as e:
                print(f"Error getting last ID: {e}")
                return None
            finally:
                connection.close()

    def connection(self, query):
        connection = self.connect_db()
        if connection:
            try:
                cursor = connection.cursor()
                cursor.execute(query)
                connection.commit()
            except Error as e:
                print(f"Error executing query: {e}")
            finally:
                connection.close()

    def get_all_data(self):
        connection = self.connect_db()
        if connection:
            try:
                cursor = connection.cursor()
                cursor.execute("SELECT * FROM generator")
                rows = cursor.fetchall()
                return rows
            except Error as e:
                print(f"Error getting all data: {e}")
                return []
            finally:
                connection.close()

    def get_data(self, table):
        connection = self.connect_db()
        if connection:
            try:
                cursor = connection.cursor()
                cursor.execute("SELECT * FROM {}".format(table))
                rows = cursor.fetchall()
                return rows
            except Error as e:
                print(f"Error getting data: {e}")
                return []
            finally:
                connection.close()

    def get_file_by_id(self, id):
        connection = self.connect_db()
        if connection:
            try:
                cursor = connection.cursor()
                query = "SELECT file FROM generator WHERE id = %s"
                cursor.execute(query, (id,))
                result = cursor.fetchone()
                if result is not None:
                    file = result[0]
                    return file
                else:
                    print("No matching row found in the database.")
                    return None
            except Error as e:
                print(f"Error getting file by ID: {e}")
                return None
            finally:
                connection.close()

    def get_data_by_id(self, id):
        files = self.get_file_by_id(id)
        connection = self.connect_db()
        if connection:
            try:
                cursor = connection.cursor()
                query = "SELECT ip, port, user, password, file, repeaat, amount, amount_per_sec FROM generator_{}".format(
                    files.split(",")[0].split("/")[-1].split(".")[0])
                cursor.execute(query)
                data = cursor.fetchall()[0]
                if data:
                    ip, port, user, password, file, repeat, total, a = data
                    repeat = bool(repeat)
                    return ip, port, user, password, file, repeat, total, a
                else:
                    return None
            except Error as e:
                print(f"Error getting data by ID: {e}")
                return None
            finally:
                connection.close()

    def send_sms(self, client, src, dst, msg, monitor, total, last_id, username, password, monitor_sec, sec):
        print("Monitor:{}/Monitor Per Sec:{}/Amount Per Sec:{}/Total:{}".format(monitor, monitor_sec, sec, total))
        if int(monitor) == int(total):
            return monitor, monitor_sec
        elif monitor_sec == sec:
            return monitor, monitor_sec
        else:
            logging.debug('Connected')
            file = open("Logs.txt", "a")
            file.write("\n\nMessage {} is Sending .................. \n\nClient Object:{},\nsrc:{}\ndst:{},\nmsg:{}"
                       .format(monitor, client, src, dst, msg))
            file.close()
            parts, encoding_flag, msg_type_flag = smpplib.gsm.make_parts(u"{}".format(msg))
            for part in parts:
                pdu = client.send_message(
                    source_addr_ton=smpplib.consts.SMPP_TON_ALNUM,
                    source_addr_npi=smpplib.consts.SMPP_NPI_UNK,
                    source_addr=src,
                    dest_addr_ton=smpplib.consts.SMPP_TON_INTL,
                    dest_addr_npi=smpplib.consts.SMPP_NPI_ISDN,
                    destination_addr=dst,
                    short_message=part,
                    data_coding=encoding_flag,
                    esm_class=msg_type_flag,
                    registered_delivery=True,
                )
                logging.info('submit_sm {}->{} seqno: {}'.format(pdu.source_addr, pdu.destination_addr, pdu.sequence))
            self.connection("UPDATE generator SET SMS={} WHERE id={}".format(int(monitor), int(last_id)))
            monitor = int(monitor) + 1
            monitor_sec = int(monitor_sec) + 1
            print("\nSending SMS Number:{}\n".format(str(monitor)))
            return monitor, monitor_sec

    def sms_per_files(self, client, files, monitor, total, last_id, username, password, monitor_sec, sec, r):
        if isinstance(files, str):
            files = [files]
        for fi in files:
            monitor, monitor_sec = self.sms_per_file(client, fi, monitor, total, last_id, username, password, monitor_sec, sec, r)
        return monitor, monitor_sec

    def sms_per_file(self, client, file, monitor, total, last_id, username, password, monitor_sec, sec, repeat):
        connection = self.connect_db()
        if connection:
            try:
                cursor = connection.cursor()
                query = "SELECT * FROM {}".format((file.split("/")[-1]).split(".")[0])
                cursor.execute(query)
                data = cursor.fetchall()
                for row in data:
                    if int(monitor) >= int(total):
                        return monitor, monitor_sec
                    if int(monitor_sec) == int(sec) and not monitor_sec == 1:
                        monitor_sec = 0
                        time.sleep(1)
                        if not repeat:
                            self.sms_per_files(client, file, monitor, total, last_id, username, password, monitor_sec, sec, repeat)
                        return monitor, monitor_sec
                    src, dst, msg = row[1], row[2], row[3]
                    monitor, monitor_sec = self.send_sms(
                        client,
                        src,
                        dst,
                        msg,
                        monitor,
                        total,
                        last_id,
                        username,
                        password,
                        monitor_sec,
                        sec
                    )
                return monitor, monitor_sec
            except Error as e:
                print(f"Error in sms_per_file method: {e}")
                return monitor, monitor_sec
            finally:
                connection.close()

    def send_per_amount(self, client, files, amount_per_sec, amount, last_id, username, password):
        monitor = 1
        done = False
        monitor_sec = 1
        while not done:
            for i in range(int(amount_per_sec)):
                print("Monitor:{},Amount:{}".format(monitor, amount))
                if int(monitor) == int(amount):
                    done = True
                    print("All sms has been sent!!!!!!!!!")
                    break
                else:
                    print("")
                    print("args:", client, files, monitor, amount, last_id, username, password, monitor_sec, int(amount_per_sec))
                    monitor, monitor_sec = self.sms_per_files(client, files, monitor, amount, last_id, username, password, monitor_sec, int(amount_per_sec), True)
                    print("the monitor is increased:", monitor)
                    print("Sms {} has been sent".format(monitor))
                    print("send_per_amount() monitor_sec=", monitor_sec)
                    print("send_per_amount() amount_per_sec=", amount_per_sec)
                    if int(monitor_sec) == int(amount_per_sec):
                        monitor_sec = 0
                        print("Sleeping for 1 sec..................")
                        time.sleep(1)
            if done:
                break
            else:
                monitor_sec = 0
                print("Sleeping for 1 sec..................")
                time.sleep(1)

    def copy_template(self, files):
        for file in files:
            self.insert_file_rows(file)

    def insert_file_rows(self, file):
        if "/" in file:
            name = (file.split("/")[-1]).split(".")[0]
        else:
            name = file.split(".")[0]
        df = pd.read_csv(file)
        cols = df.columns
        self.connection("""CREATE TABLE IF NOT EXISTS {} (
                   id INT AUTO_INCREMENT PRIMARY KEY,
                   SID VARCHAR(255),
                   Destination VARCHAR(255),
                   Content  VARCHAR(255)
        )""".format(str(name)))
        if len(cols) != 3:
            print("Number of columns in DataFrame doesn't match the expected count.")
            return
        src, dst, msg = str(cols[0]), str(cols[1]), str(cols[2])
        for i, row in df.iterrows():
            self.connection("INSERT INTO {}(SID, Destination, Content) VALUES ('{}', '{}', '{}')".format(name, str(row.iloc[0]), str(row.iloc[1]), str(row.iloc[2])))

    def checked(self, name):
        connection = self.connect_db()
        if connection:
            try:
                cursor = connection.cursor()
                cursor.execute("SELECT COUNT(*) FROM {}".format(name))
                count = cursor.fetchone()[0]
                return count
            except Error as e:
                print(f"Error checking table: {e}")
                return 0
            finally:
                connection.close()

    def main(self, ip, port, user, password, files, repeat=False, a=0, total=0, last_id=1):
        total = int(total)
        self.connection("UPDATE generator set SMS={} where ip='{}'".format(0, str(str(ip) + ":" + str(port))))
        client = smpplib.client.Client(str(ip), int(port))
        client.set_message_sent_handler(
            lambda pdu: logging.info('submit_sm_resp seqno: {} msgid: {}'.format(pdu.sequence, pdu.message_id)))

        def handle_deliver_sm(pdu):
            logging.info('delivered msgid:{}'.format(pdu.receipted_message_id))
            return 0

        client.set_message_received_handler(lambda pdu: handle_deliver_sm(pdu))
        client.connect()
        client.bind_transceiver(system_id=str(user), password=str(password))

        print("Files:{},length:{}".format(files, len(files)))
        print("main args:", ip, port, user, password, files, repeat, total, a, last_id)

        if repeat:
            if isinstance(files, str):
                if len(list(files.split(","))) == 1:
                    total = total
                elif len(files) > 1:
                    total = int(total / len(list(files.split(","))))
                else:
                    print("No Files Inputed.......")
                print("Before sending.........", files)
                self.send_per_amount(client, files, a, total, last_id, user, password)
            else:
                if len(list(files)) == 1:
                    total = total
                elif len(files) > 1:
                    total = int(total / len(files))
                else:
                    print("No Files Inputed.......")
                print("Before sending.........", files)
                self.send_per_amount(client, files, a, total, last_id, user, password)
        else:
            file_list = ",".join(files)
            name = file_list.split(",")[0].split("/")[-1].split(".")[0]
            rows = self.checked(name)
            if (int(total) >= int(rows)):
                total = rows
            else:
                total = total
            if isinstance(files, str):
                if len(list(files.split(","))) == 1:
                    total = int(total) + int(a)
                elif len(list(files.split(","))) > 1:
                    total = int(total / len(list(files.split(",")))) + int(a)
                else:
                    print("No Files Inputed.......")
                print("Before sending.........", total)
            else:
                if len(list(files)) == 1:
                    total = int(total) + int(a)
                elif len(files) > 1:
                    total = int(total / len(list(files))) + int(a)
                else:
                    print("No Files Inputed.......")
                print("Before sending.........", files)
            print("\n\nTotal Before running", total)
            self.sms_per_files(client, files, 2, int(total), last_id, user, password, 0, a, False)


if __name__ == "__main__":
    print("sys.executable:", sys.executable)
    print("sys.path:", sys.path)
    import psutil
    print("psutil version:", psutil.__version__)

    # Ajoutez ces lignes pour tester la création des tables
    sms_gen = sms_generator()
    sms_gen.create_tables()
    print("Tables created successfully.")

