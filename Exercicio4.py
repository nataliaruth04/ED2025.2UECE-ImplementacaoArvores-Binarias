"""LinkedBinaryTree + travessias + verificador de igualdade
"""

from typing import Any, Optional, Generator


class LinkedBinaryTree:
    """Árvore binária encadeada simples.

    Cada nó guarda referência para pai, filho esquerdo e filho direito.
    A classe fornece uma pequena API baseada na ideia de `Position`.
    """

    class _Node:
        __slots__ = ("elem", "parent", "left", "right")

        def __init__(self, elem: Any, parent: Optional["LinkedBinaryTree._Node"] = None):
            self.elem = elem
            self.parent = parent
            self.left: Optional["LinkedBinaryTree._Node"] = None
            self.right: Optional["LinkedBinaryTree._Node"] = None

    class Position:
        """Objeto leve que expõe um nó (sem permitir acesso direto ao ponteiro)."""
        def __init__(self, container: "LinkedBinaryTree", node: Optional["_Node"]):
            self._container = container
            self._node = node

        def element(self) -> Any:
            return self._node.elem

        def __eq__(self, other: object) -> bool:
            return type(other) is type(self) and other._node is self._node

        def __bool__(self) -> bool:
            return self._node is not None

    # ---------------- construtor e utilitários ----------------
    def __init__(self):
        self._root: Optional[LinkedBinaryTree._Node] = None
        self._size = 0

    def __len__(self) -> int:
        return self._size

    def _validate(self, p: "LinkedBinaryTree.Position") -> "_Node":
        if not isinstance(p, LinkedBinaryTree.Position):
            raise TypeError("p deve ser uma Position")
        if p._container is not self:
            raise ValueError("Position não pertence a esta árvore")
        if p._node is None:
            raise ValueError("Position inválida (node é None)")
        return p._node

    def _make_position(self, node: Optional["_Node"]) -> Optional["LinkedBinaryTree.Position"]:
        return LinkedBinaryTree.Position(self, node) if node is not None else None

    # ---------------- acessores básicos ----------------
    def root(self) -> Optional["LinkedBinaryTree.Position"]:
        return self._make_position(self._root)

    def parent(self, p: "LinkedBinaryTree.Position") -> Optional["LinkedBinaryTree.Position"]:
        node = self._validate(p)
        return self._make_position(node.parent)

    def left(self, p: "LinkedBinaryTree.Position") -> Optional["LinkedBinaryTree.Position"]:
        node = self._validate(p)
        return self._make_position(node.left)

    def right(self, p: "LinkedBinaryTree.Position") -> Optional["LinkedBinaryTree.Position"]:
        node = self._validate(p)
        return self._make_position(node.right)

    def is_root(self, p: "LinkedBinaryTree.Position") -> bool:
        return self.root() == p

    def is_leaf(self, p: "LinkedBinaryTree.Position") -> bool:
        node = self._validate(p)
        return node.left is None and node.right is None

    def is_empty(self) -> bool:
        return self._size == 0

    # ---------------- modificadores (simples) ----------------
    def add_root(self, e: Any) -> "LinkedBinaryTree.Position":
        """Cria a raiz se não existir (erro se já existir)."""
        if self._root is not None:
            raise ValueError("Raiz já existe")
        self._root = LinkedBinaryTree._Node(e)
        self._size = 1
        return self._make_position(self._root)  # type: ignore

    def add_left(self, p: "LinkedBinaryTree.Position", e: Any) -> "LinkedBinaryTree.Position":
        node = self._validate(p)
        if node.left is not None:
            raise ValueError("Filho esquerdo já existe")
        node.left = LinkedBinaryTree._Node(e, parent=node)
        self._size += 1
        return self._make_position(node.left)  # type: ignore

    def add_right(self, p: "LinkedBinaryTree.Position", e: Any) -> "LinkedBinaryTree.Position":
        node = self._validate(p)
        if node.right is not None:
            raise ValueError("Filho direito já existe")
        node.right = LinkedBinaryTree._Node(e, parent=node)
        self._size += 1
        return self._make_position(node.right)  # type: ignore

    def replace(self, p: "LinkedBinaryTree.Position", e: Any) -> Any:
        node = self._validate(p)
        old = node.elem
        node.elem = e
        return old

    # ---------------- travessias implementadas como geradores ----------------
    def preorder(self) -> Generator["LinkedBinaryTree.Position", None, None]:
        """Gera posições em pré-ordem (root, left, right)."""

        def _subtree_preorder(n: Optional[LinkedBinaryTree._Node]):
            if n is None:
                return
            yield self._make_position(n)
            yield from _subtree_preorder(n.left)
            yield from _subtree_preorder(n.right)

        yield from (pos for pos in _subtree_preorder(self._root) if pos is not None)  

    def inorder(self) -> Generator["LinkedBinaryTree.Position", None, None]:
        """Gera posições em ordem infixa (left, root, right)."""

        def _subtree_inorder(n: Optional[LinkedBinaryTree._Node]):
            if n is None:
                return
            yield from _subtree_inorder(n.left)
            yield self._make_position(n)
            yield from _subtree_inorder(n.right)

        yield from (pos for pos in _subtree_inorder(self._root) if pos is not None)  

    def postorder(self) -> Generator["LinkedBinaryTree.Position", None, None]:
        """Gera posições em pós-ordem (left, right, root)."""

        def _subtree_postorder(n: Optional[LinkedBinaryTree._Node]):
            if n is None:
                return
            yield from _subtree_postorder(n.left)
            yield from _subtree_postorder(n.right)
            yield self._make_position(n)

        yield from (pos for pos in _subtree_postorder(self._root) if pos is not None)  

    # ---------------- utilitários para debug / visão geral ----------------
    def __str__(self) -> str:
        """Representação simples: lista infixa de elementos (útil pra debug)."""
        return "[" + ", ".join(str(p.element()) for p in self.inorder()) + "]"


# ---------------- função para verificar igualdade de árvores ----------------
def trees_identical(T1: LinkedBinaryTree, T2: LinkedBinaryTree) -> bool:
    """Retorna True se T1 e T2 são idênticas (mesma forma e mesmos elementos)."""

    def _ident(n1: Optional[LinkedBinaryTree._Node], n2: Optional[LinkedBinaryTree._Node]) -> bool:
        # se ambos são None, tudo bem se só um é None, não-idênticas
        if n1 is None and n2 is None:
            return True
        if (n1 is None) ^ (n2 is None):
            return False
        # agora ambos não são None, comparar elemento e recursivamente filhos
        if n1.elem != n2.elem:
            return False
        return _ident(n1.left, n2.left) and _ident(n1.right, n2.right)

    return _ident(T1._root, T2._root)


# ---------------- exemplo / teste rápido (estilo estudante) ----------------
if __name__ == "__main__":
    print("== Teste rápido LinkedBinaryTree ==")

    # Montando árvore T1 (manual, só pra testar)
    T1 = LinkedBinaryTree()
    r = T1.add_root("A")          # raiz A
    b = T1.add_left(r, "B")       #  / \
    c = T1.add_right(r, "C")      # B   C
    T1.add_left(b, "D")           # B tem filho esquerdo D
    T1.add_right(b, "E")          # B tem filho direito E
    T1.add_right(c, "F")          # C tem filho direito F

    print("T1 (inorder):", list(p.element() for p in T1.inorder()))
    print("T1 (preorder):", list(p.element() for p in T1.preorder()))
    print("T1 (postorder):", list(p.element() for p in T1.postorder()))

    # Montando T2 idêntica a T1
    T2 = LinkedBinaryTree()
    r2 = T2.add_root("A")
    b2 = T2.add_left(r2, "B")
    c2 = T2.add_right(r2, "C")
    T2.add_left(b2, "D")
    T2.add_right(b2, "E")
    T2.add_right(c2, "F")

    print("T1 == T2 ?", trees_identical(T1, T2))  # espera True

    # Mudar T2 para não-idêntica
    T2.replace(b2, "B_changed")
    print("Depois de alterar T2: T1 == T2 ?", trees_identical(T1, T2))  # espera False

    # Outro exemplo: estruturas diferentes
    T3 = LinkedBinaryTree()
    r3 = T3.add_root("A")
    T3.add_left(r3, "B")  # diferente (não tem C)
    print("T1 == T3 ?", trees_identical(T1, T3))  # espera False
