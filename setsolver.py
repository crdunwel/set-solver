import itertools
import random
import json
import argparse


class Card(object):

	def __init__(self, idval, dimensions=None):
		self.id = idval
		self.dims = dimensions or {}

	def to_dict(self):
		return {'id': self.id, 'dims': self.dims}


class SetGame(object):

	class InvalidCardError(Exception):

		def __init__(self, e):
			msg = 'Invalid deck. Card "{0}" contains ' \
			'invalid data "{1}"'.format(e[0], e[1])
			super().__init__(msg)

	def __init__(self, dim_map=None, cards=None):
		self.cards = cards or []
		self.dim_map = dim_map or {}

	def addCard(self, card):
		self.cards.append(card)

	def make_deck(self):
		self.cards = []
		attrs = [v for k,v in self.dim_map.items()]
		i = 0
		for element in itertools.product(*attrs):
			dims = dict(zip(self.dim_map.keys(), element))
			self.addCard(Card(i, dims))
			i+=1

	def load_dims_from_file(self, filename='dims.json'):
		try:
			with open(filename, 'r') as f:
				self.dim_map = json.load(f)
		except FileNotFoundError:
			print('{0} not found.'.format(filename))
		except ValueError:
			print('{0} is not a valid json file.'.format(filename))

	def write_deck_to_file(self, filename="deck.json"):
		with open(filename, 'w+') as f:
			toWrite = {
				'dimensions': self.dim_map,
				'cards': [c.to_dict() for c in self.cards]
			}
			f.write(json.dumps(toWrite, indent=2))

	def valid_deck(self, deck):
		for c in deck['cards']:
			for d,v in c['dims'].items():
				if d not in deck['dimensions'].keys():
					return (c['id'], d)
				if v not in deck['dimensions'][d]:
					return (c['id'], v)
		return True

	def load_deck_from_file(self, filename="deck.json"):
		self.cards = []
		with open(filename, 'r') as f:
			deck_data = json.load(f)

			vd = self.valid_deck(deck_data)
			if vd != True:
				raise self.InvalidCardError(vd)

			self.dim_map = deck_data['dimensions']
			for c in deck_data['cards']:
				self.addCard(Card(c['id'], c['dims']))

	def valid_set(self, card_combo):
		for prop in self.dim_map.keys():
			set_length = len(set([c.dims[prop] for c in card_combo]))
			if set_length != 1 and set_length != len(card_combo):
				return False
		return True

	def finish_set(self, uset):
		sets = []
		for c in self.cards:
			if c.id in [u.id for u in uset]:
				continue
			elif self.valid_set(uset + (c,)):
				sets.append(c.id)
		return sets

	def possible_sets(self, choose=3):
	  sets = []
	  combos = itertools.combinations(self.cards, choose)
	  for combo in combos:
	  	if self.valid_set(combo):
	  		sets.append(tuple(c.id for c in combo))
	  return sets
	

def main():
	parser = argparse.ArgumentParser()
	parser.add_argument('--dims', type=str,
  	help='dimension json file with possible attributes and values')
	parser.add_argument('--deck', type=str,
    help='deck json file with cards to play')
	parser.add_argument('--choose', nargs='?', default=3, type=int,
    help='number of cards required for a set')

	args = parser.parse_args()

	sg = SetGame()
	if args.deck:
		sg.load_deck_from_file(args.deck)
	elif args.dims:
		sg.load_dims_from_file(args.dims)
		sg.make_deck()
	else:
		sg.load_dims_from_file('test_data/dims/simple_dim1.json')
		sg.make_deck()

	print(sg.possible_sets(args.choose))

if __name__ == "__main__":
    main()
