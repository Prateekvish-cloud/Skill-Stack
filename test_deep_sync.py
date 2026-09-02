import urllib.request
import json
import re

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
    'Accept': '*/*',
    'Referer': 'https://www.codechef.com/'
}

def test_codeforces(handle="Prateek24_"):
    url = f"https://codeforces.com/api/user.status?handle={handle}&from=1&count=100"
    try:
        req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        with urllib.request.urlopen(req, timeout=5) as resp:
            data = json.loads(resp.read().decode('utf-8'))
            print("Codeforces status:", data.get("status"))
            result = data.get("result", [])
            print(f"Codeforces total submissions for {handle}:", len(result))
            ok_probs = []
            seen = set()
            for sub in result:
                if sub.get("verdict") == "OK":
                    prob = sub.get("problem", {})
                    name = prob.get("name")
                    contestId = prob.get("contestId", "")
                    index = prob.get("index", "")
                    if name and name not in seen:
                        seen.add(name)
                        ok_probs.append({
                            "name": name,
                            "code": f"{contestId}{index}",
                            "url": f"https://codeforces.com/problemset/problem/{contestId}/{index}"
                        })
            print("Codeforces OK solved problems:", len(ok_probs), ok_probs[:10])
            return ok_probs
    except Exception as e:
        print("Codeforces Error:", e)
        return []

def test_codechef_recent(handle="crash_chef_57"):
    urls = [
        f"https://www.codechef.com/recent/user?page=0&user_handle={handle}",
        f"https://www.codechef.com/recent/user?page=1&user_handle={handle}",
        f"https://www.codechef.com/users/{handle}"
    ]
    for url in urls:
        print(f"\nTesting CodeChef URL: {url}")
        try:
            req = urllib.request.Request(url, headers=headers)
            with urllib.request.urlopen(req, timeout=8) as resp:
                body = resp.read().decode('utf-8')
                print("Response length:", len(body))
                try:
                    data = json.loads(body)
                    print("JSON keys:", list(data.keys()))
                    html = data.get("content", "") or data.get("html", "")
                    if html:
                        probs = re.findall(r'href="/problems/([A-Za-z0-9_]+)"', html)
                        print("Found CodeChef problems in JSON HTML:", list(set(probs))[:15])
                except Exception:
                    probs = re.findall(r'href="/problems/([A-Za-z0-9_]+)"', body)
                    print("Found CodeChef problems in raw HTML:", list(set(probs))[:15])
        except Exception as e:
            print("CodeChef Error:", e)

def test_hackerrank_submissions(handle="vishpratee2004"):
    url = f"https://www.hackerrank.com/rest/hackers/{handle}/recent_challenges?limit=50&cursor=null"
    try:
        req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        with urllib.request.urlopen(req, timeout=8) as resp:
            data = json.loads(resp.read().decode('utf-8'))
            models = data.get('models', [])
            print(f"HackerRank total submissions for {handle}:", len(models))
            clean_list = []
            seen = set()
            for m in models:
                title = (m.get('ch_title') or m.get('name') or "").strip()
                slug = m.get('ch_slug') or title.lower().replace(' ', '-')
                topic = m.get('track', {}).get('name') or "Algorithms"
                if title and title not in seen:
                    seen.add(title)
                    clean_list.append({
                        "title": title,
                        "slug": slug,
                        "topic": topic,
                        "url": f"https://www.hackerrank.com/challenges/{slug}/problem"
                    })
            print("HackerRank clean solved challenges:", len(clean_list), clean_list[:10])
            return clean_list
    except Exception as e:
        print("HackerRank Error:", e)
        return []

if __name__ == '__main__':
    print("=== TESTING CODEFORCES ===")
    test_codeforces("Prateek24_")

    print("\n=== TESTING CODECHEF ===")
    test_codechef_recent("crash_chef_57")

    print("\n=== TESTING HACKERRANK ===")
    test_hackerrank_submissions("vishpratee2004")
