# ./RICAP/remove_md.py

import re
from os import remove

from create_pdf import converter


class controlmark():

    def __init__(self) -> None:
        self.controlmark_to_remove = (
            "l1Ol1Ss20Hl8D",
            "s0B",
            "s4B2",
            "s4B"
        )
        self.nonalpha = r"[^a-zA-Z0-9\s:|.,/+-_ ]"

    def remove_control_marks(self, line: str) -> str:
        for mark in self.controlmark_to_remove:
            line = line.replace(mark, "")
        return line

    def remove_nonalpha(self, line: str) -> str:
        return re.sub(self.nonalpha, "", line)[:-1]

    def rem_fromarchive(self, path_from_archive: str) -> None:
        with open(path_from_archive, "r") as file:
            lines = file.readlines()
        for line in lines:
            line = self.remove_nonalpha(line)
            line = self.remove_control_marks(line)
            with open(path_from_archive+"_NoMarks", "a") as new:
                new.write(line+"\n")

    def rem_fromallfiles(self, path: str) -> None:
        arch_list = converter()
        arch_list.map_path(path, param="Gpr")
        for file_path in arch_list.arch_list:
            self.rem_fromarchive(file_path)
            remove(file_path)


if __name__ == "__main__":
    main = controlmark()
    main.rem_fromallfiles(".\\")
