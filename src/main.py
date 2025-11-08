import sys
import os
import random

# Garantir que o pacote local seja importável (mesmo comportamento de antes)
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from dataset import baixar_e_listar_imagens
from auth import autenticar

# ANSI cores para deixar o menu bonito (sem libs extras)
CSI = "\033["
RESET = CSI + "0m"
BOLD = CSI + "1m"
CYAN = CSI + "36m"
MAGENTA = CSI + "35m"
YELLOW = CSI + "33m"
GREEN = CSI + "32m"
RED = CSI + "31m"
WHITE_BG = CSI + "47m"  # só usado com moderação

def _print_title():
    w = 66
    print()
    print(GREEN + "╔" + "═" * (w - 2) + "╗" + RESET)
    title = "SISTEMA DE AUTENTICAÇÃO BIOMÉTRICA"
    subtitle = "IMPRESSÃO DIGITAL"
    print(GREEN + "║" + RESET + title.center(w - 2) + GREEN + "║" + RESET)
    print(GREEN + "║" + RESET + subtitle.center(w - 2) + GREEN + "║" + RESET)
    print(GREEN + "╚" + "═" * (w - 2) + "╝" + RESET)
    print()

def _print_menu():
    print()
    box_w = 66
    print(MAGENTA + "╔" + "═" * (box_w - 2) + "╗" + RESET)
    header = " MENU PRINCIPAL "
    print(MAGENTA + "║" + RESET + header.center(box_w - 2) + MAGENTA + "║" + RESET)
    print(MAGENTA + "╠" + "═" * (box_w - 2) + "╣" + RESET)
    print(MAGENTA + "║" + RESET + f"  {CYAN}[1]{RESET} Entrar no sistema usando a biometria".ljust(box_w - 2) + MAGENTA + "║" + RESET)
    print(MAGENTA + "║" + RESET + f"  {CYAN}[2]{RESET} Iniciar teste — selecionar imagens para comparar".ljust(box_w - 2) + MAGENTA + "║" + RESET)
    print(MAGENTA + "║" + RESET + f"  {CYAN}[3]{RESET} Sair do programa".ljust(box_w - 2) + MAGENTA + "║" + RESET)
    print(MAGENTA + "╚" + "═" * (box_w - 2) + "╝" + RESET)
    print()

def _print_inline_box(title, lines):
    w = 66
    print(YELLOW + "┏" + "━" * (w - 2) + "┓" + RESET)
    print(YELLOW + "┃ " + BOLD + title.center(w - 4) + RESET + YELLOW + " ┃" + RESET)
    print(YELLOW + "┣" + "━" * (w - 2) + "┫" + RESET)
    for line in lines:
        print(YELLOW + "┃ " + RESET + line.ljust(w - 4) + YELLOW + " ┃" + RESET)
    print(YELLOW + "┗" + "━" * (w - 2) + "┛" + RESET)

def main():
    _print_title()

    try:
        print(CYAN + "Iniciando download/varredura do dataset no Kaggle..." + RESET)
        imagens = baixar_e_listar_imagens()

        if len(imagens) < 2:
            print(RED + "Erro: não há imagens suficientes para executar comparações." + RESET)
            return

        print(f"{GREEN}Dataset pronto — {len(imagens)} imagens encontradas.{RESET}")

        while True:
            _print_menu()
            escolha = input(BOLD + "Escolha uma opção (1-3): " + RESET).strip()
            if escolha == "1":
                entrar_no_sistema(imagens)
            elif escolha == "2":
                teste_manual(imagens)
            elif escolha == "3":
                print(GREEN + "\nObrigado por usar o sistema. Até logo!\n" + RESET)
                break
            else:
                print(YELLOW + "Opção inválida — tente novamente." + RESET)

    except Exception as exc:
        print(f"Erro inesperado no fluxo principal: {exc}")

def entrar_no_sistema(imagens):
    """Fluxo de login: pergunta o cargo do usuário, guarda a escolha e depois valida
    a biometria escolhida contra perfis com níveis de acesso (1,2,3)."""
    title = "ENTRAR NO SISTEMA (BIOMETRIA / REQUISITO DE CARGO)"
    intro = [
        "Antes de selecionar a impressão, informe seu cargo.",
        "O sistema verificará se a biometria escolhida confere com o nível de acesso",
        "associado ao perfil biométrico registrado.",
        "",
        "Mapeamento de níveis:",
        "  Nível 1 — Acesso geral (qualquer funcionário)",
        "  Nível 2 — Diretores (acesso restrito)",
        "  Nível 3 — Ministro (acesso total)"
    ]
    _print_inline_box(title, intro)

    # leitura do cargo e armazenamento na sessão temporária
    cargo = None
    cargo_nivel = 0
    while True:
        escolha_cargo = input(BOLD + "\nEscolha seu cargo: [1] Funcionário  [2] Diretor  [3] Ministro  (q = sair): " + RESET).strip().lower()
        if escolha_cargo == "1":
            cargo = "funcionario"
            cargo_nivel = 1
            print(GREEN + "Cargo selecionado: Funcionário (Nível 1)" + RESET)
            break
        if escolha_cargo == "2":
            cargo = "diretor"
            cargo_nivel = 2
            print(YELLOW + "Cargo selecionado: Diretor (Nível 2)" + RESET)
            break
        if escolha_cargo == "3":
            cargo = "ministro"
            cargo_nivel = 3
            print(GREEN + "Cargo selecionado: Ministro (Nível 3)" + RESET)
            break
        if escolha_cargo == "q":
            print(YELLOW + "Operação cancelada pelo usuário." + RESET)
            return False
        print(YELLOW + "Entrada inválida — escolha 1, 2, 3 ou q." + RESET)

    # verifica se há imagens suficientes para criar perfis
    if len(imagens) < 3:
        print(YELLOW + "Não há imagens suficientes para configuração automática. Abrindo seleção manual..." + RESET)
        return teste_manual(imagens)

    # define perfis (convenção)
    try:
        # perfil biométrico e seu nível associado
        perfil_ministro = (imagens[0], 3)       # Nível 3
        perfil_diretor = (imagens[4], 2)        # Nível 2
        perfil_funcionario = (imagens[7], 1)    # Nível 1
    except Exception:
        print(YELLOW + "Perfis automáticos não disponíveis (índices faltando). Usando seleção manual..." + RESET)
        return teste_manual(imagens)

    perfil_lines = [
        f"Ministro  -> {os.path.basename(perfil_ministro[0])} (Nível 3)",
        f"Diretor   -> {os.path.basename(perfil_diretor[0])} (Nível 2)",
        f"Funcionário -> {os.path.basename(perfil_funcionario[0])} (Nível 1)",
        "",
        "Agora escolha a imagem de teste (mostrando até 10 primeiras):"
    ]
    _print_inline_box("PERFIS BIOMETRICOS", perfil_lines)

    for i, caminho in enumerate(imagens[:10], start=1):
        print(f"  {i:2d}. {os.path.basename(caminho)}")

    try:
        idx_test = int(input("\nÍndice da imagem de teste (1-10): ").strip()) - 1
        if not (0 <= idx_test < len(imagens)):
            print(YELLOW + "Índice inválido." + RESET)
            return False

        img_teste = imagens[idx_test]
        print(CYAN + "\nAutenticando contra perfis registrados..." + RESET)

        # testar cada perfil sem prints internos e sem outcomes repetidos
        match_ministro = autenticar(perfil_ministro[0], img_teste, verbose=False, show_outcome=False)
        match_diretor = autenticar(perfil_diretor[0], img_teste, verbose=False, show_outcome=False)
        match_func = autenticar(perfil_funcionario[0], img_teste, verbose=False, show_outcome=False)

        # descobrir qual perfil correspondeu e o nível exigido
        matched_level = 0
        matched_label = None
        if match_ministro:
            matched_level = perfil_ministro[1]; matched_label = "Ministro"
        elif match_diretor:
            matched_level = perfil_diretor[1]; matched_label = "Diretor"
        elif match_func:
            matched_level = perfil_funcionario[1]; matched_label = "Funcionário"

        # se houver match, validar permissão com base no cargo declarado
        if matched_level > 0:
            # condicional de autorização:
            # permitido se cargo_nivel >= matched_level (cargo declarado tem igual ou maior privilégio)
            if cargo_nivel >= matched_level:
                # acesso concedido — mensagem chamativa que varia conforme nível
                w = 66
                if matched_level == 3:
                    print(GREEN + "╔" + "═" * (w - 2) + "╗" + RESET)
                    print(GREEN + "║" + RESET + BOLD + " ✦✦✦ ACESSO NÍVEL 3 CONCEDIDO ✦✦✦ ".center(w - 2) + RESET + GREEN + "║" + RESET)
                    print(GREEN + "║" + RESET + BOLD + f"    AUTORIZAÇÃO: {matched_label} / MINISTÉRIO    ".center(w - 2) + RESET + GREEN + "║" + RESET)
                    print(GREEN + "╚" + "═" * (w - 2) + "╝" + RESET)
                    print("\n" + BOLD + GREEN + ">>> ACESSO TOTAL: BEM-VINDO, ACESSO AO NÍVEL 3 <<<" + RESET + "\n")
                elif matched_level == 2:
                    print(YELLOW + "╔" + "═" * (w - 2) + "╗" + RESET)
                    print(YELLOW + "║" + RESET + BOLD + " ✦✦ ACESSO NÍVEL 2 CONCEDIDO ✦✦ ".center(w - 2) + RESET + YELLOW + "║" + RESET)
                    print(YELLOW + "║" + RESET + BOLD + f"      AUTORIZAÇÃO: {matched_label} / DIRETORIA      ".center(w - 2) + RESET + YELLOW + "║" + RESET)
                    print(YELLOW + "╚" + "═" * (w - 2) + "╝" + RESET)
                    print("\n" + BOLD + YELLOW + ">>> ACESSO RESTRITO: BEM-VINDO, ACESSO AO NÍVEL 2 <<<" + RESET + "\n")
                else:
                    print(GREEN + "╔" + "═" * (w - 2) + "╗" + RESET)
                    print(GREEN + "║" + RESET + BOLD + " ✦ ACESSO NÍVEL 1 CONCEDIDO ✦ ".center(w - 2) + RESET + GREEN + "║" + RESET)
                    print(GREEN + "║" + RESET + f"        AUTORIZAÇÃO: {matched_label} (Acesso geral)        ".center(w - 2) + GREEN + "║" + RESET)
                    print(GREEN + "╚" + "═" * (w - 2) + "╝" + RESET)
                    print("\n" + BOLD + GREEN + ">>> ACESSO LIBERADO: BEM-VINDO (NÍVEL 1) <<<" + RESET + "\n")
                return True
            else:
                # perfil exige nível maior que cargo declarado -> negar
                w = 66
                print(RED + "╔" + "═" * (w - 2) + "╗" + RESET)
                print(RED + "║" + RESET + BOLD + " ✖✖✖ ACESSO NEGADO ✖✖✖ ".center(w - 2) + RESET + RED + "║" + RESET)
                print(RED + "║" + RESET + f"  Biometria detectada: {matched_label} (Nível {matched_level})".center(w - 2) + RED + "║" + RESET)
                print(RED + "║" + RESET + f"  Cargo declarado: {cargo.capitalize()} (Nível {cargo_nivel}) — privilégios insuficientes  ".center(w - 2) + RED + "║" + RESET)
                print(RED + "╚" + "═" * (w - 2) + "╝" + RESET)
                print("\n" + BOLD + RED + ">>> ACESSO NEGADO — PERFIL/ CARGO INCOMPATÍVEIS <<<" + RESET + "\n")
                return False

        # nenhuma correspondência biométrica
        w = 66
        print(RED + "╔" + "═" * (w - 2) + "╗" + RESET)
        print(RED + "║" + RESET + BOLD + " ✖✖✖ ACESSO NEGADO ✖✖✖ ".center(w - 2) + RESET + RED + "║" + RESET)
        print(RED + "║" + RESET + "               Impressão digital não reconhecida               ".center(w - 2) + RED + "║" + RESET)
        print(RED + "╚" + "═" * (w - 2) + "╝" + RESET)
        print("\n" + BOLD + RED + ">>> ACESSO NEGADO — AUTENTICAÇÃO FALHOU <<<" + RESET + "\n")
        return False

    except ValueError:
        print(YELLOW + "Entrada inválida — operação abortada." + RESET)
        return False

def teste_automatico(imagens):
    """Seleciona duas imagens aleatórias e testa vários limiares."""
    _print_inline_box("TESTE AUTOMÁTICO", ["Selecionando duas imagens aleatórias e avaliando com vários limiares."])
    img_a, img_b = random.sample(imagens, 2)
    print(f"\n{CYAN}Imagem A:{RESET} {os.path.basename(img_a)}")
    print(f"{CYAN}Imagem B:{RESET} {os.path.basename(img_b)}\n")

    limiares = [50, 60, 70, 80]
    for limiar in limiares:
        print(MAGENTA + f"--- Testando com limiar = {limiar}% ---" + RESET)
        sucesso = autenticar(img_a, img_b, limiar=limiar)
        status = (GREEN + "AUTENTICADO" + RESET) if sucesso else (RED + "NEGADO" + RESET)
        print(f"Resultado: {status}\n")

def teste_manual(imagens):
    """Permite ao usuário escolher índices das imagens para comparar."""
    _print_inline_box("INICIAR TESTE", ["Escolha duas imagens para comparar. Mostrando até 10 primeiras."])
    for i, caminho in enumerate(imagens[:10], start=1):
        print(f"  {i:2d}. {os.path.basename(caminho)}")

    try:
        i1 = int(input("\nÍndice da 1ª imagem (1-10): ").strip()) - 1
        i2 = int(input("Índice da 2ª imagem (1-10): ").strip()) - 1

        if 0 <= i1 < len(imagens) and 0 <= i2 < len(imagens):
            img1 = imagens[i1]
            img2 = imagens[i2]
            limiar_str = input("Limiar de similaridade (0-100, padrão 60): ").strip()
            limiar = int(limiar_str) if limiar_str else 60
            autenticar(img1, img2, limiar=limiar)
        else:
            print(YELLOW + "Índices fora do intervalo." + RESET)
    except ValueError:
        print(YELLOW + "Entrada inválida — operação abortada." + RESET)

def teste_multiplas_comparacoes(imagens):
    """Executa várias comparações aleatórias e mostra estatísticas simples."""
    _print_inline_box("TESTE MÚLTIPLO", ["Executando múltiplas comparações aleatórias e mostrando estatísticas."])
    n = min(10, len(imagens) // 2)
    limiar = 60
    print(f"{CYAN}Realizando {n} execuções com limiar = {limiar}%...{RESET}")

    resultados = []
    for k in range(n):
        a, b = random.sample(imagens, 2)
        ok = autenticar(a, b, limiar=limiar)
        resultados.append(ok)
        print(f"  Teste {k+1:2d}: " + (GREEN + "OK" + RESET if ok else RED + "FALHA" + RESET))

    positivos = sum(resultados)
    taxa = (positivos / n) * 100 if n > 0 else 0.0

    resumo = [
        f"Total de testes: {n}",
        f"Autenticações bem-sucedidas: {positivos}",
        f"Taxa de sucesso: {taxa:.1f}%"
    ]
    _print_inline_box("RESUMO", resumo)

if __name__ == "__main__":
    main()