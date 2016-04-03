## rolodex descriptor
from exceptions import FieldException
from regexen import first_last_name_re, last_first_name_re


class RecordProperty:
    '''
    class descriptor
    @regex : regular expression 
    @val : placeholder for value to be tested against regex
    '''
    def __init__(self, regex, val):
        self.regex = regex
        self.val = val

    def __get__(self, instance, cls):
        ''' instance.var <- '''
        return self.val

    def __set__(self, instance, val):
        ''' 
        @val: string 
        match val 
        '''
        self.val = val.strip(" ")
        match = self.regex.match(self.val)
        if match and self.regex == first_last_name_re:
            instance.firstname = match.group(1)
            instance.lastname = match.group(2)
        elif match and self.regex == last_first_name_re:
            instance.firstname = match.group(2)
            instance.lastname = match.group(1)
        elif not match:
            raise FieldException("{0} Not Matched by {1}".format(
                val,
                self.regex
                )
            )
