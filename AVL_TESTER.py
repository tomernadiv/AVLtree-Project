"""
mini tester by Yaron and Eviatar 
(parent of the root is None)
(successor of maximun is virtual node)

"""
from AVLTree import AVLTree, AVLNode, VirtualLeaf, VirtualRoot
from print_tree import *

def check_size(node):
    if isinstance(node, VirtualRoot) or isinstance(node, VirtualLeaf):
        return 0
    temp=check_size(node.left)+check_size(node.right)+1
    if temp!= node.size:
        print("probelm with ", node.key,". size should be ",temp," but its ",node.size)

    return temp

def check_height(node):
    if isinstance(node, VirtualRoot) or isinstance(node, VirtualLeaf):
        return -1
    temp=max(check_height(node.left),check_height(node.right))+1
    if temp!= node.height:
        print("probelm with ", node.key,". height should be ",temp," but its ",node.height)
    return temp

def get_successor(node):
    dontAskWhy=node
    if node.right.is_real_node():
        nodi=node.right
        while nodi.left.is_real_node():
            nodi=nodi.left
        return nodi
    else:
        while not isinstance(node.parent, VirtualRoot):
            if node==node.parent.left:
                return node.parent
            node=node.parent
    while dontAskWhy.left.is_real_node():
        dontAskWhy=dontAskWhy.left
    return dontAskWhy.left

def check_successor(node, p = False):
    while node.left.is_real_node():
        node=node.left
    while(node.is_real_node()):
        realSucc=get_successor(node)
        maybeSucc=node.successor
        if p:
            if isinstance(realSucc, VirtualLeaf) and isinstance(maybeSucc, VirtualLeaf):
                print("analyzing ", node.key, ". successor should be virtual node and it is so")
            elif isinstance(realSucc, VirtualLeaf) and (maybeSucc.is_real_node()):
                print("analyzing ", node.key,". node successor is", maybeSucc.key, "altough it needs to be virtual")
            elif (realSucc.is_real_node()) and isinstance(maybeSucc, VirtualLeaf):
                print("analyzing ", node.key,". node successor is Virtual altough it needs to be", realSucc.key)
            else:
                print("analyzing ", node.key, ". successor shold be", realSucc.key," and its", maybeSucc.key)
        if realSucc!=maybeSucc:

            print("probelm with successor of ", node.key,". successor shold be", realSucc.key," but its", maybeSucc.key)
            return
        node=maybeSucc

def visualy_check_maxRange(Tree,a,b):
    lst = Tree.avl_to_array()
    print(' '.join(map(str, lst)))
    node=Tree.max_range(a,b)
    print("max is", node.value, "in node ",node.key)

def check_balanced(node):
    if isinstance(node, VirtualRoot) or isinstance(node, VirtualLeaf):
        return True
    heightL=node.left.height
    heightR=node.right.height
    a = heightL - heightR
    t = a in (0,1,-1)
    balanced =  t and check_balanced(node.left) and check_balanced(node.right)
    if not balanced:
        print(node.key,"is not balanced")
    return balanced

T1=AVLTree()
n=10
for i in range(n):
    T1.insert(i,"")
    T1.insert((2*n)-i,"")
for i in range(0,n,3):
    T1.delete(T1.search((2*n)-i))


T2=AVLTree()
for i in range (n):
    T2.insert(i,"")


T3=AVLTree()
T3.insert(15,"a")
T3.insert(8,"a")
T3.insert(22,"c")
T3.insert(4,"")
T3.insert(11,"d")
T3.insert(20,"z")
T3.insert(24,"")
T3.insert(2,"")
T3.insert(9,"b")
T3.insert(12,"e")
T3.insert(18,"a")
T3.insert(13,"f")
T3.delete(T3.search(24))
T3.insert(10,"c")
T3.insert(11.5,"c")
T3.insert(23,"g")
T3.delete(T3.search(2))
T3.delete(T3.search(4))


T4 = AVLTree() #NOT BALANCED
T4.insert(2,"")
vir=T4.get_root().left
T4.insert(1,"")
T4.insert(3,"")
T4.get_root().right.right=AVLNode(4,"")
T4.get_root().right.left=vir
T4.get_root().right.right.right=AVLNode(5,"")
T4.get_root().right.right.right.left=vir
T4.get_root().right.right.right.right=vir
T4.get_root().right.right.left=vir




m=1000
T5=AVLTree()
for i in range(m):
    T5.insert(i,"")
for i in range(0,m,3):
    T5.delete(T5.search(i))
for i in range(m,2*m,2):
    T5.insert(i,"")
for i in range(m,2*m,4):
    T5.delete(T5.search(i))

print("started")
# check_height(T1.get_root())
# check_height(T2.get_root())
# check_height(T3.get_root())
# check_height(T5.get_root())
check_size(T1.get_root())
# check_size(T2.get_root())
# check_size(T3.get_root())
# check_size(T5.get_root())
# check_successor(T1.get_root(), False)
# check_successor(T2.get_root(),False)
# check_successor(T3.get_root(),False)
# check_successor(T5.get_root(),False)
# check_balanced(T1.get_root())
# check_balanced(T2.get_root())
# check_balanced(T3.get_root())
# check_balanced(T5.get_root())
print("completed")