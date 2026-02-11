#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
CATEGORY MANAGER
===============
Manager wszystkich strategii kategoryzacji - Chain of Responsibility pattern.
"""

from typing import List
from models import TravelRecord
from strategies.base_strategy import CategoryStrategy
from strategies.training_strategy import TrainingStrategy
from strategies.equipment_strategy import EquipmentStrategy
from strategies.policy_strategy import PolicyStrategy
from strategies.flight_strategy import FlightStrategy
from strategies.kitesafari_strategy import KitesafariStrategy
from strategies.egypt_strategy import EgyptStrategy
from strategies.greece_strategy import GreeceStrategy
from strategies.countries_strategy import CountriesStrategy
from strategies.exotic_strategy import ExoticStrategy

class CategoryManager:
    """Manager strategii kategoryzacji - orchestrator wzorców"""
    
    def __init__(self, normalizer: object) -> None:
        self.normalizer = normalizer
        self.strategies = self._create_strategies()
    
    def _create_strategies(self) -> List[CategoryStrategy]:
        """Factory method - tworzy wszystkie strategie w odpowiedniej kolejności"""
        strategies = [
            TrainingStrategy(self.normalizer),       # Priority 1
            EquipmentStrategy(self.normalizer),      # Priority 2
            PolicyStrategy(self.normalizer),         # Priority 3
            FlightStrategy(self.normalizer),         # Priority 4
            KitesafariStrategy(self.normalizer),     # Priority 9
            EgyptStrategy(self.normalizer),          # Priority 10
            GreeceStrategy(self.normalizer),         # Priority 11
            CountriesStrategy(self.normalizer),      # Priority 12
            ExoticStrategy(self.normalizer),         # Priority 13
        ]
        
        # Sortuj według priorytetu (niższe = wyższy priorytet)
        return sorted(strategies, key=lambda s: s.priority)
    
    def categorize_record(self, record: TravelRecord) -> str:
        """Główna metoda kategoryzacji używająca Chain of Responsibility"""
        
        # Specjalne przypadki na początku (jak w oryginalnym kodzie)
        hotel = record.hotel_normalized or ''
        destination = record.destination_normalized or ''
        
        # Specjalny przypadek: hotel nan + kierunek Hurghada = Nieprzypisane
        if hotel in ['N/A', 'nan'] and destination in ['hrg', 'hurghada', 'egipt, hurghada']:
            return 'Nieprzypisane'
        
        # Specjalny przypadek: hotel nan + dowolny kierunek = Nieprzypisane 
        if hotel in ['N/A', 'nan'] and destination not in ['kitesafari', 'polisa']:
            return 'Nieprzypisane'
        
        # Próbuj każdą strategię w kolejności priorytetu
        for strategy in self.strategies:
            if strategy.can_handle(record):
                return strategy.categorize(record)
        
        # Jeśli żadna strategia nie obsłużyła - fallback na specjalne przypadki
        return self._handle_fallback(record)
    
    def _handle_fallback(self, record: TravelRecord) -> str:
        """Obsługuje przypadki których nie obsłużyła żadna strategia"""
        hotel = record.hotel_normalized or ''
        destination = record.destination_normalized or ''
        
        # Rezygnacje i skrócenia wyjazdu → Nieprzypisane
        if ('rezygnacja' in hotel or 'rezygnacja' in destination or
            'skrocenie' in hotel or 'skrocenie' in destination or
            'skrócenie' in hotel or 'skrócenie' in destination):
            return 'Nieprzypisane'
        
        # Narty
        if 'narty' in hotel or destination == 'austria':
            return 'Narty'
        
        # Vouchery (ale nie szkolenie)
        voucher_keywords = ['voucher', 'vocher', 'prezentowy', 'bezterminowy']
        if any(keyword in hotel for keyword in voucher_keywords):
            # Wykluczenia - to NIE są vouchery
            training_keywords = ['kurs', 'szkolenie', 'lekcj', 'godzinn', 'ind', 'premium', 'standard']
            if not any(keyword in hotel for keyword in training_keywords):
                return 'Voucher'
        
        # Specjalne przypadki nieprzypisanych
        if 'apartament' in hotel or hotel in ['test', 'N/A'] or hotel == '':
            return 'Nieprzypisane'
        
        # Ubezpieczenia (ogólne) - wszystkie formy słowa polisa
        insurance_keywords = [
            'polisa', 'polisy', 'polisę', 'polisą', 'polisie', 'polis',
            'ubezp', 'ubezpieczenie', 'ubezpieczenia', 'sporty wyczynowo', 'filipiny', 
            'wietnam', 'tajlandia', '3 polisy', 'ubkr'
        ]
        if any(keyword in hotel for keyword in insurance_keywords):
            return 'Ubezpieczenie'
        if any(keyword in destination for keyword in insurance_keywords):
            return 'Ubezpieczenie'
        
        # Brak pola touroperator w miniaturze strukturze - pomijamy sprawdzenie firm ubezpieczeniowych
        
        # Nieprzypisane kierunki
        if destination in {'nieznany', 'voucher', 'kurs', 'wynajem sprzętu'}:
            return 'Nieprzypisane'
        
        # Sprawdź puste hotele z niepustymi kierunkami (na końcu!)
        empty_values = ['', 'nan', 'none', 'brak']
        hotel_empty = hotel.lower() in empty_values
        destination_not_empty = destination and destination.lower() not in empty_values
        if hotel_empty and destination_not_empty:
            return 'Nieprzypisane'
        
        return 'Nieprzypisane'