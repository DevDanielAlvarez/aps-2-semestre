from load import preprocessar_imagem
from coleta import extrair_caracteristicas, comparar_digitais
import os

def autenticar(imagem_registrada, imagem_teste, limiar=60, verbose=True, show_outcome=True, show_header=True):
    """
    Autentica uma impressão digital comparando com uma imagem registrada.
    - verbose: mostra logs detalhados de pré-processamento / extração / matches
    - show_outcome: mostra a linha textual final (✅/❌)
    - show_header: mostra o cabeçalho inicial (🔐 Iniciando...) e o bloco numérico.
    """
    try:
        # Cabeçalho básico — opcional
        if show_header:
            print("\n🛡️ Iniciando processo de autenticação...")
            print(f"📁 Imagem registrada: {os.path.basename(imagem_registrada)}")
            print(f"📁 Imagem de teste: {os.path.basename(imagem_teste)}")

        # Checagem de existência dos arquivos (erros sempre exibidos)
        if not os.path.exists(imagem_registrada):
            if show_header:
                print(f"❌ Erro: Imagem registrada não encontrada: {imagem_registrada}")
            return False
        if not os.path.exists(imagem_teste):
            if show_header:
                print(f"❌ Erro: Imagem de teste não encontrada: {imagem_teste}")
            return False

        # Pré-processamento (mensagem de progresso só se verbose=True)
        if verbose and show_header:
            print("\n🔄 Pré-processando imagens...")
        proc_reg = preprocessar_imagem(imagem_registrada)
        proc_test = preprocessar_imagem(imagem_teste)
        if proc_reg is None or proc_test is None:
            if show_header:
                print("❌ Erro no pré-processamento das imagens")
            return False

        # Extração de descritores
        if verbose and show_header:
            print("\n🔍 Extraindo características...")
        _, desc_reg = extrair_caracteristicas(proc_reg, verbose=verbose)
        _, desc_test = extrair_caracteristicas(proc_test, verbose=verbose)
        if desc_reg is None or desc_test is None:
            if show_header:
                print("❌ Erro na extração de características")
            return False

        # Comparação
        if verbose and show_header:
            print("\n⚖️ Comparando impressões digitais...")
        similaridade = comparar_digitais(desc_reg, desc_test, verbose=verbose)

        # Bloco numérico de resultado: exibido se show_header True (padrão) ou se show_outcome True
        if show_header or show_outcome:
            print("\n📬 RESULTADO DA AUTENTICAÇÃO:")
            print(f"   Similaridade: {similaridade:.2f}%")
            print(f"   Limiar: {limiar}%")

        if similaridade >= limiar:
            if show_outcome:
                print("✅ ACESSO PERMITIDO - Impressões digitais correspondem!")
            return True
        else:
            if show_outcome:
                print("❌ ACESSO NEGADO - Impressões digitais não correspondem")
            return False

    except Exception as err:
        if show_header or show_outcome:
            print(f"❌ Erro durante a autenticação: {err}")
        return False
