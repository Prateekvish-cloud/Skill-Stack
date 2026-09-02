from datetime import datetime
import urllib.request
import json

def get_live_upcoming_contests():
    upcoming = []
    now_ts = int(datetime.utcnow().timestamp())
    
    # 1. LeetCode Live GraphQL API
    try:
        url = 'https://leetcode.com/graphql'
        query = 'query topTwoContests { topTwoContests { title titleSlug startTime } }'
        req = urllib.request.Request(url, data=json.dumps({'query': query}).encode('utf-8'), headers={'Content-Type': 'application/json', 'User-Agent': 'Mozilla/5.0'})
        with urllib.request.urlopen(req, timeout=5) as resp:
            data = json.loads(resp.read().decode('utf-8')).get('data', {}).get('topTwoContests', [])
            for c in data:
                start_ts = c.get('startTime', 0)
                diff_sec = max(0, start_ts - now_ts)
                days = diff_sec // 86400
                hours = (diff_sec % 86400) // 3600
                mins = (diff_sec % 3600) // 60
                dt_str = datetime.fromtimestamp(start_ts).strftime("%a, %b %d • %I:%M %p IST")
                
                upcoming.append({
                    "id": f"lc_{c.get('titleSlug')}",
                    "platform": "leetcode",
                    "plat_label": "LeetCode",
                    "name": c.get('title'),
                    "date": dt_str,
                    "url": f"https://leetcode.com/contest/{c.get('titleSlug')}/",
                    "countdown": f"{days}d {hours}h {mins}m"
                })
    except Exception as e:
        print("LeetCode live API notice:", e)

    # 2. Codeforces Live REST API
    try:
        url = 'https://codeforces.com/api/contest.list?gym=false'
        req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        with urllib.request.urlopen(req, timeout=5) as resp:
            data = json.loads(resp.read().decode('utf-8'))
            if data.get('status') == 'OK':
                cf_list = [c for c in data.get('result', []) if c.get('phase') == 'BEFORE']
                cf_list.sort(key=lambda x: x.get('startTimeSeconds', 0))
                for c in cf_list[:2]:
                    start_ts = c.get('startTimeSeconds', 0)
                    diff_sec = max(0, start_ts - now_ts)
                    days = diff_sec // 86400
                    hours = (diff_sec % 86400) // 3600
                    mins = (diff_sec % 3600) // 60
                    dt_str = datetime.fromtimestamp(start_ts).strftime("%a, %b %d • %I:%M %p IST")

                    upcoming.append({
                        "id": f"cf_{c.get('id')}",
                        "platform": "codeforces",
                        "plat_label": "Codeforces",
                        "name": c.get('name'),
                        "date": dt_str,
                        "url": f"https://codeforces.com/contestRegistration/{c.get('id')}",
                        "countdown": f"{days}d {hours}h {mins}m"
                    })
    except Exception as e:
        print("Codeforces live API notice:", e)

    # 3. CodeChef Live REST API
    try:
        url = 'https://www.codechef.com/api/list/contests/all?status=future'
        req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        with urllib.request.urlopen(req, timeout=5) as resp:
            data = json.loads(resp.read().decode('utf-8'))
            cc_list = data.get('future_contests', [])
            for c in cc_list[:2]:
                c_code = c.get('contest_code')
                c_name = c.get('contest_name')
                dt_raw = c.get('contest_start_date', '')
                upcoming.append({
                    "id": f"cc_{c_code}",
                    "platform": "codechef",
                    "plat_label": "CodeChef",
                    "name": c_name,
                    "date": dt_raw,
                    "url": f"https://www.codechef.com/{c_code}",
                    "countdown": "Upcoming"
                })
    except Exception as e:
        print("CodeChef live API notice:", e)

    return upcoming

if __name__ == '__main__':
    res = get_live_upcoming_contests()
    print("LIVE REAL CONTESTS FETCHED:")
    for r in res:
        print(" ", r['platform'], "|", r['name'], "| Direct URL:", r['url'], "| Timer:", r['countdown'])
