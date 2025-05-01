[CONTENT]
"Required packages": ["pygame"],

"Required Other language third-party packages": [],

"Logic Analysis": [
    {
        "filename": "main.py",
        "classes": [
            {
                "class": "Main",
                "methods": [
                    {
                        "method": "main",
                        "description": "Entry point of the game that initializes the game loop."
                    }
                ]
            }
        ]
    },
    {
        "filename": "game.py",
        "classes": [
            {
                "class": "Game",
                "methods": [
                    {
                        "method": "start_game",
                        "description": "Initializes game settings and starts the game."
                    },
                    {
                        "method": "update",
                        "description": "Updates the game state, including player and enemy movements."
                    },
                    {
                        "method": "check_collisions",
                        "description": "Checks for collisions between bullets and tanks."
                    },
                    {
                        "method": "end_game",
                        "description": "Handles game termination and displays results."
                    }
                ]
            },
            {
                "class": "Player",
                "methods": [
                    {
                        "method": "move",
                        "description": "Moves the player's tank based on input direction."
                    },
                    {
                        "method": "fire_bullet",
                        "description": "Fires a bullet from the player's tank."
                    }
                ]
            },
            {
                "class": "Enemy",
                "methods": [
                    {
                        "method": "shoot",
                        "description": "Shoots bullets in a random direction."
                    }
                ]
            },
            {
                "class": "Score",
                "methods": [
                    {
                        "method": "add_points",
                        "description": "Adds points to the player's score."
                    },
                    {
                        "method": "get_score",
                        "description": "Retrieves the current score."
                    }
                ]
            }
        ]
    }
],

"Task list": [
    "main.py",
    "game.py",
    "game_data.txt",
    "health_data.txt"
],

"Shared Knowledge": [
    "Pygame documentation: https://www.pygame.org/docs/",
    "Python game development tutorials: https://realpython.com/pygame-a-primer/"
]
[/CONTENT]