* Para rodar o projeto pelo VSCode

1. Clone o projeto para seu PC - git clone https://github.com/luishcsantos/TCC_Sistema_Estoque.git
2. Crie um ambiente virtual (venv) - python -m venv venv
3. Ative o venv - .\venv\Scripts\activate
4. Instale os requisitos - pip install -r .\requirements.txt
5. Rode o comando `flask run --debug` ou `python app.py` , você poderá acessar a aplicação pelo navegador em `127.0.0.1:5000` ou `localhost:5000`

* Para fazer o APP.exe

Com console:

pyinstaller `
  --onedir `
  --name "Lab" `
  --add-data "templates;templates" `
  --add-data "static;static" `
  --add-data "database\\bancoestoque.db;database" `
  --paths "estoque\\Lib\\site-packages" `
  index.py


Sem console:

pyinstaller `
  --onedir `
  --windowed `
  --name "Lab" `
  --add-data "templates;templates" `
  --add-data "static;static" `
  --add-data "database\\bancoestoque.db;database" `
  --paths "estoque\\Lib\\site-packages" `
  index.py


Depois colamos o database atualizado na pasta database

Caso queira colocar todas as templentes em um file para não dar acesso aos arquivos:

pyinstaller `
  --onefile `
  --name "Lab" `
  --add-data "templates;templates" `
  --add-data "static;static" `
  --paths "estoque\\Lib\\site-packages" `
  index.py

Ou sem o console:

pyinstaller `
  --onefile `
  --windowed `
  --name "Lab" `
  --add-data "templates;templates" `
  --add-data "static;static" `
  --paths "estoque\\Lib\\site-packages" `
  index.py

E colamos o banco na mesma pasta.

Ao executar o .exe, seu PC estará rodando a aplicação da mesma forma que no console. Para fechar basta parar o processo `Lab` pelo gerenciador de tarefas do Windows.