#!/bin/bash
#
# PTERO-AI Ultra Pro - Instalador Oficial
# Instalação automática estilo AnyDesk
# Suporta: Ubuntu 20.04+, Debian 11+
#

set -e

# Cores
RED='\033[0;31m'
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
PURPLE='\033[0;35m'
CYAN='\033[0;36m'
NC='\033[0m'

# Configurações
VERSION="2.0.0"
INSTALL_DIR="/opt/ptero-ai-ultra"
CONFIG_DIR="$HOME/.config/ptero-ai-ultra"
REPO_URL="https://raw.githubusercontent.com/jotakkg133/ptero-ai-ultra/main"

# Banner
show_banner() {
    clear
    echo -e "${PURPLE}"
    cat << "EOF"
╔═══════════════════════════════════════════════════════════╗
║                                                           ║
║     ██████╗ ████████╗███████╗██████╗  ██████╗            ║
║     ██╔══██╗╚══██╔══╝██╔════╝██╔══██╗██╔═══██╗           ║
║     ██████╔╝   ██║   █████╗  ██████╔╝██║   ██║           ║
║     ██╔═══╝    ██║   ██╔══╝  ██╔══██╗██║   ██║           ║
║     ██║        ██║   ███████╗██║  ██║╚██████╔╝           ║
║     ╚═╝        ╚═╝   ╚══════╝╚═╝  ╚═╝ ╚═════╝            ║
║                                                           ║
║              AI ULTRA PRO - INSTALLER                     ║
║                    v2.0.0                                 ║
║                                                           ║
╚═══════════════════════════════════════════════════════════╝
EOF
    echo -e "${NC}"
}

# Verificar root
check_root() {
    if [ "$EUID" -ne 0 ]; then 
        echo -e "${RED}[✗] Este instalador precisa de permissões root${NC}"
        echo -e "${YELLOW}[!] Execute: sudo $0${NC}"
        exit 1
    fi
}

# Detectar sistema
detect_system() {
    if [ -f /etc/os-release ]; then
        . /etc/os-release
        OS=$NAME
        VER=$VERSION_ID
    else
        echo -e "${RED}[✗] Sistema não suportado${NC}"
        exit 1
    fi
    
    echo -e "${CYAN}[*] Sistema detectado: $OS $VER${NC}"
}

# Verificar dependências
check_dependencies() {
    echo -e "${BLUE}[1/8] Verificando dependências...${NC}"
    
    local missing=""
    
    if ! command -v python3 &> /dev/null; then
        missing="$missing python3"
    fi
    
    if ! command -v pip3 &> /dev/null; then
        missing="$missing python3-pip"
    fi
    
    if [ -n "$missing" ]; then
        echo -e "${YELLOW}[!] Instalando dependências faltantes...${NC}"
        apt update -qq
        apt install -y $missing > /dev/null 2>&1
    fi
    
    echo -e "${GREEN}[✓] Dependências verificadas${NC}"
}

# Instalar pacotes do sistema
install_system_packages() {
    echo -e "${BLUE}[2/8] Instalando pacotes do sistema...${NC}"
    
    apt update -qq
    
    # Instalar bibliotecas Qt e X11 necessárias
    DEBIAN_FRONTEND=noninteractive apt install -y \
        python3 \
        python3-pip \
        python3-venv \
        libxcb-xinerama0 \
        libxcb-cursor0 \
        libxcb-icccm4 \
        libxcb-image0 \
        libxcb-keysyms1 \
        libxcb-randr0 \
        libxcb-render-util0 \
        libxcb-shape0 \
        libxkbcommon-x11-0 \
        libxcb1 \
        libx11-xcb1 \
        libgl1-mesa-glx \
        libdbus-1-3 \
        x11-apps \
        dbus-x11 \
        procps \
        psmisc \
        wmctrl \
        xdotool \
        curl \
        wget \
        git > /dev/null 2>&1
    
    echo -e "${GREEN}[✓] Pacotes instalados${NC}"
}

# Criar estrutura de diretórios
create_directories() {
    echo -e "${BLUE}[3/8] Criando diretórios...${NC}"
    
    mkdir -p $INSTALL_DIR
    mkdir -p $CONFIG_DIR
    mkdir -p $CONFIG_DIR/logs
    mkdir -p $CONFIG_DIR/cache
    mkdir -p $HOME/ptero_ultra_backups
    
    echo -e "${GREEN}[✓] Diretórios criados${NC}"
}

# Baixar arquivos
download_files() {
    echo -e "${BLUE}[4/8] Baixando arquivos...${NC}"
    
    cd $INSTALL_DIR
    
    # Arquivos principais
    curl -fsSL $REPO_URL/ptero_ai_gui.py -o ptero_ai_gui.py
    curl -fsSL $REPO_URL/ptero_ai_ultra_pro.py -o ptero_ai_ultra_pro.py
    curl -fsSL $REPO_URL/svg_icons.py -o svg_icons.py
    
    chmod +x ptero_ai_gui.py ptero_ai_ultra_pro.py
    
    echo -e "${GREEN}[✓] Arquivos baixados${NC}"
}

# Configurar ambiente Python
setup_python_env() {
    echo -e "${BLUE}[5/8] Configurando ambiente Python...${NC}"
    
    cd $INSTALL_DIR
    
    # Criar venv
    python3 -m venv venv
    source venv/bin/activate
    
    # Atualizar pip
    pip install --upgrade pip > /dev/null 2>&1
    
    # Instalar pacotes Python (PyQt6 via pip já que Ubuntu 22.04 não tem no apt)
    pip install \
        PyQt6 \
        PyQt6-Qt6 \
        PyQt6-sip \
        google-generativeai \
        requests > /dev/null 2>&1
    
    deactivate
    
    echo -e "${GREEN}[✓] Ambiente Python configurado${NC}"
}

# Criar arquivos de configuração
create_config() {
    echo -e "${BLUE}[6/8] Criando configuração...${NC}"
    
    if [ ! -f "$CONFIG_DIR/config.json" ]; then
        cat > $CONFIG_DIR/config.json << 'EOF'
{
    "gemini_api_key": "",
    "theme": "dark",
    "blur_enabled": true,
    "transparency": 0.95,
    "animation_speed": "normal",
    "auto_backup": true,
    "backup_dir": "~/ptero_ultra_backups",
    "terminal_detection": true,
    "safety_level": "maximum",
    "log_level": "info"
}
EOF
    fi
    
    echo -e "${GREEN}[✓] Configuração criada${NC}"
}

# Criar script de inicialização
create_launcher() {
    echo -e "${BLUE}[7/8] Criando launcher...${NC}"
    
    # Script de inicialização
    cat > $INSTALL_DIR/ptero-ai-ultra << 'EOF'
#!/bin/bash
# PTERO-AI Ultra Pro Launcher

# Ativar venv
source /opt/ptero-ai-ultra/venv/bin/activate

# Configurar DISPLAY
if [ -z "$DISPLAY" ]; then
    export DISPLAY=:0
fi

# Configurar XDG
export XDG_RUNTIME_DIR=/run/user/$(id -u)

# Iniciar aplicação
cd /opt/ptero-ai-ultra
python3 ptero_ai_gui.py "$@"
EOF
    
    chmod +x $INSTALL_DIR/ptero-ai-ultra
    
    # Link simbólico global
    ln -sf $INSTALL_DIR/ptero-ai-ultra /usr/local/bin/ptero-ai
    
    # Desktop entry
    cat > /usr/share/applications/ptero-ai-ultra.desktop << 'EOF'
[Desktop Entry]
Version=1.0
Type=Application
Name=PTERO-AI Ultra Pro
GenericName=AI Code Manager
Comment=Interface gráfica com IA para gerenciamento Pterodactyl
Exec=/usr/local/bin/ptero-ai
Icon=utilities-terminal
Terminal=false
Categories=Development;Utility;IDE;
Keywords=ai;pterodactyl;automation;code;development;
StartupNotify=true
EOF
    
    # Atualizar cache de aplicações
    update-desktop-database > /dev/null 2>&1 || true
    
    echo -e "${GREEN}[✓] Launcher criado${NC}"
}

# Finalizar instalação
finalize() {
    echo -e "${BLUE}[8/8] Finalizando...${NC}"
    
    # Ajustar permissões
    chown -R $SUDO_USER:$SUDO_USER $CONFIG_DIR
    chown -R $SUDO_USER:$SUDO_USER $HOME/ptero_ultra_backups
    
    # Criar arquivo de versão
    echo "$VERSION" > $INSTALL_DIR/VERSION
    
    echo -e "${GREEN}[✓] Instalação finalizada${NC}"
}

# Mostrar informações pós-instalação
show_info() {
    echo ""
    echo -e "${GREEN}╔════════════════════════════════════════════════════╗${NC}"
    echo -e "${GREEN}║                                                    ║${NC}"
    echo -e "${GREEN}║  ✓  Instalação concluída com sucesso!             ║${NC}"
    echo -e "${GREEN}║                                                    ║${NC}"
    echo -e "${GREEN}╚════════════════════════════════════════════════════╝${NC}"
    echo ""
    echo -e "${CYAN}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
    echo -e "${YELLOW}  COMO USAR${NC}"
    echo -e "${CYAN}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
    echo ""
    echo -e "  ${GREEN}1.${NC} Configure sua API Key do Gemini:"
    echo -e "     ${BLUE}nano ~/.config/ptero-ai-ultra/config.json${NC}"
    echo -e "     ${YELLOW}Obtenha em: https://makersuite.google.com/app/apikey${NC}"
    echo ""
    echo -e "  ${GREEN}2.${NC} Inicie a aplicação:"
    echo -e "     ${BLUE}ptero-ai${NC}"
    echo ""
    echo -e "  ${GREEN}3.${NC} Ou via menu de aplicações:"
    echo -e "     ${BLUE}Menu → PTERO-AI Ultra Pro${NC}"
    echo ""
    echo -e "${CYAN}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
    echo -e "${YELLOW}  RECURSOS${NC}"
    echo -e "${CYAN}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
    echo ""
    echo -e "  ${GREEN}✓${NC} Interface gráfica moderna com blur"
    echo -e "  ${GREEN}✓${NC} Chat interativo com IA"
    echo -e "  ${GREEN}✓${NC} Detecção automática de terminal"
    echo -e "  ${GREEN}✓${NC} Análise profunda de código"
    echo -e "  ${GREEN}✓${NC} 5 camadas de validação"
    echo -e "  ${GREEN}✓${NC} Backup automático"
    echo -e "  ${GREEN}✓${NC} Segurança máxima"
    echo ""
    echo -e "${CYAN}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
    echo -e "${YELLOW}  SUPORTE${NC}"
    echo -e "${CYAN}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
    echo ""
    echo -e "  ${BLUE}Documentação:${NC} https://github.com/jotakkg133/ptero-ai-ultra"
    echo -e "  ${BLUE}Issues:${NC} https://github.com/jotakkg133/ptero-ai-ultra/issues"
    echo -e "  ${BLUE}Gist:${NC} https://gist.github.com/jotakkg133/18d0e2b328d4d0cacbf025e2a1721eeb"
    echo ""
    echo -e "${PURPLE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
    echo ""
}

# Função principal
main() {
    show_banner
    check_root
    detect_system
    check_dependencies
    install_system_packages
    create_directories
    download_files
    setup_python_env
    create_config
    create_launcher
    finalize
    show_info
}

# Executar
main
