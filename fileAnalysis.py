from arrangement import setting_address
from tabulate import tabulate
from functools import reduce
import pickle
import os


def question(ques: str, cond: tuple = ("Y", "N")):

    ques_dict = {
        "openRecent": "DO YOU WANT TO OPEN THE MOST RECENT FILE?\n[Y]es OR [N]o : ",
        "wanToSave": "DO YOU WANT TO SAVE THIS DATA?\n[Y]es OR [N]o : ",
        "fileName": "FILE NAME : "
    }

    while True:

        scan = input(ques_dict[ques])

        if scan in cond: break

        print("Please enter a valid value.\n")

    print()

    return scan


def data_text(data: dict):

    text = f"\n총 자료 수 : {sum((len(v) for i, v in data.items() if i != 'WHEN'))}\nWHEN : {data['WHEN']}\n"

    editext = lambda t, i, isx: t + f"{i[0]} : {tabulate(i[1]) if isx and i[0] == 'DATA' else i[1]}"

    for k, v in tuple(data.items())[:-1]:

        text += "=" * 100 + f"\n{k} | 자료 수 : {len(v)}\n" + "-" * 100 + "\n" * 2

        for j in v:

            isx = False if j["EXTENSION"] == '.hwp' else True

            reduce(editext, (i for i in j.items()), text)

            text += "\n"

        text += "=" * 100 + "\n" * 3

    return text

if __name__ == "__main__":

    origin_path = os.path.abspath(".")

    listdir = os.listdir(setting_address())

    filename = listdir[-1] if question("openRecent") == "Y" else question("fileName", tuple(listdir))

    with open(filename, "rb") as f: info = data_text(pickle.load(f))

    os.chdir(origin_path)

    if question("wanToSave") == "Y":

        with open(f".{'/result' if 'result' in os.listdir('.') else ''}/R{filename}", "w+t") as f: f.write(info)

    input("PRESS ANY KEY TO EXIT. ")
