class LinkedBinaryTree:
    class _Node:
        def __init__(self, element, left=None, right=None):
            self.element = element
            self.left = left
            self.right = right

    def __init__(self):
        self._root = None
        self._size = 0
    
    # Inserção básica (utilizada nos testes)
    def add_root(self, e):
        if self._root is not None:
            raise ValueError("Raiz já existe")
        self._root = self._Node(e)
        self._size = 1
        return self._root
    
    def add_left(self, node, e):
        if node.left is not None:
            raise ValueError("Esse nó já tem filho esquerdo")
        node.left = self._Node(e)
        self._size += 1
        return node.left
    
    def add_right(self, node, e):
        if node.right is not None:
            raise ValueError("Esse nó já tem filho direito")
        node.right = self._Node(e)
        self._size += 1
        return node.right

   
    #               Traversals – Seção 8.4.4 do PDF
   

    def preorder(self):
        """Retorna lista com os elementos visitados em Preorder."""
        resultado = []
        self._preorder(self._root, resultado)
        return resultado

    def _preorder(self, node, lista):
        if node is not None:
            lista.append(node.element)            # visita o nó
            self._preorder(node.left, lista)      # visita subárvore esquerda
            self._preorder(node.right, lista)     # visita subárvore direita

    def inorder(self):
        """Retorna lista com os elementos visitados em Inorder."""
        resultado = []
        self._inorder(self._root, resultado)
        return resultado

    def _inorder(self, node, lista):
        if node is not None:
            self._inorder(node.left, lista)       # esquerda
            lista.append(node.element)            # nó
            self._inorder(node.right, lista)      # direita

    def postorder(self):
        """Retorna lista com os elementos visitados em Postorder."""
        resultado = []
        self._postorder(self._root, resultado)
        return resultado

    def _postorder(self, node, lista):
        if node is not None:
            self._postorder(node.left, lista)     # filho esquerdo
            self._postorder(node.right, lista)    # filho direito
            lista.append(node.element)            # visita o nó
