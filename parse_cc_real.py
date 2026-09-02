import urllib.request
import json
import re

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
    'Accept': 'application/json, text/plain, */*',
    'Referer': 'https://www.codechef.com/users/crash_chef_57'
}

def test_codechef_endpoints(handle="crash_chef_57"):
    urls = [
        f"https://www.codechef.com/api/ratings/all?username={handle}",
        f"https://www.codechef.com/users/{handle}",
        f"https://codechef-api2.vercel.app/handle/{handle}"
    ]
    for url in urls:
        print(f"\nTesting CodeChef URL: {url}")
        try:
            req = urllib.request.Request(url, headers=headers)
            with urllib.request.urlopen(req, timeout=5) as resp:
                print("Status:", resp.status)
                content = resp.read().decode('utf-8', errors='ignore')
                print("Content length:", len(content))
                # Search for problem codes in HTML
                codes = re.findall(r'/status/([A-Z0-9_]+)', content)
                if codes:
                    unique_codes = [c for c in set(codes) if c not in ['EASY', 'MEDIUM', 'HARD', 'SCHOOL']]
                    print("Found CodeChef solved codes:", unique_codes[:20])
                    return unique_codes
                # Search for problem links /problems/CODE
                prob_codes = re.findall(r'href="/problems/([A-Za-z0-9_]+)"', content)
                if prob_codes:
                    clean_probs = [p for p in set(prob_codes) if p not in ['easy', 'medium', 'hard', 'school', 'submit']]
                    print("Found CodeChef problem links:", clean_probs[:20])
                    return clean_probs
        except Exception as e:
            print("Error:", e)

if __name__ == '__main__':
    test_codechef_endpoints("crash_chef_57")
