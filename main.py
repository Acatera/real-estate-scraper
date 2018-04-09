from classes.Website import Website

def web1():
    print("Function: web1")

websites = [Website("web1", web1)]
debug = False

print("Real estate web scraper")

if debug:
    print("websites")
    print(websites)

for site in websites:
    site.scraper()

# olx? - invite-only
# publi24? - api seems not implemented
# homezz.ro
# la jumate.ro
# romimo.ro
# imobiliare.ro
