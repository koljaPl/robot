# Procurement check record — 2026-10-23

Scope: component selection, exact printing calculations, mounting hardware and
German delivery plan. No procurement, supplier messages, address entry, physical
assembly/test or manufacturing release.

- Rechecked exact Welectron WS8-015024 listing: €3.50 incl19%VAT, short supply,
  1–3workingdays; six-unit stock not confirmed. Package text lists one servo only.
  Waveshare's package-tab image shows three horn shapes/three screws; dimensions,
  batch inclusion and screw threads remain unknown. Saved photograph for review.
- BerryBase selected DUPK-40-FF-50: €2.20 inclVAT,60shown,1–3days.20cm unavailable.
  Goobay11638:€1.10 inclVAT,100+shown; exact listing specifies5A/30VDC,5.5×2.1mm,
  nut/washer and solder lugs. Both remain subject to harness/bench verification.
- Funduino WebMCP read-only exact product lookup confirms available
  F23107397 MPU6050 €3.62 and F23108007 10cm extension €1.14. No cart mutation.
  Browser-opened current policy confirms standard Germany DHL€4.90 with tracking.
- Three Schraubenking ear-fastener packs: P010265€1.51/100,
  P003474€1.13/100, P004198€0.99/100; German DHL€5.90.
  Nut price directly verified in browser because indexed page was stale.
  Installation needs12/12/24, not100each. Horn fasteners remain separate/unpriced.
- Meltlab exact uploaded STL quotations recorded in quotes.json. PETG compact batch
  €48.70: original checkout text recovered from this session transcript after tab
  expired; saved as meltlab-petg-batch.txt, no batch screenshot.
  TPU two-component batch €20.09 with DOM/screenshot. No sample/bonding/hole finishing
  or full hardware kit quoted. No supplier acceptance of fit. Non-binding web prices.
- USB adapter omitted unless PC lacksUSB-A. A USB-A–Micro-B data cable is still listed.

Locally executed after edits:

- `python tools/quote_layout.py`:7disconnected frames, unchanged total volume;
  bounding boxes185×167×38.25mm;2disconnected soles185×45×1mm, no frame redesign.
- Quotation-file SHA256s match quotes.json; component source hashes recorded.
  Per-job arithmetic checked, including VAT-inclusive fees and separate shipping.
- `python tools/budget_gate.py`: expected exit1, OVER BUDGET, known€163.63,
  route shortfall€63.63, full totalnull, purchase_clearedfalse.
- `python -m pytest -q`: **29passed in8.01s**.
- Current model/control SHA256 remains
  `3d93f768188c8c55c903658192be75b87124f9a62852720fb5d2fd5b54666a8a`.

Remaining human evidence: postcode/USB-A availability, six exact servos with matched
horns/retainers, actual interfaces and safe M2 stack, cheaper delivered manufacturing
route including finishing/adhesive/sample, helper charge and JR branch/current tests.
No physical parameter or control calibration was inferred from shopping research.
