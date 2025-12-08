from typing import Any, Optional, Iterator, List
from collections import deque

class LinkedBinaryTree:
    """Implementação de uma árvore binária.
    """

    # ---------------- nested Position class ----------------
    class Position:
        """Abstração para a posição de um elemento dentro da árvore."""
        def __init__(self, container: 'LinkedBinaryTree', node: 'LinkedBinaryTree._Node'):
            self._container = container
            self._node = node

        def element(self) -> Any:
            return self._node.element

        def __eq__(self, other: object) -> bool:
            if not isinstance(other, LinkedBinaryTree.Position):
                return False
            return other._node is self._node and other._container is self._container

        def __ne__(self, other: object) -> bool:
            return not (self == other)

        def __repr__(self) -> str:
            return f"Position({self._node.element!r})"

    # ---------------- internal Node class ----------------
    class _Node:
        __slots__ = 'element', 'parent', 'left', 'right'
        def __init__(self, element: Any, parent: Optional['LinkedBinaryTree._Node'] = None,
                     left: Optional['LinkedBinaryTree._Node'] = None,
                     right: Optional['LinkedBinaryTree._Node'] = None):
            self.element = element
            self.parent = parent
            self.left = left
            self.right = right

    # ---------------- constructor ----------------
    def __init__(self):
        # cria árvore vazia
        self._root: Optional[LinkedBinaryTree._Node] = None
        self._size: int = 0

    # ---------------- utilitários internos ----------------
    def _validate(self, p: 'LinkedBinaryTree.Position') -> 'LinkedBinaryTree._Node':
        """Transforma uma Position em nó interno; levanta erro se inválido."""
        if not isinstance(p, LinkedBinaryTree.Position):
            raise TypeError("p deve ser uma Position válido")
        if p._container is not self:
            raise ValueError("p não pertence a esta árvore")
        if p._node.parent is p._node:                # convenção para nó desativado
            raise ValueError("p já foi removido")
        return p._node

    def _make_position(self, node: Optional['_Node']) -> Optional['Position']:
        """Retorna Position para nó (ou None)."""
        return None if node is None else LinkedBinaryTree.Position(self, node)

    # ---------------- informações básicas ----------------
    def __len__(self) -> int:
        return self._size

    def is_empty(self) -> bool:
        return self._size == 0

    def root(self) -> Optional['Position']:
        return self._make_position(self._root)

    def parent(self, p: 'Position') -> Optional['Position']:
        node = self._validate(p)
        return self._make_position(node.parent)

    def left(self, p: 'Position') -> Optional['Position']:
        node = self._validate(p)
        return self._make_position(node.left)

    def right(self, p: 'Position') -> Optional['Position']:
        node = self._validate(p)
        return self._make_position(node.right)

    def sibling(self, p: 'Position') -> Optional['Position']:
        node = self._validate(p)
        parent = node.parent
        if parent is None:
            return None
        if parent.left is node:
            return self._make_position(parent.right)
        else:
            return self._make_position(parent.left)

    def num_children(self, p: 'Position') -> int:
        node = self._validate(p)
        cnt = 0
        if node.left is not None:
            cnt += 1
        if node.right is not None:
            cnt += 1
        return cnt

    def children(self, p: 'Position') -> Iterator['Position']:
        node = self._validate(p)
        if node.left is not None:
            yield self._make_position(node.left)
        if node.right is not None:
            yield self._make_position(node.right)

    # ---------------- modificadores (update) ----------------
    def add_root(self, e: Any) -> 'Position':
        """Adiciona raiz se árvore estiver vazia, retorna a posição da raiz."""
        if self._root is not None:
            raise ValueError("raiz já existe")
        self._root = LinkedBinaryTree._Node(e)
        self._size = 1
        # posição da raiz
        return self._make_position(self._root)  # type: ignore

    def add_left(self, p: 'Position', e: Any) -> 'Position':
        node = self._validate(p)
        if node.left is not None:
            raise ValueError("já existe filho esquerdo")
        node.left = LinkedBinaryTree._Node(e, parent=node)
        self._size += 1
        return self._make_position(node.left)  # type: ignore

    def add_right(self, p: 'Position', e: Any) -> 'Position':
        node = self._validate(p)
        if node.right is not None:
            raise ValueError("já existe filho direito")
        node.right = LinkedBinaryTree._Node(e, parent=node)
        self._size += 1
        return self._make_position(node.right)  # type: ignore

    def replace(self, p: 'Position', e: Any) -> Any:
        """Substitui o elemento em p por e; retorna o elemento antigo."""
        node = self._validate(p)
        old = node.element
        node.element = e
        return old

    def delete(self, p: 'Position') -> Any:
        """Remove o nó p que tem no máximo 1 filho.
        Retorna o elemento do nó removido.
        Após remoção, a posição p fica inválida (marcada).
        """
        node = self._validate(p)
        if self.num_children(p) == 2:
            raise ValueError("não pode remover nó com dois filhos")
        # filho único ou nenhum
        child = node.left if node.left is not None else node.right
        if child is not None:
            child.parent = node.parent
        if node is self._root:
            self._root = child
        else:
            parent = node.parent
            if parent.left is node:
                parent.left = child
            else:
                parent.right = child
        self._size -= 1
        # desativa node
        node.parent = node  # convenção: parent aponta para si mesmo significa inválido
        return node.element

    def attach(self, p: 'Position', t1: 'LinkedBinaryTree', t2: 'LinkedBinaryTree') -> None:
        """Anexa duas árvores t1 e t2 como subárvores esquerda/direita de p (que deve ser folha).
        Depois da operação, t1 e t2 ficam vazias (seus nós são transferidos para self).
        """
        node = self._validate(p)
        if self.num_children(p) > 0:
            raise ValueError("p deve ser folha para attach")
        # anexar t1 como left
        if not t1.is_empty():
            t1_root = t1._root
            node.left = t1_root
            t1_root.parent = node
            self._size += t1._size
            # esvazia t1
            t1._root = None
            t1._size = 0
        # anexar t2 como right
        if not t2.is_empty():
            t2_root = t2._root
            node.right = t2_root
            t2_root.parent = node
            self._size += t2._size
            t2._root = None
            t2._size = 0

    # ---------------- traversals / iterators ----------------
    def _subtree_preorder(self, p: 'Position') -> Iterator['Position']:
        yield p
        for c in self.children(p):
            yield from self._subtree_preorder(c)

    def preorder(self) -> Iterator['Position']:
        if not self.is_empty():
            yield from self._subtree_preorder(self.root())  # type: ignore

    def _subtree_postorder(self, p: 'Position') -> Iterator['Position']:
        for c in self.children(p):
            yield from self._subtree_postorder(c)
        yield p

    def postorder(self) -> Iterator['Position']:
        if not self.is_empty():
            yield from self._subtree_postorder(self.root())  # type: ignore

    def _subtree_inorder(self, p: 'Position') -> Iterator['Position']:
        """Inorder específico para árvore binária: left, node, right."""
        node = self._validate(p)
        if node.left is not None:
            yield from self._subtree_inorder(self._make_position(node.left))  # type: ignore
        yield self._make_position(node)  # type: ignore
        if node.right is not None:
            yield from self._subtree_inorder(self._make_position(node.right))  # type: ignore

    def inorder(self) -> Iterator['Position']:
        if not self.is_empty():
            yield from self._subtree_inorder(self.root())  # type: ignore

    def breadthfirst(self) -> Iterator['Position']:
        if not self.is_empty():
            fringe = deque()
            fringe.append(self.root())
            while fringe:
                p = fringe.popleft()
                yield p  # type: ignore
                for c in self.children(p):  # type: ignore
                    fringe.append(c)

    # ---------------- utilitários de representação ----------------
    def __iter__(self) -> Iterator[Any]:
        """Itera sobre elementos em inorder (útil para debugging)."""
        for p in self.inorder():
            yield p.element()  # type: ignore

    def __str__(self) -> str:
        if self.is_empty():
            return "LinkedBinaryTree()"
        return "LinkedBinaryTree(inorder: [" + ", ".join(repr(e) for e in self) + "])"

# ---------------- exemplo rápido de uso ----------------
if __name__ == "__main__":
    # criação simples: raiz e dois filhos
    T = LinkedBinaryTree()
    r = T.add_root("root")
    left = T.add_left(r, "L")
    right = T.add_right(r, "R")
    T.add_left(left, "L-L")
    T.add_right(left, "L-R")
    T.add_left(right, "R-L")

    print("Impressão inorder (percorrendo elementos):")
    for elem in T:
        print(" ", elem)

    print("\nPreorder (posições):")
    for p in T.preorder():
        print(" ", p)

    print("\nEstrutura (str):", T)
