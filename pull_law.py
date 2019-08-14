"""
python pull_law [url to html of gesetze-im-internet.de] [target file as json]
"""
import json
import sys
import requests
import os
from lxml import html


def merge_subs(subparagraphs):
    def check_str(string):
        return string is not None and string.startswith("(") and string.endswith(")")

    for i, subparagraph in enumerate(subparagraphs):
        text = subparagraph["text"]
        if check_str(text) and i+1 < len(subparagraphs): subparagraphs[i+1]["text"] = text + " " + subparagraphs[i+1]["text"]

    return [subparagraph for subparagraph in subparagraphs if not check_str(subparagraph["text"])]


def extract_from_subparagraph(paragraph):
    try:
        children = paragraph.getchildren()
        text = paragraph.text_content()

        for child in children:
            text = text.replace(child.text_content(), "")

        if paragraph.text is not None and paragraph.text != text:
            text = text.replace(paragraph.text, paragraph.text + "||")

        subparagraphs = [extract_from_subparagraph(sub) for sub in paragraph.findall("dl/dd/div")]
        subparagraphs = merge_subs(subparagraphs)

        return {
            "text": text,
            "sub": subparagraphs
        }

    except Exception as e:
        print("%r" % e)
        print("Exception at %s" % paragraph.text_content())
        return None


def extract_from_header(div):
    return {
                "type": "section",
                "title": " – ".join([el.text_content() for el in div.findall("div//span")])
    }


def extract_from_norm(div):
        jnenbez = div.find_class("jnenbez")

        if len(jnenbez) == 0: return None
        desc = div.find_class("jnenbez")[0].text
        print("Parsing %s" % desc)

        title = div.find_class("jnentitel")[0].text
        paragraphs = [extract_from_subparagraph(par) for par in div.find_class("jurAbsatz")]

        return {
            "type": "norm",
            "norm": desc,
            "title": title,
            "paragraphs": paragraphs
        }


def extract_from_div(div):
    try:
        title = div.get("title")

        if title == "Einzelnorm": return extract_from_norm(div)
        elif title == "Gliederung": return extract_from_header(div)
        else:
            print("Unknown title: %s" % title)
            return None

    except Exception as e:
        print("%r" % e)
        return None


def get_and_parse_gii(url):
    page = requests.get(url)
    tree = html.fromstring(page.content)

    paragraphs = tree.xpath("//div[@class='jnnorm']")
    parsed_norms = list(filter(lambda x: x is not None, map(extract_from_div, paragraphs)))

    return parsed_norms


def main():
    URL = sys.argv[1] if len(sys.argv) >= 2 else "https://www.gesetze-im-internet.de/bgb/BJNR001950896.html"
    TARGET_JSON = sys.argv[2] if len(sys.argv) >= 3 else "bgb.json"

    parsed_norms = get_and_parse_gii(URL)

    with open(TARGET_JSON, "w", encoding="utf-8") as fp:
        json.dump(fp=fp,
                  obj=parsed_norms,
                  ensure_ascii=False,
                  indent=4)


if __name__ == "__main__":
    main()
