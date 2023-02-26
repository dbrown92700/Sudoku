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

    def __init__(self, init_input):
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
                output_character = '-'
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


def identify_pairs(init_dataset):

    # Search for 2 cells with only 2 numbers each that mach
    #   Create a set of all cells with only 2 numbers
    #   Recursively check for matches

    dataset = []
    for init_list in init_dataset:
        dataset.append(init_list.copy())
    pair_results = []
    hard_pairs = []
    for cell_num, candidates in enumerate(dataset):
        if len(candidates) == 2:
            hard_pairs.append({'pair': candidates, 'cell_num': cell_num})
    if len(hard_pairs) > 1:
        for first_pair in range(len(hard_pairs) - 1):
            for second_pair in range(first_pair+1, len(hard_pairs)):
                if hard_pairs[first_pair]['pair'] == hard_pairs[second_pair]['pair']:
                    pair_results.append({'pair': hard_pairs[first_pair]['pair'].copy(),
                                         'cells': [hard_pairs[first_pair]['cell_num'],
                                                   hard_pairs[second_pair]['cell_num']]})
    for result in pair_results:
        for candidates in dataset:
            for candidate in result['pair']:
                if candidate in candidates:
                    candidates.remove(candidate)

    candidate_cells = {1: [], 2: [], 3: [], 4: [], 5: [], 6: [], 7: [], 8: [], 9: []}
    for cell_num, candidates in enumerate(dataset):
        for candidate in candidates:
            candidate_cells[candidate].append(cell_num)
    for candidate in range(1, 10):
        if len(candidate_cells[candidate]) != 2:
            del candidate_cells[candidate]
    candidates = list(candidate_cells.keys())
    candidates_qty = len(candidates)
    if candidates_qty > 1:
        for first_candidate in range(candidates_qty-1):
            for second_candidate in range(first_candidate+1, candidates_qty):
                if candidate_cells[candidates[first_candidate]] == candidate_cells[candidates[second_candidate]]:
                    pair_results.append({'pair': [candidates[first_candidate], candidates[second_candidate]],
                                         'cells': candidate_cells[candidates[first_candidate]]})

    for result in pair_results:
        for candidates in dataset:
            for candidate in result['pair']:
                if candidate in candidates:
                    candidates.remove(candidate)
        for cell in result['cells']:
            dataset[cell] = result['pair']

    return pair_results, dataset


class Sudoku:

    def __init__(self, sudoku_file):
        self.matrix = []
        with open(sudoku_file) as s_file:
            for line in s_file.readlines():
                row = []
                for cell in list(line.rstrip('\n')):
                    row.append(Cell(cell))
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

        return_values = {'all_values': [], 'all_candidates': [], 'dataset': []}
        for cell_num, cell in enumerate(self.matrix[row_num]):
            return_values['dataset'].append(cell.candidates)
            if cell_num == col_num:
                continue
            if cell.status in ['Input', 'Final']:
                return_values['all_values'].append(cell.value)
            else:
                return_values['all_candidates'] = list(set(return_values['all_candidates'] + cell.candidates))
        return return_values

    def column_values(self, row_num, col_num):

        return_values = {'all_values': [], 'all_candidates': [], 'dataset': []}
        for this_row_num, row in enumerate(self.matrix):
            cell = row[col_num]
            return_values['dataset'].append(cell.candidates)
            if row_num == this_row_num:
                continue
            if cell.status in ['Input', 'Final']:
                return_values['all_values'].append(cell.value)
            else:
                return_values['all_candidates'] = list(set(return_values['all_candidates'] + cell.candidates))
        return return_values

    def cell_values(self, row_num, col_num):

        return_values = {'all_values': [], 'all_candidates': [], 'dataset': []}
        bigcell_row = int(row_num / 3)
        bigcell_col = int(col_num / 3)
        for this_cell_row in range(bigcell_row * 3, (bigcell_row + 1) * 3):
            for this_cell_col in range(bigcell_col * 3, (bigcell_col + 1) * 3):
                cell = self.matrix[this_cell_row][this_cell_col]
                return_values['dataset'].append(cell.candidates)
                if (this_cell_col == col_num) and (this_cell_row == row_num):
                    continue
                if cell.status in ['Input', 'Final']:
                    return_values['all_values'].append(cell.value)
                else:
                    return_values['all_candidates'] = list(set(return_values['all_candidates'] + cell.candidates))
        return return_values

    def eliminate_candidates(self):
        solved_count = 0
        eliminated_count = 0
        print(f'{bcolors.BOLD}Eliminate candidates and find sole candidates.{bcolors.ENDC}')

        for row_num, row in enumerate(self.matrix):
            for cell_num, cell in enumerate(row):
                if cell.status in ['Input', 'Final']:
                    continue
                this_cell_values = self.cell_values(row_num, cell_num)
                this_col_values = self.column_values(row_num, cell_num)
                this_row_values = self.row_values(row_num, cell_num)
                for candidate_value in cell.candidates.copy():

                    # If candidate is Final elsewhere in row, col or cell, delete it

                    if candidate_value in this_row_values['all_values'] + this_col_values['all_values'] + \
                            this_cell_values['all_values']:
                        cell.candidates.remove(candidate_value)
                        eliminated_count += 1
                        # print(f'Remove {candidate_value}')
                        if len(cell.candidates) == 1:
                            cell.value = cell.candidates[0]
                            cell.candidates = []
                            cell.status = 'Final'
                            print(f'Row:{row_num+1} Col:{cell_num+1} Value:{cell.value} -> Other Candidates Eliminated')
                            solved_count += 1
                            break
                        continue

                    # If candidate is not candidate elsewhere in cell, row or col, make it Final

                    if candidate_value not in this_row_values['all_candidates']:
                        reason = f'Only {candidate_value} in Row'
                    elif candidate_value not in this_col_values['all_candidates']:
                        reason = f'Only {candidate_value} in Column'
                    elif candidate_value not in this_cell_values['all_candidates']:
                        reason = f'Only {candidate_value} in Cell'
                    else:
                        continue

                    cell.value = candidate_value
                    cell.candidates = []
                    cell.status = 'Final'
                    print(
                        f'Row:{row_num + 1} Col:{cell_num + 1} Value:{cell.value} -> {reason}')
                    solved_count += 1
                    break

        return {'solved': solved_count, 'eliminated': eliminated_count}

    def apply_pairs(self):

        start_stats = self.stats_count()
        pairs_found = 0
        print(f'{bcolors.BOLD}Find and apply pairs.{bcolors.ENDC}')

        # Evaluate Rows for Pairs

        for row_num in range(9):
            dataset = self.row_values(row_num, 0)['dataset']
            pair_results, result_dataset = identify_pairs(dataset)
            if pair_results:
                print(f'Row: {row_num}', pair_results)
                pairs_found += len(pair_results)
                all_cells = sum([result['cells'] for result in pair_results], [])
                for cell in range(9):
                    self.matrix[row_num][cell].candidates = result_dataset[cell].copy()
                    if cell in all_cells:
                        self.matrix[row_num][cell].status = 'Pair'

        # Evaluate Columns for Pairs

        for col_num in range(9):
            dataset = self.column_values(0, col_num)['dataset']
            pair_results, result_dataset = identify_pairs(dataset)
            if pair_results:
                print(f'Column: {col_num}', pair_results)
                pairs_found += len(pair_results)
                all_cells = sum([result['cells'] for result in pair_results], [])
                for cell in range(9):
                    self.matrix[cell][col_num].candidates = result_dataset[cell].copy()
                    if cell in all_cells:
                        self.matrix[cell][col_num].status = 'Pair'

        # Evaluate Cells for Pairs

        for row_num in range(0, 9, 3):
            for col_num in range(0, 9, 3):
                dataset = self.cell_values(row_num, col_num)['dataset']
                pair_results, result_dataset = identify_pairs(dataset)
                if pair_results:
                    print(f'Cell: {row_num}, {col_num}', pair_results)
                    pairs_found += len(pair_results)
                    all_cells = sum([result['cells'] for result in pair_results], [])
                    for cell in range(9):
                        cell_row = row_num + int(cell / 3)
                        cell_col = col_num + cell % 3
                        self.matrix[cell_row][cell_col].candidates = result_dataset[cell].copy()
                        if cell in all_cells:
                            self.matrix[cell_row][cell_col].status = 'Pair'

        end_stats = self.stats_count()

        return {'solved': start_stats["solved"] - end_stats["solved"],
                'eliminated': start_stats["candidates"] - end_stats["candidates"],
                'pairs_found': pairs_found}

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
            if results['solved'] + results['eliminated'] > 0:
                game.print_table()
