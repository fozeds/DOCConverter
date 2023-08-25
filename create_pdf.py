# ./RICAP/create_pdf.py

from os import listdir, remove
from os.path import join

from reportlab.pdfgen import canvas


class converter():

    def __init__(self) -> None:
        self.arch_list: list = []
        self.output = ".pdf"

    def map_path(self, folder_path: str, printer=None, param="NoMarks") -> None:
        self.arch_list = [_ for _ in listdir(folder_path) if param in _]
        self.arch_list = [join(folder_path, _) for _ in self.arch_list]
        if printer:
            print(self.arch_list)

    def convert(self) -> None:
        for archive in self.arch_list:
            output_name = archive[:-4] + self.output
            with open(archive, 'r', encoding='utf-8') as file:
                content = file.read()
            lines = content.splitlines()
            y_sizelocation = 1190
            page = canvas.Canvas(output_name, pagesize=(1800, y_sizelocation))
            page.setFont("Courier", 12)
            for line in lines:
                y_sizelocation -= 20
                page.drawString(30, y_sizelocation, line)
                if "Considerando somente" in line:
                    page.showPage()
                    y_sizelocation = 1190
                    page.setFont("Courier", 12)
            page.save()
            remove(archive)


if __name__ == "__main__":
    main = converter()
    main.map_path("./")
    main.convert()
