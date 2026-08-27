# RECON-AI 🤖

**RECON-AI** é um pipeline de reconhecimento automatizado que transforma o output caótico de ferramentas de Web Pentest em relatórios acionáveis. Ele orquestra as melhores ferramentas de Bug Bounty e fornece uma triagem inteligente via IA, sem falsos positivos, direto no seu terminal.

---

## 🚀 Principais Características

| Característica | Descrição |
|----------------|-----------|
| **Triagem Cognitiva** | Usa IA para ler logs confusos e descartar falsos positivos |
| **Pipeline Completo** | Do reconhecimento passivo à exploração ativa |
| **Evasão de WAF** | Sistema de *backoff* automático (SIGSTOP) ao detectar HTTP 429 |
| **Multi-Modelos** | Suporte integrado para Gemini, OpenAI e DeepSeek |
| **Organização Automática** | Salva todos os *outputs* em pastas específicas por alvo |
| **Setup Inteligente** | Instala dependências em Go e Python nativamente |

---

## 📦 Instalação Rápida

```bash
# Baixar repositório
git clone https://github.com/Hvxyznn/recon-ai.git
cd recon-ai

python3 -m venv venv
source venv/bin/activate

# Instalar dependências Python
pip install -r requirements.txt

# Configurar ambiente (Instala Subfinder, Nuclei, Httpx, etc)
python3 reconai.py --setup
```

---

## 🔧 Configuração das APIs

### Adicionar Chaves (Necessário para a IA)

```bash
# Configurar Google Gemini (Recomendado)
python3 reconai.py --set-api gemini SUA_CHAVE_AQUI

# Configurar OpenAI
python3 reconai.py --set-api openai SUA_CHAVE_AQUI

# Configurar DeepSeek
python3 reconai.py --set-api deepseek SUA_CHAVE_AQUI
```

---

## 💬 Exemplo Rápido

```bash
# Iniciar pipeline contra o alvo
python3 reconai.py --target example.com --ai gemini
```

**Resposta (relatório limpo no terminal):**

```
============================================================
             RELATÓRIO EXECUTIVO E TRIAGEM (TERMINAL)
============================================================
[ALVO & TIPO]
https://admin.example.com - Painel Administrativo Exposto (High)

[IMPACTO REAL]
Possível ataque de força bruta ou bypass de autenticação.

[VALIDAÇÃO MANUAL RÁPIDA]
Acesse a URL diretamente no navegador ou via cURL:
curl -I https://admin.example.com
============================================================
```

---

## 🎯 Para que Serve?

- ✅ **Bug Bounty**: Escale seus hunts encontrando falhas reais mais rápido
- ✅ **Web Pentest**: Automatize a fase massante de reconhecimento
- ✅ **Red Team**: Mapeie perímetros com baixo ruído de rede (*Low & Slow*)
- ✅ **Análise de Logs**: Pare de ler milhares de linhas JSON manualmente
- ✅ **Estudos**: Entenda como vulnerabilidades reais se comportam

---

## 🔥 Diferenciais

| RECON-AI | Scanners Tradicionais |
|----------|------------------------|
| **Triagem via IA** | Triagem manual |
| **Evasão de WAF (SIGSTOP)** | Sem evasão de WAF |
| **Output limpo e direto** | Logs extensos e brutos |
| **Foco em qualidade (High/Critical)** | Foco em quantidade |
| **Totalmente grátis** | Custo variável |

---

## 📊 Ecossistema de Ferramentas

| Categoria | Ferramentas Integradas |
|-----------|--------------------------|
| **Reconhecimento** | Subfinder, Assetfinder, Httpx |
| **Crawling & Endpoints** | Katana, GAU (GetAllUrls) |
| **Parameter Fuzzing** | Arjun |
| **Scanning Ativo** | Nuclei, Dalfox |

---

## 🛠️ Comandos Úteis

```bash
# Instalar todas as ferramentas e dependências
python3 reconai.py --setup

# Rodar scan usando modelo DeepSeek
python3 reconai.py --target site.com --ai deepseek

# Ver painel de ajuda e argumentos disponíveis
python3 reconai.py -h
```

---

## ⚖️ Uso Responsável

O RECON-AI foi criado para acelerar o reconhecimento em **alvos autorizados** — programas de Bug Bounty, contratos de pentest ou laboratórios próprios. O uso contra sistemas sem autorização é de responsabilidade exclusiva de quem executa a ferramenta.

---

## 📝 Resumo

> **RECON-AI** = Enumeração Massiva → Sondagem Web → Fuzzing → Scanning → Triagem com IA → Relatório Limpo

Desenvolvido por **Hvx**. Transforme o caos do reconhecimento em inteligência acionável! 🚀
