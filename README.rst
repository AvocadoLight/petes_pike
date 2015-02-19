ThinkFun Pete's Pike Game Solver
================================

This program allows to solve any Pete's Pike game. Pete's Pike is a nice board
game created by Thinkfun.


Features
--------

#. Algorithm isn't restricted to a fixed board game size.
#. Logic that prunes branches that causes infinite loops.
#. Backtracking algorithm can found almost all or just one solution
   ("almost all" because of the above).
#. N number of goats are allowed.


Usage
-----

::

   $ ./petes_pike.py --help
   usage: petes_pike.py [-h] [-d] [--version] [-g GAME] [-f]

   Pete's Pike Game Solver

   optional arguments:
     -h, --help            show this help message and exit
     -d, --debug           Output debug information.
     --version             show program's version number and exit
     -g GAME, --game GAME  Path to game model.
     -f, --first           Show first solution only (instead of all of them)

For example:

::

   $ cat games/24.json
   {
       "goats": {
           "A": [0, 0],
           "B": [0, 4],
           "C": [4, 0],
           "E": [4, 4]
       },
       "pete": [1, 2],
       "target": [2, 2]
   }

   $ ./petes_pike.py -g games/24.json
   *** SOLUTIONS ***
   SOLUTION 1::
       B-D, E-L, C-URD, B-L, X-D
   SOLUTION 2::
       A-D, C-R, E-ULD, A-R, X-D


License
-------

::

   Copyright (C) 2015 Carlos Jenkins <carlos@jenkins.co.cr>

   Licensed under the Apache License, Version 2.0 (the "License");
   you may not use this file except in compliance with the License.
   You may obtain a copy of the License at

     http://www.apache.org/licenses/LICENSE-2.0

   Unless required by applicable law or agreed to in writing,
   software distributed under the License is distributed on an
   "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY
   KIND, either express or implied.  See the License for the
   specific language governing permissions and limitations
   under the License.
