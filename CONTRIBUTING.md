# 🤝 Contribuindo para PTERO-AI Ultra Pro

Obrigado por considerar contribuir para o PTERO-AI Ultra Pro! 🎉

## 📋 Índice

- [Como Contribuir](#como-contribuir)
- [Reportar Bugs](#reportar-bugs)
- [Sugerir Funcionalidades](#sugerir-funcionalidades)
- [Pull Requests](#pull-requests)
- [Padrões de Código](#padrões-de-código)
- [Estrutura do Projeto](#estrutura-do-projeto)

---

## Como Contribuir

### 1️⃣ Fork o Repositório

```bash
# Clique em "Fork" no GitHub
# Clone seu fork
git clone https://github.com/SEU_USUARIO/ptero-ai-ultra.git
cd ptero-ai-ultra
```

### 2️⃣ Crie uma Branch

```bash
# Para nova funcionalidade
git checkout -b feature/nome-da-funcionalidade

# Para correção de bug
git checkout -b fix/nome-do-bug

# Para documentação
git checkout -b docs/melhoria-docs
```

### 3️⃣ Faça suas Mudanças

- Escreva código limpo e bem comentado
- Siga os padrões de código do projeto
- Teste suas mudanças
- Atualize documentação se necessário

### 4️⃣ Commit

```bash
git add .
git commit -m "feat: adiciona nova funcionalidade X"
```

**Padrão de commits:**
- `feat:` Nova funcionalidade
- `fix:` Correção de bug
- `docs:` Documentação
- `style:` Formatação
- `refactor:` Refatoração
- `test:` Testes
- `chore:` Manutenção

### 5️⃣ Push e Pull Request

```bash
git push origin feature/nome-da-funcionalidade
```

Abra um Pull Request no GitHub com:
- Título descritivo
- Descrição detalhada das mudanças
- Screenshots se aplicável
- Referência a issues relacionadas

---

## 🐛 Reportar Bugs

Encontrou um bug? Abra uma [issue](https://github.com/jotakkg133/ptero-ai-ultra/issues) incluindo:

### Informações Necessárias:

```markdown
## Descrição do Bug
[Descreva o bug claramente]

## Como Reproduzir
1. Abra a aplicação
2. Clique em '...'
3. Digite '...'
4. Veja o erro

## Comportamento Esperado
[O que deveria acontecer]

## Comportamento Atual
[O que está acontecendo]

## Screenshots
[Se aplicável]

## Ambiente
- OS: Ubuntu 22.04
- Python: 3.10.6
- Versão: 2.0.0
- Qt: 6.2.4

## Logs
[Cole logs de ~/.config/ptero-ai-ultra/logs/]
```

---

## 💡 Sugerir Funcionalidades

Tem uma ideia? Abra uma [issue](https://github.com/jotakkg133/ptero-ai-ultra/issues) com:

```markdown
## Funcionalidade Proposta
[Descrição clara da funcionalidade]

## Motivação
[Por que isso seria útil?]

## Exemplo de Uso
[Como você usaria isso?]

## Alternativas Consideradas
[Outras abordagens que você pensou]
```

---

## 🔀 Pull Requests

### Checklist:

- [ ] Código segue os padrões do projeto
- [ ] Comentários claros em código complexo
- [ ] Documentação atualizada
- [ ] Testes passando (se aplicável)
- [ ] Sem conflitos com `main`
- [ ] Commit messages descritivos

### Processo de Review:

1. Mantenedor revisa o PR
2. Discussão e ajustes se necessário
3. Aprovação
4. Merge para `main`

---

## 📝 Padrões de Código

### Python

```python
# Use docstrings
def minha_funcao(param1: str, param2: int) -> bool:
    """
    Descrição breve da função.
    
    Args:
        param1: Descrição do parâmetro 1
        param2: Descrição do parâmetro 2
    
    Returns:
        True se sucesso, False caso contrário
    """
    pass

# Type hints sempre que possível
def processar_dados(dados: List[Dict]) -> Optional[str]:
    pass

# Nomes descritivos
nome_arquivo = "config.json"  # ✅
f = "config.json"             # ❌

# Constantes em UPPERCASE
MAX_RETRIES = 3
API_TIMEOUT = 30
```

### Estrutura de Classes

```python
class MinhaClasse:
    """Docstring da classe."""
    
    def __init__(self, param: str):
        """Construtor."""
        self.param = param
        self._private = None
    
    def metodo_publico(self) -> None:
        """Método público."""
        pass
    
    def _metodo_privado(self) -> None:
        """Método privado (convenção)."""
        pass
```

### Qt/PyQt6

```python
# Nomenclatura de widgets
self.btnSend = QPushButton("Enviar")      # ✅
self.button1 = QPushButton("Enviar")      # ❌

# Conexões de sinais
self.btnSend.clicked.connect(self.sendMessage)

# Estilos inline para testes, arquivo CSS para produção
self.widget.setStyleSheet("""
    QWidget {
        background: rgba(30, 30, 46, 230);
        border-radius: 10px;
    }
""")
```

---

## 📁 Estrutura do Projeto

```
ptero-ai-ultra/
├── ptero_ai_gui.py           # Interface gráfica principal
├── ptero_ai_ultra_pro.py     # Engine de IA
├── svg_icons.py              # Ícones SVG
├── install.sh                # Instalador
├── build-deb.sh              # Builder .deb
├── README.md                 # Documentação principal
├── LICENSE                   # Licença MIT
├── CONTRIBUTING.md           # Este arquivo
├── docs/                     # Documentação adicional
│   ├── GUIA_VISUAL.md
│   ├── ANALISE_PROFUNDA.md
│   └── screenshots/
├── tests/                    # Testes (futuro)
└── .github/                  # GitHub configs
    ├── workflows/
    └── ISSUE_TEMPLATE/
```

---

## 🧪 Testes

### Executar Testes (quando disponível)

```bash
# Instalar dependências de teste
pip install pytest pytest-qt

# Executar todos os testes
pytest

# Executar teste específico
pytest tests/test_gui.py

# Com cobertura
pytest --cov=ptero_ai_ultra_pro
```

### Criar Novos Testes

```python
# tests/test_exemplo.py
import pytest
from ptero_ai_ultra_pro import CodeAnalyzer

def test_code_analyzer_init():
    """Testa inicialização do CodeAnalyzer."""
    analyzer = CodeAnalyzer(model=None)
    assert analyzer is not None

def test_detect_language():
    """Testa detecção de linguagem."""
    analyzer = CodeAnalyzer(model=None)
    assert analyzer._detect_language("test.py") == "python"
    assert analyzer._detect_language("test.tsx") == "typescript"
```

---

## 📚 Documentação

### Atualizar Documentação

Se sua mudança afeta o uso:
1. Atualize README.md
2. Atualize docs/ se necessário
3. Adicione exemplos
4. Atualize screenshots

### Exemplo de Documentação:

```markdown
## Nova Funcionalidade X

### Como Usar

1. Abra a interface
2. Clique em "X"
3. Configure Y
4. Execute Z

### Exemplo

\`\`\`python
# Código de exemplo
resultado = funcionalidade_x(parametro)
\`\`\`

### Screenshot

![Funcionalidade X](docs/screenshots/funcionalidade-x.png)
```

---

## 🎨 UI/UX

### Contribuindo com Interface

- Mantenha consistência com tema Catppuccin
- Use animações suaves (300ms padrão)
- Blur radius: 20px
- Border radius: 10-20px
- Transparência: 0.9-0.95

### Cores (Catppuccin Mocha)

```python
COLORS = {
    'base': '#1e1e2e',
    'surface': '#313244',
    'overlay': '#45475a',
    'text': '#cdd6f4',
    'subtext': '#a6adc8',
    'blue': '#89b4fa',
    'green': '#a6e3a1',
    'yellow': '#f9e2af',
    'red': '#f38ba8',
    'purple': '#cba6f7',
}
```

---

## 🌍 Traduções

Interessado em traduzir?

1. Copie `i18n/en.json`
2. Traduza strings
3. Salve como `i18n/SEU_IDIOMA.json`
4. Abra PR

---

## 📧 Contato

- **GitHub Issues**: Para bugs e features
- **Discussions**: Para perguntas gerais
- **Email**: jotakkg@example.com

---

## 🙏 Reconhecimento

Contribuidores serão listados em:
- README.md (seção Contributors)
- CHANGELOG.md
- Release notes

---

## ⚖️ Código de Conduta

### Nosso Compromisso

Criar um ambiente acolhedor e respeitoso para todos.

### Comportamento Esperado

- ✅ Seja respeitoso e inclusivo
- ✅ Aceite críticas construtivas
- ✅ Foque no que é melhor para o projeto
- ✅ Mostre empatia

### Comportamento Inaceitável

- ❌ Linguagem ofensiva
- ❌ Trolling ou comentários depreciativos
- ❌ Assédio público ou privado
- ❌ Spam

---

<div align="center">

**Obrigado por contribuir! 🎉**

[⬆ Voltar ao topo](#-contribuindo-para-ptero-ai-ultra-pro)

</div>
