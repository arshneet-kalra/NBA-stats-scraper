'''
Arshneet Kalra, 2332452, Prash Charlot, 2330052
Professor Robert Vincent
Programming Techniques and Applications
Final Project'''

# Program dependencies

# Make sure to pip install beatifulsoup4, requests and lxml

from bs4 import BeautifulSoup 
import cloudscraper
import os
import sys
import time


# Defining certain colors for the typewriter effect

green = "\033[0;92m"
BIGreen="\033[1;92m"
BIPurple="\033[1;95m" 
purple="\033[0;35m"       
blue="\033[0;34m"
red ="\033[0;31m"
yellow = "\033[0;93m"
grey_back="\033[0;40m"
reset = "\033[0m"


# Defining all of the functions to run the program


# Creating the typewriter effect

def typewriter(message):
    for char in message:
        sys.stdout.write(char)
        sys.stdout.flush()
        time.sleep(0.005) # Speed of the effect


# Will introduce the project while using the typewriter effect

def menu():
    os.system('clear') # Clear previous lines
    title = (BIPurple + "🏀Welcome to the NBA Player Stats Scraper🏀" + reset)
    typewriter(title)
    message = ("\n\nThis program, created by" + blue +" Arshneet Kalra"+reset+" and"+blue+" Prash Charlot"+reset+", utilizes BeautifulSoup to scrape data from a basketball stats website and present it to the user in a user-friendly format. Enjoy! \n\n")
    typewriter(message)


# This is the legend for summary stats, it explains what each abbreviation means

def legend():
    os.system('clear')
    legend = ("🏀" + BIGreen + "Legend:" + reset + "🏀\n G = Games Played\n PTS = Points Per Game\n TRB = Total Rebounds Per Game\n AST = Assists Per Game\n FG% = Field Goal Percentage\n FG3% = 3-Point Field Goal Percentage\n FT% = Free Throw Percentage\n eFG% = Effective Field Goal Percentage\n PER = Player Efficiency Rating\n WS = Winshare\n\n")
    typewriter(legend)


# This is the legend for seasonal stats, it explains what each abbreviation means

def legend_season():
    os.system('clear')
    legend_season = ("🏀" + BIGreen + "Season Stats Legend:" + reset + "🏀\n G = Games Played\n GS = Games Started\n MP = Minutes Played\n FG = Field Goals Made\n FGA = Field Goals Attempted\n FG% = Field Goal %\n 3P = 3-Point Made\n 3PA = 3-Point Attempted\n 3P% = 3-Point %\n FT = Free Throws Made\n FTA = Free Throws Attempted\n FT% = Free Throw %\n ORB = Offensive Rebounds\n DRB = Defensive Rebounds\n TRB = Total Rebounds\n AST = Assists\n STL = Steals\n BLK = Blocks\n TOV = Turnovers\n PF = Personal Fouls\n PTS = Points\n\n")
    typewriter(legend_season)

    
# Function the prompt the main program (right before the user is asked for the player name)

def main_program():
    
    # Player name input
    # A loop is used to restart if the user inputs an invalid prompt
    while True:
        
        # Make sure to create delay to prevent accidental mistyping
        time.sleep(0.1)
        
        # Remove leading and trailing blank spaces
        
        player_input = input('Input player first and last name: ').lower().strip()
        
        # Make sure that the name inputed is the first and last name
        try:
            first, last = player_input.split()
        except ValueError:
            print("Please enter the player's first and last name.")
            continue
            
        # Here we respect the formatting used by Basketball-reference to find a player
        first_letter = last[0]
        player_url_id = last.replace("'", '')[:5] + first[:2] 
        player_url = 'https://www.basketball-reference.com/players/' + first_letter + '/' + player_url_id + '01.html'

        # This is to call a request to access the site's html
        # code 200 is the default successful status, we make sure to obtain that code
        scraper = cloudscraper.create_scraper()
        req = scraper.get(player_url)
        if req.status_code != 200:
            print("Player not found.")
            continue
        break

    # This is to obtain the html
    html_text = scraper.get(player_url).text

    # Use BeautifulSoup to use lxml to process the html (will enable the use of .find commands and so on)
    soup = BeautifulSoup(html_text, 'lxml')
    
    # Finding the player name
    player_name = soup.find('h1').text.replace('\n', '')

    # Will print the legend before the rest of the code    
    legend()

    # Print name of the player as a title
    print(f"\nPlayer Found: {player_name}") #rewrite player name
    
    # This is to find the career summary of the player
    # Here we will specify that we're looking specifically the summary table, and not the whole soup file
    summary = soup.find('div', class_='stats_pullout')

    # Make sure that the summary table exists
    if summary:
        print("\nCareer Summary Stats:\n")
        
        # Find the group title
        group_title = summary.find_all('span', class_ = 'poptip')
        
        # Find the stat numbers (the first two are empty)
        p = summary.find_all('p')[3:]
        player_stats = []

        # The elements in p that happen to not be blank are the even indices
        for element in range(len(p)):
            if element % 2 == 0:
                player_stats.append(p[element])

        # Associate each title to its respective stat
        tuple = list(zip(group_title, player_stats))
        for i in range(len(tuple)):
            print(f'{tuple[i][0].text}: {tuple[i][1].text}')

    
    # Second part of the program where we return the average stats of the player in a given season
    
    def season_program():
        
        # Ask the user for which specific season they want to see stats for
        season_input = input("\nEnter a season (e.g., 2024-2025) to see stats: ").strip()

        # Input the legend for seasons
        legend_season()
        
        # Find per game stats
        tables = soup.find('div', id = 'all_per_game_stats')

        # Look through 3 seperate html classes
        titles = tables.find_all('th', class_ = ['poptip center', 'poptip sort_default_asc center', 'poptip hide_non_quals center'])[:31]

        # Check if the player has stats for this year
        table_non_text = soup.find('tr', id = f'per_game_stats.{season_input[-4:]}')

        # table_non_text will by typeNone if year not found
        if table_non_text != None:
            table = table_non_text.text
        else:
            print("Please input a year where the player played")

            # Will ask for year again
            season_program()

        # Associate each statline with its respective stat
        if table:
            table_list = table.split(' ')
            tuple_ = list(zip(titles, table_list[1:]))

            # 'Did Not Player' is written if the player retired mid-career
            if len(tuple_) < 29:
                print("Did Not Play")

                # Asks to whether they want to request another player to not
                loop()
            else:

                # Associate each title to its respective stat
                for i in range(len(tuple_)):
                    print(f'{tuple_[i][0].text}: {tuple_[i][1]}')

                # Asks to whether they want to request another player to not
                loop()

        # If we cant find the stat
        else:
            print("No per game stats table found.")
            loop()

    # Run season_program once part 1 of the program is done 
    season_program()

# Runs the menu bar
menu()

# Loop
while True:


    # Function to reprompt the player question without ever exiting the program
    
    def loop():
        user_input = input("\nWould you like to search for player? (yes/no): ").lower().strip()

        # If yes, continue program
        if user_input == 'yes':
            legend()
            main_program()

        # If no, exit program
        elif user_input == 'no':
            print("Thank you for using the NBA Player Stats Scraper!")
            exit()

        # else, reloop
        else:
            print("Invalid input. Please enter 'yes' or 'no'.")

    # Runs the loop function
    loop()