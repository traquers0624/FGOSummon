import random
import sqlite3
from PIL import Image, ImageTk
from io import BytesIO
import tkinter as tk

def rng() :
    return random.randint(1,59)

def getServantId(id):
    #Connect database
    conn = sqlite3.connect('Servants.db')
    cursor = conn.cursor()

    #Fetch servant info from id
    cursor.execute("SELECT * FROM servants WHERE id = ?", (id,))
    result = cursor.fetchone()

    conn.close()
    return result

def summonServant():
    random_id = rng()
    servant = getServantId(random_id)

    servant_name.set(f"Name: {servant[1]}")
    servant_class.set(f"Class: {servant[3]}")
    image_data = servant[2]
    image = Image.open(BytesIO(image_data))
    image_tk = ImageTk.PhotoImage(image)
    servant_image_label.config(image=image_tk)
    servant_image_label.image = image_tk

#Tkinter setup
root = tk.Tk()
root.title("Servant Summoning")

servant_name = tk.StringVar()
servant_class = tk.StringVar()

tk.Label(root, textvariable=servant_name).pack()
tk.Label(root, textvariable=servant_class).pack()

summon_button = tk.Button(root, text="Summon Servant", command=summonServant)
summon_button.pack()

servant_image_label = tk.Label(root)
servant_image_label.pack()

root.mainloop()
