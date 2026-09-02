import urllib.request
import json
from datetime import datetime
from app import db_query

gfg_headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
    'Content-Type': 'application/json',
    'Origin': 'https://www.geeksforgeeks.org',
    'Referer': 'https://www.geeksforgeeks.org/'
}

def sync_live_gfg(handle="vishpratdzsq"):
    url = "https://practiceapi.geeksforgeeks.org/api/v1/user/problems/submissions/"
    payload = json.dumps({"handle": handle}).encode('utf-8')
    req = urllib.request.Request(url, data=payload, headers=gfg_headers, method='POST')
    res = []
    try:
        with urllib.request.urlopen(req, timeout=8) as resp:
            data = json.loads(resp.read().decode('utf-8'))
            result = data.get("result", {})
            for diff, probs in result.items():
                if isinstance(probs, dict):
                    for prob_id, details in probs.items():
                        if isinstance(details, dict):
                            pname = details.get("pname")
                            slug = details.get("slug")
                            if pname:
                                res.append({
                                    "pname": pname,
                                    "slug": slug[:140],
                                    "diff": diff.capitalize() if diff else "Medium"
                                })
    except Exception as e:
        print(f"GFG Sync Error for {handle}: {e}")
    return res

def sync_live_leetcode(handle="Prateek_vish"):
    url = 'https://leetcode.com/graphql'
    query = 'query recentAcSubmissions($username: String!, $limit: Int!) { recentAcSubmissionList(username: $username, limit: $limit) { title titleSlug } }'
    payload = json.dumps({'query': query, 'variables': {'username': handle, 'limit': 50}}).encode('utf-8')
    lc_headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
        'Content-Type': 'application/json'
    }
    req = urllib.request.Request(url, data=payload, headers=lc_headers)
    res = []
    try:
        with urllib.request.urlopen(req, timeout=8) as resp:
            data = json.loads(resp.read().decode('utf-8'))
            subs = data.get('data', {}).get('recentAcSubmissionList', [])
            seen = set()
            for s in subs:
                t = s.get('title')
                slug = s.get('titleSlug')
                if t and t not in seen:
                    seen.add(t)
                    res.append({
                        "title": t,
                        "slug": slug[:140],
                        "diff": "Medium"
                    })
    except Exception as e:
        print(f"LeetCode Sync Error for {handle}: {e}")
    return res

def sync_live_hackerrank(handle="vishpratee2004"):
    url = f"https://www.hackerrank.com/rest/hackers/{handle}/recent_challenges?limit=30&cursor=null"
    req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
    res = []
    try:
        with urllib.request.urlopen(req, timeout=8) as resp:
            data = json.loads(resp.read().decode('utf-8'))
            models = data.get('models', [])
            seen = set()
            for m in models:
                t = (m.get('ch_title') or m.get('name') or "").strip()
                slug = m.get('ch_slug') or t.lower().replace(' ', '-')
                if t and t not in seen:
                    seen.add(t)
                    res.append({
                        "title": t,
                        "slug": slug[:140],
                        "diff": "Easy"
                    })
    except Exception as e:
        print(f"HackerRank Sync Error for {handle}: {e}")
    return res

def run_full_live_sync(user_id=1):
    print("Clearing database table user_solved_problems for user 1...")
    db_query('DELETE FROM user_solved_problems WHERE user_id = %s', (user_id,), commit=True)
    
    total_inserted = 0

    # 1. GFG
    gfg_probs = sync_live_gfg("vishpratdzsq")
    print(f"Fetched {len(gfg_probs)} REAL GFG problems for @vishpratdzsq.")
    for idx, p in enumerate(gfg_probs):
        db_query(
            '''INSERT INTO user_solved_problems (user_id, problem_id, title, num, topic, diff, platform, created_at)
               VALUES (%s, %s, %s, %s, %s, %s, %s, NOW())''',
            (user_id, f"gfg_{p['slug']}", p['pname'], str(idx+1), 'arr', p['diff'], 'gfg'),
            commit=True
        )
        total_inserted += 1

    # 2. LeetCode
    lc_probs = sync_live_leetcode("Prateek_vish")
    print(f"Fetched {len(lc_probs)} REAL LeetCode problems for @Prateek_vish.")
    for idx, p in enumerate(lc_probs):
        db_query(
            '''INSERT INTO user_solved_problems (user_id, problem_id, title, num, topic, diff, platform, created_at)
               VALUES (%s, %s, %s, %s, %s, %s, %s, NOW())''',
            (user_id, f"lc_{p['slug']}", p['title'], str(idx+1), 'arr', p['diff'], 'leetcode'),
            commit=True
        )
        total_inserted += 1

    # 3. HackerRank
    hr_probs = sync_live_hackerrank("vishpratee2004")
    print(f"Fetched {len(hr_probs)} REAL HackerRank problems for @vishpratee2004.")
    for idx, p in enumerate(hr_probs):
        db_query(
            '''INSERT INTO user_solved_problems (user_id, problem_id, title, num, topic, diff, platform, created_at)
               VALUES (%s, %s, %s, %s, %s, %s, %s, NOW())''',
            (user_id, f"hr_{p['slug']}", p['title'], str(idx+1), 'arr', p['diff'], 'hackerrank'),
            commit=True
        )
        total_inserted += 1

    print(f"SYNC COMPLETE! Successfully inserted {total_inserted} 100% REAL LIVE solved problems into database!")

if __name__ == '__main__':
    run_full_live_sync(1)
