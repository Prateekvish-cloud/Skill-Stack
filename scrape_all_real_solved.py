import urllib.request
import json
import re

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
    'Accept-Language': 'en-US,en;q=0.5'
}

def test_gfg_scrape(handle="vishpratdzsq"):
    urls = [
        f"https://www.geeksforgeeks.org/user/{handle}/",
        f"https://auth.geeksforgeeks.org/user/{handle}/practice/"
    ]
    for url in urls:
        try:
            req = urllib.request.Request(url, headers=headers)
            with urllib.request.urlopen(req, timeout=8) as resp:
                html = resp.read().decode('utf-8', errors='ignore')
                print(f"GFG HTML length from {url}: {len(html)}")
                # Search for problem titles or links
                matches = re.findall(r'href="https://[^\"]*geeksforgeeks\.org/problems/([^/\"]+)', html)
                if matches:
                    print(f"GFG found problem slugs from {url}:", list(set(matches))[:15])
                    return list(set(matches))
                # Search for json data embedded in html
                json_matches = re.findall(r'"problem_name":"([^"]+)"', html)
                if json_matches:
                    print(f"GFG JSON matches from {url}:", list(set(json_matches))[:15])
                    return list(set(json_matches))
        except Exception as e:
            print(f"GFG Error for {url}: {e}")
    return []

def test_codechef_scrape(handle="crash_chef_57"):
    url = f"https://www.codechef.com/users/{handle}"
    try:
        req = urllib.request.Request(url, headers=headers)
        with urllib.request.urlopen(req, timeout=8) as resp:
            html = resp.read().decode('utf-8', errors='ignore')
            print(f"CodeChef HTML length: {len(html)}")
            # Find solved problems section
            # CodeChef lists problem codes inside <a href="/problems/CODE">
            matches = re.findall(r'href="/problems/([A-Z0-9_]+)"', html)
            if matches:
                clean = [m for m in set(matches) if m not in ['EASY', 'MEDIUM', 'HARD', 'SCHOOL', 'BASIC', 'CHALLENGE']]
                print("CodeChef solved problem codes:", clean[:15])
                return clean
            # Check script data
            script_data = re.findall(r'problems_solved\s*:\s*(\[[^\]]+\])', html)
            if script_data:
                print("CodeChef script data:", script_data[:5])
    except Exception as e:
        print(f"CodeChef error: {e}")
    return []

def test_hackerrank_api(handle="vishpratee2004"):
    url = f"https://www.hackerrank.com/rest/hackers/{handle}/recent_challenges?limit=20&cursor=null"
    try:
        req = urllib.request.Request(url, headers=headers)
        with urllib.request.urlopen(req, timeout=8) as resp:
            data = json.loads(resp.read().decode('utf-8'))
            print("HackerRank API response keys:", list(data.keys()))
            models = data.get('models', [])
            titles = [m.get('ch_title') or m.get('name') for m in models if m.get('ch_title') or m.get('name')]
            print("HackerRank solved titles:", titles[:15])
            return titles
    except Exception as e:
        print(f"HackerRank error: {e}")
    return []

if __name__ == '__main__':
    print("=== TESTING REAL GFG SCRAPE ===")
    test_gfg_scrape("vishpratdzsq")

    print("\n=== TESTING REAL CODECHEF SCRAPE ===")
    test_codechef_scrape("crash_chef_57")

    print("\n=== TESTING REAL HACKERRANK API ===")
    test_hackerrank_api("vishpratee2004")
