from time import strftime, localtime
from openpyxl import load_workbook
from multiprocessing import Pool
from datetime import datetime
from glob import glob
import docx2txt
import olefile
import getpass
import pickle
import os


def search(path: str):

    result = list()

    def process():

        try:

            if v == "*.docx": return docx2txt.process(u)

            elif v == "*.hwp": return olefile.OleFileIO(u).openstream('PrvText').read().decode('UTF-16')

            elif v == "*.xlsx": return tuple(tuple(k.value for k in j) for j in load_workbook(u, data_only=True).active.rows)

        except OSError: return

    for p, ds, fs in os.walk(path):

        if not os.access(path, os.X_OK): return

        for v in ("*.hwp", "*.xlsx", "*.docx"):

            for u in glob(os.path.join(p, v)):

                data = process()

                if not data: continue

                st = os.stat(p)

                dates = (strftime("%y.%m.%d", localtime(s)) for s in (st.st_ctime, st.st_mtime))

                result.append({"PATH": p, "NAME": u, "DATE_CREATED": next(dates), "DATE_MODIFIED": next(dates), "DATA": data})

    return result


if __name__ == '__main__':

    origin, now, partial, pool = "./bin", datetime.now(), "C://Users/" + getpass.getuser(), Pool(processes=4)

    if "OneDrive" not in os.listdir(partial): desktop, document = partial + "/Desktop", partial + "/Documents"

    else: desktop, document = partial + "/OneDrive/바탕 화면", partial + "/OneDrive/문서"

    info = dict(zip(("D_Drive", "DESKTOP", "DOCUMENT"), pool.map(search, ("D:/", desktop, document))))

    info["WHEN"] = f"{str(now.year)[2:]}.{now.month:0>2}.{now.day:0>2}.{now.hour:0>2}:{now.minute:0>2}:{now.second:0>2}"

    file_name = f"{int(os.listdir(origin)[-1][:3]) + 1 if os.stat(origin).st_size else 0:0>3}_&_{info['WHEN']}.txt".replace(":", ".")

    with open(origin + f"\\{file_name}", "w+b") as f: pickle.dump(info, f)
