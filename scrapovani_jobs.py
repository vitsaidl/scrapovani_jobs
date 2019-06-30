# -*- coding: utf-8 -*-
"""
Created on Sun Jun 16 21:43:02 2019

@author: Vit Saidl
"""

import datetime
import os.path
import re
import fpdf
import matplotlib.pyplot as plt
from matplotlib.ticker import MaxNLocator
import numpy as np
import pandas as pd
import scrapy
from scrapy.crawler import CrawlerProcess

class Pdf(fpdf.FPDF):
    """Třída umožňující narozdíl od defaultní fpdf.FPDF zobrazení zápatí
    """
    def footer(self):
        self.set_y(-15)
        self.set_font("Times", "I", 10)
        datum = datetime.datetime.now().strftime("%d. %m. %Y")
        self.cell(0, 10, f"Datum platnosti {datum}", 0, 0, "L")
        self.cell(0, 10, f"Strana {self.page_no()}", 0, 0, "R")

class InzeratyJobsSpider(scrapy.Spider):
    """Třída zajišťující dolování informací ze stránek
    """
    name = 'inzeraty_for'
    start_urls = ['https://www.jobs.cz/prace/is-it-vyvoj-aplikaci-a-systemu/']

    def parse(self, response):
        """Defaultně volaná fce koukající na seznam inzerátů
        """
        dalsi_strana_selector = "a.button.button--slim.pager__next ::attr(href)"
        dalsi_strana = response.css(dalsi_strana_selector).extract_first()
        if dalsi_strana:
            yield scrapy.Request(response.urljoin(dalsi_strana), callback=self.parse)

        for prvek in response.css('div.standalone.search-list__item'):
            pozice_selector = ".search-list__main-info__title__link ::text"
            zamestnavatel_selector = ".search-list__main-info__company ::text"
            adresa_selector = ".search-list__main-info__address :nth-child(2) ::text"
            platy_selector = ".search-list__salary :nth-child(2) ::text"
            platnost_od = "span.label-added ::attr(data-label-added-valid-from)"
            platnost_do = "span.label-added ::attr(data-label-added-valid-to)"
            odkaz_selector = "a.search-list__main-info__title__link ::attr(href)"

            pozice = prvek.css(pozice_selector).extract_first()
            zamestnavatel = prvek.css(zamestnavatel_selector).extract_first()
            adresa = prvek.css(adresa_selector).extract_first()
            platy = prvek.css(platy_selector).extract_first()
            platnost_od = prvek.css(platnost_od).extract_first()
            platnost_do = prvek.css(platnost_do).extract_first()
            odkaz = prvek.css(odkaz_selector).extract_first()

            metaslovnik = {
                "pozice" : pozice,
                "zamestnavatel" : zamestnavatel,
                "adresa" : adresa,
                "platy" : platy,
                "platnost_od" : platnost_od,
                "platnost_do" : platnost_do
                }
            #v prvcích jsou i neinzerátové věci, které ale v sobě pozice_selector
            #nemají
            if pozice is not None:
                yield response.follow(odkaz, self.parsuj_inzerat, meta=metaslovnik)

    def parsuj_inzerat(self, response):
        """Fce volaná dcí parse; kouká na jendotlivé inzeráty
        """
        pozice = response.meta["pozice"]
        zamestnavatel = response.meta["zamestnavatel"]
        adresa = response.meta["adresa"]

        platy = response.meta["platy"]
        platnost_od = response.meta["platnost_od"]
        platnost_do = response.meta["platnost_do"]
        plat_bez_bilych_znaku = usekej_bile_znaky_prostredek(usekej_bile_znaky_okraj(platy))
        plat_minimum, plat_maximum = naparsuj_min_max_mzdu(plat_bez_bilych_znaku)
        ocistena_pozice = usekej_bile_znaky_okraj(pozice)

        #krom defaultní šablony inzerátů existují i custom šablony
        #jeden typ byl u lmc, jiný u t-mobilu
        #používají je ale i jiné firmy
        telo_inz_klasik_sel = "div.standalone.jobad__body ::text"
        telo_inz_lmc_sel = "div.cse-block.offset-bottom--large ::text"
        telo_inz_tmobile_sel = "div.cse-block ::text"

        telo_inz_klasik = response.css(telo_inz_klasik_sel).extract()
        telo_inz_lmc = response.css(telo_inz_lmc_sel).extract()
        telo_inz_tmobile = response.css(telo_inz_tmobile_sel).extract()

        if telo_inz_klasik:
            telo_inzeratu = telo_inz_klasik
        elif telo_inz_lmc:
            telo_inzeratu = telo_inz_lmc
        else:
            telo_inzeratu = telo_inz_tmobile

        yield {'pozice' : ocistena_pozice,
               'zamestnavatel': usekej_bile_znaky_okraj(zamestnavatel),
               'adresa': usekej_bile_znaky_okraj(adresa),
               'Praha' : obsahuje_retezec(adresa, "praha"),
               'plat': plat_bez_bilych_znaku,
               'plat_min': plat_minimum,
               'plat_max': plat_maximum,
               'platnost od' : vrat_datum_z_timestampy(platnost_od),
               'platnost do' : vrat_datum_z_timestampy(platnost_do),
               'titulka_python' : obsahuje_python(ocistena_pozice),
               'titulka_java' : obsahuje_java(ocistena_pozice),
               'titulka_javascript' : obsahuje_javascript(ocistena_pozice),
               'titulka_csharp' : obsahuje_c_sharp(ocistena_pozice),
               'titulka_sql' : obsahuje_sql(ocistena_pozice),
               'titulka_scala' : obsahuje_scala(ocistena_pozice),
               'titulka_elasticsearch' : obsahuje_elasticsearch(ocistena_pozice),
               'titulka_cpp' : obsahuje_cpp(ocistena_pozice),
               'titulka_netsuite' : obsahuje_netsuite(ocistena_pozice),
               'titulka_keras' : obsahuje_keras(ocistena_pozice),
               'inzerat' : telo_inzeratu,
               'inzerat_python' : obsahuje_python_inzerat(telo_inzeratu),
               'inzerat_java' : obsahuje_java_inzerat(telo_inzeratu),
               'inzerat_javascript' : obsahuje_javascript_inzerat(telo_inzeratu),
               'inzerat_csharp' : obsahuje_c_sharp_inzerat(telo_inzeratu),
               'inzerat_sql' : obsahuje_sql_inzerat(telo_inzeratu),
               'inzerat_scala' : obsahuje_sql_inzerat(telo_inzeratu),
               'inzerat_elasticsearch' : obsahuje_elasticsearch_inzerat(telo_inzeratu),
               'inzerat_cpp' : obsahuje_cpp_inzerat(telo_inzeratu),
               'inzerat_netsuite' : obsahuje_netsuite_inzerat(telo_inzeratu),
               'inzerat_keras' : obsahuje_keras_inzerat(telo_inzeratu),
               }

    def closed(self, reason):
        """Fce volaná, když spider všechny stránky proleze
        """
        print("Informace z jobs.cz byly vydolovány.")

def aktualni_datum():
    """Vrací aktuální datum ve formátu DDMMYY, např. 220619 pro 22. 6. 2019

    Returns:
        string: Stringová podoba aktuálního data
    """
    return datetime.datetime.now().strftime("%d%m%y")

def smazani_dnesniho_souboru():
    """Maže soubor se scrapovanými daty za aktuální datum

    Scrapy při opětovném běhu cílový soubor nemaže, ale k němu appenduje.
    Tím pádem bychom následně při zpracovávání dat narazili na duplicity.
    """
    jmeno_souboru = f"prace_{aktualni_datum()}.csv"
    soubor_existuje = os.path.exists(f".\\scrapovana_data\\{jmeno_souboru}")
    if soubor_existuje:
        os.remove(f".\\scrapovana_data\\{jmeno_souboru}")



def usekej_bile_znaky_okraj(retezec):
    """Vrací slovo očištěné o bíle znaky na začátku/konci řetězce, resp. "Neuvedeno"

    "Neuvedeno" se vrátí v případě, že žádný řetězec nebyl naparsován (obvykle
    nastává u platu).

    Args:
        retezec(string/None)

    Returns:
        string: Očištěný řetězec či "Neuvedeno"
    """
    if retezec is None:
        return "Neuvedeno"
    else:
        return retezec.strip()

def usekej_bile_znaky_prostredek(retezec):
    """Hromadu bílých znaků uprostřed řetězce nahrazuje za jednu mezeru

    Args:
        retezec(string/None)

    Returns:
        string: O nadměrné  bílé znaky očištěný řetězec
    """
    separovany_retezec = retezec.split()
    znovuspojeny_retezec = " ".join(separovany_retezec)
    return znovuspojeny_retezec

def vrat_datum_z_timestampy(timestampa):
    """Vrací datum (pokud přijde timestampa) či "Neuvedeno" (pokud přijde None)

    Args:
        timestampa(string): Řetězec ve formátu datumTcas

    Returns:
        string: Datum či neuvedeno
    """
    if timestampa is not None:
        separovana_timestampa = timestampa.split("T")
        return separovana_timestampa[0]
    else:
        return "Neuvedeno"

def naparsuj_min_max_mzdu(platove_rozpeti):
    """Z řetězce vybere max a min hodnotu mzdy + přepočítá případné eura na koruny

    Args:
        platove_rozpeti (string/None): Formát řetězce buďto X Kč - Y Kč, anebo X Kč

    Returns:
        integer: Dva integery - minimální a maximální nabízená mzda v Kč
    """
    kurs_euro = 25.5
    rozpeti_bez_mezer = platove_rozpeti.replace(" ", "")

    matchnuti = re.search("(\\d+)[-–]?(\\d*)(\\w+)", rozpeti_bez_mezer)
    if matchnuti is None:
        minimum = "Neuvedeno"
        maximum = "Neuvedeno"
    elif matchnuti.group(2) == "":
        minimum = int(matchnuti.group(1))
        maximum = minimum
    else:
        minimum = int(matchnuti.group(1))
        maximum = int(matchnuti.group(2))

    if (matchnuti is not None and matchnuti.group(3) == "EUR"):
        minimum = round(kurs_euro * minimum)
        maximum = round(kurs_euro * maximum)

    return minimum, maximum

def obsahuje_retezec(text, retezec):
    """Vrací Ture/False na zákadě toho, zda text obsahuje retezec

    Args:
        text (string): Text (titulka/tělo inzerátu), který je prohledáván
        retezec (string): Řetězec, který v titulce/těle inzerátu hledáme

    Returns:
        bool: Informace o tom, zda e retezec v textu k nalezení
    """
    text = text.lower()
    index_hledaneho = text.find(retezec)
    if index_hledaneho == -1:
        return False
    else:
        return True

def obsahuje_python(popis_pozice):
    """Kontroluje, zda se v titulce inzerátu objevuje Python
    """
    return obsahuje_retezec(popis_pozice, "python")

def obsahuje_javascript(popis_pozice):
    """Kontroluje, zda se v titulce inzerátu objevuje Javascript, Angular či React
    """
    #mezery na obe stranykonci, neb by to mohlo chytat i jina slova (pred se chyta na Node.js)
    return (obsahuje_retezec(popis_pozice, "javascript") or obsahuje_retezec(popis_pozice, "js ")
            or obsahuje_retezec(popis_pozice, "angular") or obsahuje_retezec(popis_pozice, "react"))

def obsahuje_java(popis_pozice):
    """Kontroluje, zda se v titulce inzerátu objevuje Java
    """
    return (obsahuje_retezec(popis_pozice, "java ") or obsahuje_retezec(popis_pozice, "java/"))

def obsahuje_c_sharp(popis_pozice):
    """Kontroluje, zda se v titulce inzerátu objevuje C#
    """
    return obsahuje_retezec(popis_pozice, "c#")

def obsahuje_sql(popis_pozice):
    """Kontroluje, zda se v titulce inzerátu objevuje SQL
    """
    return obsahuje_retezec(popis_pozice, "sql")

def obsahuje_scala(popis_pozice):
    """Kontroluje, zda se v titulce inzerátu objevuje Scala
    """
    return obsahuje_retezec(popis_pozice, "scala")

def obsahuje_elasticsearch(popis_pozice):
    """Kontroluje, zda se v titulce inzerátu objevuje Elastisearch
    """
    return obsahuje_retezec(popis_pozice, "elasticsearch") or obsahuje_retezec(popis_pozice, "kibana")

def obsahuje_cpp(popis_pozice):
    """Kontroluje, zda se v titulce inzerátu objevuje C++
    """
    return obsahuje_retezec(popis_pozice, "c++")

def obsahuje_netsuite(popis_pozice):
    """Kontroluje, zda se v titulce inzerátu objevuje Netsuite
    """
    return obsahuje_retezec(popis_pozice, "netsuite")

def obsahuje_keras(popis_pozice):
    """Kontroluje, zda se v titulce inzerátu objevuje Keras
    """
    return obsahuje_retezec(popis_pozice, "keras")

def obsahuje_python_inzerat(inzerat):
    """Kontroluje, zda se v těle inzerátu objevuje Python
    """
    #inzerat je fakticky list, ktery chceme slozit v jeden string
    popis_pozice = " ".join(inzerat)
    return obsahuje_python(popis_pozice)

def obsahuje_javascript_inzerat(inzerat):
    """Kontroluje, zda se v těle inzerátu objevuje Javascript, Angular či React
    """
    #inzerat je fakticky list, ktery chceme slozit v jeden string
    popis_pozice = " ".join(inzerat)
    return obsahuje_javascript(popis_pozice)

def obsahuje_java_inzerat(inzerat):
    """Kontroluje, zda se v těle inzerátu objevuje Java
    """
    #inzerat je fakticky list, ktery chceme slozit v jeden string
    popis_pozice = " ".join(inzerat)
    return obsahuje_java(popis_pozice)

def obsahuje_c_sharp_inzerat(inzerat):
    """Kontroluje, zda se v těle inzerátu objevuje C#
    """
    #inzerat je fakticky list, ktery chceme slozit v jeden string
    popis_pozice = " ".join(inzerat)
    return obsahuje_c_sharp(popis_pozice)

def obsahuje_sql_inzerat(inzerat):
    """Kontroluje, zda se v těle inzerátu objevuje SQl
    """
    #inzerat je fakticky list, ktery chceme slozit v jeden string
    popis_pozice = " ".join(inzerat)
    return obsahuje_sql(popis_pozice)

def obsahuje_scala_inzerat(inzerat):
    """Kontroluje, zda se v těle inzerátu objevuje Scala
    """
    #inzerat je fakticky list, ktery chceme slozit v jeden string
    popis_pozice = " ".join(inzerat)
    return obsahuje_scala(popis_pozice)

def obsahuje_elasticsearch_inzerat(inzerat):
    """Kontroluje, zda se v těle inzerátu objevuje Elasticsearch
    """
    #inzerat je fakticky list, ktery chceme slozit v jeden string
    popis_pozice = " ".join(inzerat)
    return obsahuje_elasticsearch(popis_pozice)

def obsahuje_cpp_inzerat(inzerat):
    """Kontroluje, zda se v těle inzerátu objevuje C++
    """
    #inzerat je fakticky list, ktery chceme slozit v jeden string
    popis_pozice = " ".join(inzerat)
    return obsahuje_cpp(popis_pozice)

def obsahuje_netsuite_inzerat(inzerat):
    """Kontroluje, zda se v těle inzerátu objevuje Netsuite
    """
    #inzerat je fakticky list, ktery chceme slozit v jeden string
    popis_pozice = " ".join(inzerat)
    return obsahuje_netsuite(popis_pozice)

def obsahuje_keras_inzerat(inzerat):
    """Kontroluje, zda se v těle inzerátu objevuje Keras
    """
    #inzerat je fakticky list, ktery chceme slozit v jeden string
    popis_pozice = " ".join(inzerat)
    return obsahuje_keras(popis_pozice)

def priprava_framu():
    """Načítá data do pandího dataframu a upravuje je

    Returns:
        dataframe: Pandí dataframe - co řádek, to inzerát
        bool: Info o tom, zda chce uživatel jen informace o Praze (True) či o celé ČR
    """
    nazev_zdroj_souboru = f".\\scrapovana_data\\prace_{aktualni_datum()}.csv"
    dataframe_inzeraty = pd.read_csv(nazev_zdroj_souboru, header=0, sep=",")
    chce_prahu = input("Chcete mít ve statistice pouze Prahu (Ano/Ne)?\n")
    if chce_prahu in ("Ano", "ANO", "ano"):
        dataframe_inzeraty = dataframe_inzeraty[dataframe_inzeraty["Praha"] == True]
        pouze_praha = True
    else:
        pouze_praha = False
    dataframe_inzeraty = dataframe_inzeraty[dataframe_inzeraty["plat_min"].notnull()]
    #"Neuvedeno" se zde převede na NaN
    dataframe_inzeraty["plat_min"] = dataframe_inzeraty["plat_min"].apply(pd.to_numeric,
                                                                          errors='coerce')
    dataframe_inzeraty["plat_max"] = dataframe_inzeraty["plat_max"].apply(pd.to_numeric,
                                                                          errors='coerce')
    dataframe_inzeraty = dataframe_inzeraty[dataframe_inzeraty["plat_min"].notnull()]
    return dataframe_inzeraty, pouze_praha

def vrat_slovnik_sum(dataframe_inzeraty):
    """Spočítá výskyty technologií v titulkách a tělech inzerátů

    Args:
        dataframe_inzeraty (dataframe): Pandí dataframe s infem o inzerátech

    Returns:
        dict: Klíče - {titulka|inzerat}_technologie, hodnoty - počet výskytů
    """
    slovnik_sum_technologii = {
        "titulka_python" : int(dataframe_inzeraty["titulka_python"].sum()),
        "titulka_java" : int(dataframe_inzeraty["titulka_java"].sum()),
        "titulka_js" : int(dataframe_inzeraty["titulka_javascript"].sum()),
        "titulka_csharp" : int(dataframe_inzeraty["titulka_csharp"].sum()),
        "titulka_sql" : int(dataframe_inzeraty["titulka_sql"].sum()),
        "titulka_scala" : int(dataframe_inzeraty["titulka_scala"].sum()),
        "titulka_elasticsearch" : int(dataframe_inzeraty["titulka_elasticsearch"].sum()),
        "titulka_cpp" : int(dataframe_inzeraty["titulka_cpp"].sum()),
        "titulka_netsuite" : int(dataframe_inzeraty["titulka_netsuite"].sum()),
        "titulka_keras" : int(dataframe_inzeraty["titulka_keras"].sum()),
        "inzerat_python" : int(dataframe_inzeraty["inzerat_python"].sum()),
        "inzerat_java" : int(dataframe_inzeraty["inzerat_java"].sum()),
        "inzerat_js" : int(dataframe_inzeraty["inzerat_javascript"].sum()),
        "inzerat_csharp" : int(dataframe_inzeraty["inzerat_csharp"].sum()),
        "inzerat_sql" : int(dataframe_inzeraty["inzerat_sql"].sum()),
        "inzerat_scala" : int(dataframe_inzeraty["inzerat_scala"].sum()),
        "inzerat_elasticsearch" : int(dataframe_inzeraty["inzerat_elasticsearch"].sum()),
        "inzerat_cpp" : int(dataframe_inzeraty["inzerat_cpp"].sum()),
        "inzerat_netsuite" : int(dataframe_inzeraty["inzerat_netsuite"].sum()),
        "inzerat_keras" : int(dataframe_inzeraty["inzerat_keras"].sum()),
        }
    return slovnik_sum_technologii

def vytvoreni_obrazku(dataframe_inzeraty, pouze_praha, pocet_vyskytu):
    """Vytváří png obrázky - histogram mezd a bar graf o zastoupení technologií

    Args:
        dataframe_inzeraty (dataframe): Informace o inzerátech
        pouze_praha (bool): Zda jsou data platná jen pro Prahu (True) či celou ČR
        pocet_vyskytu (dict): Mapuje technologii na počet jejího výskytu v inzerátech
    """
    fig_mzdy = plt.figure(figsize=(10, 6))
    plt.hist([dataframe_inzeraty["plat_min"], dataframe_inzeraty["plat_max"]], 50)
    plt.xlabel("Mzda v Kč")
    plt.ylabel("Počet pozic")
    plt.legend(["Spodní hranice mzdového intervalu", "Horní hranice mzdového intervalu"],
               loc=1)
    if pouze_praha:
        lokace = "jen Praha"
    else:
        lokace = "celá ČR"
    plt.title(f"Histogram mezd IT pozic nabízených na jobs.cz ({lokace})")
    plt.savefig(f".\\grafy\\histogram_mzdy_{aktualni_datum()}.png")

    plt.clf()
    #graf - boxplot - srovnavajici zastoupeni technologii
    titulky_sumy = (pocet_vyskytu["titulka_python"],
                    pocet_vyskytu["titulka_java"],
                    pocet_vyskytu["titulka_js"],
                    pocet_vyskytu["titulka_csharp"],
                    pocet_vyskytu["titulka_sql"],
                    pocet_vyskytu["titulka_scala"],
                    pocet_vyskytu["titulka_elasticsearch"],
                    pocet_vyskytu["titulka_cpp"],
                    pocet_vyskytu["titulka_netsuite"],
                    pocet_vyskytu["titulka_keras"]
                    )
    inzeraty_sumy = (pocet_vyskytu["inzerat_python"],
                     pocet_vyskytu["inzerat_java"],
                     pocet_vyskytu["inzerat_js"],
                     pocet_vyskytu["inzerat_csharp"],
                     pocet_vyskytu["inzerat_sql"],
                     pocet_vyskytu["inzerat_scala"],
                     pocet_vyskytu["inzerat_elasticsearch"],
                     pocet_vyskytu["inzerat_cpp"],
                     pocet_vyskytu["inzerat_netsuite"],
                     pocet_vyskytu["inzerat_keras"]
                     )
    osy = plt.axes()
    stredy_baru = np.arange(len(titulky_sumy))

    #aby byly na yové ose jen integery
    osy.yaxis.set_major_locator(MaxNLocator(integer=True))
    sirka_baru = 0.35
    levy_sloupec = osy.bar(stredy_baru - sirka_baru/2,
                           titulky_sumy,
                           sirka_baru,
                           label="Titulky inzerátů")
    pravy_sloupec = osy.bar(stredy_baru + sirka_baru/2,
                            inzeraty_sumy,
                            sirka_baru,
                            label="Těla inzerátů")

    osy.set_xticks(stredy_baru)
    osy.set_xticklabels(("Python", "Java", "Javascript", "C#", "SQL", "Scala",
                         "Elasticsearch", "C++", "Netsuite", "Keras"))
    osy.legend()
    plt.title(f"Počet výskytů technologií v inzerátech na jobs.cz ({lokace})")
    plt.savefig(f".\\grafy\\srovnani_tech_{aktualni_datum()}.png")

def vytvoreni_pdf(dataframe_inzeraty, pouze_praha):
    """Funkce vytváří pdf soubor se souhrnými informacemi

    Args:
        dataframe_inzeraty (dataframe): Informace o inzerátech
        pouze_praha (bool): Zda jsou data platná jen pro Prahu (True) či celou ČR
    """
    report = Pdf()
    report.add_page()
    report.add_font("Times", "", r"c:\windows\fonts\times.ttf", uni=True)
    report.set_font("Times", "B", 20)
    if pouze_praha:
        oblast_platnosti = "Praze"
    else:
        oblast_platnosti = "celé republice"
    text_nadpisu = f"IT pozice v inzerátech z jobs.cz v {oblast_platnosti}"
    report.cell(w=0, h=10, txt=text_nadpisu, ln=1, align="C")

    report.set_font("Times", "", 14)
    report.image(name=f".\\grafy\\histogram_mzdy_{aktualni_datum()}.png", w=180)
    median_min_platu = int(dataframe_inzeraty["plat_min"].median())
    median_max_platu = int(dataframe_inzeraty["plat_max"].median())
    text_median = ("Mediánová hodnota spodní hranice nabízených mezd v "
                   f"{oblast_platnosti} činí {median_min_platu} Kč. Medián horní "
                   f"hranice představuje {median_max_platu} Kč.")
    report.multi_cell(w=0, h=10, txt=text_median)
    report.image(name=f".\\grafy\\srovnani_tech_{aktualni_datum()}.png", w=180)

    nazev_souboru = f".\\reporty\\jobs_{datetime.datetime.now().strftime('%d%m%y')}.pdf"
    report.output(name=nazev_souboru, dest="F")

if __name__ == '__main__':
    smazani_dnesniho_souboru()
    crawler = CrawlerProcess({
        "USER_AGENT": "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1)",
        "FEED_FORMAT": "csv",
        "FEED_URI": f"scrapovana_data\\prace_{aktualni_datum()}.csv",
        "LOG_LEVEL" : "WARN"
        })
    print("Scrapování začíná")
    crawler.crawl(InzeratyJobsSpider)
    crawler.start()

    inzeraty, jen_praha_flag = priprava_framu()
    sumy_tech = vrat_slovnik_sum(inzeraty)
    vytvoreni_obrazku(inzeraty, jen_praha_flag, sumy_tech)
    vytvoreni_pdf(inzeraty, jen_praha_flag)
    print("Report byl vyroben")
