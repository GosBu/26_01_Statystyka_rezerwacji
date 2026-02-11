#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Data Loading Module

Handles loading and parsing travel data from Excel/HTML files.
"""

import pandas as pd
from pathlib import Path
from typing import List, Dict, Set, Optional, Any
from models import TravelRecord
from config import Config

class DataLoader:
    """Klasa odpowiedzialna za wczytywanie danych"""
    
    def __init__(self) -> None:
        self.config = Config()
    
    def load_year_data(self, year: int) -> List[TravelRecord]:
        """Wczytuje dane z pojedynczego roku"""
        file_path = self.config.get_source_file_path(year)
        
        if not file_path.exists():
            raise FileNotFoundError(f"Brak pliku: {file_path}")
            
        print(f"  📄 Przetwarzam {file_path.name} (rok {year})")
        
        try:
            # Wczytaj HTML jako tabelę (pliki są w formacie HTML, nie Excel)
            df_list = pd.read_html(str(file_path), encoding='utf-8')
            df = df_list[0]
            
            # Jeśli kolumny to liczby, pierwszy wiersz to nazwy
            if df.columns.tolist() == list(range(len(df.columns))):
                df.columns = df.iloc[0] 
                df = df.drop(df.index[0]).reset_index(drop=True)
            
            # Inteligentne mapowanie kolumn (jak w oryginalnym kodzie)
            column_mapping = self._map_columns(df.columns)
            if not column_mapping:
                print(f"    Nie znaleziono żadnych kolumn w roku {year}")
                return []
            
            # Wyciągnij dane
            available_cols = [col for col in column_mapping.values() if col in df.columns]
            if not available_cols:
                print(f"    Brak dostępnych kolumn w roku {year}")
                return []
                
            extracted_data = df[available_cols].copy()
            # Zmapuj nazwy kolumn
            reverse_mapping = {v: k for k, v in column_mapping.items() if v in available_cols}
            extracted_data.columns = [reverse_mapping.get(col, col) for col in extracted_data.columns]
            
            # Dodaj rok i oczyść dane
            extracted_data['Rok'] = year
            extracted_data = extracted_data.dropna(how='all')
            
            # Usuń wiersze nagłówków
            mask = extracted_data.get('Hotel', pd.Series()).astype(str).str.contains(
                'nr rez|hotel|kierunek|klient', case=False, na=False
            )
            if mask.any():
                extracted_data = extracted_data[~mask]
            
            # Konwertuj na TravelRecord
            records = []
            for _, row in extracted_data.iterrows():
                try:
                    # Mapuj kolumny na TravelRecord - tylko 6 wymaganych kolumn
                    record_data = {
                        'Lp.': row.get('Lp.'),
                        'Nr rez.': row.get('Nr rez.', ''),
                        'Klient ID': row.get('Klient ID', ''),
                        'Data utworzenia': row.get('Data utworzenia'),
                        'Kierunek': row.get('Kierunek', ''),
                        'Hotel': row.get('Hotel', '')
                    }
                    
                    record = TravelRecord.from_series(pd.Series(record_data))
                    record.year = year  # Force year z nazwy pliku
                    records.append(record)
                except Exception as e:
                    print(f"Błąd w rekordzie roku {year}: {e}")
                    continue
            
            print(f"    Wyciągnięto {len(records)} rekordów")
            return records
            
        except Exception as e:
            print(f"Błąd wczytywania roku {year}: {e}")
            return []
    
    def load_all_data(self) -> List[TravelRecord]:
        """Wczytuje dane ze wszystkich lat"""
        print("📁 Wczytywanie danych z 6 plików...")
        
        all_records = []
        for year in sorted(self.config.SOURCE_FILES.keys()):
            year_records = self.load_year_data(year)
            all_records.extend(year_records)
        
        print(f"Łącznie wczytano {len(all_records)} rekordów z {len(self.config.SOURCE_FILES)} lat")
        return all_records
    
    def load_single_year(self, year: int) -> List[TravelRecord]:
        """Wczytuje dane z pojedynczego roku"""
        print(f"📁 Wczytywanie danych tylko z roku {year}...")
        
        if year not in self.config.SOURCE_FILES:
            print(f"Rok {year} nie jest zdefiniowany w konfiguracji")
            print(f"Dostępne lata: {sorted(self.config.SOURCE_FILES.keys())}")
            return []
        
        records = self.load_year_data(year)
        print(f"Wczytano {len(records)} rekordów z roku {year}")
        return records
    
    def load_selected_years(self, years: List[int]) -> List[TravelRecord]:
        """Wczytuje dane z wybranych lat"""
        print(f"📁 Wczytywanie danych z lat: {', '.join(map(str, years))}...")
        
        all_records = []
        for year in sorted(years):
            if year not in self.config.SOURCE_FILES:
                print(f"Rok {year} nie jest zdefiniowany w konfiguracji - pomijam")
                continue
            
            year_records = self.load_year_data(year)
            all_records.extend(year_records)
        
        print(f"Łącznie wczytano {len(all_records)} rekordów z {len([y for y in years if y in self.config.SOURCE_FILES])} lat")
        return all_records
    
    def get_records_by_year(self, records: List[TravelRecord]) -> Dict[int, List[TravelRecord]]:
        """Grupuje rekordy po latach"""
        by_year: Dict[int, List[TravelRecord]] = {}
        for record in records:
            year = record.year
            if year not in by_year:
                by_year[year] = []
            by_year[year].append(record)
        return by_year
    
    def validate_data_integrity(self, records: List[TravelRecord], expected_years: Optional[Set[int]] = None) -> bool:
        """Sprawdza integralność danych"""
        issues: List[str] = []
        
        # Sprawdź czy są rekordy
        if not records:
            issues.append("Brak rekordów do przetworzenia")
        
        # Sprawdź lata tylko jeśli podano oczekiwane lata
        if expected_years is not None:
            years = {r.year for r in records}
            missing_years = expected_years - years
            if missing_years:
                issues.append(f"Brakujące lata: {missing_years}")
        
        # Sprawdź lata - dla pełnej analizy
        elif expected_years is None:
            years = {r.year for r in records}
            all_expected_years = set(self.config.SOURCE_FILES.keys())
            missing_years = all_expected_years - years
            if missing_years:
                issues.append(f"Brakujące lata: {missing_years}")
        if missing_years:
            issues.append(f"Brakujące lata: {missing_years}")
        
        # Sprawdź puste pola kluczowe
        empty_hotels = sum(1 for r in records if not r.hotel or r.hotel.lower() in ['', 'nan', 'brak'])
        empty_destinations = sum(1 for r in records if not r.destination or r.destination.lower() in ['', 'nan', 'brak'])
        
        if empty_hotels > len(records) * 0.1:  # Więcej niż 10%
            issues.append(f"Zbyt wiele pustych hoteli: {empty_hotels}/{len(records)}")
        
        if empty_destinations > len(records) * 0.1:
            issues.append(f"Zbyt wiele pustych kierunków: {empty_destinations}/{len(records)}")
        
        # Raportuj problemy
        if issues:
            print("PROBLEMY Z DANYMI:")
            for issue in issues:
                print(f"   - {issue}")
            return False
        
        print("Walidacja danych: OK")
        return True
    
    def _map_columns(self, columns: Any) -> Dict[str, str]:
        """Mapuje kolumny z plików na standardowe nazwy - tylko 6 wymaganych kolumn"""
        column_mapping = {}
        required_columns = ["Lp.", "Nr rez.", "Klient ID", "Data utworzenia", "Kierunek", "Hotel"]
        
        for required_col in required_columns:
            found_col = None
            for col in columns:
                col_str = str(col).lower().strip()
                req_str = required_col.lower().replace('.', '').strip()
                
                if req_str in col_str or col_str in req_str:
                    found_col = col
                    break
                # Specjalne przypadki
                if required_col == "Lp." and any(x in col_str for x in ['lp', 'l.p', 'linia']):
                    found_col = col
                    break
                if required_col == "Klient ID" and any(x in col_str for x in ['klient', 'client', 'id']):
                    found_col = col
                    break
                if required_col == "Data utworzenia" and any(x in col_str for x in ['data utworzenia', 'data utw']):
                    found_col = col
                    break
            
            if found_col is not None:
                column_mapping[required_col] = found_col
        
        return column_mapping