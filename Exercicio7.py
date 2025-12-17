from linkedBinaryTree import LinkedBinaryTree


def buscar_ancestrais(arvore, valor):
    # se a árvore estiver vazia, não há ancestrais
    if len(arvore) == 0:
        return []

    lista_ancestrais = []
    achou = procura_no(arvore.root(), arvore, valor, lista_ancestrais)

    if not achou:
        return []

    return lista_ancestrais


def procura_no(no, arvore, valor, lista_ancestrais):
    if no is None:
        return False

    # se encontrou o nó procurado
    if no.element() == valor:
        return True

    # procura nas subárvores esquerda e direita
    encontrou_esq = procura_no(arvore.left(no), arvore, valor, lista_ancestrais)
    encontrou_dir = procura_no(arvore.right(no), arvore, valor, lista_ancestrais)

    # se o valor foi encontrado em algum filho, o nó atual é ancestral
    if encontrou_esq or encontrou_dir:
        lista_ancestrais.append(no.element())
        return True

    return False


def exercicio_7():
    print("\n" + "-" * 60)
    print("Exercício 7 - Ancestrais de um nó")
    print("-" * 60)

    # árvore do exemplo
    arvore1 = LinkedBinaryTree()
    r = arvore1._add_root(1)
    n2 = arvore1._add_left(r, 2)
    n3 = arvore1._add_right(r, 3)
    arvore1._add_left(n2, 4)
    n5 = arvore1._add_right(n2, 5)
    n6 = arvore1._add_left(n3, 6)
    n7 = arvore1._add_right(n3, 7)
    arvore1._add_left(n6, 8)
    arvore1._add_right(n7, 9)

    print("\nÁrvore:")
    print("         1")
    print("        / \\")
    print("       2   3")
    print("      / \\  / \\")
    print("     4  5 6   7")
    print("        /     \\")
    print("       8       9\n")

    testes = [9, 6, 5]

    for v in testes:
        ancestrais = buscar_ancestrais(arvore1, v)
        if ancestrais:
            print(f"Os ancestrais do nó {v} são {', '.join(map(str, ancestrais))}.")
        else:
            print(f"O nó {v} não foi encontrado ou não possui ancestrais.")

    # caso da raiz
    print(f"\nAncestrais do nó 1: {buscar_ancestrais(arvore1, 1)}")

    # nó que não existe
    print(f"Ancestrais do nó 100: {buscar_ancestrais(arvore1, 100)}")

    # outra árvore para teste
    arvore2 = LinkedBinaryTree()
    r2 = arvore2._add_root(10)
    n5_2 = arvore2._add_left(r2, 5)
    arvore2._add_right(r2, 15)
    arvore2._add_left(n5_2, 3)

    print("\nOutra árvore:")
    print("       10")
    print("      /  \\")
    print("     5    15")
    print("    /")
    print("   3")

    print(f"\nAncestrais do nó 3: {', '.join(map(str, buscar_ancestrais(arvore2, 3)))}")
    print(f"Ancestrais do nó 15: {', '.join(map(str, buscar_ancestrais(arvore2, 15)))}")


if __name__ == "__main__":
    exercicio_7()
