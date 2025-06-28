from PyQt5.QtWidgets import (
    QMainWindow, QVBoxLayout, QHBoxLayout, QWidget,
    QLabel, QLineEdit, QPushButton, QMessageBox,
    QDateEdit, QComboBox, QCompleter, QStatusBar, QSpacerItem, QSizePolicy, QFrame,
    QGridLayout, QScrollArea # Adicionado QScrollArea
)
from PyQt5.QtCore import Qt, QDate, QStringListModel, QUrl
from PyQt5.QtGui import QFont, QIntValidator, QIcon, QPixmap # Adicionado QPixmap para imagem
from PyQt5.Qt import QDesktopServices
import os
import sys # Necessário para sys._MEIPASS

# Importa os módulos de negócio e banco de dados
from core.database import get_db_connection
from core.document_generator import generate_document

# --- Função auxiliar para lidar com caminhos de recursos no PyInstaller ---
def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    try:
        # PyInstaller cria uma pasta temporária e armazena o caminho em _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        # Em ambiente de desenvolvimento, o caminho base é o diretório atual do script
        # Assumimos que o script está na raiz do projeto ou em um nível abaixo (e.g., ui/)
        base_path = os.path.abspath(os.path.dirname(sys.argv[0]))
    return os.path.join(base_path, relative_path)

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Sistema de Homologação de Atestados Médicos")
        # Definindo um tamanho inicial e mínimo maior para melhor visualização
        self.setGeometry(100, 100, 900, 750)
        self.setMinimumSize(850, 700) 

        self.is_autofilling = False

        # Configurar a barra de status
        self._statusBar = QStatusBar()
        self.setStatusBar(self._statusBar)
        self.update_status("Sistema pronto.")

        # --- Adicionar o ícone da janela ---
        # O PyInstaller usa o --icon= argument, mas para a janela em si
        # precisamos definir programaticamente.
        # Certifique-se que 'assets/app_icon.ico' ou 'assets/app_logo.png' existe.
        try:
            icon_path_for_window = resource_path("assets/app_logo.ico") # Ou app_icon.ico
            if not QPixmap(icon_path_for_window).isNull():
                self.setWindowIcon(QIcon(icon_path_for_window))
            else:
                print(f"Aviso: Ícone da janela não carregado. Pixmap nulo para: {icon_path_for_window}")
        except Exception as e:
            print(f"Erro ao definir ícone da janela: {e}")
            # Continua sem ícone se houver erro
            pass 

        self.init_ui()
        self.apply_stylesheet()
        self.setup_completers()


    def init_ui(self):
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        # --- QScrollArea para Responsividade ---
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True) 
        scroll_area.setHorizontalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        scroll_area.setVerticalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        scroll_area.setFrameShape(QFrame.NoFrame) 
        
        scroll_widget = QWidget() # Widget que será rolado
        scroll_area.setWidget(scroll_widget)
        
        # Layout principal do scroll_widget
        main_layout = QVBoxLayout(scroll_widget)
        main_layout.setContentsMargins(20, 20, 20, 20)
        main_layout.setSpacing(0) 

        # --- Header com Logo e Título Principal ---
        header_widget = self.create_header()
        main_layout.addWidget(header_widget)
        main_layout.addSpacing(30) 

        # --- Container Centralizado para o Conteúdo do Formulário ---
        # Este container terá uma largura máxima para que o formulário não se estique infinitamente
        content_container = QWidget()
        content_container.setObjectName("contentContainer")
        content_container.setMaximumWidth(800)  # Largura máxima para melhor legibilidade
        content_container.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Preferred) # Força largura fixa, altura preferencial
        
        content_layout = QVBoxLayout(content_container)
        content_layout.setContentsMargins(0, 0, 0, 0) 
        content_layout.setSpacing(25) 

        # --- Seções do Formulário (criadas por funções auxiliares) ---
        content_layout.addWidget(self.create_patient_section())
        content_layout.addWidget(self.create_certificate_section())
        content_layout.addWidget(self.create_doctor_section())
        content_layout.addStretch() # Empurra o conteúdo para o topo

        # --- Botões Principais ---
        button_widget = self.create_buttons()
        content_layout.addWidget(button_widget)
        content_layout.addSpacing(20)

        # Centralizar o 'content_container' dentro do 'main_layout'
        container_layout = QHBoxLayout()
        container_layout.addStretch() # Espaço flexível à esquerda
        container_layout.addWidget(content_container)
        container_layout.addStretch() # Espaço flexível à direita
        
        main_layout.addLayout(container_layout) 
        
        # Adicionar o QScrollArea ao layout principal da janela
        # O layout da central_widget já é QVBoxLayout por padrão, basta adicionar os widgets
        main_window_layout = QVBoxLayout(central_widget)
        main_window_layout.setContentsMargins(0, 0, 0, 0)
        main_window_layout.addWidget(scroll_area)


    def create_header(self):
        """Cria o header com logo e título principal e subtítulo."""
        header_widget = QWidget()
        header_widget.setObjectName("headerWidget")
        header_layout = QHBoxLayout(header_widget)
        header_layout.setContentsMargins(20, 20, 20, 10)

        # --- Logo (canto superior esquerdo) ---
        logo_container = QWidget()
        logo_container.setObjectName("logoContainer")
        logo_container.setFixedSize(80, 80)
        logo_layout = QVBoxLayout(logo_container)
        logo_layout.setContentsMargins(0, 0, 0, 0)
        
        self.logo_label = QLabel()
        self.logo_label.setObjectName("logoLabel")
        self.logo_label.setAlignment(Qt.AlignCenter)
        self.logo_label.setFixedSize(80, 80)

        # Código para carregar logo (para exibição dentro do cabeçalho)
        logo_file_path = resource_path("assets/app_logo.ico") # Ou o nome do seu arquivo de logo
        try:
            pixmap = QPixmap(logo_file_path)
            if not pixmap.isNull():
                scaled_pixmap = pixmap.scaled(70, 70, Qt.KeepAspectRatio, Qt.SmoothTransformation)
                self.logo_label.setPixmap(scaled_pixmap)
                self.logo_label.setText("") 
            else:
                self.logo_label.setText("LOGO") 
                print(f"Aviso: QPixmap é nulo para o caminho: {logo_file_path}. Verifique o arquivo.")
        except Exception as e:
            print(f"Erro ao carregar logo para cabeçalho: {e}")
            self.logo_label.setText("LOGO") 
            pass

        logo_layout.addWidget(self.logo_label)

        # --- Título e Subtítulo Centralizado ---
        title_container = QWidget()
        title_layout = QVBoxLayout(title_container)
        title_layout.setContentsMargins(20, 0, 0, 0) 
        title_layout.setSpacing(5) 
        title_layout.setAlignment(Qt.AlignCenter) 

        main_title = QLabel("Sistema de Homologação")
        main_title.setObjectName("mainTitle") 
        
        subtitle = QLabel("Por Kauan Kelvin")
        subtitle.setObjectName("subtitle") 

        title_layout.addWidget(main_title)
        title_layout.addWidget(subtitle)
        title_layout.addStretch() 

        header_layout.addWidget(logo_container)
        header_layout.addWidget(title_container)
        header_layout.addStretch() 

        return header_widget

    def create_patient_section(self):
        """Cria a seção de dados do paciente"""
        # Criando o QFrame que envolve a seção
        patient_frame = QFrame()
        patient_frame.setObjectName("sectionFrame")
        
        # O layout de grid dentro do frame
        patient_grid_layout = QGridLayout(patient_frame) 
        patient_grid_layout.setContentsMargins(20, 20, 20, 20)
        patient_grid_layout.setHorizontalSpacing(30) 
        patient_grid_layout.setVerticalSpacing(15)  
        patient_grid_layout.setColumnStretch(0, 1) # Coluna de labels
        patient_grid_layout.setColumnStretch(1, 2) # Coluna de inputs

        self.add_section_title_to_grid(patient_grid_layout, "Dados do Paciente", "sectionTitle") 
        
        # Linha 1 (Nome)
        patient_grid_layout.addWidget(QLabel("Nome Completo do Paciente:", objectName="formLabel", alignment=Qt.AlignRight | Qt.AlignVCenter), 1, 0)
        self.nome_paciente_input = QLineEdit(placeholderText="Nome Completo")
        patient_grid_layout.addWidget(self.nome_paciente_input, 1, 1)
        
        # Linha 2 (CPF)
        patient_grid_layout.addWidget(QLabel("CPF do Paciente:", objectName="formLabel", alignment=Qt.AlignRight | Qt.AlignVCenter), 2, 0)
        self.cpf_paciente_input = QLineEdit(placeholderText="Ex: 123.456.789-00", maxLength=14)
        self.cpf_paciente_input.setInputMask("000.000.000-00; ")
        patient_grid_layout.addWidget(self.cpf_paciente_input, 2, 1)
        
        # Linha 3 (Cargo)
        patient_grid_layout.addWidget(QLabel("Cargo do Paciente:", objectName="formLabel", alignment=Qt.AlignRight | Qt.AlignVCenter), 3, 0)
        self.cargo_paciente_input = QLineEdit(placeholderText="Ex: Analista Financeiro")
        patient_grid_layout.addWidget(self.cargo_paciente_input, 3, 1)
        
        # Linha 4 (Empresa)
        patient_grid_layout.addWidget(QLabel("Empresa do Paciente:", objectName="formLabel", alignment=Qt.AlignRight | Qt.AlignVCenter), 4, 0)
        self.empresa_paciente_input = QLineEdit(placeholderText="Nome da Empresa")
        patient_grid_layout.addWidget(self.empresa_paciente_input, 4, 1)
        
        # Conectar eventos de autofill
        self.nome_paciente_input.editingFinished.connect(self.autofill_patient_by_name_exact)
        self.cpf_paciente_input.textEdited.connect(self.autofill_patient_by_cpf)

        return patient_frame

    def create_certificate_section(self):
        """Cria a seção de dados do atestado"""
        atestado_frame = QFrame()
        atestado_frame.setObjectName("sectionFrame")
        
        atestado_grid_layout = QGridLayout(atestado_frame)
        atestado_grid_layout.setContentsMargins(20, 20, 20, 20)
        atestado_grid_layout.setHorizontalSpacing(30)
        atestado_grid_layout.setVerticalSpacing(15)
        atestado_grid_layout.setColumnStretch(0, 1) 
        atestado_grid_layout.setColumnStretch(1, 2) 

        self.add_section_title_to_grid(atestado_grid_layout, "Dados do Atestado", "sectionTitle")

        # Linha 1 (Data Atestado)
        atestado_grid_layout.addWidget(QLabel("Data do Atestado:", objectName="formLabel", alignment=Qt.AlignRight | Qt.AlignVCenter), 1, 0)
        self.data_atestado_input = QDateEdit(calendarPopup=True, objectName="dateEdit")
        self.data_atestado_input.setMinimumDate(QDate(1900, 1, 1))
        self.data_atestado_input.setDate(QDate.currentDate())
        self.data_atestado_input.setDisplayFormat("dd/MM/yyyy")
        atestado_grid_layout.addWidget(self.data_atestado_input, 1, 1)
        
        # Linha 2 (Dias Afastados)
        atestado_grid_layout.addWidget(QLabel("Dias Afastados:", objectName="formLabel", alignment=Qt.AlignRight | Qt.AlignVCenter), 2, 0)
        self.qtd_dias_atestado_input = QLineEdit(placeholderText="Número de dias")
        self.qtd_dias_atestado_input.setValidator(QIntValidator())
        atestado_grid_layout.addWidget(self.qtd_dias_atestado_input, 2, 1)
        
        # Linha 3 (CID)
        atestado_grid_layout.addWidget(QLabel("CID:", objectName="formLabel", alignment=Qt.AlignRight | Qt.AlignVCenter), 3, 0)
        self.codigo_cid_input = QLineEdit(placeholderText="Ex: A00, F32.9")
        atestado_grid_layout.addWidget(self.codigo_cid_input, 3, 1)

        return atestado_frame

    def create_doctor_section(self):
        """Cria a seção de dados do médico"""
        medico_frame = QFrame()
        medico_frame.setObjectName("sectionFrame")
        
        medico_layout = QVBoxLayout(medico_frame)
        medico_layout.setContentsMargins(25, 25, 25, 25)
        medico_layout.setSpacing(20)

        # Título da seção
        title = QLabel("Dados do Médico (Atestado)")
        title.setObjectName("sectionTitle")
        medico_layout.addWidget(title)

        # Grid para os campos
        grid = QGridLayout()
        grid.setHorizontalSpacing(20)
        grid.setVerticalSpacing(18)
        grid.setColumnStretch(0, 1) # Coluna de labels
        grid.setColumnStretch(1, 2) # Coluna de inputs

        # Linha 1 (Nome Médico)
        grid.addWidget(QLabel("Nome Completo do Médico:", objectName="formLabel"), 0, 0)
        self.nome_medico_input = QLineEdit(placeholderText="Nome Completo")
        grid.addWidget(self.nome_medico_input, 0, 1)
        
        # Linha 2 (UF Registro)
        grid.addWidget(QLabel("UF do Registro:", objectName="formLabel"), 1, 0)
        self.uf_crm_input = QComboBox(objectName="comboBox")
        self.uf_crm_input.addItems(["AC", "AL", "AP", "AM", "BA", "CE", "DF", "ES", "GO", "MA", "MT", "MS", "MG", "PA", "PB", "PR", "PE", "PI", "RJ", "RN", "RS", "RO", "RR", "SC", "SP", "SE", "TO"])
        grid.addWidget(self.uf_crm_input, 1, 1)
        
        # Linha 3: Registro do Profissional (Tipo + Número + Botão)
        grid.addWidget(QLabel("Registro do Profissional:", objectName="formLabel"), 2, 0)
        registro_widget = QWidget()
        registro_layout = QHBoxLayout(registro_widget)
        registro_layout.setContentsMargins(0, 0, 0, 0)
        registro_layout.setSpacing(10)

        self.tipo_registro_medico_combo = QComboBox(objectName="registroTypeCombo")
        self.tipo_registro_medico_combo.addItems(["CRM", "CRO", "RMS"])
        self.tipo_registro_medico_combo.setCurrentText("CRM")
        self.tipo_registro_medico_combo.setFixedWidth(80) 

        self.numero_registro_medico_input = QLineEdit(placeholderText="Número do Registro", objectName="registroNumberInput")

        self.consult_online_button = QPushButton("Consultar Online", objectName="consultOnlineButton")
        self.consult_online_button.setFixedWidth(140) 
        self.consult_online_button.clicked.connect(self.open_online_consultation)

        registro_layout.addWidget(self.tipo_registro_medico_combo)
        registro_layout.addWidget(self.numero_registro_medico_input)
        registro_layout.addWidget(self.consult_online_button)
        
        grid.addWidget(registro_widget, 2, 1) # Adiciona o widget de registro na segunda coluna
        
        medico_layout.addLayout(grid) # Adiciona o grid ao layout do frame médico
        
        # Conectar eventos de autofill para médico
        self.nome_medico_input.editingFinished.connect(self.autofill_doctor_by_name_exact)
        self.numero_registro_medico_input.textEdited.connect(self.autofill_doctor_by_registro)
        self.tipo_registro_medico_combo.currentIndexChanged.connect(self.autofill_doctor_by_registro)
        
        return medico_frame

    def create_buttons(self):
        """Cria o widget contendo os botões principais."""
        button_widget = QWidget()
        button_layout = QHBoxLayout(button_widget)
        button_layout.setSpacing(15)
        button_layout.setAlignment(Qt.AlignCenter)

        self.generate_button = QPushButton("Gerar Declaração", objectName="generateButton")
        self.generate_button.clicked.connect(self.generate_declaration)
        button_layout.addWidget(self.generate_button)

        self.clear_button = QPushButton("Limpar Campos", objectName="clearButton")
        self.clear_button.clicked.connect(self.clear_fields)
        button_layout.addWidget(self.clear_button)

        self.exit_button = QPushButton("Sair", objectName="exitButton")
        self.exit_button.clicked.connect(self.close)
        button_layout.addWidget(self.exit_button)

        return button_widget

    # As funções create_line_edit, create_date_edit, create_combo_box
    # e add_section_title_to_grid foram simplificadas e não retornam mais tuplas.
    # Elas agora criam e retornam o widget de input diretamente.
    # Os labels são criados diretamente no QGridLayout (e.g., QLabel("Label Text:", objectName="formLabel"))

    def create_line_edit(self, label_text, placeholder="", validator=None, max_length=None, input_mask=None):
        line_edit = QLineEdit()
        line_edit.setPlaceholderText(placeholder)
        if max_length:
            line_edit.setMaxLength(max_length)
        if validator == "int":
            line_edit.setValidator(QIntValidator())
        if input_mask:
            line_edit.setInputMask(input_mask)
        return line_edit

    def create_date_edit(self, label_text):
        date_edit = QDateEdit(calendarPopup=True)
        date_edit.setMinimumDate(QDate(1900, 1, 1))
        date_edit.setDate(QDate.currentDate())
        date_edit.setDisplayFormat("dd/MM/yyyy")
        date_edit.setObjectName("dateEdit")
        return date_edit

    def create_combo_box(self, label_text, items):
        combo_box = QComboBox()
        combo_box.addItems(items)
        combo_box.setObjectName("comboBox")
        return combo_box

    def add_section_title_to_grid(self, grid_layout, title_text, obj_name=None):
        title_label = QLabel(title_text)
        title_label.setFont(QFont("Arial", 12, QFont.Bold))
        if obj_name:
            title_label.setObjectName(obj_name)
        grid_layout.addWidget(title_label, 0, 0, 1, 2, alignment=Qt.AlignCenter)
        grid_layout.setRowStretch(0, 0) # Não estica a linha do título

    def apply_stylesheet(self):
        # Estilos QSS para uma aparência moderna e consistente
        stylesheet = """
        /* Estilos Globais */
        QMainWindow {
            background: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1,
                                      stop: 0 #f8f9fa, stop: 1 #e9ecef);
            font-family: "Segoe UI", "Roboto", "Arial", sans-serif;
            color: #343a40;
        }

        QScrollArea {
            border: none;
            background-color: transparent;
        }

        /* Container de Conteúdo Principal (para centralização e largura máxima) */
        #contentContainer {
            background-color: transparent;
        }
        
        /* Header */
        #headerWidget {
            background: qlineargradient(x1: 0, y1: 0, x2: 1, y2: 0,
                                      stop: 0 #2c3e50, stop: 1 #34495e);
            border-radius: 12px;
            margin: 10px;
            padding: 15px 20px;
            /* box-shadow: 0 4px 15px rgba(0, 0, 0, 0.2); -- Remover se der "Unknown property" */
        }

        #logoContainer {
            background-color: rgba(255, 255, 255, 0.1);
            border-radius: 10px;
            border: 2px solid rgba(255, 255, 255, 0.2);
            padding: 5px;
        }

        #logoLabel {
            color: #ffffff;
            font-weight: bold;
            font-size: 12pt;
            background-color: transparent;
        }

        #mainTitle {
            color: #ffffff;
            font-family: "Segoe UI", "Roboto", sans-serif;
            font-size: 28pt; 
            font-weight: 700; 
            letter-spacing: -0.5px;
            margin: 0px;
            padding: 0px;
            qproperty-alignment: AlignLeft; /* Alinha à esquerda no layout do header */
        }

        #subtitle {
            color: #bdc3c7; 
            font-family: "Segoe UI", "Roboto", sans-serif;
            font-size: 16pt;
            font-weight: 300; 
            margin: 0px;
            padding: 0px;
            qproperty-alignment: AlignLeft;
        }

        /* Seções (Frames) */
        QFrame#sectionFrame {
            background-color: #ffffff;
            border: 1px solid #dee2e6;
            border-radius: 12px;
            padding: 20px;
            margin: 0px 0px; 
            /* box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1); -- Remover se der "Unknown property" */
        }
        
        QFrame#sectionFrame:hover {
            border-color: #3498db;
            /* box-shadow: 0 4px 12px rgba(52, 152, 219, 0.15); -- Remover se der "Unknown property" */
        }

        /* Títulos de Seção */
        #sectionTitle {
            color: #2c3e50;
            font-family: "Segoe UI", "Roboto", sans-serif;
            font-size: 16pt;
            font-weight: 600;
            padding: 10px 0px 15px 0px;
            border-bottom: 2px solid #ecf0f1;
            margin-bottom: 15px; 
            qproperty-alignment: AlignLeft;
        }

        /* Labels dos Formulários */
        QLabel#formLabel {
            font-family: "Segoe UI", "Roboto", sans-serif;
            font-size: 11pt;
            color: #495057;
            font-weight: 500;
            qproperty-alignment: AlignRight | AlignVCenter;
            min-height: 40px; 
            padding-right: 20px; 
            word-wrap: normal;
            white-space: nowrap;
        }

        /* Campos de Entrada (QLineEdit, QDateEdit, QComboBox) */
        QLineEdit, QDateEdit, QComboBox {
            background-color: #ffffff;
            border: 2px solid #e9ecef;
            border-radius: 8px;
            padding: 12px 15px;
            font-family: "Segoe UI", "Roboto", sans-serif;
            font-size: 11pt;
            color: #495057;
            min-height: 20px;
            selection-background-color: #3498db;
        }
        
        QLineEdit:focus, QDateEdit:focus, QComboBox:focus {
            border-color: #3498db;
            background-color: #f8f9ff;
            outline: none;
        }
        
        QLineEdit:hover, QDateEdit:hover, QComboBox:hover {
            border-color: #adb5bd;
        }

        /* Ajustes específicos para QDateEdit */
        QDateEdit::drop-down {
            subcontrol-origin: padding;
            subcontrol-position: top right;
            width: 30px;
            border-left: 1px solid #dee2e6;
            border-top-right-radius: 6px;
            border-bottom-right-radius: 6px;
            background-color: #f8f9fa;
        }

        QDateEdit::down-arrow {
            image: url(data:image/svg+xml;base64,PHN2ZyB3aWR0aD0iMTYiIGhlaWdodD0iMTYiIHZpZXdCb3g9IjAgMCAxNiAxNiIgZmlsbD0ibm9uZSIgeG1sbnM9Imh0dHA6Ly93d3cudzMub3JnLzIwMDAvc3ZnIj4KPHBhdGggZD0iTTQgNkw4IDEwTDEyIDYiIHN0cm9rZT0iIzY5NzY4OSIgc3Ryb2tlLXdpZHRoPSIyIiBzdHJva2UtbGluZWNhcD0icm91bmQiIHN0cm9rZS1saW5lam9pbj0icm91bmQiLz4KPC9zdmc+);
            width: 16px;
            height: 16px;
        }

        /* Ajustes específicos para QComboBox */
        QComboBox {
            qproperty-frame: false;
            padding-left: 15px; 
        }

        QComboBox::drop-down {
            subcontrol-origin: padding;
            subcontrol-position: top right;
            width: 30px;
            border-left: 1px solid #dee2e6;
            border-top-right-radius: 6px;
            border-bottom-right-radius: 6px;
            background-color: #f8f9fa;
        }

        QComboBox::down-arrow {
            image: url(data:image/svg+xml;base64,PHN2ZyB3aWR0aD0iMTYiIGhlaWdodD0iMTYiIHZpZXdCb3g9IjAgMCAxNiAxNiIgZmlsbD0ibm9uZSIgeG1sbnM9Imh0dHA6Ly93d3cudzMub3JnLzIwMDAvc3ZnIj4KPHBhdGggZD0iTTQgNkw4IDEwTDEyIDYiIHN0cm9rZT0iIzY5NzY4OSIgc3Ryb2tlLXdpZHRoPSIyIiBzdHJva2UtbGluZWNhcD0icm91bmQiIHN0cm9rZS1saW5lam9pbj0icm91bmQiLz4KPC9zdmc+);
            width: 16px;
            height: 16px;
        }

        QComboBox QAbstractItemView { /* Estilo para o menu suspenso do ComboBox */
            background-color: #ffffff;
            border: 1px solid #dee2e6;
            border-radius: 8px;
            selection-background-color: #3498db;
            selection-color: #ffffff;
            padding: 5px;
            min-height: 20px;
        }

        /* Botões */
        QPushButton {
            background: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1,
                                      stop: 0 #3498db, stop: 1 #2980b9);
            color: #ffffff;
            border: none;
            border-radius: 8px;
            padding: 14px 28px;
            font-family: "Segoe UI", "Roboto", sans-serif;
            font-size: 12pt;
            font-weight: 600;
            min-width: 140px;
            min-height: 20px;
            /* transition: all 0.2s ease-in-out; -- Remover se der "Unknown property" */
        }
        
        QPushButton:hover {
            background: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1,
                                      stop: 0 #2980b9, stop: 1 #21618c);
        }
        
        QPushButton:pressed {
            background: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1,
                                      stop: 0 #21618c, stop: 1 #1b4f72);
        }

        QPushButton#generateButton {
            background: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1,
                                      stop: 0 #27ae60, stop: 1 #229954);
        }
        QPushButton#generateButton:hover {
            background: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1,
                                      stop: 0 #229954, stop: 1 #1e8449);
        }

        QPushButton#clearButton {
            background: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1,
                                      stop: 0 #e74c3c, stop: 1 #c0392b);
        }
        QPushButton#clearButton:hover {
            background: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1,
                                      stop: 0 #c0392b, stop: 1 #a93226);
        }

        QPushButton#exitButton {
            background: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1,
                                      stop: 0 #95a5a6, stop: 1 #7f8c8d);
        }
        QPushButton#exitButton:hover {
            background: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1,
                                      stop: 0 #7f8c8d, stop: 1 #6c7b7d);
        }

        QPushButton#consultOnlineButton {
            background: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1,
                                      stop: 0 #f39c12, stop: 1 #e67e22);
            min-width: 120px; /* Levemente ajustado */
            padding: 10px 20px; /* Levemente ajustado */
            font-size: 10pt; /* Levemente ajustado */
        }
        QPushButton#consultOnlineButton:hover {
            background: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1,
                                      stop: 0 #e67e22, stop: 1 #d35400);
        }
        
        /* Ajustes específicos para QComboBox do registro médico */
        #registroTypeCombo {
            max-width: 90px; 
            min-width: 70px;
            font-size: 10pt;
        }

        /* Status Bar */
        QStatusBar {
            background: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1,
                                      stop: 0 #ecf0f1, stop: 1 #d5dbdb);
            color: #2c3e50;
            font-family: "Segoe UI", "Roboto", sans-serif;
            font-size: 10pt;
            padding: 8px 15px;
            border-top: 1px solid #bdc3c7;
        }

        /* Message Box (Pop-ups) */
        QMessageBox {
            background-color: #ffffff;
            font-family: "Segoe UI", "Roboto", sans-serif;
            font-size: 11pt;
        }

        QMessageBox QPushButton {
            background: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1,
                                      stop: 0 #3498db, stop: 1 #2980b9);
            color: #ffffff;
            border: none;
            border-radius: 6px;
            padding: 8px 20px;
            min-width: 80px;
            font-size: 10pt;
            font-weight: 500;
        }

        QMessageBox QPushButton:hover {
            background: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1,
                                      stop: 0 #2980b9, stop: 1 #21618c);
        }

        /* Scrollbar customization */
        QScrollBar:vertical {
            background-color: #f8f9fa;
            width: 12px;
            border-radius: 6px;
        }
        QScrollBar::handle:vertical {
            background-color: #adb5bd;
            border-radius: 6px;
            min-height: 20px;
            margin: 2px;
        }
        QScrollBar::handle:vertical:hover {
            background-color: #6c757d;
        }
        QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {
            border: none;
            background: none;
        }
        QScrollBar:horizontal {
            background-color: #f8f9fa;
            height: 12px;
            border-radius: 6px;
        }
        QScrollBar::handle:horizontal {
            background-color: #adb5bd;
            border-radius: 6px;
            min-width: 20px;
            margin: 2px;
        }
        QScrollBar::handle:horizontal:hover {
            background-color: #6c757d;
        }
        QScrollBar::add-line:horizontal, QScrollBar::sub-line:horizontal {
            border: none;
            background: none;
        }
        """
        self.setStyleSheet(stylesheet)


    # --- Métodos de Lógica e Funcionalidade (Inalterados, mantidos na versão anterior) ---
    def setup_completers(self):
        self.patient_name_model = QStringListModel()
        self.patient_completer = QCompleter(self.patient_name_model, self)
        self.patient_completer.setCaseSensitivity(Qt.CaseInsensitive)
        self.nome_paciente_input.setCompleter(self.patient_completer)
        self.patient_completer.activated.connect(self.autofill_patient_by_name_selected)
        
        self.doctor_name_model = QStringListModel()
        self.doctor_completer = QCompleter(self.doctor_name_model, self)
        self.doctor_completer.setCaseSensitivity(Qt.CaseInsensitive)
        self.nome_medico_input.setCompleter(self.doctor_completer)
        self.doctor_completer.activated.connect(self.autofill_doctor_by_name_selected)

        self.load_patient_names_for_completer()
        self.load_doctor_names_for_completer()

    def load_patient_names_for_completer(self):
        self.update_status("Carregando nomes de pacientes...")
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT DISTINCT nome_completo FROM pacientes ORDER BY nome_completo")
        names = [row['nome_completo'] for row in cursor.fetchall()]
        conn.close()
        self.patient_name_model.setStringList(names)
        self.update_status("Nomes de pacientes carregados.")

    def load_doctor_names_for_completer(self):
        self.update_status("Carregando nomes de médicos...")
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT DISTINCT nome_completo FROM medicos ORDER BY nome_completo")
        names = [row['nome_completo'] for row in cursor.fetchall()]
        conn.close()
        self.doctor_name_model.setStringList(names)
        self.update_status("Nomes de médicos carregados.")

    def autofill_patient_by_name_selected(self, text):
        if self.is_autofilling:
            return
        self.update_status(f"Buscando dados de paciente: {text}...")
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM pacientes WHERE nome_completo = ?", (text,))
        patient = cursor.fetchone()
        conn.close()

        if patient:
            self.is_autofilling = True
            self.cpf_paciente_input.setText(patient['cpf'])
            self.nome_paciente_input.setText(patient['nome_completo'])
            self.cargo_paciente_input.setText(patient['cargo'])
            self.empresa_paciente_input.setText(patient['empresa'])
            self.is_autofilling = False
            self.update_status(f"Dados de paciente '{patient['nome_completo']}' preenchidos.")
        else:
            self.update_status(f"Paciente '{text}' não encontrado para autocompletar.")


    def autofill_patient_by_name_exact(self):
        if self.is_autofilling:
            return

        name = self.nome_paciente_input.text().strip()
        if not name:
            self.is_autofilling = True
            self.cpf_paciente_input.clear()
            self.cargo_paciente_input.clear()
            self.empresa_paciente_input.clear()
            self.is_autofilling = False
            self.update_status("Campo de nome do paciente limpo.")
            return
        
        self.update_status(f"Verificando paciente por nome exato: {name}...")
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM pacientes WHERE nome_completo = ?", (name,))
        patient = cursor.fetchone()
        conn.close()

        if patient:
            self.is_autofilling = True
            self.cpf_paciente_input.setText(patient['cpf'])
            self.nome_paciente_input.setText(patient['nome_completo'])
            self.cargo_paciente_input.setText(patient['cargo'])
            self.empresa_paciente_input.setText(patient['empresa'])
            self.is_autofilling = False
            self.update_status(f"Dados de paciente '{patient['nome_completo']}' preenchidos por nome exato.")
        else:
            self.update_status(f"Nome de paciente '{name}' não encontrado no banco de dados.")


    def autofill_patient_by_cpf(self):
        if self.is_autofilling:
            return

        cpf_formatted = self.cpf_paciente_input.text().strip()
        cpf_cleaned = ''.join(filter(str.isdigit, cpf_formatted))
        
        if len(cpf_cleaned) < 11:
            self.update_status("CPF do paciente incompleto. Preenchimento automático suspenso.")
            return

        self.update_status(f"Buscando paciente por CPF: {cpf_cleaned}...")
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM pacientes WHERE cpf = ?", (cpf_cleaned,))
        patient = cursor.fetchone()
        conn.close()

        if patient:
            self.is_autofilling = True
            self.nome_paciente_input.setText(patient['nome_completo'])
            self.cpf_paciente_input.setText(patient['cpf'])
            self.cargo_paciente_input.setText(patient['cargo'])
            self.empresa_paciente_input.setText(patient['empresa'])
            self.is_autofilling = False
            self.update_status(f"Dados de paciente '{patient['nome_completo']}' preenchidos por CPF.")
        else:
            self.update_status(f"Paciente com CPF '{cpf_cleaned}' não encontrado no banco de dados.")


    def autofill_doctor_by_name_selected(self, text):
        if self.is_autofilling:
            return
        self.update_status(f"Buscando dados de médico: {text}...")
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM medicos WHERE nome_completo = ?", (text,))
        doctor = cursor.fetchone()
        conn.close()

        if doctor:
            self.is_autofilling = True
            self.nome_medico_input.setText(doctor['nome_completo'])
            self.tipo_registro_medico_combo.setCurrentText(doctor['tipo_crm'])
            self.numero_registro_medico_input.setText(doctor['crm'])
            self.uf_crm_input.setCurrentText(doctor['uf_crm'])
            self.is_autofilling = False
            self.update_status(f"Dados de médico '{doctor['nome_completo']}' preenchidos.")
        else:
            self.update_status(f"Médico '{text}' não encontrado para autocompletar.")


    def autofill_doctor_by_name_exact(self):
        if self.is_autofilling:
            return

        name = self.nome_medico_input.text().strip()
        if not name:
            self.is_autofilling = True
            self.tipo_registro_medico_combo.setCurrentText("CRM")
            self.numero_registro_medico_input.clear()
            self.uf_crm_input.setCurrentIndex(0)
            self.is_autofilling = False
            self.update_status("Campo de nome do médico limpo.")
            return

        self.update_status(f"Verificando médico por nome exato: {name}...")
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM medicos WHERE nome_completo = ?", (name,))
        doctor = cursor.fetchone()
        conn.close()

        if doctor:
            self.is_autofilling = True
            self.nome_medico_input.setText(doctor['nome_completo'])
            self.tipo_registro_medico_combo.setCurrentText(doctor['tipo_crm'])
            self.numero_registro_medico_input.setText(doctor['crm'])
            self.uf_crm_input.setCurrentText(doctor['uf_crm'])
            self.is_autofilling = False
            self.update_status(f"Dados de médico '{doctor['nome_completo']}' preenchidos por nome exato.")
        else:
            self.update_status(f"Nome de médico '{name}' não encontrado no banco de dados.")


    def autofill_doctor_by_registro(self):
        if self.is_autofilling:
            return

        tipo_registro = self.tipo_registro_medico_combo.currentText().strip()
        numero_registro = self.numero_registro_medico_input.text().strip()
        
        if not tipo_registro or not numero_registro:
            self.is_autofilling = True
            self.nome_medico_input.clear()
            self.uf_crm_input.setCurrentIndex(0)
            self.is_autofilling = False
            self.update_status("Registro do médico incompleto. Campos limpos.")
            return

        self.update_status(f"Buscando médico por registro: {tipo_registro} {numero_registro}...")
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM medicos WHERE tipo_crm = ? AND crm = ?", (tipo_registro, numero_registro))
        doctor = cursor.fetchone()
        conn.close()

        if doctor:
            self.is_autofilling = True
            self.nome_medico_input.setText(doctor['nome_completo'])
            self.uf_crm_input.setCurrentText(doctor['uf_crm'])
            self.is_autofilling = False
            self.update_status(f"Dados de médico '{doctor['nome_completo']}' preenchidos por registro.")
        else:
            self.update_status(f"Médico com registro '{tipo_registro} {numero_registro}' não encontrado.")


    def clear_fields(self):
        self.nome_paciente_input.clear()
        self.cpf_paciente_input.clear()
        self.cargo_paciente_input.clear()
        self.empresa_paciente_input.clear()
        self.data_atestado_input.setDate(QDate.currentDate())
        self.qtd_dias_atestado_input.clear()
        self.codigo_cid_input.clear()
        self.nome_medico_input.clear()
        self.tipo_registro_medico_combo.setCurrentText("CRM") 
        self.numero_registro_medico_input.clear()
        self.uf_crm_input.setCurrentIndex(0)

        self.load_patient_names_for_completer()
        self.load_doctor_names_for_completer()
        self.update_status("Campos limpos. Sistema pronto.")


    def generate_declaration(self):
        self.update_status("Gerando declaração... Verificando campos.")
        data = {
            "nome_paciente": self.nome_paciente_input.text().strip(),
            "cpf_paciente": self.cpf_paciente_input.text().strip(),
            "cargo_paciente": self.cargo_paciente_input.text().strip(),
            "empresa_paciente": self.empresa_paciente_input.text().strip(),
            "data_atestado": self.data_atestado_input.date().toString("dd/MM/yyyy"),
            "qtd_dias_atestado": self.qtd_dias_atestado_input.text().strip(),
            "codigo_cid": self.codigo_cid_input.text().strip(),
            "nome_medico": self.nome_medico_input.text().strip(),
            "tipo_registro_medico": self.tipo_registro_medico_combo.currentText().strip(),
            "crm__medico": self.numero_registro_medico_input.text().strip(),
            "uf_crm_medico": self.uf_crm_input.currentText().strip()
        }

        required_fields = {
            "nome_paciente": "Nome do Paciente",
            "cpf_paciente": "CPF do Paciente",
            "data_atestado": "Data do Atestado",
            "qtd_dias_atestado": "Dias Afastados",
            "codigo_cid": "CID",
            "nome_medico": "Nome do Médico",
            "tipo_registro_medico": "Tipo de Registro do Médico",
            "crm__medico": "Número de Registro do Médico",
            "uf_crm_medico": "UF do Registro do Médico"
        }

        cpf_para_validacao = ''.join(filter(str.isdigit, data.get("cpf_paciente", '')))

        for key, display_name in required_fields.items():
            if not data.get(key) or (key == "cpf_paciente" and len(cpf_para_validacao) != 11):
                QMessageBox.warning(self, "Campos Obrigatórios", f"O campo '{display_name}' é obrigatório ou está incompleto.")
                self.update_status(f"Erro: Campo '{display_name}' não preenchido.")
                return

        try:
            data["qtd_dias_atestado"] = int(data.get("qtd_dias_atestado", 0))
        except ValueError:
            QMessageBox.warning(self, "Erro de Entrada", "O campo 'Dias Afastados' deve ser um número inteiro.")
            self.update_status("Erro: Dias Afastados inválido.")
            return

        self.update_status("Salvando dados no banco de dados...")
        self.save_or_update_data(data)

        self.load_patient_names_for_completer()
        self.load_doctor_names_for_completer()

        self.update_status("Gerando arquivo DOCX...")
        try:
            output_path = generate_document(data)
            if output_path:
                QMessageBox.information(self, "Sucesso", f"Declaração gerada com sucesso!\nSalvo em: {output_path}")
                self.clear_fields()
                self.update_status("Declaração gerada e campos limpos.")
            else:
                QMessageBox.critical(self, "Erro", "Não foi possível gerar a declaração. Verifique o modelo e os logs.")
                self.update_status("Falha ao gerar declaração.")
        except Exception as e:
            QMessageBox.critical(self, "Erro na Geração", f"Ocorreu um erro ao gerar o documento: {e}")
            self.update_status(f"Erro crítico na geração: {e}")


    def save_or_update_data(self, data):
        self.update_status("Persistindo dados no banco de dados...")
        conn = get_db_connection()
        cursor = conn.cursor()

        cpf_para_db = ''.join(filter(str.isdigit, data.get("cpf_paciente", '')))

        cursor.execute("SELECT id FROM pacientes WHERE cpf = ?", (cpf_para_db,))
        patient_row = cursor.fetchone()

        if patient_row:
            cursor.execute(
                "UPDATE pacientes SET nome_completo = ?, cargo = ?, empresa = ? WHERE id = ?",
                (data.get("nome_paciente"), data.get("cargo_paciente"), data.get("empresa_paciente"), patient_row['id'])
            )
        else:
            cursor.execute(
                "INSERT INTO pacientes (nome_completo, cpf, cargo, empresa) VALUES (?, ?, ?, ?)",
                (data.get("nome_paciente"), cpf_para_db, data.get("cargo_paciente"), data.get("empresa_paciente"))
            )

        cursor.execute("SELECT id FROM medicos WHERE tipo_crm = ? AND crm = ?", (data.get("tipo_registro_medico"), data.get("crm__medico")))
        doctor_row = cursor.fetchone()

        if doctor_row:
            cursor.execute(
                "UPDATE medicos SET nome_completo = ?, uf_crm = ? WHERE id = ?",
                (data.get("nome_medico"), data.get("uf_crm_medico"), doctor_row['id'])
            )
        else:
            cursor.execute(
                "INSERT INTO medicos (nome_completo, tipo_crm, crm, uf_crm) VALUES (?, ?, ?, ?)",
                (data.get("nome_medico"), data.get("tipo_registro_medico"), data.get("crm__medico"), data.get("uf_crm_medico"))
            )

        cursor.execute(
            "INSERT INTO atestados (paciente_id, medico_id, data_atestado, qtd_dias_atestado, codigo_cid, data_homologacao) VALUES ((SELECT id FROM pacientes WHERE cpf = ?), (SELECT id FROM medicos WHERE tipo_crm = ? AND crm = ?), ?, ?, ?, ?)",
            (cpf_para_db, data.get("tipo_registro_medico"), data.get("crm__medico"), data.get("data_atestado"), data.get("qtd_dias_atestado"), data.get("codigo_cid"), QDate.currentDate().toString("dd/MM/yyyy"))
        )

        conn.commit()
        conn.close()
        self.update_status("Dados salvos no banco de dados.")

    def update_status(self, message):
        self._statusBar.showMessage(message)

    def open_online_consultation(self):
        tipo_registro = self.tipo_registro_medico_combo.currentText().strip()
        numero_registro = self.numero_registro_medico_input.text().strip()
        uf_registro = self.uf_crm_input.currentText().strip()

        if not numero_registro or not uf_registro:
            QMessageBox.warning(self, "Consulta Online", "Por favor, preencha o número de registro e a UF para consultar online.")
            self.update_status("Campos incompletos para consulta online.")
            return

        consult_urls = {
            "CRM": "https://portal.cfm.org.br/busca-medicos/",
            "CRO": f"https://website.cfo.org.br/busca-profissionais/",
            "RMS": "https://www.google.com/search?q=consulta+registro+profissional+saude+"+tipo_registro+"+"+numero_registro+"+"+uf_registro
        }

        url = consult_urls.get(tipo_registro)

        if url:
            try:
                QDesktopServices.openUrl(QUrl(url))
                self.update_status(f"Abrindo consulta online para {tipo_registro} {numero_registro}-{uf_registro} no navegador.")
                
                if tipo_registro == "CRM":
                    QMessageBox.information(self, "Instruções para Consulta Online", 
                        "A página de consulta do CRM exige preenchimento manual e um reCAPTCHA. "
                        "Por favor, digite o nome do médico, UF e CRM diretamente na página do navegador que foi aberta e resolva o CAPTCHA para prosseguir."
                    )
                
            except Exception as e:
                QMessageBox.critical(self, "Erro ao Abrir Navegador", f"Não foi possível abrir o navegador. Erro: {e}")
                self.update_status(f"Erro ao abrir navegador: {e}")
        else:
            QMessageBox.warning(self, "Consulta Online", f"Não há URL de consulta configurada para o tipo de registro: {tipo_registro}. Por favor, consulte manualmente.")
            self.update_status(f"URL de consulta não configurada para {tipo_registro}.")