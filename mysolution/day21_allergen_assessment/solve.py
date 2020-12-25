from __future__ import annotations

import collections
import functools
import operator
import os
import re
from dataclasses import dataclass
from typing import NewType

Ingredient = NewType('Ingredient', str)
Allergen = NewType('Allergen', str)

RECIPE_RE = re.compile(
    r'(?P<ingredients>\w+(?: \w+)*) '
    r'\(contains (?P<allergens>\w+(?:, \w+)*)\)',
)
SPLIT_RE = re.compile(r'\W+')


def main():
    this_dir = os.path.dirname(os.path.abspath(__file__))
    input_file = os.path.join(this_dir, 'input.txt')
    foods = read_input_files(input_file)

    # Part 1
    definitely_safe_ingredients = find_definitely_safe_ingredients(foods)
    p1_answer = sum(len(f.ingredients & definitely_safe_ingredients) for f in foods)
    print(p1_answer)

    # Part 2
    offending_ingredients = map_offending_ingredients(foods)
    canonical_dangerous_ingredient_list = [
        offending_ingredients[allergen]
        for allergen in sorted(offending_ingredients.keys())
    ]
    p2_answer = ','.join(canonical_dangerous_ingredient_list)
    print(p2_answer)


@dataclass
class Food:
    ingredients: set[Ingredient]
    allergens: set[Allergen]

    @classmethod
    def from_raw(cls, raw: str) -> Food:
        matchobj = RECIPE_RE.fullmatch(raw)
        ingredients = {Ingredient(i) for i in SPLIT_RE.split(matchobj['ingredients'])}
        allergens = {Allergen(a) for a in SPLIT_RE.split(matchobj['allergens'])}
        return Food(ingredients, allergens)


def find_definitely_safe_ingredients(foods: list[Food]) -> set[Ingredient]:
    all_ingredients = {i for f in foods for i in f.ingredients}
    all_allergens = {a for f in foods for a in f.allergens}

    exclusive_ingredient_sets = (find_ingredients_may_contain(a, foods) for a in all_allergens)
    maybe_unsafe_ingredients = functools.reduce(operator.or_, exclusive_ingredient_sets)

    return all_ingredients - maybe_unsafe_ingredients


def map_offending_ingredients(foods: list[Food]) -> dict[Allergen, Ingredient]:
    all_allergens = {a for f in foods for a in f.allergens}
    candidate_ingredients = {a: find_ingredients_may_contain(a, foods) for a in all_allergens}

    offending_ingredients = {}
    queue = collections.deque(
        allergens
        for allergens, candidates in candidate_ingredients.items()
        if len(candidates) == 1
    )

    while queue:
        allergens = queue.popleft()
        offender = candidate_ingredients[allergens].pop()
        offending_ingredients[allergens] = offender
        for other_allergen, other_candidates in candidate_ingredients.items():
            try:
                other_candidates.remove(offender)
            except KeyError:
                pass
            else:
                if len(other_candidates) == 1:
                    queue.append(other_allergen)

    return offending_ingredients


def find_ingredients_may_contain(allergen: Allergen, foods: list[Food]) -> set[Ingredient]:
    inclusive_ingredient_sets = (f.ingredients for f in foods if allergen in f.allergens)
    return functools.reduce(operator.and_, inclusive_ingredient_sets)


def read_input_files(input_file: str) -> list[Food]:
    """
    Extracts a list of food ingredients and known allergens.
    """
    with open(input_file) as input_fobj:
        foods = [Food.from_raw(line.strip()) for line in input_fobj]
    return foods


if __name__ == '__main__':
    main()
