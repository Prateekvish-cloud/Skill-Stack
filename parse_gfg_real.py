import urllib.request
import json

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
    'Content-Type': 'application/json',
    'Origin': 'https://www.geeksforgeeks.org',
    'Referer': 'https://www.geeksforgeeks.org/'
}

def fetch_gfg_real_submissions(handle="vishpratdzsq"):
    url = "https://practiceapi.geeksforgeeks.org/api/v1/user/problems/submissions/"
    payload = json.dumps({"handle": handle}).encode('utf-8')
    req = urllib.request.Request(url, data=payload, headers=headers, method='POST')
    
    try:
        with urllib.request.urlopen(req, timeout=5) as resp:
            data = json.loads(resp.read().decode('utf-8'))
            result = data.get("result", {})
            
            solved_list = []
            for diff, probs in result.items():
                if isinstance(probs, dict):
                    for prob_id, details in probs.items():
                        if isinstance(details, dict):
                            pname = details.get("pname")
                            slug = details.get("slug")
                            subtime = details.get("user_subtime")
                            if pname:
                                solved_list.append({
                                    "pname": pname,
                                    "slug": slug,
                                    "diff": diff,
                                    "subtime": subtime
                                })
            print(f"GFG Total Real Solved Problems for @{handle}: {len(solved_list)}")
            return solved_list
    except Exception as e:
        print("GFG Error:", e)
        return []

if __name__ == '__main__':
    probs = fetch_gfg_real_submissions("vishpratdzsq")
    for p in probs[:25]:
        print(f"  [{p['diff']}] {p['pname']} ({p['slug']}) - {p['subtime']}")
