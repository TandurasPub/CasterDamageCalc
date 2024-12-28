import json
from spell import Spell
from enum import Enum

class Limbs(Enum): 
    HEAD = 1.5
    BODY = 1.0
    ARM = 0.8
    LEG = 0.6
    HAND = 0.5

class Caster_Class: 
    def __init__(self, name: str, spell_list = {}, gearsets = {}, sps=0.0, mpb=0.0, mpen=0.0, cata=0.0, addM=0, addT=0): 
        self.name = name
        self.spell_list = spell_list
        self.gearsets = gearsets
        self.sps = sps
        self.mpb = mpb
        self.mpen=mpen
        self.cata = cata
        self.addM = addM
        self.addT = addT
        
    def set_player_stats(self, sps=0, mpb=0, cata=0, addM=0, addT=0): 
        self.sps = sps
        self.mpb = mpb
        self.cata = cata
        self.addM = addM
        self.addT = addT

    def set_player_stats_from_dict(self, gearset: dict): 
        self.mpb = gearset['mpb']
        self.sps = gearset['sps']
        self.cata = gearset['cata']
        self.addM = gearset['addM']
        self.addT = gearset['addT']

    # time to do some fuckery. Load the gearsets into the class's gearset dict, and then swap active gearsets out from this dict for easier access
    def populate_gearset_list(self): 

        gearsets = self.load_gear_sets(f'GearsetJsons/CasterGearSets.json')
        self.gearsets = gearsets['gear_sets']

    
    def set_gearset(self, gearset='shit_kit'): 
        self.set_player_stats_from_dict(self.gearsets[gearset]['stats'])

    def calc_splash(self, spell: Spell): 
        if spell.is_merge: 
            cata = 0
        else: 
            cata = self.cata


        mag_damage = ((spell.splash_base + (cata * (spell.splash_abr))) * (1 + (self.mpb * spell.splash_abr))) + (self.addM * spell.splash_abr)
        true_damage = (self.addT * spell.splash_abr)
        return {'mag_splash': mag_damage, 'true_splash': true_damage}
    
    def calc_impact(self, spell: Spell): 
        if spell.is_merge: 
            cata = 0
        else: 
            cata = self.cata

        mag_damage = ((spell.damage + (cata * (spell.abr))) * (1 + (self.mpb * spell.abr))) + (self.addM * spell.abr)
        true_damage = (self.addT * spell.abr)
        return {'mag_damage': mag_damage, 'true_damage' : true_damage } 
    
    def calc_burn(self, spell: Spell):
        if spell.is_merge: 
            cata = 0
        else: 
            cata = self.cata

        burn_ticks = spell.burn_dura

        total_burn_mag_damage = ((spell.burn_base + (cata* (spell.burn_abr))) * (1 + (self.mpb * spell.burn_abr))) + (self.addM * spell.burn_abr)
        total_burn_true_damage = (self.addT * spell.burn_abr)

        tick_burn_damage = (total_burn_mag_damage / burn_ticks) + (total_burn_true_damage / burn_ticks)
        return {'total_mag_burn': total_burn_mag_damage, 'total_true_burn' : total_burn_true_damage, 'burn_tick' : tick_burn_damage} 

    def calc_channel(self, spell: Spell): 

        if spell.is_merge: 
            cata = 0
        else: 
            cata = self.cata

        final_dura = (spell.chan_dura / ( 1 + self.sps)) 
        tick_magic_damage = ((spell.damage + (cata * (spell.abr))) * (1 + (self.mpb * spell.abr))) + (self.addM * spell.abr) 
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

        if 'splash' in damage_dict: 
            magic_damage += damage_dict['splash']['mag_splash']
            true_damage += damage_dict['splash']['true_splash']

        sum_damage_dict = {}
        if magic_damage: 
            sum_damage_dict['total_mag_damage'] = magic_damage
        if projectile_magic_damage: 
            sum_damage_dict['total_proj_mag_damage'] = projectile_magic_damage
        if true_damage: 
            sum_damage_dict['total_true_damage'] = true_damage
   
        return sum_damage_dict
    
    def calc_post_defensives(self, sum_damage_dict: dict, mdr=0.0, proj_resist=0.0, headshot_reduction=0.0, spell_name=''): 

        proj_dam = 0 
        magic_dam = 0 
        true_dam = 0

        # this is gross and can be avoided by populating the numbers with 0
        # but I don't want to do that because I'm too lazy to go back (and add checks where we need it)
        if 'total_proj_mag_damage' in sum_damage_dict: 
            proj_dam = sum_damage_dict['total_proj_mag_damage']

        if 'total_mag_damage' in sum_damage_dict:
            magic_dam = sum_damage_dict['total_mag_damage']

        if 'total_true_damage' in sum_damage_dict: 
            true_dam = sum_damage_dict['total_true_damage']


        post_proj_magic = proj_dam * ((1 - mdr) * (1 - self.mpen)) * (1 - proj_resist)
        post_mdr_magic = magic_dam * ((1 - mdr) * (1 - self.mpen))

        total_damage = post_proj_magic + post_mdr_magic + true_dam

        post_resist_dict = {}
        post_resist_dict['total_damage'] = total_damage
        post_resist_dict['post_proj_magic'] = post_proj_magic
        post_resist_dict['post_mdr_magic'] = post_mdr_magic
        post_resist_dict['true_damage'] = true_dam
        

        return post_resist_dict
    
    def calc_cast_time(self, spell:Spell): 
        modified_cast_time = (spell.cast_time / ( 1 + self.sps)) 

        return modified_cast_time
    

    def load_spells(self): 
        with open(f'SpellJsons/{self.name}Spells.json', 'r') as file: 
            data = json.load(file)
            file.close()

        return data


    def load_gear_sets(self, gear_set_filepath: str): 
        with open(f'{gear_set_filepath}', 'r') as file: 
            data = json.load(file)
        file.close() 

        return data
    

    
# This is hacky - I don't know the 'correct' way to parse the JSON to get correct data types quickly and didn't want to spend time on this
# Presumably you can create a validation/constructor to use this and it'd be a little cleaner
# Somehow this list is being shared across caster_classes 
    def populate_spell_list(self): 
        spell_list = self.load_spells()['spell_list']
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
            if 'is_merge' in spell: 
                s.is_merge = (spell['is_merge'] == 'True')

            ret_list[s.name] = s

        self.spell_list = ret_list