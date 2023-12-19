from pydicom import Dataset


class FindQuery:
    def __init__(self, p_id='', p_name='', s_id='', s_num='', qry=''):
        self._ds = Dataset()

        self.__setattr__('PatientID', p_id)
        self.__setattr__('PatientName', p_name)
        self.__setattr__('StudyID', s_id)
        self.__setattr__('SeriesNumber', s_num)
        self.__setattr__('QueryRetrieveLevel', qry)

    def __setattr__(self, key, value):
        if None == value or (isinstance(value, str) and '' == value):
            return

        if '_ds' == key:
            self.__dict__[key] = value
        else:
            self._ds.__setattr__(key, value)

    def toDataset(self):
        return self._ds
