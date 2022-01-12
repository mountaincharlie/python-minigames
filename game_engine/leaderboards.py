""" Leaderboards module for Python Minigames """

# imports
import gspread
from oauth2client.service_account import ServiceAccountCredentials
# to import run.py from parent directory
import sys
sys.path.append('.')
import run

# setting up the constant variabels for the API
SCOPE = [
    "https://spreadsheets.google.com/feeds",
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive.file",
    "https://www.googleapis.com/auth/drive"
]
CREDS = ServiceAccountCredentials.from_json_keyfile_name("creds.json", SCOPE)
CLIENT = gspread.authorize(CREDS)
SHEET = CLIENT.open("leaderboards")

# defining the leaderboards_menu outside main()
leaderboards_menu = run.menu_dict
leaderboards_menu.pop(str(len(leaderboards_menu)))


# finding all unique usernames using a set and | operator
def unique_usernames(sheets):
    """
    """
    usernames = set()
    # looping through each worksheet in the 'sheets' list
    for sheet in sheets:
        worksheet = SHEET.worksheet(sheet)  # getting the worksheet
        data = worksheet.col_values(2)  # getting the values in username col
        usernames |= set(data[1:])  # creating a union of both sets

    # converting the set into dictionary weith number keys
    usernames_dict = {}
    for i, name in enumerate(usernames):
        usernames_dict[i] = name
    return usernames_dict


# finding the row number to insert the user's data
def row_to_insert_at(score_list, user_score):
    """
    """
    for i in range(1, len(score_list)):
        # finds the first score its lower than
        if user_score <= int(score_list[i]):
            insert_at_row = i+1
            break
        # otherwise it will need to be added at the very end
        insert_at_row = len(score_list)+1
    return insert_at_row


# calculate the user's rank
def rank_generator(insert_at_row):
    """ Converts a number into a rank """
    num = insert_at_row
    if num in range(11, 14):
        place = 'th'
    elif str(num)[-1] == '1':
        place = 'st'
    elif str(num)[-1] == '2':
        place = 'nd'
    elif str(num)[-1] == '3':
        place = 'rd'
    else:
        place = 'th'
    rank = str(num) + place

    return rank


# fixing the rank column
def rank_refresh(leaderboard):
    """
    Takes the list of rank data.
    """
    rank_col = leaderboard.col_values(1)
    rank_title = rank_col.pop(0)
    new_rank_col = []

    for i in range(1, len(rank_col)+1):
        rank = rank_generator(i)
        new_rank_col.append(rank)
    new_rank_col.insert(0, rank_title)

    # inserting the new col data
    for i, rank in enumerate(new_rank_col):
        row = i+1
        leaderboard.update_cell(row, 1, rank)


def print_leaderboard_dict(leaderboards_menu):
    """
    """
    for key in leaderboards_menu:
        game_name = leaderboards_menu[key][5:]
        print(key, '-', game_name)


# choosing a leaderboard option
def leaderboard_choice(user, menu):
    """
    """
    while True:
        try:
            # make a leaderboard print functions?
            print('Leaderboards Menu:')
            print_leaderboard_dict(menu)

            leaderboard = input("\nEnter a number to select an option (or 'quit' to exit):\n")

            if leaderboard == 'quit':
                user.quit_status = leaderboard
                break
            elif leaderboard in menu:
                leaderboard_name = menu[leaderboard][5:]

                print(f'\nOpening the {leaderboard_name} leaderboard ...\n')

                # open and display the sheet
                print(f'{leaderboard_name.upper()} LEADERBOARD:')
                leaderboard_worksheet = SHEET.worksheet(leaderboard_name)
                data = leaderboard_worksheet.get_all_values()
                for row in data:
                    print(row[0], '--', row[1], '--', row[2])
                choice = input("\nHit ENTER to return to the Leaderboards Menu or 'quit' to return to the Main Menu:\n")
                if choice == 'quit':
                    user.quit_status = choice
                break
            else:
                raise ValueError
        except ValueError:
            print("\nInvalid entry. Enter a number from the options below.\nOr 'quit' to exit\n")


def main(user):
    """
    """
    # setting username and calling welcome message
    username = user.username
    # creating new instance of Player (so quit status doesnt affect in run.py)
    leaderboard_user = run.Player(username, 0, None, None)
    print(f'Welcome to the Python Minigames Leaderboards {leaderboard_user.username}!\n')

    # make leaderboard_choice function and call by
    while leaderboard_user.quit_status != 'quit':
        leaderboard_choice(leaderboard_user, leaderboards_menu)

    print(f'\nThank you for using the Python Minigame Leaderboards {username}!\n')
