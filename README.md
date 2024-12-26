# Caster Damage Calc

A sketchy damage calc for Dark and Darker. It's currently just text output, but it's still as useful as a damage calc for a niche game can be. 
A GUI is tentatively planned, but will likely look pretty awful. There's a couple of hiccups with spell functionality I'm trying to figure out, and I hate UI work so that GUI might just never come about.

The goal was to seperate out all of the damage calc formulas from the gearsets/spell information so anyone could keep those updated and get accurate damage numbers and (I think) that's done. 
If you find any issues (specifically with the calculations / how some spells currently function), let me know. Feel free to DM me on Discord (Tanduras), or just @ me in the relevant chat. 


## Getting Started
Download the repo, run the code, see the numbers. 
If there are any issues/conflicts DM me and I can see about fixing it, but there shouldn't be any issues (on Windows) if you have a semi-recent version of Python or are just running the .exe. 
I have 0 idea how to actually support Mac, and if you're on Linux I'm gonna trust you know how to get it working for yourself. 

### Prerequisites
Don't trust random .exes from discord folk unless you really trust the dude, or know how to run them safely. 
If you do, you can run the .exe found in the dist folder and it should work without any finagling. 

Otherwise, you can install python and run the code in tester.py yourself for the text-based calculator. 

The JSON the .exe uses is seperate from the one used by the python code because I'm dumb and lazy. Keep the one you're using updated if you're not grabbing updates from here. 


### TODO
* Limb Calculations - unlikely to be shown in the text display, but needed for GUI stuff
* The GUI (gross) - It will probably just being another TKinter shit box like the previous to get it working. This will need to be done before anything below.
* Add Spell Generator to create new spells and damage profiles 
* Add Gear Profile Generator to more easily create gearsets for comparisons
* Add Data visualization portions for spells + additional damage breakdowns


### Bugs
* Channel Calcs are wrong, and I'm not sure what's the cause. It looks like channeled spells have 2 extra ticks (with .1s ticks). The math lines up, but the calc doesn't have these factored in, and I'm not certain this is correct. 
    * Generically, damage over time / channeled spells that do NOT have channel_interval scaling are off by roughly 5-10% depending on spell cast speed and flat damage amounts. 
