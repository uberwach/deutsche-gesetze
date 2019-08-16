import os
import json
from glob import glob

ANNOTATION_DIR = "annotation"


class Annotation(object):

    def __init__(self, norm):
        self.__norm = norm
        self.__comments = []
        self.__is_marked = False

    def set_marked(self, mark):
        self.__is_marked = mark

    def is_marked(self):
        return self.__is_marked

    def str(self):
        return "§ %s" % self.__norm



class Annotations(object):
    """Keeps the annotations for the norms of a norm book (e.g. BGB, HGB), but only one."""

    def __init__(self):
        self.__dict = dict()
        self.__marked = set()
        self._read_files()

    def _read_files(self):
        file_names = glob(ANNOTATION_DIR + "/*.json")


        for file_name in file_names:
            print("Getting annotations from %s" % file_name)
            with open(file_name, "r") as fp:
                data = json.load(fp)

                for item in data:
                    self._digest_data(item)


    def _digest_data(self, data):
        data_type = data["type"]

        if data_type == "marked":
            norms = data["norm"]

            if not isinstance(norms, list): norms = [norms]

            for norm in norms:
                self.__marked.add(norm)


    def is_marked(self, norm):
        return norm in self.__marked
