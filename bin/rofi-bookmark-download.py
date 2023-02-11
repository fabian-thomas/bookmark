#!/usr/bin/env python
import os
import subprocess
import tldextract
import requests
import sys
import tempfile
import shutil
import favicon
from urllib.parse import urlparse

# returns True on success
def fix_image(filepath):
    tmp=tempfile.mktemp(suffix='.ico')
    # this fixes problems with images that are weirdly compressed and therefore
    # not supported by rofi
    p = subprocess.run(["convert", "-compress", "None", filepath, tmp])
    # only copy when succesfull, some images break when we call convert...
    if p.returncode == 0 and os.path.exists(tmp):
        shutil.move(tmp, filepath)
        return True
    else:
        # try one more time with 50% resizing which works in practice
        p = subprocess.run(["convert", "-resize", "50%", filepath, tmp])
        if p.returncode == 0 and os.path.exists(tmp):
            shutil.move(tmp, filepath)
            return True
        else:
            if os.path.exists(tmp):
                os.remove(tmp)
            return False

# User agent makes sure that some websites allow scraping.
headers={"User-Agent": "Mozilla/5.0 (X11; Linux x86_64; rv:109.0) Gecko/20100101 Firefox/109.0"}

retry = len(sys.argv) > 1 and sys.argv[1] == '--retry'

bookmarks_dir=os.getenv("BOOKMARKS_DIR", os.path.join(os.getenv("HOME"), '.bookmarks'))
cache_dir=os.path.join(os.getenv("CACHE_DIR", os.path.join(os.getenv("HOME"), ".cache")), "bookmarks")
cache_rofi=os.path.join(cache_dir, "rofi")

os.makedirs(cache_dir, exist_ok=True)

# maps bookmarks to the correct second level domain
bookmarks = {}
# maps the origins (scheme+domain+port) to icon file names
origins = {}
with subprocess.Popen(['bookmark', 'list'], stdout=subprocess.PIPE) as proc:
    stdout, _ = proc.communicate()
    for line in stdout.splitlines():
            name = line.decode()
            with open(os.path.join(bookmarks_dir, name), 'r') as file:
                url = file.readline()
                res = urlparse(url)
                origin = res._replace(fragment="", path="", params="", query="").geturl()
                # origin == "" can happen for bookmarks that contain no url.
                if origin != "":
                    if not origin in origins:
                        origins[origin] = os.path.join(cache_dir, origin.replace("/", "")+".ico")
                    # Bookmarks that have no origin are just ignored. This might
                    # lead to issues in the future?
                    bookmarks[name] = origin

# download icons
for origin in origins:
    filepath = origins[origin]
    # we touch all the files so that they are not tried again on a normal run
    # but for retries we check these too
    if not os.path.exists(filepath) or (retry and os.stat(filepath).st_size == 0):
        worked = False
        # First try to download via duckduckgo service. Finding the favicon for
        # each site is too slow. So use the cache by default.
        res = tldextract.extract(origin)
        second_level = '.'.join(res[1:])
        res = requests.get("https://icons.duckduckgo.com/ip3/"+second_level+".ico")
        if res.status_code == requests.codes.ok:
            with open(filepath, 'wb') as file:
                file.write(res.content)
            # All images should survive this, just try with favicon library
            # again if it does not work.
            worked = fix_image(filepath)

        # Try with favicon library if no success with ddg.
        if not worked:
            try:
                icons = favicon.get(origin, timeout=2, headers=headers)
                if len(icons) > 0:
                    icon = icons[0]
                    res = requests.get(icon.url, headers=headers)
                    if res.status_code == requests.codes.ok:
                        with open(filepath, 'wb') as image:
                            image.write(res.content)
                        worked = fix_image(filepath)
            except Exception:
                pass

        # If the file does not exist something went wrong. But don't retry if we
        # run again, so just touch the file.
        if not os.path.exists(filepath):
            open(filepath, 'w').close()

# prepare rofi input
rofi = ''
for name in bookmarks:
    origin = bookmarks[name]
    filepath = origins[origin]
    if os.path.exists(filepath) and os.stat(filepath).st_size != 0:
        rofi += name + '\0icon\x1f' + filepath + '\n'
    else:
        rofi += name + '\n'

with open(cache_rofi, 'w') as file:
    file.write(rofi)
