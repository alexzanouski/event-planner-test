# Validation

Owner: validator
Run: 2026-10-13-corporate-krakow
Status: final

Overall: PASS

## G1 Budget total is within the limit
Result: PASS
Findings: budget.md states Total 1523.99 EUR, Limit 2500 EUR, Remainder 976.01 EUR, "Within limit: yes". Recomputed from the Costs sections: venue 0 EUR + catering (472.08 + 451.99 + 462.04 = 1386.11 EUR) + program 0 EUR + services (43.37 + 10.27 + 84.24 + 0 = 137.88 EUR) + weather/checklist "No costs" = 1523.99 EUR, which matches budget.md exactly. PLN-to-EUR conversions were re-checked at the NBP rate of 4.3806 (confirmed on api.nbp.pl, effectiveDate 2026-10-13): 2068.00 / 1980.00 / 2024.00 / 190.00 / 45.00 / 369.00 PLN give 472.08 / 451.99 / 462.04 / 43.37 / 10.27 / 84.24 EUR. No line is counted twice. Note: the unpriced items listed in budget Open issues (delivery/installation, the 500 PLN deposit if it is not deducted, the garland per-day vs per-event question, a possible larger sound set, a hot dish) are not in the total. With 976.01 EUR headroom, they are unlikely to break the limit, but the budget has to be re-checked once they are quoted.
Owner: -

## G2 Venue capacity covers the guest count
Result: PASS
Findings: Recommended venue Restauracja Dworek, restaurant hall "48 miejsc siedzacych" (48 seats) >= 40 guests. 40 guests also meets the 35-person minimum for exclusive use. The rain fallback is the same 48-seat hall, so capacity also holds in the rain case.
Owner: -

## G3 Dietary restrictions are covered
Result: PASS
Findings: Requirements: vegetarian x5, vegan x2. catering.md Dietary coverage: Vegetarian (5) is covered by the whole Bufet wegetarianski plus Salatka Szopska and Caprese. Vegan (2) is covered by guacamole with tortilla and red beans, tortilla with avocado, lentil salad with goat cheese on the side, and dairy-free focaccia/bread. The vegetarian buffet is ordered for 40 persons and 2 labelled vegan plates are set aside at 18:45, so portions are sufficient. Note: the vegan status of the tortillas, bread and focaccia, and the goat-cheese swap, are "to be confirmed" with the restaurant by 2026-11-07 (checklist task 11). Guacamole with red beans stays vegan even without the swaps, so coverage does not depend on them alone.
Owner: -

## G4 Program fits into the time window
Result: PASS
Findings: Checked 10 slots against the user's 18:00-23:00 window: 18:00-18:20, 18:20-18:30, 18:30-18:45, 18:45-19:45, 19:45-20:30, 20:30-20:50, 20:50-21:00, 21:00-22:30, 22:30-22:45, 22:45-23:00. All slots are inside the window and contiguous, with no overlaps or gaps, and each stated duration matches its times. The catering serving plan (18:00-23:00) and service use times (18:00-23:00) also stay inside the window. Set-up 16:30-18:00 is before the event and is not a program slot.
Venue-hours dependency (note, not a fail): the offer PDF gives 12:00-21:00 and the homepage gives "Sobota: 12:00 - 22:00" (verified on restauracjadworek.com). The slots 21:00-22:30, 22:30-22:45 and 22:45-23:00 therefore depend on the restaurant agreeing to stay open until 23:00. venue.md Open issues advised not planning past 22:00 until this is confirmed. The coordinator says the user chose the full window. program.md, catering.md, services.md and checklist.md all record this, and checklist task 1 (deadline 2026-10-14) makes written confirmation of the 23:00 end the first organiser task. If the restaurant refuses, the program planner must shorten the slots from 21:00 onwards and G4 must be re-checked against the confirmed end time.
Owner: -

## G5 Outdoor events have a rain fallback
Result: PASS
Findings: The event is "either, outdoor preferred" and has an outdoor welcome from 18:00 to 18:20 in the manor park, so G5 applies. program.md has a concrete Rain fallback section: a go/no-go check at 17:30 (rain/snow, feels-like below 0 °C, or wind above about 25 km/h). If it is a no-go, the welcome moves to the indoor Restauracja Dworek restaurant hall (48 seats, ul. Papiernicza 2). This is exactly the "Fallback space" named in venue.md. Times are unchanged and no slot is cancelled. checklist task 18 matches the same rule.
Owner: -

## G6 No duplicate vendors, venues or activities
Result: PASS
Findings: Interpretation used: no venue or vendor is booked or costed by more than one planning artifact for the same role. Cross-references in checklist and budget, and alternatives that were not chosen, are not duplicates. Bookings: venue Restauracja Dworek (venue.md, 0 EUR). Caterer Restauracja Dworek in-house kitchen (catering.md), which is the venue's mandatory in-house catering ("Catering wewnetrzny") and one booking with the venue, not a second venue. Sound by WynajemGlosnikow.pl and decor garland by Sprzet Eventowy (services.md only). The services row "Restauracja Dworek standard table setting" is 0 EUR and is explicitly part of the venue offer, so nothing is booked or paid twice. Services rejected the Dworek cultural centre sound equipment to avoid a duplicate. PURO, COCO Club and Creative Grapes appear only as alternatives in one artifact each. Activities: the 10 program slots are all distinct. The welcome drinks and coffee/tea round appear in both program.md and catering.md, but these are the same slots cross-referenced, not listed twice.
Owner: -

## G7 Every recommendation links to a real source page
Result: PASS
Findings: All 19 distinct source URLs use https and were fetched:
- restauracjadworek.com homepage: address, +48 798 641 805, kontakt@restauracjadworek.com and "Sobota: 12:00 - 22:00" confirmed.
- Bridebook listing: indoor up to 120, park 300+, minimum 20 guests, "wygodny parking", "Catering wewnetrzny" confirmed.
- dworek.eu/wynajem: banquet and outdoor event hire, mobile stage and technical equipment, contact Anna Radwanek and the two price list downloads confirmed.
- dworek.eu/deklaracja-dostepnosci: stair platforms, automatic doors, accessible toilets and 1 disabled space at Dworek Bialopradnicki confirmed.
- dworek.eu/kontakt: trams 5, 7, 18 to Bialopradnicka, tram 7 from Dworzec Glowny Tunel, Mackiewicza "5 min pieszo", buses 105/132/405 and then 137/138/169/172, about 22 min walk, 13 min from Krowodrza Gorka, staff-only car park, public car park at Zajazd Kosciuszkowski ul. Bialopradnicka 3 and bike racks confirmed. One fetch summary also mentioned tram lines 50 and 75, so the page lists more lines than the checklist cites. This is not a conflict.
- thetimey.com tram 18: Bialopradnicka between Pachonskiego P+R and Gornickiego, Teatr Bagatela and Stary Kleparz confirmed.
- purohotels.com: Halicka 14a, garden up to 350 with electric heaters, Glass 70, Enamel 50, no price confirmed.
- cococlub.pl: Szpitalna 38, 20-70 partial, 100 minimum exclusive, 100 PLN per person minimum spend, sound/lighting/LED confirmed.
- api.nbp.pl: 4.3806 on 2026-10-13 confirmed.
- open-meteo.com docs and historical-weather-api: forecast/geocoding docs and hourly temperature/apparent temperature/precipitation/wind confirmed.
- wynajemglosnikow.pl: ul. Cystersow 9, contact, "1x Yamaha Stagepass 300 (dwa glosniki oraz powermikser)" 190 PLN gross, AKG WMS 40 45 PLN gross/24 h, Sunday-to-Monday day not charged, returns Mon-Fri 08:00-20:00 and Saturdays confirmed.
- sprzeteventowy.pl Girlanda 25mb: 25 m, bulb every 1.0 m, 230 V, 40 W, indoor and outdoor use, 300.00 net / 369.00 gross confirmed.
- sprzeteventowy.pl Multimedia i oswietlenie: Sp. z o.o., ul. Wladyslawa Lokietka 177, 31-263 Krakow, phone and email confirmed.
- sprzeteventowy.pl Dekoracje i dodatki: KOC DEKORACYJNY 10.00 net / 12.30 gross confirmed.
- sprzeteventowy.pl Jak zamawiac: quoted step confirmed, no transport price published.
- creativegrapes.pl: 200 PLN gross/24 h, one portable speaker with built-in amplifier and a Sennheiser e935 mic, small room up to 100 m2, Jozefinska 31a/19 confirmed.
Not machine-verifiable (note, not a fail, per the coordinator's instruction):
- https://restauracjadworek.com/wp-content/uploads/2025/01/oferta-dworek3.pdf loads (application/pdf, 962.5 KB, an Illustrator-produced single-page offer "oferta dworek3"). WebFetch could not extract its text, and local PDF rendering is unavailable here because pdftoppm is not installed. These claims could therefore not be independently verified: 48 seats, the min 35 guests / 9000 zl rule, 10% service, 500 zl deposit, 12:00-21:00 hours, the Bufet 2 47.00 / Bufet wegetarianski 45.00 / Bufet slodkosci 41.00 / drinks 46.00 / Zestaw 195.00 zl prices, corkage 50 zl, cake fee 7 zl, table setting and tablecloth 30 zl. The coordinator reports they were checked by reading the file locally. Note that the selected catering prices (1386.11 EUR, 55% of the budget) and the G2 capacity figure rest only on this PDF.
- https://dworek.eu/wp-content/uploads/2026/07/01.09.2026-cennik.docx loads (DOCX, 16.8 KB) but could not be parsed. It is only cited for a rejected alternative (sound 300.00 zl, microphone 50.00 zl), so it does not affect any recommendation.
Owner: -
