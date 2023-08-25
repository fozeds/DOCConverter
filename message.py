# ./RICAP/message.py
import ctypes


def windows_message(message: str, title: str = "alert") -> None:
    ctypes.windll.user32.MessageBoxW(0, message, title, 0)
