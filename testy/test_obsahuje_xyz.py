from scrapovani_jobs import obsahuje_python, obsahuje_javascript, obsahuje_java, obsahuje_c_sharp, obsahuje_sql, obsahuje_scala

def test_obsahuje_python_ano():
    text = "tralala lalala Python skákal pes přes oves"
    ocekavany_vysledek = True
    fakticky_vysledek = obsahuje_python(text)
    assert ocekavany_vysledek == fakticky_vysledek

def test_obsahuje_python_ne():
    text = "tralala lalala skákal pes přes oves"
    ocekavany_vysledek = False
    fakticky_vysledek = obsahuje_python(text)
    assert ocekavany_vysledek == fakticky_vysledek

def test_obsahuje_javascript_ano_cele_jmeno():
    text = "tralala lalala Javascript skákal pes přes oves"
    ocekavany_vysledek = True
    fakticky_vysledek = obsahuje_javascript(text)
    assert ocekavany_vysledek == fakticky_vysledek

def test_obsahuje_javascript_ano_zkratka():
    text = "tralala lalala JS skákal pes přes oves"
    ocekavany_vysledek = True
    fakticky_vysledek = obsahuje_javascript(text)
    assert ocekavany_vysledek == fakticky_vysledek
    
def test_obsahuje_javascript_ano_angular():
    text = "tralala lalala angular skákal pes přes oves"
    ocekavany_vysledek = True
    fakticky_vysledek = obsahuje_javascript(text)
    assert ocekavany_vysledek == fakticky_vysledek
    
def test_obsahuje_javascript_ano_react():
    text = "tralala lalala react skákal pes přes oves"
    ocekavany_vysledek = True
    fakticky_vysledek = obsahuje_javascript(text)
    assert ocekavany_vysledek == fakticky_vysledek
    
def test_obsahuje_javascript_ne():
    text = "tralala lalala skákal pes přes oves"
    ocekavany_vysledek = False
    fakticky_vysledek = obsahuje_javascript(text)
    assert ocekavany_vysledek == fakticky_vysledek
    
def test_obsahuje_java_ano():
    text = "tralala lalala java skákal pes přes oves"
    ocekavany_vysledek = True
    fakticky_vysledek = obsahuje_java(text)
    assert ocekavany_vysledek == fakticky_vysledek
    
def test_obsahuje_java_ano_lomitko():
    text = "tralala lalala java/ skákal pes přes oves"
    ocekavany_vysledek = True
    fakticky_vysledek = obsahuje_java(text)
    assert ocekavany_vysledek == fakticky_vysledek
    
def test_obsahuje_java_ne():
    text = "tralala lalala skákal pes přes oves"
    ocekavany_vysledek = False
    fakticky_vysledek = obsahuje_java(text)
    assert ocekavany_vysledek == fakticky_vysledek
    
def test_obsahuje_csharp_ano():
    text = "tralala lalala c# skákal pes přes oves"
    ocekavany_vysledek = True
    fakticky_vysledek = obsahuje_c_sharp(text)
    assert ocekavany_vysledek == fakticky_vysledek
    
def test_obsahuje_csharp_ne():
    text = "tralala lalala skákal pes přes oves"
    ocekavany_vysledek = False
    fakticky_vysledek = obsahuje_c_sharp(text)
    assert ocekavany_vysledek == fakticky_vysledek
    
def test_obsahuje_sql_ano():
    text = "tralala lalala sql skákal pes přes oves"
    ocekavany_vysledek = True
    fakticky_vysledek = obsahuje_sql(text)
    assert ocekavany_vysledek == fakticky_vysledek
    
def test_obsahuje_sql_ne():
    text = "tralala lalala skákal pes přes oves"
    ocekavany_vysledek = False
    fakticky_vysledek = obsahuje_sql(text)
    assert ocekavany_vysledek == fakticky_vysledek

def test_obsahuje_scala_ano():
    text = "tralala lalala scala skákal pes přes oves"
    ocekavany_vysledek = True
    fakticky_vysledek = obsahuje_scala(text)
    assert ocekavany_vysledek == fakticky_vysledek
    
def test_obsahuje_scala_ne():
    text = "tralala lalala skákal pes přes oves"
    ocekavany_vysledek = False
    fakticky_vysledek = obsahuje_scala(text)
    assert ocekavany_vysledek == fakticky_vysledek