# Set Solver

Solves generalized game of set by providing all valid card combinations that create a set based on given input. There is no bound on the number of dimensions, possible values, or number of cards that make a set.

## Getting Started

Tested in **Python 3.7.0**. If you use pyenv then the included .python-version file should choose the correct version for you.

No external packages are used.

## Running

Run `python setsolver.py -h` for a summary of inputs. At minimum you must provide a `--dims` or `--deck` argument which are file paths to valid JSON representing dimensions or a deck. See examples in test_data directory for examples of how to format these files. 

If a dimensional file is provided then a deck will be generated for all possible combinations of the dimensions.

If no arguments are provided then the solver will load dimensions for a standard set deck and create 81 cards containing all possible combinations.

## Complexity

Values of set size, dimensions, and values much beyond the standard game may take a long time to calculate because the set solver must check `(n choose k)` possible sets. This expands to `n! / (k!(n-k)!)` or a kth-degree polynomial thus the calculation is `O(n^k)` where n is the size of the deck and k is the set size.

For example, a standard game of set contains 81 cards with 4 dimensions that have 3 possible values. This leads to `(81 choose 3) = 85320` possible sets and `(81*80*1)/3! = 1080` valid sets.

## Improvements

The algorithm for validating a possible set can be parallelized for speed up by distributing parts of the possible possible set list to different machines or cores and combining for final results.

## Running the tests

You can run the test suite by running `python tests.py`. These make take a dozen seconds to run. It will showcase the calculation time difference for different dimensions, values, and set size.

## License

This project is licensed under the [MIT License](https://opensource.org/licenses/MIT).