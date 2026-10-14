# Weather

Owner: weather
Run: 2026-10-13-graduation-warsaw
Status: final
Inputs: requirements

## Summary
The event date 2026-11-28 is 46 days away, beyond the 16-day forecast range, so this is climatology, not a forecast: it summarises the same date (2023-11-28, 2024-11-28, 2025-11-28) from the Open-Meteo historical archive. In all three years the 17:00-23:00 evening was almost dry (at most 0.3 mm in total), with light winds (max 13.3 km/h) and gusts no higher than 23.8 km/h, but cold (-4.9 to 5.7 °C). Conditions for a short outdoor fireworks show are suitable on this basis; keep the indoor fallback ready because the real weather is only known from about 2026-11-12 onwards.

## Details

Basis: climatology (not a forecast), Open-Meteo historical archive (ERA5), hourly data for 2023-11-28, 2024-11-28 and 2025-11-28. Location: Warsaw, resolved by geocoding to 52.22977, 21.01178 (archive grid cell 52.26713, 20.961182, elevation 113 m); no specific suburb is named in the requirements. Data was requested in GMT and converted to local time as CET (UTC+1): 17:00-23:00 local = 16:00-22:00 UTC.

Event window, 3-year mean per hour (local time, CET):

| Hour (local) | Temperature mean (range) | Rain frequency | Precipitation mean (max) | Wind mean (max) | Gusts mean (max) |
|---|---|---|---|---|---|
| 17:00 | 0.3 °C (-3.5 to 5.0) | 0 of 3 years | 0.00 mm (0.0) | 11.5 km/h (12.8) | 22.4 km/h (23.8) |
| 18:00 | 0.4 °C (-3.8 to 5.6) | 1 of 3 years | 0.03 mm (0.1) | 11.5 km/h (13.3) | 23.2 km/h (23.8) |
| 19:00 | 0.1 °C (-4.1 to 5.6) | 1 of 3 years | 0.07 mm (0.2) | 10.5 km/h (11.2) | 22.3 km/h (23.0) |
| 20:00 | 0.1 °C (-4.3 to 5.6) | 0 of 3 years | 0.00 mm (0.0) | 10.3 km/h (11.3) | 20.5 km/h (21.6) |
| 21:00 | 0.1 °C (-4.5 to 5.7) | 0 of 3 years | 0.00 mm (0.0) | 10.0 km/h (11.7) | 20.5 km/h (21.2) |
| 22:00 | 0.0 °C (-4.9 to 5.6) | 0 of 3 years | 0.00 mm (0.0) | 8.8 km/h (10.7) | 19.4 km/h (21.2) |
| 23:00 | 0.1 °C (-4.9 to 5.4) | 0 of 3 years | 0.00 mm (0.0) | 7.9 km/h (9.8) | 16.8 km/h (19.1) |

Rain frequency is the share of the three years with any precipitation in that hour. The archive does not provide a precipitation probability, so this replaces it.

Per year, 17:00-23:00 local:

| Year | Temperature | Precipitation total | Max wind | Max gust |
|---|---|---|---|---|
| 2023-11-28 | -4.9 to -3.5 °C | 0.0 mm | 13.3 km/h | 23.8 km/h |
| 2024-11-28 | 5.0 to 5.7 °C | 0.3 mm (18:00-19:00) | 11.5 km/h | 23.4 km/h |
| 2025-11-28 | -1.1 to -0.3 °C | 0.0 mm | 10.5 km/h | 22.3 km/h |

Outdoor suitability: suitable (for the outdoor fireworks show; the main event is indoors). In the three reference years the evening had at most 0.3 mm of precipitation in total, wind of at most 13.3 km/h and gusts of at most 23.8 km/h, with wind and gusts easing towards 22:00-23:00 (mean gusts 19.4 and 16.8 km/h). The main drawback is cold: mean around 0 °C, as low as -4.9 °C.

Recommendation: Schedule the fireworks later in the evening (around 21:00-22:00, when wind and gusts were lowest in the data), keep it short, and plan warm-up options for guests going outside (coat check access, hot drinks). Keep the indoor fallback (cold sparklers or light show) booked, and have the fireworks provider confirm the go/no-go against the real forecast in the last days before the event.

## Costs
No costs

## Sources
- [Open-Meteo API documentation](https://open-meteo.com/en/docs) - geocoding of Warsaw and historical hourly temperature, precipitation, wind speed and wind gusts (ERA5 archive) for 2023-11-28, 2024-11-28 and 2025-11-28

## Open issues
- This is climatology from only three years, not a forecast. A real forecast for 2026-11-28 becomes available about 16 days before (from 2026-11-12); the weather check should be re-run then.
- The precipitation values do not distinguish rain from snow; snow was not requested separately.
- Coordinates are central Warsaw; the exact suburb of the venue may differ slightly. Re-run with the venue location once it is fixed if needed.
- Wind limits for a safe fireworks launch are set by the licensed provider; their thresholds should be compared with the forecast closer to the date.
