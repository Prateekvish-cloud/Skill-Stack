import urllib.request
import json
import re

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
    'Accept': 'application/json, text/javascript, */*; q=0.01',
    'X-Requested-With': 'XMLHttpRequest',
    'Referer': 'https://www.codechef.com/users/crash_chef_57'
}

url = "https://www.codechef.com/recent/user?page=0&user_handle=crash_chef_57"
req = urllib.request.Request(url, headers=headers)
with urllib.request.urlopen(req) as resp:
    data = json.loads(resp.read().decode('utf-8'))
    content = data.get("content", "")
    print("Content length:", len(content))
    with open("cc_content.html", "w", encoding="utf-8") as f:
        f.write(content)

    # Search for links in content
    # CodeChef recent submissions table has <tr> with problem link <a href="/problems/CODE">
    matches = re.findall(r'<a[^>]+href="[^"]*/problems/([^"]+)"[^>]*>([^<]+)</a>', content)
    print("Matched problem links in table:", matches[:20])

    # Search for status link
    status_matches = re.findall(r'href="[^"]*/status/([^,"]+)', content)
    print("Matched status links in table:", list(set(status_matches))[:20])
