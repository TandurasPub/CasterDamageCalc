from caster_class import Caster_Class


#TODO
# Limb Calculations 
# UI Portion (tkinter shitbox)
# Gearset Generation 
# Opponent Gearset JSONs/Generation (Need data)
# Spell Generation (for damage profiles) (not super needed)

 
# Test code output 
wizard = Caster_Class(name="Wizard")

warlock = Caster_Class(name="Warlock")

sorcerer = Caster_Class(name="Sorcerer")

cleric = Caster_Class(name="Cleric")

druid = Caster_Class(name="Druid")

full_class_list = [wizard, warlock, sorcerer, cleric, druid]

for caster in full_class_list: 
    caster.populate_gearset_list()

wizard.populate_spell_list() 
cleric.populate_spell_list()
warlock.populate_spell_list()
druid.populate_spell_list()
sorcerer.populate_spell_list()

class_dict = {}
class_dict['Wizard'] = wizard
class_dict['Cleric'] = cleric
class_dict['Warlock'] = warlock
class_dict['Druid'] = druid
class_dict['Sorcerer'] = sorcerer

opp_mdr = 0.0
opp_proj_resist = 0.0

class_to_display = class_dict['Sorcerer']

display_all = False
# calc_cast_time(self, spell:Spell): 

def display_all(): 
    for k in class_dict: 
        print(f'=================== {k} =========================')
        print(f'{k} stats | mpb: {(class_dict[k].mpb * 100):.2f}% | sps: {class_dict[k].sps * 100}% | catalyst_damage: {class_dict[k].cata} | add_mag: {class_dict[k].addM} | add_true: {class_dict[k].addT} |')
        print(f'Target stats | mdr: {opp_mdr*100}% | proj_resist: {opp_proj_resist*100}% |')
        for spell in class_dict[k].spell_list: 

            total_channel_time = 0
            damage_dict = class_dict[k].calc_damage(class_dict[k].spell_list[spell])
            if 'total channel' in damage_dict: 
                total_channel_time += damage_dict['total channel']['final_duration']


            post_calc_damage_dict = class_dict[k].calc_post_defensives(
                    class_dict[k].sum_damage_dict(
                        damage_dict,
                        class_dict[k].spell_list[spell]
                    ), mdr=opp_mdr, proj_resist=opp_proj_resist, spell_name=spell
                )
            total_damage = post_calc_damage_dict['total_damage']

            text_total_damage = f'total damage: {total_damage:.2f}'
            spell_text = f'{spell}:'
            display_text = f'{spell_text:70} {text_total_damage:20}'

            if total_channel_time: 
                display_text +=  f' | channel dps: {(total_damage/total_channel_time):.2f}'

            print(f'{display_text}') #### This is the actual spell info

def display_single_class(class_selection): 

    class_to_display = Caster_Class(name=class_selection)
    class_to_display.populate_spell_list() 
    class_to_display.populate_gearset_list()
    class_to_display.set_gearset(gearset_selection)

    print(f'=================== {class_to_display.name} =========================')
    print(f'{class_to_display.name} stats | mpb: {(class_to_display.mpb * 100):.2f}% | sps: {class_to_display.sps * 100}% | book_dam: {class_to_display.cata} | add_mag: {class_to_display.addM} | add_true: {class_to_display.addT} |')
    print(f'Target stats | mdr: {opp_mdr*100}% | proj_resist: {opp_proj_resist*100}% |')
       
    for spell in class_to_display.spell_list: 
        total_channel_time = 0

        damage_dict = class_to_display.calc_damage(class_to_display.spell_list[spell])
        if 'total channel' in damage_dict: 
            total_channel_time += damage_dict['total channel']['final_duration']

        post_calc_damage_dict = class_to_display.calc_post_defensives(
                class_to_display.sum_damage_dict(
                    damage_dict,
                    class_to_display.spell_list[spell]
                ), mdr=opp_mdr, proj_resist=opp_proj_resist, spell_name=spell
            )
        total_damage = post_calc_damage_dict['total_damage']

        text_total_damage = f'total damage: {total_damage:.2f}'
        spell_text = f'{spell}:'
        display_text = f'{spell_text:100} {text_total_damage:20}'

        if total_channel_time: 
            display_text +=  f' | channel dps: {(total_damage/total_channel_time):.2f}'

        print(f'{display_text}') #### This is the actual spell info


class_list = ["all", "wizard", "warlock", "sorcerer", "cleric", "druid"]
gearset_list = ["squire", "shit_kit", "mid_kit", "good_kit", "bis_kit"]

class_selection = '' 
while class_selection != 'exit': 
    print("input 'exit' as an input to end the program.")
    class_selection = input(f'Enter Class {class_list}:')

    if class_selection == 'exit': 
        break
    
    gearset_selection = input(f'Enter Gearset {gearset_list}:')
    if gearset_selection == 'exit': 
        break

    if class_selection == 'all': 
        for k in class_dict: 
            class_dict[k].set_gearset(gearset_selection)
        display_all()
    else: 
        display_single_class(class_selection)

    print('======================================================')