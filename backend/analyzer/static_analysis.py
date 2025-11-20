import re

def parse_changed_files(diff_text: str):
    files = set()
    for line in diff_text.splitlines():
        m = re.match(r'^\+\+\+ b/(.+)$', line)
        if m:
            files.add(m.group(1).strip())

    tokens = re.findall(r'[\w\/\-\_\.]+\.(py|js|ts|go|java|sql|json)', diff_text)
    for t in tokens:
        files.add(t)

    return list(files)
