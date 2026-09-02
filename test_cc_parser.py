import urllib.request
import json
import re
import time

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
    'Accept': 'application/json, text/javascript, */*; q=0.01',
    'X-Requested-With': 'XMLHttpRequest',
    'Referer': 'https://www.codechef.com/users/crash_chef_57'
}

def fetch_codechef_real_solved(handle="crash_chef_57"):
    solved_problems = []
    seen = set()
    
    for page in range(5):
        url = f"https://www.codechef.com/recent/user?page={page}&user_handle={handle}"
        try:
            req = urllib.request.Request(url, headers=headers)
            with urllib.request.urlopen(req, timeout=8) as resp:
                data = json.loads(resp.read().decode('utf-8'))
                content = data.get("content", "")
                if not content or "No Recent Submissions" in content:
                    break
                
                rows = re.findall(r'<tr.*?>(.*?)</tr>', content, re.DOTALL)
                for row in rows:
                    if 'tick-icon.gif' in row or "title='accepted'" in row or "(100)" in row:
                        # Extract problem title/code & link
                        matches = re.findall(r"<a\s+href='([^']+)'[^>]*>([^<]+)</a>", row)
                        if matches:
                            href, title = matches[0]
                            title = title.strip()
                            if title and title != "View" and title not in seen:
                                seen.add(title)
                                full_url = f"https://www.codechef.com{href}" if href.startswith('/') else href
                                solved_problems.append({
                                    "title": title,
                                    "code": title,
                                    "url": full_url,
                                    "diff": "Easy"
                                })
            time.sleep(0.5)
        except Exception as e:
            print(f"CodeChef page {page} notice for {handle}: {e}")
            break

    print(f"CodeChef Total Real Solved Problems for @{handle}: {len(solved_problems)}")
    return solved_problems

if __name__ == '__main__':
    probs = fetch_codechef_real_solved("crash_chef_57")
    for p in probs:
        print(f"  CodeChef Solved: {p['title']} -> {p['url']}")
