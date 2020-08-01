import os
import re
import shutil
import smtplib
import sys
from datetime import datetime as dt
from email import encoders
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

import mysql.connector
from Extracttext_from_logo2 import *
from cryptography.fernet import Fernet

start = dt.now()

Logo = "bmw"
#
# source=config.Inbound_GHB_path
# this is value coming from the bash file
source = sys.argv[1]
sourceBkp = sys.argv[2]
service_name = "logodetection"
checking_regulerex = "bmw"
table_name = "{}".format(sys.argv[3])
insert_table_name = table_name

# EMAIL
email_from = config.EMAIL_ADDRESS_REPORT
email_password = config.PASSWORD
# email_to = config.EMAIL_ADDRESS1_REPORT+','+config.EMAIL_ADDRESS12_REPORT
email_to = config.EMAIL_ADDRESS12_REPORT
email_user = config.EMAIL_USER
email_host = config.EMAIL_HOST
subject = 'No ECAM Found_' + str(dt.now())
msg = MIMEMultipart()
msg['From'] = email_from
msg['To'] = email_to
msg['Subject'] = subject
body = 'There is NO EcamSecure found in this image. Please find attached document for more information!'
msg.attach(MIMEText(body, 'plain'))


def init_email(file):
    file_name = file
    attachment = open(file_name, 'rb')

    part = MIMEBase('application', 'octet-stream')
    part.set_payload(attachment.read())
    encoders.encode_base64(part)
    part.add_header('Content-Disposition', "attachment; filename= " + file_name)

    msg.attach(part)
    text = msg.as_string()

    return text


def send_email(email_from, email_to, emailText):
    try:

        server = smtplib.SMTP(email_host, 2525)
        server.starttls()
        server.login(email_user, email_password)
        server.sendmail(email_from, email_to.split(','), emailText)
        server.quit()
        print("Success: email has sent!!")
    except:
        print("Email failed to send..")


# INSERT INTO MYSQL DATA BASE
def insert_MYSQL(val, is_logo):
    file = open(config.automate_python_path + 'key.key', 'rb')
    key = file.read()
    file.close()
    f = Fernet(key)
    host_value = str(f.decrypt(config.mysql_host))[2:-1]
    user_value = str(f.decrypt(config.mysql_user))[2:-1]
    passwd_value = str(f.decrypt(config.mysql_passwd))[2:-1]

    print("checking host value", host_value, user_value, passwd_value)

    try:

        mydb = mysql.connector.connect(

            host=host_value,
            user=user_value,
            port=int(config.mysql_port),
            passwd=passwd_value,
            database=config.mysql_database

        )
    except mysql.connector.Error as e:
        print("Error code:", e.errno)
        print("SQLSTATE value:", e.sqlstate)
        print("Error message:", e.msg)
        print("Error:", e)

    mycursor = mydb.cursor()
    sql = "INSERT INTO" + " " + insert_table_name + "(image_path,isService,image_text,Created_On) VALUES (%s,%s,%s,%s)"
    sql1 = """INSERT INTO alarms(image,type_of_exception,image_text,created_on,location,type_of_services,comments)
              VALUES (%s,%s,%s,%s," + '"' + insert_table_name + '"' + "," + '"' + service_name + '"' + ",'NULL')"""

    print("checking the flag...", is_logo)
    if is_logo == 'True':
        print(Logo + " insertion")
        mycursor.execute(sql, val)
    else:
        print("non_" + Logo + "insertion")
        mycursor.execute(sql1, val)
    mydb.commit()
    print(mycursor.rowcount, "record inserted into MYSQL Database.")


time.sleep(5)

fileNames = os.listdir(source)
os.chdir(source)

print('number of files read:' + str(len(fileNames)))
if (len(fileNames) > 10):
    notify_text = ""
    notify_text = "There are more number of files in the folder which are not processed"
    send_email(email_from, email_to, notify_text)

fileNames1 = []
duplicateImages = []
fileNames.append('dummy')
print("checking/ the file length .....", len(fileNames))
for i in range(0, len(fileNames) - 1):

    if fileNames[i].endswith('.jpg'):
        if fileNames[i][16:32] == fileNames[i + 1][16:32]:
            print('This image is duplicate > ' + fileNames[i])
            duplicateImages.append(fileNames[i])
        else:
            if os.path.exists(sourceBkp + fileNames[i]):
                os.remove(source + fileNames[i])
            else:
                fileNames1.append(fileNames[i])


def get_timestamp(file_name):
    f1 = file_name.split("_")[-2]
    return f1[8:16]


sorted_list = sorted(fileNames1, key=get_timestamp)
print("checking sorted list..", len(sorted_list))

x = 0
sorted1 = []
for file1 in sorted_list:
    x = x + 1
    sorted1.append(file1)
    if x == 10: break

print("sorted list for processing", sorted1)

x = 0
selected_files = []
for filename in sorted1:
    x = x + 1
    print(x)
    if x == 11: break

is_logo = False
is_date = False
data_to_insert_in_db = []

print("selected sorted files before processing", sorted1)
for file in sorted1:
    print('file' + file)
    if len(sorted1) < 1:
        print(' Number of sorted files:' + str(len(sorted1)))
    else:
        try:
            text_from_logo = azure_detec_text(file, source)
            print("text_from_logo......", text_from_logo)
        except:
            print("if exception happened")
            print("checking the error file", file)
            except_value = ()
            except_value = file,
            except_value = except_value + ("bad data file in " + Logo, "",)
            insert_MYSQL(except_value, is_logo)
            exception_emailText = ''
            exception_emailText = init_email(file)
            # send_email(email_from,email_to,exception_emailText)
            shutil.move(file, sourceBkp)
            sys.exit()

        if (any(re.findall(checking_regulerex, text_from_logo, re.IGNORECASE))):
            print('possible' + Logo + 'matches found in Azure Cognitive service API......')
            is_logo = True
            print("in " + Logo + " loop ......", is_logo)
        else:
            is_logo = False
            print("permenant loop checking .....")
        res = file + '|is_logo:' + str(is_logo) + '|text_from_logo' + text_from_logo
        print('res:' + res)
        data_to_insert_in_db.append(res)
        print("data insertion checking after loop", data_to_insert_in_db)

tempval = ()
is_logo_found = ''
print("data insertion into db", data_to_insert_in_db)
for file in data_to_insert_in_db:
    filename = file.split('|is_logo:')[0]
    print('File Name >>>>> ' + filename)
    print("checking file index.....", file)
    is_logo = file.split('|is_logo:')[1].split('|')[0]
    print("is_logo after changing ....", is_logo)
    image_text = file.split('|text_from_logo')[1]
    print('image_text', image_text)
    tempval = sourceBkp.split('/')[-2] + "/" + filename + "",

    created_file_date = time.ctime(os.path.getctime(filename))
    created_file_date = created_file_date[4:]
    print("checking", created_file_date)
    final_date_insertion_db = dt.strptime(created_file_date, '%b  %d %H:%M:%S %Y')

    print("process created date", final_date_insertion_db)

    if is_logo == 'True':
        is_logo_found = Logo + ' Found'
    else:
        is_logo_found = Logo + ' not Found'

    if is_logo == 'False':
        print(is_logo_found)
        emailText = ''
        emailText = init_email(filename)
        # send_email(email_from,email_to,emailText)

    val = tempval + (is_logo_found, image_text, final_date_insertion_db,)
    print(val)
    insert_MYSQL(val, is_logo)

    shutil.move(filename, sourceBkp)

end = dt.now()
diff = end - start
print('Current unit of work has processed in ' + str(diff.seconds) + 's')
