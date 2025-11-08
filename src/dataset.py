import kagglehub
import os
import time

def baixar_e_listar_imagens():
    """
    Baixa um dataset de impressões digitais via Kaggle e retorna uma lista com os caminhos das imagens.
    Mantém a mesma funcionalidade e comportamento da versão anterior.
    """
    try:
        print("🔄 Iniciando download do dataset no Kaggle...")
        dataset_id = "kundurunonieshreddy/finger-print-dataset"
        print(f"🔌 Dataset solicitado: {dataset_id}")

        inicio = time.time()
        destino = kagglehub.dataset_download(dataset_id)
        duracao = time.time() - inicio

        print(f"📁 Diretório retornado: {destino}")
        print(f"⏱ Tempo gasto na requisição: {duracao:.2f} segundos")

        imagens = []
        extensoes_validas = (".png", ".jpg", ".jpeg", ".bmp", ".tiff")

        for raiz, _, arquivos in os.walk(destino):
            for nome in arquivos:
                if nome.lower().endswith(extensoes_validas):
                    imagens.append(os.path.join(raiz, nome))

        total = len(imagens)
        print(f"📬 Encontradas {total} imagens no dataset.")

        if total:
            print("📁 Exemplos (até 5):")
            for i, caminho in enumerate(imagens[:5], start=1):
                print(f"   {i}. {os.path.basename(caminho)}")
            if total > 5:
                print(f"   ... e mais {total - 5} arquivos")
        else:
            print("⚠️ Nenhuma imagem localizada no diretório do dataset.")

        return imagens

    except Exception as e:
        print(f"❌ Falha ao baixar ou listar o dataset: {e}")
        print("💡 Cheque sua conexão ou credenciais do Kaggle e tente novamente.")
        return []
