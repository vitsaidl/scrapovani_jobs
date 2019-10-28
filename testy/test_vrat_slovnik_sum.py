from scrapovani_jobs import vrat_slovnik_sum
import pandas as pd

def test_spravne_secteni_technologii():
    testovaci_dataframe = pd.read_csv(r".\\testy\\testovaci_frame.txt", header=0, sep=",")
    technologie = ["python", "java", "javascript"]
    ocekavany_slovnik = {
        "titulka_python" : 0,
        "titulka_java" : 1,
        "titulka_javascript" : 0,
        "inzerat_python" : 1,
        "inzerat_java" : 2,
        "inzerat_javascript" : 1,
    }
    fakticky_slovnik = vrat_slovnik_sum(testovaci_dataframe, technologie)
    assert ocekavany_slovnik == fakticky_slovnik
    
def test_spatne_secteni_technologii():
    testovaci_dataframe = pd.read_csv(r".\\testy\\testovaci_frame.txt", header=0, sep=",")
    technologie = ["python", "java", "javascript"]
    ocekavany_slovnik = {
        "titulka_python" : 0,
        "titulka_java" : 1,
        "titulka_javascript" : 0,
        "inzerat_python" : 1,
        "inzerat_java" : 2,
        "inzerat_javascript" : 0,
    }
    fakticky_slovnik = vrat_slovnik_sum(testovaci_dataframe, technologie)
    assert ocekavany_slovnik != fakticky_slovnik