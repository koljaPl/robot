# Component and delivery review — 2026-10-23

**Procurement stopped: this selected route has €163.63 of priced positions, already
€63.63 above the €100 cap, before remaining required costs. Nothing ordered or
reserved; no supplier messages sent.** This is a route-specific shortfall, not proof
that every possible supplier route costs this much. The full total remains unknown.
Authoritative quantities/prices: [procurement.json](../procurement.json).

## What was resolved

- Six exact Waveshare15024 MG90S remain €21.00 inclVAT at
  [Welectron](https://www.welectron.com/Waveshare-15024-MG90S-Servo_1).
  Listing says short supply; six-unit availability is not established.
- Available **DUPK-40-FF-50**, 40 female/female 50cm leads, replaces unavailable20cm:
  [BerryBase €2.20](https://www.berrybase.de/40pin-jumper-dupont-kabel-female-female-trennbar/laenge-0-50-m).
  Logic only; helper must keep I2C short and validate the completed harness.
- **Goobay11638**, 5.5×2.1mm solder socket, is listed at
  [BerryBase €1.10](https://www.berrybase.de/dc-einbaubuchse-fuer-hohlstecker-5-5x2-1mm-metallausfuehrung-loetanschluss),
  rated5A/30V DC with nut/washer. Replaces unpriced Delock83290 candidate.
  This is a retailer specification, not an electrical test. Insulation/strain relief
  and branch ratings remain helper/bench gates. No servo current through Pico.
- Funduino's **current** [policy](https://funduino.com/policies/shipping-policy)
  confirms standard German DHL **€4.90**, free above€69 after discounts, tracking.
  The browser resolved the previously inaccessible policy; [snapshot](procurement/2026-10-23/funduino-shipping.txt).
- Exact standard M2 ear fastener packs now sourced:100 screws€1.51,
  100nuts€1.13,100washers€0.99; DHL€5.90. Used quantities12/12/24.
  See the linked SKUs in SUMMARY; lengths and clearance remain provisional.
- No USB adapter is in the base basket. USB-A–Micro-B **data cable remains required**;
  only a PC without USB-A needs an additional priced adapter.

## File-specific print prices — actual web calculations, no order

[Quote records/settings/hashes](procurement/2026-10-23/quotes.json).

| Job, qty1 file at100% scale | Parts € | Support removal € | Order fee € | DHL € | Delivered € |
|---|---:|---:|---:|---:|---:|
| Seven PETG parts in compact batch |24.66|11.90|5.95|6.19|**48.70**|
| Two TPU95A sole slabs in batch |7.95|0.00|5.95|6.19|**20.09**|

VAT19% included. Quote from [Meltlab configurator](https://meltlab.de/konfigurator):
PETG black,0.2mm,3walls,25%infill; TPU black,0.2mm,3walls,4top/bottom layers,
15%infill setting (skins fill the1mm slab). Advertised4workingdays production
**after payment**, then DHL1–2workingdays. No delivery date or slot reserved.
Germany selected; no postcode/address entered. Combined-material order fees and
shipping savings are **unconfirmed**; costs conservatively count two jobs.
The seven-individual-file alternative was€78.31; not added to the basket.

`cad/quotation/` contains seven and two disconnected original components, respectively;
these layouts replace individual-file submission, not extra robot parts.
`tools/quote_layout.py` preserves dimensions/volume and records source hashes.
**Layouts are for quotation only:** structural layer orientation and actual fit require
review. Web prices do not cover hole clearing, horn-fit inspection, a sample,
adhesive/sole bonding, or a matched screw kit. TPU grip is not measured.
The original compact-PETG checkout text was recovered from this session transcript
after its temporary tab expired; no batch screenshot. The sole quote has saved DOM
and screenshot.
Final measured files/settings must be re-quoted before purchase.

## Horns and fasteners: do not guess compatibility

Waveshare's [package photograph](https://www.waveshare.com/img/devkit/accBoard/MG90S-Servo/MG90S-Servo-1.jpg)
shows three horn shapes and three screws. Both manufacturer and retailer text list
only one servo. This supports accessory availability, **not exact Welectron-batch
inclusion or a known spline, screw thread, hole pattern or fit**. No generic25T horn
or guessed M2 centre screw is selected. Keep six matched horns/retainers unpriced
until the supplier confirms their inclusion or an exact compatible accessory price.

M2 ear mounting needs12screws,12nuts,24washers. For the proposed3mm printed plate,
0.3mm washers and1.6mm nut, M2×8 leaves2.8mm for ear thickness **before** allowing
thread projection; one0.4mm pitch of projection leaves2.4mm. This is a calculated
fit check, not evidence the real ear is thin enough. Head diameter4mm, washer OD5mm
and nut SW4 also need sweep/access checks. Do not clamp/crush a plastic ear.
The12horn-to-frame screws and12washers are separate from six shaft retainers;
factory horn holes may require a different diameter/thread. Do not drill/tap horns.

## Precise human/supplier actions — drafts, not sent

1. **Welectron, WS8-015024:**
   “Bitte bestätigen Sie6gleiche Waveshare15024 zu je3,50€inklMwSt ab Lager,
   inklusive passender Servohebel und je einer Abtriebs-Befestigungsschraube.
   Welche Verzahnung, Schraubengewinde/-länge und Hebel-Lochmaße sind enthalten?
   Bitte Maßzeichnung für Gehäuse, Befestigungsohren, Wellenmitte und Kabelausgang;
   ist3,3V PWM garantiert?” Confirm exact stock and contents before selecting spares.
2. **Print provider, after measured interface approval:**
   “Bitte Angebot für7PETG-Teile und2TPU95A-Sohlen90×45×1mm gemäß Dateien,
   maßhaltig und montagefertig: Stützen entfernt, Löcher frei, Sohlen verklebt
   inklusive Klebstoff. Bitte Schichtorientierung und Schraubenpassung prüfen;
   separates Muster, Nacharbeit, gemischte Materialien und Versand nach Deutschland
   vollständig ausweisen. Keine Fertigung ohne Freigabe.” Provide final hashes;
   ask for one combined shipment/fee, but do not assume a discount.
3. **Helper:** confirm free labour/consumables or quote them; inspect socket polarity,
   fully insulated low-voltage input and short buses, JR branch fit/gauge/contacts,
   MCU signal levels and short I2C leads. Bench-test current/droop/watchdog/cutoff.
4. **User:** German delivery postcode and PC USB-A availability remain unanswered.
   Final address/payment stays with user. No paid priority/split shipments selected.
   Any bench/sample-first split adds new deliveries; recheck the full budget first.

**Next:** obtain a genuinely cheaper complete frame/sole/finishing route with exact
files (for example a school/local service quote, never assumed free), or explicitly
revise the budget with the user. Current electronics/delivery€85.31 plus ear-fastener
shipment€9.53 leaves only€5.16 for every print, horn, finishing and helper unknown.
Do not recommend the current over-budget basket for ordering; do not weaken servos.
