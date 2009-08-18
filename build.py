#coding:utf-8
import sys
reload(sys)
sys.setdefaultencoding("utf-8")

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

from mako.lookup import TemplateLookup
from os import walk
from collections import defaultdict
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
                if number == "init":
                    title = pathfile.read().strip()
                    chapter_title_dict[chapter] = title
                elif number.isdigit():
                    number = int(number)
                    chapter_content_dict[chapter].append( (number , pathfile.read().lstrip()) )


for k,v in list(chapter_content_dict.items()):
    chapter_content_dict[k]=[
        i for n,i in sorted(v,key=lambda x:x[0])
    ]

chapter_list = chapter_title_dict.keys()
chapter_list.sort()

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



