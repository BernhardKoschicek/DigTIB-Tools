import re
#filenames = ['tib1_output.txt', 'tib2_output.txt', 'tib3_output.txt', 'tib4_output.txt', 'tib5_output.txt',
#             'tib6_output.txt', 'tib7_output.txt', 'tib8_output.txt']
exclude = ("BOOR", "Innoc.", "SVORONOS","TAFEL-THOMAS","BEES","DELATTE","NESBITT-WITTA","GIANNOPULOS","KRETSCHMER",
           "KADAS","EUSTRATIADES","MOTZO","DELATTE","Arvanid","TOPPING","KRETSCHMER","Lettres","BOMBACI","JAUBERT",
           "SARROS","BEKKER","Ktitorikon","MM","HOPF","AVEZAC","THALL","Mich.","Beit Hanīs","GALLAY","VASILIEV","Armeniorum",
           "OSKIAN","FAVRE","GOTEIN","DAGRON","SANJIAN","ALISHAN","Yāqūt","Barhebraeus","MANSI","GOUILLARD","Theod.",
           "Theoph.","Syr.","SCHIR","Schriftstücke","BENEŠEVIĆ","İNALCIK","AGOROPULU","FEISSEL","Taxinitis",
           "Chronography","Tzetz.","Test.","Pach.","Suppl.","ΜOTZO")
filenames = []

for i in range(1, 13):
    c = str(13)  # str(i)
    input = "register/tib"+c+"_input.txt"
    output = "register/tib"+c+"_output.xml"
    filenames.append(output)
    reg = re.compile('.[>].*')
    results = []
    with open(input, mode="r", encoding="utf8") as file:
        for line in file:

            # Alle Spaces entfernen:http://stackoverflow.com/questions/8270092/python-remove-all-whitespace-in-a-string
            # Das Problem ist, dass ich ja teilweise auch Sätze habe
            # line = ''.join(line.split())
            if line.strip():
                #print(line)
                #line = line.replace(",", " ")
                #print(line)
                """line = line.replace("[", "<i>")
                line = line.replace("]", "</i>")
                line = line.replace("{", "<b>")
                line = line.replace("}", "</b>")"""
                out = {"text": "<toponym>", "pages": "", "pointer": "<pointer>", "tib": "<tib>TIB "+c+"</tib>"}
                #
                if re.search(".[\>].*", line):
                    reg = re.search(".[\>].*", line)
                    find = re.findall(".[\>].*", line)
                    str1 = ''.join(find)
                    out["pointer"] += str1
                    m = reg.span()
                    line = line[0:m[0]]

                if any(s in line for s in exclude):
                    #alle ausnahme werden in die liste exclude eingetragen. Wenn ein wort vorkommt dann konnt nächstes file
                        print(line)
                else:
                    line = line.split()
                    for i in line:
                        if i.strip():
                            if i[0].isdigit():
                                i = i.replace("A.", " A. ")
                                out["pages"] += i + " "
                            elif i.startswith("A."):
                                out["pages"] += i + " "
                            elif i.startswith("TIB12"):
                                out["pointer"] += "-> TIB 12"
                            elif i.startswith("TIB11"):
                                out["pointer"] += "-> TIB 11"
                            elif i.startswith("TIB10"):
                                out["pointer"] += "-> TIB 10"
                            elif i.startswith("TIB9"):
                                out["pointer"] += "-> TIB 9"
                            elif i.startswith("TIB8"):
                                out["pointer"] += "-> TIB 8"
                            elif i.startswith("TIB7"):
                                out["pointer"] += "-> TIB 7"
                            elif i.startswith("TIB6"):
                                out["pointer"] += "-> TIB 6"
                            elif i.startswith("TIB5"):
                                out["pointer"] += "-> TIB 5"
                            elif i.startswith("TIB4"):
                                out["pointer"] += "-> TIB 4"
                            elif i.startswith("TIB3"):
                                out["pointer"] += "-> TIB 3"
                            elif i.startswith("TIB2"):
                                out["pointer"] += "-> TIB 2"
                            elif i.startswith("TIB1"):
                                out["pointer"] += "-> TIB 1"
                            else:
                                out["text"] += i + " "
                    out["text"] += "</toponym>"
            # Nicht elegant, aber es löscht die letzten zwei Chars von den Pages, ein Char ist ein Whitespace
            # und dann kommt das Komma. Muss kontrolliert werden ob das so wirklich überall passt. aber sollte schon sein
                    #p = out["pages"]
                    out["pages"] = "<pages>" + out["pages"] + "</pages>"
                    #out["pages"] += "</td>"
                    out["pointer"] += "</pointer>"
                    results.append(out)
                    #print(out)

    print(results)


    with open(output, mode="w", encoding="utf-8") as file:
        file.write("<tib-volume>"+ "\n")
        for d in results:
            file.write("<lemma>" + "\n")
            file.write(d["text"] + "\n")
            file.write(d["pages"] + "\n")
            file.write(d["pointer"] + "\n")
            file.write(d["tib"] + "\n")
            file.write("</lemma>\n")
        file.write("</tib-volume>"+ "\n")



    #Hier muss man jetzt echt mit regex arbeiten. Alle kursiven Namen sind mit <> gekennzeichnet. die muss man ggf. zusammenbringen
    #frage ist halt wie zahlen und andere namen extrahiert werden...
    #
    # Abstände sollten weggelöscht werden beim file in
    # if > Abstand und Zahl bzw buchstabe von A-Z, a-z, Sonderzeichen wie . :  und dann Abstand und und Zahl steht

with open('register/tib_all.xml', mode="w", encoding="utf8") as outfile:
    for fname in filenames:
        with open(fname, encoding="utf8") as infile:
            for line in infile:
                #print(line)
                outfile.write(line)
