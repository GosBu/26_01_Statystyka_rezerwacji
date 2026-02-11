#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
ADVANCED VISUALIZATIONS & ANALYTICS
===================================
Zunifikowany moduł łączący funkcjonalności generate_charts.py i enhanced_analytics.py
do tworzenia kompletnych analiz i wizualizacji danych podróżnych.
"""

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
from pathlib import Path
from typing import Dict, List, Tuple, Optional
import warnings
warnings.filterwarnings('ignore')

# Konfiguracja matplotlib
plt.rcParams['font.family'] = 'Arial'
plt.rcParams['font.size'] = 10
plt.rcParams['figure.dpi'] = 150

class AdvancedVisualizations:
    """Zunifikowana klasa do tworzenia zaawansowanych analiz i wizualizacji"""
    
    def __init__(self, data_path: str = "Wyniki/travel_statistics_COMBINED.xlsx"):
        self.data_path = data_path
        self.output_dir = Path("Wyniki")
        self.output_dir.mkdir(exist_ok=True)
        
        # Konfiguracja kategorii
        self.category_order = [
            'Egipt - El Gouna', 'Egipt - Hamata', 'Egipt - inne',
            'Kitesafari', 'Sal', 'Turcja', 'Grecja - Rodos', 'Grecja - Limnos', 'Grecja - Inne',
            'Fuerteventura', 'Brazylia', 'Mauritius', 'Egzotyka - inne',
            'Polisa', 'Sam przelot', 'Szkolenia', 'Sprzęt', 'Nieprzypisane', 'Maroko'
        ]
        
        # Kategorie kierunków podróży
        self.travel_categories = self._get_travel_categories()
        
        self.excluded_from_viz = ['Nieprzypisane', 'Szkolenia', 'Sprzęt', 'Sam przelot', 'Ubezpieczenie']
        self.months_order = [
            'Styczeń', 'Luty', 'Marzec', 'Kwiecień', 'Maj', 'Czerwiec',
            'Lipiec', 'Sierpień', 'Wrzesień', 'Październik', 'Listopad', 'Grudzień'
        ]
        self.years = [2019, 2020, 2021, 2022, 2023, 2024, 2025]
        
        # Wczytaj dane
        self.df_all = None
        self.monthly_df = None
        self.yearly_df = None
        self._load_data()
    
    def _load_data(self):
        """Wczytuje dane z plików Excel"""
        try:
            combined_file = Path(self.data_path)
            if not combined_file.exists():
                print("Błąd: Brak pliku zbiorczego. Uruchom najpierw main.py")
                return
            
            self.df_all = pd.read_excel(combined_file, sheet_name='Wszystkie_Dane')
            self.monthly_df = pd.read_excel(combined_file, sheet_name='Statystyki_Miesięczne')
            self.yearly_df = pd.read_excel(combined_file, sheet_name='Statystyki_Roczne')
            
            print(f"Wczytano {len(self.df_all)} rekordów")
        except Exception as e:
            print(f"Błąd wczytywania danych: {e}")
            raise
    
    def _get_travel_categories(self) -> Dict[str, List[str]]:
        """Definiuje kategorie kierunków wyjazdowych"""
        return {
            'egypt': ['Egipt - El Gouna', 'Egipt - Hamata', 'Egipt - inne'],
            'greece': ['Grecja - Limnos', 'Grecja - Rodos', 'Grecja - Inne'],
            'exotic': ['Egzotyka - inne', 'Brazylia', 'Mauritius'],
            'other': ['Fuerteventura', 'Kitesafari', 'Maroko', 'Sal', 'Turcja'],
            'exclude': ['Sam przelot', 'Sprzęt', 'Szkolenia', 'Ubezpieczenie', 'Nieprzypisane', 'SUMA', 'Miesiąc']
        }
    
    def create_all_years_monthly_trend(self):
        """Tworzy wykres trendu miesięcznego ze wszystkich lat na jednym wykresie"""
        months = ['Sty', 'Lut', 'Mar', 'Kwi', 'Maj', 'Cze',
                 'Lip', 'Sie', 'Wrz', 'Paź', 'Lis', 'Gru']
        full_months = ['Styczeń', 'Luty', 'Marzec', 'Kwiecień', 'Maj', 'Czerwiec',
                      'Lipiec', 'Sierpień', 'Wrzesień', 'Październik', 'Listopad', 'Grudzień']
        
        plt.figure(figsize=(16, 10))
        
        # Kolory dla różnych lat
        colors = ['#1f77b4', '#ff7f0e', '#2ca02c', '#d62728', '#9467bd', '#8c564b', '#e377c2']
        
        for i, year in enumerate(self.years):
            try:
                year_file = Path(f"Wyniki/travel_statistics_{year}.xlsx")
                if not year_file.exists():
                    print(f"Brak pliku dla roku {year}")
                    continue
                    
                year_df = pd.read_excel(year_file, sheet_name=f'stat_{year}')
                
                # Przygotuj dane miesięczne dla roku
                month_data = []
                
                for full_month in full_months:
                    # Szukaj wiersza z miesiącem
                    month_row = year_df[year_df['Miesiąc'].str.contains(full_month, na=False)]
                    
                    if not month_row.empty:
                        # Suma wszystkich kierunków wyjazdowych dla tego miesiąca
                        total = 0
                        for col in year_df.columns:
                            if col not in self.travel_categories['exclude'] and col != 'Miesiąc' and col != 'Razem':
                                val = month_row.iloc[0].get(col, 0)
                                if pd.notna(val) and val != '':
                                    try:
                                        total += int(val)
                                    except ValueError:
                                        pass
                        month_data.append(total)
                    else:
                        month_data.append(0)
                
                # Dodaj linię dla roku
                plt.plot(months, month_data, marker='o', linewidth=2.5, markersize=6, 
                        label=f'{year}', color=colors[i % len(colors)])
                
                print(f"Dane dla {year}: {month_data}")
                
            except Exception as e:
                print(f"Błąd przy roku {year}: {e}")
        
        plt.title('Trend miesięczny rezerwacji kierunków wyjazdowych (2019-2025)', 
                  fontsize=16, fontweight='bold', pad=20)
        plt.xlabel('Miesiąc', fontsize=14)
        plt.ylabel('Liczba rezerwacji', fontsize=14)
        plt.legend(loc='upper right', fontsize=12, title='Rok')
        plt.grid(True, alpha=0.3)
        
        plt.xticks(fontsize=12)
        plt.yticks(fontsize=12)
        
        plt.tight_layout()
        plt.savefig(self.output_dir / 'all_years_monthly_trend.png', dpi=200, bbox_inches='tight')
        plt.close()
        
        print("Zapisano wykres: all_years_monthly_trend.png")
    
    def create_monthly_trends_by_year(self):
        """Tworzy wykresy miesięcznych trendów dla każdego roku osobno"""
        
        months = ['Styczeń', 'Luty', 'Marzec', 'Kwiecień', 'Maj', 'Czerwiec',
                 'Lipiec', 'Sierpień', 'Wrzesień', 'Październik', 'Listopad', 'Grudzień']
        
        for year in self.years:
            try:
                year_file = Path(f"Wyniki/travel_statistics_{year}.xlsx")
                if not year_file.exists():
                    continue
                    
                year_df = pd.read_excel(year_file, sheet_name=f'stat_{year}')
                
                # Przygotuj dane miesięczne dla roku
                month_data = []
                for month in months:
                    month_row = year_df[year_df['Miesiąc'].str.contains(month, na=False)]
                    if not month_row.empty:
                        total = 0
                        for col in year_df.columns:
                            if col not in self.travel_categories['exclude'] and col != 'Miesiąc' and col != 'Razem':
                                val = month_row.iloc[0].get(col, 0)
                                if pd.notna(val):
                                    total += val
                        month_data.append(int(total))
                    else:
                        month_data.append(0)
                
                # Wykres liniowy dla roku
                plt.figure(figsize=(12, 6))
                plt.plot(months, month_data, marker='o', linewidth=2, markersize=6, color='#2E8B57')
                plt.title(f'Rezerwacje kierunków wyjazdowych - {year}', fontsize=14, fontweight='bold')
                plt.xlabel('Miesiąc', fontsize=12)
                plt.ylabel('Liczba rezerwacji', fontsize=12)
                plt.xticks(rotation=45)
                plt.grid(True, alpha=0.3)
                
                # Dodaj wartości na wykresie
                for i, value in enumerate(month_data):
                    plt.annotate(f'{value}', (i, value), textcoords="offset points", 
                               xytext=(0,10), ha='center', fontsize=9)
                
                plt.tight_layout()
                plt.savefig(self.output_dir / f'monthly_trend_{year}.png', dpi=150, bbox_inches='tight')
                plt.close()
                
                print(f"Zapisano wykres: monthly_trend_{year}.png")
                
            except Exception as e:
                print(f"Błąd przy roku {year}: {e}")
    
    def create_destination_breakdown(self):
        """Tworzy wykres podziału miesięcznego według głównych kierunków"""
        
        months = ['Styczeń', 'Luty', 'Marzec', 'Kwiecień', 'Maj', 'Czerwiec',
                 'Lipiec', 'Sierpień', 'Wrzesień', 'Październik', 'Listopad', 'Grudzień']
        
        # Przygotuj dane dla głównych kierunków
        egypt_data = []
        greece_data = []
        exotic_data = []
        other_data = []
        
        for month in months:
            month_row = self.monthly_df[self.monthly_df['Miesiąc'] == month]
            if not month_row.empty:
                row = month_row.iloc[0]
                
                # Egipt
                egypt_total = sum(row.get(cat, 0) for cat in self.travel_categories['egypt'])
                egypt_data.append(egypt_total)
                
                # Grecja
                greece_total = sum(row.get(cat, 0) for cat in self.travel_categories['greece'])
                greece_data.append(greece_total)
                
                # Egzotyka
                exotic_total = sum(row.get(cat, 0) for cat in self.travel_categories['exotic'])
                exotic_data.append(exotic_total)
                
                # Inne kierunki
                other_total = sum(row.get(cat, 0) for cat in self.travel_categories['other'])
                other_data.append(other_total)
            else:
                egypt_data.append(0)
                greece_data.append(0)
                exotic_data.append(0)
                other_data.append(0)
        
        # Stacked bar chart
        x = np.arange(len(months))
        width = 0.8
        
        plt.figure(figsize=(14, 8))
        
        p1 = plt.bar(x, egypt_data, width, label='Egipt', color='#FF6B35')
        p2 = plt.bar(x, greece_data, width, bottom=egypt_data, label='Grecja', color='#004E89') 
        p3 = plt.bar(x, exotic_data, width, bottom=np.array(egypt_data) + np.array(greece_data), 
                     label='Egzotyka', color='#009639')
        p4 = plt.bar(x, other_data, width, 
                     bottom=np.array(egypt_data) + np.array(greece_data) + np.array(exotic_data),
                     label='Inne kierunki', color='#7209B7')
        
        plt.title('Miesięczny podział rezerwacji według głównych kierunków (2019-2025)', 
                  fontsize=14, fontweight='bold')
        plt.xlabel('Miesiąc', fontsize=12)
        plt.ylabel('Liczba rezerwacji', fontsize=12)
        plt.xticks(x, months, rotation=45)
        plt.legend(loc='upper right')
        plt.grid(True, alpha=0.3, axis='y')
        
        plt.tight_layout()
        plt.savefig(self.output_dir / 'destination_breakdown.png', dpi=150, bbox_inches='tight')
        plt.close()
        
        print("Zapisano wykres: destination_breakdown.png")
    
    def create_destination_trends(self):
        """Tworzy wykresy trendów dla głównych kierunków"""
        
        months = ['Styczeń', 'Luty', 'Marzec', 'Kwiecień', 'Maj', 'Czerwiec',
                 'Lipiec', 'Sierpień', 'Wrzesień', 'Październik', 'Listopad', 'Grudzień']
        
        # Przygotuj dane
        egypt_data = []
        greece_data = []
        exotic_data = []
        
        for month in months:
            month_row = self.monthly_df[self.monthly_df['Miesiąc'] == month]
            if not month_row.empty:
                row = month_row.iloc[0]
                
                egypt_total = sum(row.get(cat, 0) for cat in self.travel_categories['egypt'])
                greece_total = sum(row.get(cat, 0) for cat in self.travel_categories['greece'])
                exotic_total = sum(row.get(cat, 0) for cat in self.travel_categories['exotic'])
                
                egypt_data.append(egypt_total)
                greece_data.append(greece_total)
                exotic_data.append(exotic_total)
            else:
                egypt_data.append(0)
                greece_data.append(0)
                exotic_data.append(0)
        
        # Line chart z trzema liniami
        plt.figure(figsize=(14, 8))
        
        x = range(len(months))
        plt.plot(x, egypt_data, marker='o', linewidth=3, markersize=8, 
                 label='Egipt', color='#FF6B35')
        plt.plot(x, greece_data, marker='s', linewidth=3, markersize=8,
                 label='Grecja', color='#004E89')
        plt.plot(x, exotic_data, marker='^', linewidth=3, markersize=8,
                 label='Egzotyka', color='#009639')
        
        plt.title('Trendy miesięczne głównych kierunków (2019-2025)', 
                  fontsize=14, fontweight='bold')
        plt.xlabel('Miesiąc', fontsize=12)
        plt.ylabel('Liczba rezerwacji', fontsize=12)
        plt.xticks(x, months, rotation=45)
        plt.legend(loc='upper right', fontsize=11)
        plt.grid(True, alpha=0.3)
        
        # Dodaj wartości przy punktach dla Egiptu (największe wartości)
        for i, value in enumerate(egypt_data):
            if value > 50:  # Tylko dla większych wartości żeby nie zaśmiecać wykresu
                plt.annotate(f'{value}', (i, value), textcoords="offset points", 
                           xytext=(0,10), ha='center', fontsize=9, color='#FF6B35')
        
        plt.tight_layout()
        plt.savefig(self.output_dir / 'destination_trends.png', dpi=150, bbox_inches='tight')
        plt.close()
        
        print("Zapisano wykres: destination_trends.png")
    
    def create_enhanced_heatmap(self, year: Optional[int] = None):
        """Tworzy heatmapę miesięcznego rozkładu kategorii"""
        
        if year:
            # Heatmapa dla konkretnego roku
            year_data = self.df_all[self.df_all['Rok'] == year]
            if len(year_data) == 0:
                print(f"Brak danych dla roku {year}")
                return
            
            pivot_data = year_data.groupby(['Miesiąc', 'Kategoria']).size().unstack(fill_value=0)
            title = f'Heatmapa rozkładu miesięcznego - {year}'
            filename = f'heatmap_{year}.png'
        else:
            # Heatmapa dla wszystkich lat
            pivot_data = self.df_all.groupby(['Miesiąc', 'Kategoria']).size().unstack(fill_value=0)
            title = 'Heatmapa rozkładu miesięcznego (2019-2025)'
            filename = 'heatmap_combined.png'
        
        # Filtruj kategorie do wizualizacji
        viz_categories = [cat for cat in pivot_data.columns if cat not in self.excluded_from_viz]
        pivot_data = pivot_data[viz_categories]
        
        plt.figure(figsize=(16, 8))
        sns.heatmap(pivot_data.T, annot=True, fmt='d', cmap='YlOrRd', 
                   cbar_kws={'label': 'Liczba rezerwacji'})
        plt.title(title, fontsize=14, fontweight='bold')
        plt.xlabel('Miesiąc', fontsize=12)
        plt.ylabel('Kategoria', fontsize=12)
        
        plt.tight_layout()
        plt.savefig(self.output_dir / filename, dpi=150, bbox_inches='tight')
        plt.close()
        
        print(f"Zapisano heatmapę: {filename}")
    
    def generate_all_visualizations(self):
        """Główna funkcja generująca wszystkie wizualizacje"""
        
        print("Generowanie kompletnego zestawu wizualizacji...")
        
        if self.df_all is None or self.monthly_df is None:
            print("Błąd: Brak danych do wizualizacji")
            return
        
        print("1. Tworzenie wykresów miesięcznych dla każdego roku...")
        self.create_monthly_trends_by_year()
        
        print("2. Tworzenie wykresu podziału według kierunków...")
        self.create_destination_breakdown()
        
        print("3. Tworzenie wykresów trendów kierunków...")
        self.create_destination_trends()
        
        print("4. Tworzenie wykresu trendu ze wszystkich lat...")
        self.create_all_years_monthly_trend()
        
        print("5. Tworzenie heatmap...")
        self.create_enhanced_heatmap()  # Zbiorczą heatmapę
        
        # Heatmapy dla wybranych lat
        for year in [2019, 2023, 2025]:
            self.create_enhanced_heatmap(year)
        
        print(f"\nWszystkie wizualizacje zapisane w folderze: {self.output_dir}")


def main():
    """Główna funkcja uruchamiająca wizualizacje"""
    try:
        visualizer = AdvancedVisualizations()
        visualizer.generate_all_visualizations()
        print("\nGenerowanie wizualizacji zakończone pomyślnie!")
        
    except Exception as e:
        print(f"Błąd podczas generowania wizualizacji: {e}")


if __name__ == "__main__":
    main()