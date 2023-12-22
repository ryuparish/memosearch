from flask import Flask
import urllib
from urllib.request import urlopen
from bs4 import BeautifulSoup

app = Flask(__name__)


@app.route("/links/<link_name>")
def links(link_name):
    """Handles the link route.

    This route gets information about the link
    and returns it in a dictionary.


    :param str link_name: The link we are interested in.
    :returns:  {title: str, text: str}
    :rtype: dict (JSON)
    """
    # Check for empty link
    if len(link_name) == 0:
        print(f"Error, link is empty: {link_name}")
        return

    # Try to use urlopen
    try:
        html = urlopen(link_name).read()
    except Exception as e:
        print(f"Error opening URL: {e}")
        return

    # Process the text
    soup = BeautifulSoup(html, features="html.parser")

    # kill all script and style elements
    for script in soup(["script", "style"]):
        script.extract()  # rip it out

    # get text
    text = soup.get_text()
    lines = (line.strip() for line in text.splitlines())

    # break multi-headlines into a line each
    chunks = (phrase.strip() for line in lines for phrase in line.split("  "))

    # drop blank lines
    text = "\n".join(chunk for chunk in chunks if chunk)

    return {"title": soup.title, "text": text}
