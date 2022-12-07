# Web scrapping

## Description
Aplikacja powinna pobierać kod źródłowy co najmniej kilku osobnych stron
(lub podstron jednego portalu) i na podstawie pobranych danych, wykonywać
pewną analizę. Powinna być możliwość zapisania otrzymanych wyników w osobnym pliku.
Jakość projektu zależy ściśle od funkcjonalności interfejsu i poziomu zaawansowania
przeprowadzonej analizy. Przykład: zaplanowanie zwiedzania
najciekawszych miejsc w danym mieście na podstawie strony tripadvisor.

## Setup

```bash
git clone git@gitlab.com:KMChris/programowanie.git webscraper
cd webscraper
```

## Switch branch to dev

```bash
git checkout dev
```

## Commit

```bash
git add .
git commit -m "Commit message"
git push
```

## Create merge request

```bash
git checkout -b feature-name
git push --set-upstream origin feature-name
```

## Merge request

```bash
git checkout dev
git merge feature-name
git push
```

## Merge dev to main

```bash
git checkout main
git merge dev
git push
```
