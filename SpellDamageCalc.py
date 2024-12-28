#Sorcerer Damage calc for Hotfix 36 of Dark and Darker
import numpy as np
import matplotlib.pyplot as  plt
from enum import Enum
from caster_class import Caster_Class

import tkinter
from tkinter import *
from tkinter import ttk

def tester(): 
    for spell in selected_class.spell_list: 
        total_channel_time = 0

        damage_dict = selected_class.calc_damage(selected_class.spell_list[spell])
        if 'total channel' in damage_dict: 
            total_channel_time += damage_dict['total channel']['final_duration']

        post_calc_damage_dict = selected_class.calc_post_defensives(
                selected_class.sum_damage_dict(
                    damage_dict,
                    selected_class.spell_list[spell]
                ), mdr=0, proj_resist=0, spell_name=spell
            )
        total_damage = post_calc_damage_dict['total_damage']

        text_total_damage = f'total damage: {total_damage:.2f}'
        spell_text = f'{spell}:'
        display_text = f'{spell_text:100} {text_total_damage:20}'

        if total_channel_time: 
            display_text +=  f' | channel dps: {(total_damage/total_channel_time):.2f}'

        print(f'{display_text}') #### This is the actual spell info


def generate_graph(): 
    #String Building
    roundedDam = np.round(10,decimals=2)
    retStr = "Total Damage: " + str(roundedDam)
    disp = tkinter.Message(frame, text=retStr)

    print(f'burn: {is_burn.get()}')
    disp.grid(row=4, column= 1, sticky="news", padx=15, pady=15)

    print(selected_class.spell_list)
    tester()

def import_caster(): 
    print("")
    
window = tkinter.Tk()
window.title("Caster Damage Calc")

frame = tkinter.Frame(window)
frame.pack()

# Creating Grids 
draw_import_frame = tkinter.LabelFrame(frame, text = "Import Information")
draw_import_frame.grid(row=0, column=0)

draw_info_frame = tkinter.LabelFrame(frame, text ="Character Stats (Use % values)")
draw_info_frame.grid(row= 1, column=0)

draw_opp_frame = tkinter.LabelFrame(frame, text="Opponent Stats (Use % values)")
draw_opp_frame.grid(row=1, column=1)

draw_spell_frame = tkinter.LabelFrame(frame, text="Spell Information (Use % values)")
draw_spell_frame.grid(row=1, column=2)

# I don't think we need this, but might as well create them for easier modification
wizard = Caster_Class(name="Wizard")
warlock = Caster_Class(name="Warlock")
sorcerer = Caster_Class(name="Sorcerer")
cleric = Caster_Class(name="Cleric")
druid = Caster_Class(name="Druid")

# This will need to be manually updated because the import setup I have doesn't include a way to generate classes. Whoops. 
full_class_list = {"Wizard" : wizard, "Warlock" : warlock, "Sorcerer" : sorcerer, "Cleric" : cleric, "Druid": druid}


class_names_list = []
gearset_list = []

# Go ahead and populate all the loadouts so we're ready to go for calculations later and don't need to worry about this
for caster in full_class_list:
    class_names_list.append(caster) 
    full_class_list[caster].populate_gearset_list()
    full_class_list[caster].populate_spell_list()

for gearset_name in wizard.gearsets: 
    gearset_list.append(gearset_name)

#Setting default selected class for reasons
selected_class = full_class_list['Wizard']
selected_gearset = gearset_list[0]
selected_opponent_gearset =''

# This is some super hacky code
def set_class_values(self, *args): 
    # Update the spell list to display here
    selected_class = class_combobox.get()
    print(f'class selected: {selected_class}')

def set_gearset_values(self, *args):
    set_caster_from_gearset()

def set_opponent_gearset_values(self, *args): 
    print('opponent gearset selected')


# Class Dropdown
class_label = tkinter.Label(draw_import_frame, text="Class")
class_value = StringVar()
class_combobox = ttk.Combobox(draw_import_frame, textvariable = class_value, values=class_names_list)

class_label.grid(row=0, column=0)
class_combobox.grid(row=0, column=1)

# Gearset Dropdown 
gearset_label = tkinter.Label(draw_import_frame, text="Gearset")
gearset_value = StringVar()
gearset_combobox = ttk.Combobox(draw_import_frame, textvariable=gearset_value, values=gearset_list)

gearset_label.grid(row=0, column=2)
gearset_combobox.grid(row=0, column=3)

# Opponent Gearset Dropdown 
opponent_gearset_label = tkinter.Label(draw_import_frame, text="Opponent Gearset")
opponent_gearset_value = StringVar()
opponent_gearset_combobox = ttk.Combobox(draw_import_frame, textvariable=opponent_gearset_value, values=['placeholder1', 'placeholder2', 'placeholder3'])

opponent_gearset_label.grid(row=1, column=0)
opponent_gearset_combobox.grid(row=1, column=1)

# combobox traces - This is the reason for the super hacky code above
class_value.trace_add('write', set_class_values)
gearset_value.trace_add('write', set_gearset_values)
opponent_gearset_value.trace_add('write', set_opponent_gearset_values)

def set_import_defaults():
    first_class = next(iter(full_class_list))

    class_combobox.insert(0, first_class)

    selected_class = full_class_list[class_combobox.get()]

    first_gearset = next(iter(full_class_list[selected_class.name].gearsets))
    gearset_combobox.insert(0, first_gearset)

    opponent_gearset_combobox.insert(0, "placeholder1")


set_import_defaults()



# Modify Gearset Checkbox
def toggle_modify_gearset(): 
    for widget in caster_entries: 
        if modify_gearset.get(): 
            widget.config(state='normal')
        else: 
            widget.config(state='disabled')

modify_gearset = BooleanVar()
modify_gearset_check = ttk.Checkbutton(draw_import_frame, text='Modify Gearset?', variable=modify_gearset,
                                  onvalue=1, offvalue=0, command=toggle_modify_gearset)
modify_gearset_check.grid(row=1, column=3)


# Caster Stat Labels

book_value = StringVar()
add_value = StringVar() 
true_value = StringVar() 
mpb_value = StringVar()
sps_value = StringVar()

book_label = tkinter.Label(draw_info_frame,  text="Casting Implement Damage:")
book_label.grid(row=0, column=0,sticky="w")
add_label = tkinter.Label(draw_info_frame, text="Additional Magic Damage:")
add_label.grid(row=1, column=0,sticky="w")
true_label = tkinter.Label(draw_info_frame, text="Additional True Magic Damage:")
true_label.grid(row=2, column=0,sticky="w")
mpb_label = tkinter.Label(draw_info_frame, text="Magic Power Bonus %:")
mpb_label.grid(row=3, column=0,sticky="w")
sps_label = tkinter.Label(draw_info_frame, text="Spell Cast Speed %:")
sps_label.grid(row=4, column=0,sticky="w")


# Caster Stat Inputs
book_entry = tkinter.Entry(draw_info_frame, textvariable=book_value)
book_entry.grid(row=0, column=1)
add_entry = tkinter.Entry(draw_info_frame, textvariable=add_value)
add_entry.grid(row=1, column=1)
true_entry = tkinter.Entry(draw_info_frame, textvariable=true_value)
true_entry.grid(row=2, column=1)
mpb_entry = tkinter.Entry(draw_info_frame, textvariable=mpb_value)
mpb_entry.grid(row=3, column=1)
sps_entry = tkinter.Entry(draw_info_frame, textvariable=sps_value)
sps_entry.grid(row=4, column=1)

caster_entries = [book_entry, add_entry, true_entry, mpb_entry, sps_entry]


def set_caster_from_gearset(): 
    gearset = selected_class.gearsets[gearset_combobox.get()]

    book_value.set(gearset['stats']['cata'])
    add_value.set(gearset['stats']['addM']) 
    true_value.set(gearset['stats']['addT']) 
    mpb_value.set(gearset['stats']['mpb']) 
    sps_value.set(gearset['stats']['sps']) 


set_caster_from_gearset()

# Caster Stat Defaults 
#book_entry.insert(0, 5)
#add_entry.insert(0, 0)
#true_entry.insert(0, 4)
#mpb_entry.insert(0, 50)
#sps_entry.insert(0, 25)


for entry in caster_entries: 
    entry.config(state='disabled')

# Opponent Stat Labels
MDR_label = tkinter.Label(draw_opp_frame, text="Opponent % MDR:")
MDR_label.grid(row=0, column=0,sticky="w")
projRes_label = tkinter.Label(draw_opp_frame, text="Opponent % Proj Resist:")
projRes_label.grid(row=1, column=0,sticky="w")
hsRes_label = tkinter.Label(draw_opp_frame, text="Opponent % Headshot Resist:")
hsRes_label.grid(row=2, column=0,sticky="w")
debuffDur_label = tkinter.Label(draw_opp_frame, text="Opponent % Debuff Duration:")
debuffDur_label.grid(row=3, column=0,sticky="w")

# Opponent Stat Inputs
MDR_entry = tkinter.Entry(draw_opp_frame)
MDR_entry.grid(row=0, column=1)
projRes_entry = tkinter.Entry(draw_opp_frame)
projRes_entry.grid(row=1, column=1)
hsRes_entry = tkinter.Entry(draw_opp_frame)
hsRes_entry.grid(row=2, column=1)
debuffDurr_entry = tkinter.Entry(draw_opp_frame)
debuffDurr_entry.grid(row=3, column=1)

opponent_entries = [MDR_entry, projRes_entry, hsRes_entry, debuffDurr_entry]


# Limb Position
headshot_label = tkinter.Label(draw_opp_frame, text="Headshot")
headshot_combobox = ttk.Combobox(draw_opp_frame, values=["Yes", "No"])
headshot_label.grid(row=4, column=0,sticky="w")
headshot_combobox.grid(row=4, column=1)


# Opponent Stat Defaults
MDR_entry.insert(0, 20)
projRes_entry.insert(0, 0)
hsRes_entry.insert(0, 0)
debuffDurr_entry.insert(0, 0)
headshot_combobox.insert(0, "No")

# Caster Stat Defaults 
#book_entry.insert(0, 5)
#add_entry.insert(0, 0)
#true_entry.insert(0, 4)
#mpb_entry.insert(0, 50)


#Spell Generic Inputs/Labels
spell_entries = [] 
spell_labels = [] 
spell_checks = []

book_label = tkinter.Label(draw_spell_frame, text="Spell Name:")
book_label.grid(row=1, column=0,sticky="w")

damage_label = tkinter.Label(draw_spell_frame, text="Spell Damage:")
damage_label.grid(row=2, column=0,sticky="w")

abr_label = tkinter.Label(draw_spell_frame, text="Spell ABR:")
abr_label.grid(row=3, column=0,sticky="w")

true_label = tkinter.Label(draw_spell_frame, text="Spell Cast Time:")
true_label.grid(row=4, column=0,sticky="w")

name_entry = tkinter.Entry(draw_spell_frame)
name_entry.grid(row=1, column=1)

damage_entry = tkinter.Entry(draw_spell_frame)
damage_entry.grid(row=2, column=1)

abr_entry = tkinter.Entry(draw_spell_frame)
abr_entry.grid(row=3, column=1)

cast_time_entry = tkinter.Entry(draw_spell_frame)
cast_time_entry.grid(row=4, column=1)

generic_entries = [name_entry, damage_entry, abr_entry, cast_time_entry]

for entry in generic_entries: 
    spell_entries.append(entry)

generic_labels = [book_label, damage_label, abr_label, true_label]

for label in generic_labels: 
    spell_labels.append(label)

# Spell Burn Labels/Inputs
burn_base_label = tkinter.Label(draw_spell_frame, text="Spell Burn Base:")
burn_base_label.grid(row=1, column=2,sticky="w")

burn_duration_label = tkinter.Label(draw_spell_frame, text="Spell Burn Duration:")
burn_duration_label.grid(row=2, column=2,sticky="w")

burn_abr_label = tkinter.Label(draw_spell_frame, text="Spell Burn ABR:")
burn_abr_label.grid(row=3, column=2,sticky="w")

def toggle_burn_entries(): 
    for widget in burn_entries: 
        if is_burn.get(): 
            widget.config(state='normal')
        else: 
            widget.config(state='disabled')

is_burn = BooleanVar()
burn_check = ttk.Checkbutton(draw_spell_frame, text='Burn?', variable=is_burn,
                                  onvalue=1, offvalue=0, command=toggle_burn_entries)
burn_check.grid(row=0, column=2)


burn_base_entry = tkinter.Entry(draw_spell_frame)
burn_base_entry.grid(row=1, column=3)
burn_base_entry.config(state="disabled")

burn_duration_entry = tkinter.Entry(draw_spell_frame)
burn_duration_entry.grid(row=2, column=3)
burn_duration_entry.config(state="disabled")

burn_abr_entry = tkinter.Entry(draw_spell_frame)
burn_abr_entry.grid(row=3, column=3)
burn_abr_entry.config(state="disabled")

burn_entries = [burn_base_entry, burn_duration_entry, burn_abr_entry]

for widget in burn_entries: 
    spell_entries.append(widget)

burn_labels = [burn_base_label, burn_duration_label, burn_abr_label]

for label in burn_labels: 
    spell_labels.append(label)

burn_checks = [burn_check]

for check in burn_checks: 
    spell_checks.append(check)


# Spell Splash Labels/Inputs
splash_base_label = tkinter.Label(draw_spell_frame, text="Spell Splash Base:")
splash_base_label.grid(row=1, column=4,sticky="w")

splash_abr_label = tkinter.Label(draw_spell_frame, text="Spell Splash ABR:")
splash_abr_label.grid(row=2, column=4,sticky="w")

def toggle_splash_entries(): 
    for widget in splash_entries: 
        if is_splash.get(): 
            widget.config(state='normal')
        else: 
            widget.config(state='disabled')

is_splash = BooleanVar()
splash_check = ttk.Checkbutton(draw_spell_frame, text='Splash?', variable=is_splash,
                                  onvalue=1, offvalue=0, command=toggle_splash_entries)
splash_check.grid(row=0, column=4)


splash_base_entry = tkinter.Entry(draw_spell_frame)
splash_base_entry.grid(row=1, column=5)
splash_base_entry.config(state="disabled")

splash_abr_entry = tkinter.Entry(draw_spell_frame)
splash_abr_entry.grid(row=2, column=5)
splash_abr_entry.config(state="disabled")

splash_entries = [splash_base_entry, splash_abr_entry]
for entry in splash_entries: 
    spell_entries.append(entry)

splash_labels = [splash_base_label, splash_abr_label]
for label in splash_labels: 
    spell_labels.append(label)

splash_checks = [splash_check]
for check in splash_checks: 
    spell_checks.append(check)

# Spell Channel Labels/Inputs
channel_dura_label = tkinter.Label(draw_spell_frame, text="Spell Channel Duration:")
channel_dura_label.grid(row=1, column=6,sticky="w")

# this should be equal to the duration for spells that do damage/s
channel_ticks_label = tkinter.Label(draw_spell_frame, text="Channel Ticks:")
channel_ticks_label.grid(row=2, column=6,sticky="w")

def toggle_channel_entries(): 
    for entry in channel_entries: 
        if is_channel.get(): 
            entry.config(state='normal')
        else: 
            entry.config(state='disabled')

# This is used for multi hit spells (incorrectly)
is_channel = BooleanVar()
channel_check = ttk.Checkbutton(draw_spell_frame, text='Channeled?', variable=is_channel,
                                  onvalue=1, offvalue=0, command=toggle_channel_entries)
channel_check.grid(row=0, column=6)

channel_dura_entry = tkinter.Entry(draw_spell_frame)
channel_dura_entry.grid(row=1, column=7)
channel_dura_entry.config(state="disabled")

channel_ticks_entry = tkinter.Entry(draw_spell_frame)
channel_ticks_entry.grid(row=2, column=7)
channel_ticks_entry.config(state="disabled")

is_channel_intervals = BooleanVar()
channel_intervals_check = ttk.Checkbutton(draw_spell_frame, text='Channel Intervals?', variable=is_channel_intervals,
                                  onvalue=1, offvalue=0, state='disabled')
channel_intervals_check.grid(row=3, column=7)

channel_entries = [channel_dura_entry, channel_ticks_entry, channel_intervals_check]
for widget in channel_entries: 
    spell_entries.append(widget)

channel_labels = [channel_dura_label, channel_ticks_label]
for label in channel_labels: 
    spell_labels.append(label)

channel_checks = [channel_check, channel_intervals_check]
for check in channel_checks: 
    spell_checks.append(check)

all_spell_widgets = [] 

for label in spell_labels: 
    all_spell_widgets.append(label)
for entry in spell_entries: 
    all_spell_widgets.append(entry)
for check in spell_checks: 
    all_spell_widgets.append(check)
 
def toggle_spell_widgets(): 
    if spell_info.get():
        for widget in all_spell_widgets:
            widget.grid()
    else:
        for widget in all_spell_widgets: 
            widget.grid_remove()
     

spell_info = BooleanVar()
spell_info_check = ttk.Checkbutton(draw_spell_frame, text='Show Spell Info?', variable=spell_info,
                                  onvalue=1, offvalue=0, command=toggle_spell_widgets)
spell_info_check.grid(row=0, column=0)


for wirget in draw_import_frame.winfo_children(): 
    widget.grid_configure(padx=5, pady=3)

for widget in draw_info_frame.winfo_children():
    widget.grid_configure(padx=5, pady=3) 

for widget in draw_opp_frame.winfo_children():
    widget.grid_configure(padx=5, pady=3) 

for widget in draw_spell_frame.winfo_children():
    widget.grid_configure(padx=5, pady=3) 
    # don't show spell widgets by default (it's even more clunky than normal tkinter stuff)
    if widget in all_spell_widgets: 
            widget.grid_remove()

# button
button = tkinter.Button(frame, text="Calculate", command= generate_graph)
button.grid(row=4, column= 0, sticky="news", padx=20, pady=20)

# display 
disp = tkinter.Message(frame)
disp.grid(row=4, column= 1, sticky="news", padx=20, pady=20)

window.mainloop()