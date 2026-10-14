# Weather

Owner: weather
Run: 2026-10-13-corporate-krakow
Status: final
Inputs: requirements

## Summary

The event on 2026-11-14 is 32 days away, which is beyond the 16-day forecast range. This artifact is therefore climatology, not a forecast. It uses observed conditions for 2023-11-14, 2024-11-14 and 2025-11-14. In those three years the 18:00-23:00 local window in Krakow was nearly dry, with 0.1 mm in total. The temperature was 3.1-10.3 °C and the feels-like temperature was -1.7 to 5.4 °C, so an evening fully outdoors is only marginal. Plan for an indoor main venue, with at most a heated, covered outdoor area.

## Details

Basis: climatology (historical reanalysis, not a forecast) for 2023-11-14, 2024-11-14 and 2025-11-14. The location is Krakow (50.06143, 19.93658), and the nearest data grid point is 50.0176, 19.9476 at 214 m.

Time conversion: the data was requested in GMT (UTC). On 2026-11-14 Krakow is on CET, so local time = UTC + 1. The UTC hours 17:00-22:00 are therefore shown as local 18:00-23:00. The archive's own Europe/Warsaw time zone setting was not used, because it applies a fixed UTC+2 offset, which is wrong for November.

Three-year average per hour (local time):

| Hour (local) | Hour (UTC) | Temperature (°C) | Feels like (°C) | Rain probability (years with >= 0.1 mm) | Precipitation (mm, avg) | Wind (km/h, avg) |
|---|---|---|---|---|---|---|
| 18:00 | 17:00 | 7.0 | 2.7 | 0/3 (0%) | 0.0 | 18.1 |
| 19:00 | 18:00 | 7.0 | 2.5 | 0/3 (0%) | 0.0 | 19.1 |
| 20:00 | 19:00 | 6.8 | 2.5 | 0/3 (0%) | 0.0 | 18.3 |
| 21:00 | 20:00 | 6.8 | 2.7 | 0/3 (0%) | 0.0 | 16.7 |
| 22:00 | 21:00 | 6.9 | 2.8 | 1/3 (33%) | 0.03 | 16.2 |
| 23:00 | 22:00 | 7.1 | 3.0 | 0/3 (0%) | 0.0 | 17.7 |

The historical archive has no precipitation probability. The "rain probability" column is the share of the three sample years that had measurable precipitation (>= 0.1 mm) in that hour.

Per-year range within 18:00-23:00 local:

| Year | Temperature (°C) | Feels like (°C) | Precipitation total (mm) | Wind (km/h) |
|---|---|---|---|---|
| 2023 | 10.0-10.3 | 4.7-5.4 | 0.0 | 23.2-27.7 |
| 2024 | 3.1-4.3 | -1.7 to 0.1 | 0.1 (at 22:00) | 15.7-18.4 |
| 2025 | 6.2-7.6 | 3.3-4.7 | 0.0 | 9.7-13.4 |

Outdoor suitability: marginal. Precipitation was low: 0.1 mm in total across all three evenings. Wind was moderate, with a three-year average of 16.2-19.1 km/h and a peak of 27.7 km/h in 2023. The cold is the problem. The average temperature is 6.8-7.1 °C, and the average feels-like temperature is 2.5-3.0 °C. In the coldest sample year (2024) the feels-like temperature was below 0 °C from 18:00 to 22:00, down to -1.7 °C, and only 0.1 °C at 23:00. Five hours outdoors after dark at these temperatures is not comfortable for 40 guests without heating.

Recommendation: Book an indoor main venue, or one with a heated and covered terrace. Use the outdoor area only for short segments such as a welcome drink, with patio heaters and blankets. Keep a rain fallback in the program, because three sample years cannot rule out rain, and re-check the real forecast once the date is within 16 days (from 2026-10-29).

## Costs

No costs

## Sources

- [Open-Meteo API documentation](https://open-meteo.com/en/docs) - geocoding and weather data interface
- [Open-Meteo Historical Weather API](https://open-meteo.com/en/docs/historical-weather-api) - hourly temperature, feels-like temperature, precipitation and wind for Krakow on 2023-11-14, 2024-11-14 and 2025-11-14, requested in GMT (climatology basis)

## Open issues

- This is climatology from only three sample days, not a forecast. Re-run the weather check with the forecast once 2026-11-14 is within 16 days (from 2026-10-29).
- Precipitation probability is not available from historical data. The rain column shows the share of years with rain, not a probability from a forecast.
