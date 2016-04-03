import json
import operator
import logging
from regexen import (
    zip_re, 
    last_first_name_re,
    first_last_name_re,
    phone_re,
    ssn_re
)
from record_property import RecordProperty
from exceptions import RecordException, FieldException

logger = logging.getLogger(__name__)


class Record:
    first_last = RecordProperty(first_last_name_re, 'first')
    last_first = RecordProperty(last_first_name_re, 'last')
    ssn = RecordProperty(ssn_re, 'ssn')
    phone = RecordProperty(phone_re, 'phone')
    zipcode = RecordProperty(zip_re, 'zipcode')


class Rolodex:
    def __init__(self, ifile):
        self.ifile = ifile
        self.record = Record()
        self.record_type = ""
        self.current_line = 0
        self.error_lines = []

    def _get_record_data(self, line):
        '''
        :param line:
        calls record setter so regex stuff is in record property
        while is looks like it could be more DRY, sending the right field
        names and values to record setter is all worked out here
        '''
        fields = line.split(',')
        if len(fields) == 5:
            if zip_re.match(fields[-1]):
                self.record_type = "last_zip"
            elif ssn_re.match(fields[-1]):
                self.record_type = "first_ssn"
        elif len(fields) == 4:
            self.record_type = "first_phone"
        else:
            raise RecordException("Bad record")

        if self.record_type == "first_phone":
            self.record.first_last = fields[0]
            self.record.ssn = fields[1]
            self.record.zipcode = fields[2]
            self.record.phone = fields[3]
        elif self.record_type == "last_zip":
            self.record.last_first = ",".join(fields[0:2])
            self.record.phone = fields[2]
            self.record.ssn = fields[3]
            self.record.zipcode = fields[4]
        else:
            self.record.first_last = "".join(fields[0:2])
            self.record.zipcode = fields[2]
            self.record.phone = fields[3]
            self.record.ssn = fields[4]

    def read(self):
        '''
        open a file, read and process the lines
        generator: yields a dict of fieldname: val
        on error, log exception and continue
        '''
        with open(self.ifile) as f:
            for line in f:
                self.current_line += 1
                try:
                    self._get_record_data(line.rstrip('\n'))
                except RecordException as e:
                    logger.error("RecordException: {}".format(str(e)))
                    self.error_lines.append(self.current_line)
                    continue
                except FieldException as e:
                    logger.error("FieldException: {}".format(str(e)))
                    self.error_lines.append(self.current_line)
                    continue
                data = {
                    "ssn": self.record.ssn,
                    "firstname": self.record.firstname,
                    "lastname": self.record.lastname,
                    "phonenumber": self.record.phone,
                    "zipcode": self.record.zipcode
                }
                yield data

    def format(self):
        entries = []
        for data in self.read():
            entries.append(data)

        sorted_entries = sorted(entries, key=operator.itemgetter('lastname', 'firstname'))
        print(json.dumps({"entries":sorted_entries, "errors": self.error_lines}, indent = 2))

if __name__ == '__main__':
    rolodex = Rolodex('data.in')
    rolodex.format()
