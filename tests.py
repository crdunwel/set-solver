from setsolver import SetGame, Card
import unittest
import os
import itertools
import timeit

class TestSetGame(unittest.TestCase):

	TEST_DATA_DIR = 'test_data/'

	def file_path(self, file):
		return os.path.join(self.TEST_DATA_DIR, file)

	def setUp(self):
		self.sg = SetGame()

	def test_invalid_deck(self):
		self.assertRaises(SetGame.InvalidCardError,
											self.sg.load_deck_from_file,
											self.file_path('decks/invalid_deck.json'))

	def test_valid_deck(self):
		self.sg.load_deck_from_file(self.file_path('decks/valid_deck.json'))

	def test_set_solver(self):
		self.sg.load_deck_from_file(self.file_path('decks/set_solver1.json'))
		sets = self.sg.possible_sets()
		assert(sets == [(0, 1, 2), (1, 2, 3)])

	def test_finish_set(self):
		self.sg.load_deck_from_file(self.file_path('decks/set_solver1.json'))
		finish = self.sg.finish_set((self.sg.cards[0], self.sg.cards[1]))
		assert(finish == [2])
		finish = self.sg.finish_set((self.sg.cards[1], self.sg.cards[2]))
		assert(finish == [0,3])
		finish = self.sg.finish_set((self.sg.cards[3], self.sg.cards[1]))
		assert(finish == [2])

	def test_all_possible_combos(self):
		"""
		Generates all possible cards for a standard set deck then uses the
		set solver to determine if the correct number of sets exist.

		There are 4 dimensions with 3 possible values so there are 3^4 = 81 cards
		in a deck. To find the number of possible sets we must first notice that
		for any two cards in a deck there is only one possible card that will
		create a valid set. Thus if two cards have the same value for an attribute
		then the third card must also have that value. If the two cards have
		different values for an attribute then the third card must have a
		different value from the other two. For a standard set deck as used in
		this test case with 81 cards and 4 dimensions with 3 possible values, this
		would yield (81*80)/3! = 1080 possible sets. Dividing by 3! is necessary
		because there are 3!=6 ways to order three items.

		tl;dr

		example 1:
		3^4 = 81 cards
		81 choose 3 = 85320 possible sets
		(81*80*1)/3! = 1080 valid sets

		example 2
		3^5 = 243 cards
		243 choose 3 = 2362041 possible sets
		(243*242*1)/3! = 9801 valid sets
		"""

		timer_string = "{0} seconds to solve for {1} cards with {2} dimensions " \
									 "containing {3} possible values"

		dim_maps = [
			('dims/simple_dim1.json', 3, 1080),
			('dims/simple_dim2.json', 3, 9801),
		]

		for dim in dim_maps:
			self.sg.load_dims_from_file(self.file_path(dim[0]))
			self.sg.make_deck()
			start_time = timeit.default_timer()
			assert(len( self.sg.possible_sets(dim[1])) == dim[2])
			elapsed = timeit.default_timer() - start_time
			print(timer_string.format(elapsed,
															 	len(self.sg.cards),
															 	len(self.sg.dim_map.keys()),
															 	len(list(self.sg.dim_map.values())[0])))

if __name__ == '__main__':
    unittest.main()
