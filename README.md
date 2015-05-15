# AgendaTCC

O AgendaTCC é um projeto para a adaptação de um sistema existente (TCCWeb) para que o mesmo se torne acessível a usuários com deficiências, além de inserir capacidades extras.

O Sistema
=========

O Sistema é dividido em duas partes. O Backend é a parte que fica no servidor e faz todo o processamento e gerencia os dados. O Frontend, consiste na interface do usuário com o Backend (o site).

Backend
-------

O desenolvimento do Backend é realizado através da framework Django 1.5 com as dependencias citadas abaixo, em Python 2.7.6.

O Projeto possui diversos um aplicativos, presentes no diretório "apps". Dentro de cada aplicativo, existem 3 arquivos principais:

#### models.py

Um ORM para definição do modelo relacional a ser utilizado pelo SGBD para a construção do BD. Todos os modelos estão descritos neste arquivo e são necessários tanto para a criação dos mesmo pelo SGBD quanto para o uso por parte da framework do Django.

#### urls.py

Este arquivo contêm todas as URL's do aplicativo, e linka cada uma delas a uma view. Todas as urls do site são definidas nestes arquivo.

#### views.py

Neste arquivo estão definidas todas as views. Cada view é responsável por interpretar um pedido, autenticar o usuário e retornar o conteúdo requerido caso o usuário tenha permissões ou retornar os devidos erros caso o usuário não tenha permissão ou não esteja autenticado.


Frontend
--------

O site será sendo desenvolvido em HTML5, CSS3 e javascript (com auxilio de JQuery) além de outras frameworks para acessibilidade.

Os templates em html podem ser encontrados em no diretório "templates".

Os arquivos estáticos de CSS e Javascript podem ser encontrados em "static".

Instalação e Uso
================

Para instalar a utilizar o sistema, recomenda-se o uso de virtual environments - ambientes virtuais, nos quais todas as dependencias são instaladas sem a necessidade de permissão do root. Para tal, é necessário criar um ambiente virtual, acessá-lo e instalar no mesmo todas as dependencias necessárias (como indicado no pórixmo passo).

Desta forma, são necessários os seguintes passos para a instalação e manuseio do ambiente virtual:

```shell
#Instalar pip install. 
#Aqui utilizo o comando apt-get considerando que estamos num ambiente Ubuntu
#Também considero que apt-get e python 2.7 já estão presentes no sistema
sudo apt-get install python-pip python-dev build-essential
sudo pip install --updgrade pip

#Instalar virtualenv
sudo pip install virtualenv

#Criar um virtualenv chamado de 'env'
virtualenv env

#Acessar o virtualenv
source env/bin/activate

#Sair do virtualenv
deactivate
```

Dependências
------------

Após a instalação do ambiente, deverão ser instaladas as dependências:

* Todas as dependencias estão descritas em requirements.txt
```shell
#Acessar o virtualenv
source env/bin/activate

pip install -r requirements.txt
```

Gerenciando o Banco de Dados
---------------------------



Executando o Sistema
--------------------

Para uso do sistema (em modo de testes) são necessários os seguintes passos, considerando que o ambiente virtual e as dependencias já estão instalados:

```shell
#Acessar o virtualenv
source env/bin/activate

#Execução do sistema em modo de testes
python manage.py runserver
```

Este método de rodar o servidor NÃO deverá ser utilizado durante fase de produção, conforme a própria equipe do Django diz.



