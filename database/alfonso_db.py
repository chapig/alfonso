import os, json

class Currencies:

    def fetch_name(self, currency):

        with open("/root/alfonso/database/currencies.json", "r") as outfile:
            p_j = json.loads(outfile.read())
            for i in p_j:
                if currency in i:
                    return i[1]
            else:
                return currency.upper()




