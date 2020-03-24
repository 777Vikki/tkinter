from re import sub
from xml.etree.ElementTree import parse, SubElement

def findAllXliffById(root, nameSpace, attribLst):
    lst = []
    for index, item in enumerate(root.find(nameSpace+"file").find(nameSpace+"body").findall(nameSpace+"trans-unit")):
        attribTxt = sub(' +', ' ', item.attrib['id'].strip().replace('\n', ''))
        if(attribTxt in attribLst[:index] + attribLst[index+1:]):
            lst.append(findTransUnit(item, nameSpace))
    return lst

def xliffAttrib(root, nameSpace):
    attribTxtList = []
    for item in root.find(nameSpace+"file").find(nameSpace+"body").findall(nameSpace+"trans-unit"):
        attribTxtList.append(sub(' +', ' ', item.attrib['id'].strip().replace('\n', ''))) 
    return attribTxtList

def findTransUnit(xliffValue, nameSpace):
    lst = []
    lst.append(sub(' +', ' ', xliffValue.attrib['id'].strip().replace('\n', '')))
    for data in xliffValue.findall(nameSpace+'note'):
        if(data.attrib['from'] == 'description'):
            lst.append(sub(' +', ' ', data.text.strip().replace('\n', '')))
        if(data.attrib['from'] == 'meaning'):
            lst.append(sub(' +', ' ', data.text.strip().replace('\n', '')))
    if(xliffValue.find(nameSpace+'source') != None):
        sourceTxt = sub(' +', ' ', xliffValue.find(nameSpace+'source').text.replace('\n', ''))

        if(xliffValue.find(nameSpace+'source').find(nameSpace+'x') != None):
            sourceTxt = sourceTxt + "--"
    else:
        sourceTxt = ""
    lst.append(sourceTxt)
    if(xliffValue.find(nameSpace+'target') != None):
        targetTxt = sub(' +', ' ', xliffValue.find(nameSpace+'target').text.replace('\n', ''))

        if(xliffValue.find(nameSpace+'target').find(nameSpace+'x') != None):
            targetTxt = sourceTxt + "--"
    else:
        targetTxt = ""
    lst.append(targetTxt)

    return lst
def findAllTransUnit(root, nameSpace):
    lst = []
    for item in root.find(nameSpace+"file").find(nameSpace+"body").findall(nameSpace+"trans-unit"):
        xliffData = findTransUnit(item, nameSpace)
        lst.append(xliffData)
    return lst
def nameSpaceURl(root):
    return root.tag[root.tag.find("{"):root.tag.find("}")+1]

def updateAllTransUnit(root, nameSpace, excelData):
    for item in root.find(nameSpace+"file").find(nameSpace+"body").findall(nameSpace+"trans-unit"):
        attribTxt = attribTxt = sub(' +', ' ', item.attrib['id'].strip().replace('\n', ''))
        if(attribTxt in excelData.keys()):
            if(item.find(nameSpace+'target') != None):
                item.find(nameSpace+'target').text = str(excelData[attribTxt])
            else:
                SubElement(item, nameSpace+'target')
                if(excelData[attribTxt]):
                    targetTxt = excelData[attribTxt]
                else:
                    targetTxt = " "
                item.find(nameSpace+'target').text = targetTxt


def updateXliff(excelData, path):
    tree = parse(path)
    root = tree.getroot()
    nameSpace = nameSpaceURl(root)
    updateAllTransUnit(root, nameSpace, excelData)
    tree.write("vivek.xlf", encoding="UTF-8", xml_declaration=True)

def i18nXmlParsing(path):
    tree = parse(path)
    root = tree.getroot()
    nameSpace = nameSpaceURl(root)
    xliffList = findAllTransUnit(root, nameSpace)
    xliffList.insert(0, ["Trans_Id", "description", "Action/Page", "Source", "Target"])
    return xliffList

def dublicateIdParsing(path):
    tree = parse(path)
    root = tree.getroot()
    nameSpace = nameSpaceURl(root)
    attribIdLst = xliffAttrib(root, nameSpace)
    if(len(attribIdLst) != len(set(attribIdLst))):
        xliffList = findAllXliffById(root, nameSpace, attribIdLst)
        xliffList.insert(0, ["Trans_Id", "description", "Action/Page", "Source", "Target"])
        return xliffList
    else:
        return "No Dublicate Id found"