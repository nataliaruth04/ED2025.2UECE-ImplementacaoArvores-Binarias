from linkedBinaryTree import LinkedBinaryTree


def imprimir_caminhos(arvore):
    # se a árvore estiver vazia, não há caminhos
    if len(arvore) == 0:
        print("Árvore vazia")
        return

    caminho_atual = []
    percorre(arvore.root(), arvore, caminho_atual)


def percorre(no, arvore, caminho_atual):
    if no is None:
        return

    # adiciona o nó atual ao caminho
    caminho_atual.append(no.element())

    # se for folha, imprime o caminho completo
    if arvore.num_children(no) == 0:
        print(" -> ".join(map(str, caminho_atual)))
    else:
        # continua descendo pela esquerda e direita
        percorre(arvore.left(no), arvore, caminho_atual)
        percorre(arvore.right(no), arvore, caminho_atual)

    # remove o último elemento para voltar na recursão
    caminho_atual.pop()


def exercicio_6():
    print("\n" + "-" * 60)
    print("Exercício 6 - Caminhos da raiz até as folhas")
    print("-" * 60)

    # árvore do exemplo do enunciado
    arvore1 = LinkedBinaryTree()
    r = arvore1._add_root(1)
    n2 = arvore1._add_left(r, 2)
    n3 = arvore1._add_right(r, 3)
    arvore1._add_left(n2, 4)
    arvore1._add_right(n2, 5)
    n6 = arvore1._add_left(n3, 6)
    n7 = arvore1._add_right(n3, 7)
    arvore1._add_left(n6, 8)
    arvore1._add_right(n7, 9)

    print("\nÁrvore 1 - Caminhos:")
    imprimir_caminhos(arvore1)

    # árvore simples
    arvore2 = LinkedBinaryTree()
    r2 = arvore2._add_root(10)
    arvore2._add_left(r2, 5)
    arvore2._add_right(r2, 15)

    print("\nÁrvore 2 - Caminhos:")
    imprimir_caminhos(arvore2)

    # árvore com apenas um nó
    arvore3 = LinkedBinaryTree()
    arvore3._add_root(42)

    print("\nÁrvore 3 - Caminhos:")
    imprimir_caminhos(arvore3)

    # árvore vazia
    arvore4 = LinkedBinaryTree()

    print("\nÁrvore 4 - Caminhos:")
    imprimir_caminhos(arvore4)


if __name__ == "__main__":
    exercicio_6()
