from abc import ABCMeta

# Game boards initialization

col_names = ['1', '2', '3', '4', '5', '6', '7', '8', '9', '10']
row_names = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J']
generic_board = {}
generic_pos = {'Coord': '', 'row': '', 'column': '', 'row_name_index': 0, 'column_name_index': 0}

for i in col_names:
    for j in row_names:
        key_name = j + i
        generic_board[key_name] = ''


# Class Definitions
class Settings:
    def __init__(self):
        # Nr of boats
        self.nrGunboats = 1
        self.nrCruisers = 0
        self.nrSubmarines = 0
        self.nrCarriers = 0
        self.nrDestroyers = 0


settings = Settings()


class Boat:
    __metaclass__ = ABCMeta

    def __init__(self):
        self.name = ''
        self.symbol = ''
        self.hp = 0
        self.size = 0
        self.position = []
        self.hasSunk = False

    def __str__(self):
        return '{} has {} hp.'.format(self.name, self.hp)

    def hit(self, coordinates):
        self.hp -= 1
        print('{} was hit! hp left = {}'.format(self.name, self.hp))
        self.position.pop(self.position.index(coordinates))
        if self.hp == 0:
            self.sink()

    def sink(self):
        print('{} has sunk!'.format(self.name))
        self.hasSunk = True


class Cruiser(Boat):
    def __init__(self, number):
        super(Cruiser, self).__init__()
        self.name = "Cruiser" + str(number)
        self.symbol = 'Cr'
        self.hp = 3
        self.size = 3


class Destroyer(Boat):
    def __init__(self, number):
        super(Destroyer, self).__init__()
        self.name = "Destroyer" + str(number)
        self.symbol = 'D'
        self.hp = 4
        self.size = 4


class Carrier(Boat):
    def __init__(self, number):
        super(Carrier, self).__init__()
        self.name = "Carrier" + str(number)
        self.symbol = 'Ca'
        self.hp = 5
        self.size = 5


class Submarine(Boat):
    def __init__(self, number):
        super(Submarine, self).__init__()
        self.name = "Submarine" + str(number)
        self.symbol = 'S'
        self.hp = 1
        self.size = 1


class Gunboat(Boat):
    def __init__(self, number):
        super(Gunboat, self).__init__()
        self.name = "Gunboat" + str(number)
        self.symbol = 'G'
        self.hp = 2
        self.size = 2


class Player:
    def __init__(self, name):
        self.name = name
        self.hp = 0  # Player hp is the sum of the hp's of his boats.
        print('Player {} has joined the game!'.format(self.name))
        self.boats = []
        self.board = generic_board.copy()
        self.hidden_board = generic_board.copy()

        #  Give boats to the player
        self.assign_boats()
        self.boat_placement()
        self.get_player_hp()

    def assign_boats(self):
        for i in range(1, settings.nrCarriers + 1):
            self.boats.append(Carrier(i))
        for i in range(1, settings.nrDestroyers + 1):
            self.boats.append(Destroyer(i))
        for i in range(1, settings.nrCruisers + 1):
            self.boats.append(Cruiser(i))
        for i in range(1, settings.nrGunboats + 1):
            self.boats.append(Gunboat(i))
        for i in range(1, settings.nrSubmarines + 1):
            self.boats.append(Submarine(i))

    def update_boards(self):
        self.board_values = list(self.board.values())
        self.hidden_board_values = list(self.hidden_board.values())
        print('')
        print('{:^43}{:^20}{:^43}'.format(43 * ' ', '***' + self.name + '***', 43 * ' '))
        print(
            '{:^3}|{:^3}|{:^3}|{:^3}|{:^3}|{:^3}|{:^3}|{:^3}|{:^3}|{:^3}|{:^3}{:^20}{:^3}|{:^3}|{:^3}|{:^3}|{:^3}|{:^3}|{:^3}|{:^3}|{:^3}|{:^3}|{:^3}'.format(
                '', col_names[0], col_names[1],
                col_names[2], col_names[3],
                col_names[4], col_names[5],
                col_names[6], col_names[7],
                col_names[8], col_names[9],
                20 * '',
                '', col_names[0], col_names[1],
                col_names[2], col_names[3],
                col_names[4], col_names[5],
                col_names[6], col_names[7],
                col_names[8], col_names[9]))

        print(
            '{:^3}+{:^3}+{:^3}+{:^3}+{:^3}+{:^3}+{:^3}+{:^3}+{:^3}+{:^3}+{:^3}{:^20}{:^3}+{:^3}+{:^3}+{:^3}+{:^3}+{:^3}+{:^3}+{:^3}+{:^3}+{:^3}+{:^3}'.format(
                3 * '-',
                3 * '-', 3 * '-', 3 * '-', 3 * '-',
                3 * '-', 3 * '-', 3 * '-', 3 * '-',
                3 * '-', 3 * '-',
                20 * '',
                3 * '-', 3 * '-', 3 * '-', 3 * '-',
                3 * '-', 3 * '-', 3 * '-', 3 * '-',
                3 * '-', 3 * '-', 3 * '-'))

        for i in range(10):
            print(
                '{:^3}|{:^3}|{:^3}|{:^3}|{:^3}|{:^3}|{:^3}|{:^3}|{:^3}|{:^3}|{:^3}{:^20}{:^3}|{:^3}|{:^3}|{:^3}|{:^3}|{:^3}|{:^3}|{:^3}|{:^3}|{:^3}|{:^3}'.format(
                    row_names[i], self.board_values[i],
                    self.board_values[i + 10],
                    self.board_values[i + 20],
                    self.board_values[i + 30],
                    self.board_values[i + 40],
                    self.board_values[i + 50],
                    self.board_values[i + 60],
                    self.board_values[i + 70],
                    self.board_values[i + 80],
                    self.board_values[i + 90],
                    20 * '',
                    row_names[i], self.hidden_board_values[i],
                    self.hidden_board_values[i + 10],
                    self.hidden_board_values[i + 20],
                    self.hidden_board_values[i + 30],
                    self.hidden_board_values[i + 40],
                    self.hidden_board_values[i + 50],
                    self.hidden_board_values[i + 60],
                    self.hidden_board_values[i + 70],
                    self.hidden_board_values[i + 80],
                    self.hidden_board_values[i + 90],
                ))
            print(
                '{:^3}+{:^3}+{:^3}+{:^3}+{:^3}+{:^3}+{:^3}+{:^3}+{:^3}+{:^3}+{:^3}{:^20}{:^3}+{:^3}+{:^3}+{:^3}+{:^3}+{:^3}+{:^3}+{:^3}+{:^3}+{:^3}+{:^3}'.format(
                    3 * '-',
                    3 * '-', 3 * '-', 3 * '-', 3 * '-',
                    3 * '-', 3 * '-', 3 * '-', 3 * '-',
                    3 * '-', 3 * '-',
                    20 * '',
                    3 * '-', 3 * '-', 3 * '-', 3 * '-',
                    3 * '-', 3 * '-', 3 * '-', 3 * '-',
                    3 * '-', 3 * '-', 3 * '-'))

    def boat_placement(self):

        def validate_start_pos(my_boat) -> tuple[dict, list]:
            user_input_ok = False
            valid = False
            my_start_pos = generic_pos.copy()
            my_possible_end_pos = []

            while not user_input_ok or not valid:
                # Returns boat start position, if it is valid and a list of possible end positions
                self.update_boards()
                my_start_pos = generic_pos.copy()
                my_possible_end_pos = []

                my_start_pos['Coord'] = input(
                    'Insert your {} start position coordinates (A1 to J10): '.format(my_boat.name)).upper()
                if my_start_pos['Coord'] in list(self.board.keys()):

                    if self.board[my_start_pos['Coord']] == '':

                        # Get row and column of the start pos and their indexes on the row and col list
                        my_start_pos['row'] = my_start_pos['Coord'][0]
                        my_start_pos['column'] = my_start_pos['Coord'][1:]
                        my_start_pos['row_name_index'] = row_names.index(my_start_pos['row'])
                        my_start_pos['column_name_index'] = col_names.index(my_start_pos['column'])
                        adjacency_ok = check_adjacent(my_start_pos['row_name_index'], my_start_pos['column_name_index'])
                        if not adjacency_ok:
                            print('Invalid input. Boat cannot be adjacent to another boat. ')
                            input('Press Enter to continue...')
                            user_input_ok = False
                        else:
                            user_input_ok = True
                    else:
                        print('Invalid input. Boat cannot be placed on top of another boat.')
                        input('Press Enter to continue...')
                        user_input_ok = False
                else:
                    print('Invalid input. Insert correct coordinate input (A1 to J10).')
                    input('Press Enter to continue...')
                    user_input_ok = False

                if user_input_ok:
                    if not isinstance(my_boat, Submarine):
                        mid_ok = True  # True by default. Only check if boat size larger than 3.

                        my_end_pos = generic_pos.copy()
                        mid_pos = generic_pos.copy()
                        # Bottom direction
                        try:  # Check if we are out of the board
                            my_end_pos['row_name_index'] = my_start_pos['row_name_index'] + my_boat.size - 1
                            my_end_pos['row'] = row_names[my_end_pos['row_name_index']]
                        except IndexError:
                            pass
                        else:
                            if my_end_pos['row_name_index'] >= 0:
                                my_end_pos['column'] = my_start_pos['column']
                                my_end_pos['column_name_index'] = col_names.index(my_end_pos['column'])
                                my_end_pos['Coord'] = my_end_pos['row'] + my_end_pos['column']

                                # If the boat size is larger than 3, we check the adjacency on the middle cells.
                                if my_boat.size > 3:
                                    mid_pos['row_name_index'] = my_end_pos['row_name_index'] - 2
                                    mid_pos['row'] = row_names[mid_pos['row_name_index']]
                                    mid_pos['column'] = my_start_pos['column']
                                    mid_pos['column_name_index'] = col_names.index(mid_pos['column'])
                                    mid_pos['Coord'] = mid_pos['row'] + mid_pos['column']
                                    mid_ok = check_adjacent(mid_pos['row_name_index'], mid_pos['column_name_index'])

                                end_ok = check_adjacent(my_end_pos['row_name_index'], my_end_pos['column_name_index'])

                                if mid_ok and end_ok:
                                    my_possible_end_pos.append(my_end_pos)
                        finally:
                            pass

                        my_end_pos = generic_pos.copy()
                        mid_pos = generic_pos.copy()
                        # Top direction
                        try:  # Check if we are out of the board
                            my_end_pos['row_name_index'] = my_start_pos['row_name_index'] - my_boat.size + 1
                            my_end_pos['row'] = row_names[my_end_pos['row_name_index']]
                        except IndexError:

                            pass
                        else:
                            if my_end_pos['row_name_index'] >= 0:
                                my_end_pos['column'] = my_start_pos['column']
                                my_end_pos['column_name_index'] = col_names.index(my_end_pos['column'])
                                my_end_pos['Coord'] = my_end_pos['row'] + my_end_pos['column']

                                # If the boat size is larger than 3, we check the adjacency on the middle cells.
                                if my_boat.size > 3:
                                    mid_pos['row_name_index'] = my_end_pos['row_name_index'] + 2
                                    mid_pos['row'] = row_names[mid_pos['row_name_index']]
                                    mid_pos['column'] = my_start_pos['column']
                                    mid_pos['column_name_index'] = col_names.index(mid_pos['column'])
                                    mid_pos['Coord'] = mid_pos['row'] + mid_pos['column']
                                    mid_ok = check_adjacent(mid_pos['row_name_index'], mid_pos['column_name_index'])

                                end_ok = check_adjacent(my_end_pos['row_name_index'], my_end_pos['column_name_index'])

                                if mid_ok and end_ok:
                                    my_possible_end_pos.append(my_end_pos)
                        finally:
                            pass

                        my_end_pos = generic_pos.copy()
                        mid_pos = generic_pos.copy()

                        # Right direction
                        try:  # Check if we are out of the board
                            my_end_pos['column_name_index'] = my_start_pos['column_name_index'] + my_boat.size - 1
                            my_end_pos['column'] = col_names[my_end_pos['column_name_index']]
                        except IndexError:
                            pass
                        else:
                            if my_end_pos['column_name_index'] >= 0:
                                my_end_pos['row'] = my_start_pos['row']
                                my_end_pos['row_name_index'] = row_names.index(my_end_pos['row'])
                                my_end_pos['Coord'] = my_end_pos['row'] + my_end_pos['column']

                                # If the boat size is larger than 3, we check the adjacency on the middle cells.
                                if my_boat.size > 3:
                                    mid_pos['column_name_index'] = my_end_pos['column_name_index'] - 2
                                    mid_pos['column'] = col_names[mid_pos['column_name_index']]
                                    mid_pos['row'] = my_start_pos['row']
                                    mid_pos['row_name_index'] = row_names.index(mid_pos['row'])

                                    mid_pos['Coord'] = mid_pos['row'] + mid_pos['column']
                                    mid_ok = check_adjacent(mid_pos['row_name_index'], mid_pos['column_name_index'])

                                end_ok = check_adjacent(my_end_pos['row_name_index'], my_end_pos['column_name_index'])

                                if mid_ok and end_ok:
                                    my_possible_end_pos.append(my_end_pos)
                        finally:
                            pass

                        my_end_pos = generic_pos.copy()
                        mid_pos = generic_pos.copy()

                        # Left direction
                        try:  # Check if we are out of the board
                            my_end_pos['column_name_index'] = my_start_pos['column_name_index'] - my_boat.size + 1
                            my_end_pos['column'] = col_names[my_end_pos['column_name_index']]
                        except IndexError:
                            pass
                        else:
                            if my_end_pos['column_name_index'] >= 0:
                                my_end_pos['row'] = my_start_pos['row']
                                my_end_pos['row_name_index'] = row_names.index(my_end_pos['row'])
                                my_end_pos['Coord'] = my_end_pos['row'] + my_end_pos['column']

                                # If the boat size is larger than 3, we check the adjacency on the middle cells.
                                if my_boat.size > 3:
                                    mid_pos['column_name_index'] = my_end_pos['column_name_index'] + 2
                                    mid_pos['column'] = col_names[mid_pos['column_name_index']]
                                    mid_pos['row'] = my_start_pos['row']
                                    mid_pos['row_name_index'] = row_names.index(mid_pos['row'])

                                    mid_pos['Coord'] = mid_pos['row'] + mid_pos['column']
                                    mid_ok = check_adjacent(mid_pos['row_name_index'], mid_pos['column_name_index'])

                                end_ok = check_adjacent(my_end_pos['row_name_index'], my_end_pos['column_name_index'])

                                if mid_ok and end_ok:
                                    my_possible_end_pos.append(my_end_pos)
                        finally:
                            pass

                        if len(my_possible_end_pos) == 0:
                            print('Invalid input. Boat will not fit there! You must have {} tiles for a {}.'.format(
                                my_boat.size,
                                my_boat.name))
                            input('Press Enter to continue...')
                            valid = False
                        else:
                            valid = True
                            self.board[my_start_pos['Coord']] = 'X'
                    else:
                        valid = True
                        self.board[my_start_pos['Coord']] = my_boat.symbol

            return my_start_pos, my_possible_end_pos

        def validate_end_pos(my_possible_end_pos, my_boat):

            my_end_pos = {}
            valid = False

            for i in my_possible_end_pos:
                self.board[i['Coord']] = '*'
            self.update_boards()
            print('Possible boat end position coordinates: ')
            possible_coordinates = [a['Coord'] for a in my_possible_end_pos]
            print(possible_coordinates)
            input_end_pos = input(
                'Insert your {} end position coordinates: '.format(my_boat.name)).upper()

            if input_end_pos in possible_coordinates:
                my_end_pos = my_possible_end_pos[possible_coordinates.index(input_end_pos)]
                for i in my_possible_end_pos:
                    self.board[i['Coord']] = ''
                valid = True

            return my_end_pos, valid

        def check_adjacent(row_index, col_index):
            # Size of "board"
            rows = 9
            cols = 9

            neighbors = lambda x, y: [(x2, y2) for x2 in range(x - 1, x + 2)
                                      for y2 in range(y - 1, y + 2)
                                      if (-1 < x <= rows and
                                          -1 < y <= cols and
                                          (x != x2 or y != y2) and
                                          (0 <= x2 <= rows) and
                                          (0 <= y2 <= cols))]

            for row_neighbor_index, col_neighbor_index in neighbors(row_index, col_index):
                name = row_names[row_neighbor_index] + str(col_names[col_neighbor_index])
                if self.board[name] not in ['', 'X']:
                    return False
            return True

        def place_boat(my_start_pos, my_end_pos, my_boat):  # This function needs some recoding.

            if not isinstance(my_boat, Submarine):
                coordinates = [my_start_pos['Coord'], my_end_pos['Coord']]
                coordinates.sort()

                if my_end_pos['row'] == my_start_pos['row']:  # Check if boat is horizontal
                    nums = [numbers[1:] for numbers in coordinates]  # Sort numeric values
                    aux = sorted(nums, key=int)

                    for column in range(col_names.index(aux[0]), (col_names.index(aux[1])) + 1):
                        coord = my_start_pos['row'] + col_names[column]
                        my_boat.position.append(coord)
                else:
                    for row in range(row_names.index(coordinates[0][0]), (row_names.index(coordinates[1][0])) + 1):
                        coord = row_names[row] + my_start_pos['column']
                        my_boat.position.append(coord)
            else:
                coord = my_start_pos['Coord']
                my_boat.position.append(coord)

            for position in my_boat.position:
                self.board[position] = my_boat.symbol

        end_pos = {}

        print('***************** Boat position rules: *****************')
        print('- Boats cannot be adjacent.\n- Boats cannot intersect boats.')
        for boat in self.boats:

            # Input and validate boat start position
            # Check for possible end positions, depending on starting position, boat intersections, adjacency
            # and start location
            start_pos, possible_end_pos = validate_start_pos(boat)

            if isinstance(boat, Submarine):
                pass
            else:
                valid_user_input = False
                while not valid_user_input:
                    end_pos, valid_user_input = validate_end_pos(possible_end_pos, boat)

            place_boat(start_pos, end_pos, boat)

    def get_player_hp(self):
        hp = 0
        for boat in self.boats:
            hp += boat.hp
        self.hp = hp


def check_hit(my_attacking_player, my_defending_player, my_shot_coordinates):
    #  Searches all defending player's boats positions.
    #  If no matches, it's a missed shot.
    for boat in my_defending_player.boats:

        if my_shot_coordinates in boat.position:
            boat.hit(my_shot_coordinates)
            my_defending_player.board[my_shot_coordinates] = 'X'
            my_attacking_player.hidden_board[my_shot_coordinates] = 'X'
            return True

    print('Shot missed!')
    if my_defending_player.board[
        my_shot_coordinates] != 'X':  # Prevent from writing * if it was repeated shot on a hit boat.
        my_defending_player.board[my_shot_coordinates] = '*'
        my_attacking_player.hidden_board[my_shot_coordinates] = '*'
    return False


def swap_player_turn():  # Returns attacking player and defending player
    global player_turn
    if player_turn == 1:
        player_turn = 2
        return player2, player1
    else:
        player_turn = 1
        return player1, player2


def check_win(my_attacking_player, my_defending_player):
    my_defending_player.get_player_hp()
    if my_defending_player.hp == 0:
        print("Player {} is victorious!!".format(my_attacking_player.name))
        return True
    return False


player_turn = 0
shot_coordinates = ''
player1 = Player('Daniel')
player2 = Player('Jakim')

shots_taken = 0
win = False
while not win:
    attacking_player, defending_player = swap_player_turn()
    user_input_ok = False
    while not user_input_ok:
        attacking_player.update_boards()
        shot_coordinates = input('{}, insert your shot coordinates (A1 to J10): '.format(attacking_player.name)).upper()
        user_input_ok = shot_coordinates in list(attacking_player.board.keys())

    hit = check_hit(attacking_player, defending_player, shot_coordinates)
    attacking_player.update_boards()
    input('Press Enter to continue...')
    win = check_win(attacking_player, defending_player)
