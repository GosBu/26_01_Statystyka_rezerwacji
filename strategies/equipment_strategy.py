#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
EQUIPMENT STRATEGY
=================
Strategia kategoryzacji sprzętu.
"""

from strategies.base_strategy import CategoryStrategy
from models import TravelRecord

class EquipmentStrategy(CategoryStrategy):
    """Strategia kategoryzacji sprzętu"""
    
    @property
    def priority(self) -> int:
        return 2
    
    def can_handle(self, record: TravelRecord) -> bool:
        """Sprawdza czy to sprzęt"""
        hotel, destination, raw_hotel, raw_destination = self.get_normalized_values(record)
        
        # Wypożyczenie sprzetu premium to szkolenie, nie sprzęt!
        if 'wypozyczenie sprzetu premium' in hotel:
            return False
        # Wypożyczenie sprzetu standard to też szkolenie, nie sprzęt!
        if 'wypoz sprzetu standard' in hotel:
            return False
        # Pełna fraza wypożyczenia sprzętu standard to też szkolenie!
        if 'wypozyczenie sprzetu standard' in hotel:
            return False
            
        equipment_keywords = [
            'sprzęt', 'sprzet', 'wynajem', 'latawce', 
            'equipment', 'zestaw kite', 'deska', 'trapez',
            'wypoz latawca', 'wypozczenie latawca'
        ]
        return any(keyword in hotel for keyword in equipment_keywords)
    
    def categorize(self, record: TravelRecord) -> str:
        """Kategoryzuje jako sprzęt"""
        return 'Sprzęt'