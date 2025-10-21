# sistema_bibliotecário - IDEP.

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

## Capturas de telas: 

<img width="1728" height="914" alt="Captura de tela 2025-10-21 015905" src="https://github.com/user-attachments/assets/7c5fca73-4d47-4ad7-bb72-5efa4d584a9f" />
<img width="1428" height="871" alt="Captura de tela 2025-10-21 015916" src="https://github.com/user-attachments/assets/65cdba06-820a-447c-843e-7f15694ce351" />
<img width="1373" height="287" alt="Captura de tela 2025-10-21 015928" src="https://github.com/user-attachments/assets/ed73add5-fbfb-4334-b248-7632aeba03af" />
<img width="1386" height="471" alt="Captura de tela 2025-10-21 015952" src="https://github.com/user-attachments/assets/42077b6f-85ed-4adc-b48f-26aee1fdb056" />
<img width="1404" height="446" alt="Captura de tela 2025-10-21 020007" src="https://github.com/user-attachments/assets/9bbebfa3-a460-4428-93e3-f3470dee18f9" />
<img width="1342" height="621" alt="Captura de tela 2025-10-21 020028" src="https://github.com/user-attachments/assets/78b7740e-3526-47f0-ad04-00fb05c311cb" />
