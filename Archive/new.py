import logging
import argparse

extra = {'__name__':'Super App'}

logger = logging.getLogger(__name__)
syslog = logging.StreamHandler()
formatter = logging.Formatter('%(asctime)s %(__name__)s : %(message)s')
syslog.setFormatter(formatter)
logger.setLevel(logging.INFO)
logger.addHandler(syslog)

logger = logging.LoggerAdapter(logger, extra)
logger.info('The sky is so blue')
logger.info(f"checking host value {1} {2} {3}")
sql1 = f'''INSERT INTO alarms(image,type_of_exception,image_text,created_on,location,type_of_services,comments) 
            VALUES (%s,%s,%s,%s, "{ 1} ","{2}",'NULL')'''
print(sql1)

try:
    x=1
except:
    print('hi')
print(x)

# parser = argparse.ArgumentParser()
# parser.add_argument('-v', '--verbose', action='count', default=0)
# args = parser.parse_args()
#
# levels = [logging.WARNING, logging.INFO, logging.DEBUG]
# level = levels[min(len(levels)-1, args.verbose)]  # capped to number of levels
#
# logging.basicConfig(level=level,
#                     format="%(asctime)s %(levelname)s %(message)s")
#
# logging.debug("a debug message")
# logging.info("a info message")
# logging.warning("a warning message")