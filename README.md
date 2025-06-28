Sistema de Homologação de Atestados Médicos

📋 Descrição do Projeto
O Sistema de Homologação de Atestados Médicos é uma aplicação desktop desenvolvida em Python com PyQt5, projetada para otimizar o processo de declaração e homologação de atestados médicos. Ele automatiza o preenchimento de documentos padronizados com dados de pacientes e médicos, armazenando essas informações localmente para facilitar futuras operações de preenchimento automático. O sistema oferece uma interface de usuário intuitiva e aprimorada esteticamente para uma experiência eficiente.

✨ Funcionalidades
Entrada de Dados Simplificada: Interface clara para inserção de Nome do Paciente, CPF, Cargo, Empresa, CID do Atestado, Data do Atestado, Dias de Afastamento, Nome do Médico, Tipo de Registro (CRM, CRO, RMs), Número de Registro e UF.

Preenchimento Automático Inteligente: Armazena dados de pacientes e médicos no banco de dados SQLite local. Ao digitar nomes ou CPFs/registros, o sistema sugere e preenche automaticamente os campos relacionados, agilizando o processo.

Formatação de CPF: O campo de CPF na interface formata automaticamente a entrada para ###.###.###-##.

Geração de Documentos DOCX: Preenche um modelo de documento .docx pré-existente com os dados inseridos, gerando uma declaração formatada e pronta para uso.

Abertura Automática do Documento: Após a geração, o documento .docx é aberto imediatamente no editor padrão do sistema.

Consulta Online (Híbrida): Um botão "Consultar Online" permite abrir o navegador na página de consulta do conselho correspondente (CRM, CRO, etc.), facilitando a validação manual dos registros (devido à presença de CAPTCHA e formulários POST em sites oficiais).

Interface Amigável e Otimizada: Design com cores suaves, botões intuitivos, organização em seções e barra de status para feedback em tempo real.

Responsividade Básica: Utiliza QScrollArea e QGridLayout para melhor adaptação a diferentes tamanhos de janela, com largura máxima de conteúdo para legibilidade.

Executável Distribuível: Pode ser empacotado como um único arquivo executável para fácil distribuição em outros computadores, sem a necessidade de instalação do Python.

🚀 Tecnologias Utilizadas
Python 3.x

PyQt5: Para a construção da interface gráfica do usuário (GUI).

python-docx: Para manipulação e preenchimento de documentos .docx.

SQLite3: Banco de dados leve e embarcado para armazenamento local de dados de pacientes e médicos.

PyInstaller: Para empacotar a aplicação em um executável.

Pillow (PIL): Biblioteca de processamento de imagens, utilizada pelo PyInstaller para manipular ícones.

⚙️ Instalação e Execução (Ambiente de Desenvolvimento)
Siga estas instruções para configurar e executar o sistema em seu ambiente de desenvolvimento.

Pré-requisitos
Python 3.x instalado (recomenda-se Python 3.8+).

Passo a Passo
Clone o Repositório (ou Baixe o Código):

Bash

git clone (https://github.com/kauankelvin7/sistema_clinica_homologacao)
cd SistemaHomologacaoAtestado
(Se você não usa Git, basta baixar a pasta do projeto e navegar até ela via terminal).

Crie e Ative um Ambiente Virtual (Recomendado):
É uma boa prática isolar as dependências do projeto.

Bash

python -m venv .venv
Windows (PowerShell):

PowerShell

.\.venv\Scripts\Activate.ps1
Windows (CMD):

DOS

.venv\Scripts\activate.bat
Linux/macOS:

Bash

source .venv/bin/activate
Instale as Dependências:
Com o ambiente virtual ativado, instale as bibliotecas necessárias:

Bash

pip install -r requirements.txt
# Certifique-se de que Pillow também está instalado para o PyInstaller
pip install Pillow
Se o requirements.txt não tiver Pillow ou pyinstaller, adicione e reinstale:

PyQt5
python-docx
Pillow
pyinstaller
Prepare os Arquivos Essenciais:

Crie uma pasta models/ na raiz do projeto e coloque seu arquivo de modelo modelo homologação.docx dentro dela.

Crie uma pasta assets/ na raiz do projeto e coloque seu arquivo de logo (ex: app_logo.png ou app_icon.ico) dentro dela. Certifique-se de que o nome do arquivo no código (ui/main_window.py) corresponde ao nome do seu arquivo.

Inicialize o Banco de Dados:
A primeira vez que você executar a aplicação, ele criará automaticamente o arquivo homologacao.db na pasta data/ com a estrutura das tabelas. Se você já tinha um banco de dados SQLite e alterou a estrutura das tabelas (medicos), pode ser necessário deletar o data/homologacao.db para que a nova estrutura seja criada.

Bash

# Opcional: Se precisar recriar o banco de dados
# Remove-Item -Path "data/homologacao.db" -ErrorAction SilentlyContinue # PowerShell
# ou
# del data\homologacao.db # CMD
Execute o Sistema:
Com o ambiente virtual ativado, execute o script principal:

Bash

python main.py
📦 Gerando um Executável
Para criar uma versão independente do seu aplicativo que pode ser executada em outros PCs sem a instalação do Python, utilize o PyInstaller.

Certifique-se de que o PyInstaller e Pillow estão instalados no seu ambiente virtual (veja o passo 3 da instalação).

Navegue até a pasta raiz do projeto no seu terminal (com o ambiente virtual ativado).

Execute o comando PyInstaller:

PowerShell

pyinstaller `
    --noconsole `
    --onefile `
    --icon="assets/app_logo.ico" `  # Substitua pelo caminho real do seu arquivo .ico
    --add-data "models;models" `
    --add-data "data\homologacao.db;data" `
    --add-data "data\generated_documents;data\generated_documents" `
    --add-data "assets;assets" `
    "main.py"
Importante: Use o acento grave ( ` ) para quebrar as linhas no PowerShell. Se estiver no CMD, use o circunflexo ( ^ ). Ou, para simplificar, digite todo o comando em uma única linha.

Certifique-se de que assets/app_logo.ico é o nome correto do seu arquivo de ícone.

Localize o Executável:
O executável (main.exe no Windows) será gerado na pasta dist/ dentro do seu projeto.

Teste o Executável:
Copie o main.exe (e, se não usar --onefile, a pasta dist inteira) para outro computador e execute-o.

🤝 Contribuição
Se você tiver sugestões para melhorias, sinta-se à vontade para:

Abrir uma Issue descrevendo a sugestão ou bug.

Criar um Pull Request com as suas modificações.

## 📄 Licença

Este projeto está licenciado sob a [MIT License](LICENSE.md) - veja o arquivo LICENSE.md para detalhes.