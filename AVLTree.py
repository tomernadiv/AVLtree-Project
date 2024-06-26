#username - tomernadiv
#id1      - 322594227 
#name1    - Tomer Nadiv
#id2      - 207731381
#name2    - Ron Ben Harosh  

"""
A class representing a virtual node in an AVL tree
"""
class VirtualNode(object):
	# A virtual Node has only a parent field.
	def __init__(self):
		self.parent = None
	
	"""returns whether self is not a virtual node 

	@rtype: bool
	@returns: False.
	"""
	def is_real_node(self):
		return False
		
"""
A class represnting a node in an AVL tree
"""
class AVLNode(object):
	"""Constructor, you are allowed to add more fields. 
	
	@type key: int or None
	@param key: key of your node
	@type value: string
	@param value: data of your node
	"""
	def __init__(self, key, value):
		self.key = key
		self.value = value
		self.left = VirtualNode()
		self.right = VirtualNode()
		self.parent = None
		self.height = -1
		self.size = 0

	def balance_factor(self):
		return self.left.height - self.right.height
		

	"""returns whether self is not a virtual node 

	@rtype: bool
	@returns: False if self is a virtual node, True otherwise.
	"""
	def is_real_node(self):
		return True



"""
A class implementing an AVL tree.
"""
class AVLTree(object):

	"""
	Constructor, you are allowed to add more fields.  

	"""
	def __init__(self):
		self.root = None


	"""searches for a node in the dictionary corresponding to the key

	@type key: int
	@param key: a key to be searched
	@rtype: AVLNode
	@returns: node corresponding to key
	"""
	def search(self, key):
		return None


	"""inserts a new node into the dictionary with corresponding key and value

	@type key: int
	@pre: key currently does not appear in the dictionary
	@param key: key of item that is to be inserted to self
	@type val: string
	@param val: the value of the item
	@rtype: int
	@returns: the number of rebalancing operation due to AVL rebalancing
	"""
	def insert(self, key, val):
		return -1


	"""deletes node from the dictionary

	@type node: AVLNode
	@pre: node is a real pointer to a node in self
	@rtype: int
	@returns: the number of rebalancing operation due to AVL rebalancing
	"""
	def delete(self, node):
		return -1


	"""returns an array representing dictionary 

	@rtype: list
	@returns: a sorted list according to key of touples (key, value) representing the data structure
	"""
	def avl_to_array(self):
		return None


	"""returns the number of items in dictionary 

	@rtype: int
	@returns: the number of items in dictionary 
	"""
	def size(self):
		return -1	


	"""compute the rank of node in the dictionary

	@type node: AVLNode
	@pre: node is in self
	@param node: a node in the dictionary to compute the rank for
	@rtype: int
	@returns: the rank of node in self
	"""
	def rank(self, node):
		return -1


	"""finds the i'th smallest item (according to keys) in the dictionary

	@type i: int
	@pre: 1 <= i <= self.size()
	@param i: the rank to be selected in self
	@rtype: AVLNode
	@returns: the node of rank i in self
	"""
	def select(self, i):
		return None


	"""finds the node with the largest value in a specified range of keys

	@type a: int
	@param a: the lower end of the range
	@type b: int
	@param b: the upper end of the range
	@pre: a<b
	@rtype: AVLNode
	@returns: the node with maximal (lexicographically) value having a<=key<=b, or None if no such keys exist
	"""
	def max_range(self, a, b):
		return None


	"""returns the root of the tree representing the dictionary

	@rtype: AVLNode
	@returns: the root, None if the dictionary is empty
	"""
	def get_root(self):
		return None



######### CUSTOM OPERATIONS ##########

	"""
  Performs a left roatation.

	@rtype: AVLNode.
	@returns: None.
	"""
	def rotate_left(self, node):
		# set meaningful names:
		A = node
		B = node.right

		# apply poninters for A.parent <-> B:
		if A.parent.left == A:
			A.parent.left = B
		else:
			A.parent.right = B
		B.parent = A.parent

		# apply pointers for A <-> B.left:
		A.right = B.left
		A.right.parent = A

		# apply pointers for A <-> B:
		B.left = A
		A.parent = B

	"""
  Performs a right roatation.

	@rtype: AVLNode.
	@returns: None.
	"""
	def rotate_right(self, node):
		# set meaningful names:
		A = node
		B = node.left

		# apply pointers for A.parent <-> B:
		if A.parent.left == A:
			A.parent.left = B
		else:
			A.parent.right = B
		B.parent = A.parent

		# apply pointers for A <-> B.right:
		A.left = B.right
		A.left.parent = A

		# apply pointers for A <-> B:
		B.right = A
		A.parent = B

	def rotate_left_right(self, node):
		# perform left rotation on node.left:
		self.rotate_left(self, node.left)
		# perform right rotation on node:
		self.rotate_right(self, node)

	def rotate_right_left(self, node):
		# perform right rotation on node.right:
		self.rotate_right(self, node.right)
		# perform left rotation on node:
		self.rotate_left(self, node)



	"""
  Fixes an AVL tree after insertion of deletion.

	@rtype: AVLNode.
  @input: criminal node with a BF in {-2,2}.
	@returns: number of rotations performed {1,2}.
	"""
	def balance(self, node):
		# dont forget to modify the counter, return counter!
		
		### Check which type of rotation to do ###
		if node.balance_factor() == -2:
			if node.right.balance_factor() == -1 or node.right.balance_factor() == 0:
				self.rotate_left(self, node)                # left rotation
				counter = 1
			elif node.right.balance_factor() == 1:
				self.rotate_right_left(self, node)          # right left rotation
				counter = 2

		if node.balance_factor() == 2:
			if node.left.balance_factor() == 1 or node.left.balance_factor() == 0:
				self.rotate_right(self, node)               # right rotation
				counter = 1
			if node.left.balance_factor() == -1:
				self.rotate_left_right(self, node)          # left right rotation
				counter = 2

		return counter
