import os
import json
from glob import glob

ANNOTATION_DIR = "annotation"


def load_annotations():
    file_names = glob(ANNOTATION_DIR + "/*.json")
    annotation_map = dict() # maps "BGB" -> the annotation data

    for file_name in file_names:
        print("Getting annotations from %s" % file_name)
        with open(file_name, "r") as fp:
            data = json.load(fp)
            annotation = Annotations(data)
            book_name = _extract_book(file_name)
            annotation_map[book_name] = annotation
            print("Added annotations about %s" % book_name)

    return annotation_map


def _extract_book(file_path):
    return os.path.basename(file_path).split(".")[0]


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

    def __init__(self, data):
        self.__marked = set()
        self._digest_data(data)


    def _digest_data(self, data):
        for item in data:
            self._digest_item(item)

    def _digest_item(self, item):
        item_type = item["type"]

        if item_type == "marked":
            norms = item["norm"]

            if not isinstance(norms, list): norms = [norms]

            for norm in norms:
                self.__marked.add(norm)

    def is_marked(self, norm):
        return norm in self.__marked

