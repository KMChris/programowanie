# Financial data analysis

## Description

Application for financial data analysis. It uses data from
[Financial Modeling Prep API](https://site.financialmodelingprep.com/developer/docs/).
API key is required to run the application. You can get
your own [here](https://site.financialmodelingprep.com/login).
Then set API_KEY environment variable to your key. You can also
use your own API key by creating `.env` file in the root directory
of the project and adding API_KEY variable with your key as a value.

The application allows you to view the financial data of a given company.
Using various analysis methods it analyzes the data, shows the results
and predicts future market prices.

**Note:** The application is still in development.

***

## Setup

```bash
git clone git@gitlab.com:KMChris/programowanie.git
cd programowanie
git checkout dev
```

## Commit

```bash
git add .
git pull
git commit -m "Commit message"
git push
```

## Merge dev to main

```bash
git checkout main
git merge dev
git push
```
