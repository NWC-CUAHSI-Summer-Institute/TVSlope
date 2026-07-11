
# 4. Results

We evaluate operational OWP HAND flood-inundation maps under five river-slope products (the static satellite
IRIS-SWORD baseline of Chen et al. (2025), three SWOT-derived slopes, and the gauge-derived time-varying S(Q) of
this study) against FIMBench across 6 SWOT-observed reaches spanning the kinematic and backwater regimes.
All maps are forced consistently by the National Water Model: the NWM v3 retrospective discharge for in-retrospective
events and the NWM operational short-range forecast for the two post-retrospective events (Big Sioux 2024,
2,072 m3/s; Ohio 2025, 14,537 m3/s), so no event is driven by a substituted gauge. Every metric is
computed on the river-mask domain (the union of the reach NWM catchments; 6 of 6 reaches;
Section 3), which removes the large, slope-invariant off-channel false-negative term that a whole-benchmark score
imposes. Central tendency is reported as the median, and the slope products are contrasted both across all reaches
and on the paired subset that carries every product, so that no product is credited on an easier set of reaches
(Tables skill_by_treatment_median.csv, skill_by_treatment_fair.csv).

## 4.1 Slope products differ by an order of magnitude and reshape the rating curve

Assigned to the same reach, the five slope products differ by factors of several to roughly thirty (Table
slope_treatments_m_per_m.csv), and the disagreement is largest on the low-gradient dam pool. On the Ohio River
below McAlpine Dam the NWM hydrofabric slope is 9.1×10⁻⁴ m m⁻¹, the satellite-fused IRIS-SWORD slope is
3.6×10⁻⁵ m m⁻¹, and the SWOT-median slope is 1.1×10⁻³ m m⁻¹ over the identical reach. Because the uncalibrated synthetic
rating curve is Manning (Q proportional to the square root of S), this range propagates into conveyance: read at a
common 10 m stage (Table discharge_at_stage10.csv), the implied mainstem discharge on the Ohio spans 5,025
to 27,311 m3/s. The slope choice thus exerts a first-order control on the rating curve.

## 4.2 Flood-extent skill is weakly sensitive to the slope source

That rating-curve sensitivity does not carry through to the mapped extent. Across the scored products the median CSI
on the river-mask domain spans only 0.499 to 0.547 (IRIS-SWORD 0.546; SWOT-median 0.537; SWOT-floodstage 0.547; SWOT-maxWSE 0.542; gauge time-varying S(Q) 0.499; Table skill_by_treatment_median.csv), a
range of about 0.05 CSI, and SWOT-floodstage is highest (0.547). An order-of-magnitude slope range therefore
collapses into a few-hundredths range in flood-extent skill. This decoupling of conveyance sensitivity from extent
sensitivity is the central quantitative result for RQ1: HAND-FIM extent accuracy is only weakly governed by the
slope source, because the square-root Manning dependence compresses the slope range and because the delivered extent
is set by terrain rather than by the rating curve.

## 4.3 The time-varying gauge slope is regime-diagnostic but does not raise skill

A genuinely time-varying slope cannot be recovered from SWOT, whose ~21-day repeat cannot resolve intra-event slope
variation; it is therefore built from paired continuous gauges. The method requires two stations that span the reach
and carry a slope signal above datum noise, a criterion met on 2 reaches: the kinematic Illinois River
(74282100101), whose water-surface slope steepens with discharge (powerlaw fit, R2 = 0.89), and the
backwater Ohio River below McAlpine Dam, whose slope flattens with discharge (quadratic fit, R2 = 0.99;
Fig. sq_relationship). The fitted S(Q) is injected into every hydro-table row by iterating Q = Q0 (S(Q)/S0)^(1/2),
and the resulting FIM is driven by the reach event discharge (NWM retrospective for the in-retrospective Illinois,
NWM forecast for the post-retrospective Ohio). On the paired subset, where every product is scored on the same
2 events, the time-varying slope is statistically indistinguishable from the static products: its median CSI is
0.499, inside the static range 0.491 to 0.510 (full set IRIS-SWORD 0.491; SWOT-median 0.510; SWOT-floodstage 0.496; SWOT-maxWSE 0.509; gauge time-varying S(Q) 0.499; Table
skill_by_treatment_fair.csv). Reach by reach, the time-varying CSI is 0.567 on the Illinois (below its
IRIS-SWORD baseline 0.593 and its best static product IRIS-SWORD 0.593) and 0.431 on the
Ohio (above the low IRIS-SWORD 0.389 but below SWOT-median 0.434). The answer to RQ2 is that the
flow dependence of slope is a strong, physically interpretable signal that reproduces the regime behaviour but does
not translate into higher flood-extent skill.

## 4.4 Hydraulic regime, not the slope product or river size, orders the skill

The controlling variable is hydraulic regime (Table skill_by_regime_median.csv). Kinematic reaches attain a median
CSI of 0.543 to 0.571 across products, whereas backwater reaches attain 0.431 to 0.480; the
regime gap of about 0.09 CSI is several times the within-regime spread between products (a few hundredths on
the kinematic reaches). River size does not order the skill: the most skilful reach is Illinois River
(74282100101, CSI 0.593) and the least skilful is Ohio River (74267300251, CSI 0.389).
The slope source matters most on the low-gradient, dam-controlled backwater reach, where the products diverge most,
yet even there the divergence penalises the physically low satellite slope (the Ohio IRIS-SWORD case carries a FAR
of 0.48, i.e. over-prediction) rather than rewarding it. On kinematic reaches of any size the slope
source is effectively immaterial. This is the answer to RQ3.

# 5. Discussion

## 5.1 Slope source is a second-order control; hydraulic regime is first-order

Across the scored reaches the source of slope, and on the paired reaches even its flow dependence, is a second-order
control on flood extent, whereas the hydraulic regime (whether the HAND normal-flow assumption holds) is
first-order. The median-CSI spread between products is about 0.05, while the kinematic-to-backwater gap is
several times larger. The operational question therefore shifts from "which slope product?" to "is the reach in a
regime that HAND can represent?"

## 5.2 A more accurate slope does not move the extent because HAND geometry is binding

HAND maps a reach discharge to a stage through the rating curve and then inundates every terrain cell below that
stage; slope enters only through the rating curve and cannot change which cells a given stage floods. Where the
dominant error is the terrain-and-geometry mapping (DEM quality, channel-floodplain conflation, or the
single-slope-per-branch assumption), a more accurate or time-varying slope only translates the rating curve without
displacing the extent. A dynamic slope is expected to help only where the rating curve, not the geometry, is the
binding error, a condition not met at these events.

## 5.3 Backwater is the binding failure mode, and a physically correct slope can worsen it

The Ohio below McAlpine Dam is the clearest limit. The kinematic HAND assumption cannot represent dam-controlled
backwater, so skill is low regardless of slope. The physically realistic, very low satellite water-surface slope
(3.6×10⁻⁵ m m⁻¹) is counter-productive: it minimises rating-curve conveyance, raises the modelled stage, and
over-predicts extent (FAR 0.48). Even the S(Q) that reproduces the observed backwater slope almost
perfectly (R2 = 0.99) cannot recover the extent (CSI 0.431). Backwater reaches require a different
model class, such as a diffusive-wave or two-dimensional solver or an explicit backwater correction, rather than a
better slope.

## 5.4 Conveyance sensitivity and extent sensitivity decouple

The two sensitivities are quantitatively distinct. Slope moves rating-curve conveyance by tens of percent to
several-fold (for example, the Ohio range of 5,025 to 27,311 m3/s at 10 m stage), yet leaves
kinematic-reach CSI unchanged to within a few hundredths and moves backwater CSI only modestly, and on the Ohio in
the direction that penalises the lowest slope. Studies that stop at the rating curve therefore overstate the
importance of slope for the delivered flood map; extent must be scored, on a domain the model can actually
influence, to reveal the regime-dependent ceiling.

## 5.5 Evaluation design: a channel-domain metric, consistent NWM forcing, and a fair paired comparison

Three design choices underpin these conclusions. First, metrics are computed on the river mask, the union of the
reach NWM catchments with the benchmark cleaned to its largest connected component; whole-benchmark scoring would
otherwise bury the slope signal under off-channel water (reservoirs, tributaries, urban and pluvial flooding) that a
single-channel HAND SRC cannot reproduce. Second, all events are forced by one NWM family (retrospective, and the
operational short-range forecast for post-2023 events), so recent floods are mapped as an operational system would
map them; on the Ohio the forecast peak (14,537 m3/s) is close to but not identical to the observed gauge, so
the reported skill already embeds forecast rather than perfect discharge. Third, because the gauge time-varying
product exists on fewer reaches than the satellite products, we contrast the treatments both across all reaches and
on the paired subset that carries every product (Ohio River (74267300251), Illinois River (74282100101)). The paired comparison is decisive: on the same 2
events every product, including the gauge time-varying slope, falls within a 0.02 CSI band (0.491 to
0.510 for the static products, 0.499 for the time-varying), so the lower all-reach median of the gauge
product reflects its restriction to the more demanding reaches rather than an intrinsic deficit.

## 5.6 Limitations and outlook

The study spans 6 reaches with heterogeneous benchmarks (high-water marks, SAR, and sub-metre optical or
PlanetScope imagery), each scored at full benchmark resolution on the river-mask domain. HAND uses a single slope
per branch, and the time-varying method was exercised on the 2 reaches whose paired gauges yield a
signal-bearing S(Q). A third candidate, the Nodaway River (74293400041, Tier-3 SAR benchmark), was tested and
rejected: its paired stations return a flat, datum-dominated S(Q) (R2 = 0.07), the same failure mode that excludes
strongly backwater or short reaches, so it cannot support a defensible time-varying demonstration. The
out-of-retrospective FIMs additionally carry forecast rather than observed discharge uncertainty. Future work should
(i) enlarge the per-regime and paired-gauge samples to test the CSI ceilings statistically, (ii) assimilate SWOT
water-surface elevation directly rather than only its slope, (iii) couple a backwater or two-dimensional solver for
dam- and tide-controlled reaches, and (iv) propagate slope and forecast-discharge uncertainty into the mapped extent
so that operational FIM can carry calibrated confidence bounds.
