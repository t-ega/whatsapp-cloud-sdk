from json import JSONEncoder

from _files.file_object import File


class MyEncoder(JSONEncoder):
    def default(self, o):
        if isinstance(o, File):
            return o.to_dict()

        return super().default(o)
