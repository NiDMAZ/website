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
        key_file_dict = {
          "type": "service_account",
          "project_id": "madrasa-db",
          "private_key_id": "b695cb15364b5b77af0acdb41d7dc6a4589f7262",
          "private_key": "-----BEGIN PRIVATE KEY-----\nMIIEvQIBADANBgkqhkiG9w0BAQEFAASCBKcwggSjAgEAAoIBAQCxy1cd/CHAo5bl\no659GECYKtgtLvye1Xb4qq7iCUuqKqmp/SWV/Elui3Byek4RPjyO0vx5lt1NS48e\nNjPdAc+Y8zIqA3UZpH6h6G61mR+mKr0x9OUYxiDGK7PSEA3peFuLkWrt6HdNMnvN\n1hjX9lvJYlnGAdEUJ2+sxh94oyVf2EpoDxq9VPxTRuVfaPL3SP2m8b1EHxwyru9R\neCukVXhO/fXrSWl6FS/SWPhbc3Sw8kzWbLkDG1EWvnqGrQQI32YmsyAobtDd5hj4\nv4CEELIGztNL6UTaAfh+wGeLZ5WkpP+/I3T0JarfWjPEK3+Pil9cgOzFCP0H6dPZ\nuDI/VaLlAgMBAAECggEARF1b8juw/tHohAScY52fuONAnJ8kpC6QwK1g8amBXr1o\n3+RnP3TzB362jk5ZFmhIAONAEcDg94fGUGenKaQ4nydkcqNBs8p8puUpLMrkUJC+\njycLsKr+jzTewDdMIioViWUxKKnqtdRjppJcmy4vvRAEVQ79xjIjztuf3lNdW6y6\n5NZb7begymCK4PUuYAQtmDunRhhFjs4VaKdUCelTBnbyyD1gGliGv3cFmfZ3gVDs\nNnfPyV4+RPndlyJKJ4hiejJAK2RoVrxCWacB+0BNEgqgzHPmNx6E9f85k1b1Ulma\nWC/M1D5Zi+JFiTEjg+2LI9zbuLUCx20Wr4Nz9bLkAQKBgQDmJ2sO1Un4eye3WsvP\n1xabcmpzXPvnRpLfR1hoimXZLOxFEue3BcEzoJJFjM0j5X2UGdzMsPc7puWavipD\nHHxUWmY//TF4wLTHlaTggf88ONFPSyBivKJZ1RS1VQENP8VF7lmNsI9WS2udzK4k\nQJlFI3FyYVoYe/bmGoLKPZtYdQKBgQDFwqjqOCOS29i/JpWBLvZEqNAciVtTu6LD\n5wx0GCzEhPRW+BNEqWQQwXvg9V/CKxsv9zK5bxfQz/zukG+PkvbhAopfdh+5XLLu\nql0l6vbhtQsj3sQke0X6c6o81TJFAg+LzHWoKFRcmdNtYL9hmI/AKWAaG/7oe9ve\nA9wi/zhSsQKBgEif16BunVDTS80H0Zhb/r4+dGjCxppMIrxh/vu98DV/f26scIHI\nRxbLbFyV+YWCPQYmww20Kc+g8oLJzvwuWO0lOW6nrpyz8leoWMafPrL6GtIymp2N\neI1wN4Cguhw8KzvN4mRbel94nRTGKY029SZj8MBvB8cCFv61DuBSYFqhAoGAbD+G\nOFasWjnOpasYENNE6AZDjCs/e1Ds4jC5Z17IOnXQTT6TRXU3Gdje1x9Y4C66PgIg\nmNIPhjQi7e7PshYu3rGGToSZDtyH8Q392MCJjLiNtX+9e36iqlnfqFbGonFjUxGC\noZ4Zt2pYCbn4aBKbNQMw4HnMiTMrAZa5S8rJ6LECgYEA2QAAPvY75B9ImnNHQT3X\nO7JZbWDZDkL+h2JJroN6sLfhg7yIaHQWgGPh23uLRP4DCFZm97/eprihi2jXKH4d\nMX7aKROIQKd/FooNM4bapSMOWLD0oyukNE2g+jwa9Zg7zU6oXPeoMRjzdTMaXC21\nphTdiBZDa/eS7UTWJqTSbhQ=\n-----END PRIVATE KEY-----\n",
          "client_email": "svc-madrasa@madrasa-db.iam.gserviceaccount.com",
          "client_id": "104966790381434740549",
          "auth_uri": "https://accounts.google.com/o/oauth2/auth",
          "token_uri": "https://accounts.google.com/o/oauth2/token",
          "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
          "client_x509_cert_url": "https://www.googleapis.com/robot/v1/metadata/x509/svc-madrasa%40madrasa-db.iam.gserviceaccount.com"
        }

        # use creds to create a client to interact with the Google Drive API
        self.scope = ['https://spreadsheets.google.com/feeds']
        self.creds = ServiceAccountCredentials.from_json_keyfile_dict(key_file_dict, self.scope)
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

