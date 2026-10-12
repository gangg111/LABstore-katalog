# LABstore — katalog

Lista aplikacji dla [LABstore](https://github.com/gangg111/Sklep). Aplikacja pobiera `catalog.json` z tego repozytorium przy każdym odświeżeniu, więc dodanie lub zmiana aplikacji to tylko commit tutaj — bez wydawania nowej wersji LABstore.

Ścieżki względne (`icons/…`) odnoszą się do tego repozytorium. Format wpisu:

```json
{
  "package": "com.przyklad.app",
  "name": "Nazwa",
  "repo": "gangg111/Repozytorium",
  "category": "Narzędzia",
  "summary": "Jedno zdanie na listę",
  "description": "Pełny opis na stronę aplikacji",
  "icon": "icons/nazwa.png",
  "banner": "banners/nazwa.jpg",
  "screenshots": ["https://raw.githubusercontent.com/..."],
  "apk": "nazwa-pliku.apk"
}
```

- `banner` (opcjonalne) to grafika promocyjna na karcie „Najnowsze wydanie”, jak „feature graphic” w Google Play: JPG 1024×500, bez tekstu, główny motyw na środku. Bez niej karta pokazuje ikonę na gradiencie.
- `screenshots`: grafiki w stylu Google Play (tło, nagłówek, telefon ze zrzutem) robi `tools/promo.py` z wierszy `tools/screenshots.tsv`; wynik trafia do `screenshots/`. Można też podać zwykłe adresy zrzutów.
- `apk` jest opcjonalne. Bez niego LABstore bierze pierwszy plik `.apk` z wydania.
- Wersja to tag wydania porównywany z `versionName`. Dokładniej działa plik `<nazwa-apk>.json` z polem `versionCode` dołączony do wydania obok APK.
- Wydanie oznaczone jako pre-release widać tylko po włączeniu „Pokaż wersje testowe”.
