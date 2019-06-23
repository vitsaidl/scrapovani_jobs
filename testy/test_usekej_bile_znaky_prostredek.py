from scrapovani_jobs import usekej_bile_znaky_prostredek

def test_odstranuje_bile_znaky():
    retezec = "jedna     dva   \ntri"
    ocekavany = "jedna dva tri"
    skutecny = usekej_bile_znaky_prostredek(retezec)
    assert ocekavany == skutecny

def test_retezec_bez_bilych_znaku_vraci_nezmeneny():
    retezec = "tralala"
    ocekavany = "tralala"
    skutecny = usekej_bile_znaky_prostredek(retezec)
    assert ocekavany == skutecny