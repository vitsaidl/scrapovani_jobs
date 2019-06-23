from scrapovani_jobs import vrat_slovnik_sum
import pandas as pd

def test_spravne_secteni_technologii():
    testovaci_dataframe = pd.read_csv(r".\\testy\\testovaci_frame.txt", header=0, sep=",")
    ocekavany_slovnik = {
        "titulka_python" : 0,
        "titulka_java" : 1,
        "titulka_js" : 0,
        "titulka_csharp" : 0,
        "titulka_sql" : 0,
        "titulka_scala" : 1,
        "inzerat_python" : 1,
        "inzerat_java" : 2,
        "inzerat_js" : 1,
        "inzerat_csharp" : 0,
        "inzerat_sql" : 0,
        "inzerat_scala" : 0,
    }
    fakticky_slovnik = vrat_slovnik_sum(testovaci_dataframe)
    assert ocekavany_slovnik == fakticky_slovnik
    
def test_spatne_secteni_technologii():
    testovaci_dataframe = pd.read_csv(r".\\testy\\testovaci_frame.txt", header=0, sep=",")
    ocekavany_slovnik = {
        "titulka_python" : 0,
        "titulka_java" : 1,
        "titulka_js" : 0,
        "titulka_csharp" : 0,
        "titulka_sql" : 0,
        "titulka_scala" : 1,
        "inzerat_python" : 1,
        "inzerat_java" : 2,
        "inzerat_js" : 0,
        "inzerat_csharp" : 0,
        "inzerat_sql" : 0,
        "inzerat_scala" : 0,
    }
    fakticky_slovnik = vrat_slovnik_sum(testovaci_dataframe)
    assert ocekavany_slovnik != fakticky_slovnik