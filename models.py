#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Travel Data Models

Classes representing the system's data structures for travel booking analysis.
"""

from dataclasses import dataclass, field
from datetime import datetime
from typing import Optional, Dict, List
import pandas as pd
import re

def parse_polish_number(value) -> Optional[float]:
    """Parsuje polskie formatowanie liczb (spacja jako separator tysięcy, przecinek dziesiętny)"""
    if pd.isna(value) or value == "" or value is None:
        return None
    
    try:
        # Jeśli to już jest liczba
        if isinstance(value, (int, float)):
            return float(value)
        
        # Konwersja na string i czyszczenie
        str_value = str(value).strip()
        if not str_value:
            return None
            
        # Usuń spacje (separatory tysięcy) i zamień przecinek na kropkę
        cleaned = str_value.replace(' ', '').replace(',', '.')
        
        # Usuń znaki waluty jeśli są
        cleaned = re.sub(r'[^\d.-]', '', cleaned)
        
        if cleaned:
            return float(cleaned)
        return None
        
    except (ValueError, TypeError):
        return None

@dataclass
class TravelRecord:
    """Pojedynczy rekord podróży - uproszczony do 6 kolumn"""
    lp: Optional[int]  # linia porządkowa
    nr_rezerwacji: str  # numer rezerwacji
    klient_id: str  # ID klienta
    date_created: datetime  # data utworzenia
    destination: str  # kierunek
    hotel: str  # hotel 
    year: Optional[int] = None
    month: Optional[str] = None
    category: str = "Nieprzypisane"
    hotel_normalized: str = ""
    destination_normalized: str = ""
    
    def __post_init__(self) -> None:
        """Automatyczne wypełnienie derived fields"""
        if self.year is None and self.date_created:
            self.year = self.date_created.year
        if self.month is None and self.date_created:
            from config import Config
            month_idx = self.date_created.month - 1
            self.month = Config.POLISH_MONTHS[month_idx]
    
    @classmethod
    def from_series(cls, row: pd.Series) -> 'TravelRecord':
        """Tworzy rekord z pandas Series"""
        return cls(
            lp=int(row.get('Lp.', 0)) if pd.notna(row.get('Lp.')) else None,
            nr_rezerwacji=str(row.get('Nr rez.', '')),
            klient_id=str(row.get('Klient ID', '')),
            date_created=pd.to_datetime(row['Data utworzenia']),
            destination=str(row.get('Kierunek', '')),
            hotel=str(row.get('Hotel', ''))
        )
    
    def to_dict(self) -> Dict:
        """Konwertuje rekord do słownika dla DataFrame"""
        return {
            'Lp.': self.lp,
            'Nr rez.': self.nr_rezerwacji,
            'Klient ID': self.klient_id,
            'Data utworzenia': self.date_created,
            'Kierunek': self.destination,
            'Hotel': self.hotel,
            'Rok': self.year,
            'Miesiąc': self.month,
            'Kategoria': self.category
        }

@dataclass 
class ProcessingStats:
    """Statystyki przetwarzania"""
    total_records: int = 0
    assigned_records: int = 0
    unassigned_records: int = 0
    records_by_year: Dict[int, int] = field(default_factory=dict)
    records_by_category: Dict[str, int] = field(default_factory=dict)
    
    @property
    def accuracy_percentage(self) -> float:
        """Procent dokładności przypisania"""
        if self.total_records == 0:
            return 0.0
        return (self.assigned_records / self.total_records) * 100
    
    def update_category_stats(self, records: List[TravelRecord]) -> None:
        """Aktualizuje statystyki kategorii"""
        self.records_by_category.clear()
        for record in records:
            category = record.category
            self.records_by_category[category] = self.records_by_category.get(category, 0) + 1
            
        self.total_records = len(records)
        self.assigned_records = sum(
            count for category, count in self.records_by_category.items() 
            if category != 'Nieprzypisane'
        )
        self.unassigned_records = self.records_by_category.get('Nieprzypisane', 0)
    
    def print_summary(self) -> None:
        """Wyświetla podsumowanie statystyk"""
        print(f"Przetwarzanie zakończone:")
        print(f"   Łącznie rekordów: {self.total_records}")
        print(f"   Przypisanych: {self.assigned_records} ({self.accuracy_percentage:.1f}%)")
        print(f"   Nieprzypisanych: {self.unassigned_records} ({100-self.accuracy_percentage:.1f}%)")

@dataclass
class YearlyStats:
    """Statystyki roczne"""
    year: int
    total_records: int
    main_records: int
    training_records: int  
    unassigned_records: int
    monthly_distribution: Dict[str, int] = field(default_factory=dict)
    
    def print_summary(self) -> None:
        """Wyświetla podsumowanie roku"""
        print(f"  📅 {self.year}: Wyniki/travel_statistics_{self.year}.xlsx")
        print(f"      Główne: {self.main_records} | Szkolenia/Sprzęt: {self.training_records} | Nieprzypisane: {self.unassigned_records}")