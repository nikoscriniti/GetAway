# You can install the required dependencies by running:
# pip install pygame pytmx


Description:
This game is a 2D action game where the player controls a character through a series of movements and interactions. The objective is to navigate through obstacles, engage with enemies, and complete various levels. The game features animated sprites, collision detection, and interactive gameplay mechanics.

Features:
Player Movement: The player can move in four directions (up, down, left, right) using animated sprites.
Collision Detection: The game features detailed collision detection for player movement, enemy interactions, and environment.
Enemy Interaction: Enemies in the game can be defeated through collisions with bullets or other mechanics.
Customizable Settings: Game settings such as speed, animations, and difficulty can be adjusted through a configuration file.
Smooth Animations: The game features basic animations for different states (moving in different directions, idle).

Files:
main.py: Contains the main game loop, initialization, and game logic.
player.py: Handles player movement, sprite animation, and collision detection.
groups.py: Manages groups of sprites such as players, enemies, and bullets.
settings.py: Contains configurable game settings like speed, screen dimensions, and other gameplay parameters.
sprites.py: Defines various sprites used in the game such as enemies, bullets, and environmental objects.


-----------------------------------------------------------------------------------------------------------
How to Play:
Starting the Game:

After running the game with python main.py, the game window will open, and you'll be placed into the game environment.
Movement:

You control the player character using the arrow keys:
Up Arrow: Move up.
Down Arrow: Move down.
Left Arrow: Move left.
Right Arrow: Move right.
The player can move freely around the game world using these keys. The player character's sprite will animate depending on the direction of movement.
Interacting with the Environment:

As you move, your player will collide with various objects (enemies, obstacles) in the game. The game has a hitbox system, meaning your player won't go through solid objects like walls or enemies unless certain conditions (like defeating an enemy) are met.
Shooting/Combat (If Applicable):

Press the Spacebar to shoot bullets (this may vary depending on the context of the game, check the in-game instructions if provided).
Bullets will collide with enemies, and hitting an enemy will trigger a destruction animation and remove the enemy from the game.
Enemy Encounters:

Enemies will move and can engage in combat with the player. If the player’s hitbox intersects with an enemy’s hitbox, certain events will happen (such as the player losing health, or the enemy getting defeated).
Defeating enemies may involve shooting them or performing a specific action.
Winning/Losing:

The game might have specific levels, objectives, or conditions that define when you win or lose (for example, clearing all enemies, reaching a specific point in the game world, or losing all health). Keep an eye on in-game indicators like score or health.
Exiting the Game:

You can exit the game at any time by closing the game window or pressing a designated key (typically Esc, if implemented).
-----------------------------------------------------------------------------------------------------------
