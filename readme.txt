The Adventures of Yolo

INTRO
-----
The Adventures of Yolo is a standard top-down scrolling
shooter, or more commonly known in the gaming world as a
"shmup" in the vein of other games such as Raiden,
Ikaruga, or Radiant Silvergun.  The general objective is
to shoot down targets that are trying to take your
character down as you survive a barrage of projectiles
sent your character's way.

You, under the guise of the anonymous "YOLO" (aptly named
"You Only Live Once), pilot a ship which travels and
tries to survive attacks by enemy ships.
In order to do fight back, your ship is accompanied by
three "drones".  Since your own ship is not a fighter ship itself, these
drones are your only offense and defense against the
enemy onslaught.

YOLO is accompanied by three drones (in some configurations
the third is not seeable and is attached underneath the
ship itself) which can be setup in 6 ways.  Each way
offers some benefit and drawback, and three of the
configurations actually allow for drone position modes
by the press of a button which will be explained in
depth shortly.

Alongside having three drones, the player can choose from
3 different weapons: Spray cannon, Torpedo, and Laser.
Likewise to the six setups, each weapon offers benefit
and drawback.


HOW TO PLAY
-----------
To start the game, run main.py using Python 2.7.2 or
compatible.

Arrow keys navigate through the title menu as well as
the equipment configuration screen, and enter is used
to confirm selections.  Pressing the ESC key either
returns the user to the title screen or exits the game
entirely.

After choosing a mode at the title menu, the player
will be taken to an equipment configuration screen
where the player can decide the Drone setup as well as
the desired weapon to use during the game.

Explanation of configurations:

STANDARD:  The standard lateral setup with tail drone.
	Offers some side protection and spread out shot
	group.
CONDENSED:  A more central-focused setup which offers
	no side protection but a more concentrated
	offense in the center with a front drone to
	act as a shield.
ROTATE:  Drones rotate around the ship to offer sporadic
	but circular protection around the ship at the
	cost of reliable accuracy.
*SNAKE:  Drones will follow the ship's movements.  
*CONTRACT:  The two lateral drones can come in or go out
	to the side.  A drone is attached underneath the
	ship.  Also, Spray behavior changes for the
	lateral drones on powerup.
*WIDEN:  The two lateral drones can be close or far at
	the side.  Another drone is underneath the ship.
	Likewise to CONTRACT, Spray behavior changes on
	powerup to have diagonal shots for the lateral
	drones.  CONTRACT and WIDEN are the only setups
	that behave in such a way.

* The starred configurations have a mode change:

SNAKE:  Doing a mode change determines whether or not
	the trail will return back to "home" position
	(at the same position as the ship) or not.
	The latter means the trail drones remain at their
	own position.
CONTRACT:  Doing a mode change either brings the two
	lateral drones in (a la CONDENSED) or brings
	them back out to the side.
WIDEN:  A mode change can send the drones far out to to
	the side or bring them back closer.

Explanation of weapons:

SPRAY:  The standard faire weapon, spray shoots out basic
	shots traditional of the genre.  They are weak, but
	can take down most projectiles.
TORPEDO:  Torpedos are slow in rate and speed compared to
	the other two weapons, but have high power and
	can destroy any projectile in the way.
LASER:  Lasers are thin piercing beams which can hit
	through any enemy without dissipating or decaying
	in strength, although they are incapable of
	taking down any other projectile, leaving one
	defenseless to onslaughts in front.  As long as
	they remain in contact with enemies, they will
	continue to damage them.

After selecting configurations, the player will finally start playing the game.

Here are the standard controls for the ship:
W		UP
A		LEFT
S		DOWN
D		RIGHT
SPACEBAR	SHOT
H		MODE CHANGE

Make sure to have caps lock off during play.

Explanation of modes:
CAMPAIGN:  The player will go through 4 stages of
	progressing difficulty.  After a while,
	each stage ends and the player transitions
	to the next stage.  After the 4th stage,
	the player is taken back to the title screen.
SURVIVAL:  A brutal endless mode where enemies have
	no mercy and become progressively more
	difficult during progression.

During the game, sometimes a powerup will be dropped
after shooting down a ship.  These powerups will
affect each weapon in a certain way:

SPRAY:  More bullets/angles/spread
TORPEDO:  More torpedos
LASER:  Increased strength

The player starts at power level 1.  Each powerup
increases the player's power level by 1 until the
player reaches level 10, which is the max level.
Afterwards, collecting more powerups will simply
increase the strength of the projectiles.

Explanation of shield and life meter:

The player starts out with full health and full shield
each stage.  The shield protects the player ship itself
from losing its health/life by absorbing impact caused
by the enemy in any which way.  Over time, the shield
can recharge.  However, absorbing too much at a time
can destroy the shield and leave the player ship
vulnerable.  Unlike the shield, life does not regenerate,
and any damage done is permanent until the next stage.
Be very careful how you use the shield to absorb
projectiles.

And there you have it.  The goal is to survive each
stage and move on to the next.  You only live once,
so no continues, so make the best of it.  2deep4u.


STRUCTURE - of data (general)
---------
main.py		- contains main() which starts the game
game.py		- the Game class is the core class
	that is central command to the entire game,
	everything takes place here, including the
	game loops
sprites.py	- ironically named, it only contains
	the Player class which defines the Player
	ship properties (my fault for naming it that)
drones.py	- Classes which define unique drone
	behaviors.  I'm proud of the trail and rotate
	ones personally.
enemy.py	- Enemy classes for enemy sprites
	with derivations of Enemy.
enemproj.py	- Enemy projectiles are instantiated
	by these classes.
level.py	- Level class which defines the
	visual properties of a stage such as the
	scrolling.
ScrollBG.py	- A class which defines a scrollable
	plane/layer, which can contain many images.
weapons.py	- Classes which define weaponry for
	the player ship.
various.py	- Assorted classes such as Animated
	Projectile classes and Overlay classes.
general.py	- General utility functions.
localdata.py	- Defines globals, so localdata is
	kind of a misnomer, but that too is my fault.


[author's notes]
------------
Furthermore, don't cheat by pressing either 1, 2, 3, or
p!  



RESOURCES AND CREDITS
---------
Artwork - Taken from other sources,
	Specified in the Documentation.
Music -
  Taken from other sources:
	Feeling_Dark.ogg - specified in the documentation
	MainTitle.ogg - specified in the documentation
  by James Stegner:
	deathangel.mp3
	shootatanything.ogg
 