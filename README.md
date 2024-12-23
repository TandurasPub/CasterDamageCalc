SpellDamageCalc will eventually have a GUI interface for generating spells / gear sets to compare the damage/cast and DPS for different spells and classes. 

Tester is  testing code w/ text output for calculations while the GUI isn't created


TODO: 
    The GUI (gross)
      Probably in a Django web-app, but no idea yet. Might end up just being another TKinter shit box like the previous to get it working
    Finish Generating Class Spell List JSONs
    Add Spell Generator to create new spells and damage profiles 
    Generate Gear Loadout Profiles 
    Add Gear Profile Generator to create new gearsets for comparisons 
    Add Data visualization portions for spells + additional damage breakdowns
    
BUGS: 
    Spell imports are fucked and is creating a single spell list. I don't know what fuckery I did to make this happen but I'm dumb and can't find it atm.
