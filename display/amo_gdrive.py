import logging
import gspread
from oauth2client.service_account import ServiceAccountCredentials
from dateutil import parser as dateparser
import threading
import time
import datetime
from datetime import timedelta
from rw_lock import RWLock


logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
handler = logging.FileHandler('amo_gdrive.log')
handler.setLevel(logging.INFO)
formatter = logging.Formatter('[%(asctime)s] [%(name)s] [%(levelname)s] %(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)

def string_to_date(s):
    dt = dateparser.parse(s)
    if dt is not None:
        return dt.date()
    raise ValueError('{!r} is not a valid datetime'.format(s))


class GDriveAuthenticator(object):
  # BASE GOOGLE DRIVE AUTHENTICATOR
  # THIS IS A VERY BASIC ABSTRACT IMPLEMENTATION AND ALSO VERY LAZY SO USE AT YOUR OWN RISK

    def __init__(self, scope):
        super(GDriveAuthenticator,self).__init__()
        self.key_file_dict = {
          "type": "service_account",
          "project_id": "amo-website-project",
          "private_key_id": "45f9c052e36d8b5013c250a949ebde25f9045dc2",
          "private_key": "-----BEGIN PRIVATE KEY-----\nMIIEvAIBADANBgkqhkiG9w0BAQEFAASCBKYwggSiAgEAAoIBAQDAep55Al457eir\n6oOTmUBFOmpuyiypqHS4Nn0vuDFft36ONP/eM3D6FqnDyzmKnwWzwUz9XAGL9+bL\nyfVPkEKs2le5H0clh/ly96pxXjrSdOcZK2/mmBTQwgJgnY2zaBKnL0TCcZasTWiV\nNU2nFEQB07XSOHmyQyscSriM41123Drh6DSpPbGfWPt4jxjDyhDmuXNg3PQtJ60E\ndj8Zbvf7oe6lDN5VCruPAsU1EHjlj1RAph0vi00ZNPCowos69XvET4lQk9ufsG2o\nXZqgNdfAYHleVYClrXgNLwNuM3soqWluzQxSzF11G8jYowaLAKUTJt1c6Gw0mPR3\nuW9Hc72xAgMBAAECggEABF0fT8VlSR1PAqtIYIG3ZJ5nfHOoVbAaVdUT61+a3HV8\nuLkEQkeSqJPYFVabm0xByQaRUhbqeM+174G4ll1CGrjAR4PZVUUu+0uYxVVWYnA4\nr1AWG1FwOt+kJcg6psIttpU+cwVX3fgLDoNw61Bc/pjb+Nwzi55k2UFLK/QJadz4\nGYc9TkutTuHfsovdtNB1ZpY55oM8K/cp9d7DDHlq9uCBbfQLXW4TyGkxL05fsXOP\nE+GM5k+u1C0OypuxuUfezeXXU0npQqv9S44n3zNuIZaBOsA/JomjkIpOO3lq/m/Z\nfTgALiSdn+VvwnvVi+IlRshpKSl8C42QBnLy8T9hgQKBgQD1s2rxmbmNM+yUzUA+\n+aM716Nqj7cURZPYyz2eCOkbjFVC1uWZruSvZgPYLfE14nHXGxizdIRwFYmjP3Gv\nP8NUKUFQ2LhI3GWrUXYALgbgfMHOleB9DolPmhYvcxoKiFf9FcRPc9ZYnh3yt1t5\nuouKbSW1SfsrIerOzfJu+PUTMQKBgQDIjBWtBExgMjuYW6y1bPQ8rTMtHp1n3ZzS\nnPbIakNB8R6B7D7A2MVG+BQn20X8SEfxsaZ6EZdq1qedSQNEzmo7t9jYfNBExhIB\nA+uRYdEt8Y0PS58rD9a5uqeVGSvnFVsS5IgBu34LNnRnPR8ZKn4DsQgRoWxO/X2k\nnHuQnS2ygQKBgAMZt4DC+tdwT0z1ZhklV0z7BKHknF/SHPKAZg+ndyGU3MKSKaWN\n0m7wL547vi565Ard2aryDnXHn8wCkfGvMUzPlHZrta+dsF7AEWghLI8Ko/tyYrnR\nRCRQAnWo0yxM2idkbey+vnax0Bju/WWE2BvwEqi9/UBnFipz6NpDo/wRAoGAPYs/\n26jGB39i6o63obWd/kDow5/xjj5kMf4ZfceefE4SnqxxVZ0wbWcUSGbyQ0mrSnDK\nNgvP++mD5rDRX/w4fbsdwNIM2A4w2D7ru+HY39CRCXCbmAt0SesOIqNm5bOYD2Qy\nmNWBCM/dSRFoycBQi7F4WHDBXDxOooWjJe4WaAECgYBUiNuTM8508k8jqIL5zTpK\ndOaxPOOSn6D3dc4BggC8odWnne74BWDXdcblD3sBdOOXr/juGXo3Px5nfhd3eGNh\nUsVqVh1gX2/07ntLYEf6q8oVDmvEjXyO20QOCv0CyOOA+4/0WdO3hLRPba2Psizm\n8qQi/UPCnpbXKTPnt/Ff1g==\n-----END PRIVATE KEY-----\n",
          "client_email": "amo-website-service-account@amo-website-project.iam.gserviceaccount.com",
          "client_id": "102240974351321514362",
          "auth_uri": "https://accounts.google.com/o/oauth2/auth",
          "token_uri": "https://accounts.google.com/o/oauth2/token",
          "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
          "client_x509_cert_url": "https://www.googleapis.com/robot/v1/metadata/x509/amo-website-service-account%40amo-website-project.iam.gserviceaccount.com"
        }
        # use creds to create a client to interact with the Google Drive API
        self.scope = scope
        self.creds = ServiceAccountCredentials.from_json_keyfile_dict(self.key_file_dict, self.scope)
        self.client = gspread.authorize(self.creds)


class GSheetReader(GDriveAuthenticator):
    def __init__(self, sheet_name):
        super(GSheetReader, self).__init__(['https://spreadsheets.google.com/feeds'])
        self._sheet_name = sheet_name
        self.sheet = self.client.open(self._sheet_name)

    def get_all_hashes(self, index_number):
        return self.sheet.get_worksheet(index=index_number).get_all_records()


class JummahKhateebUpdator(GSheetReader):
    def __init__(self, refresh_interval=60):
        self.refresh_interval = refresh_interval
        super(self.__class__, self).__init__(sheet_name='jummah_khateeb')
        self._set_lock = RWLock()
        self._cache = dict()
        logger.info('**** Starting Jummah Khateeb Updator ****')
        logger.info('This will update every {} seconds'.format(self.refresh_interval))

    def get_jummah_date(self, date_time=datetime.datetime.now()):
        assert type(date_time) == datetime.datetime, "Only accepts {}, recieved {}".format(datetime.datetime,
                                                                                       type(date_time))
        if date_time.isoweekday() < 5:
          # print 'Its before Friday'
            return (date_time + timedelta(days=5 - date_time.isoweekday())).date()
        elif date_time.isoweekday() > 5:
          # print 'Its after Friday'
            return (date_time + timedelta(days=(7 - date_time.isoweekday()) + 5)).date()
        elif date_time.isoweekday() == 5:
          # print 'Its Friday'
            if type(date_time) == datetime.datetime:
                if date_time.hour >= 14:
                    return self.get_jummah_date(date_time + timedelta(days=1))
                else:
                    return date_time.date()

    def update_cache(self):
        logger.info("Updating Cache")
        local_cache = dict()
        # TODO: Implement a proper locking here
        logger.info('Reading Google Sheet')
        for i in self.get_all_hashes(index_number=0):
            if len(i.get('KHATEEB')) > 0:
                # IGNORING EMPTY CELLS
                logger.info('{}:{}'.format(string_to_date(i.get('DATE')), i.get('KHATEEB').title()))
                local_cache.update({string_to_date(i.get('DATE')): i.get('KHATEEB').title()})

        with self._set_lock.write_lock():
            self._cache.clear()
            self._cache.update(local_cache)
            logger.info('cached updated')


    def _update_cache_thread(self):
        while True:
            logger.info('Update Cache Thread waking up')
            self.update_cache()
            logger.info('Will update cache at {}'.format(datetime.datetime.now() + timedelta(seconds=self.refresh_interval)))
            #logger.info('sleeping for {} seconds'.format(self.refresh_interval))
            time.sleep(self.refresh_interval)

    def run(self):
        try:
          update_cache_thread = threading.Thread(target=self._update_cache_thread, name='JummahKhateebUpdateCacheThread')
          update_cache_thread.setDaemon(True)
          update_cache_thread.start()

        except KeyboardInterrupt:
            logger.info('Killing JummahKhateebUpdator Thread')
            update_cache_thread.join(1)


    def get_this_week_khateeb(self):
        logger.info('Getting this weeks Khateeb')
        return self.get_khateeb_for_date()

    def get_khateeb_for_date(self, date=datetime.datetime.today()):
        with self._set_lock.read_lock():
            logger.info('Getting Khateeb for {}'.format(date))
            return {self.get_jummah_date(date): self._cache.get(self.get_jummah_date(date))}


JummahKhateebLookup = JummahKhateebUpdator()
JummahKhateebLookup.run()