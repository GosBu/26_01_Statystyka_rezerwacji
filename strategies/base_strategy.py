#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
STRATEGY BASE CLASS
==================
Bazowa klasa dla wszystkich strategii kategoryzacji.
"""

from abc import ABC, abstractmethod
from typing import Optional, Tuple
from models import TravelRecord

class CategoryStrategy(ABC):
    """Bazowa klasa abstrakcyjna dla strategii kategoryzacji"""
    
    def __init__(self, normalizer: Optional[object] = None) -> None:
        self.normalizer = normalizer
    
    @abstractmethod
    def can_handle(self, record: TravelRecord) -> bool:
        """Sprawdza czy strategia może obsłużyć ten rekord"""
        pass
    
    @abstractmethod
    def categorize(self, record: TravelRecord) -> str:
        """Kategoryzuje rekord - zwraca nazwę kategorii"""
        pass
    
    @property
    @abstractmethod
    def priority(self) -> int:
        """Priorytet strategii - niższe wartości = wyższy priorytet"""
        pass
    
    def get_normalized_values(self, record: TravelRecord) -> Tuple[str, str, str, str]:
        """Helper do pobierania znormalizowanych wartości"""
        hotel = record.hotel_normalized or ''
        destination = record.destination_normalized or ''
        raw_hotel = record.hotel.lower() if record.hotel else ''
        raw_destination = record.destination.lower() if record.destination else ''
        
        return hotel, destination, raw_hotel, raw_destination