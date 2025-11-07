import cv2
import numpy as np

def extrair_caracteristicas(imagem, verbose=True):
    """
    Detecta e descreve pontos-chave em uma impressão digital usando ORB.
    Mantém a mesma lógica e parâmetros da versão anterior.
    Se verbose=False suprime saídas de progresso.
    """
    try:
        if imagem is None:
            return None, None

        orb = cv2.ORB_create(
            nfeatures=1000,
            scaleFactor=1.2,
            nlevels=8,
            edgeThreshold=15,
            firstLevel=0,
            WTA_K=2,
            scoreType=cv2.ORB_HARRIS_SCORE,
            patchSize=31
        )

        keypoints, descritores = orb.detectAndCompute(imagem, None)

        if descritores is not None:
            if verbose:
                print(f"✅ Extraídas {len(keypoints)} características")
        else:
            if verbose:
                print("⚠️ Nenhuma característica extraída")

        return keypoints, descritores

    except Exception as e:
        if verbose:
            print(f"Erro na extração de características: {e}")
        return None, None

def comparar_digitais(desc1, desc2, verbose=True):
    """
    Compara dois conjuntos de descritores e devolve um score de similaridade (0-100).
    Se verbose=False suprime detalhes dos matches.
    """
    try:
        if desc1 is None or desc2 is None:
            return 0

        bf = cv2.BFMatcher(cv2.NORM_HAMMING, crossCheck=True)
        matches = bf.match(desc1, desc2)

        if len(matches) == 0:
            return 0

        matches = sorted(matches, key=lambda m: m.distance)

        num_good = min(len(matches), 50)
        best = matches[:num_good]

        avg_dist = np.mean([m.distance for m in best])

        max_distance = 100
        score = max(0, 100 - (avg_dist / max_distance) * 100)

        if verbose:
            print(f"🔍 {len(matches)} matches encontrados, {num_good} melhores")
            print(f"📊 Distância média: {avg_dist:.2f}, Score: {score:.2f}")

        return score

    except Exception as e:
        if verbose:
            print(f"Erro na comparação: {e}")
        return 0
