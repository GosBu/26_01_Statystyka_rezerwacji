#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
KITESAFARI STRATEGY
==================
Strategia kategoryzacji kitesafari.
"""

from strategies.base_strategy import CategoryStrategy
from models import TravelRecord

class KitesafariStrategy(CategoryStrategy):
    """Strategia kategoryzacji kitesafari"""
    
    @property
    def priority(self) -> int:
        return 9  # Przed Egiptem i Grecją, ale po przelotach
    
    def can_handle(self, record: TravelRecord) -> bool:
        """Sprawdza czy to kitesafari"""
        hotel, destination, raw_hotel, raw_destination = self.get_normalized_values(record)
        
        # Wykluczenia - Brazil Kite Safari to Brazylia, nie kitesafari!
        if 'brazil' in hotel:
            return False
        
        # Sprawdź czy zawiera słowa kluczowe kitesafari
        if 'kite safari' in hotel or 'kitesafari' in hotel:
            return True
        
        # AML HAYATY to kitesafari
        if 'aml hayaty' in hotel:
            return True
        
        # Valerie to kitesafari (jacht motorowy lub M/Y)
        if 'valerie' in hotel:
            return True
        
        # Jacht motorowy to kitesafari
        if 'jacht motorowy' in hotel:
            return True
        
        # Ogólna reguła: jacht w polu hotel = Kitesafari
        if 'jacht' in hotel:
            return True
        
        return destination == 'kitesafari'
    
    def categorize(self, record: TravelRecord) -> str:
        """Kategoryzuje jako kitesafari"""
        return 'Kitesafari'