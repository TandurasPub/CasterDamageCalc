SpellDamageCalc will (probably) have a GUI interface for generating spells / gear sets to compare the damage/cast and DPS for different spells and classes. 

Tester is currently all of the functioning Damage Calc code in text output. 
Edit the JSONs to get the gearsets you want/end up running most frequently to get the damage calcs to line up with what you want. 

tester.exe instructions:
Disclaimer - This is dogshit code, and a dogshit exe. You shouldn't be running this as a random exe unless you know how to protect yourself from sketchy exe downloads, or you really trust me (as a random on the internet). This is currently being kept updated, but if it falls behind any updates to spell damage numbers can be done through the JSON. 
Double check the JSONs after any patches if you don't see an update, and feel free to ping me/msg me on Discord and I can push updates if people are actually using this.


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

Bugs: 
    Channel Calcs are wrong, and I'm not sure what's the cause. It looks like channeled spells have 2 extra ticks (with .1s ticks). The math lines up, but the calc doesn't have these factored in. 
    Generically, damage over time / channeled spells are off (by roughly 5-10% depending on spell cast speed and flat damage)
