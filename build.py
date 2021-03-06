#coding:utf-8
import sys
reload(sys)
sys.setdefaultencoding("utf-8")

from cStringIO import StringIO

import re
from cgi import escape
PAGE_RE = re.compile(r"(page:)(.*?)([\s|\n])")
BLOD_RE = re.compile(r"(\[\[)(.*?)(\]\])")
#BLOD_RE.sub(r'<b>\2</b>', line)
romanNumeralMap = (('M',  1000), 
                   ('CM', 900),
                   ('D',  500),
                   ('CD', 400),
                   ('C',  100),
                   ('XC', 90),
                   ('L',  50),
                   ('XL', 40),
                   ('X',  10),
                   ('IX', 9),
                   ('V',  5),
                   ('IV', 4),
                   ('I',  1))
from urllib2 import unquote
import re
linkre = re.compile(r'((?:https?://)'
                    r'[\w\-.%/=+#:~!,\'\*\^]+'
                    r'(?:\?[\w\-.%/=;+@#:~!,\'\*&$]*)?)')



def escape_link(s):
    s = str(s).decode('utf8', 'ignore').encode('utf8')
    rs=[]
    for tok in linkre.split(s):
        if linkre.match(tok) and tok not in '"<>':
            linktext = tok
            if tok.startswith('http://') or tok.startswith('https://'):
                href = tok
            else:
                href = 'http://' + tok
            rs.append("""<a target="_blank" href="%s">%s</a>""" % (href,linktext))
        else:
            rs.append(tok)
    return ''.join(rs)

def toRoman(n):
    """convert integer to Roman numeral"""
    result = ""
    for numeral, integer in romanNumeralMap:
        while n >= integer:
            result += numeral
            n -= integer
    return result

from os.path import dirname,join
PREFIX = dirname(__file__)
PREFIX_OUTPUT = join(PREFIX,"html")

from os import walk
from collections import defaultdict
from mako.lookup import TemplateLookup

lookup = TemplateLookup(
    directories=join(PREFIX,'template'),
    disable_unicode=True,
    encoding_errors="ignore",
    default_filters=['str', 'h'],
)

def render(template,*args,**kwds):
    return lookup.get_template(template).render(*args,**kwds)

chapter_title_dict={}
chapter_content_dict=defaultdict(list)
for root, dirs, files in walk(join(PREFIX,"book")):
    for file in files:
        if not file.endswith(".txt"):
            continue
        path = join(root,file).replace("\\","/")
        other,chapter, number = path.rsplit("/",2)
        number = number[:-4]
        if chapter.isdigit():
            chapter = int(chapter)
            with open(path) as pathfile:
                pathfile_read = pathfile.read()
                if number == "init":
                    title = pathfile_read.strip()
                    chapter_title_dict[chapter] = title
                elif number.isdigit():
                    number = int(number)
                    
                    chapter_content_dict[chapter].append( (number , pathfile_read.rstrip()) )


for k,v in list(chapter_content_dict.items()):
    v = sorted(v,key=lambda x:int(x[0]))
    v = [
        i for n,i in v
    ]
    chapter_content_dict[k]=v


chapter_list = chapter_title_dict.keys()
chapter_list.sort()


pre_link = None
next_link = None
for chapter in chapter_list:
    pathfile_list = chapter_content_dict.get(chapter,[])

    for filepos,pathfile_read in  enumerate(pathfile_list):
        if pathfile_read.strip():
            filename = "%s_%s.html"%(chapter,filepos)

            with open(join(PREFIX_OUTPUT,filename),"w") as index:
                pos = pathfile_read.find("\n")
                if pos==-1:
                    continue
                content = pathfile_read[pos:].strip()
                if content:
                    if filepos<len(pathfile_list)-1 and pathfile_list[filepos+1].count("\n"):
                        next_link = "%s_%s.html"%(chapter,1+filepos)
                    elif chapter!=chapter_list[-1]:
                        next_link = "%s_%s.html"%(chapter_list[chapter_list.index(chapter)+1],0)
                    else:
                        next_link = None
                    
                else:
                    continue
                content = escape(content)
                content = BLOD_RE.sub(r'<b>\2</b>', content)
                content = PAGE_RE.sub(r'<a href="page/\2" target="_blank">链接</a> ',content)
                buffer = []

                s = StringIO()
                s.write(content)
                s.seek(0)
                inpre = False
                
                for line in s:
                    line=line.rstrip()
                    line_strip = line.strip()
                    #print line
                    if line.startswith("~~"):
                        line = line.lstrip('~  ')
                        buffer.append("""<p><a href="%s">%s</a></p>"""%(line,line))
                    elif line.startswith("===") and line.endswith("==="):
                        buffer.append("<h3>%s</h3>"%line.strip(" ="))
                    elif line.startswith("==") and line.endswith("=="):
                        buffer.append("<h2>%s</h2>"%line.strip(" ="))
                    elif line_strip == "{{{":
                        inpre=True
                        buffer.append("""<div class="content"><pre>""")
                    elif line_strip == "}}}":
                        inpre=False
                        buffer.append("""</pre></div>""")
                    elif line_strip == "==&gt;":
                        buffer.append("""<blockquote>""")
                    elif line_strip == "&lt;==":
                        buffer.append("""</blockquote>""")
                    elif line_strip.startswith("----"):
                        buffer.append("""<div style="border:0;border-bottom:1px #ccc dotted;margin:40px 0;"></div>""")
                    elif line[-4:] in (".jpg",".gif",".png"):
                        alt = ""
                        link = line.rsplit(" ",1)
                        if len(link)==2:
                            alt,link = link
                        elif len(link)==1:
                            link=link[0]
                        buffer.append("""<div class="imageblock">
<div class="content">
<img alt="%s" src="img/%s"/>
</div>
"""%(alt,link))
                        if alt:
                            buffer.append("""<div class="image-title">图:%s</div>"""%alt)
                        buffer.append("""</div>""")
                    elif line:
                        line = escape_link(line)
                        if inpre:
                            buffer.append(line)
                        else:
                            buffer.append("<p>%s</p>"%line)
                    elif inpre:
                        buffer.append("")

                content = "\n".join(buffer)
                index.write(
                    render(
                        "page.html",
                        title = pathfile_read.strip().split("\n")[0],
                        content=content,
                        pre_link = pre_link,
                        next_link = next_link
                    ),
                )
                pre_link = filename


with open(join(PREFIX_OUTPUT,"index.html"),"w") as index:
    index.write(
        render(
            "index.html",
            chapter_list = chapter_list,
            chapter_number=map(toRoman,chapter_list),
            chapter_title_dict = chapter_title_dict,
            chapter_content_dict = chapter_content_dict
        ),
    )



