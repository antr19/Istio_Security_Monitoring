from bs4 import BeautifulSoup
import requests
import re


last_bulletin = ""


def get_bulletins():
    res = requests.get("https://istio.io/latest/news/security/", verify=False)
    soup = BeautifulSoup(res.text, 'html.parser')

    return soup.find("table").find_all("tr")


def stay_alive():
    print(requests.get("https://istio-monitoring.onrender.com/", verify=False))


def get_titles(lines):
    for col in lines[0].find_all("th"):
        yield col.text


def get_last_vuh(lines):
    def validate_url(url):
        regex = re.compile(
            r'^(?:http|ftp)s?://' # http:// or https://
            r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+(?:[A-Z]{2,6}\.?|[A-Z0-9-]{2,}\.?)|' #domain...
            r'localhost|' #localhost...
            r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})' # ...or ip
            r'(?::\d+)?' # optional port
            r'(?:/?|[/?]\S+)$', re.IGNORECASE)
        return re.match(regex, url) is not None

    for col in lines[1].find_all("td"):
        if col.find("a"):
            if validate_url(col.a['href']):
                link = col.a['href']
            else:
                link = "https://istio.io" + col.a['href']
            yield f"<a href=\"{link}\">{col.text}</a>"
        else:
            yield col.text


def create_report(lines):
    report = []
    for title, value in zip(get_titles(lines), get_last_vuh(lines)):
        report.append(f"<b>{title}</b>: {value}")
    report.append("")
    report.append("<b><a href=\"https://istio.io/latest/news/security/\">Security Bulletins</a></b>")
    return "\n".join(report)


def istio_checking():
    global last_bulletin
    lines = get_bulletins()
    bul = [col for col in get_last_vuh(lines)]
    check = "_".join(bul)
    if last_bulletin != check:
        last_bulletin = check
        return create_report(lines)
    return None


def start():
    global last_bulletin
    lines = get_bulletins()
    bul = [col for col in get_last_vuh(lines)]
    last_bulletin = "_".join(bul)


start()