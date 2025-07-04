### Management App

Um app para gerenciamento de dados para pequenos empreendedores.
- ([x]) Gerenciamento de Clientes
- ([x]) Gerenciamento de Registros
- ([x]) Agenda
- ([x]) Gerenciamento fianceiro

## Em breve - 03/07/2025 às 23:59
# <span>Movendo a authenticação do backend para uma solução integrada ao banco de dados</span>

<p>Para instalação local o camando de execução é...</p>

### Geral:
<p>git clone https://github.com/NeatlySimplify/ManagementApp.git </p>
<p>cd ManagementApp </p>

#### Com Pip
<p>python3 -m venv venv</p>
<p>source venv/bin/activate   <!-- Linux/macOS --></p>
<p>.\venv\Scripts\activate     <!-- Windows --> </p>

#### Com Poetry
<p>poetry install <!-- Recomendado --> </p>
<p><!-- Se não tiver instalado recomendo a instalação do Poetry usando Pipx --> </p>


### A Database Gel
#### Instale a cli da database:
<p>https://docs.geldata.com/learn/installation</p>

#### Após instalação, na pasta BAckEnd digite:
<p>gel project init</p>
<p>gel</p>

#### Insira a query:
<p>insert Administrator{name:= "Seu nome de usuário", email:="Qualquer email", password:="Alguma senha"}</p>

<p>Copie e cole a resposta da query no seu arquivo .env dentro de BackEnd, o nome da variável é "ADMIN_ID"</p>
<p>No momento eu não fiz um UI para administradores como controle de usuários então este email e senha não precisão ser válidos, sómente precisão existir. O tipo administrador é uma base para fazeer outras queries.</p>

#### Crie um texto aleátorio para usar na criação do JWT Token, pode ser usando openssl ou um criador de hex online:
<p>openssl rand -hex 64</p>
<p>Copie e cole o hex no arqivo .env com o nome "SECRET"</p>

### Executar
<p>uvicorn src.main:app --reload </p>

