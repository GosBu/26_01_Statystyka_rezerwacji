#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""System Configuration

Central configuration management for the travel analytics system.
"""

import os
from pathlib import Path
from typing import List, Dict

class Config:
    """Centralna konfiguracja systemu"""
    
    # Ścieżki
    BASE_DIR = Path(__file__).parent  # liczenie_rok
    DATA_DIR = BASE_DIR / "Dane" / "przetworzone"  # Dane wyczyszczone i znormalizowane
    RESULTS_DIR = BASE_DIR / "Wyniki"
    
    # Pliki źródłowe - dane przetworzone (wyczyszczone i znormalizowane)
    SOURCE_FILES: Dict[int, str] = {
        2019: "rok_2019_processed.xls",
        2020: "rok_2020_processed.xls", 
        2021: "rok_2021_processed.xls",
        2022: "rok_2022_processed.xls",
        2023: "rok_2023_processed.xls",
        2024: "rok_2024_processed.xls",
        2025: "rok_2025_processed.xls"
    }
    
    # Kolumny wymagane
    REQUIRED_COLUMNS: List[str] = [
        'Lp.', 'Nr rez.', 'Klient ID', 'Data utworzenia', 'Kierunek', 'Hotel'
    ]
    
    # Arkusze wyjściowe
    OUTPUT_SHEETS: Dict[str, str] = {
        'monthly': 'Statystyki_Miesięczne',
        'yearly': 'Statystyki_Roczne', 
        'training': 'Szkolenia_Sprzęt',
        'unassigned': 'Nieprzypisane',
        'all_data': 'Wszystkie_Dane',
        'normalized': 'Znormalizowane_Dane',
        'stats_table': 'stat_COMBINED'
    }
    
    # Kategorie z nagłówków użytkownika (dla tabeli miesiąc × kategorie)
    USER_CATEGORIES: List[str] = [
        'Razem',
        'Egipt - El Gouna',
        'Egipt - Hamata',
        'Egipt - inne',
        'Kitesafari',
        'Sal',
        'Turcja',
        'Grecja - Rodos',
        'Grecja - Limnos',
        'Grecja - Inne',
        'Fuerteventura',
        'Brazylia',
        'Mauritius',
        'Egzotyka - inne',
        'Ubezpieczenie',
        'Sam przelot',
        'Nieprzypisane'
    ]
    
    # Kategorie główne (w kolejności dla sortowania)
    MAIN_CATEGORIES = [
        'Brazylia', 'Chorwacja', 'Egipt - El Gouna', 'Egipt - Hamata',
        'Egipt - inne', 'Egzotyka - inne', 'Fuerteventura', 'Grecja - Inne',
        'Grecja - Limnos', 'Grecja - Rodos', 'Kitesafari', 'Maroko',
        'Mauritius', 'Narty', 'Rezygnacje', 'Sal', 'Sam przelot',
        'Tunezja', 'Turcja', 'Ubezpieczenie', 'Voucher'
    ]
    
    # Kategorie szkoleń/sprzętu
    TRAINING_CATEGORIES = ['Szkolenia', 'Sprzęt']
    
    # Miesiące polskie
    POLISH_MONTHS = [
        'Styczeń', 'Luty', 'Marzec', 'Kwiecień', 'Maj', 'Czerwiec',
        'Lipiec', 'Sierpień', 'Wrzesień', 'Październik', 'Listopad', 'Grudzień'
    ]
    
    @classmethod
    def ensure_directories(cls) -> None:
        """Tworzy katalogi jeśli nie istnieją"""
        cls.RESULTS_DIR.mkdir(exist_ok=True)
        
    @classmethod
    def get_source_file_path(cls, year: int) -> Path:
        """Zwraca pełną ścieżkę do pliku źródłowego"""
        filename = cls.SOURCE_FILES.get(year)
        if not filename:
            raise ValueError(f"Brak konfiguracji dla roku {year}")
        return cls.DATA_DIR / filename
        
    @classmethod
    def get_output_file_path(cls, filename: str) -> Path:
        """Zwraca pełną ścieżkę do pliku wynikowego"""
        return cls.RESULTS_DIR / filename