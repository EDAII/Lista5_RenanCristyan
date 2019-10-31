# Árvore Vermelho e Preto

from time import sleep

class Node():
    def __init__(self, v, color='red'):
        self.value = v
        self.color = color
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
        
        print('color = ', self.color)
        print('-'*10,'\n')

class ArvoreVermelhoPreto():
    def __init__(self, r=None):
        self.root = Node(r)
        self.nil = Node(v='nil', color='black')

    def setRoot(self, r):
        self.root = Node(r)
        self.root.left = self.nil
        self.root.right = self.nil
        self.root.color = 'black'

    def showRoot(self):
        print('Raiz da árvore: ')
        self.root.showNode()

    def getGrandparent(self, node):
        if node.parent.parent != None: return node.parent.parent
        else: return None

    def getUncle(self, node):
        g = self.getGrandparent(node)

        if g.left != node.parent: return g.left
        else: return g.right

    def getSibling(self, node):
        if node.parent.left != node: return node.parent.left
        else: return node.parent.right

    def insert(self, v, check_insertion=True):
        # Cria um novo nó com valor v e insere na árvore no local correto

        new_node = Node(v)
        new_node.left = self.nil
        new_node.right = self.nil
        new_node_parent = self.findNode(v, return_last_node=True)
        new_node.setParent(new_node_parent)

        if check_insertion: self.checkInsertionCases(new_node)

    def insertNodes(self, list_of_values):
        self.setRoot(list_of_values[0])
        
        i = 1
        while i < len(list_of_values):
            self.insert(list_of_values[i])
            i += 1

    def checkInsertionCases(self, node):
        # Caso 1: Se for a raiz
        if node.parent == None:
            self.insertCase1(node)

        # Caso 2: se a cor do nó pai for preta
        elif node.parent.color == 'black':
            self.insertCase2(node)

        # Caso 3: se as cores do pai e do tio forem vermelho
        elif node.parent.color == 'red' and my_tree.getUncle(node).color == 'red':
            self.insertCase3(node)

        elif node.parent.color == 'red' and my_tree.getUncle(node).color == 'black':
            self.insertCase4(node)

    def insertCase1(self, node):
        if node.parent == None: node.color = 'black'

    def insertCase2(self, node):
        # Não faz nada...
        pass

    def insertCase3(self, node):
        node.parent.color = 'black'
        my_tree.getUncle(node).color = 'black'
        my_tree.getGrandparent(node).color = 'red'
        
        my_tree.checkInsertionCases(my_tree.getGrandparent(node))

    def insertCase4(self, node):
        # left-right
        if node == node.parent.right and node.parent == my_tree.getGrandparent(node).left:
            my_tree.rotateLeft(node.parent)
            node.color = 'black'
            node.parent.color = 'red'
            my_tree.rotateRight(node.parent)

        # right-left
        elif node == node.parent.left and node.parent == my_tree.getGrandparent(node).right:
            my_tree.rotateRight(node.parent)
            node.color = 'black'
            node.parent.color = 'red'
            my_tree.rotateLeft(node.parent)

        # right-right
        elif node == node.parent.left and node.parent == my_tree.getGrandparent(node).left:
            node.parent.color = 'black'
            my_tree.getGrandparent(node).color = 'red'
            my_tree.rotateRight(my_tree.getGrandparent(node))

        # left-left
        elif node == node.parent.right and node.parent == my_tree.getGrandparent(node).right:
            node.parent.color = 'black'
            my_tree.getGrandparent(node).color = 'red'
            my_tree.rotateLeft(my_tree.getGrandparent(node))

    def remove(self, v, check_removal=True):
        # Remove um valor v da árvore

        if type(v) is int: node = self.findNode(v)
        elif type(v) is Node: node = v

        # Remoção se o nó não tem filho
        if node.left == self.nil and node.right == self.nil:
            if node.parent == None:
                return None
            if node.parent.left == node: 
                node.parent.left = self.nil
                to_check = node.parent.left
            else: 
                node.parent.right = self.nil
                to_check = node.parent.right

            del node

        # Remoção se o nó só tem o filho da direita
        elif node.left == self.nil:
            # Se o nó eh a raiz:
            if node == self.root:
                self.setRoot(node.right)
                self.root.parent = None
                to_check = self.root
            else:
                if node.parent.left == node: 
                    node.parent.left = node.right
                    to_check = node.parent.left
                else:
                    node.parent.right = node.right
                    to_check = node.parent.right

                node.right.parent = node.parent
                del node

        # Remoção se o nó só tem o filho da esquerda
        elif node.right == None:
            if node == self.root:
                self.setRoot(node.left)
                self.root.parent = None
                to_check = self.root
            else:
                if node.parent.left == node:
                    node.parent.left = node.left
                    to_check = node.parent.left
                else:
                    node.parent.right = node.left
                    to_check = node.parent.right

                node.left.parent = node.parent
                del node

        # Remoção se o nó tem dois filhos
        else:
            pred = self.predecessor(node)
            node.value = pred.value
            to_check = node
            self.remove(pred)

    def predecessor(self, node):
        pred = node.left

        if node.left == self.nil:
            return None

        while pred.right != self.nil:
            pred = pred.right

        return pred

    def findNode(self, v, return_last_node=False):
        # Retorna o nó com o valor informado se encontrar na árvore
        # Se nao encontrar, retorna None
        # Se não encontrar e return_last_node == True, retorna o último nó antes de None (útil para inserção)

        atual = self.root

        while True:
            if v < atual.value:
                if atual.left == self.nil: # Chegou no fim e não achou
                    if return_last_node: return atual
                    else: return None
                else:
                    atual = atual.left
            
            elif v > atual.value:
                if atual.right == self.nil: # Chegou no fim e não achou
                    if return_last_node: return atual
                    else: return None
                else:
                    atual = atual.right
            
            else: # Achou
                return atual

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

    def preOrder(self, root):
        root.showNode()
        if root.left != self.nil: self.preOrder(root.left)
        if root.right != self.nil: self.preOrder(root.right)

    def inOrder(self, root):
        if root.left != self.nil: self.inOrder(root.left)
        root.showNode()
        if root.right != self.nil: self.inOrder(root.right)

    def postOrder(self, root):
        if root.left != self.nil: self.postOrder(root.left)
        if root.right != self.nil: self.postOrder(root.right)
        root.showNode()
