from collections import defaultdict
import types
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import logging

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
ch = logging.StreamHandler()
ch.setLevel(logging.INFO)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
ch.setFormatter(formatter)

logger.addHandler(ch)


def list2htmltable(input, colname=None, colval=None, color='#FF0000', header_color='#003366'):
    """
    This was taken from ctp_python.legacy.tradeops.ctp_email
    
    Takes a list and converts to html table, table header default color is blue.
    Row colors can be changed based on column name and value in row
    """
    out = '<table border="1", cellpadding="5">'
    header = input[0]
    headerindex = None
    if colname:
        headerindex = header.index(colname) if colname in header else None
    for i, row in enumerate(input):
        out+="<tr>"
        bgcolor = "#FFFFFF"
        tag='td'
        if headerindex is not None and row[headerindex] == colval:
            bgcolor = color
            tag='td'
            if i == 0:
                tag = 'th'
            # HEADER COLOR
            bgcolor = header_color
        for j, c in enumerate(row):
            thiscell = "<{tag} bgcolor={bgcolor}>"+str(c)+"</{tag}>"
            out += thiscell.format(bgcolor=bgcolor,tag=tag)
            out+="</tr>\n"
            out+="</table>"
    return out


class GDriveMadrasaDatabase(object):
    def __init__(self):
        # use creds to create a client to interact with the Google Drive API
        self.scope = ['https://spreadsheets.google.com/feeds']
        self.creds = ServiceAccountCredentials.from_json_keyfile_name(
            '/Users/safraz/django_projects/website/madrasa/madrasa_db_secret.json', self.scope)
        self.client = gspread.authorize(self.creds)

        # Find a workbook by name and open the first sheet
        # Make sure you use the right name here.
        self.sheet = self.client.open("TEST_MADRASA_DATABASE").sheet1

        # Extract and print all of the values
        self.list_of_rows = self.sheet.get_all_records()
        self.user_by_id = {}
        self.ids_by_class = defaultdict(lambda:[])
        self.ids_quicbooks_id = defaultdict(lambda: [])
        self.ids_gender = defaultdict(lambda: [])
        self.ids_by_alerts = defaultdict()
        self.allergy_list = defaultdict()
        logger.info("Starting")
        self._load_data()

        self._student_fields = ['ID', 'FIRST_NAME', 'LAST_NAME', 'DOB', 'GENDER', 'CLASS']


    def _Authorize(self):
        pass

    def _load_data(self):
        for row in self.list_of_rows:
            student_id = row.get('ID')
            student_class = row.get('CLASS').lower() if type(row.get('CLASS')) == types.StringType else row.get('CLASS')
            logger.info('Adding ID: {} --> {} {} Class --> {}'.format(student_id, row.get('FIRST_NAME'), row.get('LAST_NAME'), student_class))
            self.user_by_id[student_id] = row
            self.ids_by_class[student_class].append(student_id)

            logger.info('Checking for Alerts for {}'.format(student_id))
            if len(row.get('alert').lower()) > 0:
                alert_msg = row.get('alert_msg')
                logger.info('Found Alert for {}, MSG: {}'.format(student_id, alert_msg))
                self.ids_by_alerts[student_id] = row.get('alert_msg')

    def get_students_infos(self, student_ids):
        students_infos = []
        for student_id in student_ids:
            student_info = []
            student = self.user_by_id.get(student_id)
            for fld  in self._student_fields:
                student_info.append(student.get(fld))

            students_infos.append(student_info)

        return list2htmltable([students_infos])


if __name__ == '__main__':
    x = GDriveMadrasaDatabase()
    x.run()

