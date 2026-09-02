import urllib.request
import json
from datetime import datetime
from app import get_user_coding_profiles, db_query

def sync_real_user_solved(user_id=1):
    profiles = get_user_coding_profiles(user_id)
    print(f"Syncing real solved problems for user {user_id}...")

    lc_handle = None
    for p in profiles:
        if p["key"] == "leetcode" and p.get("connected"):
            lc_handle = p.get("raw_handle")
            break

    if not lc_handle:
        lc_handle = "Prateek_vish"

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
    payload = json.dumps({'query': query, 'variables': {'username': lc_handle, 'limit': 30}}).encode('utf-8')
    req = urllib.request.Request(url, data=payload, headers={'Content-Type': 'application/json', 'User-Agent': 'Mozilla/5.0'})

    try:
        with urllib.request.urlopen(req, timeout=5) as resp:
            data = json.loads(resp.read().decode('utf-8'))
            subs = data.get('data', {}).get('recentAcSubmissionList', [])
            
            if subs:
                # Clear sample/demo data
                db_query('DELETE FROM user_solved_problems WHERE user_id = %s', (user_id,), commit=True)
                
                seen = set()
                inserted = 0
                for idx, s in enumerate(subs):
                    title = s.get('title')
                    slug = s.get('titleSlug')
                    if title and title not in seen:
                        seen.add(title)
                        prob_id = f"lc_{slug}"
                        db_query(
                            '''INSERT INTO user_solved_problems (user_id, problem_id, title, num, topic, diff, platform, created_at)
                               VALUES (%s, %s, %s, %s, %s, %s, %s, %s)''',
                            (user_id, prob_id, title, str(idx+1), 'arr', 'Medium', 'leetcode', datetime.utcnow()),
                            commit=True
                        )
                        inserted += 1
                print(f"Successfully inserted {inserted} REAL solved problems for @{lc_handle}!")
    except Exception as e:
        print(f"Error fetching real solved problems for {lc_handle}: {e}")

if __name__ == '__main__':
    sync_real_user_solved(1)
