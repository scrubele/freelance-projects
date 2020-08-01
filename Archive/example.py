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
from cryptography.fernet import Fernet

# sourse in config.py
import config

start = dt.now()

Logo = "bmw"
#
# source=config.Inbound_some_path
# this is value coming from the bash file
source = sys.argv[1]
sourceBkp = sys.argv[2]
service_name = "logodetection"
checking_regulerex = "ibm"
table_name = "{}".format(sys.argv[3])
insert_table_name = table_name

# EMAIL
email_From = config.EMAIL_ADDRESS_REPORT
email_password = config.PASSWORD
# email_To = config.EMAIL_ADDRESS1_REPORT+','+config.EMAIL_ADDRESS12_REPORT
email_To = config.EMAIL_ADDRESS12_REPORT
email_user = config.EMAIL_USER
email_host = config.EMAIL_HOST
subject = 'No ECAM Found_' + str(dt.now())
msg = MIMEMultipart()
msg['From'] = email_From
msg['To'] = email_To
msg['Subject'] = subject
body = 'There is NO EcamSecure found in this image. Please find attached document for more information!'
msg.attach(MIMEText(body, 'plain'))


def init_email(file):
    filename = file
    attachment = open(filename, 'rb')

    part = MIMEBase('application', 'octet-stream')
    part.set_payload((attachment).read())
    encoders.encode_base64(part)
    part.add_header('Content-Disposition', "attachment; filename= " + filename)

    msg.attach(part)
    text = msg.as_string()

    return text


def send_email(email_From, email_To, emailText):
    try:

        server = smtplib.SMTP(email_host, 2525)
        server.starttls()
        server.login(email_user, email_password)
        server.sendmail(email_From, email_To.split(','), emailText)
        server.quit()
        print("Success: email has sent!!")
    except:
        print("Email failed to send..")


# INSERT INTO MYSQL DATA BASE
def insert_MYSQL(val, isLogo):
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
    sql1 = "INSERT INTO alarms(image,type_of_exception,image_text,created_on,location,type_of_services,comments) VALUES (%s,%s,%s,%s," + '"' + insert_table_name + '"' + "," + '"' + service_name + '"' + ",'NULL')"
    print("checking the flag...", isLogo)
    if (isLogo == 'True'):
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
    notifyText = ""
    notifyText = "There are more number of files in the folder which are not processed"
    send_email(email_From, email_To, notifyText)

fileNames1 = []
duplicateImages = []
fileNames.append('dummy')
print("checking/ the file length .....", len(fileNames))
for i in range(0, len(fileNames) - 1):

    if (fileNames[i].endswith('.jpg')):
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
    if (x == 10): break

print("sorted list for processing", sorted1)

x = 0
SelectedFiles = []
for filename in sorted1:
    x = x + 1
    print(x)
    if (x == 11): break

isLogo = False
isDate = False
DatatoinsertinDB = []

print("selected sorted files before processing", sorted1)
for file in sorted1:
    print('file' + file)
    if (len(sorted1) < 1):
        print(' Number of sorted files:' + str(len(sorted1)))
    else:
        try:
            textfromLogo = azure_detec_text(file, source)
            print("textfromlogo......", textfromLogo)
        except:
            print("if exception happened")
            print("checking the error file", file)
            except_value = ()
            except_value = file,
            except_value = except_value + ("bad data file in " + Logo, "",)
            insert_MYSQL(except_value, isLogo)
            exception_emailText = ''
            exception_emailText = init_email(file)
            # send_email(email_From,email_To,exception_emailText)
            shutil.move(file, sourceBkp)
            sys.exit()

        if (any(re.findall(checking_regulerex, textfromLogo, re.IGNORECASE))):
            print('possible' + Logo + 'matches found in Azure Cognitive service API......')
            isLogo = True
            print("in " + Logo + " loop ......", isLogo)
        else:
            isLogo = False
            print("permenant loop checking .....")
        res = file + '|isLogo:' + str(isLogo) + '|textfromLogo' + textfromLogo
        print('res:' + res)
        DatatoinsertinDB.append(res)
        print("data insertion checking after loop", DatatoinsertinDB)

tempval = ()
isLogoFound = ''
print("data insertion into db", DatatoinsertinDB)
for file in DatatoinsertinDB:
    filename = file.split('|isLogo:')[0]
    print('File Name >>>>> ' + filename)
    print("checking file index.....", file)
    isLogo = file.split('|isLogo:')[1].split('|')[0]
    print("isLogo after changing ....", isLogo)
    image_text = file.split('|textfromLogo')[1]
    print('image_text', image_text)
    tempval = sourceBkp.split('/')[-2] + "/" + filename + "",

    created_file_date = time.ctime(os.path.getctime(filename))
    created_file_date = created_file_date[4:]
    print("checking", created_file_date)
    final_date_insertion_db = dt.strptime(created_file_date, '%b  %d %H:%M:%S %Y')

    print("process created date", final_date_insertion_db)

    if (isLogo == 'True'):
        isLogoFound = Logo + ' Found'
    else:
        isLogoFound = Logo + ' not Found'

    if (isLogo == 'False'):
        print(isLogoFound)
        emailText = ''
        emailText = init_email(filename)
        # send_email(email_From,email_To,emailText)

    val = tempval + (isLogoFound, image_text, final_date_insertion_db,)
    print(val)
    insert_MYSQL(val, isLogo)

    shutil.move(filename, sourceBkp)

end = dt.now()
diff = end - start
print('Current unit of work has processed in ' + str(diff.seconds) + 's')

пример
# encoding: utf-8
"""
AWS Reports
"""
import argparse
import logging
import logging.config

from vigoutilities.lib import config, logging as vigo_loging
from aws_reports import
from aws_reports.io.in_aws import AWSInput
from aws_reports.io.out_console import OutputConsole
from aws_reports.io.out_sqlserver import OutputSqlServer

set_logger = logging.getLogger(APP_NAME)
try:
    vigo_loging.base_logger_conf(set_logger, APP_NAME)
    logger = vigo_loging.LoggerProxy(set_logger, {'app_name': APP_NAME})
except config.KeyNotFoundError:
    set_logger.error('Unable to load logging level from configuration. Falling back to default configuration.')
    logger = set_logger
    ch = logging.StreamHandler()
    ch.setFormatter(logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s'))
    logger.addHandler(ch)


def main():
    """
    Entrypoint of the command line tool
    :return: Nothing
    """
    parser = argparse.ArgumentParser(prog=APP_NAME)
    parser.add_argument('--verbose', '-v', default=0, action='count')
    parser.add_argument('--output', '-o', choices=['console', 'sqlserver'], default='console',
                        help='Output of the report')
    parser.add_argument('--profiles', default='default',
                        help="AWS credentials/configuration profile to use (coma separated)")
    parser.add_argument('reports', nargs='+', choices=['eip', 'elb'], help='The report to run')
    args = parser.parse_args()

    if args.verbose >= 3:
        set_logger.setLevel(1)
    elif args.verbose == 2:
        set_logger.setLevel(logging.DEBUG)
    elif args.verbose == 1:
        set_logger.setLevel(logging.INFO)

    # Create the output selected
    output = None
    if args.output == 'console':
        output = OutputConsole(config)
    elif args.output == 'sqlserver':
        output = OutputSqlServer(config)
    else:
        logger.error('No output selected. Exiting.')
        exit(1)
    output.start_job()

    logger.debug('Requested reports: %s', args.reports)
    logger.debug('Specified profiles: %s', args.profiles)
    profiles = args.profiles.split(',')

    aws_input = AWSInput(config)

    if 'eip' in args.reports:
        logger.debug('Running EPI report...')
        output.write_report(aws_input.get_all_eip(profiles), 'AWSEIPs')

    if 'elb' in args.reports:
        logger.debug('Running ELB report...')
        output.write_report(aws_input.get_all_elb_dns_names(profiles), 'AWSELBs')

    output.end_job()


if __name__ == "__main__":
    main()
