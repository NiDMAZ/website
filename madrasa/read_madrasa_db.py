from collections import defaultdict
import types
import os
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import logging
from .python_modules.formattors import HtmlTableCreator


logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
ch = logging.StreamHandler()
ch.setLevel(logging.INFO)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
ch.setFormatter(formatter)

logger.addHandler(ch)


class GDriveMadrasaDatabase(object):
    def __init__(self):
        # use creds to create a client to interact with the Google Drive API
        self.scope = ['https://spreadsheets.google.com/feeds']
        self.creds = ServiceAccountCredentials.from_json_keyfile_name(
            '{}'.format(os.path.join(os.getcwd(), 'madrasa/madrasa_db_secret.json')), self.scope)
        self.client = gspread.authorize(self.creds)

        # Find a workbook by name and open the first sheet
        # Make sure you use the right name here.
        self.sheet = self.client.open("MADRASA_DATABASE").sheet1

        # Extract and print all of the values
        self.list_of_rows = self.sheet.get_all_records()
        self.user_by_id = {}
        self.ids_by_class = defaultdict(lambda: [])
        self.ids_quicbooks_id = defaultdict(lambda: [])
        self.ids_gender = defaultdict(lambda: [])
        self.ids_by_alerts = defaultdict()
        self.allergy_list = defaultdict()
        logger.info("Starting")
        self._load_data()

        self._student_fields = ['ID',
                                'FIRST_NAME',
                                'LAST_NAME',
                                'DOB',
                                'GENDER',
                                'CLASS',
                                'ALLERGIES',
                                'STUDENT_EMAIL',
                                'alert',
                                'alert_msg']

    def _Authorize(self):
        pass

    def _load_data(self):
        for row in self.list_of_rows:
            student_id = row.get('ID')
            student_class = row.get('CLASS').lower() if type(row.get('CLASS')) == types.StringType else row.get('CLASS')
            logger.info(
                'Adding ID: {} --> {} {} Class --> {}'.format(student_id, row.get('FIRST_NAME'), row.get('LAST_NAME'),
                                                              student_class))
            self.user_by_id[student_id] = row
            self.ids_by_class[student_class].append(student_id)

            logger.info('Checking for Alerts for {}'.format(student_id))
            if len(row.get('alert').lower()) > 0:
                alert_msg = row.get('alert_msg')
                logger.info('Found Alert for {}, MSG: {}'.format(student_id, alert_msg))
                self.ids_by_alerts[student_id] = row.get('alert_msg')


    def _get_students_infos(self, student_ids=None):
        students_infos = []
        student_ids = student_ids if student_ids is not None else self.user_by_id.keys()
        for student_id in student_ids:
            student_info = []
            student = self.user_by_id.get(student_id)
            for fld in self._student_fields:
                student_info.append(student.get(fld))

            students_infos.append(student_info)
        return students_infos

    def get_students_infos(self, student_ids=None):
        student_infos = self._get_students_infos(student_ids=student_ids)
        html_table = HtmlTableCreator()
        html_table.add_header(self._student_fields)
        for i in student_infos:
            html_table.add_row(i)

        return html_table.get_html_table()

    def get_students_by_class(self, class_name):
        results = ""
        for class_n in [class_name]:
            results += "<h4>{}</h4>".format(class_n)
            results += self.get_students_infos(student_ids=self.ids_by_class.get(class_n.lower()))

        return results

