### Management App

Um app para gerenciamento de dados para pequenos empreendedores.
- ([x]) Gerenciamento de Clientes
- ([x]) Gerenciamento de Registros
- ([x]) Agenda
- ([x]) Gerenciamento fianceiro

### Em breve - 01/07/2025
#### Refatorando o frontend

Para instalação local o camando de execução é...
#### Geral:
git clone https://github.com/NeatlySimplify/ManagementApp.git
cd ManagementApp

#### Com Pip
python3 -m venv venv
source venv/bin/activate   <!-- Linux/macOS -->
.\venv\Scripts\activate     <!-- Windows -->

#### Com Poetry
poetry install <!-- Recomendado -->
<!-- Se não tiver instalado recomendo a instalação do Poetry usando Pipx -->

### Executar
uvicorn src.main:app --reload
