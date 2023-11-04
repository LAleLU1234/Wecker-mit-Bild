import tkinter as tk
from PIL import Image, ImageTk
import datetime
import time
import threading
import pygame

def custom_messagebox(title, message, geometry):
    # Erstellen eines TopLevel-Fensters als Dialog
    dialog = tk.Toplevel(root)
    dialog.title(title)
    dialog.geometry(geometry)  # Setzen Sie die Position des Dialogs
    tk.Label(dialog, text=message).pack(pady=10)
    button = tk.Button(dialog, text="OK", command=dialog.destroy)
    button.pack(pady=5)
    dialog.transient(root)  # Machen Sie den Dialog transient zum Hauptfenster
    dialog.grab_set()  # Setzen Sie den Fokus auf den Dialog
    root.wait_window(dialog)  # Warten Sie, bis der Dialog geschlossen wird

def alarm_setzen(weckzeit):
    pygame.mixer.init()
    while True:
        aktuelle_zeit = datetime.datetime.now().time()
        if (aktuelle_zeit.hour, aktuelle_zeit.minute, aktuelle_zeit.second) >= (weckzeit.hour, weckzeit.minute, 0):
            try:
                pygame.mixer.music.load('/home/lappi/Schreibtisch/hereagain/wecker/alarm.mp3')
                pygame.mixer.music.play()
            except pygame.error:
                custom_messagebox("Fehler", "Die Alarmdatei konnte nicht geladen werden.", "+130+145")  # Anpassen der Position
            break
        time.sleep(20)

def weckzeit_starten():
    weckzeit_str = e_weckzeit.get()
    try:
        weckzeit = datetime.datetime.strptime(weckzeit_str, "%H:%M").time()
        custom_messagebox("Wecker gestellt", f"Der Wecker ist gestellt auf {weckzeit} Uhr.", "+1030+145")  # Anpassen der Position
        threading.Thread(target=alarm_setzen, args=(weckzeit,), daemon=True).start()
    except ValueError:
        custom_messagebox("Fehler", "Das Format der Zeit war nicht korrekt. Bitte verwende das Format HH:MM.", "+1030+145")  # Anpassen der Position

def bild_einfuegen(pfad):
    try:
        bild = Image.open(pfad).resize((300, 400), Image.Resampling.LANCZOS)
        bild_tk = ImageTk.PhotoImage(bild)
        bild_label = tk.Label(root, image=bild_tk)
        bild_label.image = bild_tk
        bild_label.pack(expand=True)
    except FileNotFoundError:
        custom_messagebox("Fehler", "Das Bild konnte nicht gefunden werden.", "+1030+145")  # Anpassen der Position

root = tk.Tk()
root.title("Wecker")
root.geometry("330x750+1000+100")

lbl_weckzeit = tk.Label(root, text="Weckzeit (HH:MM):")
lbl_weckzeit.pack(pady=5)

e_weckzeit = tk.Entry(root)
e_weckzeit.pack(pady=5)

btn_stellen = tk.Button(root, text="Wecker stellen", command=weckzeit_starten)
btn_stellen.pack(pady=10)

bild_einfuegen('/home/lappi/Schreibtisch/hereagain/wecker/bild.jpg')

root.mainloop()
