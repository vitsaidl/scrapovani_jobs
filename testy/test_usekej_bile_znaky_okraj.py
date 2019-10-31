from scrapovani_jobs import usekej_bile_znaky_okraj


def test_odstranuje_bile_znaky():
    retezec = "   tral ala      "
    ocekavany = "tral ala"
    skutecny = usekej_bile_znaky_okraj(retezec)
    assert ocekavany == skutecny


def test_retezec_neobklopeny_bilymi_znaky_vraci_nezmeneny():
    retezec = "tral ala"
    ocekavany = "tral ala"
    skutecny = usekej_bile_znaky_okraj(retezec)
    assert ocekavany == skutecny


def test_pro_vstup_none_vraci_neuvedeno():
    retezec = None
    ocekavany = "Neuvedeno"
    skutecny = usekej_bile_znaky_okraj(retezec)
    assert ocekavany == skutecny
