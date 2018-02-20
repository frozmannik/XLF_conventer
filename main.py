import os
from xml.etree.ElementTree import ElementTree
from xml.etree.ElementTree import Element
import xml.etree.ElementTree as etree
import codecs

file_name = "ex3.xlf"  #original file (version 2)

new_file = os.path.abspath(os.path.join('files', "new.xlf"))  # new file
file_path = os.path.abspath(os.path.join('files', file_name)) # path to xliff files

dom = etree.parse(file_path)
old_root = dom.getroot()

srcLang = old_root.attrib['srcLang']
trgLang = old_root.attrib['trgLang']

# print etree.tostring(old_root)  print whole file
tags =[]

for c in old_root:
    tags.append([c.tag,c.attrib])
    tagID = c.attrib['id']

    try:  # try tags if they exist in original file
        original = c.attrib['original']
    except KeyError:
        original = ""


    #print (c.tag, c.attrib)



root = Element('xliff')
tree = ElementTree(root)
name = Element('file')
root.append(name)

#name.text = 'original ="' + str(original) + '" source-language="'+ str(srcLang)

root.set('version','1.2')
name.set('original',original)
name.set('source-language',srcLang)
name.set('target-language',trgLang)

body = Element('body')
root.append(body)


units = old_root.findall('unit')
cont = dict() # container for translation units

for part in old_root: # go throw whole xml
    for unit in part: #find unit
        if unit.tag.endswith('unit'):  #find <unit>
           #trans_unit.set('id',unit.attrib['id'])  # create trans unit in new file
           #cont.append(unit.attrib['id'])  # add value in container
           #print unit.attrib['id']

           for segment in unit: # find segment
               cont[unit.attrib['id']]=[]
               for element in segment:  #find source and target

                   if element.tag.endswith('source'):
                       cont[(unit.attrib['id'])].append(element.text)
                   if element.tag.endswith('target'):
                       cont[(unit.attrib['id'])].append(element.text)


for x in cont:
    print x
    print cont[x][0]
    trans_unit = Element('trans-unit')
    body.append(trans_unit)
    trans_unit.set('id',x)

    source = Element('source')
    trans_unit.append(source)
    source.set('xml:lang',srcLang)
    source.text = cont[x][0]

    target = Element('target')
    trans_unit.append(target)
    target.set('xml:lang',trgLang)
    target.text = cont[x][1]

        #print (element.tag, "::", element.attrib)

        #print element.attrib['id']
#print etree.tostring(root)


tree.write(open(new_file.encode("UTF-8"), 'w'))


