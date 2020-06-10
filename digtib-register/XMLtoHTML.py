import os
import re
import string

import bs4

source = "C:/Users/bkoschicek/Desktop/Python/dig-tib/register/better/"  # this is where the tgn files are
target = "C:/Users/bkoschicek/Desktop/Python/dig-tib/register/better/linked/"  # the original dispatch files

lof = os.listdir(source)
result = []
tibname = ""


def getXML():
    for f in lof:
        tib = []
        dump = []
        filename, ext = os.path.splitext(f)
        if f.startswith("tib"):
            file = open(source + f, 'r', encoding="utf8")
            tibname = re.findall(r'[0-9]+', f)
            pdfLink = 'https://tib.oeaw.ac.at/reader/TIB/tib' + str(tibname[0]).strip(
                '[]') + '.html#page/'
            soup = bs4.BeautifulSoup(''.join(file), features="lxml")
            for l in soup.find_all('lemma'):
                tmp = []
                for p in l.pages:
                    if isinstance(p, bs4.element.Tag):
                        text = p.text
                        text = text.replace(" ", "")
                        if '—' in text:
                            linknumber = text.split('—')
                            linknumber = str(linknumber[0].strip('[]')).replace(" ", "").replace(
                                "\n", "")
                            link = pdfLink + ''.join(linknumber)
                            e = '<a href="' + link + '" target="_blank">' + text + '</a>'
                            tmp.append("<b>" + e + "</b>")
                        elif text.isspace():
                            dump.append(text)
                        elif not text:
                            pass
                        else:
                            linknumber = re.findall(r'[0-9]+', text)
                            link = pdfLink + ''.join(linknumber)
                            e = '<a href="' + link + '" target="_blank">' + text + '</a>'
                            tmp.append("<b>" + e + "</b>")
                    else:
                        currentline = p.split(",")
                        for n in currentline:
                            if n.startswith(' u. A.'):
                                tmp.append(n)
                            elif n.startswith(' A.'):
                                tmp.append(n)
                            elif n.isspace():
                                dump.append(n)
                            elif not n:
                                pass
                            elif '—' in n:
                                n = n.split('—')
                                n = str(n[0].strip('[]')).replace(" ", "").replace("\n", "")
                                link = pdfLink + n
                                entry = '<a href="' + link + '" target="_blank">' + n + '</a>'
                                tmp.append(entry)
                            else:
                                number = re.findall(r'[0-9]+', n)
                                link = pdfLink + ''.join(number)
                                entry = '<a href="' + link + '" target="_blank">' + n.replace(" ",
                                                                                              "") + '</a>'
                                tmp.append(entry)
                if l.pointer.string is None:
                    poi = ""
                else:
                    poi = l.pointer.string
                d = {
                    'toponym': l.toponym.string,
                    'pages': ', '.join(tmp),
                    'pointer': poi,
                    'tib': l.tib.string
                }
                # print(d)
                tib.append(d)
            result.append(tib)
            print(f)
            writeHTML(tibname, tib)


def writeHTML(tibname, liste):
    filename = 'tib' + str(tibname[0]).strip('[]') + '_output'
    print(target + filename)
    print(liste)
    with open(target + filename + ".txt", mode="w", encoding="utf-8") as file:
        for d in liste:
            file.write("<tr>")
            file.write("<td>" + d["toponym"] + "</td>")
            file.write("<td>" + d["pages"] + "</td>")
            file.write("<td>" + d["pointer"] + "</td>")
            file.write("<td>" + d["tib"] + "</td>")
            file.write("</tr>\n")


def write_all():
    print(result)
    with open(target + "tib_all" + ".txt", mode="w", encoding="utf-8") as file:
        for l in result:
            for d in l:
                file.write("<tr>")
                file.write("<td>" + d["toponym"] + "</td>")
                file.write("<td>" + d["pages"] + "</td>")
                file.write("<td>" + d["pointer"] + "</td>")
                file.write("<td>" + d["tib"] + "</td>")
                file.write("</tr>\n")


getXML()
# write_all()
