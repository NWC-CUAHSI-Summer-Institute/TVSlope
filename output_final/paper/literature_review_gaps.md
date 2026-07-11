# Literature review, research gaps, and solutions implemented

*Companion to `code/work6_3DHRS.ipynb` (the 13-step time-varying-slope → HAND-FIM study). Papers reviewed are in
`paper/`; machine-readable conversions are in `output_final/paper/md/`.*

---

## 1. What the literature establishes

### 1.1 Channel slope is a first-order, badly-biased control on HAND-FIM
- **Chen et al. (2025, *Scientific Data*) — HF/IRIS FIM benchmark.** Establishes that the operational OWP
  hydrofabric channel slope is severely biased at reach scale (**median error ≈ 76 % ± 168 %** vs surveyed
  slopes) and that replacing it with a static satellite slope measurably improves flood-map skill: the
  IRIS/ICESat-2 product raises mean **CSI by ≈ 31 % ± 25 %**, and a static SWOT-derived slope by ≈ 12 %. This is
  the paper that motivates slope substitution and supplies the **IRIS-SWORD** baseline used here.
- **Aristizabal et al. (2024) — DEM controls on HAND-FIM.** Ranks channel slope among the strongest DEM-derived
  controls on HAND-FIM error, with a **negative CSI sensitivity to slope** (a steeper injected slope drains the
  Manning SRC and shrinks the extent). Confirms the sign and magnitude of the conveyance effect we exploit.

### 1.2 Water-surface slope is observable and physically meaningful — but regime-dependent
- **Bauer-Gottwein et al. (2024) — time-variable water-surface slope.** Shows the water-surface slope (WSS) is
  temporally **more stable and more physically meaningful than stage alone**, and can be tracked through time
  from paired water-surface observations. Direct support for a *time-varying* slope treatment.
- **Liu et al. (2023, 2026) — stage / slope / discharge & SWOT gauge-independent discharge.** Demonstrate the
  stage–slope–discharge coupling and that in **backwater** the convenient assumption *water-surface slope ≈
  energy/friction slope* breaks down, so a single static slope misrepresents conveyance where downstream control
  dominates. This is the physical basis for our kinematic-vs-backwater stratification.
- **Jiang et al. (2025) — SWOT river slope (Missouri).** Confirms SWOT can retrieve reach water-surface slope but
  that per-overpass slope is **sparse (multi-day revisit) and noisy at reach scale** — i.e. SWOT alone does not
  yield a continuous rating.

### 1.3 Supporting infrastructure
- **Altenau et al. (2021) — SWORD.** The reach/node river database that defines our SWOT reaches and centerlines.
- **Andreadis et al. (2025) — SWOT discharge; SWOT ATBD / WSE filtering.** Space-based WSE and discharge context
  and the pixel-cloud/WSE quality background.
- **Anupal (2025) — FIMServe; Frame et al. (2024) — rapid inundation from NWM + satellite.** The HAND-FIM
  serving/rapid-mapping context our FIMbox runs sit within.
- **Cohen et al. (2025), Dipsikha (2026) — FIM evaluation.** The CSI/POD/FAR/F1 contingency framework and
  benchmark-comparison methodology we adopt (FIMBench scoring).

---

## 2. The gap

Every operational slope product above — hydrofabric, IRIS/ICESat-2, static SWOT — is **static**: one slope per
reach. Yet Manning conveyance ($Q \propto \sqrt{S}$) makes the *correct* slope **flow-dependent**: it **steepens
with discharge on kinematic reaches and flattens on backwater reaches** (the loop rating of unsteady
open-channel flow). Consequences unaddressed in the literature:

1. **No continuous, flow-dependent $S(Q)$ is injected into the operational HAND SRC** and scored against
   observed-flood benchmarks. SWOT's time-varying slope is real but overpass-sparse and reach-noisy (Jiang 2025),
   so it does not by itself provide a continuous rating.
2. **Slope-substitution skill is reported as a reach-average**, not resolved by hydraulic regime — even though
   theory (Liu 2023/2026; Bauer 2024) predicts the static-slope error is largest exactly where the slope varies
   most with flow (backwater).
3. **Evaluation is bounded by the NWM retrospective** (Chen 2025), excluding recent large floods (e.g. 2025) for
   which no NWM-retrospective discharge exists.

---

## 3. Solutions implemented in this study

| Gap | Solution (notebook step) |
|---|---|
| No continuous flow-dependent slope | **Gauge time-varying $S(Q)$** — paired-station WSS as a function of on-reach discharge, fit non-linearly and injected per hydro-table row by iteratively solving $Q=Q_0\sqrt{S(Q)/S_0}$ (Steps 6–8). |
| Regime not resolved | **Regime stratification** — each reach classed kinematic vs backwater from $\rho(\text{slope},\text{stage})$; skill reported per regime (Steps 7, 12–13). |
| NWM-retrospective bound | **Gauge-driven FIM** — the 2025 Ohio flood is mapped from on-reach gauge discharge, extending scoring past the retrospective (Steps 8–9). |
| Big-river stage is IV-only | **IV→daily aggregation** — `per_reach3` falls back to daily-averaged instantaneous stage/discharge when the daily service is empty (enables large-river gauges). |
| Whole-tile scoring dilutes skill | **Reach-corridor evaluation area** — CSI/POD/FAR/F1 are scored inside a corridor buffered along the reach (∩ FIMBench), not the whole benchmark tile, so no scored pixel falls away from the reach (Steps 5, 11). |

### 3.1 Where the new method is demonstrated
The time-varying gauge $S(Q)$ is demonstrated on the two **gauge-paired** reaches with a strong, real $S(Q)$
signal, one per regime:

| Reach | River | Regime | $S(Q)$ fit |
|---|---|---|---|
| 74282100101 | Illinois | kinematic ($\rho>0$, $S$ rises with $Q$) | power-law, **R² = 0.89** |
| 74267300251 | Ohio (below McAlpine Dam) | backwater ($\rho<0$, $S$ falls with $Q$) | quadratic, **R² = 0.99** |

### 3.2 Method-limit findings (honest negatives)
Two reaches were tested for gauge pairing and **set aside**, which is itself a result about the method's domain:
- **Neches 75120400053** — the only working twin gauges (08040600 / 08041000) are **48.7 km apart**, far longer
  than the SWOT reach, so the paired "slope" is not a reach property. Kept as a static/SWOT-scored reach.
- **Mississippi at Thebes 74270100061** — even after IV→daily aggregation, the twin-gauge slope is **flat and
  datum-dominated** ($R^2\approx0.08$, $\rho\approx0$): on this very low-gradient reach the water-surface slope
  does not track discharge, so a gauge $S(Q)$ carries no information. Kept as a static/SWOT-scored backwater reach.

**Takeaway for the method's applicability:** the gauge time-varying $S(Q)$ needs (i) two stage gauges spanning a
distance comparable to the reach, with (ii) a slope signal large relative to datum/observation error — i.e.
moderate-gradient reaches. On very low-gradient large rivers the twin-gauge slope is dominated by datum
uncertainty and the method degenerates to the static case.

---

## 4. Open items / future work
- Replace absolute-datum WSS with a self-consistent SWOT WSE slope on low-gradient reaches (removes the datum
  floor that defeats the Mississippi case).
- Extend the gauge $S(Q)$ to more out-of-retrospective events via gauge-driven FIM.
- Blend SWOT (spatially dense, temporally sparse) with gauge $S(Q)$ (temporally dense, spatially two-point) into
  a single continuous slope field.
