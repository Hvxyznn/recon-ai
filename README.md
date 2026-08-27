Markdown# RECON-AI 🤖

**RECON-AI** é um pipeline automatizado de reconhecimento que transforma o output caótico de ferramentas de Web Pentest em relatórios acionáveis usando Inteligência Artificial. Ele orquestra as melhores ferramentas de Bug Bounty e fornece uma triagem limpa, sem falsos positivos, direto no seu terminal.

---

## 🚀 Principais Características

| Característica | Descrição |
|----------------|-----------|
| **Triagem Cognitiva** | Usa IA para ler logs do Nuclei e descartar falsos positivos |
| **Evasão de WAF** | Sistema de *backoff* automático (SIGSTOP) ao detectar HTTP 429 |
| **Pipeline Completo** | Do Subdomain Recon ao Vulnerability Scanning |
| **Organização Automática** | Salva todos os *outputs* em pastas específicas por alvo |
| **Setup Inteligente** | Instala todas as dependências em Go e Python nativamente |
| **Multi-Modelos** | Suporte integrado para Gemini, OpenAI e DeepSeek |

---

## 📦 Instalação Rápida

```bash
# Baixar repositório
git clone [https://github.com/Hvxyznn/recon-ai.git](https://github.com/Hvxyznn/recon-ai.git)
cd recon-ai

# Instalar dependências Python (Opcional: use venv)
pip install -r requirements.txt

# Configurar ambiente (Instala Subfinder, Nuclei, Httpx, etc)
python3 recon-ai.py --setup
🔧 Configuração de APIsAntes de rodar as varreduras, adicione a chave da IA que fará a triagem (as chaves ficam salvas localmente no config_apis.json).Bash# Configurar Google Gemini (Recomendado)
python3 recon-ai.py --set-api gemini SUA_CHAVE_AQUI

# Configurar OpenAI
python3 recon-ai.py --set-api openai SUA_CHAVE_AQUI

# Configurar DeepSeek
python3 recon-ai.py --set-api deepseek SUA_CHAVE_AQUI
💬 Exemplo Rápido de UsoBash# Iniciar pipeline contra o alvo
python3 recon-ai.py --target example.com --ai gemini

# O script rodará todas as fases e retornará a triagem da IA:
============================================================
             RELATÓRIO EXECUTIVO E TRIAGEM (TERMINAL)          
============================================================
[ALVO & TIPO] 
[https://admin.example.com](https://admin.example.com) - Painel Administrativo Exposto (High)

[IMPACTO REAL] 
Possível ataque de força bruta ou bypass de autenticação.

[VALIDAÇÃO MANUAL RÁPIDA] 
Acesse a URL diretamente no navegador ou via cURL:
curl -I [https://admin.example.com](https://admin.example.com)
============================================================
🎯 Para que Serve?✅ Bug Bounty: Escale seus hunts encontrando falhas reais mais rápido✅ Web Pentest: Automatize a fase massante de reconhecimento✅ Análise de Logs: Pare de ler milhares de linhas json de scanners✅ Red Team: Mapeie perímetros com baixo ruído de rede (Low & Slow)🔥 DiferenciaisRECON-AIScanners TradicionaisTriagemContextual por IAEvasão WAFPausa o processo a nível de KernelOutputTerminal limpo e diretoFocoQualidade (High/Critical)📊 Ecossistema de FerramentasCategoriaFerramentas IntegradasReconhecimentoSubfinder, Assetfinder, HttpxCrawling & EndpointsKatana, GAU (GetAllUrls)Parameter FuzzingArjunScanning AtivoNuclei, Dalfox🛠️ Comandos ÚteisBash# Instalar todas as ferramentas e dependências
python3 recon-ai.py --setup

# Rodar scan usando modelo DeepSeek
python3 recon-ai.py --target site.com --ai deepseek

# Ver painel de ajuda e argumentos disponíveis
python3 recon-ai.py -h
📝 ResumoRECON-AI = Enumeração Massiva → Sondagem Web → Varredura (CVE/XSS) → Triagem com IA → Relatório LimpoDesenvolvido por Hvx. Transforme o caos do reconhecimento em inteligência acionável! 🚀
