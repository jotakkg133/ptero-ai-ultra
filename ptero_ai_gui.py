#!/usr/bin/env python3
"""
PTERO-AI ULTRA PRO v2.0 - Interface Gráfica
Interface moderna estilo macOS com blur, transparência e animações
"""

import sys
import json
import os
from pathlib import Path
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QTextEdit, QLineEdit, QPushButton, QLabel, QScrollArea, QFrame,
    QGraphicsDropShadowEffect, QSplitter, QListWidget, QListWidgetItem
)
from PyQt6.QtCore import Qt, QTimer, QPropertyAnimation, QEasingCurve, QPoint, QSize, pyqtSignal, QThread
from PyQt6.QtGui import (
    QPalette, QColor, QLinearGradient, QPainter, QBrush, QPen,
    QFont, QIcon, QPainterPath, QPixmap
)
from PyQt6.QtSvgWidgets import QSvgWidget
import subprocess
import threading

# Importar o engine da IA
try:
    from ptero_ai_ultra_pro import PteroAIUltraPro
except ImportError:
    print("⚠️  Módulo ptero_ai_ultra_pro não encontrado")
    PteroAIUltraPro = None


class BlurredWidget(QWidget):
    """Widget com efeito blur e transparência"""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setAutoFillBackground(False)
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
    
    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        
        # Fundo com blur
        path = QPainterPath()
        path.addRoundedRect(0, 0, self.width(), self.height(), 20, 20)
        
        # Gradiente de fundo
        gradient = QLinearGradient(0, 0, 0, self.height())
        gradient.setColorAt(0, QColor(30, 30, 46, 230))  # Quase transparente
        gradient.setColorAt(1, QColor(17, 17, 27, 240))
        
        painter.fillPath(path, QBrush(gradient))
        
        # Borda brilhante
        pen = QPen(QColor(94, 129, 172, 100))
        pen.setWidth(1)
        painter.setPen(pen)
        painter.drawPath(path)


class MessageBubble(QFrame):
    """Balão de mensagem estilo chat"""
    
    def __init__(self, text, is_user=True, parent=None):
        super().__init__(parent)
        self.is_user = is_user
        self._text = text
        self.setupUI()
    
    def setupUI(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(15, 12, 15, 12)
        layout.setSpacing(0)
        
        # Label do texto
        self.label = QLabel(self._text)
        self.label.setWordWrap(True)
        self.label.setTextInteractionFlags(Qt.TextInteractionFlag.TextSelectableByMouse)
        self.label.setMinimumWidth(100)
        self.label.setMaximumWidth(500)
        
        # Definir tamanho do frame também
        self.setMinimumWidth(120)
        self.setMaximumWidth(550)
        
        # Estilo baseado em quem enviou
        if self.is_user:
            # Usuário - azul
            self.setStyleSheet("""
                QFrame {
                    background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                        stop:0 rgba(137, 180, 250, 220),
                        stop:1 rgba(116, 199, 236, 220));
                    border-radius: 18px;
                    border: 1px solid rgba(255, 255, 255, 50);
                }
            """)
            self.label.setStyleSheet("""
                QLabel {
                    color: #1e1e2e;
                    font-size: 14px;
                    font-weight: 500;
                    background: transparent;
                    border: none;
                }
            """)
        else:
            # IA - cinza escuro com ícone
            self.setStyleSheet("""
                QFrame {
                    background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                        stop:0 rgba(49, 50, 68, 220),
                        stop:1 rgba(30, 30, 46, 230));
                    border-radius: 18px;
                    border: 1px solid rgba(148, 226, 213, 50);
                }
            """)
            self.label.setStyleSheet("""
                QLabel {
                    color: #cdd6f4;
                    font-size: 14px;
                    font-weight: 400;
                    background: transparent;
                    border: none;
                }
            """)
        
        # Sombra
        shadow = QGraphicsDropShadowEffect()
        shadow.setBlurRadius(20)
        shadow.setColor(QColor(0, 0, 0, 100))
        shadow.setOffset(0, 4)
        self.setGraphicsEffect(shadow)
        
        layout.addWidget(self.label)
        
        # Definir tamanho mínimo antes de animar
        self.adjustSize()
        
        # Animação de entrada com opacidade
        self.setWindowOpacity(0)
        self.opacity_animation = QPropertyAnimation(self, b"windowOpacity")
        self.opacity_animation.setDuration(300)
        self.opacity_animation.setStartValue(0.0)
        self.opacity_animation.setEndValue(1.0)
        self.opacity_animation.setEasingCurve(QEasingCurve.Type.OutCubic)
        QTimer.singleShot(50, self.opacity_animation.start)
    
    def setText(self, text):
        self._text = text
        if hasattr(self, 'label'):
            self.label.setText(text)
            self.adjustSize()
    
    def text(self):
        return self._text


class AnimatedLogo(QWidget):
    """Logo SVG animado"""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setFixedSize(60, 60)
        self.rotation = 0
        self.pulse_scale = 1.0
        
        # Timer para animação
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.animate)
        self.timer.start(50)
    
    def animate(self):
        self.rotation += 2
        self.pulse_scale = 1.0 + 0.1 * abs(((self.rotation % 60) - 30) / 30)
        self.update()
    
    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        
        # Centro
        center = self.rect().center()
        painter.translate(center)
        painter.rotate(self.rotation)
        painter.scale(self.pulse_scale, self.pulse_scale)
        
        # Círculo externo (azul brilhante)
        gradient = QLinearGradient(-25, -25, 25, 25)
        gradient.setColorAt(0, QColor(137, 180, 250))
        gradient.setColorAt(1, QColor(116, 199, 236))
        
        painter.setBrush(QBrush(gradient))
        painter.setPen(QPen(QColor(255, 255, 255, 100), 2))
        painter.drawEllipse(-25, -25, 50, 50)
        
        # Círculo interno (roxo)
        gradient2 = QLinearGradient(-15, -15, 15, 15)
        gradient2.setColorAt(0, QColor(203, 166, 247))
        gradient2.setColorAt(1, QColor(180, 190, 254))
        
        painter.setBrush(QBrush(gradient2))
        painter.drawEllipse(-15, -15, 30, 30)
        
        # Ponto central (branco)
        painter.setBrush(QBrush(QColor(255, 255, 255)))
        painter.drawEllipse(-5, -5, 10, 10)


class StatusIndicator(QWidget):
    """Indicador de status animado"""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setFixedSize(12, 12)
        self.status = "idle"  # idle, thinking, working
        self.opacity = 1.0
        self.direction = -1
        
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.animate)
        self.timer.start(30)
    
    def setStatus(self, status):
        self.status = status
    
    def animate(self):
        if self.status == "thinking":
            self.opacity += 0.05 * self.direction
            if self.opacity <= 0.3 or self.opacity >= 1.0:
                self.direction *= -1
        else:
            self.opacity = 1.0
        
        self.update()
    
    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        
        # Cor baseada no status
        if self.status == "idle":
            color = QColor(166, 227, 161)  # Verde
        elif self.status == "thinking":
            color = QColor(249, 226, 175)  # Amarelo
        elif self.status == "working":
            color = QColor(137, 180, 250)  # Azul
        else:
            color = QColor(243, 139, 168)  # Vermelho
        
        color.setAlpha(int(self.opacity * 255))
        
        painter.setBrush(QBrush(color))
        painter.setPen(Qt.PenStyle.NoPen)
        painter.drawEllipse(0, 0, 12, 12)
        
        # Brilho
        gradient = QLinearGradient(0, 0, 12, 12)
        gradient.setColorAt(0, QColor(255, 255, 255, 50))
        gradient.setColorAt(1, QColor(255, 255, 255, 0))
        painter.setBrush(QBrush(gradient))
        painter.drawEllipse(0, 0, 12, 12)


class TerminalDetector(QWidget):
    """Widget para detectar terminal ativo"""
    
    terminalDetected = pyqtSignal(str)
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setupUI()
        self.monitoring = False
    
    def setupUI(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(20, 15, 20, 15)
        
        # Título
        title = QLabel("🖥️ Detecção de Terminal")
        title.setStyleSheet("""
            color: #cdd6f4;
            font-size: 16px;
            font-weight: 600;
        """)
        layout.addWidget(title)
        
        # Instrução
        instruction = QLabel("Digite algo no terminal que deseja controlar...")
        instruction.setStyleSheet("""
            color: #a6adc8;
            font-size: 13px;
            margin-top: 5px;
        """)
        layout.addWidget(instruction)
        
        # Status
        self.statusLabel = QLabel("⏳ Aguardando atividade no terminal...")
        self.statusLabel.setStyleSheet("""
            color: #f9e2af;
            font-size: 13px;
            margin-top: 10px;
            padding: 10px;
            background: rgba(249, 226, 175, 20);
            border-radius: 8px;
        """)
        layout.addWidget(self.statusLabel)
        
        # Botão iniciar
        self.startBtn = QPushButton("▶ Iniciar Detecção")
        self.startBtn.setStyleSheet("""
            QPushButton {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 rgba(166, 227, 161, 220),
                    stop:1 rgba(148, 226, 213, 220));
                color: #1e1e2e;
                border: none;
                border-radius: 10px;
                padding: 12px;
                font-size: 14px;
                font-weight: 600;
            }
            QPushButton:hover {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 rgba(166, 227, 161, 255),
                    stop:1 rgba(148, 226, 213, 255));
            }
        """)
        self.startBtn.clicked.connect(self.toggleMonitoring)
        layout.addWidget(self.startBtn)
    
    def toggleMonitoring(self):
        if not self.monitoring:
            self.monitoring = True
            self.startBtn.setText("⏸ Parar Detecção")
            self.statusLabel.setText("👀 Monitorando terminais ativos...")
            self.statusLabel.setStyleSheet("""
                color: #89b4fa;
                font-size: 13px;
                margin-top: 10px;
                padding: 10px;
                background: rgba(137, 180, 250, 20);
                border-radius: 8px;
            """)
            # Iniciar thread de monitoramento
            threading.Thread(target=self.monitorTerminals, daemon=True).start()
        else:
            self.monitoring = False
            self.startBtn.setText("▶ Iniciar Detecção")
            self.statusLabel.setText("⏳ Aguardando atividade no terminal...")
    
    def monitorTerminals(self):
        """Monitora terminais ativos"""
        try:
            # Listar processos de terminal
            result = subprocess.run(
                ['ps', 'aux'], 
                capture_output=True, 
                text=True
            )
            
            terminal_processes = []
            for line in result.stdout.split('\n'):
                if any(term in line.lower() for term in ['bash', 'zsh', 'fish', 'pts']):
                    terminal_processes.append(line)
            
            if terminal_processes:
                # Pegar primeiro terminal encontrado
                first_terminal = terminal_processes[0]
                self.terminalDetected.emit(first_terminal)
                
                self.statusLabel.setText(f"✓ Terminal detectado!")
                self.statusLabel.setStyleSheet("""
                    color: #a6e3a1;
                    font-size: 13px;
                    margin-top: 10px;
                    padding: 10px;
                    background: rgba(166, 227, 161, 20);
                    border-radius: 8px;
                """)
        except Exception as e:
            self.statusLabel.setText(f"❌ Erro: {e}")


class AIWorker(QThread):
    """Thread worker para processar IA em background"""
    responseReady = pyqtSignal(str)
    
    def __init__(self, ai_engine, message):
        super().__init__()
        self.ai_engine = ai_engine
        self.message = message
    
    def run(self):
        try:
            # Usar método chat ao invés de process_request
            result = self.ai_engine.chat(self.message)
            self.responseReady.emit(result)
        except Exception as e:
            import traceback
            error_detail = traceback.format_exc()
            print(f"❌ Erro completo:\n{error_detail}")
            self.responseReady.emit(f"❌ Erro: {str(e)}")


class ChatInterface(QMainWindow):
    """Interface principal de chat"""
    
    def __init__(self):
        super().__init__()
        self.messages = []
        self.ai_status = "idle"
        self.ai_engine = None
        self.current_worker = None
        
        # Carregar config e inicializar IA
        self.loadConfig()
        self.setupUI()
        self.applyStyles()
    
    def loadConfig(self):
        """Carrega configuração e inicializa engine da IA"""
        config_path = Path.home() / ".config" / "ptero-ai-ultra" / "config.json"
        
        if config_path.exists():
            with open(config_path) as f:
                config = json.load(f)
                api_key = config.get("gemini_api_key", "")
                
                if api_key and PteroAIUltraPro:
                    try:
                        # Inicializar engine
                        self.ai_engine = PteroAIUltraPro(api_key, "ptero_ai_ultra_config.json")
                        print("✅ Engine da IA inicializado")
                    except Exception as e:
                        print(f"❌ Erro ao inicializar IA: {e}")
                        import traceback
                        traceback.print_exc()
                else:
                    print("⚠️  API Key não configurada ou módulo não importado")
        else:
            print(f"⚠️  Arquivo de configuração não encontrado: {config_path}")
    
    def setupUI(self):
        self.setWindowTitle("PTERO-AI ULTRA PRO v2.0")
        self.setGeometry(100, 100, 1200, 800)
        
        # Widget central
        central = QWidget()
        self.setCentralWidget(central)
        
        # Layout principal
        main_layout = QHBoxLayout(central)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)
        
        # Splitter para dividir tela
        splitter = QSplitter(Qt.Orientation.Horizontal)
        
        # === PAINEL ESQUERDO (Sidebar) ===
        sidebar = self.createSidebar()
        splitter.addWidget(sidebar)
        
        # === PAINEL CENTRAL (Chat) ===
        chat_panel = self.createChatPanel()
        splitter.addWidget(chat_panel)
        
        # === PAINEL DIREITO (Info) ===
        info_panel = self.createInfoPanel()
        splitter.addWidget(info_panel)
        
        # Proporções
        splitter.setSizes([250, 650, 300])
        
        main_layout.addWidget(splitter)
    
    def createSidebar(self):
        """Cria barra lateral"""
        sidebar = BlurredWidget()
        layout = QVBoxLayout(sidebar)
        layout.setContentsMargins(15, 20, 15, 20)
        layout.setSpacing(15)
        
        # Logo animado
        logo_container = QWidget()
        logo_layout = QHBoxLayout(logo_container)
        logo_layout.setContentsMargins(0, 0, 0, 0)
        logo = AnimatedLogo()
        logo_layout.addStretch()
        logo_layout.addWidget(logo)
        logo_layout.addStretch()
        layout.addWidget(logo_container)
        
        # Título
        title = QLabel("PTERO-AI")
        title.setStyleSheet("""
            color: #cdd6f4;
            font-size: 24px;
            font-weight: 700;
            margin-bottom: 5px;
        """)
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(title)
        
        subtitle = QLabel("Ultra Pro v2.0")
        subtitle.setStyleSheet("""
            color: #a6adc8;
            font-size: 12px;
            margin-bottom: 20px;
        """)
        subtitle.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(subtitle)
        
        # Status
        status_container = QWidget()
        status_layout = QHBoxLayout(status_container)
        status_layout.setContentsMargins(10, 8, 10, 8)
        
        self.statusIndicator = StatusIndicator()
        status_layout.addWidget(self.statusIndicator)
        
        self.statusText = QLabel("Pronto")
        self.statusText.setStyleSheet("""
            color: #a6e3a1;
            font-size: 13px;
            font-weight: 500;
        """)
        status_layout.addWidget(self.statusText)
        status_layout.addStretch()
        
        layout.addWidget(status_container)
        
        # Separador
        separator = QFrame()
        separator.setFrameShape(QFrame.Shape.HLine)
        separator.setStyleSheet("background: rgba(148, 226, 213, 30);")
        layout.addWidget(separator)
        
        # Detector de terminal
        self.terminalDetector = TerminalDetector()
        self.terminalDetector.terminalDetected.connect(self.onTerminalDetected)
        layout.addWidget(self.terminalDetector)
        
        layout.addStretch()
        
        # Informações
        info_label = QLabel("💡 Dica: Digite no terminal\npara eu identificar qual\ncomando você quer\nque eu execute!")
        info_label.setStyleSheet("""
            color: #a6adc8;
            font-size: 11px;
            padding: 10px;
            background: rgba(137, 180, 250, 15);
            border-radius: 8px;
        """)
        info_label.setWordWrap(True)
        layout.addWidget(info_label)
        
        return sidebar
    
    def createChatPanel(self):
        """Cria painel de chat"""
        panel = BlurredWidget()
        layout = QVBoxLayout(panel)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(15)
        
        # Área de mensagens
        self.scrollArea = QScrollArea()
        self.scrollArea.setWidgetResizable(True)
        self.scrollArea.setStyleSheet("""
            QScrollArea {
                background: transparent;
                border: none;
            }
            QScrollBar:vertical {
                background: rgba(69, 71, 90, 100);
                width: 8px;
                border-radius: 4px;
            }
            QScrollBar::handle:vertical {
                background: rgba(137, 180, 250, 150);
                border-radius: 4px;
            }
        """)
        
        self.messagesWidget = QWidget()
        self.messagesLayout = QVBoxLayout(self.messagesWidget)
        self.messagesLayout.setContentsMargins(0, 0, 10, 0)
        self.messagesLayout.setSpacing(12)
        self.messagesLayout.addStretch()
        
        self.scrollArea.setWidget(self.messagesWidget)
        layout.addWidget(self.scrollArea, 1)
        
        # Área de input
        input_container = QWidget()
        input_layout = QHBoxLayout(input_container)
        input_layout.setContentsMargins(0, 0, 0, 0)
        input_layout.setSpacing(10)
        
        self.inputField = QLineEdit()
        self.inputField.setPlaceholderText("Digite sua mensagem...")
        self.inputField.setStyleSheet("""
            QLineEdit {
                background: rgba(49, 50, 68, 200);
                border: 1px solid rgba(148, 226, 213, 50);
                border-radius: 20px;
                padding: 12px 20px;
                color: #cdd6f4;
                font-size: 14px;
            }
            QLineEdit:focus {
                border: 1px solid rgba(137, 180, 250, 150);
            }
        """)
        self.inputField.returnPressed.connect(self.sendMessage)
        input_layout.addWidget(self.inputField)
        
        sendBtn = QPushButton("Enviar")
        sendBtn.setStyleSheet("""
            QPushButton {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 rgba(137, 180, 250, 220),
                    stop:1 rgba(116, 199, 236, 220));
                border: none;
                border-radius: 20px;
                padding: 12px 25px;
                color: #1e1e2e;
                font-size: 14px;
                font-weight: 600;
            }
            QPushButton:hover {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 rgba(137, 180, 250, 255),
                    stop:1 rgba(116, 199, 236, 255));
            }
        """)
        sendBtn.clicked.connect(self.sendMessage)
        input_layout.addWidget(sendBtn)
        
        layout.addWidget(input_container)
        
        return panel
    
    def createInfoPanel(self):
        """Cria painel de informações"""
        panel = BlurredWidget()
        layout = QVBoxLayout(panel)
        layout.setContentsMargins(15, 20, 15, 20)
        layout.setSpacing(15)
        
        # Título
        title = QLabel("📊 Informações")
        title.setStyleSheet("""
            color: #cdd6f4;
            font-size: 16px;
            font-weight: 600;
        """)
        layout.addWidget(title)
        
        # Sistema
        system_label = QLabel("🖥️ Sistema")
        system_label.setStyleSheet("color: #a6adc8; font-size: 13px; margin-top: 10px;")
        layout.addWidget(system_label)
        
        self.systemInfo = QLabel("Ubuntu 22.04\nPterodactyl instalado")
        self.systemInfo.setStyleSheet("""
            color: #cdd6f4;
            font-size: 12px;
            padding: 10px;
            background: rgba(49, 50, 68, 150);
            border-radius: 8px;
            margin-bottom: 15px;
        """)
        layout.addWidget(self.systemInfo)
        
        # Arquivos analisados
        files_label = QLabel("📁 Arquivos Analisados")
        files_label.setStyleSheet("color: #a6adc8; font-size: 13px;")
        layout.addWidget(files_label)
        
        self.filesList = QListWidget()
        self.filesList.setStyleSheet("""
            QListWidget {
                background: rgba(49, 50, 68, 150);
                border: 1px solid rgba(148, 226, 213, 30);
                border-radius: 8px;
                color: #cdd6f4;
                font-size: 12px;
                padding: 5px;
            }
            QListWidget::item {
                padding: 8px;
                border-radius: 5px;
            }
            QListWidget::item:hover {
                background: rgba(137, 180, 250, 50);
            }
        """)
        layout.addWidget(self.filesList)
        
        layout.addStretch()
        
        return panel
    
    def applyStyles(self):
        """Aplica estilos globais"""
        self.setStyleSheet("""
            QMainWindow {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
                    stop:0 rgba(17, 17, 27, 255),
                    stop:1 rgba(30, 30, 46, 255));
            }
        """)
    
    def addMessage(self, text, is_user=True):
        """Adiciona mensagem ao chat"""
        print(f"[DEBUG] addMessage: text={text[:50]}..., is_user={is_user}")
        
        bubble = MessageBubble(text, is_user)
        bubble.setVisible(True)  # Forçar visibilidade
        
        print(f"[DEBUG] Bubble created: size={bubble.size()}, visible={bubble.isVisible()}")
        
        # Container para alinhamento
        container = QWidget()
        container.setVisible(True)
        container_layout = QHBoxLayout(container)
        container_layout.setContentsMargins(0, 5, 0, 5)
        
        if is_user:
            container_layout.addStretch()
            container_layout.addWidget(bubble, 0, Qt.AlignmentFlag.AlignRight)
        else:
            container_layout.addWidget(bubble, 0, Qt.AlignmentFlag.AlignLeft)
            container_layout.addStretch()
        
        # Remove stretch temporário
        count = self.messagesLayout.count()
        if count > 0:
            item = self.messagesLayout.takeAt(count - 1)
        
        self.messagesLayout.addWidget(container)
        self.messagesLayout.addStretch()
        
        print(f"[DEBUG] Container added. Total widgets: {self.messagesLayout.count()}")
        
        # Forçar update
        self.messagesWidget.updateGeometry()
        self.scrollArea.updateGeometry()
        
        # Scroll para baixo
        QTimer.singleShot(100, lambda: self.scrollToBottom())
    
    def scrollToBottom(self):
        """Scroll automático para última mensagem"""
        if hasattr(self, 'scrollArea'):
            scrollbar = self.scrollArea.verticalScrollBar()
            scrollbar.setValue(scrollbar.maximum())
    
    def sendMessage(self):
        """Envia mensagem"""
        text = self.inputField.text().strip()
        if not text:
            return
        
        # Adicionar mensagem do usuário
        self.addMessage(text, is_user=True)
        self.inputField.clear()
        
        # Verificar se IA está configurada
        if not self.ai_engine:
            self.addMessage(
                "❌ Engine da IA não está configurado.\n\n"
                "Configure sua API Key do Gemini em:\n"
                "~/.config/ptero-ai-ultra/config.json",
                is_user=False
            )
            return
        
        # Atualizar status e adicionar indicador "digitando..."
        self.setStatus("thinking", "Pensando...")
        self.showTypingIndicator()
        
        # Processar com IA em thread separada
        self.current_worker = AIWorker(self.ai_engine, text)
        self.current_worker.responseReady.connect(self.onAIResponse)
        self.current_worker.start()
    
    def showTypingIndicator(self):
        """Mostra indicador de 'digitando...'"""
        typing_label = QLabel("🤖 Digitando...")
        typing_label.setStyleSheet("""
            QLabel {
                color: #a6adc8;
                font-size: 13px;
                font-style: italic;
                padding: 10px 20px;
                background: transparent;
            }
        """)
        
        # Container
        self.typing_container = QWidget()
        layout = QHBoxLayout(self.typing_container)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.addWidget(typing_label)
        layout.addStretch()
        
        # Remover stretch e adicionar
        count = self.messagesLayout.count()
        if count > 0:
            self.messagesLayout.takeAt(count - 1)
        
        self.messagesLayout.addWidget(self.typing_container)
        self.messagesLayout.addStretch()
        
        QTimer.singleShot(100, self.scrollToBottom)
    
    def hideTypingIndicator(self):
        """Remove indicador de 'digitando...'"""
        if hasattr(self, 'typing_container') and self.typing_container:
            self.messagesLayout.removeWidget(self.typing_container)
            self.typing_container.deleteLater()
            self.typing_container = None
    
    def onAIResponse(self, response):
        """Callback quando IA responde"""
        self.hideTypingIndicator()
        self.addMessage(response, is_user=False)
        self.setStatus("idle", "Pronto")
        self.current_worker = None
    
    def setStatus(self, status, text):
        """Atualiza status"""
        self.ai_status = status
        self.statusIndicator.setStatus(status)
        self.statusText.setText(text)
        
        # Cor do texto baseado no status
        colors = {
            "idle": "#a6e3a1",
            "thinking": "#f9e2af",
            "working": "#89b4fa",
            "error": "#f38ba8"
        }
        self.statusText.setStyleSheet(f"""
            color: {colors.get(status, '#cdd6f4')};
            font-size: 13px;
            font-weight: 500;
        """)
    
    def onTerminalDetected(self, terminal_info):
        """Callback quando terminal é detectado"""
        self.addMessage(f"✅ Terminal detectado!\n\n{terminal_info}\n\nAgora posso executar comandos neste terminal.", is_user=False)
        self.setStatus("idle", "Terminal conectado")


def main():
    app = QApplication(sys.argv)
    
    # Fonte personalizada
    font = QFont("SF Pro Display", 13)
    app.setFont(font)
    
    # Criar e mostrar janela
    window = ChatInterface()
    window.show()
    
    # Mensagem de boas-vindas
    QTimer.singleShot(500, lambda: window.addMessage(
        "👋 Olá! Sou a PTERO-AI Ultra Pro.\n\n"
        "Vou te ajudar a gerenciar seu Pterodactyl com segurança máxima.\n\n"
        "Digite algo no terminal que você quer que eu controle, "
        "ou simplesmente converse comigo!", 
        is_user=False
    ))
    
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
