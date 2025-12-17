from linkedBinaryTree import LinkedBinaryTree


def verifica_arvore_soma(arvore):
    # árvore vazia é considerada árvore soma
    if len(arvore) == 0:
        return True

    # começa a verificação a partir da raiz
    valido, _ = checa_no(arvore.root(), arvore)
    return valido


def checa_no(no, arvore):
    # se o nó não existe, não influencia na soma
    if no is None:
        return True, 0

    # nó folha sempre é válido
    if arvore.num_children(no) == 0:
        return True, no.element()

    # verifica recursivamente esquerda e direita
    ok_esq, soma_esq = checa_no(arvore.left(no), arvore)
    ok_dir, soma_dir = checa_no(arvore.right(no), arvore)

    # se alguma subárvore não for soma, já retorna falso
    if not ok_esq or not ok_dir:
        return False, 0

    # confere se o valor do nó é a soma das subárvores
    if no.element() != soma_esq + soma_dir:
        return False, 0

    # soma total da subárvore atual
    soma_total = no.element() + soma_esq + soma_dir
    return True, soma_total


def exercicio_5():
    print("\n" + "-" * 60)
    print("Exercício 5 - Verificação de Árvore Soma")
    print("-" * 60)

    # árvore do exemplo do enunciado
    arvore1 = LinkedBinaryTree()
    r1 = arvore1._add_root(44)
    l1 = arvore1._add_left(r1, 9)
    d1 = arvore1._add_right(r1, 13)
    arvore1._add_left(l1, 4)
    arvore1._add_right(l1, 5)
    arvore1._add_left(d1, 6)
    arvore1._add_right(d1, 7)

    # árvore que não satisfaz a condição
    arvore2 = LinkedBinaryTree()
    r2 = arvore2._add_root(10)
    l2 = arvore2._add_left(r2, 3)
    arvore2._add_right(r2, 5)
    arvore2._add_left(l2, 1)
    arvore2._add_right(l2, 2)

    # árvore soma simples
    arvore3 = LinkedBinaryTree()
    r3 = arvore3._add_root(10)
    arvore3._add_left(r3, 4)
    arvore3._add_right(r3, 6)

    # árvore com apenas um nó
    arvore4 = LinkedBinaryTree()
    arvore4._add_root(5)

    # árvore vazia
    arvore5 = LinkedBinaryTree()

    print("\nÁrvore 1:", verifica_arvore_soma(arvore1))
    print("Árvore 2:", verifica_arvore_soma(arvore2))
    print("Árvore 3:", verifica_arvore_soma(arvore3))
    print("Árvore 4:", verifica_arvore_soma(arvore4))
    print("Árvore 5:", verifica_arvore_soma(arvore5))


if __name__ == "__main__":
    exercicio_5()
