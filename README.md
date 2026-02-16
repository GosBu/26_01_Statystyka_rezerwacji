# System Analizy Rocznej Statystyk Podróżnych

## Informacja o przetwarzaniu danych
**Ten system służy do demonstracji procesu przetwarzania danych wrażliwych.**

Dane źródłowe nie zostały udostępnione w repozytorium ze względu na:
- Ochronę danych osobowych (RODO)
- Poufność informacji biznesowych  
- Bezpieczeństwo danych finansowych

### Proces anonimizacji
System pokazuje transformację danych surowych w bezpieczne dane demonstracyjne poprzez:

1. **Selekcję kolumn** - wyciągnięcie tylko niezbędnych pól (6 z ~30)
2. **Czyszczenie** - usunięcie duplikatów i błędów  
3. **Anonimizację** - zastąpienie identyfikatorów demonstracyjnymi
4. **Normalizację** - ujednolicenie formatów
5. **Walidację** - zweryfikowanie kompletności i spójności

#### Struktura bezpiecznych danych (6 kolumn):
- **Lp.** - numer porządkowy (wygenerowany)
- **Nr rezerwacji** - anonimowy identyfikator (DEMO12345) 
- **Klient ID** - anonimowy identyfikator klienta (K1234)
- **Data utworzenia** - data rezerwacji (zweryfikowana)
- **Kierunek** - cel podróży (znormalizowany)
- **Hotel** - nazwa hotelu (znormalizowana)

#### Zachowana funkcjonalność:
- Pipeline normalizacji hoteli i kierunków (1000+ reguł)
- Kategoryzacja według reguł biznesowych  
- Analiza statystyczna i raportowanie
- Wszystkie algorytmy działają identycznie jak na danych rzeczywistych

Pliki `rok_*_processed.xls` w `/Dane/przetworzone/` powstały właśnie dzięki procesowi anonimizacji z użyciem `anonymize_data.py`.

## Opis
Zaawansowany system do analizy i kategoryzacji danych podróżnych z wielu lat (2019-2025). System pracuje na **zanonimizowanych danych demonstracyjnych** i automatycznie normalizuje dane hotelowe oraz kierunkowe, a następnie kategoryzuje rekordy zgodnie z predefinowanymi regułami biznesowymi.

## Funkcjonalności
- **Automatyczna normalizacja** hoteli i kierunków na podstawie reguł JSON
- **Inteligentna kategoryzacja** z hierarchią priorytetów 
- **98.7% dokładność** kategoryzacji (3859/3909 rekordów)
- **Wszechstronne raportowanie** - tabele miesięczne, roczne, zbiorcze
- **Obsługa 16 kategorii** zgodnie z wymaganiami biznesowymi
- **Pełna analiza 7 lat** danych podróżnych (2019-2025)

## Architektura
```
System składa się z modularnych komponentów:

główne/
├── main.py              # Punkt wejścia - orkiestruje cały proces
├── data_loader.py       # Wczytywanie i walidacja danych z Excel
├── normalizer.py        # Normalizacja hoteli/kierunków (1000+ reguł)
├── categorizer.py       # Kategoryzacja z logiką biznesową
├── analyzer.py          # Analiza i tworzenie statystyk
├── exporter.py          # Eksport do Excel z formatowaniem
├── models.py           # Modele danych (TravelRecord)
├── config.py           # Centralna konfiguracja systemu
└── requirements.txt    # Zależności Python

strategies/          # Strategy Pattern dla kategoryzacji
├── base_strategy.py        # Bazowa klasa strategii
├── category_manager.py     # Manager wszystkich strategii
├── policy_strategy.py      # Strategia ubezpieczeń/polis
├── flight_strategy.py      # Strategia przelotów
├── training_strategy.py    # Strategia szkoleń
├── equipment_strategy.py   # Strategia sprzętu
└── [inne strategie]...     # Strategie dla różnych kategorii

config/
├── hotel_rules.json        # 1000+ reguł normalizacji hoteli
├── destination_rules.json  # 150+ reguł normalizacji kierunków
└── patterns.json           # Wzorce rozpoznawania

Dane/
├── surowe/             # (Puste - dane źródłowe usunięte ze względów bezpieczeństwa)
├── przetworzone/       # Zanonimizowane dane demonstracyjne (rok_2019-2025.xls)  
└── oczyszczone/        # Dane po przetworzeniu i normalizacji

Wyniki/             # Wygenerowane raporty Excel
```

## Architektura klas - wyjaśnienie `def __init__`


### Strategy Pattern w praktyce:
System używa **Strategy Pattern** - każda kategoria ma swoją strategię:
- `PolicyStrategy` - obsługuje ubezpieczenia/polisy
- `FlightStrategy` - obsługuje przeloty
- `TrainingStrategy` - obsługuje szkolenia
- `CategoryManager` - orkiestruje wszystkie strategie

## Instalacja i Uruchomienie

### Wymagania
- Python 3.9+
- pip

### Kroki instalacji
```bash
# 1. Sklonuj repozytorium
cd Travel_stat/liczenie_rok

# 2. Zainstaluj zależności  
pip install -r requirements.txt

# 3. Uruchom analizę (używa zanonimizowanych danych demonstracyjnych)
python main.py
```

**Uwaga:** System używa zanonimizowanych danych demonstracyjnych z folderu `/Dane/przetworzone/`.

## Wyniki
System generuje kompletne raporty w folderze `Wyniki/`:

### Pliki wyjściowe:
- `travel_statistics_COMBINED.xlsx` - zbiorczy raport wszystkich lat
- `travel_statistics_2019.xlsx` - analiza roku 2019
- `travel_statistics_2020.xlsx` - analiza roku 2020  
- `travel_statistics_2021.xlsx` - analiza roku 2021
- `travel_statistics_2022.xlsx` - analiza roku 2022
- `travel_statistics_2023.xlsx` - analiza roku 2023
- `travel_statistics_2024.xlsx` - analiza roku 2024
- `travel_statistics_2025.xlsx` - analiza roku 2025

### Zawartość raportów:
- **Statystyki Miesięczne** - tabela miesiąc × kategoria
- **Statystyki Roczne** - podsumowania roczne  
- **Szkolenia/Sprzęt** - dedykowana analiza szkoleń
- **Nieprzypisane** - rekordy wymagające uwagi (1.2%)
- **Wszystkie Dane** - pełen zestaw danych z kategoriami
- **Znormalizowane Dane** - dane po normalizacji

## Kategorie biznesowe
System rozpoznaje 16 głównych kategorii:

| Kategoria | Opis | Przykłady |
|-----------|------|-----------|
| **Egipt - El Gouna** | Hotele w El Gouna | Movenpick, Sheraton, Three Corners |
| **Egipt - Hamata** | Hotele w Hamata | Wadi Lahmy, Kite Village |
| **Egipt - inne** | Pozostałe hotele egipskie | Soma Bay, Marsa Alam, Sharm |
| **Kitesafari** | Safari kitesurfingowe | AML Hayaty, Valerie, jachty |
| **Grecja - Limnos** | Hotele na Limnos | Keros Blue |
| **Grecja - Rodos** | Hotele na Rodos | Ledras Beach, Ocean Palace |
| **Grecja - Inne** | Pozostałe wyspy greckie | Zakynthos, Korfu, Kos |
| **Sal** | Wyspy Zielonego Przylądka | Paradisio, Oasis Atlantico |
| **Fuerteventura** | Wyspy Kanaryjskie | SBH Monica, Club Paraiso |
| **Brazylia** | Fortaleza, Salvador | Brazil Kite Safari |
| **Mauritius** | Mauritius | Riu Creole |
| **Turcja** | Hotele tureckie | Xeno Eftalia, Kirman Belazur |
| **Egzotyka - inne** | Pozostałe egzotyczne | RPA, Filipiny, Tajlandia |
| **Szkolenia** | Kursy i szkolenia | YALLA KITE, kursy IKO |
| **Sprzęt** | Wypożyczenie sprzętu | Wynajmy kitów, desek |
| **Sam przelot** | Bilety lotnicze | WAW-HRG, instruktorskie |
| **Ubezpieczenie** | Polisy podróżne | Allianz, ERV, ubezpieczenia KR |
| **Voucher** | Vouchery prezentowe | Bezterminowe |
| **Narty** | Wyjazdy narciarskie | Austria, narty |
| **Nieprzypisane** | Rekordy specjalne | Rezygnacje, skrócenia, testy |

## Wydajność
- **Czas przetwarzania**: ~5 sekund dla 3909 rekordów
- **Dokładność kategoryzacji**: 98.7%
- **Automatyczna normalizacja**: 1000+ reguł
- **Obsługa**: 7 lat danych (2019-2025)

## Konfiguracja
Główne ustawienia w `config.py`:
- Ścieżki do plików źródłowych
- Lista lat do analizy
- Mapowanie kategorii
- Ustawienia eksportu

Reguły normalizacji w `config/*.json`:
- `hotel_rules.json` - 1000+ reguł hoteli
- `destination_rules.json` - 150+ reguł kierunków
- `patterns.json` - wzorce rozpoznawania

## Statystyki systemu
- **Rekordów przetworzonych**: 3,909
- **Lat analizowanych**: 7 (2019-2025)
- **Kategorii**: 16 głównych + nieprzypisane
- **Reguł normalizacji**: 1000+
- **Dokładność**: 98.7%
- **Nieprzypisanych**: 50 rekordów (1.3%)
