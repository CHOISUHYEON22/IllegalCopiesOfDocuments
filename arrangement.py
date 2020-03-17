import os


def setting_address():
    while True:

        try:

            address = input("ENTER ABSOLUTE LOCATION OF bin FOLDER : ").replace("\\", "\\")

            if address[-3:] == "bin": break

            else: print("ERROR, THIS FOLDER IS NOT bin.\n")

        except (FileNotFoundError, OSError): print("ERROR, INVALID LOCATION.\n")

    print()

    os.chdir(address)

    return address


if __name__ == "__main__":

    process = {i[6:-4]: i for i in os.listdir(setting_address())}

    result = ((process[v], f"{i:0>3}" + process[v][3:]) for i, v in enumerate(sorted(list(process.keys()))))

    for i in result: os.rename(next(i), next(i))

    input("\nPRESS ANY KEY TO EXIT.\n")
