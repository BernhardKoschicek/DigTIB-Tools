# coding=utf-8
import os
import re
from builtins import open, print
from pathlib import Path

dir_ = Path('D:/TIB05')

name_list = Path(__file__).parent / 'lists' / 'tib5.txt'


def main():
    for root, dirs, files in os.walk(dir_, topdown=False):

        for name in files:
            with open(name_list, mode="r", encoding="utf-8") as file:
                for line in file:
                    src_name = re.findall("^(.*)[;]", line)
                    dst_name = re.findall(";(.*)", line)

                    dst = dst_name[0] + ".jpg"
                    dst_path = os.path.join(root, dst)

                    if name == src_name[0] + ".jpg":
                        source = os.path.join(root, name)
                        os.rename(source, dst_path)
                        print("suc: " + source + " renamed in: " + dst_path)


main()
