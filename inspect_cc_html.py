import urllib.request
import re

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8'
}

url = "https://www.codechef.com/users/crash_chef_57"
req = urllib.request.Request(url, headers=headers)
with urllib.request.urlopen(req) as resp:
    html = resp.read().decode('utf-8', errors='ignore')
    print("HTML length:", len(html))
    
    # Save HTML to debug file
    with open("cc_profile.html", "w", encoding="utf-8") as f:
        f.write(html)
        
    # Search for problem codes in HTML
    # CodeChef displays solved problems inside <a> tags within rating-data-section or problem-solved
    probs = re.findall(r'<a[^>]+href="[^"]*(?:/status/|/problems/)([A-Z0-9_]+)"[^>]*>([^<]+)</a>', html)
    print("Found (code, text) pairs:", probs[:30])

    # Search for plain text inside solved problems list
    section = re.findall(r'Fully Solved.*?</h3>(.*?)</article>', html, re.DOTALL)
    if section:
        print("Fully Solved section found!")
        links = re.findall(r'<a[^>]*>([^<]+)</a>', section[0])
        print("Fully Solved problem titles:", links)
