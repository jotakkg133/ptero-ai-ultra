#!/bin/bash
#
# Build .deb package for PTERO-AI Ultra Pro
# Creates native Ubuntu/Debian installer
#

set -e

VERSION="2.0.0"
ARCH="amd64"
PACKAGE_NAME="ptero-ai-ultra"
BUILD_DIR="build/${PACKAGE_NAME}_${VERSION}_${ARCH}"

echo "🔨 Building .deb package..."
echo ""

# Limpar build anterior
rm -rf build/
mkdir -p $BUILD_DIR

# Criar estrutura DEBIAN
mkdir -p $BUILD_DIR/DEBIAN
mkdir -p $BUILD_DIR/opt/ptero-ai-ultra
mkdir -p $BUILD_DIR/usr/share/applications
mkdir -p $BUILD_DIR/usr/share/doc/ptero-ai-ultra
mkdir -p $BUILD_DIR/usr/local/bin

# Copiar arquivos da aplicação
echo "📦 Copiando arquivos..."
cp ptero_ai_gui.py $BUILD_DIR/opt/ptero-ai-ultra/
cp ptero_ai_ultra_pro.py $BUILD_DIR/opt/ptero-ai-ultra/
cp svg_icons.py $BUILD_DIR/opt/ptero-ai-ultra/
cp README.md $BUILD_DIR/usr/share/doc/ptero-ai-ultra/

# Criar control file
cat > $BUILD_DIR/DEBIAN/control << EOF
Package: ptero-ai-ultra
Version: $VERSION
Section: devel
Priority: optional
Architecture: $ARCH
Depends: python3 (>= 3.8), python3-pip, python3-venv, qt6-base-dev, libqt6svg6, libqt6widgets6, python3-pyqt6, python3-pyqt6.qtsvg, libxcb-xinerama0, libxcb-cursor0, libxkbcommon-x11-0, x11-apps, dbus-x11
Maintainer: jotakkg133 <jotakkg@example.com>
Homepage: https://github.com/jotakkg133/ptero-ai-ultra
Description: Interface gráfica com IA para gerenciamento Pterodactyl
 PTERO-AI Ultra Pro é uma interface moderna estilo macOS que usa
 Inteligência Artificial (Google Gemini) para gerenciar código do
 Pterodactyl Panel com segurança máxima.
 .
 Recursos:
  - Interface moderna com blur e transparência
  - Chat interativo com IA
  - Detecção automática de terminal
  - Análise profunda de código
  - 5 camadas de validação
  - Backup automático
EOF

# Criar postinst script
cat > $BUILD_DIR/DEBIAN/postinst << 'EOF'
#!/bin/bash
set -e

INSTALL_DIR="/opt/ptero-ai-ultra"
CONFIG_DIR="/home/$SUDO_USER/.config/ptero-ai-ultra"

echo "🔧 Configurando PTERO-AI Ultra Pro..."

# Criar ambiente virtual
cd $INSTALL_DIR
python3 -m venv venv
source venv/bin/activate
pip install --upgrade pip > /dev/null 2>&1
pip install PyQt6 google-generativeai requests > /dev/null 2>&1
deactivate

# Criar diretórios de configuração
mkdir -p $CONFIG_DIR/logs
mkdir -p $CONFIG_DIR/cache
mkdir -p /home/$SUDO_USER/ptero_ultra_backups

# Criar config.json
if [ ! -f "$CONFIG_DIR/config.json" ]; then
    cat > $CONFIG_DIR/config.json << 'CONFIGEOF'
{
    "gemini_api_key": "",
    "theme": "dark",
    "blur_enabled": true,
    "transparency": 0.95,
    "animation_speed": "normal",
    "auto_backup": true,
    "backup_dir": "~/ptero_ultra_backups",
    "terminal_detection": true,
    "safety_level": "maximum"
}
CONFIGEOF
fi

# Ajustar permissões
chown -R $SUDO_USER:$SUDO_USER $CONFIG_DIR
chown -R $SUDO_USER:$SUDO_USER /home/$SUDO_USER/ptero_ultra_backups

# Criar launcher
cat > $INSTALL_DIR/ptero-ai-ultra << 'LAUNCHEREOF'
#!/bin/bash
source /opt/ptero-ai-ultra/venv/bin/activate
export DISPLAY=${DISPLAY:-:0}
cd /opt/ptero-ai-ultra
python3 ptero_ai_gui.py "$@"
LAUNCHEREOF

chmod +x $INSTALL_DIR/ptero-ai-ultra
ln -sf $INSTALL_DIR/ptero-ai-ultra /usr/local/bin/ptero-ai

# Desktop entry
cat > /usr/share/applications/ptero-ai-ultra.desktop << 'DESKTOPEOF'
[Desktop Entry]
Version=1.0
Type=Application
Name=PTERO-AI Ultra Pro
Comment=Interface gráfica com IA para Pterodactyl
Exec=/usr/local/bin/ptero-ai
Icon=utilities-terminal
Terminal=false
Categories=Development;Utility;
DESKTOPEOF

update-desktop-database > /dev/null 2>&1 || true

echo "✅ PTERO-AI Ultra Pro instalado com sucesso!"
echo ""
echo "Execute: ptero-ai"
echo ""

exit 0
EOF

chmod +x $BUILD_DIR/DEBIAN/postinst

# Criar prerm script
cat > $BUILD_DIR/DEBIAN/prerm << 'EOF'
#!/bin/bash
set -e

echo "🗑️  Removendo PTERO-AI Ultra Pro..."

rm -f /usr/local/bin/ptero-ai
rm -f /usr/share/applications/ptero-ai-ultra.desktop
update-desktop-database > /dev/null 2>&1 || true

exit 0
EOF

chmod +x $BUILD_DIR/DEBIAN/prerm

# Criar desktop entry
cat > $BUILD_DIR/usr/share/applications/ptero-ai-ultra.desktop << EOF
[Desktop Entry]
Version=1.0
Type=Application
Name=PTERO-AI Ultra Pro
GenericName=AI Code Manager
Comment=Interface gráfica com IA para Pterodactyl
Exec=/usr/local/bin/ptero-ai
Icon=utilities-terminal
Terminal=false
Categories=Development;Utility;IDE;
Keywords=ai;pterodactyl;automation;
StartupNotify=true
EOF

# Criar copyright
cat > $BUILD_DIR/usr/share/doc/ptero-ai-ultra/copyright << EOF
Format: https://www.debian.org/doc/packaging-manuals/copyright-format/1.0/
Upstream-Name: ptero-ai-ultra
Source: https://github.com/jotakkg133/ptero-ai-ultra

Files: *
Copyright: 2025 jotakkg133
License: MIT
 Permission is hereby granted, free of charge, to any person obtaining a
 copy of this software and associated documentation files (the "Software"),
 to deal in the Software without restriction, including without limitation
 the rights to use, copy, modify, merge, publish, distribute, sublicense,
 and/or sell copies of the Software, and to permit persons to whom the
 Software is furnished to do so, subject to the following conditions:
 .
 The above copyright notice and this permission notice shall be included
 in all copies or substantial portions of the Software.
EOF

# Criar changelog
cat > $BUILD_DIR/usr/share/doc/ptero-ai-ultra/changelog << EOF
ptero-ai-ultra ($VERSION) stable; urgency=medium

  * Initial release
  * Interface gráfica moderna estilo macOS
  * Sistema de análise profunda de código
  * 5 camadas de validação de segurança
  * Detecção automática de terminal
  * Chat interativo com IA

 -- jotakkg133 <jotakkg@example.com>  $(date -R)
EOF

gzip -9 $BUILD_DIR/usr/share/doc/ptero-ai-ultra/changelog

# Calcular tamanho instalado
INSTALLED_SIZE=$(du -sk $BUILD_DIR | cut -f1)
echo "Installed-Size: $INSTALLED_SIZE" >> $BUILD_DIR/DEBIAN/control

# Ajustar permissões
find $BUILD_DIR -type d -exec chmod 755 {} \;
find $BUILD_DIR -type f -exec chmod 644 {} \;
chmod 755 $BUILD_DIR/DEBIAN/postinst
chmod 755 $BUILD_DIR/DEBIAN/prerm

# Construir pacote
echo "🔨 Construindo pacote .deb..."
dpkg-deb --build $BUILD_DIR

# Mover para diretório releases
mkdir -p releases
mv build/${PACKAGE_NAME}_${VERSION}_${ARCH}.deb releases/

echo ""
echo "✅ Pacote criado: releases/${PACKAGE_NAME}_${VERSION}_${ARCH}.deb"
echo ""
echo "📦 Para instalar:"
echo "   sudo dpkg -i releases/${PACKAGE_NAME}_${VERSION}_${ARCH}.deb"
echo "   sudo apt-get install -f"
echo ""
