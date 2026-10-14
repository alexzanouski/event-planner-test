# Validation

Owner: validator
Run: 2026-10-13-graduation-warsaw
Status: final
Inputs: requirements.md, venue.md, weather.md, catering.md, program.md, services.md, checklist.md, budget.md

Overall: PASS

## G1 Budget total is within the limit
Result: PASS
Findings: budget.md states Total 14797.33 EUR, Limit 18000 EUR, Remainder 3202.67 EUR, "Within limit: yes". Recomputed from the Costs sections: venue 9039.86 EUR (39600 PLN / 4.3806) + catering 2739.35 EUR (12000 PLN / 4.3806) + program 0.00 EUR + services 684.84 + 445.14 + 1600.47 + 63.96 + 223.71 = 3018.12 EUR, total 14797.33 EUR. This matches the budget. The services "Total services" row was correctly not counted twice. Every PLN to EUR conversion was checked at the NBP rate of 4.3806 and is correct. The PyroTech order of 3 x 1900 = 5700 PLN net is above the 5000 PLN net minimum. Travel: 134 km x 1.70 PLN = 227.80 PLN net, x 1.23 = 280.19 PLN gross.
Note on price risk, not a failure: the largest line (venue, 9039.86 EUR) uses the published wedding starting price "od 330 zł/os.". The pik.warszawa.pl listing confirms an NYE price of 600-700 PLN per person. The non-venue costs total 5757.47 EUR, so the budget stays within 18000 EUR only while the venue's corporate quote is at most about 446.91 PLN per person (12242.53 EUR for 120 guests). At 600 PLN per person the total would be 22193.57 EUR. Unpriced items listed in budget.md (DJ travel, corkage fee, FrameRent delivery and granulate, photographer surcharges, net vs gross for DJ and FrameRent) also come out of the 3202.67 EUR remainder.
Owner: -

## G2 Venue capacity covers the guest count
Result: PASS
Findings: the recommended venue is Hotel Venecia Palace. Its page https://hotelveneciapalace.pl/imprezy-integracyjne/ loads and says "Nasz hotel jest w stanie pomieścić imprezę nawet do 300 osób". 300 >= 120 guests. The halls "możemy dowolnie aranżować", so the stage, tables and dance floor fit.
Owner: -

## G3 Dietary restrictions are covered
Result: PASS
Findings: requirements.md records "Dietary restrictions: None". catering.md Dietary coverage lists "None ... 0 guests with restrictions", so no restriction is left uncovered.
Note on the vegetarian wish, not a restriction: every course has a vegetarian dish. Cold buffet: aubergine rolls, cheese board, caprese, beetroot and gorgonzola salad, roast pumpkin salad. Served main: "Cotoletta z bakłażana", by pre-order. Hot buffet: hot sides, plus a vegetarian hot dish still to be agreed. Sweet and coffee buffets are vegetarian. All 120 guests can reach the buffets, and the served vegetarian mains follow the RSVP pre-order count. All example dishes were checked against the pik.warszawa.pl NYE menu and are listed there, including the "VEGE" item. The soup and the vegetarian hot buffet dish still have to be confirmed with the venue kitchen (catering Open issues, checklist task 12).
Owner: -

## G4 Program fits into the event time window
Result: PASS
Findings: there are 12 slots: 17:00-17:45, 17:45-18:00, 18:00-18:30, 18:30-19:15, 19:15-20:30, 20:30-20:50, 20:50-21:15, 21:15-21:30, 21:30-21:40, 21:40-21:55, 21:55-22:45, 22:45-23:00. Each slot starts when the previous one ends. The first starts at 17:00 and the last ends at 23:00. The durations add up to 360 min. There are no overlaps and no slot outside the 17:00-23:00 window. The rain fallback uses the same slot times. The catering serving plan (17:00-17:45, 19:15-20:30, 21:40-21:55, 21:55-22:45) and the services times (DJ 17:00-23:00, photographer 17:00-22:45, fireworks and fallback 21:30-21:40) are also inside the window.
Owner: -

## G5 Outdoor events have a rain fallback
Result: PASS
Findings: the main event is indoors. The fireworks block (21:15-21:40, palace garden) is outdoors, so the gate applies to it. program.md has a "Rain fallback" section. It sets a go/no-go rule (forecast check at 12:00, provider call on site at 21:00, announcement at 21:15). It replaces the show with a cold-spark show or light show in the main hall at 21:30-21:40. This is the fallback space named in venue.md ("the indoor halls of Hotel Venecia Palace ... in the main hall"). services.md books the indoor alternative: 2 FrameRent cold-spark machines, 223.71 EUR, "bezpieczne do stosowania we wnętrzach" (confirmed on the vendor page), fired in the main hall at 21:30-21:40. The light-show fallback uses the DJ's LED lighting, which is included in the DJ Adam Pokora package.
Notes: (1) The venue has not yet confirmed that cold sparks are allowed indoors (venue, program and services Open issues, checklist task 3). If they are refused, the light show is the fallback. (2) program.md, Rain fallback, Conditions, says the indoor effect comes from the fireworks provider or the DJ/band "so there is no second vendor". services.md instead books FrameRent, a separate vendor. This does not break the gate, but the program wording is now out of date.
Owner: -

## G6 No duplicate vendors or venues
Result: PASS
Findings: one venue is booked: Hotel Venecia Palace, in venue.md. The in-house kitchen in catering.md is the same booking. Its food package is costed only in venue.md, and catering adds only the separate alcohol line (2739.35 EUR), so nothing is double counted. Each vendor is booked in exactly one artifact, all in services.md: DJ Adam Pokora, ZDJECIAEVENTOWE.PL, PyroTech SHOW, FrameRent. Checklist and budget only refer to them as tasks or cost lines and do not book them again. PyroTech's own stage sparks are only an optional alternative quote and are not costed. Pałac w Jabłonnie and Gościniec Maria are backup venues only. No program activity appears twice. The welcome drink and hot drinks appear in both program and catering, but that is the same item: the program gives the time slot and catering supplies the drinks.
Owner: -

## G7 Every recommendation links to a real source page
Result: PASS
Findings: all 27 distinct source URLs were fetched. Every one loaded and matched what it is cited for:
- Hotel Venecia Palace pages: wedding (address, "od 330 zł/os.", min. 30 guests Fri-Sun, "2 dania serwowane + 4 dania w bufetach", "Bufet kawowy", unlimited soft drinks only, welcome sparkling wine, "Salut armatni"), imprezy-integracyjne (up to 300), restauracja (14:00-21:00), kontakt (address, "parking dozorowany").
- pik.warszawa.pl Venecia NYE: garden fireworks, 600/700 PLN, "ALKOHOL – bez ograniczeń", "można wnieść swój własny ulubiony alkohol", every menu item cited by catering.
- Trip.com: free private parking, accessible rooms, wheelchairs, 15-minute drive.
- Pałac w Jabłonnie site, Bridebook and the pik.warszawa.pl Jabłonna NYE 2021 page ("pokazem sztucznych ogni").
- Gościniec Maria: 300 m2, 200 guests, 100 m2 dance floor.
- NBP API: 4.3806, effective 2026-10-13.
- Open-Meteo docs.
- Interia: "50-100 zł za osobę".
- cenauslug.pl: alcohol quantities.
- DJ Adam Pokora: "3000,00 (nagłośnienie,światła) poza sezonem weselnym", season "kwiecień-październik", "do 8 GODZIN GRANIA", "+ dojazd", English +500 PLN.
- ZDJECIAEVENTOWE.PL: "1950 zł brutto", 150 photos.
- PyroTech pages: Bronze 1900 net / 2337 gross per minute, minimum 5000 PLN net, "1,70 zł netto/km (liczone w jedną stronę)", licences, insurance, Warsaw page, cold sparklers indoors with the venue's permission, "nie korzystamy z gotowych cenników".
- conadrogach.pl: 134 km.
- FrameRent: "490,00 zł / doba", indoor-safe, 600 W.
- Gmina Michałowice transport pages: WKD stops, line 61 route, about every 30 min on Saturdays, 5:00-23:00.
- WKD site.
Note: the DJ price list also says "Warszawa poza strefą SCT - dojazd gratis" (wedding terms). This is consistent with services.md, which says travel to Michałowice is not priced.
Owner: -
