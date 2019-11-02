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
        if type(r) is int: self.root = Node(r)
        elif type(r) is Node: self.root = Node(r.value)

        self.root.left = self.nil
        self.root.right = self.nil
        self.root.color = 'black'

    def showRoot(self):
        print('Raiz da árvore: ')
        self.root.showNode()

    def getGrandparent(self, node):
        if node.parent.parent != None: 
            return node.parent.parent
        else: 
            return None

    def getUncle(self, node):
        g = self.getGrandparent(node)

        if g.left != node.parent:
            return g.left
        else:
            return g.right

    def getSibling(self, node):
        if node.parent.left != node:
            return node.parent.left
        else:
            return node.parent.right

    def insert(self, v, check_insertion=True):
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
        elif node.parent.color == 'red' and self.getUncle(node).color == 'red':
            self.insertCase3(node)

        # Caso 4: se a cor do pai for vermelho e a do tio for preta
        elif node.parent.color == 'red' and self.getUncle(node).color == 'black':
            self.insertCase4(node)

    def insertCase1(self, node):
        if node.parent == None:
            node.color = 'black'

    def insertCase2(self, node):
        # Do nothing...
        pass

    def insertCase3(self, node):
        node.parent.color = 'black'
        self.getUncle(node).color = 'black'
        self.getGrandparent(node).color = 'red'
        
        self.checkInsertionCases(self.getGrandparent(node))

    def insertCase4(self, node):
        # left-right
        if node == node.parent.right and node.parent == self.getGrandparent(node).left:
            self.rotateLeft(node.parent)
            node.color = 'black'
            node.parent.color = 'red'
            self.rotateRight(node.parent)

        # right-left
        elif node == node.parent.left and node.parent == self.getGrandparent(node).right:
            self.rotateRight(node.parent)
            node.color = 'black'
            node.parent.color = 'red'
            self.rotateLeft(node.parent)

        # right-right
        elif node == node.parent.left and node.parent == self.getGrandparent(node).left:
            node.parent.color = 'black'
            self.getGrandparent(node).color = 'red'
            self.rotateRight(self.getGrandparent(node))

        # left-left
        elif node == node.parent.right and node.parent == self.getGrandparent(node).right:
            node.parent.color = 'black'
            self.getGrandparent(node).color = 'red'
            self.rotateLeft(self.getGrandparent(node))

    def remove(self, v, check_removal=True):
        if type(v) is int: node = self.findNode(v)
        elif type(v) is Node: node = v

        # Remoção se o nó não tem filho
        if node.left == self.nil and node.right == self.nil:
            if node.parent == None:
                return None
            
            if node.parent.left == node: 
                node.parent.left = self.nil
            else: 
                node.parent.right = self.nil

            if node.color == 'red':
                # Do nothing...
                del node
            
            elif node.color == 'black':
                to_check = node.left # Tanto faz se é left ou right já que os dos são nil
                to_check.parent = node.parent

                if node == node.parent.left:
                    node.parent.left = to_check
                else:
                    node.parent.right
                
                del node

                self.checkRemoveCases(to_check)

        # Remoção se o nó só tem o filho da direita
        elif node.left == self.nil:
            # Se o nó eh a raiz:
            if node == self.root:
                self.setRoot(node.right)
                self.root.parent = None
            else:
                if node.parent.left == node: 
                    node.parent.left = node.right
                    to_check = node.parent.left
                else:
                    node.parent.right = node.right
                    to_check = node.parent.right

                node.right.parent = node.parent
                del node

                self.checkRemoveCases(to_check)

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

                self.checkRemoveCases(to_check)

        # Remoção se o nó tem dois filhos
        else:
            pred = self.predecessor(node)
            node.value = pred.value
            self.remove(pred)

    def checkRemoveCases(self, node):
        # Caso 1: node é a nova raiz
        if node.parent == None:
            # Do nothing...
            pass

        # Caso 2: todos pretos, apenas sibling é vermelho
        elif (node.color == 'black' and node.parent.color == 'black' and 
            self.getSibling(node).color == 'red' and 
            self.getSibling(node).left.color == 'black' and
            self.getSibling(node).right.color == 'black'):

            self.removeCase2(node)

        # Caso 3: todos pretos
        if (node.color == 'black' and node.parent.color == 'black' and 
            self.getSibling(node).color == 'black' and 
            self.getSibling(node).left.color == 'black' and
            self.getSibling(node).right.color == 'black'):

            self.removeCase3(node)

        # Caso 4: todos pretos, apenas o pai de node é vermelho
        elif (node.color == 'black' and node.parent.color == 'red' and 
            self.getSibling(node).color == 'black' and 
            self.getSibling(node).left.color == 'black' and
            self.getSibling(node).right.color == 'black'):

            self.removeCase4(node)

        # Caso 5: todos pretos, apenas o filho a esqueda de sibling é vermelho
        elif (node.color == 'black' and node.parent.color == 'black' and
            self.getSibling(node).color == 'black' and
            self.getSibling(node).left.color == 'red' and
            self.getSibling(node).right.color == 'black'):

            self.removeCase5(node)

        # Caso 5 especial: todos pretos, mas os dois filhos de sibling são vermelhos
        elif (node.color == 'black' and node.parent.color == 'black' and
            self.getSibling(node).color == 'black' and
            self.getSibling(node).left.color == 'red' and
            self.getSibling(node).right.color == 'red'):

            self.removeCase5S(node)

        # Caso 6: todos pretos, apenas o filho a direita de sibling é vermelho
        elif (node.color == 'black' and
            self.getSibling(node).color == 'black' and
            self.getSibling(node).left.color == 'black' and
            self.getSibling(node).right.color == 'red'):

            self.removeCase6(node)

    def removeCase2(self, node):
        node.parent.color = 'red'
        self.getSibling(node).color = 'black'
        self.rotateLeft(node.parent)

    def removeCase3(self, node):
        self.getSibling(node).color = 'red'

    def removeCase4(self, node):
        node.parent.color = 'black'
        self.getSibling(node).color = 'red'

    def removeCase5(self, node):
        p = node.parent # para não perder o ponteiro para o pai

        self.getSibling(node).color = 'red'
        
        self.getSibling(node).left.color = 'black'
        self.rotateRight(self.getSibling(node))

        node.parent = p
        self.removeCase6(node)

    def removeCase5S(self, node):
        self.getSibling(node).right.color = 'black'
        self.rotateLeft(node.parent)

    def removeCase6(self, node):
        p = node.parent
        
        self.getSibling(node).right.color = 'black'
        self.getSibling(node).color = node.parent.color
        node.parent.color = 'black'
        self.rotateLeft(p)

        self.nil.parent = None # A folha nil não tem pai pois é compartilhada,
                               #  então é necessário resetar

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

    # Chama a função recursva para imprimir os nós em ordem 
    # Não tem necessidade de passar a raiz da árvore, já que é um método dela mesma
    def inOrder(self):
        self.inOrderRec(self.root)

    # Percorre a arvore recursivamente e imprime os nós em ordem
    def inOrderRec(self, node):
        if node.left != self.nil: self.inOrderRec(node.left)
        node.showNode()
        if node.right != self.nil: self.inOrderRec(node.right)

    def preOrder(self):
        self.preOrderRec(self.root)

    def preOrderRec(self, node):
        node.showNode()
        if node.left != self.nil: self.preOrderRec(node.left)
        if node.right != self.nil: self.preOrderRec(node.right)

    def postOrder(self):
        self.postOrderRec(self.root)

    def postOrderRec(self, node):
        if node.left != self.nil: self.postOrder(node.left)
        if node.right != self.nil: self.postOrder(node.right)
        node.showNode()

# Alguns exemplos...

arvore = ArvoreVermelhoPreto()

# EXEMPLO 1:
# nodes1 = [30,10,60,5,15,50,70,90]
# arvore.insertNodes(nodes1)
# arvore.inOrder()

# EXEMPLO 2:
# Essa entrada causa os casos dw remoção 5-6 se remover o número 10
# nodes = [30,10,60,50]
# arvore.insertNodes(nodes)

# print('#'*20, 'Antes de remover 10', '#'*20)
# arvore.inOrder()

# arvore.remove(10)

# print('#'*20, 'Depois de remover 10', '#'*20)
# arvore.inOrder()
