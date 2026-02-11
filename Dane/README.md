# 📂 Struktura foldera Dane

## Organizacja danych:

### 📄 `/surowe/`
**Nie udostępnione w repozytorium**
- Oryginalne pliki: rok_YYYY_raw.xls (np. rok_2020_raw.xls)
- Zawierają informacje wrażliwe (dane osobowe, finansowe)
- **Powód braku:** Ochrona danych osobowych i poufność biznesowa

### `/oczyszczone/` 
**Puste** - Folder na dane po pierwszym etapie czyszczenia
- Dane po usunięciu duplikatów i błędnych wpisów
- Nadal mogą zawierać informacje wrażliwe

### `/przetworzone/`
**Dane wejściowe systemu** - Bezpieczne do publicznego udostępnienia
- **Struktura:** 6 kolumn - tylko niezbędne do analizy
- **Zawartość:** Znormalizowane, wyczyszczone, zanonimizowane dane
- **Pliki:** rok_2019_processed.xls, rok_2020_processed.xls, ..., rok_2025_processed.xls

---

## Pipeline przetwarzania:

```
rok_YYYY_raw.xls → Czyszczenie → Normalizacja → Anonimizacja → rok_YYYY_processed.xls
     (brak)         (oczyszczone)                                    (obecne)
```

## Cel:
Demonstracja pełnej funkcjonalności systemu analitycznego przy zachowaniu bezpieczeństwa i prywatności danych źródłowych.