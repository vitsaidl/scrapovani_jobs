from scrapovani_jobs import naparsuj_min_max_mzdu


def test_rozpeti_od_do():
    mzda = "25 000 - 35 000 Kč"
    ocekavane_min = 25000
    ocekavane_max = 35000
    vracene_min, vracene_max = naparsuj_min_max_mzdu(mzda)
    assert ocekavane_min == vracene_min
    assert ocekavane_max == vracene_max


def test_jen_jedna_castka():
    mzda = "25 000 Kč"
    ocekavane_min = 25000
    ocekavane_max = 25000
    vracene_min, vracene_max = naparsuj_min_max_mzdu(mzda)
    assert ocekavane_min == vracene_min
    assert ocekavane_max == vracene_max


def test_mzda_v_eurech_jen_jedna_castka():
    mzda = "1 000 EUR"
    ocekavane_min = 25500
    ocekavane_max = 25500
    vracene_min, vracene_max = naparsuj_min_max_mzdu(mzda)
    assert ocekavane_min == vracene_min
    assert ocekavane_max == vracene_max


def test_mzda_v_eurech_od_do():
    mzda = "1 000 - 2 000 EUR"
    ocekavane_min = 25500
    ocekavane_max = 51000
    vracene_min, vracene_max = naparsuj_min_max_mzdu(mzda)
    assert ocekavane_min == vracene_min
    assert ocekavane_max == vracene_max
