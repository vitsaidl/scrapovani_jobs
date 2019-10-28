# -*- coding: utf-8 -*-
"""
Created on Sun Jun 16 21:43:02 2019

@author: Vit Saidl
"""

import datetime
import os.path
import re
import numpy as np
import pandas as pd
import yaml
import fpdf
from matplotlib.ticker import MaxNLocator
import matplotlib.pyplot as plt
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

    def __init__(self, *args):
        self.technologies = args[0]["technologies"]

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

        slovnik_informaci = {
            'pozice' : ocistena_pozice,
            'zamestnavatel': usekej_bile_znaky_okraj(zamestnavatel),
            'adresa': usekej_bile_znaky_okraj(adresa),
            'Praha' : obsahuje_retezec(adresa, "praha"),
            'plat': plat_bez_bilych_znaku,
            'plat_min': plat_minimum,
            'plat_max': plat_maximum,
            'platnost od' : vrat_datum_z_timestampy(platnost_od),
            'platnost do' : vrat_datum_z_timestampy(platnost_do),
            'inzerat' : telo_inzeratu,
            }

        for element in self.technologies:
            klic_titulka = "titulka_" + element
            klic_inzerat = "inzerat_" + element
            inzerat_string = " ".join(telo_inzeratu)
            slovnik_informaci[klic_titulka] = obsahuje_retezec(ocistena_pozice, element)
            slovnik_informaci[klic_inzerat] = obsahuje_retezec(inzerat_string, element)

        yield slovnik_informaci

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
    """Vrací True/False na zákadě toho, zda text obsahuje retezec

    Args:
        text (string): Text (titulka/tělo inzerátu), který je prohledáván
        retezec (string): Řetězec, který v titulce/těle inzerátu hledáme

    Returns:
        bool: Informace o tom, zda e retezec v textu k nalezení
    """
    text = text.lower()
    retezec = retezec.lower()
    #aby se do javy nezapocitaval i javascript
    if retezec == "java":
        matchnuti = re.search("java[^s]", text)
        index_hledaneho = 1 if matchnuti is not None else -1
    else:
        index_hledaneho = text.find(retezec)
    return not index_hledaneho == -1

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

def vrat_slovnik_sum(dataframe_inzeraty, technologie):
    """Spočítá výskyty technologií v titulkách a tělech inzerátů

    Args:
        dataframe_inzeraty (dataframe): Pandí dataframe s infem o inzerátech

    Returns:
        dict: Klíče - {titulka|inzerat}_technologie, hodnoty - počet výskytů
    """

    slovnik_sum_technologii = {}
    for prvek in technologie:
        sloupec_titulka = "titulka_" + prvek
        sloupec_inzerat = "inzerat_" + prvek
        print(dataframe_inzeraty[sloupec_titulka])
        slovnik_sum_technologii[sloupec_titulka] = int(dataframe_inzeraty[sloupec_titulka].sum())
        slovnik_sum_technologii[sloupec_inzerat] = int(dataframe_inzeraty[sloupec_inzerat].sum())

    return slovnik_sum_technologii

def vytvoreni_obrazku(dataframe_inzeraty, pouze_praha, pocet_vyskytu, technologie):
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
    titulky_sumy = []
    inzeraty_sumy = []
    for prvek in technologie:
        sloupec_titulka = "titulka_" + prvek
        sloupec_inzerat = "inzerat_" + prvek
        titulky_sumy.append(pocet_vyskytu[sloupec_titulka])
        inzeraty_sumy.append(pocet_vyskytu[sloupec_inzerat])

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
    osy.set_xticklabels(technologie)
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
    with open("technologies.yaml") as file:
        technologies = yaml.load(file, Loader=yaml.FullLoader)
    crawler = CrawlerProcess({
        "USER_AGENT": "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1)",
        "FEED_FORMAT": "csv",
        "FEED_URI": f"scrapovana_data\\prace_{aktualni_datum()}.csv",
        "LOG_LEVEL" : "WARN"
        })
    print("Scrapování začíná")
    crawler.crawl(InzeratyJobsSpider, technologies)
    crawler.start()

    inzeraty, jen_praha_flag = priprava_framu()
    sumy_tech = vrat_slovnik_sum(inzeraty, technologies["technologies"])
    vytvoreni_obrazku(inzeraty, jen_praha_flag, sumy_tech, technologies["technologies"])
    vytvoreni_pdf(inzeraty, jen_praha_flag)
    print("Report byl vyroben")
