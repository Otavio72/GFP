from PIL import Image
import pytesseract
import re

class OCR:
    def __init__(self,img,tipo):
        self.img = Image.open(img)
        self.tipo = tipo

        self.coordenadas = {
            "CPFL": (200,1950, 200+1600 , 1950+362),
            "Naturgy": (200,1950, 200+1600 , 1950+362),
            "Energisa": (200,1600, 200+1600 , 1600+362),
            "Vivo": (50 , 1150 , 50+1000, 1150+362)
        }

    def pegar_coordenadas(self):
        self.esquerda,self.topo,self.direita,self.baixo = self.coordenadas.get(self.tipo)
        return self.cortar()

    def cortar(self):
        img_cut = self.img.crop((self.esquerda,self.topo,self.direita,self.baixo))
        return self.extrair(img_cut)
        
    def extrair(self,img_cut):
        text = pytesseract.image_to_string(img_cut)

        data = re.compile(r'\b\d{2}/\d{2}/\d{4}\b')
        valor = re.compile(r'\b\d{2,3},\d{2,3}\b')

        data_encontrada = data.findall(text)
        valor_encontrado = valor.findall(text)

        data_final = data_encontrada[0] if data_encontrada else ""
        valor_final = valor_encontrado[0] if valor_encontrado else ""

        return data_final , valor_final
