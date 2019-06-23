from scrapovani_jobs import vrat_datum_z_timestampy

def test_vrat_datum_z_timestampy():
    timestampa = "2019-06-04T12:45:12"
    ocekavane_datum = "2019-06-04"
    datum_z_fce = vrat_datum_z_timestampy(timestampa)
    assert ocekavane_datum == datum_z_fce