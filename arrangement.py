import os


def setting_address():
    while True:

        try:

            address = input("ENTER ABSOLUTE LOCATION OF bin FOLDER : ").replace("\\", "/")

            if address[3] != "/": address = address[:3] + "/" + address[3:]

            os.chdir(address)

            if "bin" == os.getcwd()[-3:]: return address

            else: print("ERROR, THIS FOLDER IS NOT bin.")

        except FileNotFoundError or OSError: print("ERROR, INVALID LOCATION.")


if __name__ == "__main__":

    process = {i[6:-4]: i for i in os.listdir(setting_address())}

    result = ((process[v], f"{i:0>3}" + process[v][3:]) for i, v in enumerate(sorted(list(process.keys()))))

    for i in result: os.rename(next(i), next(i))

    input("\nPRESS ANY KEY TO EXIT.\n")
