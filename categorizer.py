#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Travel Categorization System

Categorizes travel records using strategy pattern for business rule classification.
"""

from typing import List
from models import TravelRecord
from normalizer import TravelNormalizer
from strategies import CategoryManager

class TravelCategorizer:
    """Klasa do kategoryzacji rekordów podróży - refactored z Strategy Pattern"""
    
    def __init__(self) -> None:
        self.normalizer = TravelNormalizer()
        self.category_manager = CategoryManager(self.normalizer)
    
    def categorize_simple(self, hotel: str, destination: str) -> str:
        """Prosta metoda kategoryzacji dla testowania"""
        from models import TravelRecord
        import datetime
        
        # Stwórz tymczasowy rekord
        record = TravelRecord(
            lp=None,
            nr_rezerwacji='',
            klient_id='',
            hotel=hotel,
            destination=destination,
            date_created=datetime.date(2024, 1, 1),
            month='Styczeń'
        )
        
        return self.categorize_record(record)
    
    def categorize_record(self, record: TravelRecord) -> str:
        """Główna metoda kategoryzacji rekordu - używa CategoryManager"""
        # Normalizuj jeśli jeszcze nie znormalizowane
        if not record.hotel_normalized:
            record.hotel_normalized = self.normalizer.normalize_hotel(record.hotel)
        if not record.destination_normalized:
            record.destination_normalized = self.normalizer.normalize_destination(record.destination)
        
        # Deleguj kategoryzację do CategoryManager (Strategy Pattern)
        return self.category_manager.categorize_record(record)
    
    def categorize_all_records(self, records: List[TravelRecord]) -> List[TravelRecord]:
        """Kategoryzuje wszystkie rekordy"""
        print("  Kategoryzacja...")
        
        for record in records:
            # Najpierw znormalizuj hotel i kierunek
            if not record.hotel_normalized:
                record.hotel_normalized = self.normalizer.normalize_hotel(record.hotel)
            if not record.destination_normalized:
                record.destination_normalized = self.normalizer.normalize_destination(record.destination)
            
            # Teraz kategoryzuj
            record.category = self.categorize_record(record)
        
        return records