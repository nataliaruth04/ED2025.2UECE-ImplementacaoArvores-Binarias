from linkedBinaryTree import LinkedBinaryTree


def transformar_em_arvore_soma(arvore):
    # se a árvore estiver vazia, não faz nada
    if len(arvore) == 0:
        return

    soma_subarvore(arvore.root(), arvore)


def soma_subarvore(no, arvore):
    if no is None:
        return 0

    # se for folha, guarda o valor antigo e substitui por 0
    if arvore.num_children(no) == 0:
        valor_antigo = no.element()
        arvore.replace(no, 0)
        return valor_antigo

    # calcula a soma das subárvores esquerda e direita
    soma_esq = soma_subarvore(arvore.left(no), arvore)
    soma_dir = soma_subarvore(arvore.right(no), arvore)

    valor_antigo = no.element()

    # novo valor do nó é a soma das subárvores
    arvore.replace(no, soma_esq + soma_dir)

    # retorna a soma total incluindo o valor antigo
    return valor_antigo + soma_esq + soma_dir


def imprimir_inorder(arvore):
    if len(arvore) == 0:
        print("Árvore vazia")
        return

    resultado = []
    coleta_inorder(arvore.root(), arvore, resultado)
    print(" ".join(map(str, resultado)))


def coleta_inorder(no, arvore, resultado):
    if no is None:
        return

    coleta_inorder(arvore.left(no), arvore, resultado)
    resultado.append(no.element())
    coleta_inorder(arvore.right(no), arvore, resultado)


def exercicio_8():
    print("\n" + "-" * 60)
    print("Exercício 8 - Conversão para Árvore Soma")
    print("-" * 60)

    # árvore do exemplo
    arvore1 = LinkedBinaryTree()
    r = arvore1._add_root(1)
    n2 = arvore1._add_left(r, 2)
    n3 = arvore1._add_right(r, 3)
    arvore1._add_right(n2, 4)
    n5 = arvore1._add_left(n3, 5)
    arvore1._add_right(n3, 6)
    arvore1._add_left(n5, 7)
    arvore1._add_right(n5, 8)

    print("\nÁrvore original (inorder):")
    imprimir_inorder(arvore1)

    transformar_em_arvore_soma(arvore1)

    print("\nÁrvore soma (inorder):")
    imprimir_inorder(arvore1)

    # segunda árvore
    print("\n" + "-" * 40)
    arvore2 = LinkedBinaryTree()
    r2 = arvore2._add_root(10)
    arvore2._add_left(r2, 5)
    arvore2._add_right(r2, 15)

    print("\nÁrvore 2 original (inorder):")
    imprimir_inorder(arvore2)

    transformar_em_arvore_soma(arvore2)

    print("\nÁrvore 2 soma (inorder):")
    imprimir_inorder(arvore2)

    # árvore com um nó
    print("\n" + "-" * 40)
    arvore3 = LinkedBinaryTree()
    arvore3._add_root(42)

    print("\nÁrvore 3 original (inorder):")
    imprimir_inorder(arvore3)

    transformar_em_arvore_soma(arvore3)

    print("\nÁrvore 3 soma (inorder):")
    imprimir_inorder(arvore3)


if __name__ == "__main__":
    exercicio_8()
