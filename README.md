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
  --name "App" `
  --add-data "templates;templates" `
  --add-data "static;static" `
  --add-data "database\\database.db;database" `
  --paths "estoque\\Lib\\site-packages" `
  app.py


Sem console:

pyinstaller `
  --onedir `
  --windowed `
  --name "App" `
  --add-data "templates;templates" `
  --add-data "static;static" `
  --add-data "database\\database.db;database" `
  --paths "estoque\\Lib\\site-packages" `
  app.py


Depois colamos o database atualizado na pasta database dentro de dist/App (pasta criada após a criação do .exe)
Quando executar o App.exe, o sistema estará rodando no seu localhost, sendo acessível por outros dispositivos em sua rede também.

Caso queira colocar todas as templentes em um file para não dar acesso aos arquivos:

pyinstaller `
  --onefile `
  --name "App" `
  --add-data "templates;templates" `
  --add-data "static;static" `
  --paths "estoque\\Lib\\site-packages" `
  app.py

Ou sem o console:

pyinstaller `
  --onefile `
  --windowed `
  --name "App" `
  --add-data "templates;templates" `
  --add-data "static;static" `
  --paths "estoque\\Lib\\site-packages" `
  app.py

E colamos o banco na mesma pasta.

Ao executar o .exe, seu PC estará rodando a aplicação da mesma forma que no console. Para fechar basta parar o processo `App` pelo gerenciador de tarefas do Windows.

* Para rodar o sistema como serviço no Windows

1. Vá até a pasta nssm-2.24, depois em win32 ou win64 e abra o prompt de comando como administrador.
2. Use o comando `nssm install AppService`, irá abrir a janela do NSSM.
3. Em application path selecione o App.exe criado anteriormente.
4. Depois na aba "Details", insira um nome de exibição em "Display name" e pode inserir uma descrição também.

Desta forma o sistema já estará rodando normalmente. Note que se reiniciar seu computador, ele vai iniciar junto com o Windows.

* Se quiser excluir o serviço

1. Abra o prompt de comando como administrador
2. Use o comando `sc delete AppService`