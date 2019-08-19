# -*- coding: utf-8 -*-

import json
import os
import itertools
from glob import glob
from annotations import load_annotations, Annotations

DATA_DIR = "data"
STATIC_DIR = "static"
ANNOTATIONS_MAP = load_annotations()
ALPHABET = [chr(ord('a') + k) for k in range(26)]


def read_json(name):
    FILE_PATH = os.path.join(DATA_DIR, "%s.json" % name)
    data = json.load(open(FILE_PATH, "r"))
    return data


def lit_gen():
    """'a', 'b', ..., 'z', 'aa', 'ab'... """
    k = 1

    while True:
        for combination in map(''.join, itertools.product(*([ALPHABET] * k))):
            yield combination

        k += 1


def generate_lawbook(name):
    ANNOTATIONS = ANNOTATIONS_MAP.get(name, Annotations(list()))

    with open(os.path.join(STATIC_DIR, "%s.html" % name), "w+") as fp:
        fp.write("""<html>
        <head>
          <title> %s </title>
          <meta charset="utf-8">
          <meta name="viewport" content="width=device-width, initial-scale=1">
          <link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/3.4.0/css/bootstrap.min.css">
          <script src="https://ajax.googleapis.com/ajax/libs/jquery/3.4.1/jquery.min.js"></script>
          <script src="https://maxcdn.bootstrapcdn.com/bootstrap/3.4.0/js/bootstrap.min.js"></script>
          <link href="css/gesetze.css" rel="stylesheet" title="Default Style">
        </head>

        <body>
        """ % name)

        data = read_json(name)

        fp.write("<h1>%s</h1>" % name)

        for entry in data:
            if entry["type"] == "section":
                fp.write("<h3>%s</h3>" % entry["title"])

            else:
                paragraph, title = entry["norm"], entry.get("title", "")
                if title is None: title = ""

                print("Writing %s %s" % (paragraph, name))

                anchor = "<a id='#%s'></a>" % entry["norm"]
                fp.write("<div class='norm'>")
                fp.write("<div class='normhead%s'>%s %s</div> %s" % (" marked" if ANNOTATIONS.is_marked(paragraph) else "", paragraph, title, anchor))
                fp.write("<div class='normtext'>")


                for absatz in entry["paragraphs"]:
                    fp.write("<div class='abs'>%s" % (absatz["text"]))

                    subs = absatz["sub"]
                    if subs != []:
                        fp.write("<div class='subbox'>")
                        for i, sub in enumerate(subs):
                            fp.write("<div class='sub'>%d. %s" % (i+1, sub["text"]))

                            subsubs = sub["sub"]


                            if subsubs != []:
                                fp.write("<div class='subsubbox'>")
                                letters = lit_gen()
                                for subsub in subsubs:
                                    fp.write("<div class='subsub'>%s) %s</div>" % (next(letters), subsub["text"]))

                                fp.write("</div>") # .subsubbox

                            fp.write("</div>") # .sub
                        fp.write("</div>") # .subbox
                    fp.write("</div>") # .abs
                fp.write("</div>") # .normtext
                fp.write("</div>") # .norm



        fp.write("</body> </html>")

if __name__ == "__main__":
    file_paths = glob(DATA_DIR + "/*.json")
    file_names = [os.path.basename(path).split(".")[0] for path in file_paths]

    for name in file_names:
        print("Generating %s" % name)
        generate_lawbook(name)
