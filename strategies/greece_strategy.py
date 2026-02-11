#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
GREECE STRATEGY
==============
Strategia kategoryzacji hoteli greckich.
"""

import json
from pathlib import Path
from typing import Optional
from strategies.base_strategy import CategoryStrategy
from models import TravelRecord

class GreeceStrategy(CategoryStrategy):
    """Strategia kategoryzacji hoteli greckich"""
    
    def __init__(self, normalizer: Optional[object] = None) -> None:
        super().__init__(normalizer)
        self.load_hotel_categories()
    
    @property
    def priority(self) -> int:
        return 11
    
    def load_hotel_categories(self) -> None:
        """Wczytuje kategorie hoteli greckich z JSON"""
        config_path = Path(__file__).parent.parent / "config" / "hotel_categories.json"
        try:
            with open(config_path, 'r', encoding='utf-8') as f:
                categories = json.load(f)
                
            self.greece_limnos_hotels = set(categories.get("greece_limnos_hotels", []))
            self.greece_rodos_hotels = set(categories.get("greece_rodos_hotels", []))
            self.greece_other_hotels = set(categories.get("greece_other_hotels", []))
            
        except Exception as e:
            print(f"Błąd wczytywania hotel_categories.json dla Grecji: {e}")
            self.greece_limnos_hotels = set()
            self.greece_rodos_hotels = set()
            self.greece_other_hotels = set()
    
    def can_handle(self, record: TravelRecord) -> bool:
        """Sprawdza czy to hotel grecki"""
        hotel, destination, raw_hotel, raw_destination = self.get_normalized_values(record)
        
        # Wszystkie warianty kierunków greckich
        greece_destinations = [
            'lxs', 'rho', 'kos', 'zth',  # kody
            'grecja, limnos', 'grecja, rodos', 'grecja rodos', 'grecja korfu', 'grecja kos', 'grecja zakynthos',
            'limnos', 'rodos', 'korfu', 'kos', 'zakynthos', 'grecja'
        ]
        
        if destination in greece_destinations or 'grecja' in destination or destination in ['limnos', 'lemnos']:
            return True
        
        # Sprawdź też hotele greckie niezależnie od kierunku
        if (any(h in hotel for h in self.greece_limnos_hotels) or
            any(h in hotel for h in self.greece_rodos_hotels) or
            any(h in hotel for h in self.greece_other_hotels)):
            return True
        
        return False
    
    def categorize(self, record: TravelRecord) -> str:
        """Kategoryzuje hotele greckie"""
        hotel, destination, raw_hotel, raw_destination = self.get_normalized_values(record)
        
        # Limnos - rozszerzone sprawdzenie
        if (destination in ['lxs', 'grecja, limnos', 'limnos', 'lemnos'] or 
            'limnos' in destination or 'lemnos' in destination or
            any(h in hotel for h in self.greece_limnos_hotels)):
            return 'Grecja - Limnos'
        # Rodos
        elif destination in ['rho', 'grecja, rodos', 'grecja rodos', 'rodos'] or any(h in hotel for h in self.greece_rodos_hotels):
            return 'Grecja - Rodos'
        # Inne wyspy greckie
        elif destination in ['kos', 'zakynthos', 'zth', 'korfu', 'grecja kos', 'grecja zakynthos'] or any(h in hotel for h in self.greece_other_hotels):
            return 'Grecja - Inne'
        # Ocean Palace i inne nieznane hotele greckie
        elif 'ocean palace' in hotel or 'summer breeze' in hotel:
            return 'Grecja - Rodos'  # Domyślnie Rodos dla nieznanych hoteli greckich
        else:
            return 'Grecja - Inne'