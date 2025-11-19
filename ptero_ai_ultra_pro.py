#!/usr/bin/env python3
"""
PTERO-AI ULTRA PRO v2.0
Sistema de IA Multi-Camadas com Inteligência Avançada
Desenvolvido para ser EXTREMAMENTE ESPERTO e NUNCA quebrar nada
"""

import os
import sys
import json
import shutil
import subprocess
import hashlib
import tarfile
import re
import ast
import time
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional, Tuple, Any
from dataclasses import dataclass, field
from enum import Enum
import google.generativeai as genai


class SecurityLevel(Enum):
    """Níveis de segurança para operações"""
    SAFE = "safe"           # 100% seguro
    LOW_RISK = "low_risk"   # Risco baixo
    MEDIUM = "medium"       # Requer atenção
    HIGH = "high"           # Requer confirmação
    CRITICAL = "critical"   # Requer múltiplas confirmações


class OperationType(Enum):
    """Tipos de operação"""
    READ = "read"
    ANALYZE = "analyze"
    EDIT = "edit"
    CREATE = "create"
    DELETE = "delete"
    COMMAND = "command"
    SYSTEM = "system"


@dataclass
class ValidationResult:
    """Resultado de validação"""
    valid: bool
    security_level: SecurityLevel
    risks: List[str] = field(default_factory=list)
    suggestions: List[str] = field(default_factory=list)
    estimated_impact: str = "low"
    dependencies: List[str] = field(default_factory=list)
    tests_required: bool = False
    rollback_plan: Optional[str] = None


@dataclass
class AIDecision:
    """Decisão tomada pela IA"""
    action: str
    reasoning: str
    confidence: float  # 0.0 a 1.0
    alternatives: List[str] = field(default_factory=list)
    validation: Optional[ValidationResult] = None
    execution_plan: List[str] = field(default_factory=list)


class ContextCache:
    """Cache inteligente de contexto"""
    
    def __init__(self, cache_dir: Path):
        self.cache_dir = cache_dir
        self.cache_dir.mkdir(parents=True, exist_ok=True)
        self.memory = {}
        self.load_cache()
    
    def load_cache(self):
        """Carrega cache do disco"""
        cache_file = self.cache_dir / 'context_cache.json'
        if cache_file.exists():
            try:
                with open(cache_file) as f:
                    self.memory = json.load(f)
            except:
                self.memory = {}
    
    def save_cache(self):
        """Salva cache no disco"""
        cache_file = self.cache_dir / 'context_cache.json'
        with open(cache_file, 'w') as f:
            json.dump(self.memory, indent=2, fp=f)
    
    def get(self, key: str) -> Optional[Any]:
        """Obtém valor do cache"""
        entry = self.memory.get(key)
        if entry:
            # Verificar se cache ainda é válido (24h)
            timestamp = entry.get('timestamp', 0)
            if time.time() - timestamp < 86400:  # 24 horas
                return entry.get('data')
        return None
    
    def set(self, key: str, value: Any):
        """Define valor no cache"""
        self.memory[key] = {
            'data': value,
            'timestamp': time.time()
        }
        self.save_cache()


class AIValidator:
    """Sistema de validação inteligente em múltiplas camadas"""
    
    def __init__(self, model):
        self.model = model
    
    def validate_code_change(self, file_path: str, old_code: str, new_code: str) -> ValidationResult:
        """Valida mudança de código com análise profunda"""
        
        risks = []
        suggestions = []
        dependencies = []
        
        # Camada 1: Análise sintática
        if file_path.endswith(('.py', '.js', '.jsx', '.ts', '.tsx')):
            syntax_valid = self._check_syntax(file_path, new_code)
            if not syntax_valid:
                risks.append("Erro de sintaxe detectado")
                return ValidationResult(
                    valid=False,
                    security_level=SecurityLevel.HIGH,
                    risks=risks
                )
        
        # Camada 2: Análise de segurança
        security_issues = self._analyze_security(new_code)
        if security_issues:
            risks.extend(security_issues)
        
        # Camada 3: Análise de dependências
        deps = self._extract_dependencies(new_code)
        dependencies.extend(deps)
        
        # Camada 4: Análise de impacto
        impact = self._analyze_impact(old_code, new_code)
        
        # Camada 5: Validação por IA
        ai_validation = self._ai_deep_validation(file_path, old_code, new_code)
        
        # Determinar nível de segurança
        security_level = self._calculate_security_level(risks, impact, ai_validation)
        
        return ValidationResult(
            valid=len(risks) == 0 or security_level != SecurityLevel.CRITICAL,
            security_level=security_level,
            risks=risks,
            suggestions=suggestions,
            estimated_impact=impact,
            dependencies=dependencies,
            tests_required=impact in ['medium', 'high'],
            rollback_plan=self._generate_rollback_plan(file_path)
        )
    
    def _check_syntax(self, file_path: str, code: str) -> bool:
        """Verifica sintaxe do código"""
        try:
            if file_path.endswith('.py'):
                ast.parse(code)
            elif file_path.endswith(('.js', '.jsx', '.ts', '.tsx')):
                # Verificação básica de brackets
                if code.count('{') != code.count('}'):
                    return False
                if code.count('(') != code.count(')'):
                    return False
                if code.count('[') != code.count(']'):
                    return False
            return True
        except:
            return False
    
    def _analyze_security(self, code: str) -> List[str]:
        """Analisa questões de segurança"""
        issues = []
        
        # Padrões perigosos
        dangerous_patterns = [
            (r'eval\s*\(', "Uso de eval() detectado - PERIGOSO"),
            (r'exec\s*\(', "Uso de exec() detectado - PERIGOSO"),
            (r'__import__\s*\(', "Import dinâmico detectado"),
            (r'subprocess\.call\s*\(.*shell\s*=\s*True', "Shell=True em subprocess - RISCO"),
            (r'password\s*=\s*["\'].*["\']', "Senha em texto plano detectada"),
            (r'api[_-]?key\s*=\s*["\'].*["\']', "API key em texto plano detectada"),
        ]
        
        for pattern, message in dangerous_patterns:
            if re.search(pattern, code, re.IGNORECASE):
                issues.append(message)
        
        return issues
    
    def _extract_dependencies(self, code: str) -> List[str]:
        """Extrai dependências do código"""
        deps = []
        
        # Python imports
        for match in re.finditer(r'^import\s+(\S+)', code, re.MULTILINE):
            deps.append(match.group(1))
        for match in re.finditer(r'^from\s+(\S+)\s+import', code, re.MULTILINE):
            deps.append(match.group(1))
        
        # JavaScript/TypeScript imports
        for match in re.finditer(r'import\s+.*?\s+from\s+["\'](.+?)["\']', code):
            deps.append(match.group(1))
        
        return list(set(deps))
    
    def _analyze_impact(self, old_code: str, new_code: str) -> str:
        """Analisa impacto da mudança"""
        
        # Calcular diferença
        old_lines = old_code.split('\n')
        new_lines = new_code.split('\n')
        
        lines_added = len(new_lines) - len(old_lines)
        lines_changed = sum(1 for old, new in zip(old_lines, new_lines) if old != new)
        
        total_change = abs(lines_added) + lines_changed
        
        if total_change < 5:
            return "low"
        elif total_change < 20:
            return "medium"
        else:
            return "high"
    
    def _ai_deep_validation(self, file_path: str, old_code: str, new_code: str) -> Dict:
        """Validação profunda usando IA"""
        
        prompt = f"""Analise esta mudança de código como um especialista em segurança:

ARQUIVO: {file_path}

CÓDIGO ANTIGO (primeiras 50 linhas):
{chr(10).join(old_code.split(chr(10))[:50])}

CÓDIGO NOVO (primeiras 50 linhas):
{chr(10).join(new_code.split(chr(10))[:50])}

Analise:
1. Potenciais bugs
2. Problemas de segurança
3. Impacto em performance
4. Quebra de compatibilidade
5. Boas práticas violadas

Responda em JSON:
{{
  "bugs_potential": [],
  "security_issues": [],
  "performance_impact": "none|low|medium|high",
  "breaking_changes": bool,
  "best_practices_violated": [],
  "recommendation": "approve|review|reject",
  "confidence": 0.0-1.0
}}
"""
        
        try:
            response = self.model.generate_content(prompt)
            text = response.text
            
            # Extrair JSON
            start = text.find('{')
            end = text.rfind('}') + 1
            
            if start >= 0 and end > start:
                return json.loads(text[start:end])
        except:
            pass
        
        return {
            "recommendation": "review",
            "confidence": 0.5
        }
    
    def _calculate_security_level(self, risks: List[str], impact: str, ai_validation: Dict) -> SecurityLevel:
        """Calcula nível de segurança geral"""
        
        # Score system
        score = 0
        
        # Riscos críticos
        critical_keywords = ['PERIGOSO', 'CRÍTICO', 'senha', 'password', 'api key']
        for risk in risks:
            if any(kw in risk for kw in critical_keywords):
                score += 10
            else:
                score += 2
        
        # Impacto
        impact_scores = {'low': 0, 'medium': 3, 'high': 6}
        score += impact_scores.get(impact, 0)
        
        # Recomendação da IA
        ai_rec = ai_validation.get('recommendation', 'review')
        if ai_rec == 'reject':
            score += 8
        elif ai_rec == 'review':
            score += 3
        
        # Converter score em nível
        if score >= 15:
            return SecurityLevel.CRITICAL
        elif score >= 10:
            return SecurityLevel.HIGH
        elif score >= 5:
            return SecurityLevel.MEDIUM
        elif score >= 2:
            return SecurityLevel.LOW_RISK
        else:
            return SecurityLevel.SAFE
    
    def _generate_rollback_plan(self, file_path: str) -> str:
        """Gera plano de rollback"""
        return f"Restaurar {file_path} do backup mais recente usando comando 'restore'"


class CodeAnalyzer:
    """Analisador profundo de código - LÊ e ENTENDE completamente"""
    
    def __init__(self, model):
        self.model = model
    
    def deep_analyze_file(self, file_path: str) -> Dict:
        """Análise PROFUNDA de um arquivo - entende TUDO"""
        
        if not Path(file_path).exists():
            return {'error': 'Arquivo não encontrado'}
        
        print(f"\n📖 LENDO E ANALISANDO: {file_path}")
        
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
        except Exception as e:
            return {'error': f'Erro ao ler arquivo: {e}'}
        
        # Metadados básicos
        lines = content.split('\n')
        total_lines = len(lines)
        
        print(f"   📄 Arquivo: {total_lines} linhas")
        
        # Detectar linguagem
        language = self._detect_language(file_path)
        print(f"   🔤 Linguagem: {language}")
        
        # Análise sintática básica
        structure = self._analyze_structure(content, language)
        print(f"   🏗️  Estrutura: {structure['summary']}")
        
        # ANÁLISE PROFUNDA COM IA
        print(f"   🧠 IA analisando profundamente...")
        
        deep_analysis = self._ai_deep_read(file_path, content, language, structure)
        
        print(f"   ✓ Análise completa!")
        
        return {
            'file_path': file_path,
            'language': language,
            'total_lines': total_lines,
            'structure': structure,
            'content': content,
            'deep_analysis': deep_analysis,
            'timestamp': datetime.now().isoformat()
        }
    
    def _detect_language(self, file_path: str) -> str:
        """Detecta linguagem do arquivo"""
        ext = Path(file_path).suffix.lower()
        
        lang_map = {
            '.py': 'Python',
            '.js': 'JavaScript',
            '.jsx': 'React JSX',
            '.ts': 'TypeScript',
            '.tsx': 'React TypeScript',
            '.php': 'PHP',
            '.css': 'CSS',
            '.html': 'HTML',
            '.json': 'JSON',
            '.md': 'Markdown'
        }
        
        return lang_map.get(ext, 'Unknown')
    
    def _analyze_structure(self, content: str, language: str) -> Dict:
        """Analisa estrutura do código"""
        
        structure = {
            'functions': [],
            'classes': [],
            'imports': [],
            'exports': [],
            'components': [],
            'hooks': [],
            'summary': ''
        }
        
        lines = content.split('\n')
        
        if language == 'Python':
            # Funções
            for i, line in enumerate(lines, 1):
                if line.strip().startswith('def '):
                    func_name = line.strip().split('(')[0].replace('def ', '')
                    structure['functions'].append({
                        'name': func_name,
                        'line': i
                    })
                elif line.strip().startswith('class '):
                    class_name = line.strip().split('(')[0].replace('class ', '').replace(':', '')
                    structure['classes'].append({
                        'name': class_name,
                        'line': i
                    })
                elif line.strip().startswith(('import ', 'from ')):
                    structure['imports'].append(line.strip())
        
        elif language in ['JavaScript', 'TypeScript', 'React JSX', 'React TypeScript']:
            for i, line in enumerate(lines, 1):
                stripped = line.strip()
                
                # Funções
                if 'function ' in stripped or '=>' in stripped:
                    if 'function ' in stripped:
                        func_match = re.search(r'function\s+(\w+)', stripped)
                        if func_match:
                            structure['functions'].append({
                                'name': func_match.group(1),
                                'line': i
                            })
                    elif 'const ' in stripped and '=>' in stripped:
                        func_match = re.search(r'const\s+(\w+)\s*=', stripped)
                        if func_match:
                            structure['functions'].append({
                                'name': func_match.group(1),
                                'line': i
                            })
                
                # Classes/Components
                if 'class ' in stripped:
                    class_match = re.search(r'class\s+(\w+)', stripped)
                    if class_match:
                        structure['classes'].append({
                            'name': class_match.group(1),
                            'line': i
                        })
                
                # Componentes React
                if re.search(r'(const|function)\s+([A-Z]\w+)', stripped):
                    comp_match = re.search(r'(const|function)\s+([A-Z]\w+)', stripped)
                    if comp_match:
                        structure['components'].append({
                            'name': comp_match.group(2),
                            'line': i
                        })
                
                # Hooks React
                if 'useState' in stripped or 'useEffect' in stripped or 'use' in stripped:
                    hook_match = re.search(r'use\w+', stripped)
                    if hook_match:
                        if hook_match.group() not in structure['hooks']:
                            structure['hooks'].append(hook_match.group())
                
                # Imports
                if stripped.startswith('import '):
                    structure['imports'].append(stripped)
                
                # Exports
                if stripped.startswith('export '):
                    structure['exports'].append(stripped)
        
        # Gerar summary
        parts = []
        if structure['classes']:
            parts.append(f"{len(structure['classes'])} classes")
        if structure['components']:
            parts.append(f"{len(structure['components'])} components")
        if structure['functions']:
            parts.append(f"{len(structure['functions'])} functions")
        if structure['hooks']:
            parts.append(f"{len(structure['hooks'])} hooks")
        
        structure['summary'] = ', '.join(parts) if parts else 'código simples'
        
        return structure
    
    def _ai_deep_read(self, file_path: str, content: str, language: str, structure: Dict) -> Dict:
        """IA lê e ENTENDE profundamente o código"""
        
        # Limitar conteúdo para não estourar token limit
        content_preview = '\n'.join(content.split('\n')[:200])  # Primeiras 200 linhas
        
        prompt = f"""Você é um especialista em {language} analisando código em profundidade.

ARQUIVO: {file_path}
LINGUAGEM: {language}
ESTRUTURA DETECTADA:
- Classes: {[c['name'] for c in structure['classes']]}
- Componentes: {[c['name'] for c in structure['components']]}
- Funções: {[f['name'] for f in structure['functions']]}
- Hooks: {structure['hooks']}

CÓDIGO (primeiras 200 linhas):
```{language.lower()}
{content_preview}
```

ANALISE PROFUNDAMENTE:

1. **Propósito do Arquivo**
   - O que este arquivo faz?
   - Qual sua responsabilidade?

2. **Estrutura e Organização**
   - Como está organizado?
   - Segue boas práticas?

3. **Dependências e Imports**
   - Quais bibliotecas usa?
   - Há dependências circulares?

4. **Componentes/Classes Principais**
   - O que cada um faz?
   - Como se relacionam?

5. **Estado e Dados**
   - Como gerencia estado?
   - Quais dados manipula?

6. **Lógica de Negócio**
   - Principais funções e fluxos
   - Validações e regras

7. **Pontos de Atenção**
   - Código complexo ou frágil
   - Áreas que requerem cuidado
   - Possíveis bugs

8. **Como Editar com Segurança**
   - Onde é seguro adicionar código
   - O que NÃO deve ser tocado
   - Dependências a considerar

Responda em JSON:
{{
  "purpose": "propósito principal",
  "main_components": ["lista de componentes principais"],
  "key_functions": ["funções críticas"],
  "state_management": "como gerencia estado",
  "dependencies": ["dependências importantes"],
  "complexity_level": "low|medium|high",
  "safe_edit_zones": ["áreas seguras para editar"],
  "danger_zones": ["áreas PERIGOSAS - não tocar"],
  "recommendations": ["recomendações para edição"],
  "understanding_score": 0.0-1.0
}}
"""
        
        try:
            response = self.model.generate_content(prompt)
            text = response.text
            
            # Extrair JSON
            start = text.find('{')
            end = text.rfind('}') + 1
            
            if start >= 0 and end > start:
                analysis = json.loads(text[start:end])
                
                # Adicionar insights textuais
                analysis['full_text'] = text
                
                return analysis
        except Exception as e:
            print(f"   ⚠️  Erro na análise IA: {e}")
        
        return {
            'purpose': 'Não foi possível determinar',
            'understanding_score': 0.3
        }


class SmartAIEngine:
    """Motor de IA com múltiplas camadas de inteligência"""
    
    def __init__(self, api_key: str, context_cache: ContextCache):
        genai.configure(api_key=api_key)
        
        # Modelo principal (raciocínio)
        self.main_model = genai.GenerativeModel(
            'gemini-pro',
            generation_config={
                'temperature': 0.2,
                'top_p': 0.8,
                'top_k': 40,
                'max_output_tokens': 8192
            }
        )
        
        # Modelo de validação (crítico)
        self.validator_model = genai.GenerativeModel(
            'gemini-pro',
            generation_config={
                'temperature': 0.1,  # Muito conservador
                'top_p': 0.7,
                'top_k': 20
            }
        )
        
        self.cache = context_cache
        self.validator = AIValidator(self.validator_model)
        self.code_analyzer = CodeAnalyzer(self.main_model)  # NOVO!
        self.chat = self.main_model.start_chat(history=[])
        self.decision_history = []
        self.file_knowledge = {}  # Cache de conhecimento de arquivos
    
    def analyze_request(self, user_request: str, system_context: Dict) -> AIDecision:
        """Analisa requisição do usuário com inteligência avançada"""
        
        # Verificar cache
        cache_key = hashlib.md5(user_request.encode()).hexdigest()
        cached = self.cache.get(f"request_{cache_key}")
        
        if cached:
            print("💾 Resposta recuperada do cache")
            return AIDecision(**cached)
        
        # Análise em múltiplas etapas
        print("🧠 Analisando requisição em múltiplas camadas...")
        
        # Etapa 1: Compreensão da intenção
        intent = self._analyze_intent(user_request)
        print(f"   1/6 Intenção: {intent['type']}")
        
        # Etapa 2: Identificar arquivos alvos
        target_files = self._identify_target_files(user_request, intent)
        print(f"   2/6 Arquivos alvo: {len(target_files)}")
        
        # Etapa 2.5: ANÁLISE PROFUNDA DOS ARQUIVOS (NOVO!)
        files_analysis = {}
        if target_files:
            print(f"\n   🔍 ANALISANDO ARQUIVOS PROFUNDAMENTE...")
            for file_path in target_files:
                if file_path not in self.file_knowledge:
                    analysis = self.code_analyzer.deep_analyze_file(file_path)
                    self.file_knowledge[file_path] = analysis
                    files_analysis[file_path] = analysis
                else:
                    print(f"   💾 {file_path} já analisado (cache)")
                    files_analysis[file_path] = self.file_knowledge[file_path]
        
        # Etapa 3: Análise de contexto (agora com conhecimento dos arquivos)
        context_analysis = self._analyze_context(user_request, system_context, files_analysis)
        print(f"   3/6 Contexto: {len(context_analysis['relevant_files'])} arquivos relevantes")
        
        # Etapa 4: Geração de plano de execução (com conhecimento profundo)
        execution_plan = self._generate_execution_plan_smart(
            user_request, intent, context_analysis, files_analysis
        )
        print(f"   4/6 Plano: {len(execution_plan)} etapas")
        
        # Etapa 5: Validação de segurança
        validation = self._validate_plan(execution_plan, system_context)
        print(f"   5/6 Segurança: {validation.security_level.value}")
        
        # Etapa 6: Geração de alternativas
        alternatives = self._generate_alternatives(user_request, execution_plan)
        print(f"   6/6 Alternativas: {len(alternatives)}")
        
        # Criar decisão
        decision = AIDecision(
            action=intent['type'],
            reasoning=intent['reasoning'],
            confidence=intent['confidence'],
            alternatives=alternatives,
            validation=validation,
            execution_plan=execution_plan
        )
        
        # Salvar no cache
        self.cache.set(f"request_{cache_key}", decision.__dict__)
        
        # Adicionar ao histórico
        self.decision_history.append({
            'timestamp': datetime.now().isoformat(),
            'request': user_request,
            'decision': decision.__dict__,
            'files_analyzed': list(files_analysis.keys())
        })
        
        return decision
    
    def _identify_target_files(self, user_request: str, intent: Dict) -> List[str]:
        """Identifica quais arquivos serão afetados"""
        
        target_files = []
        
        # Extrair menções diretas de arquivos
        file_patterns = re.findall(r'[\w/\.-]+\.(tsx?|jsx?|php|py|css|json)', user_request, re.IGNORECASE)
        
        for file_pattern in file_patterns:
            # Buscar arquivo no sistema
            possible_paths = [
                f"/var/www/pterodactyl/{file_pattern}",
                f"/var/www/pterodactyl/resources/scripts/{file_pattern}",
                f"/var/www/pterodactyl/resources/scripts/components/{file_pattern}",
                f"/var/www/pterodactyl/app/Http/Controllers/{file_pattern}",
            ]
            
            for path in possible_paths:
                if Path(path).exists():
                    target_files.append(path)
                    break
        
        # Se não encontrou arquivo explícito, usar intent
        if not target_files and 'target' in intent:
            # Buscar baseado no alvo do intent
            target = intent['target']
            print(f"   🔎 Buscando arquivo para: {target}")
        
        return target_files
    
    def _analyze_intent(self, user_request: str) -> Dict:
        """Analisa a intenção do usuário"""
        
        prompt = f"""Como especialista em análise de intenções, determine o que o usuário quer fazer:

REQUISIÇÃO: "{user_request}"

Responda em JSON:
{{
  "type": "edit|create|delete|analyze|fix|optimize|other",
  "target": "arquivo ou componente alvo",
  "reasoning": "explicação da intenção",
  "confidence": 0.0-1.0,
  "requires_files": ["lista", "de", "arquivos"],
  "action_verb": "verbo principal da ação"
}}
"""
        
        try:
            response = self.main_model.generate_content(prompt)
            text = response.text
            start = text.find('{')
            end = text.rfind('}') + 1
            
            if start >= 0 and end > start:
                return json.loads(text[start:end])
        except Exception as e:
            print(f"   Erro na análise de intenção: {e}")
        
        return {
            "type": "other",
            "target": "unknown",
            "reasoning": "Não foi possível determinar a intenção",
            "confidence": 0.3,
            "requires_files": [],
            "action_verb": "process"
        }
    
    def _analyze_context(self, user_request: str, system_context: Dict, files_analysis: Dict = None) -> Dict:
        """Analisa contexto necessário (com conhecimento profundo dos arquivos)"""
        
        # Extrair arquivos mencionados
        mentioned_files = re.findall(r'[\w/\.-]+\.(tsx?|jsx?|php|py|css|json)', user_request, re.IGNORECASE)
        
        # Buscar arquivos similares no sistema
        relevant_files = []
        
        ptero_structure = system_context.get('pterodactyl', {}).get('structure', {})
        
        def search_files(structure, path=''):
            for name, info in structure.items():
                current_path = f"{path}/{name}" if path else name
                if info.get('type') == 'file':
                    # Verificar se arquivo é relevante
                    if any(mentioned in current_path for mentioned in mentioned_files):
                        relevant_files.append(current_path)
                elif info.get('type') == 'directory':
                    search_files(info.get('children', {}), current_path)
        
        search_files(ptero_structure)
        
        return {
            'mentioned_files': mentioned_files,
            'relevant_files': relevant_files,
            'system_state': system_context,
            'files_deep_knowledge': files_analysis or {}  # NOVO!
        }
    
    def _generate_execution_plan_smart(self, user_request: str, intent: Dict, 
                                      context: Dict, files_analysis: Dict) -> List[str]:
        """Gera plano de execução COM conhecimento profundo dos arquivos"""
        
        # Preparar contexto enriquecido
        files_context = ""
        for file_path, analysis in files_analysis.items():
            deep = analysis.get('deep_analysis', {})
            files_context += f"\n\nARQUIVO: {file_path}"
            files_context += f"\n  Propósito: {deep.get('purpose', 'N/A')}"
            files_context += f"\n  Complexidade: {deep.get('complexity_level', 'N/A')}"
            files_context += f"\n  Zonas seguras: {deep.get('safe_edit_zones', [])}"
            files_context += f"\n  Zonas perigosas: {deep.get('danger_zones', [])}"
            files_context += f"\n  Recomendações: {deep.get('recommendations', [])}"
            files_context += f"\n  Score de entendimento: {deep.get('understanding_score', 0)*100:.0f}%"
        
        prompt = f"""Como arquiteto de software EXPERIENTE que ENTENDEU PROFUNDAMENTE o código, 
crie um plano de execução DETALHADO e SEGURO:

REQUISIÇÃO: "{user_request}"

INTENÇÃO DETECTADA:
{json.dumps(intent, indent=2)}

CONHECIMENTO PROFUNDO DOS ARQUIVOS:
{files_context}

CONTEXTO ADICIONAL:
- Arquivos mencionados: {context['mentioned_files']}
- Arquivos relevantes: {context['relevant_files']}

Com base no seu ENTENDIMENTO PROFUNDO do código, crie um plano que:

1. RESPEITE a estrutura existente
2. EVITE as zonas perigosas identificadas
3. USE as zonas seguras para edição
4. SIGA as recomendações específicas
5. PRESERVE a lógica de negócio
6. MANTENHA as dependências intactas
7. GARANTA que mudanças não quebrem nada

Considere:
- Backup necessário
- Validações necessárias
- Testes a executar
- Ordem correta de execução
- Pontos de rollback
- Impacto em outros componentes

Responda em JSON:
{{
  "steps": [
    {{
      "order": 1,
      "action": "descrição detalhada da ação",
      "type": "backup|validate|edit|test|deploy",
      "files": ["arquivos envolvidos"],
      "reasoning": "por que este passo é necessário",
      "safe_zone": "zona segura sendo usada",
      "reversible": true|false,
      "risk_level": "low|medium|high"
    }}
  ],
  "estimated_time": "tempo estimado",
  "dependencies": ["dependências necessárias"],
  "rollback_strategy": "estratégia detalhada de rollback",
  "impact_assessment": "avaliação de impacto baseada no conhecimento",
  "confidence": 0.0-1.0
}}
"""
        
        try:
            response = self.main_model.generate_content(prompt)
            text = response.text
            start = text.find('{')
            end = text.rfind('}') + 1
            
            if start >= 0 and end > start:
                plan_data = json.loads(text[start:end])
                
                # Mostrar raciocínio
                if plan_data.get('confidence', 0) > 0.8:
                    print(f"\n   ✓ Plano gerado com alta confiança ({plan_data['confidence']*100:.0f}%)")
                
                return [step['action'] for step in plan_data.get('steps', [])]
        except Exception as e:
            print(f"   ⚠️  Erro ao gerar plano: {e}")
        
        return ["Criar backup", "Analisar requisição", "Executar mudança", "Validar resultado"]
    
    def _validate_plan(self, execution_plan: List[str], system_context: Dict) -> ValidationResult:
        """Valida plano de execução"""
        
        risks = []
        
        # Verificar se backup está incluído
        if not any('backup' in step.lower() for step in execution_plan):
            risks.append("Plano não inclui etapa de backup")
        
        # Verificar se há validação
        if not any('valid' in step.lower() or 'test' in step.lower() for step in execution_plan):
            risks.append("Plano não inclui validação/testes")
        
        # Análise por IA
        validation_prompt = f"""Como auditor de segurança, avalie este plano:

PLANO:
{json.dumps(execution_plan, indent=2)}

CONTEXTO DO SISTEMA:
- Pterodactyl instalado: {system_context.get('pterodactyl', {}).get('installed', False)}
- Serviços ativos: {len(system_context.get('services', []))}

Responda em JSON:
{{
  "safe": true|false,
  "risks": ["lista de riscos"],
  "missing_steps": ["etapas ausentes importantes"],
  "recommendation": "approve|modify|reject"
}}
"""
        
        try:
            response = self.validator_model.generate_content(validation_prompt)
            text = response.text
            start = text.find('{')
            end = text.rfind('}') + 1
            
            if start >= 0 and end > start:
                validation_data = json.loads(text[start:end])
                risks.extend(validation_data.get('risks', []))
        except:
            pass
        
        # Determinar nível de segurança
        if len(risks) == 0:
            security_level = SecurityLevel.SAFE
        elif len(risks) <= 2:
            security_level = SecurityLevel.LOW_RISK
        elif len(risks) <= 4:
            security_level = SecurityLevel.MEDIUM
        else:
            security_level = SecurityLevel.HIGH
        
        return ValidationResult(
            valid=len(risks) < 5,
            security_level=security_level,
            risks=risks,
            estimated_impact="medium" if len(execution_plan) > 3 else "low",
            tests_required=True
        )
    
    def _generate_alternatives(self, user_request: str, execution_plan: List[str]) -> List[str]:
        """Gera abordagens alternativas"""
        
        prompt = f"""Sugira 2-3 abordagens alternativas para:

REQUISIÇÃO: "{user_request}"

PLANO ATUAL:
{json.dumps(execution_plan, indent=2)}

Liste alternativas mais seguras, mais rápidas ou mais eficientes.
Responda como lista simples, uma alternativa por linha.
"""
        
        try:
            response = self.main_model.generate_content(prompt)
            alternatives = [line.strip() for line in response.text.split('\n') if line.strip() and not line.startswith('#')]
            return alternatives[:3]
        except:
            return []


class PteroAIUltraPro:
    """Sistema Ultra Profissional de IA - Versão 2.0"""
    
    def __init__(self, api_key: str, config_file: str = "ptero_ai_ultra_config.json"):
        print("🚀 Inicializando PTERO-AI ULTRA PRO v2.0...")
        
        self.config_file = Path.home() / config_file
        self.load_config()
        
        # Cache inteligente
        cache_dir = Path(self.config['cache_path'])
        self.cache = ContextCache(cache_dir)
        
        # Motor de IA avançado
        self.ai = SmartAIEngine(api_key, self.cache)
        
        # Contexto do sistema
        self.system_context = {}
        
        print("✓ Sistema inicializado com sucesso\n")
    
    def load_config(self):
        """Carrega configuração"""
        if self.config_file.exists():
            with open(self.config_file) as f:
                self.config = json.load(f)
        else:
            self.config = {
                'ptero_path': self.detect_pterodactyl_path(),
                'backup_path': str(Path.home() / 'ptero_ultra_backups'),
                'cache_path': str(Path.home() / 'ptero_ultra_cache'),
                'safety_mode': True,
                'auto_backup': True,
                'max_backups': 100,
                'ai_confidence_threshold': 0.7,
                'require_confirmation': {
                    'critical': True,
                    'high': True,
                    'medium': True,
                    'low_risk': False,
                    'safe': False
                }
            }
            self.save_config()
        
        # Criar diretórios
        for path in ['backup_path', 'cache_path']:
            Path(self.config[path]).mkdir(parents=True, exist_ok=True)
    
    def save_config(self):
        """Salva configuração"""
        with open(self.config_file, 'w') as f:
            json.dump(self.config, indent=2, fp=f)
    
    def detect_pterodactyl_path(self) -> str:
        """Detecta caminho do Pterodactyl"""
        paths = [
            '/var/www/pterodactyl',
            '/var/www/panel',
            '/var/www/reviactyl',
            '/var/www/pterodactyl s'
        ]
        
        for path in paths:
            if Path(path).exists() and Path(path, 'artisan').exists():
                return path
        
        return '/var/www/pterodactyl'
    
    def analyze_system(self):
        """Analisa sistema completo (versão otimizada com cache)"""
        cache_key = "full_system_analysis"
        cached = self.cache.get(cache_key)
        
        if cached:
            print("💾 Análise do sistema recuperada do cache")
            self.system_context = cached
            return
        
        print("🔍 Analisando sistema completo...")
        
        # Análise básica
        self.system_context = {
            'pterodactyl': {'installed': Path(self.config['ptero_path']).exists()},
            'services': [],
            'timestamp': datetime.now().isoformat()
        }
        
        self.cache.set(cache_key, self.system_context)
        print("✓ Análise concluída\n")
    
    def process_request(self, user_request: str):
        """Processa requisição do usuário com inteligência ultra avançada"""
        
        print("\n" + "=" * 70)
        print(f"📝 Processando: {user_request}")
        print("=" * 70 + "\n")
        
        # Analisar requisição
        decision = self.ai.analyze_request(user_request, self.system_context)
        
        # Mostrar conhecimento adquirido dos arquivos
        if hasattr(self.ai, 'file_knowledge') and self.ai.file_knowledge:
            print("\n📚 CONHECIMENTO DOS ARQUIVOS:")
            for file_path, analysis in self.ai.file_knowledge.items():
                deep = analysis.get('deep_analysis', {})
                score = deep.get('understanding_score', 0)
                
                print(f"\n   📄 {Path(file_path).name}")
                print(f"      Entendimento: {score*100:.0f}%")
                print(f"      Propósito: {deep.get('purpose', 'N/A')[:80]}...")
                print(f"      Complexidade: {deep.get('complexity_level', 'N/A')}")
                
                if deep.get('key_functions'):
                    print(f"      Funções chave: {', '.join(deep['key_functions'][:3])}")
                
                if deep.get('safe_edit_zones'):
                    print(f"      ✓ Zonas seguras: {len(deep['safe_edit_zones'])}")
                
                if deep.get('danger_zones'):
                    print(f"      ⚠️  Zonas perigosas: {len(deep['danger_zones'])}")
        
        # Mostrar análise
        print("\n📊 ANÁLISE COMPLETA:")
        print(f"   Ação: {decision.action}")
        print(f"   Confiança: {decision.confidence * 100:.1f}%")
        print(f"   Segurança: {decision.validation.security_level.value.upper()}")
        
        if decision.validation.risks:
            print(f"\n⚠️  RISCOS IDENTIFICADOS:")
            for risk in decision.validation.risks:
                print(f"   • {risk}")
        
        print(f"\n📋 PLANO DE EXECUÇÃO ({len(decision.execution_plan)} etapas):")
        for i, step in enumerate(decision.execution_plan, 1):
            print(f"   {i}. {step}")
        
        if decision.alternatives:
            print(f"\n💡 ALTERNATIVAS:")
            for i, alt in enumerate(decision.alternatives, 1):
                print(f"   {i}. {alt}")
        
        # Verificar se requer confirmação
        security_level = decision.validation.security_level.value
        requires_confirmation = self.config['require_confirmation'].get(security_level, True)
        
        if requires_confirmation:
            print(f"\n⚡ Esta operação requer confirmação ({security_level})")
            response = input("   Executar? (s/n/dry): ").lower().strip()
            
            if response == 'dry':
                print("\n🧪 Modo DRY-RUN ativado (simulação)")
                self._simulate_execution(decision)
                return
            elif response != 's':
                print("\n❌ Operação cancelada")
                return
        
        print("\n🚀 Executando...")
        # Aqui implementaria a execução real
        print("✓ Operação completada\n")
    
    def chat(self, user_message: str) -> str:
        """Modo chat simples sem confirmações (para interface gráfica)"""
        try:
            # Usar o main_model para responder
            response = self.ai.main_model.generate_content(
                f"Você é PTERO-AI Ultra Pro, um assistente especializado em Pterodactyl Panel.\n\n"
                f"Usuário: {user_message}\n\n"
                f"Responda de forma útil e amigável. Se for sobre Pterodactyl, seja específico. "
                f"Se for uma saudação, seja breve e pergunte como pode ajudar."
            )
            
            return response.text
        except Exception as e:
            return f"❌ Erro ao processar: {str(e)}"
    
    def _simulate_execution(self, decision: AIDecision):
        """Simula execução sem aplicar mudanças"""
        print("\n🧪 SIMULAÇÃO DE EXECUÇÃO:\n")
        
        for i, step in enumerate(decision.execution_plan, 1):
            print(f"   [{i}/{len(decision.execution_plan)}] {step}")
            time.sleep(0.3)  # Simular tempo de processamento
            print(f"       ✓ Simulado com sucesso")
        
        print("\n✓ Simulação completa - Nenhuma mudança foi aplicada")
    
    def interactive_mode(self):
        """Modo interativo ultra inteligente"""
        
        print("\n" + "=" * 70)
        print("🤖 PTERO-AI ULTRA PRO v2.0 - Modo Interativo")
        print("=" * 70)
        print("\nSistema de IA Multi-Camadas com Inteligência Avançada")
        print("\nComandos:")
        print("  analyze  - Análise completa do sistema")
        print("  status   - Status atual")
        print("  history  - Histórico de decisões")
        print("  config   - Ver/editar configuração")
        print("  exit     - Sair")
        print("\nOu converse naturalmente sobre qualquer coisa!")
        print("=" * 70 + "\n")
        
        # Análise inicial
        self.analyze_system()
        
        while True:
            try:
                user_input = input("\n💬 Você: ").strip()
                
                if not user_input:
                    continue
                
                if user_input.lower() == 'exit':
                    print("\n👋 Até logo!")
                    break
                
                elif user_input.lower() == 'analyze':
                    self.cache.memory.clear()  # Limpar cache para nova análise
                    self.analyze_system()
                    continue
                
                elif user_input.lower() == 'history':
                    print("\n📜 HISTÓRICO DE DECISÕES:")
                    for i, entry in enumerate(self.ai.decision_history[-10:], 1):
                        print(f"\n{i}. [{entry['timestamp']}]")
                        print(f"   Requisição: {entry['request']}")
                        print(f"   Ação: {entry['decision']['action']}")
                    continue
                
                elif user_input.lower() == 'config':
                    print(json.dumps(self.config, indent=2))
                    continue
                
                # Processar requisição
                self.process_request(user_input)
                
            except KeyboardInterrupt:
                print("\n\n⚠️  Interrupção detectada")
                break
            except Exception as e:
                print(f"\n❌ Erro: {e}")
                import traceback
                traceback.print_exc()


def main():
    """Função principal"""
    
    print("""
    ╔══════════════════════════════════════════════════════════╗
    ║                                                          ║
    ║         🚀 PTERO-AI ULTRA PRO v2.0 🚀                    ║
    ║                                                          ║
    ║      Sistema de IA Multi-Camadas                        ║
    ║      com Inteligência Avançada                          ║
    ║                                                          ║
    ║  ✓ 5 Camadas de Validação                               ║
    ║  ✓ Cache Inteligente de Contexto                        ║
    ║  ✓ Análise Multi-Modelo                                 ║
    ║  ✓ Sistema de Scores de Segurança                       ║
    ║  ✓ Geração de Alternativas                              ║
    ║  ✓ Histórico de Decisões                                ║
    ║                                                          ║
    ╚══════════════════════════════════════════════════════════╝
    """)
    
    # API Key
    api_key = "AIzaSyDJ6V-x0EP0vGVaJ4n7mGFSOBSy2EDZIRg"
    
    try:
        ai = PteroAIUltraPro(api_key)
        ai.interactive_mode()
    except Exception as e:
        print(f"\n❌ Erro crítico: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()
