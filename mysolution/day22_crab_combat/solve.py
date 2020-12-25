from __future__ import annotations

import collections
import itertools
import os
import re
from typing import NamedTuple

import more_itertools

PLAYER_NAME_RE = re.compile(r'(.*):')


def main():
    this_dir = os.path.dirname(os.path.abspath(__file__))
    input_file = os.path.join(this_dir, 'input.txt')
    fst, snd = read_input_files(input_file)

    # Part 1
    winner = play_combat(fst, snd)
    p1_answer = sum(factor * card for factor, card in enumerate(reversed(winner.deck), start=1))
    print(p1_answer)

    # Part 2
    winner = play_recursive_combat(fst, snd)
    p2_answer = sum(factor * card for factor, card in enumerate(reversed(winner.deck), start=1))
    print(p2_answer)


class DeckInfo(NamedTuple):
    player_name: str
    deck: tuple[int, ...]

    @classmethod
    def from_raw(cls, raw: list[str]) -> DeckInfo:
        player_name = PLAYER_NAME_RE.fullmatch(raw[0].strip()).group(1)
        deck = tuple(int(line) for line in raw[1:])
        return DeckInfo(player_name, deck)


def play_combat(fst: DeckInfo, snd: DeckInfo) -> DeckInfo:
    """
    Returns the winning deck information of the winner
    at the end of the combat game.
    """
    fst_deck = collections.deque(fst.deck)
    snd_deck = collections.deque(snd.deck)

    while fst_deck and snd_deck:
        fst_card = fst_deck.popleft()
        snd_card = snd_deck.popleft()
        if fst_card > snd_card:
            fst_deck.extend([fst_card, snd_card])
        elif snd_card > fst_card:
            snd_deck.extend([snd_card, fst_card])
        else:
            raise RuntimeError

    if fst_deck:
        return DeckInfo(fst.player_name, tuple(fst_deck))
    elif snd_deck:
        return DeckInfo(snd.player_name, tuple(snd_deck))
    else:
        raise RuntimeError


def play_recursive_combat(fst: DeckInfo, snd: DeckInfo) -> DeckInfo:
    """
    Returns the winning deck information of the winner
    at the end of the recursive combat game.
    """
    fst_deck = collections.deque(fst.deck)
    snd_deck = collections.deque(snd.deck)
    recorded_round_configs = set()

    while fst_deck and snd_deck:

        # Checks if the round has already been repeated
        # Note that the rules is not clear of what should be considered
        # the final state of the deck of the winner
        round_config = tuple(itertools.chain(fst_deck, ':', snd_deck))
        if round_config in recorded_round_configs:
            return DeckInfo(fst.player_name, tuple(fst_deck) + tuple(snd_deck))
        recorded_round_configs.add(round_config)

        # Continue the game as usual
        fst_card = fst_deck.popleft()
        snd_card = snd_deck.popleft()

        if len(fst_deck) >= fst_card and len(snd_deck) >= snd_card:
            # Play recursive game to determine the winner
            subwinner = play_recursive_combat(
                DeckInfo(fst.player_name, tuple(fst_deck)[:fst_card]),
                DeckInfo(snd.player_name, tuple(snd_deck)[:snd_card]),
            )
            if subwinner.player_name == fst.player_name:
                fst_deck.extend([fst_card, snd_card])
            elif subwinner.player_name == snd.player_name:
                snd_deck.extend([snd_card, fst_card])
            else:
                raise RuntimeError

        # Otherwise, the usual combat rules apply
        elif fst_card > snd_card:
            fst_deck.extend([fst_card, snd_card])
        elif snd_card > fst_card:
            snd_deck.extend([snd_card, fst_card])
        else:
            raise RuntimeError

    if fst_deck:
        return DeckInfo(fst.player_name, tuple(fst_deck))
    elif snd_deck:
        return DeckInfo(snd.player_name, tuple(snd_deck))
    else:
        raise RuntimeError


def read_input_files(input_file: str) -> tuple[DeckInfo, DeckInfo]:
    """
    Extracts a pair of starting decks where each deck is a list of cards.
    """
    with open(input_file) as input_fobj:
        fst, snd = more_itertools.split_at(input_fobj, pred=lambda line: not line.strip())
        fst = DeckInfo.from_raw(fst)
        snd = DeckInfo.from_raw(snd)
        assert fst.player_name == 'Player 1' and snd.player_name == 'Player 2'
    return fst, snd


if __name__ == '__main__':
    main()
