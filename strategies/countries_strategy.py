#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
COUNTRIES STRATEGY
=================
Strategia kategoryzacji krajów.
"""

import json
from pathlib import Path
from typing import Optional
from strategies.base_strategy import CategoryStrategy
from models import TravelRecord

class CountriesStrategy(CategoryStrategy):
    """Strategia kategoryzacji różnych krajów"""
    
    def __init__(self, normalizer: Optional[object] = None) -> None:
        super().__init__(normalizer)
        self.load_hotel_categories()
    
    @property
    def priority(self) -> int:
        return 12
    
    def load_hotel_categories(self) -> None:
        """Wczytuje kategorie hoteli z JSON"""
        config_path = Path(__file__).parent.parent / "config" / "hotel_categories.json"
        try:
            with open(config_path, 'r', encoding='utf-8') as f:
                categories = json.load(f)
                
            self.turkey_hotels = set(categories.get("turkey_hotels", []))
            self.sal_hotels = set(categories.get("sal_hotels", []))
            self.fuerteventura_hotels = set(categories.get("fuerteventura_hotels", []))
            
        except Exception as e:
            print(f"Błąd wczytywania hotel_categories.json dla krajów: {e}")
            self.turkey_hotels = set()
            self.sal_hotels = set()
            self.fuerteventura_hotels = set()
    
    def can_handle(self, record: TravelRecord) -> bool:
        """Sprawdza czy to jeden ze wspieranych krajów"""
        hotel, destination, raw_hotel, raw_destination = self.get_normalized_values(record)
        
        # Maroko
        if 'maroko' in destination or destination == 'aga':
            return True
        
        # Tunezja → Nieprzypisane
        if 'tunezja' in destination or destination in ['tun', 'dba']:
            return True
        
        # Chorwacja
        if destination == 'chorwacja':
            return True
        
        # Turcja
        if destination == 'turcja' or any(h in hotel for h in self.turkey_hotels):
            return True
        
        # Mauritius
        if (destination == 'mauritius' or destination == 'mru' or 
            'mauritius' in destination or 'riu creole' in hotel or
            'hotle riu creole' in hotel):
            return True
        
        # Sal i Fuerteventura
        if destination == 'sal' or any(h in hotel for h in self.sal_hotels):
            return True
        if destination == 'fuerteventura' or any(h in hotel for h in self.fuerteventura_hotels):
            return True
        
        # Brazylia
        if (destination in ['for', 'ssa'] or 
            'brazylia' in destination or 
            'fortaleza' in destination or
            'barra grande' in hotel or
            'jericoacoara' in hotel or
            'brazil kite safari' in hotel):
            return True
        
        return False
    
    def categorize(self, record: TravelRecord) -> str:
        """Kategoryzuje kraje"""
        hotel, destination, raw_hotel, raw_destination = self.get_normalized_values(record)
        
        # Maroko
        if 'maroko' in destination or destination == 'aga':
            return 'Maroko'
        
        # Tunezja → Nieprzypisane
        if 'tunezja' in destination or destination in ['tun', 'dba']:
            return 'Nieprzypisane'
        
        # Chorwacja
        if destination == 'chorwacja':
            return 'Chorwacja'
        
        # Turcja
        if destination == 'turcja' or any(h in hotel for h in self.turkey_hotels):
            return 'Turcja'
        
        # Mauritius
        if (destination == 'mauritius' or destination == 'mru' or 
            'mauritius' in destination or 'riu creole' in hotel or
            'hotle riu creole' in hotel):
            return 'Mauritius'
        
        # Sal i Fuerteventura
        if destination == 'sal' or any(h in hotel for h in self.sal_hotels):
            return 'Sal'
        if destination == 'fuerteventura' or any(h in hotel for h in self.fuerteventura_hotels):
            return 'Fuerteventura'
        
        # Brazylia
        if (destination in ['for', 'ssa'] or 
            'brazylia' in destination or 
            'fortaleza' in destination or
            'barra grande' in hotel or
            'jericoacoara' in hotel or
            'brazil kite safari' in hotel):
            return 'Brazylia'
        
        return 'Nieprzypisane'