# Prioritized Issue List — Member 4

## Purpose
Consolidate important delivery-performance issues and the evidence available in the cleaned dataset.

## Prioritization and definitions
- Segment rates are based on item-level rows unless explicitly labeled distinct orders.
- Provisional on-time definition: `Advance shipping` or `Shipping on time`; eligible denominator includes `Advance shipping`, `Shipping on time`, and `Late delivery`.
- Delay proxy: `Days for shipping (real) - Days for shipment (scheduled)`.
- Carrier ranking, customer-rating analysis, and distance-band analysis are unsupported unless validated fields or a matched source are supplied.
- `Delivery Status = Shipping canceled` and `Order Status = CANCELED` are distinct definitions.
- Segment rankings are descriptive, not proof of cause.
