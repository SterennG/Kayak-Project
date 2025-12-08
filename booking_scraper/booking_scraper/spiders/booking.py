# booking_scraper/spiders/booking.py

import scrapy
from ..items import BookingHotelItem

class BookingSpider(scrapy.Spider):
    name = 'booking'
    allowed_domains = ['booking.com']
    
    # Liste de villes
    french_cities = [
        "Mont-Saint-Michel", "Saint-Malo", "Bayeux", "Le Havre", "Rouen", "Paris", "Amiens", "Lille",
        "Strasbourg", "Haut-Koenigsbourg", "Colmar", "Eguisheim", "Besancon", "Dijon",
        "Annecy", "Grenoble", "Lyon", "Gorges du Verdon", "Bormes-les-Mimosas", "Cassis",
        "Marseille", "Aix-en-Provence", "Avignon", "Uzès", "Nîmes", "Aigues-Mortes",
        "Saintes-Maries-de-la-Mer", "Collioure", "Carcassonne", "Ariège", "Toulouse",
        "Montauban", "Biarritz", "Bayonne", "La Rochelle"
    ]

    def start_requests(self):
        # Boucle sur chaque ville pour créer une requête
        for city in self.french_cities:
            search_url = f'https://www.booking.com/searchresults.fr.html?ss={city}'
            
            # Envoi de la requête et on passe la ville dans le dictionnaire 'meta'
            # pour la récupérer plus tard dans la fonction parse.
            yield scrapy.Request(
                url=search_url, 
                callback=self.parse, 
                meta={'city_name': city}
            )

    def parse(self, response):
        city = response.meta['city_name']
        
        # 1. Parcourir les listes d'hôtels
        hotel_listings = response.css('div[data-testid="property-card"]')
        
        for listing in hotel_listings:
            # On prépare l'Item, mais on ne le renvoie pas tout de suite
            item = BookingHotelItem()
            item['city'] = city
            
            # Extraction des données de la page de résultats
            
            # URL
            relative_url = listing.css('h3 a[data-testid="title-link"]::attr(href)').get()
            item['url'] = response.urljoin(relative_url) if relative_url else None
            
            # Nom
            item['name'] = listing.css('h3 a[data-testid="title-link"] div[data-testid="title"]::text').get()
            
            # Score
            score_text = listing.css('div[data-testid="review-score"] div::text').get()
            item['score'] = score_text.strip() if score_text else None

            # Description (sélecteurs basés sur l'inspection)
            item['description'] = listing.css('div.fff1944c52::text').get()
            
            # 2. Suivre le lien vers la page de détails pour extraire les coordonnées
            if item['url']:
                yield scrapy.Request(
                    url=item['url'],
                    callback=self.parse_hotel_details,
                    # On passe l'item déjà rempli pour le compléter après
                    meta={'item': item}
                )
        

    def parse_hotel_details(self, response):
        # Récupération de l'item créé à l'étape précédente
        item = response.meta['item']
        
        # Extraction des coordonnées
        
        # 1. Extraire la chaîne "latitude,longitude"
        coords_string = response.css('a[data-atlas-latlng]::attr(data-atlas-latlng)').get()

        if coords_string:
            # 2. Séparer la chaîne par la virgule
            try:
                # S'assurer que la chaîne contient une virgule et deux parties
                latitude_val, longitude_val = coords_string.split(',', 1)
                
                # 3. Assigner les valeurs à l'Item
                item['latitude'] = latitude_val.strip()
                item['longitude'] = longitude_val.strip()
                
            except ValueError:
                # Gérer le cas où la chaîne est mal formatée
                item['latitude'] = None
                item['longitude'] = None
        else:
            item['latitude'] = None
            item['longitude'] = None
            
        # Renvoyer l'Item complété
        yield item