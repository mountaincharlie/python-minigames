""" Leaderboards module for Python Minigames """

# imports
import gspread
from oauth2client.service_account import ServiceAccountCredentials
# remove at end of project (unless using for project)
# from pprint import pprint

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

# checking it works
# first_leaderboard = SHEET.worksheet('minesweeper')
# data = first_leaderboard.get_all_values()
# pprint(data)

# accessing rows/columns/cells (delete)
# row = first_leaderboard.row_values(2)
# col = first_leaderboard.col_values(2)
# cell = first_leaderboard.cell(2,2).value

# DEFINE 'sheets' in run.py
# sheets = ['minesweeper', 'hangman']


# welcome message function
def welcome_msg():
    print('Welcome to the Python Minigames Leaderboards!')


# finding all unique usernames using a set and | operator
def unique_usernames(sheets):
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


# test calling functions
# unique_usernames(sheets)