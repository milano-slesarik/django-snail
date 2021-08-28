import datetime
import decimal
import json
import typing
from json import JSONEncoder


class JsonArrayFileWriterNotOpenError(Exception):
    pass


class JsonArrayFileWriter:
    def __init__(self, filepath: str, indent: typing.Optional[int], ):
        self.filepath = filepath
        self.indent = indent
        self.lines = 0
        self.file = None

    def __enter__(self) -> object:
        self.open()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb) -> None:
        self.close()

    def open(self) -> None:
        self.file = open(self.filepath, 'w')
        self.file.write('[')

    def write(self, dct: dict) -> None:
        if getattr(self, 'file', None) is None:
            raise JsonArrayFileWriterNotOpenError(
                "JsonArrayFileWriter needs to be opened by calling `.open()` or used in a context manager `with JsonArrayFileWriter(<FILENAME>,<INDENT>) as writer:`")
        jsn = json.dumps(dct, indent=self.indent)
        self.file.write(',\n') if self.lines else self.file.write('\n')
        self.file.write(jsn)
        self.lines += 1

    def write_dict(self, dct: dict) -> None:
        self.write(dct)

    def close(self) -> None:
        self.file.write('\n')
        self.file.write(']')
        self.file.close()


# instantiate the writer
writer = JsonArrayFileWriter('output.json', indent=4)

# open the writer
writer.open()

# write entries
writer.write_dict({"id": 1, "first_name": "Peter", "last_name": "Sveter", "age": datetime.datetime.now().isoformat(), "height": "50 CM",
                   "grades": {"Math": "A", "History": "B+", "Programming": "F-"}})
writer.write_dict({"id": 2, "first_name": "Donald", "last_name": "Donaldson", "age": 9, "height": "150 CM",
                   "grades": {"Math": "C", "History": "B", "Programming": "A"}})

# close the writer
writer.close()

