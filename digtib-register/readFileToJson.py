import re
import json
#filenames = ['tib1_output.txt', 'tib2_output.txt', 'tib3_output.txt', 'tib4_output.txt', 'tib5_output.txt',
#             'tib6_output.txt', 'tib7_output.txt', 'tib8_output.txt']
exclude = ("BOOR", "Innoc.", "SVORONOS","TAFEL-THOMAS","BEES","DELATTE","NESBITT-WITTA","GIANNOPULOS","KRETSCHMER",
           "KADAS","EUSTRATIADES","MOTZO","DELATTE","Arvanid","TOPPING","KRETSCHMER","Lettres","BOMBACI","JAUBERT",
           "SARROS","BEKKER","Ktitorikon","MM","HOPF","AVEZAC","THALL","Mich.","Beit Hanīs","GALLAY","VASILIEV","Armeniorum",
           "OSKIAN","FAVRE","GOTEIN","DAGRON","SANJIAN","ALISHAN","Yāqūt","Barhebraeus","MANSI","GOUILLARD","Theod.",
           "Theoph.","Syr.","SCHIR","Schriftstücke","BENEŠEVIĆ","İNALCIK","AGOROPULU","FEISSEL","Taxinitis",
           "Chronography","Tzetz.","Test.","Pach.","Suppl.","ΜOTZO")
filenames = []
all = []

for i in [11]:
    c = str(i)
    input = "C:/Users/bkoschicek/Desktop/DigTIB-Tools/digtib-register/tib"+c+"_input.txt"
    output = "tib"+c+"_output.json"
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
                out = {"Name": "", "Pages": "", "Notes": "", "Volume": "TIB "+c}
                #
                if re.search(".[\>].*", line):
                    reg = re.search(".[\>].*", line)
                    find = re.findall(".[\>].*", line)
                    str1 = ''.join(find)
                    out["Notes"] += str1
                    m = reg.span()
                    line = line[0:m[0]]

                if any(s in line for s in exclude):
                    #alle ausnahme werden in die liste exclude eingetragen. Wenn ein wort vorkommt dann konnt nächstes file
                        print(line)
                else:
                    line = line.split()
                    for i in line:
                        if i.strip():
                            if i.startswith("{"):
                                out["Pages"] += i.replace('}', '</b>')\
                                                    .replace('{', '<b>') + " "
                            elif i[0].isdigit():
                                i = i.replace("A.", " A. ")
                                out["Pages"] += i + " "
                            elif i.startswith("A."):
                                out["Pages"] += i + " "
                            elif i.startswith("TIB12"):
                                out["Notes"] += "-> TIB 12"
                            elif i.startswith("TIB11"):
                                out["Notes"] += "-> TIB 11"
                            elif i.startswith("TIB10"):
                                out["Notes"] += "-> TIB 10"
                            elif i.startswith("TIB9"):
                                out["Notes"] += "-> TIB 9"
                            elif i.startswith("TIB8"):
                                out["Notes"] += "-> TIB 8"
                            elif i.startswith("TIB7"):
                                out["Notes"] += "-> TIB 7"
                            elif i.startswith("TIB6"):
                                out["Notes"] += "-> TIB 6"
                            elif i.startswith("TIB5"):
                                out["Notes"] += "-> TIB 5"
                            elif i.startswith("TIB4"):
                                out["Notes"] += "-> TIB 4"
                            elif i.startswith("TIB3"):
                                out["Notes"] += "-> TIB 3"
                            elif i.startswith("TIB2"):
                                out["Notes"] += "-> TIB 2"
                            elif i.startswith("TIB1"):
                                out["Notes"] += "-> TIB 1"
                            else:
                                out["Name"] += i + " "
                    #out["text"] += "</td>"
            # Nicht elegant, aber es löscht die letzten zwei Chars von den Pages, ein Char ist ein Whitespace
            # und dann kommt das Komma. Muss kontrolliert werden ob das so wirklich überall passt. aber sollte schon sein
                    p = out["Pages"]
                    out["Pages"] = p
                    #out["pages"] += "</td>"
                    #out["pointer"] += "</td>"
                    results.append(out)

                    #print(out)

    #print(results)
    results.append(all)


    with open(output, mode="w", encoding="utf-8") as file:
        json.dump(results, file, ensure_ascii=False)
        # for d in results:
        #     file.write("<tr>")
        #     file.write(d["text"])
        #     file.write(d["pages"])
        #     file.write(d["pointer"])
        #     file.write(d["tib"])
        #     file.write("</tr>\n")



    #Hier muss man jetzt echt mit regex arbeiten. Alle kursiven Namen sind mit <> gekennzeichnet. die muss man ggf. zusammenbringen
    #frage ist halt wie zahlen und andere namen extrahiert werden...
    #
    # Abstände sollten weggelöscht werden beim file in
    # if > Abstand und Zahl bzw buchstabe von A-Z, a-z, Sonderzeichen wie . :  und dann Abstand und und Zahl steht

# with open('register/tib_all.json', mode="w", encoding="utf8") as outfile:
#     json.dump(all, outfile)
#     # for fname in filenames:
#     #     with open(fname, encoding="utf8") as infile:
#     # #         for line in infile:
#     #             #print(line)
#     #             outfile.write(line)
