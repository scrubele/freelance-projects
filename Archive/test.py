import argparse
import logging
import os
import re
import shutil
import smtplib
import sys
from copy import deepcopy
from datetime import datetime as dt, time
from email import encoders
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

import mysql.connector
import mysql.connector
from cryptography.fernet import Fernet

# from Extracttext_from_logo2 import *

# args = None
# logger = None

START_TIME = dt.now()
LOGO = "bmw"
SERVICE_NAME = "logodetection"
REGEX_TO_FIND = "bmw"

# SOURCE=config.inbound_GHB_path

# These values coming from the bash file:
SOURCE = sys.argv[1]
SOURCE_BKP = sys.argv[2]
INSERT_TABLE_NAME = "{}".format(sys.argv[3])


def setup_argument_parser():
    parser = argparse.ArgumentParser(prog=__name__)
    parser.add_argument('--verbose', '-v', default=0, action='count')
    # parser.add_argument('--env_vars', '-e', nargs='+', help='<Required> Set flag', required=True)
    # parser.add_argument('--EMAIL_ADDRESS_REPORT', action='store')
    # parser.add_argument('--inbound_GHB_path', action='store')
    # parser.add_argument('--EMAIL_ADDRESS12_REPORT', action='store')
    # parser.add_argument('--PASSWORD', action='store',  required=False)
    # parser.add_argument('--EMAIL_USER', action='store')
    # parser.add_argument('--EMAIL_HOST', action='store')
    # parser.add_argument('--AUTOMATE_PYTHON_PATH', action='store')
    # parser.add_argument('--MYSQL_HOST', action='store')
    # parser.add_argument('--MYSQL_DATABASE', action='store')
    # parser.add_argument('--MYSQL_PORT', action='store')
    # parser.add_argument('--MYSQL_USER', action='store')
    # parser.add_argument('--MYSQL_PASSWORD', action='store')

    # parser.add_argument('--output', '-o', choices=['console', 'sqlserver'], default='console',
    #                     help='Output of the report')
    # parser.add_argument('--profiles', default='default',
    #                     help="AWS credentials/configuration profile to use (coma separated)")
    # parser.add_argument('reports', nargs='+', choices=['eip', 'elb'], help='The report to run')
    global args
    args = parser.parse_args()


def setup_global_env_vars():
    pass


def setup_logger(level=logging.INFO):
    """
    The function for the logger initialization.
    :level - logger level, can be DEBUG, INFO, etc.
    :return: None
    """
    global logger
    extra = {'__name__': 'Super App'}

    logger = logging.getLogger(__name__)
    syslog = logging.StreamHandler()
    formatter = logging.Formatter('%(asctime)s %(__name__)s : %(message)s')
    syslog.setFormatter(formatter)
    levels = [logging.WARNING, logging.INFO, logging.DEBUG]
    level = levels[min(len(levels) - 1, args.verbose)]  # capped to number of levels
    logger.setLevel(level)
    logger.addHandler(syslog)

    logger = logging.LoggerAdapter(logger, extra)
    logger.debug("a debug message")
    logger.info("a info message")
    logger.warning("a warning message")


def create_an_email(config):
    """
    The function for creating email body
    :param config - args or config file
    :return:
        - email_host
        - email_from
        - email_password
        - email_user
        - email_password
        - msg - an email message (MIMEMultipart object)
    """
    email_host = config.EMAIL_HOST
    email_from = config.EMAIL_ADDRESS_REPORT
    email_to = config.EMAIL_ADDRESS12_REPORT
    email_user = config.EMAIL_USER
    email_password = config.PASSWORD
    msg = MIMEMultipart()
    msg['From'] = email_from
    msg['To'] = email_to
    msg['Subject'] = 'No ECAM Found_' + str(dt.now())
    body = 'There is NO EcamSecure found in this image. Please find attached document for more information!'
    msg.attach(MIMEText(body, 'plain'))
    return email_host, email_from, email_to, email_password, email_user, email_password, msg


def pr1():
    print('hey')
    logger.info('hey')
    print('no')


def init_email(file_name):
    """
    The function for creating the email message.
    :param file_name - the file name;
    :return:
    - msg_text - the text of the email message.
    """
    attachment = open(file_name, 'rb')
    msg_part = MIMEBase('application', 'octet-stream')
    msg_part.set_payload(attachment.read())
    encoders.encode_base64(msg_part)
    msg_part.add_header('Content-Disposition', "attachment; filename= " + file_name)
    msg.attach(msg_part)
    msg_text = msg.as_string()
    return msg_text


def send_email(email_from, email_to, emailText):
    try:
        server = smtplib.SMTP(email_host, 2525)
        server.START_TIMEtls()
        server.login(email_user, email_password)
        server.sendmail(email_from, email_to.split(','), emailText)
        server.quit()
        logger.info("Success: email has sent!!")
    except:
        logger.info("Email failed to send..")


def connect_to_MYSQL_db():
    """
        The function for connecting to MySQL database using keys.
    :return:
    """
    key_file = open(args.AUTOMATE_PYTHON_PATH + 'key.key', 'rb')
    key = key_file.read()
    key_file.close()
    fernet = Fernet(key)
    host_value = str(fernet.decrypt(args.MYSQL_HOST))[2:-1]
    user_value = str(fernet.decrypt(args.MYSQL_USER))[2:-1]
    password_value = str(fernet.decrypt(args.MYSQL_PASSWORD))[2:-1]
    logger.info(f"checking host value {host_value} {user_value} {password_value}")

    try:
        database = mysql.connector.connect(
            host=host_value,
            user=user_value,
            port=int(args.MYSQL_PORT),
            passwd=password_value,
            database=args.MYSQL_DATABASE
        )
    except mysql.connector.Error as db_connector:
        logger.info(f"Error code: {db_connector.errno}")
        logger.info(f"SQLSTATE value: {db_connector.sqlstate}")
        logger.info(f"Error message: {db_connector.msg}")
        logger.info(f"Error: {db_connector}")
    return database


def insert_into_MYSQL_DB(value, is_logo):
    """
    The function for the inserting data into MySQL database.
    :param value:
    :param is_logo:
    """
    database = connect_to_MYSQL_db()
    db_cursor = database.cursor()
    insert_into_table_query = f"INSERT INTO {INSERT_TABLE_NAME} (image_path,isService,image_text,Created_On) VALUES (%s,%s,%s,%s)"
    insert_into_alarms_query = f'''INSERT INTO alarms(image,type_of_exception,image_text,created_on,location,type_of_services,comments) 
                VALUES (%s,%s,%s,%s, "{INSERT_TABLE_NAME} ","{SERVICE_NAME}",'NULL')'''
    logger.info(f"checking the flag...{is_logo}")
    if is_logo == 'True':
        logger.info(f"{LOGO} insertion")
        db_cursor.execute(insert_into_table_query, value)
    else:
        logger.info(f"non_ {LOGO} insertion")
        db_cursor.execute(insert_into_alarms_query, value)
    database.commit()
    logger.info(f"{db_cursor.rowcount} record inserted into MYSQL Database.")


def get_timestamp(file_name):
    f1 = file_name.split("_")[-2]
    return f1[8:16]


def get_source_files():
    source_files = os.listdir(SOURCE)
    os.chdir(SOURCE)
    logger.info(f"number of files read: {len(source_files)}")
    return source_files


def check_number_of_source_files(source_files, max_file_number):
    """
        The function for checking if number of files in the source is greater than max file number.
    """
    if len(source_files) > max_file_number:
        notify_text = "There are more number of files in the folder which are not processed"
        send_email(email_from, email_to, notify_text)


def select_jpg_files(source_files):
    """
        The function for choosing unique JPG files that don't exist in sourceBkp folder.
    """
    image_file_names = []
    duplicate_images = []
    source_files.append('dummy')
    logger.info(f"checking/ the file length .....{len(source_files)}")
    for i in range(0, len(source_files) - 1):
        if source_files[i].endswith('.jpg'):
            if source_files[i][16:32] == source_files[i + 1][16:32]:
                logger.info(f"This image is duplicate > {source_files[i]}")
                duplicate_images.append(source_files[i])
            else:
                if os.path.exists(SOURCE_BKP + source_files[i]):
                    os.remove(SOURCE + source_files[i])
                else:
                    image_file_names.append(source_files[i])

    image_sorted_list = sorted(image_file_names, key=get_timestamp)
    logger.info(f"checking sorted list..{len(image_sorted_list)}")
    return image_sorted_list


def select_the_first_n_files(image_sorted_list, number_to_select):
    # x = 0
    # selected_sorted_files = []
    # for file1 in image_sorted_list:
    #     x = x + 1
    #     selected_sorted_files.append(file1)
    #     if x == 10: break
    #
    # print("sorted list for processing", selected_sorted_files)
    #
    # x = 0
    # selected_files = []
    # for filename in selected_sorted_files:
    #     x = x + 1
    #     print(x)
    #     if x == 11: break
    selected_sorted_files = deepcopy(image_sorted_list)[0:number_to_select]
    logger.info(f"selected sorted files before processing {selected_sorted_files}")
    return selected_sorted_files


def extract_text_from_logo(selected_file, is_logo):
    text_from_logo = ""
    try:
        text_from_logo = azure_detec_text(selected_file, SOURCE)
        logger.info(f"text_from_logo......{text_from_logo}")

    except Exception as e:
        logger.info("if exception happened")
        logger.info(f"checking the error file {selected_file}")
        except_value = selected_file,
        except_value = except_value + ("bad data file in " + LOGO, "",)
        insert_into_MYSQL_DB(except_value, is_logo)
        exception_email_text = init_email(selected_file)
        send_email(email_from, email_to, exception_email_text)
        shutil.move(selected_file, SOURCE_BKP)
        sys.exit()
    return text_from_logo


def form_the_data_for_insertion(selected_sorted_files):
    is_logo = False
    data_to_insert_in_db = []

    for selected_file in selected_sorted_files:
        logger.info(f"file {selected_file}")
        if len(selected_sorted_files) < 1:
            logger.info(f"Number of sorted files: {len(selected_sorted_files)}")
        else:
            text_from_logo = extract_text_from_logo(selected_file, is_logo)
            if any(re.findall(REGEX_TO_FIND, text_from_logo, re.IGNORECASE)):
                is_logo = True
                logger.info(f"possible {LOGO} matches found in Azure Cognitive service API......")
                logger.info(f"in {LOGO}  loop ...... {is_logo}")
            else:
                is_logo = False
                logger.info("permanent loop checking .....")
            res = selected_file + '|is_logo:' + str(is_logo) + '|text_from_logo' + text_from_logo
            logger.info(f"res: {res}")
            data_to_insert_in_db.append(res)
            logger.info(f"data insertion checking after loop {data_to_insert_in_db}")
    return data_to_insert_in_db


def insert_data_into_db(data_to_insert_in_db):
    file_path = ()
    is_logo_found = ''
    logger.info(f"data insertion into db {data_to_insert_in_db}")
    for file in data_to_insert_in_db:
        filename = file.split('|is_logo:')[0]
        logger.info(f"File Name >>>>> {filename}")
        logger.info(f"checking file index.....{file}")

        is_logo = file.split('|is_logo:')[1].split('|')[0]
        logger.info(f"is_logo after changing .... {is_logo}")

        image_text = file.split('|text_from_logo')[1]
        logger.info(f"image_text {image_text}")

        file_path = SOURCE_BKP.split('/')[-2] + "/" + filename + "",
        created_file_date = time.ctime(os.path.getctime(filename))
        created_file_date = created_file_date[4:]
        logger.info(f"checking {created_file_date}")
        final_date_insertion_db = dt.strptime(created_file_date, '%b  %d %H:%M:%S %Y')

        logger.info(f"process created date {final_date_insertion_db}")

        if is_logo == 'True':
            is_logo_found = LOGO + ' Found'
        # else:
        #     is_logo_found = LOGO + ' not Found'
        elif is_logo == 'False':
            logger.info(is_logo_found)
            email_text = init_email(filename)
            send_email(email_from, email_to, email_text)

        data_to_insert = file_path + (is_logo_found, image_text, final_date_insertion_db,)
        logger.info(data_to_insert)
        insert_into_MYSQL_DB(data_to_insert, is_logo)

        shutil.move(filename, SOURCE_BKP)


def display_execution_time():
    end = dt.now()
    diff = end - START_TIME
    logger.info(f"Current unit of work has processed in {diff.seconds}s")


def setup_env():
    setup_argument_parser()
    setup_logger()
    setup_global_env_vars()
    pr1()


def main():
    setup_env()
    global email_host, email_from, email_to, email_password, email_user, email_password, msg
    email_host, email_from, email_to, email_password, email_user, email_password, msg = create_an_email(args)
    print(email_host)
    time.sleep(5)

    max_file_number = 10
    source_files = get_source_files()
    check_number_of_source_files(max_file_number)
    image_sorted_list = select_jpg_files(source_files)
    selected_sorted_files = select_the_first_n_files(image_sorted_list, max_file_number)
    data_to_insert_in_db = form_the_data_for_insertion(selected_sorted_files)
    insert_data_into_db(data_to_insert_in_db)
    display_execution_time()


if __name__ == "__main__":
    main()
