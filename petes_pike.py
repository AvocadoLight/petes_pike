#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# Copyright (C) 2015 Carlos Jenkins <carlos@jenkins.co.cr>
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#   http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing,
# software distributed under the License is distributed on an
# "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY
# KIND, either express or implied.  See the License for the
# specific language governing permissions and limitations
# under the License.

"""
Pete's Pike Game Solver.
"""

from __future__ import unicode_literals
from __future__ import print_function
from __future__ import absolute_import

import logging

log = logging.getLogger(__name__)

__version__ = '0.1.0'


def direction(past, future):
    """
    Given two position determine the relative movement.
    """
    if past[0] < future[0]:
        return 'D'
    if past[0] > future[0]:
        return 'U'
    if past[1] < future[1]:
        return 'R'
    return 'L'


class Goat(object):

    def __init__(self, i, j, name):
        """
        I'm a Goat totem.
        """
        self.i = i
        self.j = j
        self.name = name

    def get_position(self):
        """
        Get current position of this totem.
        """
        return (self.i, self.j)

    def set_position(self, position):
        """
        Set current position of this totem.
        """
        self.i, self.j = position

    def can_move(self, totem, state):
        """
        Check if this totem can pull the other totem.
        """

        # Check basic movement
        basic = (self.i == totem.i and abs(self.j - totem.j) > 1) or \
            (self.j == totem.j and abs(self.i - totem.i) > 1)

        if not basic:
            return False

        # Check collision with other totems
        for other in state:
            on, oi, oj = other
            if oi == self.i:
                if min(self.j, totem.j) < oj < max(self.j, totem.j):
                    return False
            elif oj == self.j:
                if min(self.i, totem.i) < oi < max(self.i, totem.i):
                    return False

        # Movement can be done
        return True

    def move(self, totem):
        """
        Calculate the coordinates to pull a totem.
        """

        # Move horizontally
        if self.i == totem.i:
            column = 1 if self.j < totem.j else -1
            return (self.i, self.j + column)

        # Move vertically
        if self.j == totem.j:
            row = 1 if self.i < totem.i else -1
            return (self.i + row, self.j)

        raise Exception('BAD MOVE: {} tried to move {}'.format(self, totem))

    def __str__(self):
        return '{}->({}, {})'.format(self.name, self.i, self.j)


class Pete(Goat):
    def __init__(self, i, j):
        """
        I'm Pete, the mountaineer.
        """
        super(Pete, self).__init__(i, j, 'X')


class Game(object):

    def __init__(self, goats, pete, target):
        """
        Pete's Pike game solver.
        """

        self.solutions = []
        self.breadcrumbs = []
        self.states = set()

        self.goats = goats
        self.pete = pete
        self.totems = self.goats + [self.pete]
        self.target = target

    def get_state(self):
        """
        Get the current state of all totems in the board.
        """
        return tuple((t.name, t.i, t.j) for t in self.totems)

    def play(self, first=False):
        """
        Play current state of the board.
        """

        # Prune loop branches
        state = self.get_state()

        log.debug('Currently at state:')
        log.debug(state)
        log.debug('State history:')
        log.debug(self.states)

        if state in self.states:
            log.debug('Loop detected. Prunning...')
            return
        self.states.add(state)

        # Check if solution
        if self.pete.get_position() == self.target:
            self.solutions.append(list(self.breadcrumbs))
            log.debug('SOLUTION FOUND!')
            return

        # Tree traversal : Amplitude
        for puller in self.totems:
            for pulled in self.totems:

                # All or just one solution
                if first and self.solutions:
                    return

                # Ignore same
                if puller == pulled:
                    continue

                # Check if this branch is plausible
                if puller.can_move(pulled, state):

                    # Record movement
                    past = pulled.get_position()
                    future = puller.move(pulled)
                    self.breadcrumbs.append(
                        (pulled.name, direction(past, future))
                    )

                    # Tree traversal : Depth
                    log.debug('{} can move {} to {}. Playing branch...'.format(
                        puller, pulled, future
                    ))
                    pulled.set_position(future)
                    self.play()

                    # Backtrack
                    self.breadcrumbs.pop()
                    pulled.set_position(past)

        # Current state played, pop it
        self.states.remove(state)

    def get_solutions(self):
        """
        Get solutions of game format.
        """
        def fsolution(solution):
            totem = None
            moves = []
            formatted = []
            for part in solution:
                name, move = part

                if totem is None:
                    totem = name

                if name == totem:
                    moves.append(move)
                    continue

                formatted.append('{}-{}'.format(totem, ''.join(moves)))

                totem = name
                moves = [move]

            return ', '.join(formatted)
        return [
            fsolution(s) for s in sorted(self.solutions, key=lambda e: len(e))
        ]


class GameLoader(object):
    @classmethod
    def load_game(cls, game_file):
        """
        Load a game model.
        """
        from json import loads
        try:
            with open(game_file, 'r') as fd:
                data = loads(fd.read())

            # Load Goats
            goats = []
            for name, pos in data['goats'].items():
                goats.append(Goat(pos[0], pos[1], name))

            # Load Pete
            pete = Pete(*tuple(data['pete']))

            # Load target
            target = tuple(data['target'])

            return Game(goats, pete, target)

        except:
            from traceback import format_exc
            log.debug(format_exc())
            return None


def parse_args(argv=None):
    """
    Parse command line arguments.
    """
    from argparse import ArgumentParser

    parser = ArgumentParser(
        description='Pete\'s Pike Game Solver'
    )
    parser.add_argument(
        '-d', '--debug',
        help='Output debug information.',
        action='store_true'
    )
    parser.add_argument(
        '--version',
        action='version',
        version='Pete\'s Pike Game Solver v{}'.format(__version__)
    )
    parser.add_argument(
        '-g', '--game',
        default=None,
        help='Path to game model.'
    )
    parser.add_argument(
        '-f', '--first',
        help='Show first solution only (instead of all of them)',
        action='store_true'
    )

    args = parser.parse_args(argv)
    return args


if __name__ == '__main__':
    import sys
    from os.path import isfile

    args = parse_args()

    if args.debug:
        logging.basicConfig(level=logging.DEBUG)

    if args.game is None:
        print(
            'ERROR: Please provide a game model.',
            file=sys.stderr
        )
        sys.exit(1)
    if not isfile(args.game):
        print(
            'ERROR: Cannot find game model "{}".'.format(args.game),
            file=sys.stderr
        )
        sys.exit(1)

    g = GameLoader.load_game(args.game)
    if g is None:
        print(
            'ERROR: Unable to load game "{}".'.format(args.game),
            file=sys.stderr
        )
        sys.exit(1)

    g.play(first=args.first)
    print('*** SOLUTIONS ***')
    for i, s in enumerate(g.get_solutions()):
        print('SOLUTION {}::'.format(i + 1))
        print('    {}'.format(s))
