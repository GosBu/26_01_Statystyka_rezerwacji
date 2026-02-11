#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
NORMALIZATOR DANYCH
==================
Klasa odpowiedzialna za normalizację hoteli i kierunków.
Używa plików JSON do konfiguracji reguł normalizacji.
"""

import json
import re
from pathlib import Path
from typing import Set, Dict, List, Any
from models import TravelRecord

class TravelNormalizer:
    """Klasa do normalizacji nazw hoteli i kierunków"""
    
    def __init__(self) -> None:
        self.config_dir = Path(__file__).parent / "config"
        self.patterns: Dict[str, Any] = {}  # Inicjalizacja patterns jako pusty dict
        self.hotel_rules: Dict[str, str] = {}
        self.destination_rules: Dict[str, str] = {}
        self.load_config_files()
    
    def load_config_files(self) -> None:
        """Wczytuje reguły normalizacji z plików JSON"""
        # Wczytanie reguł hoteli
        hotel_file = self.config_dir / "hotel_rules.json"
        if hotel_file.exists():
            with open(hotel_file, 'r', encoding='utf-8') as f:
                hotel_data = json.load(f)
            
            # Sprawdź czy to już płaski słownik (nowy format) czy zagnieżdżony (stary format)
            if isinstance(list(hotel_data.values())[0], str):
                # Nowy format - płaski słownik
                self.hotel_rules = hotel_data
            else:
                # Stary format - zagnieżdżony słownik
                self.hotel_rules = {}
                for category, rules in hotel_data.items():
                    self.hotel_rules.update(rules)
        else:
            print(f"Brak pliku: {hotel_file}")
            self.hotel_rules = {}
        
        # Wczytanie reguł kierunków
        dest_file = self.config_dir / "destination_rules.json" 
        if dest_file.exists():
            with open(dest_file, 'r', encoding='utf-8') as f:
                dest_data = json.load(f)
            
            # Sprawdź czy to już płaski słownik (nowy format) czy zagnieżdżony (stary format)
            first_value = list(dest_data.values())[0]
            if isinstance(first_value, str):
                # Nowy format - płaski słownik
                self.destination_rules = dest_data
            else:
                # Stary format - zagnieżdżony słownik
                self.destination_rules = {}
                for category, rules in dest_data.items():
                    if isinstance(rules, dict):
                        self.destination_rules.update(rules)
                    else:
                        # To może być pojedyncza reguła w starym formacie
                        self.destination_rules[category] = rules
        else:
            print(f"Brak pliku: {dest_file}")
            self.destination_rules = {}
            
        # Wczytanie wzorców
        patterns_file = self.config_dir / "patterns.json"
        if patterns_file.exists():
            with open(patterns_file, 'r', encoding='utf-8') as f:
                self.patterns = json.load(f)
        else:
            print(f"Brak pliku: {patterns_file}")
            self.patterns = {}
    
    def normalize_text(self, text: str) -> str:
        """Podstawowa normalizacja tekstu"""
        if not text or not isinstance(text, str):
            return ""
        
        # Usuń gwiazdki, cyfry i znaki specjalne
        text = re.sub(r'[*★☆\d(),.]', '', text)
        # Usuń nadmiarowe spacje
        text = re.sub(r'\s+', ' ', text)
        
        return (text.lower()
                    .strip()
                    .replace('ł', 'l')
                    .replace('ą', 'a')
                    .replace('ć', 'c') 
                    .replace('ę', 'e')
                    .replace('ń', 'n')
                    .replace('ó', 'o')
                    .replace('ś', 's')
                    .replace('ź', 'z')
                    .replace('ż', 'z')
                    .replace('-', ' ')
                    .replace('_', ' ')
                    .strip())
    
    def _normalize_with_rules(self, text: str, rules: Dict[str, str]) -> str:
        """Wspólna metoda normalizacji z regułami - eliminuje duplikację kodu"""
        if not text:
            return ''
        
        text_lower = text.lower().strip()
        
        # Najpierw sprawdź dokładne dopasowania z oryginalnymi nazwami
        if text_lower in rules:
            return rules[text_lower]
        
        # Potem sprawdź częściowe dopasowania z oryginalnymi nazwami
        for pattern, normalized in rules.items():
            if pattern in text_lower:
                return normalized
        
        # Na koniec normalizuj tekst standardowo
        return self.normalize_text(text)
    
    def normalize_hotel(self, hotel: str) -> str:
        """Normalizuje nazwę hotelu"""
        return self._normalize_with_rules(hotel, self.hotel_rules)
    
    def normalize_destination(self, destination: str) -> str:
        """Normalizuje kierunek"""
        return self._normalize_with_rules(destination, self.destination_rules)
    
    def detect_flight_patterns(self, text: str) -> bool:
        """Wykrywa wzorce przelotów w tekście"""
        text_lower = text.lower()
        
        # Sprawdzenie wzorców przelotów z pliku konfiguracyjnego
        for pattern in self.patterns.get('flight_patterns', []):
            if re.search(pattern, text_lower):
                return True
        
        # Sprawdzenie wzorców kitesafari
        for pattern in self.patterns.get('kitesafari_patterns', []):
            if re.search(pattern, text_lower):
                return True
        
        return False
    
    def has_transfer_patterns(self, text: str) -> bool:
        """Sprawdza czy tekst zawiera wzorce transferów"""
        text_lower = text.lower()
        
        for pattern in self.patterns.get('transfer_patterns', []):
            if pattern in text_lower:
                return True
        
        return False
    
    def normalize_all_records(self, records: List[TravelRecord]) -> List[TravelRecord]:
        """Normalizuje wszystkie rekordy"""
        print("  Normalizacja hoteli...")
        for record in records:
            record.hotel_normalized = self.normalize_hotel(record.hotel)
            
        print("  Normalizacja kierunków...")
        for record in records:
            record.destination_normalized = self.normalize_destination(record.destination)
        
        return records
    
    def process_record(self, record: TravelRecord) -> TravelRecord:
        """Przetwarza pojedynczy rekord - normalizuje hotel i kierunek"""
        record.hotel_normalized = self.normalize_hotel(record.hotel)
        record.destination_normalized = self.normalize_destination(record.destination)
        
        return record
    
    def get_all_hotels(self) -> Set[str]:
        """Zwraca wszystkie znormalizowane nazwy hoteli"""
        return set(self.hotel_rules.values())
    
    def get_all_destinations(self) -> Set[str]:
        """Zwraca wszystkie znormalizowane kierunki"""
        return set(self.destination_rules.values())
    
    def reload_config(self) -> None:
        """Przeładowuje konfigurację z plików JSON"""
        print("Przeładowuję konfigurację normalizacji...")
        self.load_config_files()
        print("Konfiguracja przeładowana")