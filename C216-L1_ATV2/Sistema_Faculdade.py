alunos = []
contador_cursos = {}

def gerar_matricula(curso):
    if curso not in contador_cursos:
        contador_cursos[curso] = 1
    else:
        contador_cursos[curso] += 1
    return f"{curso}{contador_cursos[curso]}"

def criar_aluno():
    nome = input("Nome: ")
    email = input("Email: ")
    curso = input("Curso: ").upper()
    matricula = gerar_matricula(curso)
    aluno = {"nome": nome, "email": email, "curso": curso, "matricula": matricula}
    alunos.append(aluno)
    print(f"Aluno cadastrado! Matrícula: {matricula}")

def listar_alunos():
    if not alunos:
        print("Nenhum aluno cadastrado.")
        return
    for aluno in alunos:
        print(aluno)

def atualizar_aluno():
    mat = input("Matrícula: ")
    for aluno in alunos:
        if aluno["matricula"] == mat:
            aluno["nome"] = input("Novo nome: ")
            aluno["email"] = input("Novo email: ")
            print("Atualizado!")
            return
    print("Aluno não encontrado.")

def deletar_aluno():
    mat = input("Matrícula: ")
    for aluno in alunos:
        if aluno["matricula"] == mat:
            alunos.remove(aluno)
            print("Removido!")
            return
    print("Aluno não encontrado.")

def menu():
    while True:
        print("\n1-Criar 2-Listar 3-Atualizar 4-Deletar 5-Sair")
        op = input("Escolha: ")
        if op == "1": criar_aluno()
        elif op == "2": listar_alunos()
        elif op == "3": atualizar_aluno()
        elif op == "4": deletar_aluno()
        elif op == "5": break
        else: print("Opção inválida!")

menu()