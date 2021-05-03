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
		address = hex(address)
		address = bin(int(address[2:], 16))[2:]
		address = (32 - len(address)) * '0' + address
		if self.number_of_index_bits == 0:
			return 0
		else:
			return int(address[-(self.number_of_block_offset_bits+self.number_of_index_bits):-self.number_of_block_offset_bits], 2)

	def get_tag(self, address):
		address = hex(address)
		address = bin(int(address[2:], 16))[2:]
		address = (32 - len(address)) * '0' + address
		return int(address[:-(self.number_of_block_offset_bits+self.number_of_index_bits)], 2)

	def get_block_offset(self, address):
		address = hex(address)
		address = bin(int(address[2:], 16))[2:]
		address = (32 - len(address)) * '0' + address
		return int(address[-(self.number_of_block_offset_bits):], 2)

	def replace_block(self, index, cache_tag, address, MEM):
		self.cache[index].pop(cache_tag)
		tag = self.get_tag(address)
		self.cache[index][tag] = ['', self.ways - 1]
		for i in range(self.block_size):
			self.cache[index][tag][0] += MEM[address + i]

	def update_recency(self, index, tag):
		self.cache[index][tag][1] = self.ways
		for cache_tag in self.cache[index].keys():
			if self.cache[index][cache_tag][1] != 0:
				self.cache[index][cache_tag][1] -= 1

	def add_block(self, address, MEM):
		index = self.get_index(address)
		tag = self.get_tag(address)
		self.cache[index][tag] = ['', self.ways - 1]
		for i in range(self.block_size):
			self.cache[index][tag][0] += MEM[address + i]

	def read(self, address, MEM):
		# print("read")
		index = self.get_index(address)
		tag = self.get_tag(address)
		block_offset = self.get_block_offset(address)
		if tag not in self.cache[index].keys():
			if len(self.cache[index]) != self.ways:
				self.add_block(address, MEM)
			else:
				for cache_tag in self.cache[index].keys():
					if self.cache[index][cache_tag][1] == 0:
						self.replace_block(index, cache_tag, address, MEM)
						break

		block = self.cache[index][tag][0]
		self.update_recency(index, tag)
		return block[block_offset:block_offset + 8]

	# Write Through and No-write Allocate
	# Data word at lower address first
	def write(self, address, data, MEM, type):
		# print("write")
		index = self.get_index(address)
		tag = self.get_tag(address)
		if tag in self.cache[index].keys():
			offset = self.get_block_offset(address)
			if type == 3:
				self.cache[index][tag][0] = self.cache[index][tag][0][:offset] + data[8:10] + data[6:8] + data[4:6] + data[2:4] + self.cache[index][tag][0][offset+8:]
			elif type == 1:
				self.cache[index][tag][0] = self.cache[index][tag][0][:offset] + data[8:10] + data[6:8] + self.cache[index][tag][0][offset+4:]
			else:
				self.cache[index][tag][0] = self.cache[index][tag][0][:offset] + data[8:10] + self.cache[index][tag][0][offset+2:]

		if type >= 3:
			MEM[address + 3] = data[2:4]
			MEM[address + 2] = data[4:6]
		if type >= 1:
			MEM[address + 1] = data[6:8]
		if type >= 0:
			MEM[address] = data[8:10]
