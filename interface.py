# ./RICAP/interface.py

import PySimpleGUI as sg

import create_pdf as cp
import printer as pr
import remove_blank as rb
import remove_md as rm
from message import windows_message as display_message

const_l = {
    "text_background": "#FFFFFF",
    "text_color": "#000000",
    "message_title": "MENSAGEM DO SISTEMA",
    "title_back": "#000000",
    "title_color": "#FFFFFF",
    "title_text": "Bot Simples Para Tratar Relatórios",
    "row": "#E0E0E0",
    "title font": "Courier New",

}
sg.PySimpleGUI.SYMBOL_TITLEBAR_MINIMIZE = "-"
prt_choices: list = []


def run():
    """
    runs the GUI and other events
    """
    def create_text(key) -> sg.Text:
        return sg.Text("",
                       background_color=const_l["text_background"],
                       text_color=const_l["text_color"],
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

    def create_button_menu(caption, menu_items,
                           key, size=(30, 2), enabled=True) -> sg.ButtonMenu:
        return sg.ButtonMenu(caption.center(30),
                             menu_def=menu_items,
                             key=key,
                             size=size,
                             auto_size_button=True,
                             text_color="green" if enabled else "gray"
                             )

    layout = [
        [sg.Titlebar(title=const_l["title_text"],
                     icon=sg.EMOJI_BASE64_HAPPY_IDEA,
                     text_color=const_l["title_color"],
                     background_color=const_l["title_back"],
                     font=(const_l["title font"], 20, "bold"))],

        [sg.FolderBrowse(initial_folder="%userprofile%\\documents",
                         auto_size_button=True,
                         size=(6, 1),
                         key="path_string",
                         enable_events=True
                         ), create_text("t1")],

        [create_button("Relatório padrão",
                       "default_report",
                       enabled=False), create_text("t6")],

        [create_button("Converter em pdf",
                       "to_pdf"
                       ), create_text("t2")],

        [create_button("Remover marcações de controle",
                       "remove_markdown"
                       ), create_text("t3")],

        [create_button_menu("Imprimir relatórios",
                            ["impressoras", [_ for _ in pr.getimp()]],
                            key="to_print",
                            size=(30, 2),
                            enabled=True), create_text("t4")],

        [create_button("Remover folhas em branco",
                       "remove_blank"
                       ), create_text("t5")],

        [sg.Table(values=[],
                  headings=["Arquivos"],
                  expand_x=True,
                  expand_y=True,
                  # display_row_numbers=True,
                  justification="center",
                  # alternating_row_color="#000000",
                  key="-TABLE-",
                  enable_click_events=True,
                  visible=False,
                  )],
    ]

    window = sg.Window(const_l["title_text"],
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
                pdf, nomarks, ptble_files, txt = pr.separete(handle.arch_list)
                file_types = {
                    "t2": pdf,
                    "t3": nomarks,
                    "t4": ptble_files,
                    "t5": ptble_files,
                    "t6": txt
                }
                tb = "-TABLE-"
                if ptble_files:
                    window[tb].Update(visible=True)
                else:
                    window[tb].Update(visible=False)
                for label, fil in file_types.items():
                    window[label].update(f"Há {len(fil)} arquivos deste tipo")
                window[tb].Update(values=[[_[-20:]] for _ in ptble_files])
                click_rows = tuple([(_, const_l["row"]) for _ in prt_choices])
                if prt_choices:
                    window[tb].update(row_colors=click_rows)
                else:
                    window[tb].update(row_colors=((0, ""),))
            if event == "remove_blank":
                rb.remove_blankpage(values["path_string"])
                display_message(
                    "FOLHAS EM BRANCO REMOVIDAS",
                    const_l["message_title"]
                                )

            if event == "remove_markdown":
                temporary_obj = rm.controlmark()
                temporary_obj.rem_fromallfiles(values["path_string"])
                del temporary_obj
                display_message(
                    "MARCAÇÕES DE CONTROLE PARA IMPRESSORA REMOVIDOS",
                    const_l["message_title"]
                )

            if event == "to_pdf":
                temporary_obj = cp.converter()
                temporary_obj.map_path(values["path_string"])
                temporary_obj.convert()
                del temporary_obj
                display_message(
                    "OS ARQUIVOS EM TXT FORAM CONVERTIDOS PARA PDF",
                    const_l["message_title"]
                )

            if event == "to_print":
                for path_index, path in enumerate(ptble_files):
                    if path_index not in prt_choices:
                        continue
                    dir = path.replace(r"/", "\\")
                    pr.net_printer(values["to_print"], dir)
                display_message(
                    "ARQUIVOS SENDO IMPRESSOS"
                )
                prt_choices.clear()
                print(prt_choices)

            if isinstance(event, tuple):
                _ = event[2][0]
                if _ in prt_choices:
                    prt_choices.remove(_)
                else:
                    prt_choices.append(_)

        except Exception as erro:
            display_message(
                f"erro: {erro}"
            )

    window.close()


if __name__ == "__main__":
    run()
