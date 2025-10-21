from .models import Book, User, RoleEnum
from . import db
import random

def popular_exemplos():
    # Limpar tabelas antes de popular (apenas para desenvolvimento)
    try:
        Book.query.delete()
        User.query.delete()
        db.session.commit()
    except:
        db.session.rollback()
    
    # Lista de 10 usuários exemplo
    usuarios = [
        User(nome="João Silva", email="joao@example.com", matricula="1001"),
        User(nome="Maria Souza", email="maria@example.com", matricula="1002"),
        User(nome="Pedro Oliveira", email="pedro@example.com", matricula="1003"),
        User(nome="Ana Santos", email="ana@example.com", matricula="1004"),
        User(nome="Carlos Lima", email="carlos@example.com", matricula="1005"),
        User(nome="Mariana Costa", email="mariana@example.com", matricula="1006"),
        User(nome="Paulo Rocha", email="paulo@example.com", matricula="1007"),
        User(nome="Julia Alves", email="julia@example.com", matricula="1008"),
        User(nome="Ricardo Pereira", email="ricardo@example.com", matricula="1009"),
        User(nome="Fernanda Cardoso", email="fernanda@example.com", matricula="1010")
    ]
    
    for usuario in usuarios:
        usuario.set_password("senha123")
    
    db.session.add_all(usuarios)

    # Lista de 50 livros com títulos reais
    livros = [
        Book(titulo="1984", autores="George Orwell", isbn="978-0-452-28423-4", quantidade=random.randint(1, 10)),
        Book(titulo="Orgulho e Preconceito", autores="Jane Austen", isbn="978-0-14-143951-8", quantidade=random.randint(1, 10)),
        Book(titulo="Dom Quixote", autores="Miguel de Cervantes", isbn="978-0-14-243723-0", quantidade=random.randint(1, 10)),
        Book(titulo="O Pequeno Príncipe", autores="Antoine de Saint-Exupéry", isbn="978-0-15-601398-7", quantidade=random.randint(1, 10)),
        Book(titulo="Harry Potter e a Pedra Filosofal", autores="J.K. Rowling", isbn="978-0-7475-3269-9", quantidade=random.randint(1, 10)),
        Book(titulo="O Senhor dos Anéis", autores="J.R.R. Tolkien", isbn="978-0-618-00222-1", quantidade=random.randint(1, 10)),
        Book(titulo="O Apanhador no Campo de Centeio", autores="J.D. Salinger", isbn="978-0-316-76953-4", quantidade=random.randint(1, 10)),
        Book(titulo="Cem Anos de Solidão", autores="Gabriel García Márquez", isbn="978-0-06-088328-7", quantidade=random.randint(1, 10)),
        Book(titulo="Crime e Castigo", autores="Fiódor Dostoiévski", isbn="978-0-14-305814-4", quantidade=random.randint(1, 10)),
        Book(titulo="O Grande Gatsby", autores="F. Scott Fitzgerald", isbn="978-0-7432-7356-5", quantidade=random.randint(1, 10)),
        Book(titulo="Dom Casmurro", autores="Machado de Assis", isbn="978-85-01-05127-1", quantidade=random.randint(1, 10)),
        Book(titulo="A Moreninha", autores="Joaquim Manuel de Macedo", isbn="978-85-01-05128-8", quantidade=random.randint(1, 10)),
        Book(titulo="Iracema", autores="José de Alencar", isbn="978-85-01-05129-5", quantidade=random.randint(1, 10)),
        Book(titulo="O Cortiço", autores="Aluísio Azevedo", isbn="978-85-01-05130-1", quantidade=random.randint(1, 10)),
        Book(titulo="Memórias Póstumas de Brás Cubas", autores="Machado de Assis", isbn="978-85-01-05131-8", quantidade=random.randint(1, 10)),
        Book(titulo="O Alienista", autores="Machado de Assis", isbn="978-85-01-05132-5", quantidade=random.randint(1, 10)),
        Book(titulo="A Divina Comédia", autores="Dante Alighieri", isbn="978-85-01-05133-2", quantidade=random.randint(1, 10)),
        Book(titulo="Ulisses", autores="James Joyce", isbn="978-85-01-05134-9", quantidade=random.randint(1, 10)),
        Book(titulo="Madame Bovary", autores="Gustave Flaubert", isbn="978-85-01-05135-6", quantidade=random.randint(1, 10)),
        Book(titulo="Em Busca do Tempo Perdido", autores="Marcel Proust", isbn="978-85-01-05136-3", quantidade=random.randint(1, 10)),
        Book(titulo="A Metamorfose", autores="Franz Kafka", isbn="978-85-01-05137-0", quantidade=random.randint(1, 10)),
        Book(titulo="Lolita", autores="Vladimir Nabokov", isbn="978-85-01-05138-7", quantidade=random.randint(1, 10)),
        Book(titulo="A Revolução dos Bichos", autores="George Orwell", isbn="978-85-01-05139-4", quantidade=random.randint(1, 10)),
        Book(titulo="O Nome da Rosa", autores="Umberto Eco", isbn="978-85-01-05140-0", quantidade=random.randint(1, 10)),
        Book(titulo="O Retrato de Dorian Gray", autores="Oscar Wilde", isbn="978-85-01-05141-7", quantidade=random.randint(1, 10)),
        Book(titulo="Drácula", autores="Bram Stoker", isbn="978-85-01-05142-4", quantidade=random.randint(1, 10)),
        Book(titulo="Frankenstein", autores="Mary Shelley", isbn="978-85-01-05143-1", quantidade=random.randint(1, 10)),
        Book(titulo="A Ilha do Tesouro", autores="Robert Louis Stevenson", isbn="978-85-01-05144-8", quantidade=random.randint(1, 10)),
        Book(titulo="As Viagens de Gulliver", autores="Jonathan Swift", isbn="978-85-01-05145-5", quantidade=random.randint(1, 10)),
        Book(titulo="Moby Dick", autores="Herman Melville", isbn="978-85-01-05146-2", quantidade=random.randint(1, 10)),
        Book(titulo="Os Três Mosqueteiros", autores="Alexandre Dumas", isbn="978-85-01-05147-9", quantidade=random.randint(1, 10)),
        Book(titulo="O Conde de Monte Cristo", autores="Alexandre Dumas", isbn="978-85-01-05148-6", quantidade=random.randint(1, 10)),
        Book(titulo="Guerra e Paz", autores="Liev Tolstói", isbn="978-85-01-05149-3", quantidade=random.randint(1, 10)),
        Book(titulo="Anna Kariênina", autores="Liev Tolstói", isbn="978-85-01-05150-9", quantidade=random.randint(1, 10)),
        Book(titulo="Os Irmãos Karamázov", autores="Fiódor Dostoiévski", isbn="978-85-01-05151-6", quantidade=random.randint(1, 10)),
        Book(titulo="O Idiota", autores="Fiódor Dostoiévski", isbn="978-85-01-05152-3", quantidade=random.randint(1, 10)),
        Book(titulo="Hamlet", autores="William Shakespeare", isbn="978-85-01-05153-0", quantidade=random.randint(1, 10)),
        Book(titulo="Romeu e Julieta", autores="William Shakespeare", isbn="978-85-01-05154-7", quantidade=random.randint(1, 10)),
        Book(titulo="Macbeth", autores="William Shakespeare", isbn="978-85-01-05155-4", quantidade=random.randint(1, 10)),
        Book(titulo="A Odisséia", autores="Homero", isbn="978-85-01-05156-1", quantidade=random.randint(1, 10)),
        Book(titulo="A Ilíada", autores="Homero", isbn="978-85-01-05157-8", quantidade=random.randint(1, 10)),
        Book(titulo="O Processo", autores="Franz Kafka", isbn="978-85-01-05158-5", quantidade=random.randint(1, 10)),
        Book(titulo="A Náusea", autores="Jean-Paul Sartre", isbn="978-85-01-05159-2", quantidade=random.randint(1, 10)),
        Book(titulo="O Estrangeiro", autores="Albert Camus", isbn="978-85-01-05160-8", quantidade=random.randint(1, 10)),
        Book(titulo="Admirável Mundo Novo", autores="Aldous Huxley", isbn="978-85-01-05161-5", quantidade=random.randint(1, 10)),
        Book(titulo="Fahrenheit 451", autores="Ray Bradbury", isbn="978-85-01-05162-2", quantidade=random.randint(1, 10)),
        Book(titulo="O Guia do Mochileiro das Galáxias", autores="Douglas Adams", isbn="978-85-01-05163-9", quantidade=random.randint(1, 10)),
        Book(titulo="O Hobbit", autores="J.R.R. Tolkien", isbn="978-85-01-05164-6", quantidade=random.randint(1, 10)),
        Book(titulo="As Crônicas de Nárnia", autores="C.S. Lewis", isbn="978-85-01-05165-3", quantidade=random.randint(1, 10)),
        Book(titulo="O Leão, a Feiticeira e o Guarda-Roupa", autores="C.S. Lewis", isbn="978-85-01-05166-0", quantidade=random.randint(1, 10))
    ]

    db.session.add_all(livros)
    db.session.commit()
    print("Dados de exemplo populados com sucesso!")