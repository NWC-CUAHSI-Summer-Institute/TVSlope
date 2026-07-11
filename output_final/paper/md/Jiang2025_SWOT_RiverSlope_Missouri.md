RESEARCH LETTER
10.1029/2025GL115953

Special Collection:
Science from the Surface Water
and Ocean Topography Satellite
Mission

Key Points:
• SWOT resolved finer river slopes

unobservable by the traditional sparse
gauge network

• High spatio‐temporal SWOT observa-

tions captured flood evolution
processes

• SWOT daily observations revealed

slope dynamics and backwater effects
at the Missouri‐Yellowstone
confluence

Supporting Information:

Supporting Information may be found in
the online version of this article.

Correspondence to:

L. Jiang,
jianglg@sustech.edu.cn

Citation:

Jiang, L., Nielsen, K., Andersen, O. B., &
Liu, J. (2025). SWOT reveals detailed
dynamics of longitudinal river slope in the
Missouri River basin. Geophysical
Research Letters, 52, e2025GL115953.
https://doi.org/10.1029/2025GL115953

Received 14 MAR 2025
Accepted 4 JUL 2025

Author Contributions:

Conceptualization: Liguang Jiang
Data curation: Liguang Jiang
Formal analysis: Liguang Jiang
Funding acquisition: Liguang Jiang
Investigation: Liguang Jiang
Methodology: Liguang Jiang
Project administration: Liguang Jiang
Resources: Liguang Jiang
Software: Liguang Jiang
Validation: Liguang Jiang
Visualization: Liguang Jiang
Writing – original draft: Liguang Jiang

© 2025 The Author(s).
This is an open access article under the
terms of the Creative Commons
Attribution‐NonCommercial License,
which permits use, distribution and
reproduction in any medium, provided the
original work is properly cited and is not
used for commercial purposes.

JIANG ET AL.

SWOT Reveals Detailed Dynamics of Longitudinal River
Slope in the Missouri River Basin
Liguang Jiang1

, Karina Nielsen2, Ole B. Andersen2

, and Junguo Liu3,4

1School of Environmental Science and Engineering, Southern University of Science and Technology (SUSTech),
Shenzhen, China, 2National Space Institute, Technical University of Denmark (DTU), Kgs. Lyngby, Denmark, 3Yellow River
Research Institute, North China University of Water Resources and Electric Power (NCWU), Zhengzhou, China, 4Henan
Provincial Key Laboratory of Hydrosphere and Watershed Water Security, North China University of Water Resources and
Electric Power (NCWU), Zhengzhou, China

Abstract River water surface slope (WSS) is a crucial variable for a wide range of studies in hydrology,
hydraulics, and morphology. However, current in situ and remote sensing methods have limitations in
characterizing the WSS of global river systems. Here, we present an exploration of SWOT satellite data for
studying WSS and longitudinal profiles in the Missouri River basin. Using 1‐day repeat data over 3 months, our
results show that SWOT not only captured temporal variations in reach‐scale WSS, but also resolved sub‐reach
local variations in WSS, revealing the intricate non‐uniform and unsteady nature of river flows. Such finer local
WSS revealed slow flood wave propagation in the James River due to its low gradient. Moreover, the
longitudinal profiles from SWOT revealed significant backwater effects at the confluence of the Missouri and
Yellowstone rivers. This study offers new insights into river WSS dynamics, suggesting the great potential of
SWOT for river science.

Plain Language Summary The water level fluctuation and slope of a river affect many of its
behaviors, such as how quickly the flow is moving through the river channel, how much sediment and water the
river can carry, and how the riverbed may erode. However, existing in situ and remote sensing methods for
measuring river water level and associated slope have many limitations that prohibit a comprehensive
understanding of global‐scale river surface dynamics, let alone their complicated processes. The new
observations from SWOT might pave the way for a better understanding of river water level and slope
dynamics. This study exploits the 1‐day repeat SWOT observations during its fast‐sampling phase to unveil the
spatio‐temporal variations in river water level and slope.

1. Introduction

Rivers are key components of the Earth system, sustaining all kinds of life. Understanding river hydraulics is
crucial for addressing many water‐related problems and phenomena (De Bartolo, 2022). River water level, or
water surface elevation (WSE), is a critical state variable for characterizing river hydraulics. Based on WSE, the
river water surface slope (WSS), defined as the ratio of water surface elevation drop to horizontal distance, can be
calculated. WSS is an important controlling variable for various hydrodynamic and morphodynamic processes,
including flood routing, sediment transport, stream habitat development, and bed roughness (Ferguson, 2012;
Palucis & Lamb, 2017). Furthermore, understanding WSS helps explain how and why rivers have evolved the
way they did and inform strategies for river restoration (Han & Endreny, 2014; Jiang, Bandini, et al., 2020).
Additionally, WSS is a key variable for estimating river discharge from space, alongside other complementary
variables (Durand et al., 2016).

Spaceborne observations of WSE have been widely used for various hydrological purposes (Abdalla et al., 2021).
For instance, WSE data derived from CryoSat‐2 has provided valuable insights into how lakes responded to
climate change in remote areas (Jiang, Nielsen, Andersen, et al., 2020). Similarly, monitoring reservoir WSEs has
proven instrumental in assessing reservoir filling status and drought resilience (Wang et al., 2024). In addition,
such observations have enhanced our understandings of river level variations through the calculation of WSE
fluctuations (Zhao et al., 2023). Despite these advancements, traditional nadir radar altimetry is limited in its
ability to directly measure river WSS, primarily because satellite ground tracks are not always aligned with river
courses. By applying sophisticated statistical models, it is possible to derive WSS using multiple altimetry
measurements over most large rivers (Jiang et al., 2024; Nielsen et al., 2022). At broader scales, digital elevation

1 of 10

Writing – review & editing:
Liguang Jiang, Karina Nielsen, Ole
B. Andersen, Junguo Liu

Geophysical Research Letters

10.1029/2025GL115953

models (DEMs), such as SRTM DEM, offer static snapshots of river WSE and have been used as proxies to
approximate WSS (Rodríguez et al., 2020). Notably, Cohen et al. (2018) built a static 15 arc‐sec global river slope
database based on the HydroSHEDS and the ETOPO DEM, providing a first‐of‐its‐kind insight into the global
distribution of river slopes. However, the accuracy of WSS estimates for smaller rivers, particularly those nar-
rower than 460 m, remains inadequate due to the inherent constraints of DEMs. Moreover, the asynchronous
nature of WSE measurements across different locations poses a significant challenge in achieving precise and
consistent results. Until the advent of the Surface Water and Ocean Topography (SWOT) mission, ICESat‐2 laser
altimetry was the most reliable spaceborne method for accurately determining WSS. By simultaneously
measuring WSE at six different locations, ICESat‐2 achieved a median absolute error of 2.3 cm/km in WSS
calculations (Scherer et al., 2022). Nonetheless, the spatial coverage and temporal resolution of ICESat‐2 are
insufficient to comprehensively capture WSS characteristics across large scales.

Monitoring river WSS poses significant challenges. Unlike channel bed slopes, which are often assumed to be
stationary over short periods, WSS is highly dynamic due to the interaction between gravitational forces and
frictional resistance. For instance, variations in vegetation growth can lead to substantial differences in WSS both
temporally and spatially, as evidenced in Danish streams (Jiang, Bandini, et al., 2020; Liu et al., 2022). These
dynamic characteristics are not yet well understood, particularly at larger scales, due in part to the inherent
difficulties in predicting and observing river hydrodynamics. Even in regions with relatively dense gauge net-
works, such as North America, the distance between adjacent gauges is often tens of kilometers or more.
Consequently, the slope determined by the twin‐gauge approach represents only the slope between the two points
(gauges) and may not accurately reflect the average slope of the specific river reach (Altenau et al., 2017). For
instance, features such as backwaters, slope breaks, and other hydraulic phenomena occurring between gauges
remain undetected (Pitcher et al., 2019). This limitation also applies to measurements from ICESat‐2 (Scherer
et al., 2022). To address these challenges, WSE data at higher spatio‐temporal resolution is essential to capture
local features and dynamics of WSS.

The SWOT mission, launched in December 2022, is a groundbreaking wide‐swath altimetry satellite designed to
simultaneously measure river stage, width, and slope for the first time (Fu et al., 2024). This capability introduces
unprecedented opportunities for advancing our understanding of WSS dynamics. However, the full potential of
SWOT observations in this context remains largely unexplored. Critical questions arise: How effective are SWOT
observations in characterizing the spatio‐temporal dynamics of river WSS? Can SWOT data capture detailed river
longitudinal profiles? To address these key issues, this study utilizes actual SWOT observations to investigate the
spatio‐temporal variability of river WSS in the Upper Missouri River basin.

2. Materials and Methods

2.1. Study Area

In this study, we focused on rivers in the Missouri River basin (Figure 1), where the 1‐day SWOT data and dense
gauging network are openly available. The Missouri River stretches over 3,700 km from its headwater tributaries
in the Rocky Mountains to its confluence with the Mississippi River at St. Louis (Frederick & Woodhouse, 2020).
The studied tributaries include the Yellowstone, Little Missouri, Cheyenne, White, Niobrara, James, Platte, and
Republican rivers, among which the confluence of the upper Missouri and Yellowstone (the largest tributary by
discharge) is of particular interest due to their interactions. The upper Missouri is largely regulated by the Fort
Peck Lake (Capacity: 18.7 MAF), while the Yellowstone is free‐flowing. The upper portion (upstream the
confluence) of the basin is driven largely by snowmelt during March and June, while the lower portion is pri-
marily driven by later spring precipitation (Wise et al., 2018).

2.2. Data

SWOT products are available in several types, such as high rate point cloud of water mask pixels (HR_PIXC), and
high rate river single pass vector (HR_RiverSP). In this study, we employed the L2_HR_RiverSP product. The
L2_HR_RiverSP product (v2.0) (SWOT, 2024) specifically provides WSE observations for nodes, with a spacing
of approximately 200 m. In this study, we only considered the data collected during the fast‐sampling phase, that
is, 30 March to 10 July 2023. Gauging river stage records were from the National Water Information System
(NWIS) (U.S. Geological Survey, 2025). See Tables S2 and S3 in Supporting Information S1 for details about
gauges and river reaches.

JIANG ET AL.

2 of 10

Geophysical Research Letters

10.1029/2025GL115953

Figure 1. Geographic map of the Missouri River Basin and assessments of WSE and WSS. (a) The Missouri River network and major lakes along the main Missouri are
shown. USGS stream gauges within SWOT coverage are indicated with green dots; the major lakes (reservoirs) are also labeled. Please refer to Table S1 in Supporting
Information S1 for detailed information about gauges. (b) Assessment accuracy of SWOT WSE against USGS in situ data in terms of unbiased root‐mean‐squared error
(ubRMSE) at 39 stations. Left‐corner box plot shows the dispersion of ubRMSE. (c) Assessment accuracy of SWOT WSS against USGS in situ data in terms of RMSE
at 16 reaches.

2.3. SWOT WSE Processing

The node shapefile product contains several outputs that describe the nature of the pixel‐to‐node aggregation
and relate to the accuracy of the data, including the distance from nadir track (xtrk_dist), fractional area of dark
water (dark_frac), a priori WSE (p_wse), uncertainty in WSE (wse_u), node quality indicator (node_q flag)
(JPL‐D‐56413, 2024). Specifically, the node_q is a summary quality indicator that checks numerous node and
pixel‐level parameters (JPL‐D‐105505, 2023). To remove outliers, we adopted a time‐space strategy as
described below. A flowchart (Figure S1 in Supporting Information S1) is also available in Supporting
Information S1.

Step 1: First, observations falling outside the nominal swath were excluded using the xtrk_dist parameter
(10 km < abs(xtrk_dist) < 60 km). Next, the summary node_q quality flag (node_q < 3) was applied to
filter out only “bad” node observations, a step designed to balance data quality and quantity. Our analysis

JIANG ET AL.

3 of 10

Geophysical Research Letters

10.1029/2025GL115953

suggests that observations flagged as “suspect” or “degraded” are not entirely invalid and retain potential
utility (see the effects of different flags as filters in Figures S2 and S3 in Supporting Information S1), in
line with the findings of Stuurman (2024). Obvious erroneous observations were discarded based on
p_wse and wse_u parameters. Specifically, observations that are 20 m away from the a priori wse value or
with uncertainty larger than 1 m were removed.

Step 2: A spatial filtering was applied to discard outliers further. Observations that remained in Step 1 were
ordered by the distance to the outlet. We adopted a rolling window size of 5 km and an increment of 1 km.
For each 5 km window, observations that are 10 m away from the median value were discarded.
Step 3: A 3‐month river longitudinal profile was then established based on a piecewise regression model.
Step 4: Based on the longitudinal profile, we screened observations along the river reach on a temporal basis.
Considering the temporal variations in the longitudinal profile for a given date, the longitudinal profile
was shifted based on the median difference between current observations and the profile. All observa-
tions that are 5 m (determined by in situ data, Table S2 in Supporting Information S1) away from this
newly set profile were removed.

Step 5: An iterative filtering was applied to the remaining observations. Specifically, for each iteration, a Locally
Weighted Scatterplot Smoothing (lowess) was fitted, and the difference between observation and pre-
diction from lowess was calculated. Then, observations with a difference larger than a given threshold
were discarded. We used four iterations with the thresholding values of 4, 3, 2, and 1 m.

The final observations were used to depict river longitudinal profiles. To examine cursory accuracy of SWOT
WSE, we compared USGS gauging records with SWOT WSE at the node closest to the gauge of interest (see
Figure 1b). The accuracy of SWOT WSE is good, with a median unbiased root‐mean‐square error (ubRMSE) of
0.25 m (Figure 1b, Table S2 in Supporting Information S1), which is on par with or slightly better than that of
nadir altimeters, such as Sentinel‐3 (Halicki & Niedzielski, 2022; Jiang et al., 2024; Jiang, Nielsen, Dinardo,
et al., 2020). It should be noted that the widths of most studied reaches are smaller than 100 m or even below 50 m
(Table S2 in Supporting Information S1). The reported accuracy here is not comparable to the SWOT Science
Requirements, which apply to reach data instead of node data (JPL‐D61923, 2018).

2.4. River WSS Estimation

In principle, the slope of any given reach can be calculated by dividing the drop of WSEs by the reach length.
However, the traditional twin‐gauge slope is determined by the WSEs at exactly the upstream and downstream
ends, regardless of the WSEs in between the two ends. Thanks to the dense measurements of WSEs from SWOT,
in this study, we not only calculated the slope of the two ends of a reach (hereafter referred to as the twin‐gauge
slope) but also calculated the slopes of all pairs of individual WSE within the reach of interest. This step was
intended to investigate how local WSS deviates from the entire reach WSS (Figure S4 in Supporting Informa-
tion S1). To evaluate SWOT‐derived slopes, we used USGS gauge WSE (i.e., height plus datum, see Table S1 in
Supporting Information S1 for datum and its accuracy) to compute ground‐based twin‐gauge slopes. Note that all
data were referenced to EGM2008.

3. Results

3.1. Temporal Variations in WSS

Given data availability constraints, we focused on 16 river reaches (Figure 1c) to examine SWOT's capability to
resolve river WSS variations. Assessment against slopes derived from USGS gauges demonstrated the high
quality of SWOT WSS, with RMSE values ranging 0.38–1.47 cm/km (median: 0.74 cm/km). Note that these
values are not directly comparable to the SWOT Science Requirements (JPL‐D61923, 2018) because our studied
reaches are generally narrower and longer (Table S3 in Supporting Information S1).

Figure 2 illustrates temporal WSS patterns, revealing strong temporal coherence between SWOT‐derived slopes
and twin‐gauge measurements across most reaches (refer to Figure S5 in Supporting Information S1 for all 16
reaches). Notably, SWOT accurately captured daily WSS increases in the Yellowstone (June) and James (April)
Rivers (Figures 2h and 2p). Moreover, SWOT might also be able to resolve sub‐reach WSS variability through
standard deviation analysis (Figure S6 in Supporting Information S1). Below we will further elaborate the spatio‐
temporal dynamics of WSS during a flood event in the James River.

JIANG ET AL.

4 of 10

Geophysical Research Letters

10.1029/2025GL115953

Figure 2. Comparison of temporal dynamics of WSS of 4 reaches (b, h, m, p correspond to the reaches labeled in Figure 1c)
for 3 months. The black line represents WSS derived from in situ gauges while the red dashed line represents SWOT derived
WSS. Note that SWOT WSS is the 3‐day moving average of SWOT twin‐gauge slopes to improve signal‐to‐noise ratio.

3.2. Spatio‐Temporal Dynamics of WSS

Here, we exemplify the potential of SWOT for monitoring the spatio‐temporal dynamics of WSS during a flood
event over the James River (see Figure 1). In general, the James River exhibited a smoothly convex profile.
During this flood event, the water level at the upstream gauge near Mitchell first peaked on the 29th of April
(Figure 3a), followed by the middle gauge near Scotland on the 3rd of May. The downstream gauge near Yankton
peaked on the 5th of May. Thus, the flood peak propagated downstream at 0.33 m/s, consistent with the river's low
gradient and meandering morphology (Table S2 in Supporting Information S1). Nevertheless, this slow propa-
gation drove asynchronous water‐level responses across gauges, which led to different temporal variations in
reach‐scale WSS, as shown in Figures 3d and 3e. Especially for the lower reach (Figure 3e), the slope increases by
about 50% within 20 days.

However, due to the long distance between the three gauges, the routing of the flood, for example, the spatial
evolution of flood waves and associated flood peak, cannot be well captured. In contrast, SWOT‐derived lon-
gitudinal profiles revealed critical spatio‐temporal heterogeneity. For example, from Figure 3f, we can see that the
flood peak moved downstream as the flood progressed, as highlighted by the gray area. Therefore, the highest
local WSS varied both in time and space, which is not unobservable through sparse gauge networks. Holistically,
we can see the non‐uniform WSS along the reaches. For instance, on the 16th of April, the slope of the upmost
50‐km reach is below 9 cm/km (refer to the blue dashed line), followed by a gradually increasing slope for the
downstream reach. This situation varied over time. On the contrary, the twin‐gauge WSS (blue dashed line in
Figure 3f) was not able to reveal such local variations. These spatio‐temporal varying river longitudinal profiles
highlight the importance of spatially dense WSE observations derived from for example SWOT. By monitoring
the variation of the longitudinal profile, flood processes can be better characterized and understood. However,
during the SWOT science phase, the lower sampling frequency might not be able to catch such flood events,
which has also been reported by Cerbelaud et al. (2024).

JIANG ET AL.

5 of 10

Geophysical Research Letters

10.1029/2025GL115953

Figure 3. Water surface slope (WSS) of the James River tributary (reaches o and p as shown in Figure 1c) of the Missouri River. (a–c) Show the in situ water levels; (d–e)
are the corresponding twin‐gauge slopes; (f) shows the instantaneous longitudinal profiles during the flood event. The gray area in (f) highlights the propagation of the
flood peak captured by SWOT. Note that there are no data over the lower reach due to the SWOT nadir gap. The site IDs of the three gauges near Mitchell, Scotland, and
Yankton are 06478000, 06478500, and 06478513, respectively.

3.3. Backwater Effects at River Confluences

Backwater is a commonly observed hydrological phenomenon at river confluences, where the flows are
obstructed to some extent due to the interactions of combining river flows. Such events often cause a rise in water
level and a decrease in flow velocity (Liu et al., 2023; Meng et al., 2025). Here, we showcase the capacity of
SWOT in monitoring river longitudinal profiles and associated WSS changes at river confluences, which has long
been a challenge to monitor (Biron et al., 2002).

JIANG ET AL.

6 of 10

Geophysical Research Letters

10.1029/2025GL115953

Figure 4. Backwater effects at the confluence of the Missouri and Yellowstone rivers. (a) Map of the river network, the two reaches used to investigate the backwater
effects, and locations of gauges from which the discharge time series are shown in (b); (c) SWOT derived 3‐day moving average WSS of two reaches as highlighted in
blue and red in (a), (d) and (e); (d) and (e) show the river long profiles on selected dates during the flood event of the Missouri and Yellowstone in May.

As shown in Figure 4a, the Yellowstone joins the Missouri just downstream of the curvature of the channel. Since
the 1st of May, the flow of the Yellowstone has been increasing (Figure 4b). The increase in flow has led to the
rising of the WSE of the river. As shown in Figure 4e, SWOT has captured the rising processes during the flood
(18–28 May). Visually, we can see that the rising of the river profile is literally spatially uniform. Thus, the WSS
is almost constant, as shown in Figure 4c. The propagation of this flood event is very different from the one
observed in the James River (Figure 3), where the upstream reach exhibited a steeper slope compared to the
downstream reach during the same period. A similar event was observed in the Missouri River during mid‐April
(Figure S7 in Supporting Information S1). At the confluence, the backwater effect caused a notable increase in
water level, resulting in a reduced slope (approximately 5 cm/km, representing a 67% decrease from the average
slope) downstream of the Yellowstone during this period, as clearly illustrated in Figure 2h.

In contrast, while the flow of the Missouri River remained nearly constant (likely due to regulation by the Fort
Peck Lake, Figure 1a),
its longitudinal profile exhibited non‐stationary and non‐uniform characteristics
(Figure 4d). The upstream reach of the Missouri River was significantly influenced by the backwater effect,
caused by asymmetric inflows (Figure 4b). During the entire period, the flow of the Missouri remained relatively
stable, leading to minimal changes in the WSE of its upper reach. However, due to the backwater effect, the WSE
of the lower reach just upstream of the confluence increased markedly. Furthermore, as the ratio of the two

JIANG ET AL.

7 of 10

Geophysical Research Letters

10.1029/2025GL115953

inflows grew, the WSE rise in the Missouri reach (blue‐shaded area) became more pronounced, reaching
approximately 1.3 m on 28th compared to 18th of May (Figure 4d). Additionally, Figure 4d reveals that the
backwater effect extended about 18 km upstream from the confluence, consistent with calculations using an
analytical formula (Liu et al., 2023). This backwater effect resulted in a corresponding decrease in WSS, which
showed an inverse correlation with the Yellowstone's inflow (Figures 4b and 4c).

According to Liu et al. (2023), the zone affected by backwater effects can extend much farther, up to 50 km,
depending on the specific combination of inflows from both rivers. In such cases, traditional stage‐discharge
rating curves for gauge stations within this range may become invalid, necessitating the use of a stage‐slope‐
discharge relationship to accurately estimate discharge (Liu et al., 2023). In this context, WSS from SWOT
can greatly facilitate the development of these advanced stage‐slope‐discharge rating curves. Moreover, this
example underscores the substantial potential of SWOT for investigating interaction dynamics at river
confluences.

4. Discussion and Conclusions

Measurements of river quantities, such as water level, width, slope, etc., are required for flood hazard man-
agement, water resource management, and climate and ecology studies. However, our understanding of such river
characteristics remains limited due to the scarcity of measurements. Even in regions with dense monitoring
networks, such as North America and Europe, hydrologic/hydraulic conditions between stations must be inter-
polated or modeled. This limitation hinders our ability to fully comprehend the intensified hydrological cycle
under global warming. Launched in December 2022, the SWOT mission has the potential to provide unprece-
dented hydrologic observations of river width, water level, and associated slope for near‐global coverage.

In this paper, we explored the capability of SWOT to monitor river water surface slope (WSS) and river lon-
gitudinal profiles in the Missouri River basin. Over a 3‐month period, SWOT successfully captured both temporal
variations at the reach scale and finer sub‐reach local variations, revealing the intricate non‐uniform and unsteady
nature of river flows. One of the notable findings is the ability of SWOT to resolve significant backwater effects at
the confluence of the Missouri and Yellowstone rivers, which is crucial for understanding flood dynamics and
ecological interactions. These observations underscore the potential of SWOT data to enhance our understanding
of river systems significantly.

However, the 21‐day repeat cycle (even the 3‐day sub‐cycle at high latitudes) may not be able to fully capture
WSS dynamics, especially for short‐duration events. This limitation needs further assessments to reach a more
general conclusion. Nevertheless, our findings underscore the transformative potential of SWOT for flood hy-
draulics, particularly in quantifying time‐varying flow nonuniformity, which is difficult, if not impossible, for
current sparse in situ monitoring networks.

As SWOT data accumulates, a broad range of new understandings and discoveries in river science will be on the
horizon. For instance, with its high spatial resolution of river WSE, global river WSS and profile concavity can be
better quantified; the questions about how many rivers worldwide are in the state of steady and uniform conditions
and how frequently they are, can be answered. Moreover, such data could critically inform hydrodynamic model
calibration and real‐time flood forecasting systems. However, realizing these potentials requires more than just
data collection. The development of high‐quality Level 2 data sets is crucial for advancing our understanding of
the questions mentioned above.

The implications of this study extend beyond the Missouri River basin, suggesting that SWOT data could
revolutionize global water resource management, flood forecasting, and ecological research by providing un-
precedented detail on river slope dynamics. Future research should focus on exploring the adequacy of SWOT's
21‐day repeat cycle for capturing short‐duration events and addressing any potential limitations in data
interpretation.

Data Availability Statement

The SWOT data used in this study are from the Level 2 River Single‐Pass Vector Data Product version 2
(L2_HR_RiverSP_v2.0) available at the NASA Physical Oceanography Distributed Active Archive Center

JIANG ET AL.

8 of 10

Acknowledgments
This work was supported by the National
Natural Science Foundation of China
(No. 42471348), the National Key R&D
Program of China (No. 2024YFF0808803),
the High‐level University Special Fund
(G03050K001), and the Open Research
Fund of Henan Provincial Key Laboratory
of Hydrosphere and Watershed Water
Security (No. HWWSF202303). The
authors wish to thank the three reviewers
and the editors for their suggestions and
comments, which greatly improved this
manuscript.

Geophysical Research Letters

10.1029/2025GL115953

(PODAAC, https://podaac.jpl.nasa.gov/SWOT). The in situ water level and discharge data are from the USGS
National Water Information System (NWIS, https://waterdata.usgs.gov/nwis).

References

Abdalla, S., Abdeh Kolahchi, A., Ablain, M., Adusumilli, S., Aich Bhowmick, S., Alou‐Font, E., et al. (2021). Altimetry for the future: Building
on 25 years of progress. Advances in Space Research, 68(2), 319–363. https://doi.org/10.1016/j.asr.2021.01.022

Altenau, E. H., Pavelsky, T. M., Moller, D., Lion, C., Pitcher, L. H., Allen, G. H., et al. (2017). AirSWOT measurements of river water surface
elevation and slope: Tanana River, AK. Geophysical Research Letters, 44(1), 181–189. https://doi.org/10.1002/2016GL071577

Biron, P. M., Richer, A., Kirkbride, A. D., Roy, A. G., & Han, S. (2002). Spatial patterns of water surface topography at a river confluence. Earth
Surface Processes and Landforms, 27(9), 913–928. https://doi.org/10.1002/esp.359

Cerbelaud, A., David, C. H., Biancamaria, S., Wade, J., Tom, M., Prata de Moraes Frasson, R., & Blumstein, D. (2024). Peak flow event durations
in the Mississippi River Basin and implications for temporal sampling of rivers. Geophysical Research Letters, 51(11). https://doi.org/10.1029/
2024GL109220

Cohen, S., Wan, T., Islam, M. T., & Syvitski, J. P. M. (2018). Global river slope: A new geospatial dataset and global‐scale analysis. Journal of
Hydrology, 563, 1057–1067. https://doi.org/10.1016/j.jhydrol.2018.06.066

De Bartolo, S. (2022). Advances in river hydraulic characterization. Water, 14(7), 1125. https://doi.org/10.3390/w14071125
Durand, M., Gleason, C. J., Garambois, P. A., Bjerklie, D., Smith, L. C., Roux, H., et al. (2016). An intercomparison of remote sensing river
discharge estimation algorithms from measurements of river height, width, and slope. Water Resources Research, 52(6), 4527–4549. https://
doi.org/10.1002/2015WR018434

Ferguson, R. I. (2012). River channel slope, flow resistance, and gravel entrainment thresholds. Water Resources Research, 48(5). https://doi.org/
10.1029/2011WR010850

Frederick, S. E., & Woodhouse, C. A. (2020). A multicentury perspective on the relative influence of seasonal precipitation on streamflow in the
Missouri River headwaters. Water Resources Research, 56(5). https://doi.org/10.1029/2019WR025756

Fu, L., Pavelsky, T., Cretaux, J., Morrow, R., Farrar, J. T., Vaze, P., et al. (2024). The surface water and ocean topography mission: A break-
through in radar remote sensing of the ocean and land surface water. Geophysical Research Letters, 51(4), 1–9. https://doi.org/10.1029/
2023GL107652

Halicki, M., & Niedzielski, T. (2022). The accuracy of the Sentinel‐3A altimetry over Polish Rivers. Journal of Hydrology, 606, 127355. https://
doi.org/10.1016/j.jhydrol.2021.127355

Han, B., & Endreny, T. A. (2014). Detailed river stage mapping and head gradient analysis during meander cutoff in a laboratory river. Water
Resources Research, 50(2), 1689–1703. https://doi.org/10.1002/2013WR013580

Jiang, L., Bandini, F., Smith, O., Klint Jensen, I., & Bauer‐Gottwein, P. (2020). The value of distributed high‐resolution UAV‐Borne observations
of water surface elevation for river management and hydrodynamic modeling. Remote Sensing, 12(7), 1171. https://doi.org/10.3390/
rs12071171

Jiang, L., Nielsen, K., & Andersen, O. B. (2024). Beyond exact repeat missions: Embracing geodetic altimetry for inland water monitoring and
modeling. Journal of Remote Sensing, 4, 1–7. https://doi.org/10.34133/remotesensing.0269

Jiang, L., Nielsen, K., Andersen, O. B., & Bauer‐Gottwein, P. (2020). A bigger picture of how the Tibetan Lakes have changed over the past
decade revealed by CryoSat‐2 altimetry. Journal of Geophysical Research: Atmospheres, 125(23), 1–15. https://doi.org/10.1029/
2020JD033161

Jiang, L., Nielsen, K., Dinardo, S., Andersen, O. B., & Bauer‐Gottwein, P. (2020). Evaluation of Sentinel‐3 SRAL SAR altimetry over Chinese
rivers. Remote Sensing of Environment, 237, 111546. https://doi.org/10.1016/j.rse.2019.111546

JPL‐D‐105505. (2023). SWOT algorithm theoretical basis document: Level 2 KaRIn high rate river single pass (L2_HR_RiverSP) science al-
gorithm software. Jet Propulsion Laboratory Internal Document.

JPL‐D‐56413. (2024). SWOT product description document: Level 2 KaRIn high rate river single pass vector (L2_HR_RiverSP) data product. Jet
Propulsion Laboratory Internal Document.

JPL‐D61923. (2018). Surface water and ocean topography mission (SWOT) project science requirements document.
Liu, J., Bauer‐Gottwein, P., Frias, M. C., Musaeus, A. F., Christoffersen, L., & Jiang, L. (2023). Stage‐slope‐discharge relationships upstream of
river confluences revealed by satellite altimetry. Geophysical Research Letters, 50(23). https://doi.org/10.1029/2023GL106394

Liu, J., Jiang, L., Bandini, F., Kittel, C. M. M., Balbarini, N., Hansted, N. G., et al. (2022). Spatio‐temporally varying Strickler coefficient: A
calibration approach applied to a Danish river using in‐situ water surface elevation and UAS altimetry. Journal of Hydrology, 613(PB), 128443.
https://doi.org/10.1016/j.jhydrol.2022.128443

Meng, Y., Jiang, L., Du, E., Zhang, X., Wang, W., & Wang, L. (2025). A new understanding of the Poyang Lake‐Yangtze River interaction: A
backwater effect on the Yangtze River perspective. Geophysical Research Letters, 52(7). https://doi.org/10.1029/2025GL114807

Nielsen, K., Zakharova, E., Tarpanelli, A., Andersen, O. B., & Benveniste, J. (2022). River levels from multi mission altimetry, a statistical
approach. Remote Sensing of Environment, 270, 112876. https://doi.org/10.1016/j.rse.2021.112876

Palucis, M. C., & Lamb, M. P. (2017). What controls channel form in steep mountain streams? Geophysical Research Letters, 44(14), 7245–7255.
https://doi.org/10.1002/2017GL074198

Pitcher, L. H., Pavelsky, T. M., Smith, L. C., Moller, D. K., Altenau, E. H., Allen, G. H., et al. (2019). AirSWOT InSAR mapping of surface water
elevations and hydraulic gradients across the Yukon Flats Basin, Alaska. Water Resources Research, 55(2), 937–953. https://doi.org/10.1029/
2018WR023274

Rodríguez, E., Durand, M., & de Frasson, R. P. M. (2020). Observing rivers with varying spatial scales. Water Resources Research, 56(9),
e2019WR026476. https://doi.org/10.1029/2019WR026476

Scherer, D., Schwatke, C., Dettmering, D., & Seitz, F. (2022). ICESat‐2 based river surface slope and its impact on water level time series from
satellite altimetry. Water Resources Research, 58(11), 1–25. https://doi.org/10.1029/2022WR032842

Stuurman, C. (2024). River product water surface elevation (WSE) and slope: Vlidation, features, and issues. In SWOT Science Team Meeting.
SWOT. (2024). SWOT level 2 river single‐pass vector data product. NASA Physical Oceanography Distributed Active Archive Center. https://
doi.org/10.5067/SWOT‐RIVERSP‐2.0

U.S. Geological Survey. (2025). National water information system data available on the world wide web (USGS Water Data for the Nation).
NASA Physical Oceanography Distributed Active Archive Center. https://doi.org/10.5066/F7P55KJN

Wang, Z., Jiang, L., Nielsen, K., & Wang, L. (2024). Reservoir filling up problems in a changing climate: Insights from CryoSat‐2 altimetry.
Geophysical Research Letters, 51(10), 1–11. https://doi.org/10.1029/2024GL108934

JIANG ET AL.

9 of 10

Geophysical Research Letters

10.1029/2025GL115953

Wise, E. K., Woodhouse, C. A., McCabe, G. J., Pederson, G. T., & St‐Jacques, J.‐M. (2018). Hydroclimatology of the Missouri River Basin.
Journal of Hydrometeorology, 19(1), 161–182. https://doi.org/10.1175/JHM‐D‐17‐0155.1

Zhao, Y., Jiang, L., Zhang, X., & Liu, J. (2023). Tracking river's pulse from space: A global analysis of river stage fluctuations. Geophysical
Research Letters, 50(23). https://doi.org/10.1029/2023GL106399

JIANG ET AL.

10 of 10
