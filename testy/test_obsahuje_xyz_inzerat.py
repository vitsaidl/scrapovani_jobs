from scrapovani_jobs import obsahuje_python_inzerat, obsahuje_javascript_inzerat, obsahuje_java_inzerat, obsahuje_c_sharp_inzerat, obsahuje_sql_inzerat, obsahuje_scala_inzerat

def test_obsahuje_python_inz__ano():
    text = ["tralala lalala Python skákal pes přes oves", "přes zelenou louku"]
    ocekavany_vysledek = True
    fakticky_vysledek = obsahuje_python_inzerat(text)
    assert ocekavany_vysledek == fakticky_vysledek

def test_obsahuje_python_inz_ne():
    text = ["tralala lalala skákal pes přes oves", "přes zelenou louku"]
    ocekavany_vysledek = False
    fakticky_vysledek = obsahuje_python_inzerat(text)
    assert ocekavany_vysledek == fakticky_vysledek
    
def test_obsahuje_javascript_inz_ano_cele_jmeno():
    text = ["tralala lalala Javascript skákal pes přes oves", "přes zelenou louku"]
    ocekavany_vysledek = True
    fakticky_vysledek = obsahuje_javascript_inzerat(text)
    assert ocekavany_vysledek == fakticky_vysledek

def test_obsahuje_javascript_inz_ano_zkratka():
    text = ["tralala lalala JS skákal pes přes oves", "přes zelenou louku"]
    ocekavany_vysledek = True
    fakticky_vysledek = obsahuje_javascript_inzerat(text)
    assert ocekavany_vysledek == fakticky_vysledek
    
def test_obsahuje_javascript_inz_ano_angular():
    text = ["tralala lalala angular skákal pes přes oves", "přes zelenou louku"]
    ocekavany_vysledek = True
    fakticky_vysledek = obsahuje_javascript_inzerat(text)
    assert ocekavany_vysledek == fakticky_vysledek
    
def test_obsahuje_javascript_inz_ano_react():
    text = ["tralala lalala react skákal pes přes oves", "přes zelenou louku"]
    ocekavany_vysledek = True
    fakticky_vysledek = obsahuje_javascript_inzerat(text)
    assert ocekavany_vysledek == fakticky_vysledek
    
def test_obsahuje_javascript_inz_ne():
    text = ["tralala lalala skákal pes přes oves", "přes zelenou louku"]
    ocekavany_vysledek = False
    fakticky_vysledek = obsahuje_javascript_inzerat(text)
    assert ocekavany_vysledek == fakticky_vysledek
    
def test_obsahuje_java_inz_ano():
    text = ["tralala lalala java skákal pes přes oves", "přes zelenou louku"]
    ocekavany_vysledek = True
    fakticky_vysledek = obsahuje_java_inzerat(text)
    assert ocekavany_vysledek == fakticky_vysledek
    
def test_obsahuje_java_inz_ano_lomitko():
    text = ["tralala lalala java/ skákal pes přes oves", "přes zelenou louku"]
    ocekavany_vysledek = True
    fakticky_vysledek = obsahuje_java_inzerat(text)
    assert ocekavany_vysledek == fakticky_vysledek
    
def test_obsahuje_java_inz_ne():
    text = ["tralala lalala skákal pes přes oves", "přes zelenou louku"]
    ocekavany_vysledek = False
    fakticky_vysledek = obsahuje_java_inzerat(text)
    assert ocekavany_vysledek == fakticky_vysledek
    
def test_obsahuje_csharp_inz_ano():
    text = ["tralala lalala c# skákal pes přes oves", "přes zelenou louku"]
    ocekavany_vysledek = True
    fakticky_vysledek = obsahuje_c_sharp_inzerat(text)
    assert ocekavany_vysledek == fakticky_vysledek
    
def test_obsahuje_csharp_inz_ne():
    text = ["tralala lalala skákal pes přes oves", "přes zelenou louku"]
    ocekavany_vysledek = False
    fakticky_vysledek = obsahuje_c_sharp_inzerat(text)
    assert ocekavany_vysledek == fakticky_vysledek
    
def test_obsahuje_sql_inz_ano():
    text = ["tralala lalala sql skákal pes přes oves", "přes zelenou louku"]
    ocekavany_vysledek = True
    fakticky_vysledek = obsahuje_sql_inzerat(text)
    assert ocekavany_vysledek == fakticky_vysledek
    
def test_obsahuje_sql_inz_ne():
    text = ["tralala lalala skákal pes přes oves", "přes zelenou louku"]
    ocekavany_vysledek = False
    fakticky_vysledek = obsahuje_sql_inzerat(text)
    assert ocekavany_vysledek == fakticky_vysledek

def test_obsahuje_scala_inz_ano():
    text = ["tralala lalala Scala skákal pes přes oves", "přes zelenou louku"]
    ocekavany_vysledek = True
    fakticky_vysledek = obsahuje_scala_inzerat(text)
    assert ocekavany_vysledek == fakticky_vysledek
    
def test_obsahuje_scala_inz_ne():
    text = ["tralala lalala skákal pes přes oves", "přes zelenou louku"]
    ocekavany_vysledek = False
    fakticky_vysledek = obsahuje_scala_inzerat(text)
    assert ocekavany_vysledek == fakticky_vysledek