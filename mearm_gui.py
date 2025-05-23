import tkinter as tk
import serial
import threading
import time

# COM-Port anpassen!
arduino = None
try:
    arduino = serial.Serial('COM7', 9600, timeout=1) #Verbindung zu arduino
    time.sleep(2)  # Warten bis Arduino bereit(2 sek zeit zum hochfahren)
    print("Arduino verbunden.")
except serial.SerialException:
    print("⚠️  Kein Arduino gefunden. Die GUI läuft trotzdem.")

angles = {
    'base': 90,
    'shoulder': 90,
    'elbow': 90,
    'gripper': 30
}# angles speichert aktuelle Position der Servos. Werden bei start in das gui geladen 

root = tk.Tk() #tkinter Gui erschaffen. Fenster mit fester größe, titel
root.title("MeArm Steuerung")
root.geometry("400x450")

labels = {} #widget für jedes gelenk, speichern im dictionary, damit flexibler
sliders = {}

def send_to_arduino():
    if arduino:
        command = f"MOVE {angles['base']} {angles['shoulder']} {angles['elbow']} {angles['gripper']}\n"
        arduino.write(command.encode()) # baut den move befehl
    else:
        print("⚠️  Kein Arduino verbunden – Befehl nicht gesendet.")

def slider_changed(joint, val):
    angles[joint] = int(val)
    send_to_arduino() # slider wert übertragen in angles, neuen wert an arduino senden

def build_gui(): # Gui bauen
    for joint in angles:
        labels[joint] = tk.Label(root, text=f"{joint.capitalize()}: {angles[joint]}") # Label mit aktuellen Namen und Winkel
        labels[joint].pack(pady=5)

        sliders[joint] = tk.Scale( # slider von 0 bis 180grad, oben definiert  
            root, from_=0, to=180, orient=tk.HORIZONTAL, length=300,
            command=lambda val, j=joint: slider_changed(j, val) #verknüpfen mit funktion slider changed
        )
        sliders[joint].set(angles[joint])
        sliders[joint].pack()
    #Buttons
    tk.Button(root, text="Position A speichern", command=save_pos_a).pack(pady=10)
    tk.Button(root, text="Position B speichern", command=save_pos_b).pack(pady=5)
    tk.Button(root, text="Auto: A → B", command=run_auto).pack(pady=10)

def save_pos_a():
    arduino.write(b"SAVEA\n")

def save_pos_b():
    arduino.write(b"SAVEB\n")

def run_auto():
    arduino.write(b"AUTO\n")

def update_labels(): # regelmässig labels aktualisieren, mit neuen winkeln von gelenekn, alles 200ms
    for joint in angles:
        labels[joint].config(text=f"{joint.capitalize()}: {angles[joint]}")
    root.after(200, update_labels)

build_gui() #baut gui
update_labels() # startet aktualisierung
root.mainloop() # startet tkinter schleife, bis fenster geschlossen wird
