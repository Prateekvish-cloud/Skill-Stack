import urllib.request
import json
import re

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8'
}

def inspect_gfg(handle="vishpratdzsq"):
    url = f"https://www.geeksforgeeks.org/user/{handle}/"
    req = urllib.request.Request(url, headers=headers)
    try:
        with urllib.request.urlopen(req, timeout=10) as resp:
            html = resp.read().decode('utf-8', errors='ignore')
            # Search for script tags containing NEXT_DATA or user profile data
            script_data = re.findall(r'<script id="__NEXT_DATA__" type="application/json">([^<]+)</script>', html)
            if script_data:
                data = json.loads(script_data[0])
                print("GFG NEXT_DATA keys:", list(data.keys()))
                props = data.get('props', {}).get('pageProps', {})
                print("GFG pageProps keys:", list(props.keys()))
                userInfo = props.get('userInfo', {}) or props.get('user', {})
                print("GFG userInfo keys:", list(userInfo.keys()))
                # Check for solved problem lists
                solved = props.get('solvedProblems', []) or props.get('postData', []) or props.get('userSubmissions', [])
                print("GFG solvedProblems sample:", str(solved)[:500])
                return props
    except Exception as e:
        print("GFG Error:", e)

def inspect_codechef(handle="crash_chef_57"):
    url = f"https://www.codechef.com/users/{handle}"
    req = urllib.request.Request(url, headers=headers)
    try:
        with urllib.request.urlopen(req, timeout=10) as resp:
            html = resp.read().decode('utf-8', errors='ignore')
            # Look for solved problems section
            section = re.findall(r'Problems Solved.*?</section>', html, re.DOTALL)
            if section:
                print("CodeChef solved section HTML sample:", section[0][:1000])
                # Extract problem codes from links inside section
                codes = re.findall(r'/status/([A-Z0-9_]+)', section[0])
                print("CodeChef problem status codes:", list(set(codes))[:20])
                return codes
            else:
                # Find all links matching /status/
                codes = re.findall(r'href="/status/([A-Z0-9_]+)', html)
                print("CodeChef status links:", list(set(codes))[:20])
                # Find all problem links
                probs = re.findall(r'/problems/([A-Z0-9_]+)', html)
                print("CodeChef problem links:", list(set(probs))[:20])
    except Exception as e:
        print("CodeChef Error:", e)

if __name__ == '__main__':
    print("=== INSPECTING GFG NEXT_DATA ===")
    inspect_gfg("vishpratdzsq")

    print("\n=== INSPECTING CODECHEF SOLVED SECTION ===")
    inspect_codechef("crash_chef_57")
