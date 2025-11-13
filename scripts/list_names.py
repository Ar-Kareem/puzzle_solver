#!/usr/bin/env python3
from pathlib import Path
import re

gallery_name_map = {
    'UnDead': 'Undead',
    'NumberMaze': 'Number Maze',
}

gallery_image_map = {
    'nonograms': 'nonogram_solved.png',
    'light_up': 'lightup_solved.png',
    'number_maze': 'numbermaze_solved.png',

    'minesweeper': 'minesweeper_pre.png',
    'inertia': 'inertia_unsolved.png',
    'guess': 'guess_3.png',
    'chess_range': 'chess_range_unsolved.png',
    'chess_solo': 'chess_solo_unsolved.png',
    'chess_melee': 'chess_melee_unsolved.png',
    'flip': 'flip_unsolved.png',
    'flood_it': 'flood_it_unsolved.png',
    'n_queens': '7_queens_solved.png',
}

def get_puzzle_names():
    d = Path('./src/puzzle_solver/puzzles')
    assert d.exists(), f'{d} does not exist'
    md_files = list(d.glob('**/README.md'))
    base_url = 'https://github.com/Ar-Kareem/puzzle_solver/tree/master/src/puzzle_solver/puzzles/'
    puzzle_names = {}
    puzzle_links = {}
    known_as = {}
    for f in md_files:
        text = f.read_text(encoding='utf-8')
        idx = [i for i, line in enumerate(text.split('\n')) if 'Puzzle Type ' in line]
        for i in idx:
            line = text.split('\n')[i]
            known_as_line = text.split('\n')[i+2]
            match = re.search(r'# (.+) \(Puzzle Type #(\d+)\)', line)  # extract "(Puzzle Type #\d+)"
            assert match
            known_as_match = re.search(r'known as(.+?)(\.?\s*)$', known_as_line)
            name = match.group(1)
            num = match.group(2)
            puzzle_names[num] = name
            puzzle_links[num] = base_url + f.relative_to(d).parent.as_posix()
            if known_as_match:
                known_as[num] = known_as_match.group(1)
    nums = sorted([int(x) for x in puzzle_names.keys()])
    assert set(nums) == set(range(1, len(nums) + 1))
    print('number of aliases:', len(known_as))
    print()
    out_txt = ''
    for i in nums:
        name = puzzle_names[str(i)]
        if str(i) in known_as:
            known_as_name = ' (Also known as' + known_as[str(i)] + ')'
        else:
            known_as_name = ' '
        out_txt += f'{i:02d}. [{name}]({puzzle_links[str(i)]}){known_as_name}\n'
    replace_in_readme(out_txt, 'ALIASES')

    base_image_url = 'https://raw.githubusercontent.com/Ar-Kareem/puzzle_solver/master/images/puzzles/'
    gallery_txt = '<tr>\n'
    count = 0
    for i in nums:
        name = puzzle_names[str(i)]
        name = gallery_name_map.get(name, name)
        name_norm = name.replace(' ', '_').replace('-', '_').lower()
        link = puzzle_links[str(i)]
        if name_norm in gallery_image_map:
            image = base_image_url + gallery_image_map[name_norm]
        else:
            image = base_image_url + f'{name_norm}_solved.png'
        if count%5 == 0 and count > 0:
            gallery_txt += '</tr>\n<tr>\n'
        gallery_txt += '  <td align="center">\n'
        gallery_txt += f'    <a href="{link}"><b>{name}</b><br><br>\n'
        gallery_txt += f'      <img src="{image}" alt="{name}" width="140">\n'
        gallery_txt += '    </a>\n'
        gallery_txt += '  </td>\n'
        count += 1
    gallery_txt += '</tr>\n'
    replace_in_readme(gallery_txt, 'GALLERY')

def replace_in_readme(text, section_name):
    readme_path = Path('./README.md')
    start_marker = f'<!-- AUTO-GENERATED {section_name} START -->'
    end_marker = f'<!-- AUTO-GENERATED {section_name} END -->'
    old_text = readme_path.read_text(encoding='utf-8')
    start_idx = old_text.find(start_marker)
    end_idx = old_text.find(end_marker)
    assert start_idx != -1 and end_idx != -1, f'{section_name} not found in README.md'
    assert start_idx < end_idx, f'{section_name} start index is greater than end index'
    start_idx += len(start_marker)
    assert readme_path.exists(), f'{readme_path} does not exist'
    new_text = old_text[:start_idx] + '\n\n' + text + '\n' + old_text[end_idx:]
    readme_path.write_text(new_text, encoding='utf-8')

if __name__ == '__main__':
    get_puzzle_names()
