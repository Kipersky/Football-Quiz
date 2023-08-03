   # Football Quiz
 #### Video Demo:  <https://youtu.be/ilp4bv_-Y3w>
 ## Description
 Football Quiz is my final project for CS50 CS50's Introduction to Programming with Python. As a fooball (the european version) fan I always enjoyed being able to check my knowledge regarding my favourite sport. Now I made it possible for others using this simple code.

 ## Folder contents
 - **project.py**: This file contains all of the code used to run the game with all of it's functions.
 - **test_project.py**: This file contains a couple of tests for project.py file.
 - **highscore.csv**: This file stores user's name, score and date they finished the game.
 - **requirements.txt**: This file contains a list of all python libraries that are necessary to run the code.

 ## Libraries used
 - ```requests``` : for sending HTTP/1.1 requests to the website (wikipedia) containing footballers list and individual footbaler's data
 - ```bs4``` : for scraping the data from wikipedia
 - ```re``` : for finding desires data in lines of html
 - ```random``` : for randomly choosing footballer
 - ```tabulate``` : for presenting player's history and scoreboard in a form of a table
 - ```sys``` : for exiting the program after finished game
 - ```unidecode``` : for ignoring accented characters in players' names
 - ```csv``` : for storing the scoreboard as csv file
 - ```datetime``` : for getting date and time of finished game
 - ```os``` : for clearing the terminal after each step of the game

 ## Games mechanics
 - Run the program via
 ```
 python project.py
 ```
 - Program scrapes "https://en.wikipedia.org/wiki/List_of_UEFA_Champions_League_top_scorers" for a list of footballers and gets their names and wikipedia pages urls. Then randomly chooses one of them.
 - A welcoming message is printed. User is asked to enter a name. It will be later used in the scoreboard.
 - A table with history of the first randomly chosen player appears.
 - User is asked to choose between guessing player's name, taking a hint, skipping to next player or quitting the game.
     - If user chooses to guess program prompts "Your guess: ". If user inputs correct name program prints "Congratulations" and "Yor score: x" (x = 3 if the user guessed without hints, x = 2 if user guessed with 1 hint, x = 1 if player guessed with 2 hints.) and next player's history is printed. If user guessed wrong a "Try again" message is shown and user is presented again with a choice what to do next.
     - If user chooses to take a hint he is presented with a hint. First hint is the player's national team and second is first letter of player's first(if applicable) name. There are only 2 hints per player.
     - If user chooses to skip to next player the correct answer is shown, a new player's history is presented and user has to choose his action again. Each skip costs the player a "life" which are represented by heart emoji under the table with player's history. After loosing all 3 of them a "GAME OVER" message is printed. Player is presented with his score and a scoreboard containing all previous games.
     - If the player choose to quit before using all his lives he is presented with a correct answer to last question, his final score and the scoreboard.

 ## Documentation

 ### project.py Functions (excluding main)
 ```python
 def highscore(name, final_score):
 ```
 **Description:**
 - Adds user's name, final score and date to the scoreboard stored in a csv file. Returns the updated scoreboard in a form of a table

 **Args:**
 - ```name``` (```str```): user's name
 - ```final_score``` (```int```): sum of points user gained each round

 **Returns:**
 - ```str```: scoreboard table formatted with tabulate
 ```python
 def get_player_names(url):
 ```
 **Description:**
 - Scrapes wikipedia page's html and returns tags containing player's name and url to his wikipedia page.

 **Args:**
 - ```url``` (```str```): Wikipedia page containing a list of footballers

 **Returns:**
 - ```class bs4.NavigableString```: tags containing players' data
 ```python
 def get_names(player_names):
 ```
 **Description:**
 - Takes tags scrapped from wikipedia page and returns list of player's names

 **Args:**
 - ```player_names``` (```class bs4.NavigableString```): tags containing players' data

 **Returns:**
 - ```list```: list of stringd containing players' names
 ```python
 def get_wikis(player_names):
 ```
 **Description:**
 - Takes tags scrapped from wikipedia page and returns list of player's wikpedia pages

 **Args:**
 - ```player_names``` (```class bs4.NavigableString```): tags containing players' data

 **Returns:**
 - ```list```: list of strings containing players' wikipedia pages
 ```python
 def get_player_history(url):
 ```
 **Description:**
 - Takes individual player's wikipedia page url and scrapes page for club history

 **Args:**
 - ```url``` (```str```): individual player's wikipedia page url

 **Returns:**
 - ```str```: list containing club's player played for in a form of a table formatted with tabulate
 ```python
 def get_player_nat(url):
 ```
 **Description:**
 - Takes individual player's wikipedia page url and scrapes page for national team

 **Args:**
 - ```url``` (```str```): individual player's wikipedia page url

 **Returns:**
 - ```str```: player's nationa team
