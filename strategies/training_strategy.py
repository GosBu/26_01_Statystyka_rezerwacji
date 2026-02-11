#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
TRAINING STRATEGY
================
Strategia kategoryzacji szkoleń - najwyższy priorytet.
"""

from strategies.base_strategy import CategoryStrategy
from models import TravelRecord
import json
from pathlib import Path

class TrainingStrategy(CategoryStrategy):
    """Strategia kategoryzacji szkoleń"""
    
    @property
    def priority(self) -> int:
        return 1  # Najwyższy priorytet
    
    def can_handle(self, record: TravelRecord) -> bool:
        """Sprawdza czy to szkolenie"""
        hotel, destination, raw_hotel, raw_destination = self.get_normalized_values(record)
        
        # Jeśli hotel został znormalizowany do "szkolenie" - to jest szkolenie!
        if hotel == 'szkolenie':
            return True
            
        # Nie kategoryzuj egzotyki jako szkolenia
        exotic_hotels = ['kitesurfing lanka', 'surfing lanka', 'sunsol punta blanca', 'sea view room']
        if any(eh in hotel for eh in exotic_hotels):
            return False
        
        # Wykluczenia - Brazil Kite Safari to Brazylia, nie szkolenie!
        if 'brazil kite safari' in hotel:
            return False
        
        # Fallback dla przypadków które nie zostały znormalizowane
        training_keywords = [
            'szkolenie', 'szkolenia', 'progress camp', 'pro camp', 'lekcje', 'instruktor', 
            'pakiet', 'duży pakiet', 'rescue pack', 'resuce pack',
            'kurs', 'indywidualne', 'indyw', 'ind.', 'ind ', 'ind x',
            'refresher', 'refr.', 'grupowo', 'promo', 'refresh',
            'yalla kite', 'godzinn', ' h ind', ' h kitesurfing',
            'windsurfing', 'opcja standard', 'euro os',
            'wypozyczenie sprzetu na kitesafari', 'wypozyczenie latawca',
            'wypsprz', 'wyp sprz', 'refresh wyp', 'refresh+wyp',
            'procamp', 'wypozyczenie sprzetu premium',
            'wypoz sprzetu standard', 'wypozyczenie sprzetu standard'
        ]
        return any(keyword in hotel for keyword in training_keywords)
    
    def categorize(self, record: TravelRecord) -> str:
        """Kategoryzuje jako szkolenie"""
        return 'Szkolenia'