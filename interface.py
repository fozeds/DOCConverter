# ./RICAP/interface.py

import PySimpleGUI as sg

import create_pdf as cp
import printer as pr
import remove_blank as rb
import remove_md as rm
from message import windows_message as display_message

const_l = {
    "text_background": "#0C1420",
    "text_color": "#FFFFFF",
    "message_title": "MENSAGEM DO SISTEMA",
    "title_back": "#1E2733",
    "title_color": "#FFD700",
    "title_text": "Bot Simples Para Tratar Relatórios",
    "row": "#35465C",
    "title font": "Arial",

}
sg.PySimpleGUI.SYMBOL_TITLEBAR_MINIMIZE = "-"
prt_choices: list = []
change_src = ""


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
                         disabled=True,
                         button_color="#001F3F",
                         mouseover_colors="#2E4057",
                         )

    def create_button_menu(caption, menu_items,
                           key, size=(25, 2)) -> sg.ButtonMenu:
        return sg.ButtonMenu(caption.center(30),
                             menu_def=menu_items,
                             key=key,
                             size=size,
                             auto_size_button=True,
                             text_color="#001F3F",
                             visible=False,
                             button_color="#001F3F",
                             background_color="#2E4057",
                             )

    title = sg.Titlebar(title=const_l["title_text"],
                        icon=sg.EMOJI_BASE64_HAPPY_IDEA,
                        text_color=const_l["title_color"],
                        background_color=const_l["title_back"],
                        font=(const_l["title font"], 18, "bold"))

    browser = sg.FolderBrowse(initial_folder="%userprofile%\\documents",
                              auto_size_button=True,
                              size=(6, 1),
                              key="path_string",
                              enable_events=True,
                              button_color="#001F3F",
                              ), create_text("t1")

    default_relatory = create_button("Relatórios não analisados",
                                     "default_report"), create_text("t6")

    nomarks_to_pdf = create_button("Converter em pdf",
                                   "to_pdf"
                                   ), create_text("t2")

    nomarks_rel = create_button("Remover marcações",
                                "remove_markdown"
                                ), create_text("t3")

    printable = create_button_menu("Imprimir Arquivos Selecionados",
                                   ["impressoras", [_ for _ in pr.getimp()]],
                                   key="to_print"), create_text("t4")

    rem_blank = create_button("Organizar relatórios",
                              "remove_blank"
                              ), create_text("t5")

    printer_table = sg.Table(values=[],
                             headings=["Arquivos"],
                             expand_x=True,
                             expand_y=True,
                             # display_row_numbers=True,
                             justification="center",
                             # alternating_row_color="#000000",
                             key="-TABLE-",
                             enable_click_events=True,
                             visible=False,
                             )
    layout = [

        [title],

        [browser],

        [default_relatory],

        [rem_blank],

        [nomarks_rel],

        [nomarks_to_pdf],

        [printable],

        [printer_table],
    ]

    window = sg.Window(const_l["title_text"],
                       layout,
                       font=("Helvetica Neue", " 14"),
                       default_button_element_size=(8, 2),
                       use_default_focus=True,
                       resizable=True,
                       modal=True,
                       location=(0, 0),
                       background_color="#02060E",
                       border_depth=2,
                       sbar_arrow_color="#AAB8C2",
                       sbar_frame_color="#35465C",
                       titlebar_background_color="#0C1420",
                       right_click_menu_selected_colors="#35465C",
                       right_click_menu_disabled_text_color="#697C96",
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
                    "t2": nomarks,
                    "t3": ptble_files,
                    "t4": prt_choices,
                    "t5": txt,
                    "t6": txt
                }

                tb = "-TABLE-"
                window[tb].Update(visible=bool(ptble_files))
                for label, fil in file_types.items():
                    window[label].update(f"{len(fil)} arquivos selecionados".center(30))
                
                window[tb].Update(values=[[_[-20:]] for _ in ptble_files])
                
                click_rows = tuple([(_, const_l["row"]) for _ in prt_choices])
                window[tb].update(row_colors=click_rows) if prt_choices else window[tb].update(row_colors=((0, ""),))
                if (0, const_l["row"]) not in click_rows:
                     window[tb].update(row_colors=((0, ""),))
                window["remove_blank"].update(disabled=not bool(txt))
                window["to_pdf"].update(disabled=not bool(nomarks))
                window["remove_markdown"].update(disabled=not bool(ptble_files))

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

            if event == "to_pdf" and nomarks:
                temporary_obj = cp.converter()
                temporary_obj.map_path(values["path_string"])
                temporary_obj.convert()
                del temporary_obj
                display_message(
                    "OS ARQUIVOS EM TXT FORAM CONVERTIDOS PARA PDF",
                    const_l["message_title"]
                )

            if prt_choices:
                window["to_print"].update(visible=True)
            else:
                window["to_print"].update(visible=False)

            if event == "to_print" and ptble_files:
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
