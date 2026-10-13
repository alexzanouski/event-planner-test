# Validation

Owner: validator
Run: 2026-10-13-birthday-warsaw
Status: final

Overall: PASS

## G1 Budget total is within the limit
Result: PASS
Findings: budget.md states Total 1740.63 EUR, Limit 2000 EUR, Remainder 259.37 EUR, Within limit: yes. The total recomputed from the Costs sections matches:
- venue: 409.90 EUR
- catering: 524.15 EUR (229.90 + 229.90 + 13.44 + 7.90 + 7.51 + 10.92 + 6.37 + 3.41 + 1.82 deposit + 4.55 + 8.43 + 0.00 staff)
- program: 125.32 EUR
- services: 681.26 EUR
- weather and checklist: 0

Sum: 1740.63 EUR. Every PLN to EUR conversion was rechecked at 4.3889 PLN/EUR (NBP, effective 2026-10-12), including the new deposit line: 16 x 0.50 PLN = 8.00 PLN = 1.82 EUR. The catering PLN subtotal is 2077.00 + 223.48 = 2300.48 PLN, which is correct. Note, not a failure: the venue price is a "from" price and some items have no price yet (tableware, cake, alcohol, kettle or cool boxes). They are listed in the budget Open issues. The 259.37 EUR remainder is the buffer for them.
Owner: -

## G2 Venue capacity covers the guest count
Result: PASS
Findings: Events4U No.2 holds "do 50 osob" (up to 50 people), confirmed on https://www.events4u.pl/. The event has 20 guests, plus the photographer and the animator, which makes 22 people. 50 >= 22.
Owner: -

## G3 Dietary restrictions are covered
Result: PASS
Findings: requirements.md lists vegetarian x3. The Dietary coverage section of catering.md covers it with the full Frykasy y Ananasy vegetarian set for 20 people: 40 vegetarian sandwiches, 30 vegetarian appetizers, 20 tartlets, 2 kg of salads and 20 vegan desserts, plus the fruit platter. That is far more than 3 portions. The set contents match https://frykasyananasy.pl/zestaw-cateringu-wegetarianskiego-dla-20-osob.html. There are labelling and first-serve rules, and the nut and sesame allergens are flagged.
Owner: -

## G4 Program fits into the time window
Result: PASS
Findings: Window 16:00-22:00. Slots: 16:00-16:30, 16:30-16:45, 16:45-17:45, 17:45-19:45, 19:45-20:15, 20:15-21:00, 21:00-21:45, 21:45-21:55, 21:55-22:00. They run back to back with no gaps or overlaps, inside the window. The catering serving plan matches the program (dinner 16:45-17:45, desserts and cake 19:45-20:15). The 15:30-16:00 delivery and setup is host preparation, not a program slot.
Owner: -

## G5 Rain fallback for outdoor events
Result: PASS
Findings: Not applicable. requirements.md confirms an indoor event. The program.md Rain fallback section says "Not needed, indoor event". venue.md matches it ("Fallback space: none needed (indoor event)").
Owner: -

## G6 No duplicate vendors, venues or activities
Result: PASS
Findings: Each vendor is recommended and costed in exactly one artifact:
- Events4U No.2: venue.md
- Frykasy y Ananasy and the shop drinks: catering.md
- Swiat Wrazen: program.md
- TomProPhoto: services.md

The other artifacts only refer to them. Pan Kanapka is the same business as Frykasy y Ananasy (same phone number, 512 100 522) and is cited only as a source. The venue's paid bar service is explicitly not booked, so it is not a second vendor. The 0.00 EUR staff line in catering is not a duplicate. There are no duplicate cost lines in budget.md and no repeated activity in program.md: the 16:30 group photo and the 21:45 final photo are separate moments, and the cake is only at 19:45-20:15.
Owner: -

## G7 Every recommendation links to a real source page
Result: PASS
Findings: All 21 cited URLs loaded on 2026-10-13 and match what they are cited for. The pages are listed in the previous validation run. In this run I fetched again the pages behind the new claims:
- https://www.events4u.pl/ contains "naglosnienie i oswietlenie imprezowe", "bar, lodowka, stoly i podstawowe zaplecze", "sprzatanie po imprezie", "ochrona w cenie", "Na miejscu obecna jest obsluga / ochrona, ktora pomaga zadbac o porzadek" and "na wylacznosc". "profesjonalna obsluga baru" is an optional add-on for 650 zl and is not included, as venue.md, catering.md, services.md and checklist.md say. The page lists no sockets or kettle, and the artifacts correctly mark both as unconfirmed.
- https://zakupy.biedronka.pl/napoje-2/ shows all 7 prices unchanged. It shows "+ kaucja 0,50 zl" on Naleczowianka and Pepsi-Cola only, not on the Tymbark juices or Sprite. That matches the 16-bottle deposit line (12 water + 4 Pepsi). All five drinks are "Chwilowo niedostepny".

Earlier notes, now resolved:
- (1) Fridge: catering.md now uses the confirmed bar fridge ("bar, lodowka") and keeps cool boxes only as a size backup.
- (2) Drinks: catering.md and checklist.md now say all drinks, not just tea and coffee, are unavailable online and are bought in a shop (checklist task 20).

Note, not a failure: the Events4U page does not say which amenities belong to the No.2 hall and which apply to all its halls. Confirm this when booking (checklist task 1).
Owner: -
