# 💸 Gerenciador de Finanças Pessoais (GFP)

[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](https://github.com/Otavio72/GFP/blob/main/LICENSE)

**GFP** é uma aplicação web full stack desenvolvida para facilitar o gerenciamento e visualização de contas por meio de gráficos, com extração automática de dados e edição de boletos enviados.

---

## 🛠️ Sobre o projeto

O GFP permite o envio de boletos das empresas CPFL, Energisa, Naturgy e VIVO. Os dados desses boletos são extraídos via OCR, seguidos de uma filtragem com **expressões regulares** para capturar apenas o valor e a data do documento. Por fim, os dados são exibidos em três gráficos utilizando a biblioteca Chart.js.

### Funcionalidades principais

- 🧾 Extração automática de dados via OCR  
- 🔐 Login e registro de usuários  
- 📚 Histórico de boletos enviados  
- 🧑‍💼 Painel de perfil e edição de boletos  

---

## 💻 Layout da aplicação

### Página inicial 
![Página Inicial 1](https://github.com/Otavio72/assets/blob/main/gfp1.png)
![Página Inicial 2](https://github.com/Otavio72/assets/blob/main/gfp2.png)

### Como funciona o envio de boletos
![Envio de boletos](https://github.com/Otavio72/assets/blob/main/gfp3.png)

### GIF
![GIF](https://github.com/Otavio72/assets/blob/main/GFP_gif.gif)

### Como funciona (detalhado)
![Como Funciona](https://github.com/Otavio72/assets/blob/main/gfp4.png)

---

## 🗂️ Modelo conceitual

![Modelo Conceitual](https://github.com/Otavio72/assets/blob/main/modeloGFPFinal.png)

---

## 🚀 Tecnologias utilizadas

### 🔙 Back end
- Python
- Django

### 🎨 Front end
- HTML
- CSS
- JavaScript

---

## ⚙️ Como executar o projeto

### ✅ Pré-requisitos

- Python 3.11+
- Ambiente virtual configurado

### 📦 Instalação

```bash
# clonar repositório
git clone https://github.com/Otavio72/GFP.git

Ative o ambiente virtual:
  python -m venv .venv

No Windows (PowerShell):
  ```powershell
  .venv\Scripts\Activate.ps1

No Linux/macOS:
  source .venv/bin/activate

Instale as dependências:
  pip install -r requirements.txt

Rode as migrações do banco de dados
  python manage.py migrate

python manage.py runserver

Acesse o projeto no navegador:
http://127.0.0.1:8000/
```
👤 Como acessar o sistema
Para acessar o GFP, faça seu cadastro:
1. Acesse: http://127.0.0.1:8000/register_view/
2. Preencha o formulário de cadastro
3. Após o registro, você será redirecionado para a página de login

# Autor
Otávio Ribeiro
[🔗 LinkedIn](https://www.linkedin.com/in/otávio-ribeiro-57a359197)
