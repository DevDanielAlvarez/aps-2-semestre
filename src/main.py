import sys
import os
import random

# Garantir que o pacote local seja importável (mesmo comportamento de antes)
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from carregar_dataset import baixar_e_listar_imagens
from src.autenticacao import autenticar

def main():
    """
    Entrada principal do programa de autenticação por digitais.
    Mantém a lógica e funcionalidades originais; apenas ajusta aparência e textos.
    """
    print("\n" + "#" * 60)
    print("   SISTEMA DE AUTENTICAÇÃO BIOMÉTRICA - IMPRESSÃO DIGITAL")
    print("#" * 60 + "\n")
    
    try:
        # Baixa o dataset (mesma ação de antes)
        print("Iniciando download/varredura do dataset no Kaggle...")
        imagens = baixar_e_listar_imagens()
        
        if len(imagens) < 2:
            print("Erro: não há imagens suficientes para executar comparações.\n")
            return
        
        print(f"Dataset pronto — {len(imagens)} imagens encontradas.\n")
        
        # Interface simples em loop (opções reduzidas)
        while True:
            print("\n" + "-" * 60)
            print(" MENU — ESCOLHA UMA AÇÃO ")
            print("-" * 60)
            print("[1] Iniciar teste   — selecionar imagens para comparar")
            print("[2] Sair do programa")
            print("-" * 60)
            
            escolha = input("Digite a opção (1-2): ").strip()
            
            if escolha == "1":
                teste_manual(imagens)
            elif escolha == "2":
                print("Finalizando. Até logo.")
                break
            else:
                print("Opção inválida — tente novamente.")
                
    except Exception as exc:
        print(f"Erro inesperado no fluxo principal: {exc}")

def teste_automatico(imagens):
    """Seleciona duas imagens aleatórias e testa vários limiares."""
    print("\n>>> TESTE AUTOMÁTICO")
    print("=" * 40)
    
    img_a, img_b = random.sample(imagens, 2)
    
    print(f"Imagem A: {os.path.basename(img_a)}")
    print(f"Imagem B: {os.path.basename(img_b)}")
    
    limiares = [50, 60, 70, 80]
    for limiar in limiares:
        print(f"\nTestando com limiar = {limiar}%")
        sucesso = autenticar(img_a, img_b, limiar=limiar)
        status = "AUTENTICADO" if sucesso else "NEGADO"
        print(f"Resultado: {status}")

def teste_manual(imagens):
    """Permite ao usuário escolher índices das imagens para comparar."""
    print("\n>>> INICIAR TESTE")
    print("=" * 40)
    
    print("Imagens disponíveis (até 10 mostradas):")
    for i, caminho in enumerate(imagens[:10]):
        print(f"  {i+1:2d}. {os.path.basename(caminho)}")
    
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
            print("Índices fora do intervalo.")
    except ValueError:
        print("Entrada inválida — operação abortada.")

def teste_multiplas_comparacoes(imagens):
    """Executa várias comparações aleatórias e mostra estatísticas simples."""
    print("\n>>> TESTE MULTIPLO")
    print("=" * 40)
    
    n = min(10, len(imagens) // 2)
    limiar = 60
    print(f"Realizando {n} execuções com limiar = {limiar}%...")
    
    resultados = []
    for k in range(n):
        a, b = random.sample(imagens, 2)
        ok = autenticar(a, b, limiar=limiar)
        resultados.append(ok)
        print(f"  Teste {k+1:2d}: {'OK' if ok else 'FALHA'}")
    
    positivos = sum(resultados)
    taxa = (positivos / n) * 100 if n > 0 else 0.0
    
    print("\nResumo:")
    print(f"  Total de testes: {n}")
    print(f"  Autenticações bem-sucedidas: {positivos}")
    print(f"  Taxa de sucesso: {taxa:.1f}%")

if __name__ == "__main__":
    main()