SpellDamageCalc will eventually have a GUI interface for generating spells / gear sets to compare the damage/cast and DPS for different spells and classes. 

Tester is currently all of the functioning Damage Calc code in text output. 
Edit the JSONs to get the gearsets you want/end up running most frequently to get the damage calcs to line up with what you want. 

tester.exe instructions:
Disclaimer - This is dogshit code, and a dogshit exe. This is unlikely to be updated, but any updates to spell damage numbers can be done through the JSON. 
If IM updates their damage calc in any substantial way, there might be an update, but there's a good chance this won't be updated for damage number changes. The main JSONs might, so check those.

Downloaded the repo
Make sure tester.exe and the two folders in the same folder (they should be by default)
Run tester.exe and follow the instructions. It is case sensitive, and it will crash if you're bad at following instructions. 


TODO: 
    Limb Calculations (in extended damage detail sections)
    The GUI (gross)
    It will probably just being another TKinter shit box like the previous to get it working
    Add Spell Generator to create new spells and damage profiles 
    Add Gear Profile Generator to create new gearsets for comparisons 
    Add Data visualization portions for spells + additional damage breakdowns
