# Nome: Renan Cristyan A. Pinheiro
# Matrícula: 17/0044386
# Disciplina: Estruturas de Dados 2 - 2019/2
# Professor: Maurício Serrano

# Árvore AVL

class Node():
    def __init__(self, v):
        self.value = v
        self.parent = None
        self.left = None
        self.right = None

    def setChildren(self, left_children, right_children):
        self.left = left_children
        self.right = right_children
        left_children.parent = self
        right_children.parent = self

    def setParent(self, parent_node):
        self.parent = parent_node
        
        if self.value <= parent_node.value:
            parent_node.left = self
        else:
            parent_node.right = self

    def showNode(self):
        print('value = ', self.value)

        if self.parent == None: print('parent = ', self.parent)
        else: print('parent = ', self.parent.value)

        if self.left == None: print('left = ', self.left)
        else: print('left = ', self.left.value)

        if self.right == None: print('right = ', self.right)
        else: print('right = ', self.right.value)

        print('-'*10,'\n')

class ArvoreAVL():
    def __init__(self, r=None):
        self.root = Node(r)

    def setRoot(self, r):
        self.root = Node(r)

    def showRoot(self):
        print('Raiz da árvore: ')
        self.root.showNode()

    def insert(self, v):
        new_node = Node(v)
        new_node_parent = self.findNode(v, return_last_node=True)
        new_node.setParent(new_node_parent)

        self.retrace(new_node)

    def insertNodes(self, list_of_values):
        self.setRoot(list_of_values[0])
        
        i = 1
        while i < len(list_of_values):
            self.insert(list_of_values[i])
            i += 1

    def remove(self, v):
        if type(v) is int: node = self.findNode(v)
        elif type(v) is Node: node = v

        # Remoção se o nó não tem filho
        if node.left == None and node.right == None:
            if node.parent == None:
                return None
            if node.parent.left == node: node.parent.left = None
            else: node.parent.right = None
            del node

        # Remoção se o nó só tem o filho da direita
        elif node.left == None:
            # Se o nó eh a raiz:
            if node.parent == self.root:
                node.right.parent = None
                self.setRoot(node.left)
            else:
                node.parent.right = node.right
                node.right.parent = node.parent
                del node

        # Remoção se o nó só tem o filho da esquerda
        elif node.right == None:
            if node == self.root:
                self.root = node.left
                node.left.parent = None
            else:
                node.parent.left = node.left
                node.left.parent = node.parent
                del node

        # Remoção se o nó tem dois filhos
        else:
            pred = self.predecessor(node)
            node.value = pred.value
            del node
            self.remove(pred)

    def predecessor(self, node):
        pred = node.left

        if node.left == None:
            return None

        while pred.right != None:
            pred = pred.right

        return pred

    def findNode(self, v, return_last_node=False):
        atual = self.root

        while True:
            if v < atual.value:
                if atual.left == None:
                    if return_last_node: return atual
                    else: return None
                else:
                    atual = atual.left
            
            elif v > atual.value:
                if atual.right == None:
                    if return_last_node: return atual
                    else: return None
                else:
                    atual = atual.right
            
            else:
                return atual

    def preOrder(self, root):
        root.showNode()
        if root.left != None: self.preOrder(root.left)
        if root.right != None: self.preOrder(root.right)

    def inOrder(self, root):
        if root.left != None: self.inOrder(root.left)
        root.showNode()
        if root.right != None: self.inOrder(root.right)

    def postOrder(self, root):
        if root.left != None: self.postOrder(root.left)
        if root.right != None: self.postOrder(root.right)
        root.showNode()

    def rotateLeft(self, node):
        aux = node.right
        aux.parent = node.parent

        if node == self.root: self.root = aux
        else:
            if node.parent.left == node: node.parent.left = aux
            else: node.parent.right = aux

        node.parent = node.right
        node.right = node.right.left
        if node.right != None: node.right.parent = node

        aux.left = node

    def rotateRight(self, node):
        aux = node.left
        aux.parent = node.parent

        if node == self.root: self.root = aux
        else:
            if node.parent.left == node: node.parent.left = aux
            else: node.parent.right = aux

        node.parent = node.left
        node.left = node.left.right
        if node.right != None: node.left.parent = node

        aux.right = node

    def height(self, node):
        if node.left == None and node.right == None:
            return 1
        elif node.left == None: 
            return 1 + self.height(node.right)
        elif node.right == None:
            return 1 + self.height(node.left)
        else:
            return 1 + max(self.height(node.left), self.height(node.right))

    def getBalanceFactor(self, node):
        if node.left == None and node.right == None:
            return 0
        elif node.left == None:
            return self.height(node.right)
        elif node.right == None:
            return -1 * self.height(node.left)
        else:
            return self.height(node.right) - self.height(node.left)

    def retrace(self, node):
        atual = node

        while atual != None:
            if self.getBalanceFactor(atual) >= 2 or self.getBalanceFactor(atual) <= -2:
                
                # Caso para rotação right-right
                if atual.left != None and atual.left.left != None:
                    self.rotateRight(atual)

                # Caso para rotação left-left
                elif atual.right != None and atual.right.right != None:
                    self.rotateLeft(atual)

                # Caso para rotação right-left
                elif atual.right != None and atual.right.left != None:
                    self.rotateRight(atual.right)
                    self.rotateLeft(atual)

                # Caso para rotação left-right
                elif atual.left != None and atual.left.right != None:
                    self.rotateLeft(atual.left)
                    self.rotateRight(atual)

            atual = atual.parent

my_tree = ArvoreAVL()
# nodes = [5,3,8,2,4,6,12,1,7,10,13,9,11]
nodes = [1,2,3,4,5]
my_tree.insertNodes(nodes)
my_tree.inOrder(my_tree.root)
