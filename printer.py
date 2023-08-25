# ./RICAP/printer.py

from subprocess import check_output

_cmd = check_output


def getimp():
    '''returns an generator for net view logonserver printers'''
    net = _cmd("net view %LOGONSERVER%", shell=True, text=True)
    return (_.strip().split()[0] for _ in net.splitlines() if "Imp" in _)


def net_printer(printer_name, arch_path) -> None:
    """printer by using type cmd"""
    _cmd(f"type \"{arch_path}\" > \"%LOGONSERVER%\\{printer_name}\"",
         shell=True,
         text=True
         )


def separete(paths: list) -> tuple:
    l: dict = {
        1: ".pdf",
        2: "NoMarks",
        3: "txt",
    }
    pdf = [_ for _ in paths if l[1] in _]
    nm = [_ for _ in paths if l[2] in _]
    norm = [_ for _ in paths if _ not in nm and _ not in pdf and l[3] not in _]
    txt = [_ for _ in paths if l[3] in _]
    return pdf, nm, norm, txt
