#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
POLICY STRATEGY
==============
Strategia kategoryzacji polis ubezpieczeniowych.
"""

from strategies.base_strategy import CategoryStrategy
from models import TravelRecord

class PolicyStrategy(CategoryStrategy):
    """Strategia kategoryzacji polis"""
    
    @property
    def priority(self) -> int:
        return 3
    
    def can_handle(self, record: TravelRecord) -> bool:
        """Sprawdza czy to polisa/ubezpieczenie"""
        hotel, destination, raw_hotel, raw_destination = self.get_normalized_values(record)
        
        # Jeśli hotel został znormalizowany do "polisa" - to jest polisa!
        if hotel == 'polisa':
            return True
        
        # Jeśli kierunek został znormalizowany do "polisa" (np. Ergo + nan) - to jest polisa!
        if destination == 'polisa':
            return True
        
        # Specjalny przypadek - Japonia z polisą
        if (destination and 'japonia' in destination and 
            hotel and 'polisa' in hotel):
            return True
            
        # "Ubezpieczenie do wyjazdu" to polisa, nie ogólne ubezpieczenie
        if hotel and 'ubezpieczenie do wyjazdu' in hotel:
            return True
        if hotel and 'polisa' in hotel and 'do wyjazdu' in hotel:
            return True
        # "dopłata do kontynuacji leczenia w RP" to polisa (znormalizowana: "doplata")
        if 'doplata do kontynuacji leczenia w rp' in hotel:
            return True
        # Ubezpieczenia KR do biletów lotniczych to polisy
        if hotel and 'ubkr' in hotel and 'bilet' in hotel:
            return True
        if hotel and 'ubezpieczenie' in hotel and 'kr' in hotel and 'bilet' in hotel:
            return True
        if hotel and 'ubezpieczenie kr' in hotel:
            return True
        
        # Wzorce polis z obsługą nan - wszystkie formy słowa polisa
        policy_patterns = [
            'polisa', 'polisy', 'polisę', 'polisą', 'polisie', 'polis',
            'ubezpieczenie', 'ubezpieczenia', 'ubezp', 'insurance', 'kr',
            'allianz', 'ergo', 'mondial', 'globtroter', 'globtrotter',
            'wiener', 'compensa'
        ]
        
        # Sprawdź w hotelu (obsługa nan)
        if hotel:
            for pattern in policy_patterns:
                if pattern in hotel:
                    return True
        
        # Brak pola touroperator w nowej strukturze - pomiń sprawdzenie
        
        return False
    
    def categorize(self, record: TravelRecord) -> str:
        """Kategoryzuje jako ubezpieczenie"""
        return 'Ubezpieczenie'