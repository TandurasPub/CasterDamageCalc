import json
from enum import Enum


class Limbs(Enum): 
    HEAD = 1.5
    BODY = 1.0
    ARM = 0.8
    LEG = 0.6
    HAND = 0.5


class Spell: 
    def __init__(self, name:str, damage=0, cast_time=0, abr=1.0, is_projectile=True, can_headshot=True, burn=False,
                  burn_base=0, burn_duration=0, burn_abr=0.5, splash_base=0, splash_abr=1.0, 
                  is_channel=False, channel_intervals=False, channel_ticks=0, channel_duration=0): 
        self.name = name
        self.damage = damage
        self.cast_time = cast_time
        self.abr = abr
        self.is_proj = is_projectile
        self.can_headshot = can_headshot
        self.burn = burn 
        self.burn_base = burn_base
        self.burn_dura = burn_duration
        self.burn_abr = burn_abr
        self.splash_base = splash_base
        self.splash_abr = splash_abr
        self.is_channel = is_channel
        self.chan_ints = channel_intervals
        self.chan_ticks = channel_ticks
        self.chan_dura = channel_duration

class Caster_Class: 
    def __init__(self, name: str, spell_list = {}, sps=0.0, mpb=0.0, cata=0.0, addM=0, addT=0): 
        self.name = name
        self.spell_list = spell_list
        self.sps = sps
        self.mpb = mpb
        self.cata = cata
        self.addM = addM
        self.addT = addT
        
    def set_player_stats(self, sps=0, mpb=0, cata=0, addM=0, addT=0): 
        self.sps = sps
        self.mpb = mpb
        self.cata = cata
        self.addM = addM
        self.addT = addT

    def calc_splash(self, spell: Spell): 
        mag_damage = ((spell.splash_base + (self.cata * (spell.splash_abr))) * (1 + (self.mpb * spell.splash_abr))) + (self.addM * spell.splash_abr)
        true_damage = (self.addT * spell.splash_abr)
        return mag_damage, true_damage
    
    def calc_impact(self, spell: Spell): 
        mag_damage = ((spell.damage + (self.cata * (spell.abr))) * (1 + (self.mpb * spell.abr))) + (self.addM * spell.abr)
        true_damage = (self.addT * spell.abr)
        return {'mag_damage': mag_damage, 'true_damage' : true_damage } 
    
    def calc_burn(self, spell: Spell):
        burn_ticks = spell.burn_dura

        total_burn_mag_damage = ((spell.burn_base + (self.cata * (spell.burn_abr))) * (1 + (self.mpb * spell.burn_abr))) + (self.addM * spell.burn_abr)
        total_burn_true_damage = (self.addT * spell.burn_abr)

        tick_burn_damage = (total_burn_mag_damage / burn_ticks) + (total_burn_true_damage / burn_ticks)
        return {'total_mag_burn': total_burn_mag_damage, 'total_true_burn' : total_burn_true_damage, 'burn_tick' : tick_burn_damage} 

    def calc_channel(self, spell: Spell): 

        final_dura = (spell.chan_dura / ( 1 + self.sps)) 
        tick_magic_damage = ((spell.damage + (self.cata * (spell.abr))) * (1 + (self.mpb * spell.abr))) + (self.addM * spell.abr) 
        tick_true_damage = (self.addT * spell.abr)

        if spell.chan_ints: 
            spell_ticks = spell.chan_ticks 
        else: 
            spell_ticks = final_dura

        mag_damage = spell_ticks * tick_magic_damage
        true_damage = spell_ticks * tick_true_damage

        return {'mag_damage': mag_damage, 'true_damage' : true_damage, 'final_duration' : final_dura } 
    
    def calc_damage(self, spell: Spell): 
        damage_dict = {}

        damage_dict['single impact'] = self.calc_impact(spell)

        if spell.splash_base > 0: 
            damage_dict['splash'] = self.calc_splash(spell)

        if spell.is_channel:
            damage_dict['total channel'] = self.calc_channel(spell) 

        if spell.burn: 
            damage_dict['burn'] = self.calc_burn(spell)

        return damage_dict
    
    def sum_damage_dict(self, damage_dict: dict, spell: Spell): 
        projectile_magic_damage = 0 
        magic_damage = 0
        true_damage = 0 

        print(damage_dict)
        if spell.is_proj: 
            if 'total channel' in damage_dict: 
                projectile_magic_damage += damage_dict['total channel']['mag_damage']
                true_damage += damage_dict['total channel']['true_damage']
            else: 
                projectile_magic_damage += damage_dict['single impact']['mag_damage']
                true_damage += damage_dict['single impact']['true_damage']

        else: 
            if 'total channel' in damage_dict: 
                magic_damage += damage_dict['total channel']['mag_damage']
                true_damage += damage_dict['total channel']['true_damage']
            else: 
                magic_damage += damage_dict['single impact']['mag_damage']
                true_damage += damage_dict['single impact']['true_damage']

        if 'burn' in damage_dict: 
            magic_damage += damage_dict['burn']['total_mag_burn']
            true_damage += damage_dict['burn']['total_true_burn']

        sum_damage_dict = {}
        if magic_damage: 
            sum_damage_dict['total_mag_damage'] = magic_damage
        if projectile_magic_damage: 
            sum_damage_dict['total_proj_mag_damage'] = projectile_magic_damage
        if true_damage: 
            sum_damage_dict['total_true_damage'] = true_damage

        return sum_damage_dict
    
    def calc_cast_time(self, spell:Spell): 
        modified_cast_time = (spell.cast_time / ( 1 + self.sps)) 

        return modified_cast_time
    

def load_spells(character_class: str): 
    with open(f'SpellJsons/{character_class}Spells.json', 'r') as file: 
        data = json.load(file)
        file.close()

    return data

# This is hacky - I don't know the 'correct' way to parse the JSON to get correct data types quickly and didn't want to spend time on this
# Presumably you can create a validation/constructor to use this and it'd be a little cleaner
# Somehow this list is being shared across caster_classes 
def populate_spell_list(caster: Caster_Class): 
    spell_list = load_spells(caster.name)['spell_list']
    ret_list = {}
    for spell in spell_list: 
        s = Spell(spell['name'])
        
        if 'damage' in spell: 
            s.damage = float(spell['damage'])
        if 'cast_time' in spell: 
            s.cast_time = float(spell['cast_time'])
        if 'abr' in spell: 
            s.abr = float(spell['abr'])
        if 'is_projectile' in spell: 
            s.is_proj = (spell['is_projectile'] == 'True')
        if 'can_headshot' in spell: 
            s.can_headshot = (spell['can_headshot'] == 'True')
        if 'burn' in spell: 
            s.burn = (spell['burn'] == 'True')
        if 'burn_base' in spell: 
            s.burn_base = float(spell['burn_base'])
        if 'burn_duration' in spell: 
            s.burn_dura = float(spell['burn_duration'])
        if 'burn_abr' in spell: 
            s.burn_abr = float(spell['burn_abr'])
        if 'splash_base' in spell: 
            s.splash_base = float(spell['splash_base'])
        if 'splash_abr' in spell: 
            s.splash_abr = float(spell['splash_abr'])
        if 'is_channel' in spell: 
            s.is_channel = (spell['is_channel'] == 'True')
        if 'channel_intervals' in spell: 
            s.chan_ints = (spell['channel_intervals'] == 'True')
        if 'channel_ticks' in spell: 
            s.chan_ticks = float(spell['channel_ticks'])
        if 'channel_duration' in spell: 
            s.chan_dura = float(spell['channel_duration'])

        ret_list[s.name] = s

    caster.spell_list = ret_list
 

    



#fireball = Spell('fireball', cast_time=2.5, damage=25, abr=1.0, is_projectile=True,
                 #splash_base=10, splash_abr=1.0,
                 #burn=True, burn_duration=3, burn_base=3, burn_abr=0.5)

#mm = Spell('magic missile', cast_time=1.25, damage=10, abr = 0.75, is_projectile=True, 
           #is_channel=True, channel_duration=3, channel_intervals=True, channel_ticks=10)

#wizard_spells = {'fireball' : fireball, 'magic missile': mm}

wizard = Caster_Class(name="Wizard")
wizard.set_player_stats(sps=0.5, mpb=0.25, cata=2, addM=1, addT=1)

warlock = Caster_Class(name="Warlock")
warlock.set_player_stats(sps=.5, mpb=.3, cata=2, addM=0, addT=2)

sorcerer = Caster_Class(name="Sorcerer")
sorcerer.set_player_stats(sps=0.5, mpb=.0, cata=0, addM=0, addT=0)

cleric = Caster_Class(name="Cleric")
cleric.set_player_stats(sps=0.25, mpb=.21, cata=2, addM=0, addT=0)

druid = Caster_Class(name="Druid")
druid.set_player_stats(sps=0.25, mpb=.21, cata=2, addM=0, addT=0)




populate_spell_list(wizard) 
populate_spell_list(cleric)
populate_spell_list(warlock)
populate_spell_list(druid)
populate_spell_list(sorcerer)

print(f'========== Wizard ==========')
for spell in wizard.spell_list: 
    print(f'{spell}: {wizard.calc_damage(wizard.spell_list[spell])}')
    print(f'{spell} total damage: {
        wizard.sum_damage_dict(
            wizard.calc_damage(wizard.spell_list[spell]),
            wizard.spell_list[spell]
        )
        }')
    print(f'{spell} cast time with {wizard.sps*100}% spell cast speed: {wizard.calc_cast_time(wizard.spell_list[spell])}')

print(f'========== Warlock ==========')
print(warlock.spell_list)
for spell in warlock.spell_list: 
    print(f'{spell}: {warlock.calc_damage(warlock.spell_list[spell])}')
    print(f'{spell} cast time with {warlock.sps*100}% spell cast speed: {warlock.calc_cast_time(warlock.spell_list[spell])}')

print(f'========== Cleric ==========')
print(cleric.spell_list)
for spell in cleric.spell_list: 
    print(f'{spell}: {cleric.calc_damage(cleric.spell_list[spell])}')
    print(f'{spell} cast time with {cleric.sps*100}% spell cast speed: {cleric.calc_cast_time(cleric.spell_list[spell])}')

print(f'========== Druid ==========')
print(druid.spell_list)
for spell in druid.spell_list: 
    print(f'{spell}: {druid.calc_damage(druid.spell_list[spell])}')
    print(f'{spell} cast time with {druid.sps*100}% spell cast speed: {druid.calc_cast_time(druid.spell_list[spell])}')

    
print(f'========== Sorcerer ==========')
print(sorcerer.spell_list)
for spell in sorcerer.spell_list: 
    print(f'{spell}: {sorcerer.calc_damage(sorcerer.spell_list[spell])}')
    print(f'{spell} cast time with {sorcerer.sps*100}% spell cast speed: {sorcerer.calc_cast_time(sorcerer.spell_list[spell])}')
