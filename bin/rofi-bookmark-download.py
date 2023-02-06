#!/usr/bin/env python
import os
import subprocess
import tldextract
import requests
import sys
import tempfile
import shutil

retry = len(sys.argv) > 1 and sys.argv[1] == '--retry'

bookmarks_dir = os.environ['BOOKMARKS_DIR'] if 'BOOKMARKS_DIR' in os.environ else os.path.join(os.environ['HOME'], '.bookmarks')
cache_dir = os.environ['CACHE_DIR']
cache_rofi = os.environ['CACHE_ROFI']

os.makedirs(cache_dir, exist_ok=True)

bookmarks = {}
url_icons = {}
with subprocess.Popen(['bookmark', 'list'], stdout=subprocess.PIPE) as proc:
    stdout, _ = proc.communicate()
    for line in stdout.splitlines():
            name = line.decode()
            with open(os.path.join(bookmarks_dir, name), 'r') as file:
                url = file.readline()
                # get second level domain
                res = tldextract.extract(url)
                second_level = '.'.join(res[1:])
                bookmarks[name] = second_level
                if second_level not in url_icons:
                    if second_level.endswith('github.com'):
                        url_icons[second_level] = (second_level + '.svg', 'https://github.githubassets.com/favicons/favicon-dark.svg')
                    else:
                        ico = second_level + '.ico'
                        url_icons[second_level] = (ico, 'https://icons.duckduckgo.com/ip3/' + ico)

# download icons
for url in url_icons:
    filepath = os.path.join(cache_dir, url_icons[url][0])
    if not os.path.exists(filepath) or (retry and os.stat(filepath).st_size == 0):
        url = url_icons[url][1]
        res = requests.get(url)
        if res.status_code == requests.codes.ok:
            with open(filepath, 'wb') as file:
                file.write(res.content)
            if not filepath.endswith("svg"): # this is for the github case and probably breaks in other cases too
                tmp=tempfile.mktemp(suffix='.ico')
                # this fixes problems with images that are weirdly compressed and therefore
                # not supported by rofi
                p = subprocess.run(["convert", "-compress", "None", filepath, tmp])
                # only copy when succesfull, some images break when we call convert...
                if p.returncode == 0 and os.path.exists(tmp):
                    shutil.move(tmp, filepath)
                else:
                    # try one more time with 50% resizing which works in practice
                    p = subprocess.run(["convert", "-resize", "50%", filepath, tmp])
                    if p.returncode == 0 and os.path.exists(tmp):
                        shutil.move(tmp, filepath)
                    else:
                        if os.path.exists(tmp):
                            os.remove(tmp)
        else:
            open(filepath, 'w').close()

# prepare rofi input
rofi = ''
for name in bookmarks:
    second_level = bookmarks[name]
    ico_filepath = os.path.join(cache_dir, url_icons[second_level][0])
    if os.path.exists(ico_filepath) and os.stat(ico_filepath).st_size != 0:
        rofi += name + '\0icon\x1f' + ico_filepath + '\n'
    else:
        rofi += name + '\n'

with open(cache_rofi, 'w') as file:
    file.write(rofi)
