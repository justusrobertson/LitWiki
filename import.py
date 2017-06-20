import os
import sys
import datetime
import bibtexparser
from bs4 import BeautifulSoup

def removeCharacters(string, characters):
	for char in characters:
		if char in string:
			string = string.replace(char,"")
	return string
	
def fileExists(file_path):
    if not file_path:
        return False
    elif not os.path.isfile(file_path):
        return False
    else:
        return True

newFile = "./LitWikiTest.html"
bibFile = "./import.bib"
paper = "./paper.pdf"
bibtex = ""
pubLink = ""
orgLink = ""
tags = []
formattedTags = []

for i in range(0, len(sys.argv)):
	if sys.argv[i] == "-bib":
		bibFile = sys.argv[i + 1]
	elif sys.argv[i] == "-pub":
		pubLink = sys.argv[i + 1]
	elif sys.argv[i] == "-org":
		orgLink = sys.argv[i + 1]
	elif sys.argv[i] == "-tags":
		tags = [x.lstrip() for x in sys.argv[i + 1].split(',')]
	elif sys.argv[i] == "-file":
		newFile = sys.argv[i + 1]
	elif sys.argv[i] == "-overwrite":
		newFile = "./LitWiki.html"
	elif sys.argv[i] == "-paper":
		paper = sys.argv[i + 1]
		
with open(bibFile) as bibtexFile:
	bibtex = bibtexparser.load(bibtexFile).entries[0]

now = datetime.datetime.now()
html_doc = open("./LitWiki.html").read()
soup = BeautifulSoup(html_doc, 'html.parser')
storeArea = soup.find(id="storeArea")

if bibtex['ENTRYTYPE'] == "article":
	formattedTags.append("[[Journal Article]]")
elif bibtex['ENTRYTYPE'] == "book":
	formattedTags.append("Book")
elif bibtex['ENTRYTYPE'] == "inproceedings":
	formattedTags.append("[[Conference Paper]]")
elif bibtex['ENTRYTYPE'] == "phdthesis":
	formattedTags.append("Dissertation")
elif bibtex['ENTRYTYPE'] == "mastersthesis":
	formattedTags.append("Thesis")
elif bibtex['ENTRYTYPE'] == "techreport":
	formattedTags.append("[[Technical Report]]")
elif bibtex['ENTRYTYPE'] == "manual":
	formattedTags.append("[[Technical Manual]]")

tag = soup.new_tag('div')

authors = bibtex['author'].split('and')
for i in range(0, len(authors)):
	authorSplit = authors[i].split(',')
	author = ""
	if len(authorSplit) > 1:
		author = authorSplit[1].strip() + " " + authorSplit[0].strip()
	else:
		author = authorSplit[0].lstrip()
	authorTag = 'author' + str(i + 1)
	tag.attrs[authorTag] = author
	if len(authorSplit) == 1:
		formattedTags.append(author)
	else:
		formattedTags.append("[[" + author + "]]")

tag.attrs['created'] = str(now.year) + str('{:02d}'.format(now.month)) + str('{:02d}'.format(now.day)) + str('{:02d}'.format(now.hour)) + str('{:02d}'.format(now.minute)) + str('{:02d}'.format(now.second)) + '000'
tag.attrs['creator'] = 'justus'

pdf = './Papers/'
for author in authors:
	authorSplit = author.split(',')
	pdf += authorSplit[0].strip() + " "
pdf += bibtex['year'] + " - " + removeCharacters(bibtex['title'], [':', ',']) + ".pdf"

tag.attrs['pdf'] = pdf

if pubLink != "":
	tag.attrs['publink'] = pubLink
	
if orgLink != "":
	tag.attrs['orglink'] = orgLink

ref = ""
for i in range(0, len(authors)):
	authorSplit = authors[i].split(',')
	if i == len(authors) - 1 and len(authors) > 1:
		ref += "and "
	ref += authorSplit[0].strip() + " "
ref += bibtex['year']
	
tag.attrs['ref'] = ref

for tagi in tags:
	if len(tagi.split(' ')) == 1:
		formattedTags.append(tagi)
	else:
		formattedTags.append("[[" + tagi + "]]")

tag.attrs['title'] = bibtex['title']

postAuthorStr = "\n"
if 'journal' in bibtex:
	tag.attrs['pub'] = bibtex['journal']
	if pubLink != "":
		postAuthorStr += '|!Journal|<a target="_blank" href={{!!publink}}>{{!!pub}}</a>|\n'
	else:
		postAuthorStr += '|!Journal|{{!!pub}}|\n'
	
if 'series' in bibtex:
	if bibtex['ENTRYTYPE'] == "book":
		tag.attrs['pub'] = bibtex['series']
		if pubLink != "":
			postAuthorStr += '|!Series|<a target="_blank" href={{!!publink}}>{{!!pub}}</a>|\n'
		else:
			postAuthorStr += '|!Series|{{!!pub}}|\n'
	elif bibtex['ENTRYTYPE'] == "inproceedings":
		tag.attrs['series'] = bibtex['series']
		postAuthorStr += '|!Series|{{!!series}}|\n'
		formattedTags.append(bibtex['series'])
	
if 'booktitle' in bibtex:
	tag.attrs['pub'] = bibtex['booktitle']
	if pubLink != "":
		postAuthorStr += '|!Conference|<a target="_blank" href={{!!publink}}>{{!!pub}}</a>|\n'
	else:
		postAuthorStr += '|!Conference|{{!!pub}}|\n'

if 'publisher' in bibtex:
	tag.attrs['publisher'] = bibtex['publisher']
	if orgLink != "":
		postAuthorStr += '|!Publisher|<a target="_blank" href={{!!orglink}}>{{!!publisher}}</a>|\n'
	else:
		postAuthorStr += '|!Publisher|{{!!publisher}}|\n'
	
if 'organization' in bibtex:
	tag.attrs['organization'] = bibtex['organization']
	if orgLink != "":
		postAuthorStr += '|!Organization|<a target="_blank" href={{!!orglink}}>{{!!organization}}</a>|\n'
	else:
		postAuthorStr += '|!Organization|{{!!organization}}|\n'

if 'school' in bibtex:
   tag.attrs['school'] = bibtex['school']
   if bibtex['ENTRYTYPE'] == "mastersthesis" or bibtex['ENTRYTYPE'] == "phdthesis":
      postAuthorStr += '|!School|<a target="_blank" href={{!!orglink}}>{{!!school}}</a>|\n'
   else:
      postAuthorStr += '|!School|{{!!school}}|\n'
      
if 'year' in bibtex:
	tag.attrs['year'] = bibtex['year']
	formattedTags.append(bibtex['year'])
	postAuthorStr += '|!Year|{{!!year}}|\n'

if 'volume' in bibtex:
	tag.attrs['volume'] = bibtex['volume']
	postAuthorStr += '|!Volume|{{!!volume}}|\n'
	
if 'number' in bibtex:
	tag.attrs['number'] = bibtex['number']
	postAuthorStr += '|!Number|{{!!number}}|\n'

if 'pages' in bibtex:
	tag.attrs['pages'] = bibtex['pages']
	postAuthorStr += '|!Pages|{{!!pages}}|\n'
	
	
tagStr = ""
for tagi in formattedTags:
	tagStr += tagi + " "
tagStr = tagStr.strip()
tag.attrs['tags'] = tagStr

preTag = soup.new_tag('pre')

preAuthorStr = '|!Authors|'
for i in range(0, len(authors)):
	if i < len(authors) - 1 and len(authors) > 2:
		preAuthorStr += '<$link to={{!!author' + str(i + 1) + '}}>{{!!author' + str(i + 1) + '}}</$link>, '
	elif i < len(authors) - 1:
		preAuthorStr += '<$link to={{!!author' + str(i + 1) + '}}>{{!!author' + str(i + 1) + '}}</$link> '
	elif len(authors) > 1:
		preAuthorStr += 'and <$link to={{!!author' + str(i + 1) + '}}>{{!!author' + str(i + 1) + '}}</$link>|'
	else:
		preAuthorStr += '<$link to={{!!author' + str(i + 1) + '}}>{{!!author' + str(i + 1) + '}}</$link>|'

preTag.string = preAuthorStr + postAuthorStr + '|!PDF|<a target="_blank" href={{!!pdf}}>{{!!ref}}</a>|'
tag.append(preTag)
storeArea.insert(len(storeArea), tag)
if not fileExists(pdf):
	os.rename(paper, pdf)

with open(newFile, "w") as file:
	file.write(str(soup))