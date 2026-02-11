#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
EGYPT STRATEGY
=============
Strategia kategoryzacji hoteli egipskich z wykorzystaniem JSON.
"""

import json
from pathlib import Path
from typing import Optional
from strategies.base_strategy import CategoryStrategy
from models import TravelRecord

class EgyptStrategy(CategoryStrategy):
    """Strategia kategoryzacji hoteli egipskich"""
    
    def __init__(self, normalizer: Optional[object] = None) -> None:
        super().__init__(normalizer)
        self.load_hotel_categories()
    
    @property
    def priority(self) -> int:
        return 10  # Średni priorytet
    
    def load_hotel_categories(self) -> None:
        """Wczytuje kategorie hoteli z JSON"""
        config_path = Path(__file__).parent.parent / "config" / "hotel_categories.json"
        try:
            with open(config_path, 'r', encoding='utf-8') as f:
                categories = json.load(f)
                
            self.el_gouna_hotels = set(categories.get("el_gouna_hotels", []))
            self.hamata_hotels = set(categories.get("hamata_hotels", []))
            self.egypt_other_hotels = set(categories.get("egypt_other_hotels", []))
            
        except Exception as e:
            print(f"Błąd wczytywania hotel_categories.json: {e}")
            # Fallback - puste zestawy
            self.el_gouna_hotels = set()
            self.hamata_hotels = set()
            self.egypt_other_hotels = set()
    
    def can_handle(self, record: TravelRecord) -> bool:
        """Sprawdza czy to hotel egipski"""
        hotel, destination, raw_hotel, raw_destination = self.get_normalized_values(record)
        
        # Wszystkie warianty kierunków egipskich
        egypt_destinations = [
            'hrg', 'rmf', 'ssh', 'soma bay',  # krótkie kody
            'egipt, hurghada', 'egipt marsa alam', 'egipt sharm el sheik', 'egipt soma bay',
            'egipt', 'hurghada', 'marsa alam', 'sharm el sheik'
        ]
        
        # Sprawdź hotele niezależnie od destination (dla przypadków z pustym destination)
        if 'soma bay' in hotel or 'palm royal' in hotel or 'sentido palm' in hotel:
            return True
        elif any(eg_hotel in hotel for eg_hotel in self.el_gouna_hotels):
            return True
        elif any(h_hotel in hotel for h_hotel in self.hamata_hotels):
            return True
        elif any(egypt_hotel in hotel for egypt_hotel in self.egypt_other_hotels):
            return True
        
        # Jeśli kierunek to Egipt
        if destination in egypt_destinations:
            return True
        
        return False
    
    def categorize(self, record: TravelRecord) -> str:
        """Kategoryzuje hotele egipskie"""
        hotel, destination, raw_hotel, raw_destination = self.get_normalized_values(record)
        
        egypt_destinations = [
            'hrg', 'rmf', 'ssh', 'soma bay',
            'egipt, hurghada', 'egipt marsa alam', 'egipt sharm el sheik', 'egipt soma bay',
            'egipt', 'hurghada', 'marsa alam', 'sharm el sheik'
        ]
        
        # Sprawdź hotele niezależnie od destination
        if 'soma bay' in hotel or 'palm royal' in hotel or 'sentido palm' in hotel:
            return 'Egipt - inne'
        elif any(eg_hotel in hotel for eg_hotel in self.el_gouna_hotels):
            return 'Egipt - El Gouna'
        elif any(h_hotel in hotel for h_hotel in self.hamata_hotels):
            return 'Egipt - Hamata'
        elif any(egypt_hotel in hotel for egypt_hotel in self.egypt_other_hotels):
            return 'Egipt - inne'
        
        # Jeśli kierunek to Egipt, ale hotel nie pasuje do żadnej kategorii
        if destination in egypt_destinations:
            return 'Nieprzypisane'  # Będzie nieprzypisane!
        
        return 'Nieprzypisane'