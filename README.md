# Caster Damage Calc

A sketchy damage calc for Dark and Darker, untested values and all. 
Tester.exe is the text output version and is likely to remain out of date.

SpellDamageCalc.exe is the current exe that's likely to be kept up to date. 

Resistances are currently not being calculated in the GUI version. The Text output has it, and I'm finishing adding this stuff in.

The goal was to seperate out all of the damage calc formulas from the gearsets/spell information so anyone could keep those updated and get accurate damage numbers and (I think) that's done. 

If you find any issues (specifically with the calculations / how some spells currently function), let me know. Feel free to DM me on Discord (Tanduras), or just @ me in the relevant chat. 

If anyone from IM ever ends up using this, I expect to get a funny role in the discord.

## Getting Started
Download the repo, run the code, see the numbers. 
If there are any issues/conflicts DM me and I can see about fixing it, but there shouldn't be any issues (on Windows) if you have a semi-recent version of Python or are just running the .exe. 
I have 0 idea how to actually support Mac, and if you're on Linux I'm gonna trust you know how to get it working for yourself. 

### Prerequisites
Random warning - don't trust random .exes from discord folk unless you really trust the dude, or know how to run them safely. 

If you do, you can run the .exe found in the dist folder and it should work without any finagling. 
The .json files in the dist folder can be edited to adjust the pre-sets, and spell balancing.

Otherwise, you can install python and run the code in tester.py / SpellDamageCalc.py yourself for the different calculators. 

The JSON the .exe uses is seperate from the one used by the python code because I'm dumb and lazy. Keep the one you're using updated if you're not grabbing updates from here. 


### TODO
* Limb Calculations - unlikely to be shown in the text display, but needed for GUI stuff
* Opponent Resistances for GUI Version
* Add Spell Generator to create new spells and damage profiles 
* Add Gear Profile Generator to more easily create gearsets for comparisons
* Add Data visualization portions for spells + additional damage breakdowns


### Bugs
* Channel Calcs are wrong, and I'm not sure what's the cause. It looks like channeled spells have 2 extra ticks (with .1s ticks). The math lines up, but the calc doesn't have these factored in, and I'm not certain this is correct. 
    * Generically, damage over time / channeled spells that do NOT have channel_interval scaling are off by roughly 5-10% depending on spell cast speed and flat damage amounts. 
