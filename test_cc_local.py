import re

with open('cc_content.html', 'r', encoding='utf-8') as f:
    content = f.read()

rows = re.findall(r'<tr.*?>(.*?)</tr>', content, re.DOTALL)
seen = set()
solved = []

for row in rows:
    if 'tick-icon.gif' in row or "title='accepted'" in row or '(100)' in row:
        matches = re.findall(r"<a\s+href='([^']+)'[^>]*>([^<]+)</a>", row)
        if matches:
            href, title = matches[0]
            title = title.strip()
            if title and title != 'View' and title not in seen:
                seen.add(title)
                solved.append({'title': title, 'href': href})

print(f'Extracted CodeChef solved problems from page 0: {len(solved)}')
for s in solved:
    print(f"  {s['title']} -> https://www.codechef.com{s['href']}")
