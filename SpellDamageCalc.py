#Sorcerer Damage calc for Hotfix 36 of Dark and Darker
import numpy as np
import matplotlib.pyplot as  plt
from enum import Enum
from caster_class import Caster_Class

import tkinter
from tkinter import ttk


def generate_graph(): 
   

    #print("Damage: " + str(dam))

    # String Building
    #roundedDam = np.round(dam,decimals=2)
    #retStr = "Total Damage: " + str(roundedDam)
    
    #disp = tkinter.Message(frame, text=retStr)
    disp.grid(row=4, column= 1, sticky="news", padx=15, pady=15)
    
window = tkinter.Tk()
window.title("Caster Damage Calc")

frame = tkinter.Frame(window)
frame.pack()

# saving user info 
draw_info_frame = tkinter.LabelFrame(frame, text ="Character Stats (Use Decimal values)")
draw_info_frame.grid(row= 0, column= 0)

draw_opp_frame = tkinter.LabelFrame(frame, text="Opponent Stats (Use Decimal values)")
draw_opp_frame.grid(row=0, column=1)

draw_spell_frame = tkinter.LabelFrame(frame, text="Spell Information (Use Decimal values)")
draw_spell_frame.grid(row=0, column=2)

MDR_label = tkinter.Label(draw_opp_frame, text="Opponent % MDR:")
MDR_label.grid(row=0, column=0,sticky="w")

projRes_label = tkinter.Label(draw_opp_frame, text="Opponent % Proj Resist:")
projRes_label.grid(row=1, column=0,sticky="w")

hsRes_label = tkinter.Label(draw_opp_frame, text="Opponent % Headshot Resist:")
hsRes_label.grid(row=2, column=0,sticky="w")

debuffDur_label = tkinter.Label(draw_opp_frame, text="Opponent % Debuff Duration:")
debuffDur_label.grid(row=3, column=0,sticky="w")

MDR_entry = tkinter.Entry(draw_opp_frame)
MDR_entry.grid(row=0, column=1)

projRes_entry = tkinter.Entry(draw_opp_frame)
projRes_entry.grid(row=1, column=1)

hsRes_entry = tkinter.Entry(draw_opp_frame)
hsRes_entry.grid(row=2, column=1)

debuffDurr_entry = tkinter.Entry(draw_opp_frame)
debuffDurr_entry.grid(row=3, column=1)

headshot_label = tkinter.Label(draw_opp_frame, text="Headshot")
headshot_combobox = ttk.Combobox(draw_opp_frame, values=["Yes", "No"])
headshot_label.grid(row=4, column=0,sticky="w")
headshot_combobox.grid(row=4, column=1)

#Defaults
MDR_entry.insert(0, 0)
projRes_entry.insert(0, 0)
hsRes_entry.insert(0, 0)
debuffDurr_entry.insert(0, 0)
headshot_combobox.insert(0, "No")

#Enhancement input
book_label = tkinter.Label(draw_info_frame, text="Casting Implement Damage:")
book_label.grid(row=0, column=0,sticky="w")

add_label = tkinter.Label(draw_info_frame, text="Additional Magic Damage:")
add_label.grid(row=1, column=0,sticky="w")

true_label = tkinter.Label(draw_info_frame, text="Additional True Magic Damage:")
true_label.grid(row=2, column=0,sticky="w")

mpb_label = tkinter.Label(draw_info_frame, text="Magic Power Bonus %:")
mpb_label.grid(row=3, column=0,sticky="w")

book_entry = tkinter.Entry(draw_info_frame)
book_entry.grid(row=0, column=1)

add_entry = tkinter.Entry(draw_info_frame)
add_entry.grid(row=1, column=1)

true_entry = tkinter.Entry(draw_info_frame)
true_entry.grid(row=2, column=1)

mpb_entry = tkinter.Entry(draw_info_frame)
mpb_entry.grid(row=3, column=1)

spell_label = tkinter.Label(draw_info_frame, text="Spell")
spell_combobox = ttk.Combobox(draw_info_frame, values=["Ignite", "Zap", "Magic Missile", "Ice Bolt", "Explosion", "Fireball (Splash)", "Fireball (Direct)", "Lightning Strike", "Chain Lightning"])
spell_label.grid(row=4, column=0)
spell_combobox.grid(row=4, column=1)

#inserting defaults 
book_entry.insert(0, 5)
add_entry.insert(0, 0)
true_entry.insert(0, 4)
mpb_entry.insert(0, 50)
spell_combobox.insert(0, "Zap")

for widget in draw_info_frame.winfo_children():
    widget.grid_configure(padx=10, pady=5) 

for widget in draw_opp_frame.winfo_children():
    widget.grid_configure(padx=10, pady=5) 

#button
button = tkinter.Button(frame, text="Calculate", command= generate_graph)
button.grid(row=4, column= 0, sticky="news", padx=20, pady=20)

#display 
disp = tkinter.Message(frame)
disp.grid(row=4, column= 1, sticky="news", padx=20, pady=20)

window.mainloop()