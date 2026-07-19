import os
import re
import time
import requests
from urllib.parse import urlparse, urljoin, unquote
from bs4 import BeautifulSoup
from tqdm import tqdm


# ==========================
# CONFIG
# ==========================

WAYBACK = "https://web.archive.org"

TIMEOUT = 40

DELAY = 0.5

USER_AGENT = (
    "Mozilla/5.0 "
    "(Windows NT 10.0; Win64; x64)"
)


session = requests.Session()

session.headers.update({
    "User-Agent": USER_AGENT
})


# ==========================
# INPUT
# ==========================

DOMAIN = input(
    "Masukkan domain (contoh: example.com): "
).strip()


if DOMAIN.startswith("http"):
    DOMAIN = urlparse(DOMAIN).netloc


OUTPUT_DIR = input(
    "Folder output (default: website): "
).strip()


if not OUTPUT_DIR:
    OUTPUT_DIR = "website"



# ==========================
# PATH
# ==========================

def url_to_path(url):

    parsed = urlparse(url)

    path = unquote(
        parsed.path
    )


    if not path or path.endswith("/"):
        path += "index.html"


    filename = os.path.basename(path)


    if "." not in filename:
        path += ".html"


    path = path.replace(
        "..",
        ""
    )


    return path.lstrip("/")



# ==========================
# SAVE FILE
# ==========================

def save_file(path, data):

    filepath = os.path.join(
        OUTPUT_DIR,
        path
    )


    folder = os.path.dirname(filepath)


    if folder:
        os.makedirs(
            folder,
            exist_ok=True
        )


    if os.path.exists(filepath):
        return


    with open(
        filepath,
        "wb"
    ) as f:
        f.write(data)



# ==========================
# DOWNLOAD
# ==========================

def download(url):

    try:

        r = session.get(
            url,
            timeout=TIMEOUT
        )


        if r.status_code == 200:
            return r.content


    except Exception:
        pass


    return None



# ==========================
# WAYBACK URL LIST
# ==========================

def get_urls():

    print(
        "\nMengambil daftar URL Wayback..."
    )


    api = (
        f"{WAYBACK}/cdx/search/cdx?"
        f"url={DOMAIN}/*&"
        "output=json&"
        "fl=timestamp,original,statuscode&"
        "filter=statuscode:200&"
        "collapse=urlkey"
    )


    r = session.get(
        api,
        timeout=60
    )


    data = r.json()


    result = {}


    for item in data[1:]:

        timestamp = item[0]
        url = item[1]


        result[url] = timestamp



    print(
        "Total URL:",
        len(result)
    )


    return result



# ==========================
# EXTRACT ASSET
# ==========================

def extract_assets(html, base):

    soup = BeautifulSoup(
        html,
        "html.parser"
    )


    assets = []


    tags = [
        ("img","src"),
        ("script","src"),
        ("link","href")
    ]


    for tag, attr in tags:

        for element in soup.find_all(tag):

            link = element.get(attr)


            if not link:
                continue


            full = urljoin(
                base,
                link
            )


            if DOMAIN in full:
                assets.append(full)



    return assets



# ==========================
# FIX HTML LINK
# ==========================

def fix_html(html):

    soup = BeautifulSoup(
        html,
        "html.parser"
    )


    tags = [
        ("a","href"),
        ("img","src"),
        ("script","src"),
        ("link","href")
    ]


    for tag, attr in tags:


        for el in soup.find_all(tag):

            value = el.get(attr)


            if not value:
                continue


            value = re.sub(
                r"https?://web\.archive\.org/web/\d+(?:id_)?/",
                "",
                value
            )


            if DOMAIN in value:

                el[attr] = url_to_path(
                    value
                )



    return str(soup)



# ==========================
# CLONE
# ==========================

def clone():

    urls = get_urls()


    if not urls:
        print(
            "Tidak ada data Wayback."
        )
        return



    for url, timestamp in tqdm(
        urls.items(),
        desc="Downloading"
    ):


        archive_url = (
            f"{WAYBACK}/web/"
            f"{timestamp}id_/"
            f"{url}"
        )


        path = url_to_path(
            url
        )


        data = download(
            archive_url
        )


        if not data:
            continue



        # HTML CHECK

        if (
            b"<html" in data.lower()
            or
            b"<!doctype" in data.lower()
        ):


            html = data.decode(
                "utf-8",
                errors="ignore"
            )


            assets = extract_assets(
                html,
                url
            )


            html = fix_html(
                html
            )


            data = html.encode(
                "utf-8"
            )


            for asset in assets:


                asset_time = urls.get(
                    asset
                )


                if not asset_time:
                    continue



                asset_archive = (
                    f"{WAYBACK}/web/"
                    f"{asset_time}id_/"
                    f"{asset}"
                )


                asset_data = download(
                    asset_archive
                )


                if asset_data:

                    save_file(
                        url_to_path(asset),
                        asset_data
                    )



        save_file(
            path,
            data
        )


        time.sleep(
            DELAY
        )



# ==========================
# RUN
# ==========================

if __name__ == "__main__":

    os.makedirs(
        OUTPUT_DIR,
        exist_ok=True
    )


    clone()


    print(
        "\nSelesai."
    )
