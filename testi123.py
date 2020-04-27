import random
import haravasto
from datetime import datetime

tila = {
    "kentta": [],
    "kayttajan_nakyma": [],
    "ajastin": 0
}

tulos = {
    "lapaisy": False,
    "aika": "00:00",
    "klikkaukset": 1,
    "pisteet": 0,
    "pvm" : "yyyy.mm.dd",
    "kello" : "00.00.00",
    "kentan_koko": 0,
    "lkm_miinat": 0
}

def piirra_kentta():
    """
    Käsittelijäfunktio, joka piirtää kaksiulotteisena listana kuvatun miinakentän
    ruudut näkyviin peli-ikkunaan. Funktiota kutsutaan aina kun pelimoottori pyytää
    ruudun näkymän päivitystä. Piirtää ikkunan sisällön käyttäen funkioita:
    -tyhjaa_ikkuna (pyyhkii edellisen kierroksen grafiikat pois)
    -piirra_tausta (asettaa ikkunan taustavärin)
    -piirra_tekstia (kirjoittaa ruudulle tekstiä)
    -aloita_ruutujen_piirto (kutsutaan ennen varsinaisen ruudukon piirtoa)
    -lisaa_piirrettava_ruutu (lisää piirrettävän ruudun)
    -piirra_ruudut (piirtää kaikki aloituksen jälkeen lisätyt ruudut)
    """
    haravasto.tyhjaa_ikkuna()
    haravasto.piirra_tausta()
    tekstin_korkeus = len(tila["kayttajan_nakyma"]) * 40 + 16
    haravasto.piirra_tekstia("Miinaharava", 9, tekstin_korkeus, vari=(0, 0, 0, 255), fontti="serif", koko=14)
    ajastimen_y = len(tila["kayttajan_nakyma"]) * 40 + 4
    aika_tekstina = "Aika: " + str(int(tila["ajastin"] / 60)).zfill(2) + ":" + str(tila["ajastin"] % 60).zfill(2)
    haravasto.piirra_tekstia(aika_tekstina, 9, ajastimen_y, vari=(0, 0, 0, 255), fontti="serif", koko=10)
    haravasto.aloita_ruutujen_piirto()
    for i in range(len(tila["kayttajan_nakyma"][0])):
        x_koordinaatti = 0 + i * 40
        for j in range(len(tila["kayttajan_nakyma"])):
            y_koordinaatti = 0 + j * 40
            haravasto.lisaa_piirrettava_ruutu(tila["kayttajan_nakyma"][j][i], x_koordinaatti, y_koordinaatti)
    haravasto.piirra_ruudut()
    
def muodosta_kentta(leveys, korkeus):
    kentta = []
    for rivi in range(korkeus):
        kentta.append([])
        for sarake in range(leveys):
            kentta[-1].append(" ")
    tila["kentta"] = kentta
    kayttajan_nakyma = []
    for rivi in range(korkeus):
        kayttajan_nakyma.append([])
        for sarake in range(leveys):
            kayttajan_nakyma[-1].append(" ")
    tila["kayttajan_nakyma"] = kayttajan_nakyma
    
def kasittele_hiiri(hiiren_x, hiiren_y, nappi, muokkaus_nappaimet):
    """
    Tätä funktiota kutsutaan kun käyttäjä klikkaa sovellusikkunaa hiirellä.
    Tulostaa hiiren sijainnin sekä painetun napin terminaaliin.
    """
    x_koordinaatti = int(hiiren_x / 40)
    y_koordinaatti = int(hiiren_y / 40)
    if nappi == haravasto.HIIRI_VASEN:
        tulvataytto(tila["kentta"], x_koordinaatti, y_koordinaatti)
        tarkista_lapaisy(1)
        tulos["klikkaukset"] += 1
    elif nappi == haravasto.HIIRI_OIKEA:
        liputus(x_koordinaatti, y_koordinaatti)
        tarkista_lapaisy(1)
        
def liputus(x_koordinaatti, y_koordinaatti):
    if tila["kayttajan_nakyma"][y_koordinaatti][x_koordinaatti] == " ":
        tila["kayttajan_nakyma"][y_koordinaatti][x_koordinaatti] = "f"
    elif tila["kayttajan_nakyma"][y_koordinaatti][x_koordinaatti] == "f":
        tila["kayttajan_nakyma"][y_koordinaatti][x_koordinaatti] = " "
        
def tarkista_lapaisy(peli_lapi):
    ruutujen_maara = len(tila["kentta"]) * len(tila["kentta"][0])
    miinojen_maara = 0
    tuntemattomien_maara = 0
    for rivi in tila["kentta"]:
        for ruutu in rivi:
            if ruutu == "x":
                miinojen_maara += 1
    for rivi in tila["kayttajan_nakyma"]:
        for ruutu in rivi:
            if ruutu == "f" or ruutu == " ":
                tuntemattomien_maara += 1
    pisteet = round((10 * (miinojen_maara / ruutujen_maara) * miinojen_maara), 1)
    aika = str(int(tila["ajastin"] / 60)) + ":" + str(tila["ajastin"] % 60).zfill(2)
    if peli_lapi == 0:
        haravasto.lopeta()
        print("\nOuch, hävisit pelin {} klikkauksen jälkeen ajassa {} ja sait {} pistettä :(".format(tulos["klikkaukset"] + 1, aika, 0))
        tulos["lapaisy"] = False
        tulos["aika"] = aika
        tulos["pisteet"] = 0
    elif tuntemattomien_maara == miinojen_maara:
        haravasto.lopeta()
        print("\nHienoa, läpäisit pelin {} klikkauksella ajassa {} ja sait {} pistettä :)".format(tulos["klikkaukset"] + 1, aika, pisteet))
        tulos["lapaisy"] = True
        tulos["aika"] = aika
        tulos["pisteet"] = pisteet

def paivitys_kasittelija(kulunut_aika):
    """
    Mittaa aikaa, kuinka kauan pelin läpäisemisessä menee.
    """
    tila["ajastin"] += 1
    
def miinoita(miinoitettava_kentta, miinojen_lkm):
    """
    Asettaa kentällä N kpl miinoja satunnaisiin paikkoihin.
    """
    jaljella = []
    for y in range(len(tila["kentta"])):
        for x in range(len(tila["kentta"][0])):
            jaljella.append((x, y))
    for i in range(miinojen_lkm):
        satunnainen_ruutu = random.choice(jaljella)
        miinoitettava_kentta[satunnainen_ruutu[1]][satunnainen_ruutu[0]] = "x"
        jaljella.remove(satunnainen_ruutu)
                   
def laske_miinat_ymparilla(miinoitettu_kentta):
    kentan_korkeus = len(miinoitettu_kentta)
    kentan_leveys = len(miinoitettu_kentta[0])
    oikea_laita = kentan_leveys - 1
    ala_laita = kentan_korkeus - 1
    jaljella = []
    for y in range(len(tila["kentta"])):
        for x in range(len(tila["kentta"][0])):
            jaljella.append((x, y))
    for y_koord, rivi in enumerate(miinoitettu_kentta):
        for x_koord, sarake in enumerate(rivi):
            if miinoitettu_kentta[y_koord][x_koord] == "x":
                continue
            elif y_koord == 0 and x_koord == 0:
                ruudut_ymparilla = [jaljella[(y_koord * kentan_leveys) + x_koord + 1],
                                    jaljella[((y_koord + 1) * kentan_leveys) + x_koord], jaljella[((y_koord + 1) * kentan_leveys) + x_koord + 1]
                                    ]
                miinat_ymparilla = 0
                for uusi_x, uusi_y in ruudut_ymparilla:
                    if miinoitettu_kentta[uusi_y][uusi_x] == "x":
                        miinat_ymparilla += 1
                    else:
                        continue
                if miinat_ymparilla > 0:
                    miinoitettu_kentta[y_koord][x_koord] = miinat_ymparilla
            elif y_koord == 0 and x_koord == oikea_laita:
                ruudut_ymparilla = [jaljella[(y_koord * kentan_leveys) + x_koord - 1],
                                    jaljella[((y_koord + 1) * kentan_leveys) + x_koord - 1], jaljella[((y_koord + 1) * kentan_leveys) + x_koord]
                                    ]
                miinat_ymparilla = 0
                for uusi_x, uusi_y in ruudut_ymparilla:
                    if miinoitettu_kentta[uusi_y][uusi_x] == "x":
                        miinat_ymparilla += 1
                    else:
                        continue
                if miinat_ymparilla > 0:
                    miinoitettu_kentta[y_koord][x_koord] = miinat_ymparilla
            elif x_koord == 0 and y_koord == ala_laita:
                ruudut_ymparilla = [jaljella[((y_koord - 1) * kentan_leveys) + x_koord], jaljella[((y_koord - 1) * kentan_leveys) + x_koord + 1],
                                    jaljella[(y_koord * kentan_leveys) + x_koord + 1]
                                    ]
                miinat_ymparilla = 0
                for uusi_x, uusi_y in ruudut_ymparilla:
                    if miinoitettu_kentta[uusi_y][uusi_x] == "x":
                        miinat_ymparilla += 1
                    else:
                        continue
                if miinat_ymparilla > 0:
                    miinoitettu_kentta[y_koord][x_koord] = miinat_ymparilla
            elif x_koord == oikea_laita and y_koord == ala_laita:
                ruudut_ymparilla = [jaljella[((y_koord - 1) * kentan_leveys) + x_koord - 1], jaljella[((y_koord - 1) * kentan_leveys) + x_koord],
                                    jaljella[(y_koord * kentan_leveys) + x_koord - 1],
                                    ]
                miinat_ymparilla = 0
                for uusi_x, uusi_y in ruudut_ymparilla:
                    if miinoitettu_kentta[uusi_y][uusi_x] == "x":
                        miinat_ymparilla += 1
                    else:
                        continue
                if miinat_ymparilla > 0:
                    miinoitettu_kentta[y_koord][x_koord] = miinat_ymparilla
            elif y_koord == 0:
                ruudut_ymparilla = [jaljella[(y_koord * kentan_leveys) + x_koord - 1], jaljella[(y_koord * kentan_leveys) + x_koord + 1],
                                    jaljella[((y_koord + 1) * kentan_leveys) + x_koord - 1], jaljella[((y_koord + 1) * kentan_leveys) + x_koord], jaljella[((y_koord + 1) * kentan_leveys) + x_koord + 1]
                                    ]
                miinat_ymparilla = 0
                for uusi_x, uusi_y in ruudut_ymparilla:
                    if miinoitettu_kentta[uusi_y][uusi_x] == "x":
                        miinat_ymparilla += 1
                    else:
                        continue
                if miinat_ymparilla > 0:
                    miinoitettu_kentta[y_koord][x_koord] = miinat_ymparilla
            elif y_koord == ala_laita:
                ruudut_ymparilla = [jaljella[(y_koord - 1) * kentan_leveys + x_koord - 1], jaljella[(y_koord - 1) * kentan_leveys + x_koord], jaljella[(y_koord - 1) * kentan_leveys + x_koord + 1],
                                    jaljella[y_koord * kentan_leveys + x_koord - 1], jaljella[y_koord * kentan_leveys + x_koord + 1]
                                    ]
                miinat_ymparilla = 0
                for uusi_x, uusi_y in ruudut_ymparilla:
                    if miinoitettu_kentta[uusi_y][uusi_x] == "x":
                        miinat_ymparilla += 1
                    else:
                        continue
                if miinat_ymparilla > 0:
                    miinoitettu_kentta[y_koord][x_koord] = miinat_ymparilla
            elif x_koord == 0:
                ruudut_ymparilla = [jaljella[(y_koord - 1) * kentan_leveys + x_koord], jaljella[(y_koord - 1) * kentan_leveys + x_koord + 1],
                                    jaljella[y_koord * kentan_leveys + x_koord + 1],
                                    jaljella[(y_koord + 1) * kentan_leveys + x_koord], jaljella[(y_koord + 1) * kentan_leveys + x_koord + 1]
                                    ]
                miinat_ymparilla = 0
                for uusi_x, uusi_y in ruudut_ymparilla:
                    if miinoitettu_kentta[uusi_y][uusi_x] == "x":
                        miinat_ymparilla += 1
                    else:
                        continue
                if miinat_ymparilla > 0:
                    miinoitettu_kentta[y_koord][x_koord] = miinat_ymparilla
            elif x_koord == oikea_laita:
                ruudut_ymparilla = [jaljella[(y_koord - 1) * kentan_leveys + x_koord - 1], jaljella[(y_koord - 1) * kentan_leveys + x_koord],
                                    jaljella[y_koord * kentan_leveys + x_koord - 1], 
                                    jaljella[(y_koord + 1) * kentan_leveys + x_koord - 1], jaljella[(y_koord + 1) * kentan_leveys + x_koord]
                                    ]
                miinat_ymparilla = 0
                for uusi_x, uusi_y in ruudut_ymparilla:
                    if miinoitettu_kentta[uusi_y][uusi_x] == "x":
                        miinat_ymparilla += 1
                    else:
                        continue
                if miinat_ymparilla > 0:
                    miinoitettu_kentta[y_koord][x_koord] = miinat_ymparilla
            else:
                ruudut_ymparilla = [jaljella[(y_koord - 1) * kentan_leveys + x_koord - 1], jaljella[(y_koord - 1) * kentan_leveys + x_koord], jaljella[(y_koord - 1) * kentan_leveys + x_koord + 1],
                                    jaljella[y_koord * kentan_leveys + x_koord - 1], jaljella[y_koord * kentan_leveys + x_koord + 1],
                                    jaljella[(y_koord + 1) * kentan_leveys + x_koord - 1], jaljella[(y_koord + 1) * kentan_leveys + x_koord], jaljella[(y_koord + 1) * kentan_leveys + x_koord + 1]
                                    ]
                miinat_ymparilla = 0
                for uusi_x, uusi_y in ruudut_ymparilla:
                    if miinoitettu_kentta[uusi_y][uusi_x] == "x":
                        miinat_ymparilla += 1
                    else:
                        continue
                if miinat_ymparilla > 0:
                    miinoitettu_kentta[y_koord][x_koord] = miinat_ymparilla
                
    
def tulvataytto(lista, x_aloitus, y_aloitus):
    """
    Merkitsee planeetalla olevat tuntemattomat alueet turvalliseksi siten, että
    täyttö aloitetaan annetusta x, y -pisteestä.
    """
    jaljella = []
    for y in range(len(tila["kentta"])):
        for x in range(len(tila["kentta"][0])):
            jaljella.append((x, y))
    kentan_korkeus = len(lista)
    kentan_leveys = len(lista[0])
    oikea_laita = kentan_leveys - 1
    ala_laita = kentan_korkeus - 1
    uusi_lista = [(x_aloitus, y_aloitus)]
    while uusi_lista:
        koordinaatit = uusi_lista.pop()
        x_koord, y_koord = koordinaatit[0], koordinaatit[1]
        if lista[y_koord][x_koord] == "x":
            tarkista_lapaisy(0)
        elif lista[y_koord][x_koord] in (1, 2, 3, 4, 5, 6, 7, 8):
            tila["kayttajan_nakyma"][y_koord][x_koord] = lista[y_koord][x_koord]
            continue
        else:
            lista[y_koord][x_koord] = "0"
            tila["kayttajan_nakyma"][y_koord][x_koord] = "0"
            if y_koord == 0 and x_koord == 0:
                ruudut_ymparilla = [jaljella[(y_koord * kentan_leveys) + x_koord], jaljella[(y_koord * kentan_leveys) + x_koord + 1],
                                    jaljella[((y_koord + 1) * kentan_leveys) + x_koord], jaljella[((y_koord + 1) * kentan_leveys) + x_koord + 1]
                                    ]
                for uusi_x, uusi_y in ruudut_ymparilla:
                    if lista[uusi_y][uusi_x] == " " or lista[uusi_y][uusi_x] in (1, 2, 3, 4, 5, 6, 7, 8):
                        uusi_lista.append((uusi_x, uusi_y))
                    else:
                        continue
            elif y_koord == 0 and x_koord == oikea_laita:
                ruudut_ymparilla = [jaljella[(y_koord * kentan_leveys) + x_koord - 1], jaljella[(y_koord * kentan_leveys) + x_koord],
                                    jaljella[((y_koord + 1) * kentan_leveys) + x_koord - 1], jaljella[((y_koord + 1) * kentan_leveys) + x_koord]
                                    ]
                for uusi_x, uusi_y in ruudut_ymparilla:
                    if lista[uusi_y][uusi_x] == " " or lista[uusi_y][uusi_x] in (1, 2, 3, 4, 5, 6, 7, 8):
                        uusi_lista.append((uusi_x, uusi_y))
                    else:
                        continue
            elif x_koord == 0 and y_koord == ala_laita:
                ruudut_ymparilla = [jaljella[((y_koord - 1) * kentan_leveys) + x_koord], jaljella[((y_koord - 1) * kentan_leveys) + x_koord + 1],
                                    jaljella[(y_koord * kentan_leveys) + x_koord], jaljella[(y_koord * kentan_leveys) + x_koord + 1]
                                    ]
                for uusi_x, uusi_y in ruudut_ymparilla:
                    if lista[uusi_y][uusi_x] == " " or lista[uusi_y][uusi_x] in (1, 2, 3, 4, 5, 6, 7, 8):
                        uusi_lista.append((uusi_x, uusi_y))
                    else:
                        continue
            elif x_koord == oikea_laita and y_koord == ala_laita:
                ruudut_ymparilla = [jaljella[((y_koord - 1) * kentan_leveys) + x_koord - 1], jaljella[((y_koord - 1) * kentan_leveys) + x_koord],
                                    jaljella[(y_koord * kentan_leveys) + x_koord - 1], jaljella[(y_koord * kentan_leveys) + x_koord]
                                    ]
                for uusi_x, uusi_y in ruudut_ymparilla:
                    if lista[uusi_y][uusi_x] == " " or lista[uusi_y][uusi_x] in (1, 2, 3, 4, 5, 6, 7, 8):
                        uusi_lista.append((uusi_x, uusi_y))
                    else:
                        continue
            elif y_koord == 0:
                ruudut_ymparilla = [jaljella[(y_koord * kentan_leveys) + x_koord - 1], jaljella[(y_koord * kentan_leveys) + x_koord], jaljella[(y_koord * kentan_leveys) + x_koord + 1],
                                    jaljella[((y_koord + 1) * kentan_leveys) + x_koord - 1], jaljella[((y_koord + 1) * kentan_leveys) + x_koord], jaljella[((y_koord + 1) * kentan_leveys) + x_koord + 1]
                                    ]
                for uusi_x, uusi_y in ruudut_ymparilla:
                    if lista[uusi_y][uusi_x] == " " or lista[uusi_y][uusi_x] in (1, 2, 3, 4, 5, 6, 7, 8):
                        uusi_lista.append((uusi_x, uusi_y))
                    else:
                        continue
            elif y_koord == ala_laita:
                ruudut_ymparilla = [jaljella[(y_koord - 1) * kentan_leveys + x_koord - 1], jaljella[(y_koord - 1) * kentan_leveys + x_koord], jaljella[(y_koord - 1) * kentan_leveys + x_koord + 1],
                                    jaljella[y_koord * kentan_leveys + x_koord - 1], jaljella[y_koord * kentan_leveys + x_koord], jaljella[y_koord * kentan_leveys + x_koord + 1]
                                    ]
                for uusi_x, uusi_y in ruudut_ymparilla:
                    if lista[uusi_y][uusi_x] == " " or lista[uusi_y][uusi_x] in (1, 2, 3, 4, 5, 6, 7, 8):
                        uusi_lista.append((uusi_x, uusi_y))
                    else:
                        continue
            elif x_koord == 0:
                ruudut_ymparilla = [jaljella[(y_koord - 1) * kentan_leveys + x_koord], jaljella[(y_koord - 1) * kentan_leveys + x_koord + 1],
                                    jaljella[y_koord * kentan_leveys + x_koord], jaljella[y_koord * kentan_leveys + x_koord + 1],
                                    jaljella[(y_koord + 1) * kentan_leveys + x_koord], jaljella[(y_koord + 1) * kentan_leveys + x_koord + 1]
                                    ]
                for uusi_x, uusi_y in ruudut_ymparilla:
                    if lista[uusi_y][uusi_x] == " " or lista[uusi_y][uusi_x] in (1, 2, 3, 4, 5, 6, 7, 8):
                        uusi_lista.append((uusi_x, uusi_y))
                    else:
                        continue
            elif x_koord == oikea_laita:
                ruudut_ymparilla = [jaljella[(y_koord - 1) * kentan_leveys + x_koord - 1], jaljella[(y_koord - 1) * kentan_leveys + x_koord],
                                    jaljella[y_koord * kentan_leveys + x_koord - 1], jaljella[y_koord * kentan_leveys + x_koord],
                                    jaljella[(y_koord + 1) * kentan_leveys + x_koord - 1], jaljella[(y_koord + 1) * kentan_leveys + x_koord]
                                    ]
                for uusi_x, uusi_y in ruudut_ymparilla:
                    if lista[uusi_y][uusi_x] == " " or lista[uusi_y][uusi_x] in (1, 2, 3, 4, 5, 6, 7, 8):
                        uusi_lista.append((uusi_x, uusi_y))
                    else:
                        continue
            else:
                ruudut_ymparilla = [jaljella[(y_koord - 1) * kentan_leveys + x_koord - 1], jaljella[(y_koord - 1) * kentan_leveys + x_koord], jaljella[(y_koord - 1) * kentan_leveys + x_koord + 1],
                                    jaljella[y_koord * kentan_leveys + x_koord - 1], jaljella[y_koord * kentan_leveys + x_koord], jaljella[y_koord * kentan_leveys + x_koord + 1],
                                    jaljella[(y_koord + 1) * kentan_leveys + x_koord - 1], jaljella[(y_koord + 1) * kentan_leveys + x_koord], jaljella[(y_koord + 1) * kentan_leveys + x_koord + 1]
                                    ]
                for uusi_x, uusi_y in ruudut_ymparilla:
                    if lista[uusi_y][uusi_x] == " " or lista[uusi_y][uusi_x] in (1, 2, 3, 4, 5, 6, 7, 8):
                        uusi_lista.append((uusi_x, uusi_y))
                    else:
                        continue
    
def main():
    """
    Lataa pelin grafiikat, luo peli-ikkunan ja asettaa siihen piirtokäsittelijän. Tekee abaut kaiken.
    """
    tila["ajastin"] = 0
    tulos["klikkaukset"] = 0
    tulos["pisteet"] = 0
    pvm_kello = str(datetime.today())[:19]
    pvm, kello = pvm_kello.split(" ")
    tulos["pvm"] = pvm
    tulos["kello"] = kello
    print("Määritä haluamasi kentän mitat")
    while True:
        try:
            leveys = int(input("Ruutujen määrä X-suunnassa (kokonaisluku): "))
            korkeus = int(input("Ruutujen määrä Y-suunnassa (kokonaisluku): "))
            miinat = int(input("Anna miinojen lukumäärä (kokonaisluku): "))
            if leveys < 2 or korkeus < 2:
                print("\nKentän sivujen tulee olla vähintään 2 ruutua ja enintään 100 ruutua, koitappa vielä\n")
                continue
            elif leveys > 100 or korkeus > 100:
                print("\nKentän sivujen tulee olla vähintään 2 ruutua ja enintään 100 ruutua, koitappa vielä\n")
                continue
            tulos["kentan_koko"] = leveys * korkeus
            tulos["lkm_miinat"] = miinat
        except ValueError:
            print("\nEipä ollu kokonaisluku, koitappa vielä\n")
        else:
            break
    muodosta_kentta(leveys, korkeus)
    miinoita(tila["kentta"], miinat)
    laske_miinat_ymparilla(tila["kentta"])
    ikkunan_leveys = int(len(tila["kentta"][0]) * 40)
    ikkunan_korkeus = int(len(tila["kentta"]) * 40) + 40
    haravasto.lataa_kuvat("spritet.zip\spritet")
    haravasto.luo_ikkuna(ikkunan_leveys, ikkunan_korkeus)
    haravasto.aseta_piirto_kasittelija(piirra_kentta)
    haravasto.aseta_hiiri_kasittelija(kasittele_hiiri)
    haravasto.aseta_toistuva_kasittelija(paivitys_kasittelija, 1)
    haravasto.aloita()
    
if __name__ == "__main__":
    main()