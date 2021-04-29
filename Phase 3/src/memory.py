import math

class Memory:
	def __init__(self, cache_size, block_size, associativity, ways):
		self.cache_size = cache_size
		self.block_size = block_size
		self.associativity = associativity
		self.ways = ways
		self.sets = 0
		self.number_of_index_bits = 0
		self.number_of_block_offset_bits = int(math.log(block_size, 2))
		#
		self.count_accesses = 0
		self.count_hits = 0
		self.count_total_misses = 0
		self.count_cold_misses = 0
		self.count_capacity_misses = 0
		self.count_conflict_misses = 0
		#
		self.set()

	def set(self):
		if self.associativity == 0:
			self.sets = 1
		elif self.associativity == 1:
			self.sets = self.cache_size // self.block_size
			self.number_of_index_bits = int(math.log(self.sets, 2))
		else:
			self.sets = self.cache_size // self.block_size
			self.sets = self.sets // self.ways
			self.number_of_index_bits = int(math.log(self.sets, 2))

		self.cache = [dict() for i in range(self.sets)] # {tag: (block, recency)}

	def get_index(self, address):
		address = bin(int(address[2:], 16))[2:]
		address = (32 - len(address)) * '0' + address
		if self.number_of_index_bits == 0:
			return 0
		else:
			return int(address[-(self.number_of_block_offset_bits+self.number_of_index_bits):-self.number_of_block_offset_bits], 2)

	def get_tag(self, address):
		address = bin(int(address[2:], 16))[2:]
		address = (32 - len(address)) * '0' + address
		return int(address[:-(self.number_of_block_offset_bits+self.number_of_index_bits)], 2)

	def get_block_offset(self, address):
		address = bin(int(address[2:], 16))[2:]
		address = (32 - len(address)) * '0' + address
		return int(address[-(self.number_of_block_offset_bits):], 2)

	def replace_block(self, index, cache_tag, tag):
		pass

	def update_recency(self, index, tag):
		curr_recency = self.cache[index][tag][1]
		self.cache[index][tag][1] = self.ways - 1
		for cache_tag in self.cache[index].keys():
			if self.cache[index][tag][1] > curr_recency:
				self.cache[index][tag][1] -= 1

	def read(self, address, MEM):
		index = self.get_index(address)
		tag = self.get_tag(address)
		block_offset = self.get_block_offset(address)
		if tag not in self.cache[index].keys():
			for cache_tag in self.cache[index].keys():
				if self.cache[index][cache_tag][1] == 0:
					self.replace_block(index, cache_tag, tag)
					break

		block = self.cache[index][tag]
		self.update_recency(index, tag)
		return block[block_offset + 3] + block[block_offset + 2] + block[block_offset + 1] + block[block_offset]

	# Write Through and No-write Allocate
	# Data at lower address first
	def write(self, address, data, MEM):
		index = self.get_index(address)
		tag = self.get_tag(address)
		if tag in self.cache[index].keys():
			offset = self.get_block_offset(address)
			self.cache[index][tag][0] = self.cache[index][tag][0][:4*offset] + data[2:] + self.cache[index][tag][0][4*offset+4:]

		idx = int(address[2:], 16)
		MEM[idx] =  data[8:10]
		MEM[idx + 1] = data[6:8]
		MEM[idx + 2] = data[4:6]
		MEM[idx + 3] = data[2:4]

# issue if data is not a word
