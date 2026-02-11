#!/usr/bin/env python3  
# -*- coding: utf-8 -*-
"""
GŁÓWNA KLASA ANALIZATORA
=======================
Orkiestruje cały proces analizy - fasada dla całego systemu.
"""

from datetime import datetime
from typing import List
from models import TravelRecord, ProcessingStats
from config import Config
from data_loader import DataLoader
from normalizer import TravelNormalizer
from categorizer import TravelCategorizer
from exporter import ExcelExporter

class TravelAnalyzer:
    """Główna klasa orkiestrująca analizę podróży"""
    
    def __init__(self) -> None:
        self.config = Config()
        self.data_loader = DataLoader()
        self.normalizer = TravelNormalizer()
        self.categorizer = TravelCategorizer()
        self.exporter = ExcelExporter()
        
        self.records: List[TravelRecord] = []
        self.stats = ProcessingStats()
        
    def run_analysis(self, single_year: int = None, selected_years: List[int] = None) -> None:
        """Główny przepływ analizy"""
        print("SYSTEM ANALIZY ROCZNEJ STATYSTYK PODRÓŻNYCH")
        print("=" * 70)
        
        if single_year:
            print(f"📅 Analiza tylko roku: {single_year}")
        elif selected_years:
            print(f"📅 Analiza wybranych lat: {', '.join(map(str, selected_years))}")
        else:
            print("📅 Analiza wszystkich dostępnych lat")
            
        print(f"⏰ Start: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        
        try:
            # Zapewnij katalogi
            self.config.ensure_directories()
            
            # 1. Wczytywanie danych
            if single_year:
                self.records = self.data_loader.load_single_year(single_year)
            elif selected_years:
                self.records = self.data_loader.load_selected_years(selected_years)
            else:
                self.records = self.data_loader.load_all_data()
            
            if not self.records:
                print("Nie znaleziono danych do analizy")
                return
            
            # 2. Walidacja danych
            expected_years = None
            if single_year:
                expected_years = {single_year}
            elif selected_years:
                expected_years = set(selected_years)
            
            if not self.data_loader.validate_data_integrity(self.records, expected_years):
                print("Błędy w danych - przerywanie analizy")
                return
            
            # 3. Przetwarzanie
            self._process_records()
            
            # 4. Generowanie statystyk  
            self._generate_statistics()
            
            # 5. Eksport wyników
            self._export_results()
            
            # 6. Enhanced Analytics
            try:
                print("\n🎨 Uruchamianie Enhanced Analytics...")
                from enhanced_analytics import EnhancedAnalytics
                analytics = EnhancedAnalytics("wyniki/travel_statistics_COMBINED.xlsx")
                analytics.generate_full_report()
            except ImportError:
                print("Enhanced Analytics niedostępne")
            except Exception as e:
                print(f"Błąd Enhanced Analytics: {e}")
            
            # 7. Podsumowanie
            self._print_summary()
            
        except Exception as e:
            print(f"Błąd krytyczny: {e}")
            raise
        
        print(f"⏰ Koniec: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    def _process_records(self) -> None:
        """Przetwarza rekordy: normalizacja + kategoryzacja"""
        print(f"\nPrzetwarzanie {len(self.records)} rekordów...")
        
        # Normalizacja
        self.records = self.normalizer.normalize_all_records(self.records)
        
        # Kategoryzacja
        self.records = self.categorizer.categorize_all_records(self.records)
    
    def _generate_statistics(self) -> None:
        """Generuje statystyki"""
        self.stats.update_category_stats(self.records)
        self.stats.print_summary()
    
    def _export_results(self) -> None:
        """Eksportuje wyniki"""
        print("\n💾 Zapisywanie wyników...")
        
        # Eksport zbiorczy
        combined_file = self.config.get_output_file_path("travel_statistics_COMBINED.xlsx")
        self.exporter.export_combined_file(self.records, combined_file, self.stats)
        
        # Eksport roczny  
        records_by_year = self.data_loader.get_records_by_year(self.records)
        yearly_stats = self.exporter.export_yearly_files(records_by_year, self.config)
        
        print("Zapisano zbiorczy plik: Wyniki/travel_statistics_COMBINED.xlsx")
        print("\n💾 Zapisywanie plików rocznych...")
        for stat in yearly_stats:
            stat.print_summary()
    
    def _print_summary(self) -> None:
        """Wyświetla podsumowanie"""
        print("Zapisano wszystkie pliki roczne")
        print("\nZAKOŃCZONO POMyŚLNIE!")
        print("📁 Wszystkie pliki zapisane w folderze: Wyniki/")
        print("   travel_statistics_COMBINED.xlsx - zbiorczy plik")
        for year in sorted(self.config.SOURCE_FILES.keys()):
            print(f"   📅 travel_statistics_{year}.xlsx - rok {year}")
    
    def get_records_by_category(self, category: str) -> List[TravelRecord]:
        """Zwraca rekordy dla konkretnej kategorii"""
        return [r for r in self.records if r.category == category]
    
    def get_unassigned_records(self) -> List[TravelRecord]:
        """Zwraca nieprzypisane rekordy"""
        return self.get_records_by_category('Nieprzypisane')
    
    def print_category_summary(self) -> None:
        """Wyświetla podsumowanie kategorii"""
        print("\nROZKŁAD KATEGORII:")
        sorted_categories = sorted(
            self.stats.records_by_category.items(),
            key=lambda x: x[1], 
            reverse=True
        )
        
        for i, (category, count) in enumerate(sorted_categories, 1):
            percentage = (count / self.stats.total_records) * 100
            print(f"  {i:2d}. {category:<20}: {count:4d} rekordów ({percentage:5.1f}%)")


# Punkt wejścia - dla zachowania kompatybilności
def main() -> None:
    """Główna funkcja uruchamiająca analizę"""
    analyzer = TravelAnalyzer()
    analyzer.run_analysis()

if __name__ == "__main__":
    main()