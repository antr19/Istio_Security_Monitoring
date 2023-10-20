import requests
import json
import os

token = os.environ['GIT_TOKEN']
date_of_last_adv = ""


def get_adv():
    res = requests.get("https://api.github.com/repos/envoyproxy/envoy/security-advisories",
                       headers={
                           "Authorization": f"Bearer {token}",
                           "Accept": "application/vnd.github+json",
                           "X-GitHub-Api-Version": "2022-11-28"
                       })
    return json.loads(res.text)[0]


def get_val(js, keys):
    val = js[keys[0]]
    for i in range(1, len(keys)):
        val = val[keys[i]]
    return val


def get_name(keys):
    return "_".join([i for i in keys if type(i) == str])


def get_report_line(js, keys, bold=False, link=False):
    if link:
        line = f"{get_name(keys).title()}: <a href=\"{link}\">{get_val(js, keys)}</a>"
    else:
        line = f"{get_name(keys).title()}: {get_val(js, keys)}"
    if bold:
        line = f"<b>{line}</b>"
    return line


def create_report(js):
    report = []
    report.append(get_report_line(js, ["summary"], bold=True, link=get_val(js, ["html_url"])))
    report.append(get_report_line(js, ["severity"], bold=True))
    report.append("")

    report.append(get_report_line(js, ["cve_id"]))
    report.append(get_report_line(js, ["cvss", "score"]))
    report.append(get_report_line(js, ["cvss", "vector_string"]))
    report.append(get_report_line(js, ["cwes", 0, "cwe_id"]))
    report.append(get_report_line(js, ["cwes", 0, "name"]))
    report.append("")

    report.append(get_report_line(js, ["vulnerabilities", 0, "patched_versions"]))
    report.append("")

    report.append(get_report_line(js, ["published_at"]))
    report.append(get_report_line(js, ["updated_at"]))
    report.append("")

    report.append("<b><a href=\"https://github.com/envoyproxy/envoy/security/advisories\">Security Advisories</a></b>")


    return "\n".join(report)


def envoy_checking():
    global date_of_last_adv
    adv = get_adv()
    if adv['published_at'] != date_of_last_adv:
        date_of_last_adv = adv['published_at']
        return create_report(adv)
    return None


def start():
    global date_of_last_adv
    adv = get_adv()
    date_of_last_adv = adv['published_at']


start()

