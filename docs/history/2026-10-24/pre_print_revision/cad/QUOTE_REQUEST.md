# Historical commercial-quotation brief — not a default order

Archived route context2026-10-23. User now compares standard stock mechanics vs
own printing; no commercial print inquiry/order is planned. See
[FRAME_ROUTES](../docs/FRAME_ROUTES.md). Original quotation requirements below
are retained for reference.

Updated2026-10-23. File-specific web calculations exist; no order or supplier
inquiry sent. Current route is over budget. [Evidence](../docs/PROCUREMENT_ACTIONS.md).

Supply **7PETG frames**: torso×1, left/right thigh×1each, shin×1each, foot×1each;
plus **2TPU95A soles90×45×1mm**. Price each part exactly once. Choose either
individual `stl/` files or the corresponding batch files in `quotation/`, never
both. Ignore old `quotation_plate.stl`: it is not an additional part or a print layout.
Batch files have7/2disconnected bodies, scale100%, mm. Layout/source hashes are
in `quotation/layout.json`; these orientations need structural review.

PETG:0.2mm layers,3walls,nominal25%infill, stiff joint mounts. TPU:0.2mm layers,
3walls,4top/bottom skins; flat1mm soles. Include support removal, clear through
holes without student drilling/tapping, bonded soles and adhesive, fit inspection,
matching fasteners, VAT and German delivery. Quote any fit sample and its delivery
separately; confirm whether both materials can share order/shipping fees.

Fasteners needed:12ear screws (provisionallyM2×8),12M2nuts,24M2washers;
6matching servo horns/retainers (supplier inclusion unresolved);12horn-to-frame
screws and12matching washers with thread/length matched to factory horn holes.
[Assembly schedule](ASSEMBLY.md). Do not substitute a guessed spline/thread.

Servo: exact Waveshare15024MG90S. Final manufacture requires actual horn, shaft,
ear and lead-exit measurements and one fit sample. Review layers for ear loads,
clear moving screw sweeps and board/cable access. Quote final hash-identified files
again after fit revisions. No approved clearances or layer strength are implied.

Observed Meltlab prices: compact7PETG€48.70, separate2TPU€20.09inclVAT/delivery;
printing/PETG support removal only. Hole finishing, bonding, sample and hardware
were NOT quoted. [Full settings/breakdown](../docs/procurement/2026-10-23/quotes.json).
The current priced route totals€163.63before remaining required costs, so procurement
is stopped under the€100cap. A cheaper fully sourced delivered route is needed.
