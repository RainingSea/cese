[CONTENT]
"Required packages": "Pygame",

"Required Other language third-party packages": "",

"Logic Analysis": [
    {
        "filename": "main.py",
        "classes": [
            {
                "class_name": "Main",
                "methods": [
                    {
                        "method_name": "main",
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
                "class_name": "Game",
                "methods": [
                    {
                        "method_name": "start",
                        "description": "Initializes the game state and starts the game loop."
                    },
                    {
                        "method_name": "update",
                        "description": "Updates the game state, including player movement and game ticks."
                    },
                    {
                        "method_name": "render",
                        "description": "Renders the current game state on the screen."
                    },
                    {
                        "method_name": "check_collisions",
                        "description": "Checks for collisions between the player ghost, walls, pellets, and monsters."
                    }
                ]
            },
            {
                "class_name": "PlayerGhost",
                "methods": [
                    {
                        "method_name": "move",
                        "description": "Moves the ghost in the specified direction based on user input."
                    },
                    {
                        "method_name": "eat_pellet",
                        "description": "Handles the logic for eating a regular pellet."
                    },
                    {
                        "method_name": "eat_superpellet",
                        "description": "Handles the logic for eating a superpellet and gaining special abilities."
                    }
                ]
            },
            {
                "class_name": "Monster",
                "methods": [
                    {
                        "method_name": "chase",
                        "description": "Chases the player's ghost based on its current position."
                    }
                ]
            },
            {
                "class_name": "Wall",
                "methods": []
            },
            {
                "class_name": "Pellet",
                "methods": []
            },
            {
                "class_name": "SuperPellet",
                "methods": []
            }
        ]
    }
],

"Task list": [
    "main.py",
    "game.py",
    "game_data.txt",
    "high_scores.txt"
],

"Shared Knowledge": "Follow Pygame conventions for game loops and event handling. Ensure clear separation of concerns in class design, with each class handling its specific responsibilities. Implement collision detection efficiently to minimize performance issues, especially as the number of game objects increases."
[/CONTENT]