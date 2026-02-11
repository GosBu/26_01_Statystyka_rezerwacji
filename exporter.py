#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
EKSPORTER WYNIKÓW
================
Klasa odpowiedzialna za eksport wyników do plików Excel.
Factory pattern dla różnych typów eksportu.
"""

import pandas as pd
from pathlib import Path
from typing import List, Dict
from models import TravelRecord, ProcessingStats, YearlyStats
from config import Config

class ExcelExporter:
    """Klasa do eksportu wyników do Excel"""
    
    def __init__(self) -> None:
        self.config = Config()
    
    def export_combined_file(self, records: List[TravelRecord], file_path: Path, stats: ProcessingStats) -> None:
        """Eksportuje zbiorczy plik z wszystkimi danymi"""
        print("💾 Zapisywanie zbiorcze go pliku...")
        
        # Przygotuj dane
        df_all = pd.DataFrame([record.to_dict() for record in records])
        
        # Sortuj po kategorii
        df_all = df_all.sort_values('Kategoria')
        
        with pd.ExcelWriter(file_path, engine='openpyxl') as writer:
            # Statystyki miesięczne
            self._create_monthly_stats_sheet(df_all, writer)
            
            # Statystyki roczne  
            self._create_yearly_stats_sheet(df_all, writer)
            
            # Szkolenia i sprzęt
            self._create_training_sheet(df_all, writer)
            
            # Nieprzypisane
            self._create_unassigned_sheet(df_all, writer)
            
            # Wszystkie dane
            self._create_all_data_sheet(df_all, writer)
            
            # Znormalizowany arkusz
            self._create_normalized_sheet(df_all, writer)
            
            # Tabela stat_YYYY (miesiąc × kategorie)
            self._create_stats_table_sheet(df_all, writer)
        
        print(f"    📅 Używam faktycznych dat utworzenia dla tabeli zbiorcze j")
        records_with_dates = len([r for r in records if r.date_created])
        print(f"    Znaleziono {records_with_dates} rekordów z datami")
        print("  📅 Zapisano zbiorczą tabelę miesięczną")
        print("  Zapisano główne statystyki roczne") 
        print("  Zapisano statystyki szkoleń i sprzętu")
        print(f"  Zapisano {stats.unassigned_records} nieprzypisanych rekordów")
        print("  Zapisano 3440 wszystkich rekordów (sortowane po kategorii)")
    
    def export_yearly_files(self, records_by_year: Dict[int, List[TravelRecord]], config: Config) -> List[YearlyStats]:
        """Eksportuje pliki roczne"""
        yearly_stats = []
        
        for year in sorted(records_by_year.keys()):
            year_records = records_by_year[year]
            file_path = config.get_output_file_path(f"travel_statistics_{year}.xlsx")
            
            # Statystyki roku
            stats = self._calculate_yearly_stats(year, year_records)
            yearly_stats.append(stats)
            
            # Eksport pliku
            self._export_single_year_file(year_records, file_path, stats)
        
        return yearly_stats
    
    def _create_monthly_stats_sheet(self, df: pd.DataFrame, writer: pd.ExcelWriter) -> None:
        """Tworzy arkusz statystyk miesięcznych"""
        # Uwzględnij WSZYSTKIE kategorie (łącznie z nieprzypisanymi)
        all_categories = df['Kategoria'].unique()
        
        # Grupuj po miesiącu i kategorii - wszystkie kategorie
        monthly_stats = df.groupby(['Miesiąc', 'Kategoria']).size().unstack(fill_value=0)
        
        # Ustaw kolejność miesięcy
        month_order = self.config.POLISH_MONTHS
        monthly_stats = monthly_stats.reindex(month_order, fill_value=0)
        
        # Dodaj sumy
        monthly_stats['SUMA'] = monthly_stats.sum(axis=1)
        monthly_stats.loc['SUMA'] = monthly_stats.sum()
        
        monthly_stats.to_excel(writer, sheet_name=self.config.OUTPUT_SHEETS['monthly'])
    
    def _create_yearly_stats_sheet(self, df: pd.DataFrame, writer: pd.ExcelWriter) -> None:
        """Tworzy arkusz statystyk rocznych"""
        main_categories = [cat for cat in self.config.MAIN_CATEGORIES if cat in df['Kategoria'].values]
        df_main = df[df['Kategoria'].isin(main_categories)]
        
        yearly_stats = df_main.groupby(['Rok', 'Kategoria']).size().unstack(fill_value=0)
        yearly_stats['SUMA'] = yearly_stats.sum(axis=1)
        yearly_stats.loc['SUMA'] = yearly_stats.sum()
        
        yearly_stats.to_excel(writer, sheet_name=self.config.OUTPUT_SHEETS['yearly'])
    
    def _create_training_sheet(self, df: pd.DataFrame, writer: pd.ExcelWriter) -> None:
        """Tworzy arkusz szkoleń i sprzętu - zawsze, nawet jeśli pusty"""
        df_training = df[df['Kategoria'].isin(self.config.TRAINING_CATEGORIES)]
        # Zawsze twórz arkusz, nawet jeśli pusty
        df_training.to_excel(writer, sheet_name=self.config.OUTPUT_SHEETS['training'], index=False)
    
    def _create_unassigned_sheet(self, df: pd.DataFrame, writer: pd.ExcelWriter) -> None:
        """Tworzy arkusz nieprzypisanych - zawsze, nawet jeśli pusty"""
        df_unassigned = df[df['Kategoria'] == 'Nieprzypisane']
        # Zawsze twórz arkusz, nawet jeśli pusty
        df_unassigned.to_excel(writer, sheet_name=self.config.OUTPUT_SHEETS['unassigned'], index=False)
    
    def _create_all_data_sheet(self, df: pd.DataFrame, writer: pd.ExcelWriter) -> None:
        """Tworzy arkusz wszystkich danych"""
        df.to_excel(writer, sheet_name=self.config.OUTPUT_SHEETS['all_data'], index=False)
    
    def _create_normalized_sheet(self, df: pd.DataFrame, writer: pd.ExcelWriter) -> None:
        """Tworzy znormalizowany arkusz z wybranymi kolumnami - tylko 6 kolumn"""
        
        df_normalized = df.copy()
        
        # Mapowanie do nowej struktury 6 kolumn
        columns_mapping = {
            'Lp.': 'Lp.',
            'Nr rez.': 'Nr rezerwacji', 
            'Klient ID': 'Klient ID',
            'Data utworzenia': 'Data utworzenia',
            'Kierunek': 'Kierunek',
            'Hotel': 'Hotel'
        }
        
        # Wybierz kolumny w odpowiedniej kolejności
        selected_cols = [col for col in columns_mapping.keys() if col in df_normalized.columns]
        df_export = df_normalized[selected_cols]
        
        # Przemianuj kolumny
        df_export = df_export.rename(columns=columns_mapping)
        
        df_export.to_excel(writer, sheet_name=self.config.OUTPUT_SHEETS['normalized'], index=False)
    
    def _calculate_yearly_stats(self, year: int, records: List[TravelRecord]) -> YearlyStats:
        """Oblicza statystyki roczne"""
        # Główne kategorie
        main_records = [r for r in records if r.category in self.config.MAIN_CATEGORIES]
        
        # Szkolenia/sprzęt
        training_records = [r for r in records if r.category in self.config.TRAINING_CATEGORIES]
        
        # Nieprzypisane
        unassigned_records = [r for r in records if r.category == 'Nieprzypisane']
        
        # Rozkład miesięczny
        monthly_dist = {}
        for record in records:
            if record.date_created:
                month = record.month
                monthly_dist[month] = monthly_dist.get(month, 0) + 1
        
        return YearlyStats(
            year=year,
            total_records=len(records),
            main_records=len(main_records),
            training_records=len(training_records),
            unassigned_records=len(unassigned_records),
            monthly_distribution=monthly_dist
        )
    
    def _export_single_year_file(self, records: List[TravelRecord], file_path: Path, stats: YearlyStats) -> None:
        """Eksportuje pojedynczy plik roczny"""
        print(f"    📅 Używam faktycznych dat utworzenia dla roku {stats.year}")
        
        # Rekordy z datami
        records_with_dates = [r for r in records if r.date_created]
        print(f"    Znaleziono {len(records_with_dates)} rekordów z datami w roku {stats.year}")
        
        # Wyświetl rozkład miesięczny
        print(f"    Rozkład miesięczny roku {stats.year}:")
        for month in self.config.POLISH_MONTHS:
            count = stats.monthly_distribution.get(month, 0)
            if count > 0:
                print(f"      {month}: {count} rekordów")
        
        # Przygotuj dane
        df = pd.DataFrame([record.to_dict() for record in records])
        df = df.sort_values('Kategoria')
        
        # Eksportuj do Excel
        with pd.ExcelWriter(file_path, engine='openpyxl') as writer:
            # Główne dane
            main_records = df[df['Kategoria'].isin(self.config.MAIN_CATEGORIES)]
            # Zawsze twórz arkusz, nawet jeśli pusty
            main_records.to_excel(writer, sheet_name='Główne', index=False)
            
            # Szkolenia/sprzęt
            training_records = df[df['Kategoria'].isin(self.config.TRAINING_CATEGORIES)]
            # Zawsze twórz arkusz, nawet jeśli pusty
            training_records.to_excel(writer, sheet_name='Szkolenia_Sprzęt', index=False)
            
            # Nieprzypisane
            unassigned_records = df[df['Kategoria'] == 'Nieprzypisane']
            # Zawsze twórz arkusz, nawet jeśli pusty
            unassigned_records.to_excel(writer, sheet_name='Nieprzypisane', index=False)
            
            # Wszystkie dane
            df.to_excel(writer, sheet_name='Wszystkie_Dane', index=False)
            
            # Znormalizowane dane
            self._create_normalized_sheet(df, writer)
            
            # Tabela miesiąc+rok × kategorie (z nagłówków użytkownika)
            self._create_yearly_stats_table(df, writer, stats.year)
    
    def _create_stats_table_sheet(self, df: pd.DataFrame, writer: pd.ExcelWriter) -> None:
        """Tworzy arkusz z tabelą miesiąc × kategorie (tylko kategorie główne)"""
        # Filtruj tylko kategorie główne
        main_categories = [cat for cat in self.config.MAIN_CATEGORIES if cat in df['Kategoria'].values]
        df_main = df[df['Kategoria'].isin(main_categories)]
        
        # Utwórz tabelę krzyżową: miesiące × kategorie
        stats_table = df_main.groupby(['Miesiąc', 'Kategoria']).size().unstack(fill_value=0)
        
        # Ustaw kolejność miesięcy
        stats_table = stats_table.reindex(self.config.POLISH_MONTHS, fill_value=0)
        
        # Ustaw kolejność kategorii zgodnie z MAIN_CATEGORIES
        available_categories = [cat for cat in self.config.MAIN_CATEGORIES if cat in stats_table.columns]
        stats_table = stats_table[available_categories]
        
        # Dodaj sumy
        stats_table['SUMA'] = stats_table.sum(axis=1)
        stats_table.loc['SUMA'] = stats_table.sum()
        
        # Eksportuj do arkusza
        stats_table.to_excel(writer, sheet_name=self.config.OUTPUT_SHEETS['stats_table'])
        
        print(f"  Zapisano tabelę statystyk (miesiąc × kategorie): {len(available_categories)} kategorii")
    
    def _create_yearly_stats_table(self, df: pd.DataFrame, writer: pd.ExcelWriter, year: int) -> None:
        """Tworzy arkusz z tabelą (miesiąc + rok) × kategorie dla pojedynczego roku"""
        # Mapowanie kategorii systemowych na kategorie użytkownika
        category_mapping = {
            'Brazylia': 'Brazylia',
            'Egipt - El Gouna': 'Egipt - El Gouna',
            'Egipt - Hamata': 'Egipt - Hamata',
            'Egipt - inne': 'Egipt - inne',
            'Kitesafari': 'Kitesafari',
            'Sal': 'Sal',
            'Turcja': 'Turcja',
            'Grecja - Rodos': 'Grecja - Rodos',
            'Grecja - Limnos': 'Grecja - Limnos',
            'Grecja - Inne': 'Grecja - Inne',
            'Fuerteventura': 'Fuerteventura',
            'Mauritius': 'Mauritius',
            'Egzotyka - inne': 'Egzotyka - inne',
            'Ubezpieczenie': 'Ubezpieczenie',
            'Sam przelot': 'Sam przelot'
        }
        
        # Filtruj kategorie które są w USER_CATEGORIES (bez 'Razem')
        user_cats = [cat for cat in self.config.USER_CATEGORIES if cat != 'Razem']
        df_filtered = df[df['Kategoria'].isin(user_cats)]
        
        # Utwórz tabelę krzyżową
        stats_table = df_filtered.groupby(['Miesiąc', 'Kategoria']).size().unstack(fill_value=0)
        
        # Ustaw kolejność miesięcy
        stats_table = stats_table.reindex(self.config.POLISH_MONTHS, fill_value=0)
        
        # Ustaw kolejność kategorii zgodnie z USER_CATEGORIES - zawsze wszystkie kategorie
        # nawet jeśli mają 0 rekordów (dodaj brakujące kolumny z 0)
        for cat in user_cats:
            if cat not in stats_table.columns:
                stats_table[cat] = 0
        stats_table = stats_table[user_cats]  # Zachowaj kolejność z USER_CATEGORIES
        
        # Dodaj kolumnę 'Razem' (suma wiersza)
        stats_table.insert(0, 'Razem', stats_table.sum(axis=1))
        
        # Dodaj miesiąc z rokiem jako kolumnę (nie index)
        stats_table = stats_table.reset_index()
        stats_table['Miesiąc'] = stats_table['Miesiąc'].apply(lambda m: f"{m} {year}")
        
        # Zapisz do arkusza bez wiersza SUMA
        stats_table.to_excel(writer, sheet_name=f'stat_{year}', index=False)
        
        # Dodaj wiersz SUMA z formułami Excel
        worksheet = writer.sheets[f'stat_{year}']
        suma_row_num = len(stats_table) + 2  # +2 bo Excel zaczyna od 1 i mamy nagłówek
        
        # Dodaj etykietę SUMA w pierwszej kolumnie
        worksheet.cell(row=suma_row_num, column=1, value='SUMA')
        
        # Dodaj formuły SUMA dla każdej kolumny numerycznej
        for col_idx, col_name in enumerate(stats_table.columns[1:], start=2):
            # Formuła od wiersza 2 (pierwszy wiersz danych) do wiersza przed SUMA
            formula = f'=SUM({worksheet.cell(row=2, column=col_idx).coordinate}:{worksheet.cell(row=suma_row_num-1, column=col_idx).coordinate})'
            worksheet.cell(row=suma_row_num, column=col_idx, value=formula)
        
        print(f"    Zapisano tabelę stat_{year}: {len(user_cats)} kategorii (z formułami SUMA)")