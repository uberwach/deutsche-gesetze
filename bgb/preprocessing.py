# -*- coding: utf-8 -*-

import json
import os

DATA_DIR = os.path.join(os.path.pardir, "data")
RAW_DIR = os.path.join(DATA_DIR, "raw")
PROCESSED_DIR = os.path.join(DATA_DIR, "processed")


def read_raw_json():
    FILE_PATH = os.path.join(RAW_DIR, "bgb.json")
    data = json.load(open(FILE_PATH, "r"))
    return data


def filter_entries(entry):
    if entry["titel"] == "(weggefallen)":
        return False

    return True

if __name__ == "__main__":
    data = read_raw_json()

    for entry in data:
        entry["absaetze"] = [absatz for absatz in entry["absaetze"] if len(absatz) >= 2]

    data = list(filter(filter_entries, data))

    with open(os.path.join(PROCESSED_DIR, "bgb.json"), "w") as fp:
        json.dump(data, fp, ensure_ascii=False)
