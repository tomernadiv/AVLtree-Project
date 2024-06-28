#username - tomernadiv
#id1      - 322594227 
#name1    - Tomer Nadiv
#id2      - 207731381
#name2    - Ron Ben Harosh  



"""
Virtual Leafs and Root objects Classes:
"""
class VirtualLeaf(object):
	"""
	A class representing a virtual node in an AVL tree.
	A virtual Leaf has no children, and a constant height, size, and balance factor.
	"""
	def __init__(self):
		self.parent = None
		self.height = -1
		self.size = 0
	
	def is_real_node(self):
		"""returns whether self is not a virtual node 

		@rtype: bool
		@returns: False.
		"""
		return False
	
	def balance_factor(self):
		return 0

class VirtualRoot(object):
	"""
	A class representing a virtual root node in an AVL tree.
	A virtual Root has no parent, and the rest of the tree is his right subtree.
	"""
	def __init__(self):
		self.key = float('-inf')
		self.left = VirtualLeaf()
		self.right = VirtualLeaf()
		self.right.parent = self
		self.left.parent = self
		self.size = 0
	
	def is_real_node(self):
		"""returns whether self is not a virtual node 

		@rtype: bool
		@returns: False.
		"""
		return False


"""
A class represnting a node in an AVL tree
"""
class AVLNode(object):
	"""
	
	@type key: int or None
	@param key: key of your node
	@type value: string
	@param value: data of your node
	"""
	def __init__(self, key, value):
		self.key = key
		self.value = value
		self.left = VirtualLeaf()
		self.right = VirtualLeaf()
		self.parent = VirtualLeaf()
		self.left.parent = self
		self.right.parent = self
		self.height = -1
		self.size = 0

	def balance_factor(self):
		"""
		Returns the balance factor of a node.

		@rtype: int
		@ returns: BF(node)
		"""
		return self.left.height - self.right.height
		
	def is_real_node(self):
		"""
		returns whether self is not a virtual node 

		@rtype: bool
		@returns: False if self is a virtual node, True otherwise.
		"""
		return True

	def is_criminal(self):
		"""
		Checks if an AVL node has a balance factor above 1 or below -1

		@ rtype: Bool
		@ returns: True if AVL criminal
		"""
		bf = self.balance_factor()
		return bf > 1 or bf < -1


"""
A class implementing an AVL tree.
"""
class AVLTree(object):

	"""
	Constructor, you are allowed to add more fields.  

	"""
	def __init__(self):
		self.virtual_root = VirtualRoot()


	def get_root(self):
		"""
		returns the root of the tree representing the dictionary

		@rtype: AVLNode
		@returns: the root, None if the dictionary is empty
		"""
		if not self.virtual_root.right.is_real_node():
			return None
		return self.virtual_root.right

	def search(self, key):
		"""
		searches for a node in the dictionary corresponding to the key.
		Iterative approach for binary search.

		@type key: int
		@param key: a key to be searched
		@rtype: AVLNode
		@returns: node corresponding to key
		"""

		node = self.virtual_root
		
		# if tree is not enpy:
		while node.is_real_node() or isinstance(node, VirtualRoot):

			# found key:
			if node.key == key:
				return node

			# left turn:
			if key < node.key:
				node = node.left

			# right turn:
			else:
				node = node.right

		return None  # the tree is empty, the root is a virtual leaf node.      

	def insert(self, key, val):
		"""
		inserts a new node into the dictionary with corresponding key and value

		@type key: int
		@pre: key currently does not appear in the dictionary
		@param key: key of item that is to be inserted to self
		@type val: string
		@param val: the value of the item
		@rtype: int
		@returns: the number of rebalancing operation due to AVL rebalancing
		"""
		# if the key appears in the tree:
		node = self.search(key)
		if node != None:
			node.value = val   # switch the value
			return 0
		
		# if we need to add the key:
		node = self.virtual_root

		while node.is_real_node() or isinstance(node, VirtualRoot):   # keep going if it's a virtual root or a real node
			if key < node.key:      # left turn
				node = node.left
			else:                   # right turn
				node = node.right

		# insert the new node and fix pointers:
		new_node = AVLNode(key, val)
		parent = node.parent
		if parent.left == node:
			parent.left = new_node
		else:
			parent.right = new_node
		new_node.parent = parent

		# update heights:
		rebalances = self.update_height(new_node)

        # Rebalance the tree if necessary and update heights
		node = new_node
		while node.is_real_node():
			if node.is_criminal():
				rebalances += self.balance(node)       # perform rotations
				self.update_height(new_node)           # update heights
				return rebalances
			
			node = node.parent                         # continue
		
		return rebalances
	
	def delete(self, node):
		"""
		deletes node from the dictionary

		@type node: AVLNode
		@pre: node is a real pointer to a node in self
		@rtype: int
		@returns: the number of rebalancing operation due to AVL rebalancing
		"""
		return -1

	def avl_to_array(self):
		"""
		returns an array representing dictionary 

		@rtype: list
		@returns: a sorted list according to key of touples (key, value) representing the data structure
		"""
		return None

	def size(self):
		"""
		returns the number of items in dictionary 

		@rtype: int
		@returns: the number of items in dictionary 
		"""
		return -1	

	def rank(self, node):
		"""
		compute the rank of node in the dictionary

		@type node: AVLNode
		@pre: node is in self
		@param node: a node in the dictionary to compute the rank for
		@rtype: int
		@returns: the rank of node in self
		"""
		return -1

	def select(self, i):
		"""
		finds the i'th smallest item (according to keys) in the dictionary

		@type i: int
		@pre: 1 <= i <= self.size()
		@param i: the rank to be selected in self
		@rtype: AVLNode
		@returns: the node of rank i in self
		"""
		return None

	def max_range(self, a, b):
		"""
		finds the node with the largest value in a specified range of keys

		@type a: int
		@param a: the lower end of the range
		@type b: int
		@param b: the upper end of the range
		@pre: a<b
		@rtype: AVLNode
		@returns: the node with maximal (lexicographically) value having a<=key<=b, or None if no such keys exist
		"""
		return None



######### HELPER FUNCTIONS ##########

	def rotate_left(self, node):
		"""
		Performs a left rotation.

		@node type: AVLnode.
		@param node: criminal node with a BF in {-2,2} or the left son of a criminal node.
		@rtype: None.
		"""

		# set meaningful names:
		A = node
		B = node.right

		### Poiners ###

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

		### Height ###
		A.height = max(A.left.height, A.right.height) + 1
		B.height = max(B.left.height, B.right.height) + 1

	def rotate_right(self, node):
		"""
		Performs a right rotation.

		@node type: AVLnode.
		@param node: criminal node with a BF in {-2,2} or the right son of a criminal node.
		@rype: None.
		"""
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

		### Height ###
		A.height = max(A.left.height, A.right.height) + 1
		B.height = max(B.left.height, B.right.height) + 1

	def rotate_left_right(self, node):
		"""
		Performs a left than right rotation.

		@node type: AVLnode.
		@param node: criminal node with a BF in {-2,2}.
		@rype: None.
		"""
		
		# perform left rotation on node.left:
		self.rotate_left(node.left)
		# perform right rotation on node:
		self.rotate_right(node)

	def rotate_right_left(self, node):
		"""
		Performs a right than left rotation.

		@node type: AVLnode.
		@param node: criminal node with a BF in {-2,2}.
		@rype: None.
		"""
		# perform right rotation on node.right:
		self.rotate_right(node.right)
		# perform left rotation on node:
		self.rotate_left(node)

	def balance(self, node):
		"""
		Fixes an AVL tree after insertion of deletion.
		Returns the number of rotations applied {1,2}

		@type node: AVLNode.
		@param node:criminal node with a BF in {-2,2}.
		@rtype: int.
		@returns: number of rotations performed {0,1,2}.
		"""
		counter = 0   # Assume no rotation occured

		if node.balance_factor() == -2:
			if node.right.balance_factor() == -1 or node.right.balance_factor() == 0:
				self.rotate_left(node)                # left rotation
				counter = 1
			elif node.right.balance_factor() == 1:
				self.rotate_right_left(node)          # right left rotation
				counter = 2

		if node.balance_factor() == 2:
			if node.left.balance_factor() == 1 or node.left.balance_factor() == 0:
				self.rotate_right(node)               # right rotation
				counter = 1
			if node.left.balance_factor() == -1:
				self.rotate_left_right(node)          # left right rotation
				counter = 2

		return counter

	def update_height(self, node):
		"""
		Travels up the path of the new inputted node, updates the height iteratively.
		
		@type node: AVLnode.
		@param node: the new inputted node.
		@rtype: int.
		@returns: the number of height changes occured.
		"""
		cnt = 0
		while node.is_real_node():
			old_height = node.height
			new_height = max(node.left.height, node.right.height) + 1 # Update the height and continue the climb
			if old_height != new_height:
				node.height = new_height
				cnt += 1                  # count the number of height changes.
			node = node.parent
		return cnt



if __name__ == '__main__':
    AVL = AVLTree()
    AVL.insert(10, 'a')
    AVL.insert(5, 'b')
    AVL.insert(1, 'c')
