from PIL import Image
import pytesseract
import re

# A classe OCR é responsável por processar a imagem do boleto e extrair a data e o valor.
# Com base no tipo de conta informado, ela recorta uma região específica da imagem e aplica OCR.

class OCR:
    def __init__(self,img,tipo):
        self.img = Image.open(img) # Abre a imagem do boleto
        self.tipo = tipo

        # Define as coordenadas de recorte para cada tipo de boleto
        self.coordenadas = {
            "CPFL": (200,1950, 200+1600 , 1950+362),
            "Naturgy": (200,1950, 200+1600 , 1950+362),
            "Energisa": (200,1600, 200+1600 , 1600+362),
            "Vivo": (50 , 1150 , 50+1000, 1150+362)
        }

    # Inicia o processo de extração de dados com base nas coordenadas definidas
    def pegar_coordenadas(self):
        self.esquerda,self.topo,self.direita,self.baixo = self.coordenadas.get(self.tipo)
        return self.cortar()

    # Recorta a imagem na região definida para o tipo de boleto
    def cortar(self):
        img_cut = self.img.crop((self.esquerda,self.topo,self.direita,self.baixo))
        return self.extrair(img_cut)
        
    # Aplica OCR e extrai a data e o valor utilizando expressões regulares
    def extrair(self,img_cut):
        text = pytesseract.image_to_string(img_cut)

        # Expressões regulares para encontrar data (dd/mm/aaaa) e valor (ex: 123,45)
        data = re.compile(r'\b\d{2}/\d{2}/\d{4}\b')
        valor = re.compile(r'\b\d{2,3},\d{2,3}\b')

        data_encontrada = data.findall(text)
        valor_encontrado = valor.findall(text)

        # Retorna o primeiro valor encontrado (ou string vazia)
        data_final = data_encontrada[0] if data_encontrada else ""
        valor_final = valor_encontrado[0] if valor_encontrado else ""

        return data_final , valor_final
