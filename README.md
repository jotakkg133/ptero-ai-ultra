# 🚀 PTERO-AI Ultra Pro

<div align="center">

![Version](https://img.shields.io/badge/version-2.0.0-blue.svg)
![Python](https://img.shields.io/badge/python-3.8+-brightgreen.svg)
![License](https://img.shields.io/badge/license-MIT-green.svg)
![Platform](https://img.shields.io/badge/platform-Ubuntu%2020.04%2B-orange.svg)

**Interface Gráfica Moderna com IA para Gerenciamento Pterodactyl**

[Instalação](#-instalação-rápida) • [Recursos](#-recursos) • [Como Usar](#-como-usar) • [Screenshots](#-screenshots) • [Documentação](#-documentação)

</div>

---

## 🎯 Sobre

**PTERO-AI Ultra Pro** é uma interface gráfica moderna estilo macOS que usa Inteligência Artificial (Google Gemini) para ajudar você a gerenciar e editar código do Pterodactyl Panel com **segurança máxima**.

### ✨ Destaques

- 🎨 **Interface Moderna**: Design estilo macOS com blur, transparência e animações
- 🧠 **IA Ultra Inteligente**: Analisa código profundamente antes de editar
- 🔒 **Segurança Máxima**: 5 camadas de validação + backup automático
- 🖥️ **Detecção de Terminal**: Identifica e executa comandos automaticamente
- 💬 **Chat Interativo**: Converse naturalmente com a IA
- 📊 **Análise Profunda**: Identifica zonas seguras e perigosas no código

---

## 📦 Instalação Rápida

### Método 1: One-Liner (Recomendado)

```bash
curl -fsSL https://raw.githubusercontent.com/jotakkg133/ptero-ai-ultra/main/install.sh | sudo bash
```

### Método 2: Manual

```bash
# Clone o repositório
git clone https://github.com/jotakkg133/ptero-ai-ultra.git
cd ptero-ai-ultra

# Execute o instalador
sudo bash install.sh
```

### Método 3: Pacote .deb

```bash
# Baixe o pacote
wget https://github.com/jotakkg133/ptero-ai-ultra/releases/latest/download/ptero-ai-ultra_2.0.0_amd64.deb

# Instale
sudo dpkg -i ptero-ai-ultra_2.0.0_amd64.deb
sudo apt-get install -f
```

---

## 🚀 Como Usar

### Iniciar a Interface

```bash
# Comando global (após instalação)
ptero-ai

# Ou via menu de aplicações
Ubuntu Menu → PTERO-AI Ultra Pro
```

### Uso Básico

1. **Inicie a detecção de terminal**
   - Clique em "▶ Iniciar Detecção"
   - Digite algo no terminal que deseja controlar
   - IA detecta automaticamente

2. **Converse com a IA**
   ```
   Você: analisa o arquivo PluginCard.tsx
   IA: [Análise profunda com 95% de compreensão]
   
   Você: adiciona um botão de compartilhar
   IA: [Plano de execução detalhado]
   
   Você: pode aplicar
   IA: [Executa com backup e validação]
   ```

3. **Comandos úteis**
   - `status` - Status do sistema
   - `listar arquivos` - Arquivos analisados
   - `backup` - Backup manual
   - `rollback` - Desfazer última mudança
   - `ajuda` - Lista de comandos

---

## ✨ Recursos

### Interface Gráfica

- 🎨 Design estilo macOS (Catppuccin Mocha)
- 💫 Blur de fundo e transparência
- 🔄 Logo animado (girando + pulsando)
- 💬 Chat com bolhas estilo iMessage
- 📊 3 painéis: Sidebar, Chat, Info
- 🎯 Indicadores de status em tempo real

### Inteligência Artificial

- 📖 **Análise Profunda**: Lê e entende código completamente
- 🎯 **Zonas Seguras**: Identifica onde pode editar sem riscos
- ⚠️ **Zonas Perigosas**: Evita áreas críticas automaticamente
- 🔍 **5 Camadas de Validação**:
  1. Sintaxe
  2. Segurança
  3. Dependências
  4. Impacto
  5. Validação IA
- 📊 **Score de Confiança**: 0-100% de compreensão
- 🛡️ **Score de Segurança**: 0-20 pontos (5 níveis)

### Segurança

- 💾 **Backup Automático**: Antes de cada mudança
- 🔄 **Rollback Fácil**: Desfaz com um comando
- 🛡️ **Validação Multi-Camadas**: Nunca quebra código
- 📝 **Histórico Completo**: Rastreamento de todas as ações
- 🔒 **Análise de Risco**: Pontua cada operação

---

## 📸 Screenshots

### Interface Principal
![Main Interface](docs/screenshots/main-interface.png)

### Análise de Código
![Code Analysis](docs/screenshots/code-analysis.png)

### Chat Interativo
![Interactive Chat](docs/screenshots/chat.png)

---

## 📋 Requisitos

- **Sistema**: Ubuntu 20.04+ ou Debian 11+
- **Python**: 3.8 ou superior
- **RAM**: Mínimo 2GB (recomendado 4GB)
- **Espaço em disco**: 500MB
- **Servidor X11**: Para interface gráfica
- **Internet**: Para comunicação com Google Gemini API

### Dependências (instaladas automaticamente)

- Python3, pip, venv
- Qt6, PyQt6
- google-generativeai
- libxcb, dbus-x11

---

## 🛠️ Configuração

### API Key do Gemini

1. Obtenha sua API key em: https://makersuite.google.com/app/apikey
2. Configure no arquivo: `~/.config/ptero-ai-ultra/config.json`

```json
{
    "gemini_api_key": "SUA_API_KEY_AQUI",
    "theme": "dark",
    "blur_enabled": true,
    "transparency": 0.95,
    "auto_backup": true,
    "safety_level": "maximum"
}
```

### Personalização

Edite `~/.config/ptero-ai-ultra/config.json`:

| Opção | Valores | Descrição |
|-------|---------|-----------|
| `theme` | `dark`, `light` | Tema da interface |
| `blur_enabled` | `true`, `false` | Efeito blur |
| `transparency` | `0.0` - `1.0` | Nível de transparência |
| `animation_speed` | `slow`, `normal`, `fast` | Velocidade das animações |
| `safety_level` | `low`, `medium`, `high`, `maximum` | Nível de proteção |

---

## 📖 Documentação

- [Guia Visual Completo](docs/GUIA_VISUAL.md)
- [Análise Profunda Explicada](docs/ANALISE_PROFUNDA.md)
- [Exemplos de Uso](docs/EXEMPLOS.md)
- [Solução de Problemas](docs/TROUBLESHOOTING.md)
- [API Reference](docs/API.md)

---

## 🤝 Contribuindo

Contribuições são bem-vindas! Veja [CONTRIBUTING.md](CONTRIBUTING.md) para detalhes.

1. Fork o projeto
2. Crie uma branch: `git checkout -b feature/NovaFuncionalidade`
3. Commit: `git commit -m 'Adiciona nova funcionalidade'`
4. Push: `git push origin feature/NovaFuncionalidade`
5. Abra um Pull Request

---

## 🐛 Reportar Bugs

Encontrou um bug? Abra uma [issue](https://github.com/jotakkg133/ptero-ai-ultra/issues) com:

- Descrição do problema
- Passos para reproduzir
- Sistema operacional e versão
- Logs (em `~/.config/ptero-ai-ultra/logs/`)

---

## 📝 Changelog

### v2.0.0 (2025-01-19)
- 🎨 Interface gráfica moderna estilo macOS
- 🧠 Sistema de análise profunda de código
- 🔒 5 camadas de validação de segurança
- 🖥️ Detecção automática de terminal
- 💬 Chat interativo com IA
- 📊 Painel de informações em tempo real

### v1.0.0 (2025-01-10)
- Primeira versão via linha de comando
- Integração com Gemini API
- Sistema básico de backup

---

## 📜 Licença

Este projeto está sob a licença MIT. Veja [LICENSE](LICENSE) para detalhes.

---

## 👤 Autor

**jotakkg133**

- GitHub: [@jotakkg133](https://github.com/jotakkg133)
- Gist: [gist:18d0e2b328d4d0cacbf025e2a1721eeb](https://gist.github.com/jotakkg133/18d0e2b328d4d0cacbf025e2a1721eeb)

---

## 🙏 Agradecimentos

- **Google Gemini**: API de IA incrível
- **Qt Project**: Framework Qt6
- **Catppuccin**: Palette de cores
- **Pterodactyl**: Painel de gerenciamento

---

## ⭐ Star History

[![Star History Chart](https://api.star-history.com/svg?repos=jotakkg133/ptero-ai-ultra&type=Date)](https://star-history.com/#jotakkg133/ptero-ai-ultra&Date)

---

## 🔗 Links Úteis

- [Website](https://ptero-ai-ultra.dev)
- [Documentação](https://docs.ptero-ai-ultra.dev)
- [Discord](https://discord.gg/ptero-ai-ultra)
- [YouTube](https://youtube.com/@ptero-ai-ultra)

---

<div align="center">

**Feito com ❤️ e muito ☕**

[⬆ Voltar ao topo](#-ptero-ai-ultra-pro)

</div>
