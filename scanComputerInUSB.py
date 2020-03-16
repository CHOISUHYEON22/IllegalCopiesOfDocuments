from openpyxl import load_workbook
from datetime import datetime
import olefile
import getpass
import pickle
import os


def search(path: str):

    global data

    result = list()

    try: os.chdir(path)

    except PermissionError: return

    for i in os.listdir(path):

        origin_path, sub_path = path, f"{path}/{i}"

        if os.path.isdir(sub_path):

            reserve = search(sub_path)

            if reserve: result.extend(reserve)

            os.chdir(origin_path)

        else:

            name, extension = os.path.splitext(i)

            if len(extension) > 0 and extension == ".hwp":

                try: data = olefile.OleFileIO(i).openstream('PrvText').read().decode('UTF-16')

                except: pass

            elif len(extension) > 0 and extension == ".xlsx":

                data = tuple(tuple(k.value for k in j) for j in load_workbook(i, data_only=True).active.rows)

            else: continue

            result.append({"PATH":path, "NAME":name, "EXTENSION":extension, "DATA":data})

    return result


if __name__ == '__main__':

    origin, now, partial = os.getcwd() + "\\bin", datetime.now(), "C://Users/" + getpass.getuser()

    if "OneDrive" not in os.listdir(partial): desktop, document = partial + "/Desktop", partial + "/Documents"

    else: desktop, document = partial + "/OneDrive/바탕 화면", partial + "/OneDrive/문서"

    info = {k: search(i) for i, k in (("D:/", "D_Drive"), (desktop, "DESKTOP"), (document, "DOCUMENT"))}

    info["WHEN"] = f"{str(now.year)[2:]}.{now.month:0>2}.{now.day:0>2}.{now.hour:0>2}:{now.minute:0>2}:{now.second:0>2}"

    os.chdir(origin)

    current = os.listdir(".")

    file_name = f"{int(current[-1][:3]) + 1 if len(current) else 0:0>3}_&_{info['WHEN']}.txt".replace(":", ".")

    with open(file_name, "w+b") as f: pickle.dump(info, f)