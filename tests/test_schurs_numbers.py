from puzzle_solver import schurs_numbers_solver as solver

def test_toy():
    n_colors = 3
    # colors = [f'C{i}' for i in range(n_colors)]
    colors = ['R', 'G', 'B']
    n = solver.find_max_n(colors=colors)
    print(f'max n = {n}')
    cnt, solutions = solver.SchurNumbers(colors=colors, n=n-1).count_num_ways()
    print(f'num ways to color {n-1} numbers with {n_colors} colors = {cnt}')
    solutions_str = []
    for solution in solutions:
        colors = sorted(solution.assignment.items(), key=lambda x: x[0])
        colors = [color[1] for color in colors]
        solutions_str.append(' '.join(colors))
    solutions_str = sorted(solutions_str)[::-1]
    for i, solution_str in enumerate(solutions_str):
        print(f'Way {i+1}:   ', solution_str)


if __name__ == '__main__':
    test_toy()
