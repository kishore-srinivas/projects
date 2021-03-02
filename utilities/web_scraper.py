from urllib.request import urlopen
import re

url = "https://www2.eecs.berkeley.edu/Research/Areas/"
page = urlopen(url)
html_bytes = page.read()
html = html_bytes.decode("utf-8")

start = html.find("<!-- YOUR CONTENT HERE -->")
end = html.find("<!-- end of YOUR CONTENT")
extract = html[start:end]

starts = [m.start() for m in re.finditer('<li>', extract)]
ends = [m.start() for m in re.finditer('</li>', extract)]

links = []
for i in range(len(ends)):
    item = extract[starts[i]+4:ends[i]]
    link = item[item.find("<a")+9:item.find("\">")]
    links.append(link)

faculty = {}

interests = ['/Research/Areas/GR', '/Research/Areas/AI', '/Research/Areas/CIR', '/Research/Areas/HCI', '/Research/Areas/MEMS']
for l in links:
    if l not in interests:
        continue
    print('>>>', l)
    url = "https://www2.eecs.berkeley.edu" + l
    page = urlopen(url)
    html_bytes = page.read()
    html = html_bytes.decode("utf-8")

    start_index = html.find("<h2>Faculty</h2>")
    end_index = html.find("<h2>Faculty Awards</h2>")
    extract = html[start_index:end_index]

    starts = [m.start() for m in re.finditer('<a', extract)]
    ends = [m.start() for m in re.finditer('.html">', extract)]

    facultySites = []
    for i in range(len(starts)):
        facultySites.append(extract[starts[i]+9:ends[i]+5])

    count = 0
    for f in facultySites:
        url = 'https://www2.eecs.berkeley.edu/' + f
        page = urlopen(url)
        html_bytes = page.read()
        html = html_bytes.decode("utf-8")

        startIdx = html.find("Research Areas")
        endIdx = html[startIdx:].find("</ul>") + startIdx
        extract = html[startIdx:endIdx]
        # print(startIdx, endIdx)

        starts = [m.start() for m in re.finditer('<li>', extract)]
        ends = [m.start() for m in re.finditer('</li>', extract)]
        # print(f, len(starts), len(ends))

        if f in faculty.keys():
            arr = faculty[f]
        else:
            arr = []
        for i in range(len(starts)):
            entry = extract[starts[i]:ends[i]]
            # print(entry)
            area = entry[entry.find("href=\"")+7:entry.find("\">")]
            # print('>>>', area)
            arr.append(area)
        faculty[f] = arr
        # print(f, faculty[f], arr)

# print(len(faculty.keys()))
# first = list(faculty.keys())[0]
# print(first)
# print(faculty[first])
# print(list(set(faculty[first])))
# areas = faculty[list(faculty.keys())[0]]
# # print(areas)
# for a in areas:
#     print(a, ('/' + a) in interests)

matches = {}
for f in faculty.keys():
    m = 0
    unique = list(set(faculty[f]))
    for a in unique:
        m += 1 if (('/' + a) in interests) else 0
    print(f, m)
    matches[f] = m
print('--------------')
print(sorted(matches.items(), key=lambda x: x[1], reverse=True))