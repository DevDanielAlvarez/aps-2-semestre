from .load import preprocessar_imagem
from .coleta import extrair_caracteristicas, comparar_digitais
import os

def autenticar(imagem_registrada, imagem_teste, limiar=60, verbose=True):
    """
    Autentica uma impressão digital comparando com uma imagem registrada.
    Comportamento:
      - Mantém logs detalhados (pré-processamento, extração, matches) somente se verbose=True
      - Sempre exibe cabeçalho básico (início + nomes dos arquivos) e o bloco de resultado final,
        mesmo quando verbose=False — para uso nos fluxos automatizados (opção 1).
    """
    try:
        # Cabeçalho básico — sempre mostrado
        print("\n🔐 Iniciando autenticação...")
        print(f"📁 Imagem registrada: {os.path.basename(imagem_registrada)}")
        print(f"📁 Imagem de teste: {os.path.basename(imagem_teste)}")

        # Checagem de existência dos arquivos (erros também sempre exibidos)
        if not os.path.exists(imagem_registrada):
            print(f"❌ Erro: Imagem registrada não encontrada: {imagem_registrada}")
            return False
        if not os.path.exists(imagem_teste):
            print(f"❌ Erro: Imagem de teste não encontrada: {imagem_teste}")
            return False

        # Pré-processamento (mensagem de progresso só se verbose=True)
        if verbose:
            print("\n🔄 Pré-processando imagens...")
        proc_reg = preprocessar_imagem(imagem_registrada)
        proc_test = preprocessar_imagem(imagem_teste)
        if proc_reg is None or proc_test is None:
            print("❌ Erro no pré-processamento das imagens")
            return False

        # Extração de descritores (mensagens internas controladas por verbose)
        if verbose:
            print("\n🔍 Extraindo características...")
        _, desc_reg = extrair_caracteristicas(proc_reg, verbose=verbose)
        _, desc_test = extrair_caracteristicas(proc_test, verbose=verbose)
        if desc_reg is None or desc_test is None:
            print("❌ Erro na extração de características")
            return False

        # Comparação (mensagens internas controladas por verbose)
        if verbose:
            print("\n⚖️ Comparando impressões digitais...")
        similaridade = comparar_digitais(desc_reg, desc_test, verbose=verbose)

        # Resultado final — sempre exibido (mesmo quando verbose=False)
        print("\n📊 RESULTADO DA AUTENTICAÇÃO:")
        print(f"   Similaridade: {similaridade:.2f}%")
        print(f"   Limiar: {limiar}%")

        if similaridade >= limiar:
            print("✅ ACESSO PERMITIDO - Impressões digitais correspondem!")
            return True
        else:
            print("❌ ACESSO NEGADO - Impressões digitais não correspondem")
            return False

    except Exception as err:
        print(f"❌ Erro durante a autenticação: {err}")
        return False
