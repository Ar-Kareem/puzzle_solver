from puzzle_solver.puzzles.abc_view import abc_view as abc_view_solver
from puzzle_solver.puzzles.aquarium import aquarium as aquarium_solver
from puzzle_solver.puzzles.area_51 import area_51 as area_51_solver
from puzzle_solver.puzzles.battleships import battleships as battleships_solver
from puzzle_solver.puzzles.binairo import binairo as binairo_solver
from puzzle_solver.puzzles.binairo import binairo_plus as binairo_plus_solver
from puzzle_solver.puzzles.black_box import black_box as black_box_solver
from puzzle_solver.puzzles.branches import branches as branches_solver
from puzzle_solver.puzzles.bridges import bridges as bridges_solver
from puzzle_solver.puzzles.chess_range import chess_range as chess_range_solver
from puzzle_solver.puzzles.chess_range import chess_solo as chess_solo_solver
from puzzle_solver.puzzles.chess_range import chess_melee as chess_melee_solver
from puzzle_solver.puzzles.circle_9 import circle_9 as circle_9_solver
from puzzle_solver.puzzles.connect_the_dots import connect_the_dots as connect_the_dots_solver
from puzzle_solver.puzzles.cow_and_cactus import cow_and_cactus as cow_and_cactus_solver
from puzzle_solver.puzzles.dominosa import dominosa as dominosa_solver
from puzzle_solver.puzzles.troix import dumplings as dumplings_solver
from puzzle_solver.puzzles.filling import filling as filling_solver
from puzzle_solver.puzzles.flood_it import flood_it as flood_it_solver
from puzzle_solver.puzzles.flip import flip as flip_solver
from puzzle_solver.puzzles.galaxies import galaxies as galaxies_solver
from puzzle_solver.puzzles.guess import guess as guess_solver
from puzzle_solver.puzzles.heyawake import heyawake as heyawake_solver
from puzzle_solver.puzzles.hidden_stars import hidden_stars as hidden_stars_solver
from puzzle_solver.puzzles.hidoku import hidoku as hidoku_solver
from puzzle_solver.puzzles.inertia import inertia as inertia_solver
from puzzle_solver.puzzles.kakurasu import kakurasu as kakurasu_solver
from puzzle_solver.puzzles.kakuro import kakuro as kakuro_solver
from puzzle_solver.puzzles.keen import keen as keen_solver
from puzzle_solver.puzzles.kropki import kropki as kropki_solver
from puzzle_solver.puzzles.kakuro import krypto_kakuro as krypto_kakuro_solver
from puzzle_solver.puzzles.light_up import light_up as light_up_solver
from puzzle_solver.puzzles.linesweeper import linesweeper as linesweeper_solver
from puzzle_solver.puzzles.link_a_pix import link_a_pix as link_a_pix_solver
from puzzle_solver.puzzles.magnets import magnets as magnets_solver
from puzzle_solver.puzzles.map import map as map_solver
from puzzle_solver.puzzles.mathema_grids import mathema_grids as mathema_grids_solver
from puzzle_solver.puzzles.minesweeper import minesweeper as minesweeper_solver
from puzzle_solver.puzzles.mosaic import mosaic as mosaic_solver
from puzzle_solver.puzzles.n_queens import n_queens as n_queens_solver
from puzzle_solver.puzzles.nonograms import nonograms as nonograms_solver
from puzzle_solver.puzzles.nonograms import nonograms_colored as nonograms_colored_solver
from puzzle_solver.puzzles.norinori import norinori as norinori_solver
from puzzle_solver.puzzles.number_path import number_path as number_path_solver
from puzzle_solver.puzzles.numbermaze import numbermaze as numbermaze_solver
from puzzle_solver.puzzles.nurikabe import nurikabe as nurikabe_solver
from puzzle_solver.puzzles.palisade import palisade as palisade_solver
from puzzle_solver.puzzles.lits import lits as lits_solver
from puzzle_solver.puzzles.pearl import pearl as pearl_solver
from puzzle_solver.puzzles.pipes import pipes as pipes_solver
from puzzle_solver.puzzles.range import range as range_solver
from puzzle_solver.puzzles.rectangles import rectangles as rectangles_solver
from puzzle_solver.puzzles.ripple_effect import ripple_effect as ripple_effect_solver
from puzzle_solver.puzzles.schurs_numbers import schurs_numbers as schurs_numbers_solver
from puzzle_solver.puzzles.shakashaka import shakashaka as shakashaka_solver
from puzzle_solver.puzzles.shingoki import shingoki as shingoki_solver
from puzzle_solver.puzzles.signpost import signpost as signpost_solver
from puzzle_solver.puzzles.singles import singles as singles_solver
from puzzle_solver.puzzles.slant import slant as slant_solver
from puzzle_solver.puzzles.slitherlink import slitherlink as slitherlink_solver
from puzzle_solver.puzzles.snail import snail as snail_solver
from puzzle_solver.puzzles.split_ends import split_ends as split_ends_solver
from puzzle_solver.puzzles.star_battle import star_battle as star_battle_solver
from puzzle_solver.puzzles.star_battle import star_battle_shapeless as star_battle_shapeless_solver
from puzzle_solver.puzzles.stitches import stitches as stitches_solver
from puzzle_solver.puzzles.sudoku import sudoku as sudoku_solver
from puzzle_solver.puzzles.suguru import suguru as suguru_solver
from puzzle_solver.puzzles.suko import suko as suko_solver
from puzzle_solver.puzzles.tapa import tapa as tapa_solver
from puzzle_solver.puzzles.tatami import tatami as tatami_solver
from puzzle_solver.puzzles.tents import tents as tents_solver
from puzzle_solver.puzzles.thermometers import thermometers as thermometers_solver
from puzzle_solver.puzzles.towers import towers as towers_solver
from puzzle_solver.puzzles.tracks import tracks as tracks_solver
from puzzle_solver.puzzles.trees_logic import trees_logic as trees_logic_solver
from puzzle_solver.puzzles.troix import troix as troix_solver
from puzzle_solver.puzzles.twiddle import twiddle as twiddle_solver
from puzzle_solver.puzzles.undead import undead as undead_solver
from puzzle_solver.puzzles.unequal import unequal as unequal_solver
from puzzle_solver.puzzles.unruly import unruly as unruly_solver
from puzzle_solver.puzzles.vectors import vectors as vectors_solver
from puzzle_solver.puzzles.vermicelli import vermicelli as vermicelli_solver
from puzzle_solver.puzzles.yajilin import yajilin as yajilin_solver
from puzzle_solver.puzzles.yin_yang import yin_yang as yin_yang_solver

from puzzle_solver.puzzles.inertia.parse_map.parse_map import main as inertia_image_parser

__all__ = [
    abc_view_solver,
    aquarium_solver,
    area_51_solver,
    battleships_solver,
    binairo_solver,
    binairo_plus_solver,
    black_box_solver,
    branches_solver,
    bridges_solver,
    chess_range_solver,
    chess_solo_solver,
    chess_melee_solver,
    circle_9_solver,
    connect_the_dots_solver,
    cow_and_cactus_solver,
    dominosa_solver,
    dumplings_solver,
    filling_solver,
    flood_it_solver,
    flip_solver,
    galaxies_solver,
    guess_solver,
    heyawake_solver,
    hidden_stars_solver,
    hidoku_solver,
    inertia_solver,
    kakurasu_solver,
    kakuro_solver,
    keen_solver,
    kropki_solver,
    krypto_kakuro_solver,
    light_up_solver,
    linesweeper_solver,
    link_a_pix_solver,
    magnets_solver,
    map_solver,
    mathema_grids_solver,
    minesweeper_solver,
    mosaic_solver,
    n_queens_solver,
    nonograms_solver,
    norinori_solver,
    number_path_solver,
    numbermaze_solver,
    nonograms_colored_solver,
    nurikabe_solver,
    palisade_solver,
    lits_solver,
    pearl_solver,
    pipes_solver,
    range_solver,
    rectangles_solver,
    ripple_effect_solver,
    schurs_numbers_solver,
    shakashaka_solver,
    shingoki_solver,
    signpost_solver,
    singles_solver,
    slant_solver,
    slitherlink_solver,
    snail_solver,
    split_ends_solver,
    star_battle_solver,
    star_battle_shapeless_solver,
    stitches_solver,
    sudoku_solver,
    suguru_solver,
    suko_solver,
    tapa_solver,
    tatami_solver,
    tents_solver,
    thermometers_solver,
    towers_solver,
    tracks_solver,
    trees_logic_solver,
    troix_solver,
    twiddle_solver,
    undead_solver,
    unequal_solver,
    unruly_solver,
    vectors_solver,
    vermicelli_solver,
    yajilin_solver,
    yin_yang_solver,
    inertia_image_parser,
]

__version__ = '1.1.5'
