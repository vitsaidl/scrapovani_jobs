from scrapovani_jobs import aktualni_datum

def test_aktualni_datum_je_string():
    vysledna_hodnota = aktualni_datum()
    assert isinstance(vysledna_hodnota, str)

def test_aktualni_datum_ma_ocekavane_hodnoty():
    vysledna_hodnota = aktualni_datum()
    den = int(vysledna_hodnota[0:2])
    mesic = int(vysledna_hodnota[2:4])
    rok = int(vysledna_hodnota[4:6])
    assert 1 <= den <=31
    assert 1 <= mesic <=12
    assert 19 <= rok <=29