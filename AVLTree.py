# Description: This file contains the implementation of an AVL tree data structure.
# Tomer Nadiv & Ron Ben Harosh 2024

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
		self.right = None
		self.left = None
	
	def __repr__(self):
		return '-Virtual Leaf-'
	
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
		self.parent = None

	def __repr__(self):
		return '-Virtual Root-'
	
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
		self.height = 0
		self.size = 1

	def __repr__(self):
		return '-AVL NODE-\n key: %s\n value: %s' % (self.key, self.value)

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

	def __init__(self):
		self.virtual_root = VirtualRoot()
		self.max_node = self.virtual_root  # initialize the maximum node to be the virtual root

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
		Time Complexity: O(log(n)).

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
		Time Complexity: O(log(n)).

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


        # Travel up, for each node change the height and check if it's criminal.
		# Count height change as +1, rotations as +1 or +2.
		# Stop when reaching the virtual root, as size maintenance is done there.

		rebalances = 0 							   # initialize counter
		curr_node = new_node.parent 			   # start from the new node
		while curr_node.is_real_node():            # continue until the virtual root is reached (or encounter break command)
			next_node = curr_node.parent           # save the next node before changing it
			# Update height:
			old_height = curr_node.height          # save old height
			new_height = max(curr_node.left.height, curr_node.right.height) + 1  # update height
			curr_node.height = new_height		   # update height

			# Decide the next move:
			if curr_node.is_criminal():            # [OBS 1]
				rebalances += self.balance(curr_node)
			else: 
				curr_node.size += 1                # update size
				if new_height != old_height:       # [OBS 3]
					rebalances += 1				   # count the number of height changes
			curr_node = next_node		           # continue to the next node		
		
		# Update Virtual Root Size & Height:
		self.virtual_root.size += 1

		# Update the maximum node if needed:
		if new_node.key > self.max_node.key:
			self.max_node = new_node

		return rebalances
	
	def delete(self, node):
		"""
		deletes node from the dictionary
		Time Complexity: O(log(n)).

		@type node: AVLNode
		@pre: node is a real pointer to a node in self
		@rtype: int
		@returns: the number of rebalancing operation due to AVL rebalancing
		"""
		# Case 1: node has less than 2 children:
		if not node.left.is_real_node() or not node.right.is_real_node():
			# find the child node
			if not node.left.is_real_node():
				child = node.right
			else:
				child = node.left
			
			# handle pointers:
			if node == node.parent.left:    # node is a left child
				node.parent.left = child
			else:                           # node is a right child
				node.parent.right = child
			child.parent = node.parent      # upward pointer

			start_node = child.parent       # just for interpertable naming

		# Case 2: node has exactly 2 children:
		else:
			successor = self.successor(node)
			node.key, node.value = successor.key, successor.value  # replace node inplace
			return self.delete(successor)                          # delete successor -> will go to Case 1
		

        # Travel up, for each node change the height and check if it's criminal.
		# Count height change as +1, rotations as +1 or +2.
		# If the hight didn't change, and current node is not a criminal - terminate.

		rebalances = 0 							   # initialize counter
		curr_node = start_node 			          
		while curr_node.is_real_node():			   # continue until the virtual root is reached        
			next_node = curr_node.parent           # save the next node before changing it
			
			# Update size:
			curr_node.size -= 1                   
			
			# Update height:
			old_height = curr_node.height          # save old height
			new_height = max(curr_node.left.height, curr_node.right.height) + 1  # update height
			curr_node.height = new_height		   # update height

			# Decide the next move:
			if curr_node.is_criminal():            # [Step 3.4 in the lecture notes]
				rebalances += self.balance(curr_node)
			else: 
				if new_height != old_height:       # [Step 3.3 in the lecture notes]
					rebalances += 1				   # count the number of height changes
			curr_node = next_node                  # continue		

		# Update Virtual Root Size & Height:
		self.virtual_root.size -= 1
		
		# Update the maximum node if needed:
		if node == self.max_node:
			new_max = self.maximum()
			self.max_node = new_max if new_max != None else self.virtual_root
		
		# Return the number of rebalances:
		return rebalances	

	def avl_to_array(self):
		"""
		Returns an array representing the dictionary.
		Time Complexity: O(n).

		@rtype: list
		@returns: a sorted list according to key of tuples (key, value) representing the data structure
		"""
		def avl_to_array_rec(node, array):
			"""
			Recurssive in-order walk.

			@type node: AVLnode.
			@param node: real root of the tree.
			@type array: python list.
			@param array: current version of dictionary as a sorted array.
			@rtype: python list.
			@returns: sorted dictionary ADT as a sorted array.
			"""
			if isinstance(node, VirtualLeaf):
				return
			avl_to_array_rec(node.left, array)
			array.append((node.key, node.value))
			avl_to_array_rec(node.right, array)

		array = []
		avl_to_array_rec(self.virtual_root.right, array)
		return array
		 
	def size(self):
		"""
		returns the number of items in dictionary 

		@rtype: int
		@returns: the number of items in dictionary 
		"""
		return self.virtual_root.size

	def rank(self, node):
		"""
		compute the rank of node in the dictionary
		Time Complexity: O(log(n)).

		@type node: AVLNode
		@pre: node is in self
		@param node: a node in the dictionary to compute the rank for
		@rtype: int
		@returns: the rank of node in self
		"""
		cnt = node.left.size                      # initialize counter with the number of nodes in the left subtree
		while node.is_real_node():                # climb up until the virtual root is reached
			if node == node.parent.right:         # if node is a right child
				cnt += node.parent.left.size + 1  # add the size of the left subtree and the parent
			node = node.parent                    # climb up
		return cnt

	def select(self, i):
		"""
		finds the i'th smallest item (according to keys) in the dictionary
		Time Complexity: O(log(n)).

		@type i: int
		@pre: 1 <= i <= self.size()
		@param i: the rank to be selected in self
		@rtype: AVLNode
		@returns: the node of rank i in self
		"""
		node = self.get_root() 					# start from the root
		while node.left.size + 1 != i: 			# continue until the rank of the root is i
			if i < node.left.size + 1: 			# if the i'th smallest node is in the left subtree
				node = node.left
			else: 								# if the i'th smallest node is in the right subtree
				i -= node.left.size + 1 		# update i
				node = node.right 				# continue to the right subtree
		return node 							# the while loop will end as 1 <= i <= self.size()

	def max_range(self, a, b):
		"""
		finds the node with the largest value in a specified range of keys
		Time Complexity: O(n).

		@type a: int
		@param a: the lower end of the range
		@type b: int
		@param b: the upper end of the range
		@pre: a<b
		@rtype: AVLNode
		@returns: the node with maximal (lexicographically) value having a<=key<=b, or None if no such keys exist
		"""
		# find the node with the smallest key greater than or equal to a
		node = self.get_root()
		while node.is_real_node() and not node.key == a:
			if node.key < a:
				node = node.right
			else:
				node = node.left

		# if node is a virtual node:
		if not node.is_real_node():
			# check if node is a right son:
			if node.parent.right == node:
				node = self.successor(node.parent)
			else:
				node = node.parent
		
		# perform a maximum of (b-a) successor calls:
		max_val_node = node
		while node.is_real_node() and node.key <= b:
			if node.value >= max_val_node.value:
				max_val_node = node
			node = self.successor(node)
		return max_val_node

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

		## Size ##
		A.size = A.left.size + A.right.size + 1
		B.size = B.left.size + B.right.size + 1

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

		## Size ##
		A.size = A.left.size + A.right.size + 1
		B.size = B.left.size + B.right.size + 1

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
		if node.balance_factor() == -2:
			if node.right.balance_factor() == -1 or node.right.balance_factor() == 0:
				self.rotate_left(node)                # left rotation
				return 1                              # Number of rotations performed is 1
			elif node.right.balance_factor() == 1:
				self.rotate_right_left(node)          # right left rotation
				return 2                              # Number of rotations performed is 2

		if node.balance_factor() == 2:
			if node.left.balance_factor() == 1 or node.left.balance_factor() == 0:
				self.rotate_right(node)               # right rotation
				return 1                              # Number of rotations performed is 1
			if node.left.balance_factor() == -1:
				self.rotate_left_right(node)          # left right rotation
				return 2                              # Number of rotations performed is 2
		return 0

	def successor(self, node):
		"""
		Return the successor node of a certain node.

		@type node: AVLnode.
		@param node: current node.
		@rtype: AVLnode.
		@returns: successor of the current node.
		"""
		# Case 0: no successor (node is maximum)
		if self.maximum() == node:
			return None
		
		# Case 1: node as a right son.
		if node.right.is_real_node():
			return self.minimum(node.right)
		
		# Case 2: node does not have a right son.
		while node.parent.right == node:  # climb up until you are no longer a right son.
			node = node.parent
		return node.parent

	def minimum(self, node=None):
		"""
		Return the minimum of a subtree. 
		If node is None -> Return the minumum of the whole tree.
		Time Complexity: O(log(n)).

		@type node: AVLnode or None.
		@param node: root of a subtree. if None, node -> real root.
		@rtype: AVLnode.
		@return: minumum node in the tree.
		"""
		# no subtree root specified:
		if node==None:
			node = self.virtual_root.right
		
		# tree is empty:
		if not node.is_real_node():
			return None
		
		# find minumum:
		while node.is_real_node(): # iterate until a virtual leaf node is encountered
			node = node.left
		return node.parent         # return the virtual leaf node parent

	def maximum(self, node=None):
		"""
		Return the maximum of a subtree. 
		If node is None -> Return the maximum of the whole tree.
		Time Complexity: O(log(n)).

		@type node: AVLnode or None.
		@param node: root of a subtree. if None, node -> real root.
		@rtype: AVLnode.
		@return: maximum node in the tree.
		"""
		# no subtree root specified:
		if node==None:
			node = self.virtual_root.right
		
		# tree is empty:
		if not node.is_real_node():
			return None
		
		# find minumum:
		while node.is_real_node(): # iterate until a virtual leaf node is encountered
			node = node.right
		return node.parent         # return the virtual leaf node parent

#### Finger-tree modification functions #####

	def insert_from_max(self, key, val):
		"""
		Inserst a new node into the dictionary with corresponding key and value, using the finger-tree algorithm.
		If needed, the maximum node is updated.
		Time Complexity: O(log(n)).

		@type key: int.
		@pre: key currently does not appear in the dictionary.
		@param key: key of item that is to be inserted to self.
		@type val: string.
		@param val: the value of the item.

		@rtype: tuple of integers.
		@returns: a tuple with the sort_cost and substitutions --> (sort_cost, substitutions)
				  sort_cost: the number of rebalancing operations due to AVL rebalancing + number of nodes visited when searching for the insertion point.
				  substitutions: the number of pairs i>j where array[i] < array[j].
		"""
		# if the tree is empty:
		if not self.virtual_root.right.is_real_node():
			return self.insert(key, val), 0
		
		# Start from the maximum node
		# iterate until we reach the right son of the first node that is smaller than the key
		node = self.max_node
		nodes_visited = 0
		while node.parent.key > key:
			nodes_visited += 1
			node = node.parent
		
		# initialize counter for the new node rank:
		new_node_rank = self.size() + 1

		# find the parent of the new node, update the new node's rank
		while node.is_real_node():
			if key < node.key:
				new_node_rank -= (node.right.size + 1)
				node = node.left
			else:
				node = node.right
			nodes_visited += 1
		parent = node.parent        # new parent found
								    # nodes_visited is ready to be returned

		# insert the new node and fix pointers:
		new_node = AVLNode(key, val)
		new_node.parent = parent
		if parent.left == node:
			parent.left = new_node
		else:
			parent.right = new_node

        # Travel up, for each node change the height and check if it's criminal.
		# Count height change as +1, rotations as +1 or +2.
		# Stop when reaching the virtual root, as size maintenance is done there.

		rebalances = 0 							   # initialize counter
		curr_node = new_node.parent 			   # start from the new node
		while curr_node.is_real_node():            # continue until the virtual root is reached (or encounter break command)
			next_node = curr_node.parent           # save the next node before changing it
			# Update height:
			old_height = curr_node.height          # save old height
			new_height = max(curr_node.left.height, curr_node.right.height) + 1  # update height
			curr_node.height = new_height		   # update height

			# Decide the next move:
			if curr_node.is_criminal():            # [OBS 1]
				rebalances += self.balance(curr_node)
			else: 
				curr_node.size += 1                # update size
				if new_height != old_height:       # [OBS 3]
					rebalances += 1				   # count the number of height changes
			curr_node = next_node		           # continue to the next node		
		
		# Update Virtual Root Size & Height:
		self.virtual_root.size += 1

		# Update the maximum node if needed:
		if new_node.key > self.max_node.key:
			self.max_node = new_node

		sort_cost = rebalances + nodes_visited
		substitutions = self.size() - new_node_rank
		return sort_cost, substitutions