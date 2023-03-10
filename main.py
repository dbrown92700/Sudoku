#!python3
import os


class bcolors:
    INIT = '\033[95m'
    INPUT = '\033[94m'
    SOLVED = '\033[92m'
    PAIR = '\033[93m'
    BORDER = '\033[96m'
    WORKING = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'


class Cell:

    def __init__(self, init_input, row_num, col_num):
        self.row = row_num
        self.col = col_num
        if init_input == '-':
            self.status = 'Init'
            self.candidates = [1, 2, 3, 4, 5, 6, 7, 8, 9]
            self.value = 0
        else:
            self.status = 'Input'
            self.candidates = []
            self.value = int(init_input)

    def print_cell(self, number, cell_split):
        if self.status in ('Input', 'Final'):
            if number == 5:
                output_character = self.value
            else:
                output_character = ' '
            if self.status == 'Input':
                output_color = bcolors.INPUT
            else:
                output_color = bcolors.SOLVED
        else:
            if number in self.candidates:
                output_character = number
            else:
                output_character = '-'
            output_color = bcolors.WORKING
            if self.status == 'Pair':
                output_color = bcolors.PAIR
            if len(self.candidates) == 9:
                output_color = bcolors.INIT
        end_character = ''
        if number in [3, 6, 9]:
            end_character = ' '
            if cell_split:
                end_character = f'{bcolors.BORDER}|'
        print(f'{output_color}{output_character}', end=end_character)

    def one_candidate_left(self):

        # All candidates but one eliminated. Mark as Final

        if len(self.candidates) == 1:
            self.value = self.candidates[0]
            self.candidates = []
            self.status = 'Final'
            print(f'Solved - Row {self.row}, Col {self.col} Value {self.value} - All Other Candidates Eliminated')
            return True
        else:
            return False


def identify_pairs(dataset, type):

    # dataset is a list of 9 Cells
    pairs_found = 0

    # Hard Pairs Algorithm
    # search dataset for a matching set of hard pairs
    for index1 in range(8):
        cell1 = dataset[index1]
        if len(cell1.candidates) == 2:
            for index2 in range(index1+1, 9):
                cell2 = dataset[index2]
                if cell2.candidates == cell1.candidates:
                    cell1.status = 'Pair'
                    cell2.status = 'Pair'
                    pairs_found += 1
                    print(f'Hard Pair {cell1.candidates} in {type} '
                          f'{cell1.row+1},{cell1.col+1} & {cell2.row+1},{cell2.col+1}')
                    # Remove candidates in identified pairs from remaining cells,
                    for candidate in cell1.candidates:
                        for cell in dataset:
                            if cell not in [cell1, cell2]:
                                if candidate in cell.candidates:
                                    cell.candidates.remove(candidate)
                                    cell_solved = cell.one_candidate_left

    # Soft Pairs Algorithm
    # Make a list of which cells a candidate appears in using candidate_cells
    candidate_cells = [[]]
    for candidate in range(1,10):
        candidate_list = []
        for cell in dataset:
            if candidate in cell.candidates:
                candidate_list.append(cell)
        candidate_cells.append(candidate_list)
    for first_candidate in range(1,9):
        if len(candidate_cells[first_candidate]) == 2:
            for second_candidate in range(first_candidate+1, 10):
                if candidate_cells[second_candidate] == candidate_cells[first_candidate]:
                    cell1 = candidate_cells[first_candidate][0]
                    cell2 = candidate_cells[first_candidate][1]
                    if len(cell1.candidates) == 2 and len(cell2.candidates) == 2:
                        # Skip previously found Hard Pair
                        continue
                    else:
                        pairs_found += 1
                        print(f'Soft Pair {[first_candidate, second_candidate]} in {type} '
                              f'{cell1.row+1},{cell1.col+1} & {cell2.row+1},{cell2.col+1}')
                        # Remove candidates in identified pairs from remaining cells,
                        # and copy pairs into identified cells to eliminate other candidates in those cells
                        for cell in candidate_cells[first_candidate]:
                            cell.candidates = [first_candidate, second_candidate]
                            cell.status = 'Pair'
                        for candidate in [first_candidate, second_candidate]:
                            for cell in dataset:
                                if cell not in candidate_cells[first_candidate]:
                                    if candidate in cell.candidates:
                                        cell.candidates.remove(candidate)
                                        cell_solved = cell.one_candidate_left

    return pairs_found


class Sudoku:

    def __init__(self, sudoku_file):
        self.matrix = []
        with open(sudoku_file) as s_file:
            for row_num, line in enumerate(s_file.readlines()):
                if line.rstrip(' \n') == '':
                    break
                row = []
                for col_num, cell in enumerate(list(line.rstrip('\n'))):
                    row.append(Cell(cell, row_num, col_num))
                self.matrix.append(row)

    def print_table(self):
        cell_divider = f'{bcolors.BORDER}+-----------------------------------+'
        cell_wall = f'{bcolors.BORDER}|           |           |           |'
        print(cell_divider)
        for row_num, row in enumerate(self.matrix):
            for candidate_row in range(3):
                print(f'{bcolors.BORDER}|', end='')
                for cell_num, cell in enumerate(row):
                    for candidate_col in range(3):
                        if cell_num % 3 == 2:
                            cell_split = True
                        else:
                            cell_split = False
                        cell.print_cell(candidate_row * 3 + candidate_col + 1, cell_split)
                print()
            if (row_num % 3) == 2:
                print(cell_divider)
            else:
                print(cell_wall)
        print(f'{bcolors.ENDC}')

    def row_values(self, row_num, col_num):

        return_values = []
        for cell_num, cell in enumerate(self.matrix[row_num]):
            return_values.append(cell)
        return return_values

    def column_values(self, row_num, col_num):

        return_values = []
        for this_row_num, row in enumerate(self.matrix):
            cell = row[col_num]
            return_values.append(cell)
        return return_values

    def sector_values(self, row_num, col_num):

        return_values = []
        bigcell_row = int(row_num / 3)
        bigcell_col = int(col_num / 3)
        for this_cell_row in range(bigcell_row * 3, (bigcell_row + 1) * 3):
            for this_cell_col in range(bigcell_col * 3, (bigcell_col + 1) * 3):
                cell = self.matrix[this_cell_row][this_cell_col]
                return_values.append(cell)
        return return_values

    def eliminate_candidates(self):
        solved_count = 0
        eliminated_count = 0
        print(f'{bcolors.BOLD}Eliminate candidates and find sole candidates.{bcolors.ENDC}')

        for row_num, row in enumerate(self.matrix):
            for col_num, cell in enumerate(row):
                if cell.status in ['Input', 'Final']:
                    continue
                other_sec_cells = self.sector_values(row_num, col_num).copy()
                other_col_cells = self.column_values(row_num, col_num).copy()
                other_row_cells = self.row_values(row_num, col_num).copy()
                for cell_array in [other_sec_cells, other_row_cells, other_col_cells]:
                    cell_array.remove(cell)
                all_other_cells = other_sec_cells + other_row_cells + other_col_cells
                all_other_values = sum([[iter_cell.value] for iter_cell in all_other_cells], [])
                other_sec_candidates = sum([iter_cell.candidates for iter_cell in other_sec_cells], [])
                other_row_candidates = sum([iter_cell.candidates for iter_cell in other_row_cells], [])
                other_col_candidates = sum([iter_cell.candidates for iter_cell in other_col_cells], [])

                for candidate_value in cell.candidates.copy():

                    # If candidate is Final elsewhere in row, col or cell, delete it

                    if candidate_value in all_other_values:
                        cell.candidates.remove(candidate_value)
                        eliminated_count += 1
                        if cell.one_candidate_left():
                            solved_count += 1
                            break
                        continue

                    # If candidate is not candidate elsewhere in cell, row or col, make it Final

                    if candidate_value not in other_row_candidates:
                        reason = f'Only {candidate_value} in Row'
                    elif candidate_value not in other_col_candidates:
                        reason = f'Only {candidate_value} in Column'
                    elif candidate_value not in other_sec_candidates:
                        reason = f'Only {candidate_value} in Cell'
                    else:
                        continue
                    cell.value = candidate_value
                    cell.candidates = []
                    cell.status = 'Final'
                    print(f'Solved - Row {row_num + 1}, Col {col_num + 1} Value {cell.value} - {reason}')
                    solved_count += 1
                    break

        return {'solved': solved_count, 'eliminated': eliminated_count}

    def apply_pairs(self):

        start_stats = self.stats_count()
        pairs_found = 0
        print(f'{bcolors.BOLD}Find and apply pairs.{bcolors.ENDC}')

        # Evaluate Rows for Pairs
        for row_num in range(9):
            dataset = self.row_values(row_num, 0)
            pairs_found += identify_pairs(dataset, 'Row')

        # Evaluate Columns for Pairs
        for col_num in range(9):
            dataset = self.column_values(0, col_num)
            pairs_found += identify_pairs(dataset, 'Column')

        # Evaluate Sectors for Pairs
        for row_num in range(0, 9, 3):
            for col_num in range(0, 9, 3):
                dataset = self.sector_values(row_num, col_num)
                pairs_found += identify_pairs(dataset, 'Sector')

        end_stats = self.stats_count()

        return {'solved': start_stats["solved"] - end_stats["solved"],
                'eliminated': start_stats["candidates"] - end_stats["candidates"],
                'pairs_found': pairs_found}

    def find_xwing(self):

        # Search all rows by candidate for doubles
        # Look for matching pair
        # Eliminate matching candidates from the pair columns
        # Do the same for columns -> rows

        eliminated_count = 0
        solved_count = 0
        eliminated = []
        print(f'{bcolors.BOLD}Find and X-Wing formations.{bcolors.ENDC}')

        for candidate in range(1, 10):
            candidate_cells = []
            for row_num in range(9):
                row_matches = []
                for col_num in range(9):
                    if candidate in self.matrix[row_num][col_num].candidates:
                        row_matches.append(col_num)
                candidate_cells.append(row_matches)
            for row1 in range(9):
                if len(candidate_cells[row1]) == 2:
                    for row2 in range(row1 + 1, 9):
                        if candidate_cells[row1] == candidate_cells[row2]:
                            print(f'X-wing for {candidate} on Rows {row1+1}, {row2+1} & Cols '
                                  f'{candidate_cells[row1][0]+1}, {candidate_cells[row1][1]+1}')
                            for row_num in range(9):
                                if row_num in [row1, row2]:
                                    continue
                                else:
                                    for col_num in candidate_cells[row1]:
                                        cell = self.matrix[row_num][col_num]
                                        if candidate in cell.candidates:
                                            cell.candidates.remove(candidate)
                                            eliminated_count += 1
                                            print(f'Eliminated {candidate} Cell {row_num}, {col_num}')
                                            eliminated.append({'value': candidate, 'cell': [row_num, col_num]})
                                            if cell.one_candidate_left():
                                                print(
                                                    f'Solved - Row:{row_num + 1} Col:{col_num + 1} Value:{cell.value} '
                                                    f'-> All Candidates Eliminated')
                                                solved_count += 1

            candidate_cells = []
            for col_num in range(9):
                col_matches = []
                for row_num in range(9):
                    if candidate in self.matrix[row_num][col_num].candidates:
                        col_matches.append(row_num)
                candidate_cells.append(col_matches)
            for col1 in range(9):
                if len(candidate_cells[col1]) == 2:
                    for col2 in range(col1 + 1, 9):
                        if candidate_cells[col1] == candidate_cells[col2]:
                            print(f'X-wing for {candidate} on Cols {col1+1}, {col2+1} & Rows '
                                  f'{candidate_cells[col1][0]+1}, {candidate_cells[col1][1]+1}')
                            for col_num in range(9):
                                if col_num in [col1, col2]:
                                    continue
                                else:
                                    for row_num in candidate_cells[col1]:
                                        cell = self.matrix[row_num][col_num]
                                        if candidate in cell.candidates:
                                            cell.candidates.remove(candidate)
                                            eliminated_count += 1
                                            eliminated.append({'value': candidate, 'cell': [row_num, col_num]})
                                            if cell.one_candidate_left():
                                                print(
                                                    f'Row:{row_num + 1} Col:{col_num + 1} Value:{cell.value} '
                                                    f'-> All Candidates Eliminated')
                                                solved_count += 1

        return {'solved': solved_count, 'eliminated': eliminated_count}

    def stats_count(self):

        total_solved = 0
        total_candidates = 0
        for row_num in range(9):
            for col_num in range(9):
                if self.matrix[row_num][col_num].status in ['Input', 'Final']:
                    total_solved += 1
                else:
                    total_candidates += len(self.matrix[row_num][col_num].candidates)
        return {'solved': total_solved, 'candidates': total_candidates}


if __name__ == '__main__':

    files = os.listdir()
    text_files = []
    menu_num = 1
    for file in files:
        if '.txt' in file:
            text_files.append(file)
            print(f'{menu_num:2}: {file}')
            menu_num += 1
    file_choice = input('Which file do you want to solve? ')
    filename = text_files[int(file_choice) - 1]

    game = Sudoku(filename)
    game.print_table()
    print(f'{bcolors.ENDC}\nEach block shows the candidate or final values in a cell.\nThey are color coded as '
          f'{bcolors.INPUT}Input Values, {bcolors.SOLVED}Solved, {bcolors.INIT}Initial Candidates, '
          f'{bcolors.WORKING}Remaining Candidates, {bcolors.ENDC}and {bcolors.PAIR}Matched Pair.'
          f'{bcolors.ENDC}\n')
    while game.stats_count()['solved'] < 81:
        response = input(f'\n{bcolors.UNDERLINE}Hit enter for next run or "quit" to stop: {bcolors.ENDC}')
        if response == 'quit':
            exit()
        else:
            print('\n\n')
        results = {'solved': 0, 'eliminated': 1}
        while results['solved'] + results['eliminated'] > 0:
            results = game.eliminate_candidates()
            print(results)
            if results['solved'] + results['eliminated'] > 0:
                game.print_table()
        results = {'solved': 0, 'eliminated': 1}
        while results['solved'] + results['eliminated'] > 0:
            results = game.apply_pairs()
            print(results)
            if results['solved'] + results['eliminated'] + results['pairs_found'] > 0:
                game.print_table()
        results = {'solved': 0, 'eliminated': 1}
        while results['solved'] + results['eliminated'] > 0:
            results = game.find_xwing()
            print(results)
            if results['solved'] + results['eliminated'] > 0:
                game.print_table()
