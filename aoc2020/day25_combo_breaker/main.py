from __future__ import annotations

import itertools


def main():
    base = 7
    modulus = 20_201_227
    # card_pk, door_pk = 5764801, 17807724
    card_pk, door_pk = 16915772, 18447943

    # Part 1
    shared_key = break_diffie_hellman_key_exchange(base, modulus, card_pk, door_pk)
    print(shared_key)


def break_diffie_hellman_key_exchange(base: int, modulus: int, alice_pk: int, bob_pk: int) -> int:
    """
    Compute shared key which is the result of Diffie-Hellman Key Exchange Algorithm.
    Just a brute forcing way of solving discrete log problem.
    """
    current = 1
    for exp in itertools.count(start=1):
        current = (current * base) % modulus
        if current == alice_pk:
            return pow(bob_pk, exp, modulus)
        if current == bob_pk:
            return pow(alice_pk, exp, modulus)


if __name__ == '__main__':
    main()
