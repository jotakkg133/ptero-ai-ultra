"""
SVG Icons para PTERO-AI Ultra Pro
Ícones vetoriais personalizados
"""

ICONS = {
    # Logo principal
    "logo": '''
        <svg viewBox="0 0 100 100" xmlns="http://www.w3.org/2000/svg">
            <defs>
                <linearGradient id="logoGradient" x1="0%" y1="0%" x2="100%" y2="100%">
                    <stop offset="0%" style="stop-color:#89b4fa;stop-opacity:1" />
                    <stop offset="100%" style="stop-color:#74c7ec;stop-opacity:1" />
                </linearGradient>
                <filter id="glow">
                    <feGaussianBlur stdDeviation="2" result="coloredBlur"/>
                    <feMerge>
                        <feMergeNode in="coloredBlur"/>
                        <feMergeNode in="SourceGraphic"/>
                    </feMerge>
                </filter>
            </defs>
            <circle cx="50" cy="50" r="45" fill="url(#logoGradient)" filter="url(#glow)"/>
            <circle cx="50" cy="50" r="30" fill="#cba6f7" opacity="0.8"/>
            <circle cx="50" cy="50" r="15" fill="#f5e0dc"/>
            <path d="M 30 50 Q 50 30 70 50 Q 50 70 30 50" fill="#89b4fa" opacity="0.5"/>
        </svg>
    ''',
    
    # Status - Idle (Verde)
    "status_idle": '''
        <svg viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg">
            <defs>
                <radialGradient id="idleGradient">
                    <stop offset="0%" style="stop-color:#a6e3a1;stop-opacity:1" />
                    <stop offset="100%" style="stop-color:#94e2d5;stop-opacity:1" />
                </radialGradient>
            </defs>
            <circle cx="12" cy="12" r="10" fill="url(#idleGradient)"/>
            <circle cx="12" cy="12" r="8" fill="#a6e3a1" opacity="0.5"/>
            <path d="M 8 12 L 11 15 L 16 9" stroke="#1e1e2e" stroke-width="2" fill="none" stroke-linecap="round"/>
        </svg>
    ''',
    
    # Status - Thinking (Amarelo pulsante)
    "status_thinking": '''
        <svg viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg">
            <defs>
                <radialGradient id="thinkGradient">
                    <stop offset="0%" style="stop-color:#f9e2af;stop-opacity:1" />
                    <stop offset="100%" style="stop-color:#fab387;stop-opacity:1" />
                </radialGradient>
                <animate attributeName="opacity" values="1;0.3;1" dur="1.5s" repeatCount="indefinite"/>
            </defs>
            <circle cx="12" cy="12" r="10" fill="url(#thinkGradient)">
                <animate attributeName="r" values="10;12;10" dur="1.5s" repeatCount="indefinite"/>
            </circle>
            <circle cx="8" cy="12" r="1.5" fill="#1e1e2e"/>
            <circle cx="12" cy="12" r="1.5" fill="#1e1e2e"/>
            <circle cx="16" cy="12" r="1.5" fill="#1e1e2e"/>
        </svg>
    ''',
    
    # Status - Working (Azul girando)
    "status_working": '''
        <svg viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg">
            <defs>
                <linearGradient id="workGradient">
                    <stop offset="0%" style="stop-color:#89b4fa;stop-opacity:1" />
                    <stop offset="100%" style="stop-color:#74c7ec;stop-opacity:1" />
                </linearGradient>
            </defs>
            <g>
                <animateTransform attributeName="transform" type="rotate" 
                    from="0 12 12" to="360 12 12" dur="2s" repeatCount="indefinite"/>
                <path d="M 12 2 A 10 10 0 0 1 22 12" stroke="url(#workGradient)" 
                    stroke-width="3" fill="none" stroke-linecap="round"/>
                <circle cx="12" cy="2" r="2" fill="#89b4fa"/>
            </g>
        </svg>
    ''',
    
    # Status - Error (Vermelho)
    "status_error": '''
        <svg viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg">
            <defs>
                <radialGradient id="errorGradient">
                    <stop offset="0%" style="stop-color:#f38ba8;stop-opacity:1" />
                    <stop offset="100%" style="stop-color:#eba0ac;stop-opacity:1" />
                </radialGradient>
            </defs>
            <circle cx="12" cy="12" r="10" fill="url(#errorGradient)"/>
            <path d="M 8 8 L 16 16 M 16 8 L 8 16" stroke="#1e1e2e" 
                stroke-width="2.5" stroke-linecap="round"/>
        </svg>
    ''',
    
    # Ícone de arquivo
    "file": '''
        <svg viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg">
            <defs>
                <linearGradient id="fileGradient" x1="0%" y1="0%" x2="0%" y2="100%">
                    <stop offset="0%" style="stop-color:#89b4fa;stop-opacity:1" />
                    <stop offset="100%" style="stop-color:#74c7ec;stop-opacity:1" />
                </linearGradient>
            </defs>
            <path d="M 5 2 L 15 2 L 19 6 L 19 22 L 5 22 Z" 
                fill="url(#fileGradient)" stroke="#cdd6f4" stroke-width="1"/>
            <path d="M 15 2 L 15 6 L 19 6" fill="#313244" stroke="#cdd6f4" stroke-width="1"/>
            <line x1="8" y1="11" x2="16" y2="11" stroke="#1e1e2e" stroke-width="1"/>
            <line x1="8" y1="14" x2="16" y2="14" stroke="#1e1e2e" stroke-width="1"/>
            <line x1="8" y1="17" x2="13" y2="17" stroke="#1e1e2e" stroke-width="1"/>
        </svg>
    ''',
    
    # Ícone de terminal
    "terminal": '''
        <svg viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg">
            <defs>
                <linearGradient id="termGradient">
                    <stop offset="0%" style="stop-color:#a6e3a1;stop-opacity:1" />
                    <stop offset="100%" style="stop-color:#94e2d5;stop-opacity:1" />
                </linearGradient>
            </defs>
            <rect x="2" y="4" width="20" height="16" rx="2" 
                fill="#1e1e2e" stroke="url(#termGradient)" stroke-width="2"/>
            <path d="M 6 9 L 9 12 L 6 15" stroke="#a6e3a1" 
                stroke-width="2" fill="none" stroke-linecap="round" stroke-linejoin="round"/>
            <line x1="11" y1="15" x2="16" y2="15" stroke="#a6e3a1" 
                stroke-width="2" stroke-linecap="round"/>
        </svg>
    ''',
    
    # Ícone de segurança
    "shield": '''
        <svg viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg">
            <defs>
                <linearGradient id="shieldGradient" x1="0%" y1="0%" x2="0%" y2="100%">
                    <stop offset="0%" style="stop-color:#a6e3a1;stop-opacity:1" />
                    <stop offset="100%" style="stop-color:#94e2d5;stop-opacity:1" />
                </linearGradient>
            </defs>
            <path d="M 12 2 L 4 6 L 4 12 Q 4 18 12 22 Q 20 18 20 12 L 20 6 Z" 
                fill="url(#shieldGradient)" stroke="#cdd6f4" stroke-width="1"/>
            <path d="M 9 12 L 11 14 L 15 9" stroke="#1e1e2e" 
                stroke-width="2" fill="none" stroke-linecap="round" stroke-linejoin="round"/>
        </svg>
    ''',
    
    # Ícone de backup
    "backup": '''
        <svg viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg">
            <defs>
                <linearGradient id="backupGradient">
                    <stop offset="0%" style="stop-color:#cba6f7;stop-opacity:1" />
                    <stop offset="100%" style="stop-color:#b4befe;stop-opacity:1" />
                </linearGradient>
            </defs>
            <circle cx="12" cy="12" r="10" fill="url(#backupGradient)"/>
            <path d="M 12 6 L 12 14 M 9 11 L 12 14 L 15 11" 
                stroke="#1e1e2e" stroke-width="2" fill="none" 
                stroke-linecap="round" stroke-linejoin="round"/>
            <line x1="8" y1="17" x2="16" y2="17" stroke="#1e1e2e" 
                stroke-width="2" stroke-linecap="round"/>
        </svg>
    ''',
    
    # Ícone de análise
    "analyze": '''
        <svg viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg">
            <defs>
                <linearGradient id="analyzeGradient">
                    <stop offset="0%" style="stop-color:#f9e2af;stop-opacity:1" />
                    <stop offset="100%" style="stop-color:#fab387;stop-opacity:1" />
                </linearGradient>
            </defs>
            <circle cx="11" cy="11" r="8" fill="none" 
                stroke="url(#analyzeGradient)" stroke-width="2"/>
            <line x1="16.5" y1="16.5" x2="21" y2="21" 
                stroke="url(#analyzeGradient)" stroke-width="2" stroke-linecap="round"/>
            <circle cx="11" cy="11" r="4" fill="#f9e2af" opacity="0.3"/>
        </svg>
    ''',
    
    # Ícone de execução
    "execute": '''
        <svg viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg">
            <defs>
                <linearGradient id="execGradient">
                    <stop offset="0%" style="stop-color:#89b4fa;stop-opacity:1" />
                    <stop offset="100%" style="stop-color:#74c7ec;stop-opacity:1" />
                </linearGradient>
            </defs>
            <circle cx="12" cy="12" r="10" fill="url(#execGradient)"/>
            <path d="M 9 7 L 17 12 L 9 17 Z" fill="#1e1e2e"/>
        </svg>
    ''',
    
    # Ícone de sucesso
    "success": '''
        <svg viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg">
            <defs>
                <radialGradient id="successGradient">
                    <stop offset="0%" style="stop-color:#a6e3a1;stop-opacity:1" />
                    <stop offset="100%" style="stop-color:#94e2d5;stop-opacity:1" />
                </radialGradient>
            </defs>
            <circle cx="12" cy="12" r="10" fill="url(#successGradient)"/>
            <path d="M 7 12 L 10 15 L 17 8" stroke="#1e1e2e" 
                stroke-width="2.5" fill="none" stroke-linecap="round" stroke-linejoin="round"/>
        </svg>
    ''',
    
    # Ícone de aviso
    "warning": '''
        <svg viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg">
            <defs>
                <linearGradient id="warnGradient">
                    <stop offset="0%" style="stop-color:#f9e2af;stop-opacity:1" />
                    <stop offset="100%" style="stop-color:#fab387;stop-opacity:1" />
                </linearGradient>
            </defs>
            <path d="M 12 2 L 22 20 L 2 20 Z" fill="url(#warnGradient)" 
                stroke="#1e1e2e" stroke-width="1"/>
            <line x1="12" y1="9" x2="12" y2="14" stroke="#1e1e2e" 
                stroke-width="2" stroke-linecap="round"/>
            <circle cx="12" cy="17" r="1" fill="#1e1e2e"/>
        </svg>
    ''',
    
    # Ícone de settings
    "settings": '''
        <svg viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg">
            <defs>
                <linearGradient id="settingsGradient">
                    <stop offset="0%" style="stop-color:#cba6f7;stop-opacity:1" />
                    <stop offset="100%" style="stop-color:#b4befe;stop-opacity:1" />
                </linearGradient>
            </defs>
            <circle cx="12" cy="12" r="3" fill="url(#settingsGradient)"/>
            <g stroke="url(#settingsGradient)" stroke-width="2" fill="none">
                <circle cx="12" cy="12" r="8"/>
                <line x1="12" y1="2" x2="12" y2="6"/>
                <line x1="12" y1="18" x2="12" y2="22"/>
                <line x1="4.93" y1="4.93" x2="7.76" y2="7.76"/>
                <line x1="16.24" y1="16.24" x2="19.07" y2="19.07"/>
                <line x1="2" y1="12" x2="6" y2="12"/>
                <line x1="18" y1="12" x2="22" y2="12"/>
                <line x1="4.93" y1="19.07" x2="7.76" y2="16.24"/>
                <line x1="16.24" y1="7.76" x2="19.07" y2="4.93"/>
            </g>
        </svg>
    ''',
    
    # Ícone de chat
    "chat": '''
        <svg viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg">
            <defs>
                <linearGradient id="chatGradient" x1="0%" y1="0%" x2="100%" y2="100%">
                    <stop offset="0%" style="stop-color:#89b4fa;stop-opacity:1" />
                    <stop offset="100%" style="stop-color:#74c7ec;stop-opacity:1" />
                </linearGradient>
            </defs>
            <path d="M 3 5 Q 3 3 5 3 L 19 3 Q 21 3 21 5 L 21 15 Q 21 17 19 17 L 8 17 L 3 21 Z" 
                fill="url(#chatGradient)" stroke="#cdd6f4" stroke-width="1"/>
            <line x1="7" y1="8" x2="17" y2="8" stroke="#1e1e2e" stroke-width="1.5" stroke-linecap="round"/>
            <line x1="7" y1="12" x2="14" y2="12" stroke="#1e1e2e" stroke-width="1.5" stroke-linecap="round"/>
        </svg>
    '''
}


def save_svg(name, path="/tmp/ptero_ai_icons/"):
    """Salva SVG em arquivo"""
    import os
    os.makedirs(path, exist_ok=True)
    
    with open(f"{path}{name}.svg", "w") as f:
        f.write(ICONS[name])


def save_all_icons(path="/tmp/ptero_ai_icons/"):
    """Salva todos os ícones"""
    for name in ICONS:
        save_svg(name, path)
    print(f"✓ {len(ICONS)} ícones salvos em {path}")


if __name__ == "__main__":
    save_all_icons()
