# sistema_biblioteca_mark_mesquita

Versão local e educativa de um sistema de biblioteca para atender o projeto do curso Análise e Projeto de Sistemas - TURMA 1
Prof. Me. Rafael Santos - 13/10 A 04/11/2025 desenvolvido em python & Flask.

## Como executar (local)
1. Criar e ativar virtualenv:
   - Windows:
     ```
     python -m venv venv
     venv\Scripts\activate
     ```
   - Linux/macOS:
     ```
     python -m venv venv
     source venv/bin/activate
     ```

2. Instalar dependências:
```
pip install -r requirements.txt
```

3. Rodar a aplicação:
```
python run.py
```

4. Acesse em: http://127.0.0.1:5000

## Credenciais padrão
Admin / bibliotecário:
- E-mail: admin@example.com
- Senha: admin123
Usuario comum:
- E-mail: ana@example.com
- Senha: senha123

O banco SQLite será criado automaticamente e exemplos serão populados na primeira execução para fins de demostração, os nomes de livros são reais e populares, os usuarios são todos ficticios e a senhas para todos é "senha123"

Caso dê pau na hora do login, tenha certeza de ter compilado e instado o modulo: de autenticação.

Para corrigir isso, basta instalar o pacote email_validator no ambiente onde está rodando seu projeto Flask. Execute no terminal dentro da pasta do projeto, com o ambiente virtual ativado, o comando:
pip install email_validator

Se quiser garantir outras dependências recomendadas, pode também instalar com o extra do WTForms assim:
pip install wtforms[email]