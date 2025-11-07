import cv2
import numpy as np

def preprocessar_imagem(caminho_imagem):
    """
    Pré-processa uma imagem de impressão digital para melhorar a extração de características.
    Mantém comportamento compatível com a versão anterior.
    """
    try:
        # Carrega a imagem em tons de cinza
        gray = cv2.imread(caminho_imagem, cv2.IMREAD_GRAYSCALE)
        if gray is None:
            raise ValueError(f"Não foi possível carregar a imagem: {caminho_imagem}")
        
        # Normaliza o tamanho para um padrão fixo
        resized = cv2.resize(gray, (300, 300))
        
        # Suaviza para reduzir ruído
        blurred = cv2.GaussianBlur(resized, (3, 3), 0)
        
        # Aumenta o contraste localmente com CLAHE
        clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8, 8))
        equalized = clahe.apply(blurred)
        
        # Binariza utilizando Otsu
        _, binary = cv2.threshold(equalized, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
        
        # Limpeza com operações morfológicas (fechar e abrir)
        kernel = np.ones((2, 2), dtype=np.uint8)
        cleaned = cv2.morphologyEx(binary, cv2.MORPH_CLOSE, kernel)
        cleaned = cv2.morphologyEx(cleaned, cv2.MORPH_OPEN, kernel)
        
        return cleaned

    except Exception as e:
        print(f"Erro no pré-processamento: {e}")
        return None
