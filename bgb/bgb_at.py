# -*- coding: utf-8 -*-

import json
import os

DATA_DIR = os.path.join(os.path.pardir, "data")
PROCESSED_DIR = os.path.join(DATA_DIR, "processed")
STATIC_DIR = os.path.join(os.path.pardir, "static")


def read_json():
    FILE_PATH = os.path.join(PROCESSED_DIR, "bgb.json")
    data = json.load(open(FILE_PATH, "r"))
    return data


if __name__ == "__main__":
    data = read_json()

    with open(os.path.join(STATIC_DIR, "bgb_at.html"), "w") as fp:
        fp.write("""<html>
        <head>
        <title> BGB Allgemeiner Teil </title>
        <link href="css/gesetze.css" rel="stylesheet" title="Default Style">
        </head>

        <body>
        """)

        fp.write("<h1>Bürgerliches Gesetzbuch – Allgemeiner Teil</h1>")
        for entry in data:
            paragraph, title = entry["paragraph"], entry["titel"]
            fp.write("<div class='normhead'>%s %s</div><br />\n" % (paragraph, title))

            fp.write("<div class='normtext'>\n")
            for absatz in entry["absaetze"]:
                fp.write("<div class='abs'>%s</div><br />\n" % (absatz))

            fp.write("</div>\n")


            if paragraph == "§ 240":
                break

        fp.write("</body> </html>")
