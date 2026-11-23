import json
import os
from pathlib import Path
import re
import subprocess
import sys
import time
from datetime import datetime
from zoneinfo import ZoneInfo

from lessons import START, END, render

day = datetime.now(ZoneInfo("Asia/Kolkata")).date()
if "--preview" in sys.argv:
    print(render(max(START,min(day,END)), "preview.jpg"))
    sys.exit()
if not START <= day <= END:
    print("Outside the campaign window")
    sys.exit()

def git(*args):
    return subprocess.check_output(["git", *args], text=True).strip()

def save(path, message):
    git("add", str(path))
    git("commit", "-m", message)
    git("push", "origin", "HEAD:main")
    return git("rev-parse", "HEAD")

version = os.environ.get("IG_API_VERSION") or ""
if not re.fullmatch(r"v\d+\.\d+", version):
    raise RuntimeError("Set IG_API_VERSION to the supported version in your Meta app")
token = os.environ.get("IG_ACCESS_TOKEN")
if not token:
    raise RuntimeError("Missing IG_ACCESS_TOKEN Actions secret")
import requests
session = requests.Session()
session.headers["Authorization"] = "Bearer " + token
base = "https://graph.instagram.com/" + version + "/"
def api(method, route, **params):
    kwargs = {"params":params} if method=="GET" else {"data":params}
    res = session.request(method, base+route, timeout=40, **kwargs)
    if not res.ok:
        raise RuntimeError(f"Instagram {res.status_code} ({res.json().get('error',{}).get('code')}) on {route}")
    return res.json()

me = api("GET","me",fields="user_id,username")
if me.get("username") != "__all_in__onee":
    raise RuntimeError("Instagram account mismatch")
account = me["user_id"]
marker = "Mana AI Lab | " + day.isoformat()
folder = Path("campaign") / str(day)
folder.mkdir(parents=True,exist_ok=True)
receipt = folder/"published.json"
if receipt.exists():
    print(json.loads(receipt.read_text())["permalink"])
    sys.exit()

def record(post):
    if not post.get("permalink") or marker not in post.get("caption",""):
        raise RuntimeError("Publication has no verified permalink or campaign marker")
    receipt.write_text(json.dumps({k:post[k] for k in ("id","permalink")},indent=2))
    save(receipt,"Verify Instagram publication for "+str(day))
    print(post["permalink"])

for post in api("GET",account+"/media",fields="id,caption,permalink",limit=50)["data"]:
    if marker in post.get("caption",""):
        record(post)
        sys.exit()

image = folder/"post.jpg"
caption = render(day, image)
if git("status","--porcelain","--",str(image)):
    save(image,"Prepare image for "+str(day))
sha = git("rev-parse","HEAD")
url = f"https://raw.githubusercontent.com/{os.environ['GITHUB_REPOSITORY']}/{sha}/{image}"
state = folder/"container.json"
if state.exists():
    cid = json.loads(state.read_text())["id"]
else:
    cid = api("POST",account+"/media",image_url=url,caption=caption)["id"]
    state.write_text(json.dumps({"id":cid}))
    save(state,"Track Instagram container for "+str(day))
for _ in range(12):
    status = api("GET",cid,fields="status_code")["status_code"]
    if status == "FINISHED": break
    if status != "IN_PROGRESS":
        raise RuntimeError("Inspect existing container before retry: "+status)
    time.sleep(5)
else:
    raise RuntimeError("Container still processing")
published = api("POST",account+"/media_publish",creation_id=cid)
record(api("GET",published["id"],fields="id,caption,permalink"))
