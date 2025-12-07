from typing import Any, Optional, Iterator, List


class LinkedBinaryTree:
    """Árvore binária encadeada
    """

    class _Node:
        __slots__ = "_element", "_parent", "_left", "_right"

        def __init__(self, element: Any, parent: Optional["LinkedBinaryTree._Node"] = None,
                     left: Optional["LinkedBinaryTree._Node"] = None,
                     right: Optional["LinkedBinaryTree._Node"] = None) -> None:
            self._element = element
            self._parent = parent
            self._left = left
            self._right = right

    class Position:
        """Uma pequena 'visão' de um nó que expõe só o necessário."""
        def __init__(self, container: "LinkedBinaryTree", node: "_Node") -> None:
            self._container = container
            self._node = node

        def element(self) -> Any:
            return self._node._element

        def __eq__(self, other: object) -> bool:
            return type(other) is type(self) and other._node is self._node

        def __repr__(self) -> str:
            return f"Position({self._node._element!r})"

    # ---- construtor ----
    def __init__(self) -> None:
        # _root guarda o nó raiz, _size conta quantos nós existem
        self._root: Optional[LinkedBinaryTree._Node] = None
        self._size: int = 0

    # ---- utilitários internos ----
    def _validate(self, p: "LinkedBinaryTree.Position") -> _Node:
        """Verifica se p é Position pertencente a esta árvore e retorna o nó."""
        if not isinstance(p, self.Position):
            raise TypeError("p deve ser uma Position válida")
        if p._container is not self:
            raise ValueError("Position não pertence a esta árvore")
        if p._node._parent is p._node:  # marca de 'removido'
            raise ValueError("Position já não é válida")
        return p._node

    def _make_position(self, node: Optional[_Node]) -> Optional["LinkedBinaryTree.Position"]:
        return self.Position(self, node) if node is not None else None

    # ---- informações básicas ----
    def __len__(self) -> int:
        return self._size

    def is_empty(self) -> bool:
        return self._size == 0

    def root(self) -> Optional["LinkedBinaryTree.Position"]:
        return self._make_position(self._root)

    def parent(self, p: "LinkedBinaryTree.Position") -> Optional["LinkedBinaryTree.Position"]:
        node = self._validate(p)
        return self._make_position(node._parent)

    def left(self, p: "LinkedBinaryTree.Position") -> Optional["LinkedBinaryTree.Position"]:
        node = self._validate(p)
        return self._make_position(node._left)

    def right(self, p: "LinkedBinaryTree.Position") -> Optional["LinkedBinaryTree.Position"]:
        node = self._validate(p)
        return self._make_position(node._right)

    def num_children(self, p: "LinkedBinaryTree.Position") -> int:
        node = self._validate(p)
        cnt = 0
        if node._left is not None:
            cnt += 1
        if node._right is not None:
            cnt += 1
        return cnt

    def is_leaf(self, p: "LinkedBinaryTree.Position") -> bool:
        return self.num_children(p) == 0

    def is_root(self, p: "LinkedBinaryTree.Position") -> bool:
        return self.root() == p

    # ---- modificadores básicos ----
    def add_root(self, e: Any) -> "LinkedBinaryTree.Position":
        """Coloca a raiz. Erro se já existir raiz."""
        if self._root is not None:
            raise ValueError("Raiz já existe")
        self._root = self._Node(e)
        self._size = 1
        return self._make_position(self._root)  # type: ignore

    def add_left(self, p: "LinkedBinaryTree.Position", e: Any) -> "LinkedBinaryTree.Position":
        node = self._validate(p)
        if node._left is not None:
            raise ValueError("Filho esquerdo já existe")
        node._left = self._Node(e, parent=node)
        self._size += 1
        return self._make_position(node._left)  # type: ignore

    def add_right(self, p: "LinkedBinaryTree.Position", e: Any) -> "LinkedBinaryTree.Position":
        node = self._validate(p)
        if node._right is not None:
            raise ValueError("Filho direito já existe")
        node._right = self._Node(e, parent=node)
        self._size += 1
        return self._make_position(node._right)  # type: ignore

    def replace(self, p: "LinkedBinaryTree.Position", e: Any) -> Any:
        node = self._validate(p)
        old = node._element
        node._element = e
        return old

    def delete(self, p: "LinkedBinaryTree.Position") -> Any:
        """Remove o nó em p (tem de ter 0 ou 1 filho). Retorna o elemento."""
        node = self._validate(p)
        if self.num_children(p) == 2:
            raise ValueError("Não é possível deletar nó com 2 filhos")
        child = node._left if node._left else node._right  # pode ser None
        if child is not None:
            child._parent = node._parent
        if node is self._root:
            self._root = child
        else:
            parent = node._parent
            if parent._left is node:
                parent._left = child
            else:
                parent._right = child
        self._size -= 1
        # marca o nó como inválido para evitar usos futuros
        node._parent = node
        return node._element

    # ---- travessias (itertools úteis) ----
    def _subtree_preorder(self, node: _Node) -> Iterator["LinkedBinaryTree.Position"]:
        # visita nó, depois esquerda, depois direita
        yield self._make_position(node)  # type: ignore
        if node._left is not None:
            for p in self._subtree_preorder(node._left):
                yield p
        if node._right is not None:
            for p in self._subtree_preorder(node._right):
                yield p

    def preorder(self) -> Iterator["LinkedBinaryTree.Position"]:
        """Percorre em pré-ordem (raiz, esquerda, direita)."""
        if not self.is_empty():
            for p in self._subtree_preorder(self._root):  # type: ignore
                yield p

    def _subtree_inorder(self, node: _Node) -> Iterator["LinkedBinaryTree.Position"]:
        # esquerda, raiz, direita (apenas para árvores binárias)
        if node._left is not None:
            for p in self._subtree_inorder(node._left):
                yield p
        yield self._make_position(node)  # type: ignore
        if node._right is not None:
            for p in self._subtree_inorder(node._right):
                yield p

    def inorder(self) -> Iterator["LinkedBinaryTree.Position"]:
        if not self.is_empty():
            for p in self._subtree_inorder(self._root):  # type: ignore
                yield p

    def _subtree_postorder(self, node: _Node) -> Iterator["LinkedBinaryTree.Position"]:
        # esquerda, direita, raiz
        if node._left is not None:
            for p in self._subtree_postorder(node._left):
                yield p
        if node._right is not None:
            for p in self._subtree_postorder(node._right):
                yield p
        yield self._make_position(node)  # type: ignore

    def postorder(self) -> Iterator["LinkedBinaryTree.Position"]:
        if not self.is_empty():
            for p in self._subtree_postorder(self._root):  # type: ignore
                yield p

    def breadthfirst(self) -> Iterator["LinkedBinaryTree.Position"]:
        """Percorre por nível (BFS)."""
        if not self.is_empty():
            from collections import deque
            q = deque()
            q.append(self._root)  # type: ignore
            while q:
                node = q.popleft()
                yield self._make_position(node)  # type: ignore
                if node._left is not None:
                    q.append(node._left)
                if node._right is not None:
                    q.append(node._right)

    # ---- utilitários para debugging/uso ----
    def __iter__(self) -> Iterator[Any]:
        """Itera pelos elementos em ordem inorder (comum em árvores binárias)."""
        for p in self.inorder():
            yield p.element()

    def positions(self) -> Iterator["LinkedBinaryTree.Position"]:
        """Retorna posições em preorder (padrão escolhido)."""
        return self.preorder()

    def __repr__(self) -> str:
        # representação simples: lista inorder dos elementos
        elems = [repr(e) for e in self]
        return f"LinkedBinaryTree(inorder=[{', '.join(elems)}])"


# ---------- Exemplo pequeno para testar ----------
if __name__ == "__main__":
    # Monta a árvore abaixo (manual, só pra testar):
    #        A
    #       / \
    #      B   C
    #     /   / \
    #    D   E   F
    t = LinkedBinaryTree()
    r = t.add_root("A")
    b = t.add_left(r, "B")
    c = t.add_right(r, "C")
    d = t.add_left(b, "D")
    e = t.add_left(c, "E")
    f = t.add_right(c, "F")

    print("Pré-ordem (visita raiz primeiro):")
    print([p.element() for p in t.preorder()])

    print("In-ordem (esquerda, raiz, direita):")
    print([p.element() for p in t.inorder()])

    print("Pós-ordem (raiz por último):")
    print([p.element() for p in t.postorder()])

    print("Por nível (BFS):")
    print([p.element() for p in t.breadthfirst()])

    # substitui um elemento
    old = t.replace(c, "C-modificado")
    print("\nApós replace em C:", old, "->", [p.element() for p in t.preorder()])

    # deleta nó D (que tem 0 filhos)
    removed = t.delete(d)
    print("Removido:", removed)
    print("Agora pre-order:", [p.element() for p in t.preorder()])
