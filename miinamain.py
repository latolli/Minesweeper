import testi123
import json

tiedostot = {
        "tilasto_data": []
}

def main(tilastot):
    print("Valitse jokin seuraavista vaihtoehdoista:")
    while True:
        valinta = input("\nU = Uusipeli\nT = Tilastot\nL = Lopeta\n").lower()
        if valinta == "l":
            break
        elif valinta == "u":
            testi123.main()
            if testi123.tulos["lapaisy"]:
                tulos = ["Pvm: " + testi123.tulos["pvm"] +
                    " Klo: " + testi123.tulos["kello"] +
                    " Voitto!" +
                    " Pisteet: " + str(testi123.tulos["pisteet"]) +
                    " Kentän koko: " + str(testi123.tulos["kentan_koko"]) +
                    " Miinoja: " + str(testi123.tulos["lkm_miinat"]) +
                    " Aika: " + testi123.tulos["aika"] +
                    " Vuorot: " + str(testi123.tulos["klikkaukset"])]
                tulos = str(tulos).strip("[").strip("]")
                tiedostot["tilasto_data"].append(tulos)
            elif not testi123.tulos["lapaisy"]:
                tulos = ["Pvm: " + testi123.tulos["pvm"] +
                    " Klo: " + testi123.tulos["kello"] +
                    " Häviö!" +
                    " Pisteet: " + str(testi123.tulos["pisteet"]) +
                    " Kentän koko: " + str(testi123.tulos["kentan_koko"]) +
                    " Miinoja: " + str(testi123.tulos["lkm_miinat"]) +
                    " Aika: " + testi123.tulos["aika"] +
                    " Vuorot: " + str(testi123.tulos["klikkaukset"])]
                tulos = str(tulos).strip("[").strip("]")
                tiedostot["tilasto_data"].append(tulos)
            try:
                with open(tilastot, "w") as kohde:
                    json.dump(tiedostot["tilasto_data"], kohde)
            except IOError:
                print("Tiedoston tallentaminen epäonnistui :/")
        elif valinta == "t":
            if not tiedostot["tilasto_data"]:
                print("\nTallennettuja tilastoja ei ole.")
            else:
                for i, rivi in enumerate(tiedostot["tilasto_data"]):
                    print((i + 1), rivi)
        else:
            print("Valintasi ei vastaa ylläolevia vaihtoehtoja, kokeile uudestaan.")
    
    
if __name__ == "__main__":
    print("Tervetuloa pelaamaan miinaharavaa!\n")
    while True:
        try:
            tiedosto = input("Anna tiedoston nimi käyttäen pelkästään kirjaimia ja numeroita, johon haluat tallentaa tilastosi peliestä: ")
            if not tiedosto:
                break
            with open(tiedosto) as lahde:
                for tilastot in lahde:
                    tiedostot["tilasto_data"] = json.loads(tilastot)
        except FileNotFoundError:
            print("\nTämän nimistä tiedostoa ei löytynyt nykyisestä kansiostasi, joten ohjelma loi uuden kansion kyseisellä nimellä.\n")
            with open(tiedosto, "w") as kohde:
                kohde.write("")
            with open(tiedosto) as lahde:
                for tilastot in lahde:
                    tiedostot["tilasto_data"] = json.loads(tilastot)
            break   
        else:
            break
    main(tiedosto)