from scrapovani_jobs import obsahuje_retezec


def test_retezec_je_v_textu():
    text = "tralala lalala Python skákal pes přes oves"
    retezec = "python"
    ocekavany_vysledek = True
    fakticky_vysledek = obsahuje_retezec(text, retezec)
    assert ocekavany_vysledek == fakticky_vysledek


def test_retezec_neni_v_textu():
    text = "tralala lalala skákal pes přes oves"
    retezec = "python"
    ocekavany_vysledek = False
    fakticky_vysledek = obsahuje_retezec(text, retezec)
    assert ocekavany_vysledek == fakticky_vysledek
