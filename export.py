import sys
import codecs
from bs4 import BeautifulSoup
from bibtexparser.bwriter import BibTexWriter
from bibtexparser.bibdatabase import BibDatabase

def formatAuthor(author):
	split = author.split(' ')
	authorStr = split[len(split) - 1]
	if len(split) > 1:
		authorStr = split[len(split) - 1] + ","
	for i in range(0, len(split) - 1):
		authorStr += " " + split[i]
	return authorStr.strip()

def createAuthorString(html):
	count = 0
	authors = []
	while True:
		count = count + 1
		authorStr = 'author' + str(count)
		if authorStr in html.attrs:
			authors.append(formatAuthor(html.attrs[authorStr]))
		else:
			break
	authorStr = ""
	if len(authors) > 1:
		for i in range(0, len(authors) - 1):
			authorStr += authors[i] + " and "
		authorStr += authors[len(authors) - 1]
	else:
		authorStr = authors[0]
	return authorStr

def createID(html):
	author = [""]
	if 'author1' in html.attrs:
		author = html.attrs['author1'].split(' ')
	id = author[len(author) - 1] + html['year']
	if id not in entryIDs:
		entryIDs.append(id)
	else:
		found = False
		count = 1
		while not found:
			count = count + 1
			newID = id + "(" + str(count) + ")"
			if newID not in entryIDs:
				id = newID
				entryIDs.append(id)
				found = True
	return id

def process(html):
	bib = {}
	if 'pages' in html.attrs:
		bib['pages'] = html.attrs['pages']
	if 'title' in html.attrs:
		bib['title'] = html.attrs['title']
	if 'year' in html.attrs:
		bib['year'] = html.attrs['year']
	if 'volume' in html.attrs:
		bib['volume'] = html.attrs['volume']
	if 'number' in html.attrs:
		bib['number'] = html.attrs['number']
	if 'author1' in html.attrs:
		bib['author'] = createAuthorString(html)
	if 'publisher' in html.attrs:
		bib['publisher'] = html.attrs['publisher']
	if 'organization' in html.attrs:
		bib['organization'] = html.attrs['organization']
	bib['ID'] = createID(html)
	return bib
	
	
wikiFile = "./LitWiki.html"
bibFile = "./export.bib"

for i in range(0, len(sys.argv)):
	if sys.argv[i] == "-bib":
		bibFile = sys.argv[i + 1]
	elif sys.argv[i] == "-wiki":
		wikiFile = sys.argv[i + 1]
		
html_doc = open(wikiFile).read()
soup = BeautifulSoup(html_doc, 'html.parser')
storeArea = soup.find(id="storeArea")
bibDB = BibDatabase()
entryIDs = []

for child in storeArea.children:
	if child.name == "div":
		if 'tags' in child.attrs:
			if '[[Journal Paper]]' in child.attrs['tags']:
				bib = process(child)
				if 'pub' in child.attrs:
					bib['journal'] = child.attrs['pub']
				bib['ENTRYTYPE'] = 'article'
				bibDB.entries.append(bib)
			elif 'Book' in child.attrs['tags']:
				bib = process(child)
				if 'pub' in child.attrs:
					bib['series'] = child.attrs['pub']
				bib['ENTRYTYPE'] = 'book'
				bibDB.entries.append(bib)
			elif '[[Conference Paper]]' in child.attrs['tags']:
				bib = process(child)
				if 'pub' in child.attrs:
					bib['booktitle'] = child.attrs['pub']
				if 'series' in child.attrs:
					bib['series'] = child.attrs['series']
				bib['ENTRYTYPE'] = 'inproceedings'
				bibDB.entries.append(bib)
			elif 'Dissertation' in child.attrs['tags']:
				bib = process(child)
				bib['ENTRYTYPE'] = 'phdthesis'
				bibDB.entries.append(bib)
			elif 'Thesis' in child.attrs['tags']:
				bib = process(child)
				bib['ENTRYTYPE'] = 'mastersthesis'
				bibDB.entries.append(bib)
			elif '[[Technical Report]]' in child.attrs['tags']:
				bib = process(child)
				bib['ENTRYTYPE'] = 'techreport'
				bibDB.entries.append(bib)
			elif '[[Technical Manual]]' in child.attrs['tags']:
				bib = process(child)
				bib['ENTRYTYPE'] = 'manual'
				bibDB.entries.append(bib)


writer = BibTexWriter()
with codecs.open(bibFile, 'w', 'utf-8') as bibfile:
	bibfile.write(writer.write(bibDB))