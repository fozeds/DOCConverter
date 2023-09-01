# ./RICAP/remove_blank.py

from os import remove as remove_file

from create_pdf import converter

PAGE_BREAK_TEXT_SENSOR = "Considerando somente"
REMOVE_PAGE_SENSOR = "0 RECLAMANTES E    0 RECLAMATORIAS"
AUX_REMOVE_PAGE = "0 RECLAMANTES E    0 DEPOSITOS"


def remove_blankpage(path_: str, param_=".txt") -> None:

    file_list = converter()
    file_list.map_path(path_, printer=None, param=param_)

# main
    for relatory in file_list.arch_list:

        text = ""
        pages: list[str] = []

        for linha in open(relatory, "r"):
            if PAGE_BREAK_TEXT_SENSOR in linha:
                text += linha
                pages.append(text)
                text = ""
            else:
                text += linha
        pages.append(text)
        pages = [x for x in pages if REMOVE_PAGE_SENSOR not in x]
        pages = [x for x in pages if AUX_REMOVE_PAGE not in x]
        if len(pages) == 0:
            remove_file(relatory)
            continue
        data = pages[0][pages[0].index("BASE:")+6:pages[0].index("BASE:")+20].strip()
        data = data[:3]+"_"+data[-4:]
        remove_file(relatory)
        teste = open(f"{relatory[0:-4]}_{data}_NB", "at")
        teste.write("".join(pages))


if __name__ == "__main__":
    remove_blankpage(".\\")
