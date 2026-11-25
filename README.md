# Liner Connectivity Observatory

Compare economy-level container-port throughput with UNCTAD's liner shipping connectivity index as published in World Development Indicators. Explore ranks and coverage by year and region, inspect individual economies, and export the matched sample.

[Open the interactive report](https://ehsan-ch.github.io/liner-connectivity-observatory/)

## Results

In 2021, **118 of 217 eligible economies** had both values. The two measures had a Spearman rank correlation of **0.896** on that matched sample. Indonesia ranked **15th in throughput and 56th in connectivity**, the largest absolute rank difference. In 2024, 103 economies had throughput data and none had a connectivity observation in this WDI snapshot. No correlation is computed for 2022–2024. The 2019, 2020 and 2021 matched samples differ in size and composition.

## Reproduce

With Python 3.12, run `python build.py` and `python -m unittest -v`. Open `index.html` directly. The project has no external dependencies at build or run time.

Rank both series from largest to smallest in the selected region and year after excluding incomplete pairs. Assign average ranks to ties and calculate Spearman's ρ as the Pearson correlation of those ranks. Correlation is unavailable with fewer than two matches or a constant rank series. Rank gap is throughput rank minus connectivity rank. Select rows by descending absolute gap, then economy code.

Coverage retains every non-aggregate economy in the frozen country metadata, including territories and economies with neither measure. Zero is an observed value. Region aggregates are excluded by the country metadata. The matched set can differ by selection. These ranks characterize the paired sample and do not establish a causal effect of connectivity.

## Sources

Both indicators credit UNCTAD and list CC BY 4.0. See [World Bank dataset terms](https://www.worldbank.org/ext/en/legal/terms-conditions/datasets). The MIT license applies to the code.

- [WDI container port traffic (IS.SHP.GOOD.TU)](https://data.worldbank.org/indicator/IS.SHP.GOOD.TU). The [2019–2024 API query](https://api.worldbank.org/v2/country/all/indicator/IS.SHP.GOOD.TU?source=2&date=2019:2024&format=json&per_page=2000) is bundled as `source-data/traffic.json`, reused from the Container Throughput Observatory snapshot.
- [WDI liner shipping connectivity index (IS.SHP.GCNW.XQ)](https://data.worldbank.org/indicator/IS.SHP.GCNW.XQ). The [2019–2024 API query](https://api.worldbank.org/v2/country/all/indicator/IS.SHP.GCNW.XQ?source=2&date=2019:2024&format=json&per_page=2000) is bundled as `source-data/connectivity.json`. Its metadata update date does not imply a new value for every year.
- [World Bank economy metadata](https://api.worldbank.org/v2/country?format=json&per_page=400) is bundled as `source-data/economies.json`.
