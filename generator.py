import random
import sqlite3
from PIL import Image, ImageTk
from io import BytesIO
import tkinter as tk

#Define rarity values, probabilities and filters
rarities = [1,2,3,4,5]
probabilities = [0.3, 0.25, 0.2, 0.15, 0.1]
selected_filters = {rarity: True for rarity in rarities}

true_rng_flag = False

def trueRng():
    return random.randint(1,59)

def rngRarity():
    active_rarities = [r for r in rarities if selected_filters[r]]
    active_probabilities = [probabilities[rarities.index(r)] for r in active_rarities]

    if not active_rarities:
        active_rarities = rarities
        active_probabilities = probabilities

    return random.choices(active_rarities, weights=active_probabilities, k=1)[0]

def summonGacha():
    rarity = rngRarity()
    servant = getServantId(rarity, true_rng_flag)
    
    displayServant(servant)

def summonTrue():
    true_rng_flag = True
    servant_id = trueRng()
    servant = getServantId(servant_id, true_rng_flag)
    true_rng_flag = False

    displayServant(servant)

def displayServant(servant):
    servant_name.set(f"Name: {servant[1]}")
    servant_class.set(f"Class: {servant[3]}")
    servant_rarity.set(f"Rarity: {servant[4]}")
    image_data = servant[2]
    image = Image.open(BytesIO(image_data))
    image_tk = ImageTk.PhotoImage(image)
    servant_image_label.config(image=image_tk)
    servant_image_label.image = image_tk
    root.geometry("")

def getServantId(rarity_or_id, true_rng_flag):
    #Connect database
    conn = sqlite3.connect('Servants.db')
    cursor = conn.cursor()

    if (true_rng_flag == True):
        #Fetch servant info from id
        cursor.execute("SELECT * FROM servants WHERE id = ?", (rarity_or_id,))
    else :
        #Fetch servant info from rarity
        cursor.execute("SELECT * FROM servants WHERE rarity = ? ORDER BY random() limit 1", (rarity_or_id,))
    
    result = cursor.fetchone()
    conn.close()
    return result


def openFilterWindow():
    filter_window = tk.Toplevel(root)
    filter_window.title("Filter rarities")
    filter_window.geometry("300x200")

    tk.Label(filter_window, text="Select which rarities you would like to summon:").pack()
    checkbox_vars = {}
    for rarity in rarities:
        var = tk.BooleanVar(value=selected_filters[rarity])
        checkbox_vars[rarity] = var
        tk.Checkbutton(filter_window, text=f"{rarity}-Star", variable=var).pack(anchor="w")

    def applyFilters():
        for rarity, var in checkbox_vars.items():
            selected_filters[rarity] = var.get()
        filter_window.destroy()
    
    tk.Button(filter_window, text="Apply", command=applyFilters).pack()
    tk.Button(filter_window, text="Cancel", command=filter_window.destroy).pack()

#Tkinter setup
root = tk.Tk()
root.geometry("300x200")
root.resizable(True, True)
root.title("FGOSummon")

servant_name = tk.StringVar()
servant_class = tk.StringVar()
servant_rarity = tk.StringVar()

tk.Label(root, textvariable=servant_name).pack()
tk.Label(root, textvariable=servant_class).pack()
tk.Label(root, textvariable=servant_rarity).pack()

summon_button = tk.Button(root, text="Gacha Summon", command=summonGacha)
summon_button.pack()
true_summon_button = tk.Button(root, text="True Summon", command=summonTrue)
true_summon_button.pack()
filter_button = tk.Button(root, text="Filter", command=openFilterWindow)
filter_button.pack()

servant_image_label = tk.Label(root)
servant_image_label.pack()

root.mainloop()
