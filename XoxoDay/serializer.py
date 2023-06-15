import json


class Serializer(object):

    @staticmethod
    def dumps(data_obj):
        try:
            return json.dumps(data_obj, ensure_ascii=False,
                              allow_nan=False,
                              indent=None,
                              separators=(",", ":")).encode("utf-8")
        except:
            return None

    @staticmethod
    def loads(data_string):
        try:
            return json.loads(data_string)
        except:
            return None
