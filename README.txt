Author : françois zajéga - frankie@frankiezafe.org
Release date: 28/09/2013
**************************************************

3D Avatar control via OSC / puredata > blender

**************************************************

* Requirements:
- puredata extended (pd-extended) > http://
- blender 2.67 (not tested on other releases) > http://
And that's it! You're ready to run this incredible demo :)

* Steps (after unzip):
- open pd/controller.pd
- if your mouse cursor is a hand (and not an arrow), press ctrl+e
- open avatar_osc.blend
- put your mouse in the 3D panel and press ctrl+p
- go back to pd and play with the sliders, you'll see the body parts move.

* Explanations:
There are 3 sliders per bones in puredata. They are all packed together by an external called packbone.pd and send to via OSC.
In blender, the first time the script is executed, all the bones of the armature are collected and stored in a collection.
An other list of eulers angles is created and set to 0.
On the second pass and all others, the eulers are applied on each bone regarding their names.
When an OSC message arrives, the script tries to locate the euler angle you want to modify. If it finds the name in the list, it stores the three angles.

**************************************************

Thanks to [name of the guy] for his "stdman" model: http://
This model is licensed under 
**************************************************

The rest of the project is under Creative Common Attribution 2.5
You must agree with this licence before using the enclosed media.

License : Attribution License 2.5
Detailled license : http://creativecommons.org/licenses/by/2.5/
