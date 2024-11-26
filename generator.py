import random
import sqlite3
from PIL import Image, ImageTk
from io import BytesIO
import tkinter as tk

#Define rarity values and probabilities
rarities = [1,2,3,4,5]
probabilities = [0.4, 0.3, 0.2, 0.08, 0.02]

#def rng() :
#    return random.randint(1,59)

def rngRarity() :
    return random.choices(rarities, weights=probabilities, k=1)[0]

def getServantId(rarity):
    #Connect database
    conn = sqlite3.connect('Servants.db')
    cursor = conn.cursor()

    #Fetch servant info from rarity
    cursor.execute("SELECT * FROM servants WHERE rarity = ? ORDER BY random() limit 1", (rarity,))
    result = cursor.fetchone()

    conn.close()
    return result

def summonServant():
    rarity = rngRarity()
    servant = getServantId(rarity)

    servant_name.set(f"Name: {servant[1]}")
    servant_class.set(f"Class: {servant[3]}")
    servant_rarity.set(f"Rarity: {servant[4]}")
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
servant_rarity = tk.StringVar()

tk.Label(root, textvariable=servant_name).pack()
tk.Label(root, textvariable=servant_class).pack()
tk.Label(root, textvariable=servant_rarity).pack()

summon_button = tk.Button(root, text="Summon Servant", command=summonServant)
summon_button.pack()

servant_image_label = tk.Label(root)
servant_image_label.pack()

root.mainloop()
