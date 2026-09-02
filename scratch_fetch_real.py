import urllib.request
import json
import re

def fetch_leetcode_real_solved(username):
    url = 'https://leetcode.com/graphql'
    query = '''
    query recentAcSubmissions($username: String!, $limit: Int!) {
      recentAcSubmissionList(username: $username, limit: $limit) {
        title
        titleSlug
        timestamp
        id
      }
    }
    '''
    payload = json.dumps({'query': query, 'variables': {'username': username, 'limit': 20}}).encode('utf-8')
    req = urllib.request.Request(url, data=payload, headers={'Content-Type': 'application/json', 'User-Agent': 'Mozilla/5.0'})
    try:
        with urllib.request.urlopen(req, timeout=5) as resp:
            data = json.loads(resp.read().decode('utf-8'))
            subs = data.get('data', {}).get('recentAcSubmissionList', [])
            seen = set()
            res = []
            for s in subs:
                t = s.get('title')
                if t and t not in seen:
                    seen.add(t)
                    res.append({
                        "title": t,
                        "titleSlug": s.get('titleSlug'),
                        "platform": "leetcode"
                    })
            return res
    except Exception as e:
        print(f"LeetCode error for {username}: {e}")
        return []

def fetch_gfg_real_solved(handle):
    # Fetch GFG user profile API
    url = f"https://geeksforgeeks-api.vercel.app/user/{handle}"
    req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
    try:
        with urllib.request.urlopen(req, timeout=5) as resp:
            data = json.loads(resp.read().decode('utf-8'))
            print("GFG raw response keys:", list(data.keys()))
            solved_probs = data.get("solvedStats", {}) or data.get("solvedProblems", {})
            return solved_probs
    except Exception as e:
        print(f"GFG fetch notice for {handle}: {e}")
        # Fallback scraping GFG user profile
        try:
            page_url = f"https://www.geeksforgeeks.org/user/{handle}/"
            preq = urllib.request.Request(page_url, headers={'User-Agent': 'Mozilla/5.0'})
            with urllib.request.urlopen(preq, timeout=5) as presp:
                html = presp.read().decode('utf-8', errors='ignore')
                matches = re.findall(r'href="https://www\.geeksforgeeks\.org/problems/([^/]+)/', html)
                seen = set()
                res = []
                for m in matches:
                    t = m.replace('-', ' ').title()
                    if t not in seen:
                        seen.add(t)
                        res.append({"title": t, "titleSlug": m, "platform": "gfg"})
                return res
        except Exception as e2:
            print(f"GFG scrape notice for {handle}: {e2}")
            return []

def fetch_codechef_real_solved(handle):
    url = f"https://codechef-api.vercel.app/handle/{handle}"
    req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
    try:
        with urllib.request.urlopen(req, timeout=5) as resp:
            data = json.loads(resp.read().decode('utf-8'))
            print("CodeChef raw response keys:", list(data.keys()))
            return data.get("solvedProblems", [])
    except Exception as e:
        print(f"CodeChef notice for {handle}: {e}")
        return []

if __name__ == '__main__':
    print("Testing GFG for vishpratdzsq:")
    gfg = fetch_gfg_real_solved("vishpratdzsq")
    print("GFG Result:", gfg)

    print("\nTesting CodeChef for crash_chef_57:")
    cc = fetch_codechef_real_solved("crash_chef_57")
    print("CodeChef Result:", cc)
