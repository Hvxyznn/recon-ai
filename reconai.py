import os
import subprocess
import sys
import json
import time
import signal
import argparse
import shutil
import platform

HOME_DIR = os.environ.get('HOME', '')
GO_BIN_PATH = os.path.join(HOME_DIR, 'go', 'bin')
GO_ROOT_BIN = '/usr/local/go/bin'
for _p in (GO_BIN_PATH, GO_ROOT_BIN):
    if _p not in os.environ.get('PATH', ''):
        os.environ['PATH'] = f"{os.environ.get('PATH', '')}:{_p}"

GO_VERSION = "1.23.4"

def exibir_banner():
    banner = r"""
 ██████╗ ███████╗██████╗ ██████╗ ███╗   ██╗       █████╗ ██╗
 ██╔══██╗██╔════╝██╔════╝██╔═══██╗████╗  ██║      ██╔══██╗██║
 ██████╔╝█████╗  ██║     ██║   ██║██╔██╗ ██║█████╗███████║██║
 ██╔══██╗██╔══╝  ██║     ██║   ██║██║╚██╗██║╚════╝██╔══██║██║
 ██║  ██║███████╗╚██████╗╚██████╔╝██║ ╚████║      ██║  ██║██║
 ╚═╝  ╚═╝╚══════╝ ╚═════╝ ╚═════╝ ╚═╝  ╚═══╝      ╚═╝  ╚═╝╚═╝

 An automated web penetration testing and bug bounty reconnaissance pipeline.
 Powered by AI for intelligent triage and false-positive reduction.

 Developed by Hvx
    """
    print(banner)

def _rodar(cmd):
    print(f"\n[*] Executando: {cmd}")
    resultado = subprocess.run(cmd, shell=True)
    return resultado.returncode == 0

def garantir_go_instalado():
    """Verifica se o Go está instalado e, se não estiver, tenta instalar automaticamente."""
    if shutil.which("go"):
        print("[+] Go já está instalado.")
        return True

    print("[!] Go não encontrado no sistema. Tentando instalar automaticamente...")

    sistema = platform.system().lower()
    arquitetura = platform.machine().lower()

    if sistema != "linux":
        print("[!] Instalação automática do Go só é suportada em Linux.")
        print("    Instale manualmente em: https://go.dev/dl/")
        return False

    mapa_arch = {
        "x86_64": "amd64",
        "amd64": "amd64",
        "aarch64": "arm64",
        "arm64": "arm64",
    }
    go_arch = mapa_arch.get(arquitetura)
    if not go_arch:
        print(f"[!] Arquitetura '{arquitetura}' não mapeada automaticamente.")
        print("    Instale manualmente em: https://go.dev/dl/")
        return False

    tarball = f"go{GO_VERSION}.linux-{go_arch}.tar.gz"
    url = f"https://go.dev/dl/{tarball}"

    passos = [
        f"wget -q -O /tmp/{tarball} {url}",
        f"sudo rm -rf /usr/local/go",
        f"sudo tar -C /usr/local -xzf /tmp/{tarball}",
    ]
    for passo in passos:
        if not _rodar(passo):
            print("[!] Falha ao instalar o Go automaticamente.")
            print("    Tente manualmente: https://go.dev/dl/")
            return False

    if GO_ROOT_BIN not in os.environ.get('PATH', ''):
        os.environ['PATH'] = f"{os.environ.get('PATH', '')}:{GO_ROOT_BIN}"

    # Persiste no PATH do usuário para próximas sessões de shell
    bashrc = os.path.join(HOME_DIR, ".bashrc")
    linha_path = f'export PATH=$PATH:{GO_ROOT_BIN}:{GO_BIN_PATH}\n'
    try:
        conteudo_atual = ""
        if os.path.exists(bashrc):
            with open(bashrc, "r") as f:
                conteudo_atual = f.read()
        if linha_path.strip() not in conteudo_atual:
            with open(bashrc, "a") as f:
                f.write(f"\n# Adicionado por recon-ai.py\n{linha_path}")
            print(f"[+] PATH do Go adicionado em {bashrc} (abra um novo terminal ou rode 'source ~/.bashrc').")
    except Exception as e:
        print(f"[!] Não foi possível atualizar {bashrc} automaticamente: {e}")

    if shutil.which("go"):
        print("[+] Go instalado com sucesso.")
        return True
    else:
        print("[!] Go foi baixado, mas ainda não está no PATH desta sessão.")
        print(f"    Rode: export PATH=$PATH:{GO_ROOT_BIN}:{GO_BIN_PATH}")
        return False

def instalar_dependencias():
    go_ok = garantir_go_instalado()

    comandos = [
        # --break-system-packages evita o erro "externally-managed-environment" (PEP 668)
        "pip install --break-system-packages google-generativeai openai arjun",
    ]

    if go_ok:
        comandos += [
            "go install -v github.com/projectdiscovery/subfinder/v2/cmd/subfinder@latest",
            "go install -v github.com/tomnomnom/assetfinder@latest",
            "go install -v github.com/projectdiscovery/httpx/cmd/httpx@latest",
            "go install -v github.com/projectdiscovery/katana/cmd/katana@latest",
            "go install -v github.com/lc/gau/v2/cmd/gau@latest",
            "go install -v github.com/projectdiscovery/nuclei/v3/cmd/nuclei@latest",
            "go install -v github.com/hahwul/dalfox/v2@latest",
        ]
    else:
        print("[!] Pulando instalação das ferramentas Go pois o Go não está disponível.")

    comandos += [
        "sudo apt update && sudo apt install -y ffuf",
        "nuclei -update-templates",
    ]

    for cmd in comandos:
        print(f"\n[*] Executando: {cmd}")
        subprocess.run(cmd, shell=True)

    print("\n[+] Instalacao concluida.")

    faltantes = [f for f in ["subfinder", "assetfinder", "httpx", "katana", "gau", "nuclei", "dalfox", "arjun", "ffuf"] if not shutil.which(f)]
    if faltantes:
        print(f"[!] Ainda faltando no PATH: {', '.join(faltantes)}")
        print("    Se acabou de instalar o Go agora, rode: source ~/.bashrc")
        print("    E rode novamente: python3 recon-ai.py --setup")
    else:
        print("[+] Todas as ferramentas foram encontradas no PATH.")

def salvar_api(provedor, chave):
    config = {}
    if os.path.exists("config_apis.json"):
        with open("config_apis.json", "r") as f:
            config = json.load(f)
    config[provedor.lower()] = chave
    with open("config_apis.json", "w") as f:
        json.dump(config, f)
    print(f"[+] Chave da API para {provedor} salva com sucesso.")

def carregar_api(provedor):
    if not os.path.exists("config_apis.json"):
        return None
    with open("config_apis.json", "r") as f:
        return json.load(f).get(provedor.lower())

def checar_dependencias():
    ferramentas = ["subfinder", "assetfinder", "httpx", "katana", "gau", "nuclei", "dalfox", "arjun"]
    faltantes = [f for f in ferramentas if not shutil.which(f)]
    if faltantes:
        print(f"[!] Ferramentas faltando no PATH: {', '.join(faltantes)}")
        print("[!] Rode 'python3 recon-ai.py --setup' primeiro.")
        if not shutil.which("go"):
            print("[!] Detectado: o Go não está instalado, por isso as ferramentas Go acima não puderam ser compiladas.")
        print()
        sys.exit(1)

def executar_comando(comando, arquivo_log=None, monitorar_429=False, limite_429=5, pausa_waf=120):
    print(f"[*] Executando: {' '.join(comando)}")
    processo = subprocess.Popen(
        comando, stdout=subprocess.PIPE, stderr=subprocess.DEVNULL, text=True, bufsize=1
    )
    contador_429 = 0
    saida_completa = []
    for linha in processo.stdout:
        linha_limpa = linha.strip()
        if not linha_limpa:
            continue
        saida_completa.append(linha_limpa)
        if monitorar_429:
            try:
                dados = json.loads(linha_limpa)
                if dados.get("status_code") == 429 or dados.get("status-code") == 429:
                    contador_429 += 1
                if contador_429 >= limite_429:
                    print(f"\n[!] WAF detectado. Pausando por {pausa_waf}s...")
                    os.kill(processo.pid, signal.SIGSTOP)
                    time.sleep(pausa_waf)
                    print("[*] Retomando execução...")
                    os.kill(processo.pid, signal.SIGCONT)
                    contador_429 = 0
            except json.JSONDecodeError:
                pass
    processo.wait()
    if arquivo_log and saida_completa:
        with open(arquivo_log, "w", encoding="utf-8") as f:
            f.write("\n".join(saida_completa))
    return saida_completa

def fase_1_subdominios(alvo, pasta):
    print("\n[+] FASE 1: Enumeração de Subdomínios")
    subfinder_out = os.path.join(pasta, "subfinder.txt")
    assetfinder_out = os.path.join(pasta, "assetfinder.txt")
    sub_finais = os.path.join(pasta, "subdominios.txt")
    executar_comando(["subfinder", "-d", alvo, "-silent", "-o", subfinder_out])
    executar_comando(["assetfinder", "--subs-only", alvo], arquivo_log=assetfinder_out)
    subs = set()
    for arq in [subfinder_out, assetfinder_out]:
        if os.path.exists(arq):
            with open(arq, "r") as f:
                for linha in f:
                    s = linha.strip().lower()
                    if s and alvo in s:
                        subs.add(s)
    with open(sub_finais, "w") as f:
        f.write("\n".join(sorted(subs)))
    return sub_finais

def fase_2_web_probing(arquivo_subdominios, pasta):
    print("\n[+] FASE 2: Sondagem Web (Httpx)")
    httpx_json = os.path.join(pasta, "httpx.json")
    urls_txt = os.path.join(pasta, "urls_vivas.txt")
    executar_comando([
        "httpx", "-l", arquivo_subdominios, "-ports", "80,443,8080,8443",
        "-threads", "30", "-rate-limit", "50", "-json", "-o", httpx_json, "-silent"
    ], monitorar_429=True)
    urls = []
    if os.path.exists(httpx_json):
        with open(httpx_json, "r") as f:
            for l in f:
                try:
                    d = json.loads(l)
                    if "url" in d:
                        urls.append(d["url"])
                except:
                    pass
    with open(urls_txt, "w") as f:
        f.write("\n".join(urls))
    return urls_txt

def fase_3_crawling(arquivo_urls, alvo, pasta):
    print("\n[+] FASE 3: Descoberta de Endpoints (Katana + GAU)")
    katana_out = os.path.join(pasta, "katana.txt")
    gau_out = os.path.join(pasta, "gau.txt")
    endpoints_txt = os.path.join(pasta, "endpoints.txt")
    executar_comando(["katana", "-list", arquivo_urls, "-depth", "3", "-silent", "-o", katana_out])
    executar_comando(["gau", alvo, "--threads", "10", "-o", gau_out])
    urls_filtradas = set()
    ignorar = ('.png', '.jpg', '.css', '.woff', '.ico', '.svg', '.gif')
    for arq in [katana_out, gau_out]:
        if os.path.exists(arq):
            with open(arq, "r") as f:
                for l in f:
                    u = l.strip()
                    if u and not u.lower().endswith(ignorar):
                        urls_filtradas.add(u)
    with open(endpoints_txt, "w") as f:
        f.write("\n".join(sorted(urls_filtradas)))
    return endpoints_txt

def fase_4_fuzzing(arquivo_urls, pasta):
    print("\n[+] FASE 4: Parameter Discovery (Arjun)")
    urls_amostra = []
    if os.path.exists(arquivo_urls):
        with open(arquivo_urls, "r") as f:
            urls_amostra = [linha.strip() for linha in f.readlines()[:10]]
    arjun_out = os.path.join(pasta, "arjun.json")
    if urls_amostra:
        amostra_txt = os.path.join(pasta, "arjun_targets.txt")
        with open(amostra_txt, "w") as f:
            f.write("\n".join(urls_amostra))
        executar_comando(["arjun", "-i", amostra_txt, "-t", "5", "--rate-limit", "20", "-oJ", arjun_out])
    return arjun_out

def fase_5_scanning(arquivo_urls, arquivo_endpoints, pasta):
    print("\n[+] FASE 5: Varredura (Nuclei + Dalfox)")
    nuclei_json = os.path.join(pasta, "nuclei.json")
    dalfox_out = os.path.join(pasta, "dalfox.txt")
    executar_comando([
        "nuclei", "-list", arquivo_urls, "-rate-limit", "30", "-delay", "1",
        "-random-agent", "-tags", "cve,misconfig,takeover,sqli",
        "-severity", "medium,high,critical", "-json-export", nuclei_json, "-silent"
    ], monitorar_429=True)
    endpoints_params = os.path.join(pasta, "endpoints_params.txt")
    total_params = 0
    if os.path.exists(arquivo_endpoints):
        with open(arquivo_endpoints, "r") as fin, open(endpoints_params, "w") as fout:
            for linha in fin:
                if "?" in linha and "=" in linha:
                    fout.write(linha)
                    total_params += 1
    if total_params > 0:
        executar_comando([
            "dalfox", "file", endpoints_params, "--silence", "--skip-bav",
            "--worker", "5", "-o", dalfox_out
        ])
    return nuclei_json, dalfox_out

def fase_6_ia(provedor, nuclei_json, dalfox_out, arjun_json):
    print("\n[+] FASE 6: Triagem com IA")
    chave = carregar_api(provedor)
    if not chave:
        print(f"[!] Chave da API {provedor} nao encontrada. Use --set-api.")
        sys.exit(1)
    consolidado = {"nuclei": [], "dalfox": [], "arjun": {}}
    if os.path.exists(nuclei_json):
        with open(nuclei_json, "r") as f:
            for l in f:
                try:
                    d = json.loads(l)
                    consolidado["nuclei"].append({
                        "id": d.get("template-id"), "alvo": d.get("matched-at"),
                        "severidade": d.get("info", {}).get("severity"),
                        "detalhes": d.get("info", {}).get("description")
                    })
                except:
                    pass
    if os.path.exists(dalfox_out):
        with open(dalfox_out, "r") as f:
            consolidado["dalfox"] = [l.strip() for l in f if l.strip()]
    if os.path.exists(arjun_json):
        try:
            with open(arjun_json, "r") as f:
                consolidado["arjun"] = json.load(f)
        except:
            pass
    if not consolidado["nuclei"] and not consolidado["dalfox"]:
        print("[*] Nenhuma falha detectada pelas ferramentas.")
        return
    prompt = f"Você é um Bug Hunter Sênior. Descarte falsos positivos e liste apenas vulnerabilidades reais formatadas para o terminal, incluindo alvo, impacto e comando de validação manual. Dados:\n{json.dumps(consolidado)}"
    print(f"[*] Solicitando analise ao modelo {provedor.upper()}...\n")
    if provedor == "gemini":
        import google.generativeai as genai
        genai.configure(api_key=chave)
        modelo = genai.GenerativeModel('gemini-1.5-pro')
        print(modelo.generate_content(prompt).text)
    elif provedor == "openai":
        from openai import OpenAI
        cliente = OpenAI(api_key=chave)
        resposta = cliente.chat.completions.create(model="gpt-4-turbo", messages=[{"role": "user", "content": prompt}])
        print(resposta.choices[0].message.content)
    elif provedor == "deepseek":
        from openai import OpenAI
        cliente = OpenAI(api_key=chave, base_url="https://api.deepseek.com/v1")
        resposta = cliente.chat.completions.create(model="deepseek-chat", messages=[{"role": "user", "content": prompt}])
        print(resposta.choices[0].message.content)

def main():
    parser = argparse.ArgumentParser(description="RECON-AI - Automação de Pentest Web")
    parser.add_argument("--setup", action="store_true", help="Instala todas as dependências do sistema")
    parser.add_argument("--set-api", nargs=2, metavar=('PROVEDOR', 'CHAVE'), help="Salva a chave de API (ex: gemini, openai, deepseek)")
    parser.add_argument("--target", type=str, help="O domínio alvo para executar o pentest")
    parser.add_argument("--ai", type=str, choices=['gemini', 'openai', 'deepseek'], help="Escolha qual modelo de IA fará a triagem")
    args = parser.parse_args()

    if args.setup:
        instalar_dependencias()
        sys.exit(0)

    if args.set_api:
        salvar_api(args.set_api[0], args.set_api[1])
        sys.exit(0)

    if args.target and args.ai:
        exibir_banner()
        checar_dependencias()
        pasta_saida = f"out_{args.target.replace('.', '_')}"
        os.makedirs(pasta_saida, exist_ok=True)
        print(f"[*] Iniciando pipeline contra o alvo: {args.target}")
        subs = fase_1_subdominios(args.target, pasta_saida)
        urls = fase_2_web_probing(subs, pasta_saida)
        if os.path.exists(urls) and os.stat(urls).st_size > 0:
            endpoints = fase_3_crawling(urls, args.target, pasta_saida)
            arjun = fase_4_fuzzing(urls, pasta_saida)
            nuclei, dalfox = fase_5_scanning(urls, endpoints, pasta_saida)
            fase_6_ia(args.ai, nuclei, dalfox, arjun)
            print(f"\n[+] Pipeline finalizado. Artefatos em: ./{pasta_saida}/")
        else:
            print("[!] Nenhuma URL viva encontrada.")
    else:
        parser.print_help()

if __name__ == "__main__":
    main()
