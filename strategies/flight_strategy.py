#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
FLIGHT STRATEGY
==============
Strategia kategoryzacji przelotów.
"""

import re
from strategies.base_strategy import CategoryStrategy
from models import TravelRecord

class FlightStrategy(CategoryStrategy):
    """Strategia kategoryzacji przelotów"""
    
    @property
    def priority(self) -> int:
        return 4
    
    def can_handle(self, record: TravelRecord) -> bool:
        """Sprawdza czy to przelot"""
        hotel, destination, raw_hotel, raw_destination = self.get_normalized_values(record)
        
        # Jeśli hotel został znormalizowany do "przelot" - to jest przelot!
        if hotel == 'przelot':
            return True
            
        # Wykluczenia - NIE są przelotami mimo że mogą zawierać kody lotnisk lub słowo "przelot"
        if 'jacht motorowy' in hotel or 'valerie' in hotel:
            return False  # to są kitesafari
        if 'noclegi' in hotel:
            return False  # to są noclegi, nie przeloty
        if 'jacht' in hotel:
            return False  # jachty to kitesafari, nie przeloty
        if 'brazil kite safari' in hotel:
            return False  # to Brazylia
        if 'riu creole' in hotel:
            return False  # to Mauritius
        if 'bez przelotu' in hotel:
            return False  # pakiety BEZ przelotu to nie przeloty
        # YALLA KITE to zawsze szkolenie, nie przelot!
        if 'yalla kite' in hotel:
            return False
        
        # Kitesafari przypadki - nie są przelotami (chyba że wyraźnie bilety lotnicze)
        if ('kitesafari' in hotel or 'kite safari' in hotel):
            # Tylko przypadki które wyraźnie wskazują na bilety lotnicze to przeloty
            if not ('bilet lot' in hotel or 
                    'lot' in hotel and ('kat-' in hotel or 'waw-' in hotel or '-hrg-' in hotel)):
                return False
        
        # Bilety (różne warianty)
        if 'bilet' in hotel or 'bilet' in destination:
            return True
        
        # Bilety instruktorskie
        if 'instruktor' in hotel or 'instruktor' in destination:
            return True
        
        if 'katowice-hurghada' in hotel and 'instruktor' in hotel:
            return True
        
        # "przelot w 1 strone" itp.
        if 'przelot' in hotel or 'przelot' in destination:
            return True
            
        # Wzorce przelotów w tekście (sprawdzamy RAW przed normalizacją)
        if raw_hotel or raw_destination:
            if (self.normalizer.detect_flight_patterns(raw_hotel) or 
                self.normalizer.detect_flight_patterns(raw_destination)):
                return True
        
        # Fallback na znormalizowany tekst
        if (self.normalizer.detect_flight_patterns(hotel) or 
            self.normalizer.detect_flight_patterns(destination)):
            return True
        
        # Wzorce typu WAW-HRG, WAW_HRG
        if 'waw' in hotel and 'hrg' in hotel:
            return True
        if 'kat' in hotel and 'hrg' in hotel:
            return True
        
        # Wzorce miasto-miasto (literówki, warianty)
        city_patterns = [
            'katowice.*hurgh',  # łapie hurghada, hurghadsa, hurghda
            'warszawa.*hurgh',
            'gdansk.*hurgh',
            'wro.*hurgh',       # wroclaw
            'krakow.*hurgh',
            'poznan.*hurgh',
            'hurgh.*katowice',  # powroty
            'hurgh.*warszawa',
            'hurgh.*gdansk',
            'hurgh.*wro',
            'hurgh.*krakow',
            'hurgh.*poznan',
            'marsa.*alam.*wro', # Marsa Alam-Wrocław
            'marsa.*alam.*warszawa',
            'marsa.*alam.*katowice',
        ]
        
        for pattern in city_patterns:
            if re.search(pattern, hotel) or re.search(pattern, destination):
                return True
        
        return False
    
    def categorize(self, record: TravelRecord) -> str:
        """Kategoryzuje jako przelot"""
        return 'Sam przelot'