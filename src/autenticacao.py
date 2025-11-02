from .preprocessamento import preprocessar_imagem
from .extracao import extrair_caracteristicas, comparar_digitais
import os

def autenticar(imagem_registrada, imagem_teste, limiar=60):
    """
    Autentica uma impressão digital comparando com uma imagem registrada.
    Mantém compatibilidade com a versão anterior.
    """
    try:
        print("\n🔐 Iniciando autenticação...")
        print(f"📁 Imagem registrada: {os.path.basename(imagem_registrada)}")
        print(f"📁 Imagem de teste: {os.path.basename(imagem_teste)}")

        # Checagem de existência dos arquivos
        if not os.path.exists(imagem_registrada):
            print(f"❌ Erro: Imagem registrada não encontrada: {imagem_registrada}")
            return False
        if not os.path.exists(imagem_teste):
            print(f"❌ Erro: Imagem de teste não encontrada: {imagem_teste}")
            return False

        # Pré-processamento
        print("\n🔄 Pré-processando imagens...")
        proc_reg = preprocessar_imagem(imagem_registrada)
        proc_test = preprocessar_imagem(imagem_teste)
        if proc_reg is None or proc_test is None:
            print("❌ Erro no pré-processamento das imagens")
            return False

        # Extração de descritores
        print("\n🔍 Extraindo características...")
        _, desc_reg = extrair_caracteristicas(proc_reg)
        _, desc_test = extrair_caracteristicas(proc_test)
        if desc_reg is None or desc_test is None:
            print("❌ Erro na extração de características")
            return False

        # Comparação
        print("\n⚖️ Comparando impressões digitais...")
        similaridade = comparar_digitais(desc_reg, desc_test)

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
