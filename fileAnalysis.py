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

    def design(d: str): return ("\n" * 2 if d == "-" else "") + d * 170 + "\n" * 2

    def inclusion(text):

        text += design("=") + f"{k} | 자료 수 : {len(v)}"

        for j in v:

            text += design("-")

            text = reduce(lambda t, i: t + f"{i[0]} : {i[1]}\n", (i for i in tuple(j.items())[:-1]), text)[:-2]

            text += design("-") + f"DATA :\n{tabulate(j['DATA']) if '.xls' in j['NAME'][-5:] else j['DATA']}\n"

        text += design("=")

        return text

    text = f"\n총 자료 수 : {sum((len(v) for i, v in data.items() if i != 'WHEN'))}\nWHEN : {data['WHEN']}\n"

    for k, v in tuple(data.items())[:-1]: text = inclusion(text)

    return text

if __name__ == "__main__":

    origin_path = os.path.abspath(".")

    listdir = os.listdir(setting_address())

    filename = listdir[-1] if question("openRecent") == "Y" else question("fileName", tuple(listdir))

    with open(filename, "rb") as f: info = data_text(pickle.load(f)); print(info)

    os.chdir(origin_path)

    if question("wanToSave") == "Y":

        with open(f".{'/result' if 'result' in os.listdir('.') else ''}/R{filename}", "w+t", encoding="utf-8") as f: f.write(info)

    input("PRESS ANY KEY TO EXIT. ")
