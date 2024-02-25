#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Description: Scraper com interface utilizando CustomTkinter do site casadosdados.com.br
Author: Guilherme Cugler
"""

import customtkinter
import requests
from bs4 import BeautifulSoup
import pandas as pd
import re
import os


def buscar_lotes(url):

    isExist = os.path.exists("./editais")
    if not isExist:
        os.makedirs("./editais")

    label.configure(text=f"Iniciando buscas na url {url}")
    app.update_idletasks()

    headers = {
    'authority': 'www.leilaoimovel.com.br',
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
    'accept-language': 'en-US,en;q=0.9,pt;q=0.8,ja;q=0.7',
    'cache-control': 'max-age=0',
    # 'cookie': 'zc_consent=1; zc_show=0; zc_cu=3zcd4db21ed35ff9873a8abc6a9d1edb0b-v3z2b8b524255c89cc12d334bc307da82a2114db889eb5802cda108af723f11e6f7; zc_tp=3za65c72f2ac9160f5a7723b9212c23bde9690a234fc045369d2cceb472198bc0e; XSRF-TOKEN=eyJpdiI6Im1OeHF4akNGU0FTbnNMcElGL21QdWc9PSIsInZhbHVlIjoieHRjR2grcldVajlPT1p2a3l0cUhhVFVTWHJOK29DUUVlbU1XVmtMd01Qc3M4bmZnWjlveFJNNFJNQlNLMG5LTEUxblVzd2NkbmV4ekNoOGJkT2VTUW9UbzYyQUZvdlVjU3Z2S0M3b21XazkvK0srT2kxUXQxdG5hMzRhNUF4SzIiLCJtYWMiOiIyYzBmM2I4YzBmMDZmNGUxZWY3ZDhiOWVhYTQwNDBmZWM2NTkwMDNiOTc0M2UxNzA1NmUzMzYyOTY5MzZlMGY3IiwidGFnIjoiIn0%3D; leilaoimovel_session=eyJpdiI6ImQzUU9pNDEyVTlwNUtFWjI2dG5FOWc9PSIsInZhbHVlIjoiQ1lQYzNJRlNSSkF5L0szV0NqQm5mNGhqQzhGT24xaG5uWHlOZFBhcVVJaEwycGhxbHdTTE13U0E1dWM1MDFib0J0aVBVOTlzRUk2MlZkTkplaUNnUWxORFBlRW5iSm9HVjlxQU5pUklVUS90cFdkQ0pzU3hnWHdNSWQ2V2FXeVoiLCJtYWMiOiI1OGRkNTYxNzAwYTUxMGY1MjlmNGFmM2ViOTk4YTBhNjdkNzJmODJlMzcxMmIyZWUyZjRlNjZlNjc1MjY2MjE2IiwidGFnIjoiIn0%3D; zc_cu_exp=1708917391000,1',
    'dnt': '1',
    'referer': 'https://www.leilaoimovel.com.br/encontre-seu-imovel?s=&cidade=3505708',
    'sec-ch-ua': '"Not A(Brand";v="99", "Google Chrome";v="121", "Chromium";v="121"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    'sec-fetch-dest': 'document',
    'sec-fetch-mode': 'navigate',
    'sec-fetch-site': 'same-origin',
    'sec-fetch-user': '?1',
    'upgrade-insecure-requests': '1',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36',
    }

    res = requests.get(url, headers=headers)


    soup = BeautifulSoup(res.content, "html.parser")

    places = soup.find_all("div", class_="place-box")

    places_links = []

    imoveis = []


    for place in places[:-1]:
        place_link = place.find("a", class_="Link_Redirecter")["href"]
        place_link = f"https://www.leilaoimovel.com.br{place_link}"
        places_links.append(place_link)

    # ####### REMOVER APÓS TESTES #############
    # places_links.clear()

    # places_links.append(f"https://www.leilaoimovel.com.br/imovel/sp/barueri/residencial-residencial-morada-dos-passaros-4-quartos-varanda-sacada-area-de-servico-3-wc-imovel-caixa-economica-federal-cef-1494683-10165415-venda-direta-caixa")

    # ####### REMOVER APÓS TESTES #############

    # for place_link in places_links[:5]: #LIMITAR QUANTIDADE DE BUSCAS
    for place_link in places_links:
        res = requests.get(place_link, headers=headers)

        soup = BeautifulSoup(res.content, "html.parser")

        endereco = soup.find("div", class_="adress row pb-md-4").find("div", class_="col-12 mt-2").text.strip()
        sobre_imovel = soup.find("div", class_="sobre-imovel")

        titulo = sobre_imovel.find("h1").text
        endereco = soup.find("div", class_="adress row pb-md-4").find("div", class_="col-12 mt-2").text.strip()
        detalhes_imovel = soup.find_all("div", class_="imovel-details row pb-2")
        mais_detalhes = soup.find_all("div", class_="more row pb-2")
        documentos_elementos = soup.find_all("div", class_="documments row pb-4")
        valores_imovel = soup.find_all("div", class_="imovel-prices details_price")

        for valor in valores_imovel:
            valor_imovel = valor.find("h2").text.strip()


        label.configure(text=f"Buscando Imóvel: {titulo}")
        app.update_idletasks()


        imovel = {"Imóvel": titulo,
                  "Valor": valor_imovel,
                "Endereço": endereco
                }

        for details in detalhes_imovel:
            detalhes = details.find_all("div", class_="detail")
            for detalhe in detalhes:
                titulo_detalhe = detalhe.find("p").text.strip().replace(":", "")
                valor_detalhe = detalhe.find("span").text.strip()
                imovel[f"{titulo_detalhe}"] = f"{valor_detalhe}"

        for ele in mais_detalhes:
            divs = ele.find_all("div")
            for div in divs:
                detalhe_titulo = div.find("b")      
                if detalhe_titulo is not None:
                    detalhes_div = div.text.strip().split(":", 1)
                    detalhes_nome = detalhes_div[0].strip().replace(":", "")
                    detalhes_nome = re.sub(' +', ' ', detalhes_nome)
                    detalhes_valor = detalhes_div[1].strip()
                    if detalhes_nome == "Código Imóvel":
                        detalhes_valor = detalhes_valor.split("/", 1)[0].strip()
                        imovel[f"{detalhe_titulo.text.strip().replace(":", "")}"] = f"{detalhes_valor}"
                    else:
                        imovel[f"{detalhe_titulo.text.strip().replace(":", "")}"] = f"{detalhes_valor}"


        imovel["Link"] = f'=HYPERLINK("{place_link}")'

        imoveis.append(imovel)

        df = pd.DataFrame.from_dict(imoveis)
        df.insert(len(df.columns)-1, 'Link', df.pop('Link'))
        df.insert(0, 'Código Imóvel', df.pop('Código Imóvel'))
        df.to_excel("Imoveis.xlsx", index=False)

        for elementos in documentos_elementos:
            docs = elementos.find_all("a", class_="documment")
            for doc in docs:
                tipo_documento = doc.find("span").text.strip()
                if tipo_documento == "Edital":
                    link_documento = doc["href"]
                    label.configure(text=f"Baixando Edital Imóvel Código: {imovel["Código Imóvel"]}")
                    app.update_idletasks()

                    pdf_file = requests.get(link_documento, headers=headers)
                    with open(f'./editais/Edital_{imovel["Código Imóvel"]}.pdf', 'wb') as fd:
                            fd.write(pdf_file.content)
    label.configure(text=f"Concluído com sucesso!")
    app.update_idletasks()

def button_callback():
    url = entry.get()

    if not url:
        label.configure(text="A URL não pode ficar em branco...")
        return

    buscar_lotes(url)

app = customtkinter.CTk()
app.geometry("600x150")
app.title("BUSCA IMÓVEIS")
customtkinter.set_appearance_mode("light")



entry = customtkinter.CTkEntry(app, placeholder_text="URL DA PESQUISA", width=500)
entry.pack(padx=5, pady=20)

label = customtkinter.CTkLabel(app, text="Insira uma URL para iniciar", fg_color="transparent")
label.pack(padx=1, pady=1)


button = customtkinter.CTkButton(app, text="Buscar", command=button_callback)
button.pack(padx=5, pady=5)

app.mainloop()