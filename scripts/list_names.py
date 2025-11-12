#!/usr/bin/env python3
from pathlib import Path
import re

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
            known_as_match = re.search(r'known as(.+?)(\.?\s*)$', known_as_line)
            if not match:
                print('INVALID LINE:', line)
                assert False
                continue
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
