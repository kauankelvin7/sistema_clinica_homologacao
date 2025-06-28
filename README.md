# Sistema de Homologação de Atestados Médicos

## Visão Geral

O Sistema de Homologação de Atestados Médicos é uma aplicação desktop desenvolvida em Python com framework PyQt5, destinada à automação e otimização do processo de declaração e homologação de atestados médicos em ambientes clínicos e administrativos.

A solução oferece preenchimento automatizado de documentos padronizados, armazenamento local de dados para reutilização e interface intuitiva para maximizar a eficiência operacional.

## Recursos Principais

### Gestão de Dados
- **Entrada de dados estruturada** com validação de campos obrigatórios
- **Armazenamento local** em banco SQLite para dados de pacientes e médicos
- **Preenchimento automático** baseado em histórico de registros
- **Formatação inteligente** de CPF e outros campos específicos

### Geração de Documentos
- **Preenchimento automatizado** de modelos DOCX pré-configurados
- **Abertura automática** do documento gerado no editor padrão
- **Padronização** de layout e formatação dos atestados

### Interface e Usabilidade
- **Design responsivo** com adaptação a diferentes resoluções
- **Feedback em tempo real** através de barra de status
- **Organização intuitiva** em seções funcionais
- **Consulta online** integrada para validação de registros profissionais

### Distribuição
- **Executável standalone** para implantação sem dependências
- **Portabilidade** para diferentes ambientes Windows

## Arquitetura Técnica

### Stack Tecnológico
| Componente | Tecnologia | Propósito |
|------------|------------|-----------|
| Interface Gráfica | PyQt5 | Framework GUI principal |
| Processamento de Documentos | python-docx | Manipulação de arquivos DOCX |
| Banco de Dados | SQLite3 | Armazenamento local |
| Empacotamento | PyInstaller | Geração de executável |
| Processamento de Imagens | Pillow (PIL) | Manipulação de ícones e assets |

### Estrutura de Dados
- **Tabela Pacientes**: Nome, CPF, Cargo, Empresa
- **Tabela Médicos**: Nome, Tipo de Registro, Número, UF
- **Tabela Atestados**: CID, Data, Dias de Afastamento

## Instalação e Configuração

### Pré-requisitos
- Python 3.8 ou superior
- Sistema operacional Windows (recomendado)
- Privilégios de administrador para instalação de dependências

### Configuração do Ambiente de Desenvolvimento

1. **Clone do Repositório**
   ```bash
   git clone https://github.com/kauankelvin7/sistema_clinica_homologacao
   cd SistemaHomologacaoAtestado
   ```

2. **Criação do Ambiente Virtual**
   ```bash
   python -m venv .venv
   
   # Windows PowerShell
   .\.venv\Scripts\Activate.ps1
   
   # Windows CMD
   .venv\Scripts\activate.bat
   
   # Linux/macOS
   source .venv/bin/activate
   ```

3. **Instalação de Dependências**
   ```bash
   pip install -r requirements.txt
   pip install Pillow  # Para suporte a ícones
   ```

### Configuração de Assets

1. **Estrutura de Diretórios**
   ```
   projeto/
   ├── models/
   │   └── modelo homologação.docx
   ├── assets/
   │   └── app_logo.png (ou .ico)
   ├── data/
   │   └── homologacao.db (criado automaticamente)
   └── main.py
   ```

2. **Preparação de Arquivos**
   - Coloque o modelo DOCX na pasta `models/`
   - Adicione o logo/ícone na pasta `assets/`
   - Verifique a correspondência de nomes no código

### Execução

```bash
python main.py
```

## Geração de Executável

### Processo de Build

```powershell
pyinstaller `
    --noconsole `
    --onefile `
    --icon="assets/app_logo.ico" `
    --add-data "models;models" `
    --add-data "data\homologacao.db;data" `
    --add-data "data\generated_documents;data\generated_documents" `
    --add-data "assets;assets" `
    "main.py"
```

### Parâmetros de Configuração
- `--noconsole`: Execução sem janela de console
- `--onefile`: Empacotamento em arquivo único
- `--icon`: Ícone personalizado da aplicação
- `--add-data`: Inclusão de arquivos de dados e assets

### Distribuição
O executável gerado estará disponível em `dist/main.exe` e pode ser distribuído independentemente.

## Funcionalidades Detalhadas

### Campos de Entrada
| Campo | Tipo | Validação | Observações |
|-------|------|-----------|-------------|
| Nome do Paciente | Texto | Obrigatório | Auto-completar disponível |
| CPF | Texto | Formato XXX.XXX.XXX-XX | Formatação automática |
| Cargo | Texto | Opcional | Histórico mantido |
| Empresa | Texto | Opcional | Histórico mantido |
| CID | Texto | Obrigatório | Código de classificação |
| Data do Atestado | Data | Obrigatório | Formato DD/MM/AAAA |
| Dias de Afastamento | Número | Obrigatório | Valor inteiro positivo |
| Nome do Médico | Texto | Obrigatório | Auto-completar disponível |
| Tipo de Registro | Lista | CRM/CRO/RM | Seleção única |
| Número de Registro | Texto | Obrigatório | Validação numérica |
| UF | Lista | Estados brasileiros | Seleção única |

### Operações Avançadas
- **Consulta Online**: Integração com sites de conselhos profissionais
- **Backup Automático**: Cópia de segurança do banco de dados
- **Histórico de Documentos**: Registro de todos os atestados gerados
- **Validação de Dados**: Verificação de integridade antes da geração

## Troubleshooting

### Problemas Comuns

**Erro de Dependências**
```bash
pip install --upgrade pip
pip install -r requirements.txt --force-reinstall
```

**Problema de Banco de Dados**
```bash
# Remover banco corrompido
del data\homologacao.db
# Executar aplicação para recriar
python main.py
```

**Erro de Modelo DOCX**
- Verificar se o arquivo existe em `models/`
- Confirmar permissões de leitura
- Validar formato do documento

## Contribuição

### Diretrizes para Desenvolvimento
1. **Padrões de Código**: Seguir PEP 8 para Python
2. **Documentação**: Documentar funções e classes
3. **Testes**: Incluir testes unitários quando aplicável
4. **Versionamento**: Usar semantic versioning

### Processo de Contribuição
1. Fork do repositório
2. Criação de branch para feature (`git checkout -b feature/nova-funcionalidade`)
3. Commit das alterações (`git commit -am 'Adiciona nova funcionalidade'`)
4. Push para o branch (`git push origin feature/nova-funcionalidade`)
5. Criação de Pull Request

### Reportar Issues
- Usar o template de issue do GitHub
- Incluir logs de erro quando relevante
- Especificar ambiente de execução
- Fornecer passos para reprodução

## Suporte e Contato

Para suporte técnico, dúvidas ou sugestões:
- **Issues**: [GitHub Issues](https://github.com/kauankelvin7/sistema_clinica_homologacao/issues)
- **Documentação**: Consulte este documento e comentários no código
- **Atualizações**: Acompanhe o repositório para novas versões

## Licença

Este projeto está licenciado sob a MIT License. Consulte o arquivo `LICENSE.md` para detalhes completos sobre termos de uso, distribuição e modificação.

---

**Versão da Documentação**: 1.0  
**Última Atualização**: Junho 2025  
**Compatibilidade**: Python 3.8+, Windows 10+
