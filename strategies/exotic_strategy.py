#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
EXOTIC STRATEGY
==============
Strategia kategoryzacji egzotyki.
"""

import json
from pathlib import Path
from typing import Optional
from strategies.base_strategy import CategoryStrategy
from models import TravelRecord

class ExoticStrategy(CategoryStrategy):
    """Strategia kategoryzacji egzotyki"""
    
    def __init__(self, normalizer: Optional[object] = None) -> None:
        super().__init__(normalizer)
        self.load_exotic_destinations()
    
    @property
    def priority(self) -> int:
        return 13
    
    def load_exotic_destinations(self) -> None:
        """Wczytuje kierunki egzotyczne z JSON"""
        config_path = Path(__file__).parent.parent / "config" / "hotel_categories.json"
        try:
            with open(config_path, 'r', encoding='utf-8') as f:
                categories = json.load(f)
                
            self.exotic_destinations = set(categories.get("exotic_destinations", []))
            
        except Exception as e:
            print(f"Błąd wczytywania hotel_categories.json dla egzotyki: {e}")
            self.exotic_destinations = set()
    
    def can_handle(self, record: TravelRecord) -> bool:
        """Sprawdza czy to egzotyka"""
        hotel, destination, raw_hotel, raw_destination = self.get_normalized_values(record)
        
        # Sprawdź czy normalizacja zwraca 'egzotyka'
        if hotel == 'egzotyka' or destination == 'egzotyka':
            return True
        
        # Specjalny przypadek: RPA, Cape Town + Sea View Room = egzotyka
        if 'rpa' in destination and 'cape town' in destination and 'sea view room' in hotel:
            return True
        
        # Sprawdź kierunki egzotyczne
        if destination in self.exotic_destinations:
            if hotel not in ['polisa', 'przelot']:
                training_keywords = ['kurs', 'szkolenie', 'lekcj', 'promo', 'ind']
                return not any(keyword in hotel for keyword in training_keywords)
        
        return False
    
    def categorize(self, record: TravelRecord) -> str:
        """Kategoryzuje jako egzotyka"""
        return 'Egzotyka - inne'