# ./RICAP/interface.py

import PySimpleGUI as sg

import create_pdf as cp
import printer as pr
import remove_blank as rb
import remove_md as rm
from message import windows_message as display_message

str_list = {
    "text_background": "#FFFFFF",
    "text_color": "#000000",
    "message_title": "MENSAGEM DO SISTEMA",
    "title_back": "#000000",
    "title_color": "#FFFFFF",
    "title_text": "Bot Simples Para Tratar Relatórios"
}
sg.PySimpleGUI.SYMBOL_TITLEBAR_MINIMIZE = "-"

temp = ""


def run():
    """
    runs the GUI and other events
    """
    def create_text(key):
        return sg.Text("",
                       background_color=str_list["text_background"],
                       text_color=str_list["text_color"],
                       auto_size_text=True,
                       expand_x=True,
                       key=key
                       )

    def create_button(caption, key, size=(30, 2), enabled=True, events=True):
        return sg.Button(caption.center(30),
                         key=key,
                         size=size,
                         auto_size_button=True,
                         enable_events=events,
                         disabled=not enabled
                         )

    def create_button_menu(caption, menu_items, key, size=(30, 2), enabled=True):
        return sg.ButtonMenu(caption.center(30),
                             menu_def=menu_items,
                             key=key,
                             size=size,
                             auto_size_button=True,
                             text_color="green" if enabled else "gray"
                             )

    layout = [
        [sg.Titlebar(title=str_list["title_text"],
                     icon=sg.EMOJI_BASE64_HAPPY_IDEA,
                     text_color=str_list["title_color"],
                     background_color=str_list["title_back"],
                     font=("Courier New", 20, "bold"))],

        [create_button("Relatório padrão",
                       "default_report",
                       enabled=False), create_text("t6")],

        [create_button("Remover folhas em branco",
                       "remove_blank"
                       ), create_text("t5")],

        [create_button_menu("Imprimir relatórios",
                            ["impressoras", [_ for _ in pr.getimp()]],
                            key="to_print",
                            size=(30, 2),
                            enabled=True), create_text("t4")],

        [create_button("Remover marcações de controle",
                       "remove_markdown"
                       ), create_text("t3")],

        [create_button("Converter em pdf",
                       "to_pdf"
                       ), create_text("t2")],

        [sg.FolderBrowse(initial_folder="%userprofile%\\documents",
                         auto_size_button=True,
                         size=(6, 1),
                         key="path_string",
                         enable_events=True
                         ), create_text("t1")]
    ]

    window = sg.Window(str_list["title_text"],
                       layout,
                       font=("Helvetica", " 15"),
                       default_button_element_size=(8, 2),
                       use_default_focus=False,
                       resizable=True,
                       modal=True,
                       location=(0, 0),
                       ).finalize()

    while True:
        try:
            event, values = window.read(timeout=100)

            if event in (sg.WIN_CLOSED, "EXIT"):
                break

            if values["path_string"]:
                handle = cp.converter()
                handle.map_path(values["path_string"], param="Gpr")
                pdf, nomarks, normal, txt = pr.separete(handle.arch_list)
                file_types = {
                    "t2": pdf,
                    "t3": nomarks,
                    "t4": normal,
                    "t5": normal,
                    "t6": txt
                }
                for label, fil in file_types.items():
                    window[label].update(f"Há {len(fil)} arquivos deste tipo")

            if event == "remove_blank":
                rb.remove_blankpage(values["path_string"])
                display_message(
                    "FOLHAS EM BRANCO REMOVIDAS",
                    str_list["message_title"]
                                )

            if event == "remove_markdown":
                temporary_obj = rm.controlmark()
                temporary_obj.rem_fromallfiles(values["path_string"])
                del temporary_obj
                display_message(
                    "MARCAÇÕES DE CONTROLE PARA IMPRESSORA REMOVIDOS",
                    str_list["message_title"]
                )

            if event == "to_pdf":
                temporary_obj = cp.converter()
                temporary_obj.map_path(values["path_string"])
                temporary_obj.convert()
                del temporary_obj
                display_message(
                    "OS ARQUIVOS EM TXT FORAM CONVERTIDOS PARA PDF",
                    str_list["message_title"]
                )

            if event == "to_print":
                for path in normal:
                    dir = path.replace(r"/", "\\")
                    pr.net_printer(values["to_print"], dir)
                display_message(
                    "ARQUIVOS SENDO IMPRIMIDOS"
                )
        except Exception as erro:
            display_message(
                f"erro: {erro}"
            )

    window.close()


if __name__ == "__main__":
    run()
