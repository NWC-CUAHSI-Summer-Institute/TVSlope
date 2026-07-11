RESEARCH LETTER
10.1029/2024GL114185

Special Collection:
Science from the Surface Water
and Ocean Topography Satellite
Mission

Key Points:
• The Surface Water and Ocean

Topography (SWOT) satellite mission
offers simultaneous and synoptic
estimates of river discharge and other
hydrological variables globally
• Results show that SWOT can track
discharge dynamics without gauge
information, with correct magnitude in
some cases but with bias in others
• SWOT has the potential to provide
valuable insights into global river
discharge estimation, with implications
for hydrologic science

Supporting Information:

Supporting Information may be found in
the online version of this article.

Correspondence to:

K. M. Andreadis,
kandread@umass.edu

Citation:

Andreadis, K. M., Coss, S. P., Durand, M.,
Gleason, C. J., Simmons, T. T., Tebaldi,
N., et al. (2025). A First look at river
discharge estimation from SWOT satellite
observations. Geophysical Research
Letters, 52, e2024GL114185. https://doi.
org/10.1029/2024GL114185

Received 9 DEC 2024
Accepted 3 MAR 2025

© 2025 His Majesty the King in Right of
Canada. Jet Propulsion Laboratory,
California Institute of Technology and The
Author(s). Government sponsorship
acknowledged. Reproduced with the
permission of the Minister of Environment
and Climate Change Canada. This article
has been contributed to by U.S.
Government employees and their work is
in the public domain in the USA.
This is an open access article under the
terms of the Creative Commons
Attribution License, which permits use,
distribution and reproduction in any
medium, provided the original work is
properly cited.

ANDREADIS ET AL.

, Steve P. Coss2

, Michael Durand2

, Craig Brinkerhoff5,6
, Igor Gejadze8, Kevin Larnier9, Pierre‐Olivier Malaterre8

A First Look at River Discharge Estimation From SWOT
Satellite Observations
Konstantinos M. Andreadis1
Travis T. Simmons1, Nikki Tebaldi3, David M. Bjerklie4
Robert W. Dudley7
Hind Oubanas8
Alessio Domeneghetti12, Omid Elmi13, Luciana Fenoglio Marc14
Renato Prata de Moraes Frasson3
Jaclyn Gehring16
J. Toby Minear21
Tamlin M. Pavelsky18
Laurence C. Smith26
Brent A. Williams3

, Ryan M. Riggs24
, Cassie Stuurman3, Jay Taneja22, Angelica Tarpanelli27, Jida Wang25

, Augusto Getirana17
, Jérôme Monnier22, Aggrey Muhebwa23

, Mohammad J. Tourian13
, Md Safat Sikder25,

, Elisa Friedmann1, Pierre‐André Garambois15

, and Bidhyananda Yadav28

, Ernesto Rodríguez3

, George H. Allen10

, Marissa Hughes18

, Colin J. Gleason1

, Cédric H. David3

, Jonghyun Lee19

, Paul D. Bates11

,
,

,

,

,

,

,

, Pascal Matte20,
,

1Civil and Environmental Engineering, University of Massachusetts Amherst, Amherst, MA, USA, 2School of Earth
Sciences, Ohio State University, Columbus, OH, USA, 3Jet Propulsion Laboratory, California Institute of Technology,
Pasadena, CA, USA, 4U.S. Geological Survey, New England Water Science Center, East Hartford, CT, USA, 5School of the
Envirnoment, Yale University, New Haven, CT, USA, 6Yale Institute for Biospheric Studies, New Haven, CT, USA, 7U.S.
Geological Survey, New England Water Science Center, Pembroke, NH, USA, 8National Research Institute for Agriculture
Food and Environment (INRAE), UMR G‐eau, Montpellier, France, 9Space Department, CS Corporation, Toulouse,
France, 10Department of Geosciences, Virginia Polytechnic Institute and State University, Blacksburg, VA, USA, 11School
of Geographical Sciences, University of Bristol, Bristol, UK, 12Department of Civil, Chemical, Environmental and
Materials Engineering, Alma Mater Studiorum‐University of Bologna, Bologna, Italy, 13Institute of Geodesy, University of
Stuttgart, Stuttgart, Germany, 14Institute of Geodesy and Geoinformation, University of Bonn, Bonn, Germany, 15INRAE,
UMR RECOVER, Aix‐Marseille‐Université, Aix‐en‐Provence, France, 16Civil and Environmental Engineering,
Northeastern University, Boston, MA, USA, 17Hydrological Sciences Lab, NASA Goddard Space Flight Center, Greenbelt,
MD, USA, 18Earth, Marine and Environmental Sciences, University of North Carolina, Chapel Hill, NC, USA,
19Department of Civil, Environmental and Construction Engineering, Water Resources Research Center, University of
Hawaii at Manoa, Honolulu, HI, USA, 20Meteorological Research Division, Environment and Climate Change Canada,
Quebec City, QC, Canada, 21Cooperative Institute for Research in Environmental Sciences, University of Colorado
Boulder, Boulder, CO, USA, 22INSA Toulouse, Institut de Mathématiques de Toulouse, Toulouse, France, 23Electrical and
Computer Engineering, University of Massachusetts Amherst, Amherst, MA, USA, 24U.S. Geological Survey, Water
Mission Area, Reston, VA, USA, 25Department of Geography and Geographic Information Science, University of Illinois at
Urbana‐Champaign, Urbana, IL, USA, 26Department of Earth, Environmental, and Planetary Sciences, Brown University,
Institute at Brown for Environment and Society, Providence, RI, USA, 27Research Institute for Geo‐hydrological
Protection, National Research Council, Perugia, Italy, 28Byrd Polar and Climate Research Center, The Ohio State
University, Columbus, OH, USA

Abstract The Surface Water and Ocean Topography (SWOT) satellite has the potential to transform global
hydrologic science by offering simultaneous and synoptic estimates of river discharge and other hydraulic
variables. Discharge is estimated from SWOT observations of water surface elevation, width, and slope. A first
assessment using just the highest quality SWOT measurements, over the first 15 months (March 2023–July
2024) of the mission evaluated at 65 gauged reaches shows results consistent with pre‐launch expectations.
SWOT estimates track discharge dynamics without relying on any gauge information: median correlation is
0.73, with a correlation interquartile range of 0.51–0.89. SWOT estimates capture discharge magnitude
correctly in some cases but are biased (median bias is 50%) in others. There are already a total of 11,274
ungauged global locations with highest quality SWOT measurements where SWOT discharge is expected to
accurately track discharge variations: this value will increase as SWOT data record length grows, algorithms are
refined and SWOT measurements are reprocessed. This first look indicates that SWOT discharge is performing
as expected for SWOT data that achieve performance requirements, providing observed information on
discharge variations in ungauged basins globally.

Plain Language Summary River discharge is the volume of water passing a location on a river over
a given interval of time. This quantity determines how much water and energy are available for humans,

1 of 11

Author Contributions:

Conceptualization: Konstantinos
M. Andreadis, Michael Durand, Colin
J. Gleason
Data curation: Steve P. Coss, Travis
T. Simmons, Nikki Tebaldi, Luciana
Fenoglio Marc, Cassie Stuurman, Brent
A. Williams
Formal analysis: Konstantinos
M. Andreadis, Michael Durand
Funding acquisition: Colin J. Gleason,
Tamlin M. Pavelsky
Investigation: Konstantinos M. Andreadis
Methodology: Konstantinos
M. Andreadis, Steve P. Coss,
Michael Durand, Robert W. Dudley,
Tamlin M. Pavelsky, Laurence C. Smith
Software: Konstantinos M. Andreadis,
Steve P. Coss, Michael Durand, Travis
T. Simmons, Nikki Tebaldi, David
M. Bjerklie, Craig Brinkerhoff, Robert
W. Dudley, Igor Gejadze, Kevin Larnier,
Pierre‐Olivier Malaterre, Hind Oubanas,
Elisa Friedmann, Pierre‐André Garambois,
Jérôme Monnier
Supervision: Michael Durand, Jay Taneja
Validation: Konstantinos M. Andreadis,
Steve P. Coss, Michael Durand, Colin
J. Gleason, Pierre‐Olivier Malaterre,
Hind Oubanas
Visualization: Konstantinos
M. Andreadis, Steve P. Coss,
Michael Durand
Writing – original draft: Konstantinos
M. Andreadis
Writing – review & editing: Konstantinos
M. Andreadis, Steve P. Coss,
Michael Durand, Colin J. Gleason, David
M. Bjerklie, Craig Brinkerhoff, Robert
W. Dudley, Hind Oubanas, George
H. Allen, Paul D. Bates, Cédric H. David,
Alessio Domeneghetti, Omid Elmi,
Luciana Fenoglio Marc, Renato Prata de
Moraes Frasson, Pierre‐André Garambois,
Jaclyn Gehring, Augusto Getirana,
Marissa Hughes, Jonghyun Lee,
Pascal Matte, J. Toby Minear,
Jérôme Monnier, Aggrey Muhebwa,
Mohammad J. Tourian, Tamlin
M. Pavelsky, Ryan M. Riggs,
Ernesto Rodríguez, Md Safat Sikder,
Laurence C. Smith, Cassie Stuurman,
Angelica Tarpanelli, Jida Wang, Brent
A. Williams, Bidhyananda Yadav

Geophysical Research Letters

10.1029/2024GL114185

ecosystems, and sedimentary processes and is therefore essential knowledge for understanding, monitoring, and
managing water movement and storage. Global knowledge of river discharge is limited by the sparsity of on‐
the‐ground measurements, especially in countries without active monitoring programs or difficult to access
sites, resulting in the vast majority of the world's rivers being unmeasured. The Surface Water and Ocean
Topography (SWOT) satellite could revolutionize how we understand global water availability by providing
comprehensive data on river flow and related variables without the need for ground‐based measurements. In this
study, we share the first estimates of river discharge from SWOT observations during the first 15 months of the
mission. Our initial assessment indicates that it is in fact possible to effectively monitor river discharge from
space, and correlations of SWOT discharge estimates with ground measurements range from moderate to
strong. Despite unavoidable limitations in our study's river selection, these preliminary results suggest that
SWOT holds promise for estimating river discharge as SWOT collects more data and its measurements become
more accurate with time.

1. Introduction

River discharge plays a unique role in the water cycle, as it integrates the different hydrological processes of an
entire basin. Therefore, river discharge estimation is essential for understanding and monitoring water fluxes and
stores while also providing key information for managing water resources and risks. Although river gauges are an
invaluable source of discharge data and have helped shape hydrologic science, they have inherent limitations due
to their sparse spatial coverage and decreasing availability caused by practical, economic or political reasons
(Gleason & Hamdan, 2017; Krabbenhoft et al., 2022). These limitations can be partially alleviated by com-
plementing gauge measurements with remote sensing observations, particularly in ungauged basins or areas
where gauges are sparse (Gleason & Durand, 2020).

Remote sensing offers a potentially viable strategy for estimating river discharge over large areas in a systematic
and consistent manner (Van Dijk et al., 2016). Compared to establishing and maintaining an extensive ground‐
based measurement network for large rivers, remote sensing can be cost‐effective as it provides more spatially
extensive observations, especially over inaccessible regions, ensuring a baseline level of regular monitoring and
data collection everywhere. While remote sensing will not remove the need for in situ discharge measurements, it
can complement the existing gauging network. Many approaches have been developed to estimate river discharge
from remotely sensed observations, all of which have historically required calibration with ground data or models.
For example, several studies developed rating curves between in situ discharge and satellite‐derived variables to
estimate discharge at particular locations (e.g., Smith et al., 1996; Tarpanelli & Domeneghetti, 2021). These
variables include river width (e.g., Feng et al., 2021), elevation (e.g., Getirana & Peters‐Lidard, 2013; Paris
et al., 2016), and slope (e.g., Paris et al., 2016). Alternative approaches have combined satellite observations with
modeling and data assimilation to derive river discharge estimates (e.g., Ishitsuka et al., 2021; Pujol et al., 2020;
Tourian et al., 2017). The overall objective of many of these studies was the estimation of discharge solely from
satellite observations (Gleason & Smith, 2014), but very few studies have successfully estimated river discharge
without in situ data (Brinkerhoff et al., 2020; Feng et al., 2021; Gleason & Smith, 2014; Gleason et al., 2014; Lin
et al., 2023) and these have limited accuracy in many contexts. These approaches primarily use optical satellites to
derive river width, and this is limited by uncertainties in the observations, clouds, river morphologies that pre-
clude width changes, and underdeveloped estimation algorithms (Tarpanelli et al., 2021).

The Surface Water and Ocean Topography (SWOT) satellite mission, launched in December 2022, is a
collaboration between the United States (NASA) and French (CNES) space agencies with the additional
participation of the UK and Canadian space agencies. SWOT uses two Synthetic Aperture Radar antennas to
provide the first‐ever two‐dimensional, high‐resolution measurements of the elevation, extent and storage
changes of land surface water bodies including rivers, lakes, and wetlands. These measurements of water surface
elevation (WSE) and inundation alone have long been recognized as potentially revolutionizing our approach to
monitoring and quantifying surface water (Alsdorf et al., 2007) and first results suggest that the SWOT mission
can meet and even exceed its science requirements in some cases (Fu et al., 2024).

While these results are transformative, SWOT holds promise for estimating ungauged river discharge which can
be considered the “holy grail of scientific hydrology” (Beven, 2006). A relatively extensive body of work has

ANDREADIS ET AL.

2 of 11

 19448007, 2025, 9, Downloaded from https://agupubs.onlinelibrary.wiley.com/doi/10.1029/2024GL114185, Wiley Online Library on [14/06/2026]. See the Terms and Conditions (https://onlinelibrary.wiley.com/terms-and-conditions) on Wiley Online Library for rules of use; OA articles are governed by the applicable Creative Commons LicenseGeophysical Research Letters

10.1029/2024GL114185

assessed and evaluated the potential of different methodologies to estimate river discharge from synthetic SWOT
observations, starting with Andreadis et al. (2007) who assimilated water elevation observations into a hydro-
dynamic model to estimate discharge over a single river reach. Many of these approaches have focused on data
assimilation (Gejadze et al., 2022; Larnier & Monnier, 2023; Revel et al., 2021) while other approaches have
considered how to improve SWOT discharge temporal resolution via interpolation (e.g., Paiva et al., 2015). As the
requirements for the SWOT mission include a river discharge data product, a set of algorithms with operational
potential was developed. These algorithms form the core of “Confluence,” an operational purpose‐built cloud‐
based software platform that combines SWOT observations and ancillary data to create estimates of SWOT
discharge globally, and pulls in situ discharge from global water agencies public repositories to assess SWOT
discharge accuracy for each run (Durand et al., 2023). Preliminary assessments of these algorithms suggested
SWOT‐like observations could yield discharge with bias dominating the error when compared to gauges (Durand
et al., 2016; Frasson et al., 2021, 2023). Fundamentally, the bias arises because the SWOT algorithms attempt to
solve the ill‐posed “mass conserved flow law inversion” problem (Larnier et al., 2021) by regularizing using a
prior information for example, on mean annual flow. SWOT discharge algorithms improve over the prior esti-
mates, but errors in prior estimates generally translate to error in SWOT discharge (Frasson et al., 2021). Thus,
SWOT discharge bias results from bias in estimates of prior information used to drive the algorithms.

Here, we present the first SWOT discharge results from the initial 15 months of the mission. We evaluate
discharge estimated only using SWOT measurements that are not subject to known anomalies in data SWOT
processing: SWOT is an experimental mission and its river data products are continuously improving, but quality
filtering is needed using SWOT's self‐reported quality flags. Thus, SWOT data are aggressively filtered, reducing
sample sizes, but increasing confidence in examining SWOT measurements that meet performance requirements.
Nonetheless, SWOT discharge is estimated without any in situ gauge information making the validation results
applicable to the problem of estimating discharge in ungauged basins. In addition to this initial validation of
SWOT discharge, we provide an estimate of the extent of global locations expected to have accurate SWOT
discharge estimates. Overall, our aim here is to assess whether or not SWOT discharge estimates meet pre‐launch
expectations, viz. accurately tracking discharge variations measured at in situ gauges (Durand et al., 2023).

2. Estimating River Discharge

River discharge estimation from SWOT leverages the unique capability of the satellite to simultaneously observe
river WSE, width, and slope (Durand et al., 2023). SWOT observes these characteristics over a set of predefined
river reaches (Altenau et al., 2021). The WSE, width and slope performance requirements are 10 cm, 15% of true
width, and 1.7 cm/km for a nominal 10 km reach, and it is required to measure rivers wider than 100 m, with a goal
of measuring rivers as narrow as 50 m (JPL, 2018). Each of these river reaches is approximately 10 km in length,
to ensure adequate precision of reach‐averaged observations (Rodríguez et al., 2020). Data at the native spatial
resolution (varying across the swath but approximately 25 m on average) of the SWOT radar are averaged over
each river to compute WSE and width measurements at “nodes,” 200 m increments along river centerlines. The
node measurements are used in turn to compute reach averaged estimates of WSE, width, and slope (Frasson
et al., 2017), which are significantly more precise than the corresponding node‐based estimates.

In this study, we exclusively use Version C of the “River Single‐Pass” data product (JPL, 2020) for the SWOT
measurements. While the minimum SWOT‐observed river width for accurate discharge estimation is an open
question (Fu et al., 2024) preliminary SWOT calibration and validation studies have demonstrated accurate WSE
measurements for rivers at least as narrow as 80 m (Stuurman, 2024) so we examine river widths greater than 80 m
in this study. From launch until July 2023, the SWOT satellite was in a 1‐day exact repeat orbit in order to facilitate
calibration and validation activities with non‐global coverage. From July 2023 until present, SWOT has been in its
nominal 21‐day repeat orbit that measures nearly all rivers globally with the number of observations being
dependent on latitude and swath geometry; there are approximately two observations every 21 days for most mid‐
latitude rivers. Here we processed all SWOT data from both the 1‐day repeat calibration/validation and the 21‐day
repeat science orbits, creating river discharge estimates for SWOT spanning from 30 March 2023 to 21 July 2024,
based on data available at the time Confluence was run. The period spans 479 days, or approximately 23 SWOT
cycles, and thus most reaches would have approximately 45 SWOT overpasses during the Science Orbit.

At the core of discharge estimation from SWOT observations is the application of flow laws that relate its ob-
servables to discharge, and a set of algorithms to estimate unobserved parameters. One such flow law is the

ANDREADIS ET AL.

3 of 11

 19448007, 2025, 9, Downloaded from https://agupubs.onlinelibrary.wiley.com/doi/10.1029/2024GL114185, Wiley Online Library on [14/06/2026]. See the Terms and Conditions (https://onlinelibrary.wiley.com/terms-and-conditions) on Wiley Online Library for rules of use; OA articles are governed by the applicable Creative Commons LicenseGeophysical Research Letters

10.1029/2024GL114185

modified Gauckler‐Manning‐Strickler equation, transformed as described by Larnier et al. (2021) and Durand
et al. (2023), which computes discharge as a function of hydraulic quantities observed by SWOT (WSE, river
width, and river slope) and flow law parameters that are unobserved (resistance coefficient, hydraulic radius, etc.).
The flow law parameters are computed using SWOT observations and a set of six algorithms with a priori in-
formation such as mean annual flow derived from global models (Durand et al., 2023). The discharge estimates
are obtained from the so‐called “unconstrained” branch of Confluence, which does not use any gauge mea-
surements to calibrate the SWOT algorithms in any way. Even though there are different discharge estimation
algorithms, here we compare gauge measurements with the SWOT “consensus” discharge, which is computed as
a simple median across the available discharge estimates from the individual algorithms. An example of SWOT
measurements and the consensus discharge estimate is shown in Figure S1 in Supporting Information S1.

To meaningfully assess SWOT discharge accuracy, we must take the data quality of SWOT observations into
account using the associated flags of the data product (JPL, 2024). In this initial study we select and analyze only
the “highest quality” SWOT measurements of WSE, width and slope by filtering out observations flagged as
anomalous (JPL, 2020). Note that the SWOT data quality is expected to improve as processing algorithms are
refined, so the scale and scope of what data are “highest quality” rapidly changes and we expect to be different
when this article goes to print. As one example, we examine only SWOT measurements where the reach falls
between 15 and 60 km of the spacecraft ground track: by design, SWOT will still produce a measurement when a
reach falls outside that range, but the data are expected to be inaccurate and thus are flagged (JPL, 2024). We
additionally filter statistical outliers identified in the time series of WSE, width and slope (details on these filters
described in Text S1 in Supporting Information S1) resulting in a set of SWOT observations that meet the
mission's performance requirements (JPL, 2018).

Even for the highest quality SWOT data used in this study, variability in discharge estimate accuracy is still a
function of some aspects of the SWOT observations and how they are used in Confluence to estimate discharge.
Hence, we stratify discharge performance based on two aspects of SWOT observations and discharge algorithm
design. In SWOT nomenclature, a river reach is “completely observed” if reach‐averaged WSE, width and slope
observations pass all data quality filters. On the other hand, a reach is “conditionally observed” if a subset of nodes
pass the data filtering but reach‐averaged observations did not. As some of the SWOT discharge algorithms operate
on node data, while others are driven by the reach‐averaged observations the former will still produce a discharge
estimate even for a “conditionally observed” river reach. Furthermore, we expect that SWOT discharge accuracy
will vary with “hydraulic consistency” of the observations. That is, we leverage the fact that WSE and width must
be positively correlated due to basic physical and geomorphic constraints on river bed geometry (Durand
et al., 2024) making time series where WSE and width are negatively correlated “inconsistent.” Negative corre-
lations is a simple but effective way to flag physically implausible behavior, as even for rivers with steep banks
width would remain effectively constant with changes in WSE. Therefore, we assess the performance of SWOT
discharge by stratifying observations into “completely observed” reaches and ones that are “hydraulically
consistent.”

Gauge discharge measurements, acquired from water monitoring agencies globally, are computed by measuring
water level and predicting discharge based on a rating curve. Studies have shown that such streamgauge ob-
servations are themselves subject to an uncertainty of at least 10% and often far greater (Coxon et al., 2015; Kiang
et al., 2018), but are the best independent reference to assess SWOT discharge. Uncertainty in the SWOT‐
estimated discharge arises from errors in the SWOT observations (WSE, width and slope), as well as flow law
approximations and assumptions (Frasson et al., 2023). These errors contribute to both random and systematic
errors, the latter of which manifests as bias in the time series of SWOT discharge estimates. In pre‐launch studies
SWOT discharge was expected to track discharge variations with bias present in some cases (Durand et al., 2016;
Frasson et al., 2023). As we are using the “unconstrained” SWOT discharge estimates here with a relatively short
time series we expect that the bias will be larger than what future versions of SWOT discharge will have but the
dynamics of observed discharge will still be captured.

3. Synoptic River Discharge

One of the most important aspects of SWOT is the ability to produce spatially continuous and consistent estimates
of river discharge globally, complementing existing in situ gauge networks (Pavelsky et al., 2014) and facilitating
the comprehensive understanding of river behavior and hydraulics across reaches (Carr et al., 2019; Li

ANDREADIS ET AL.

4 of 11

 19448007, 2025, 9, Downloaded from https://agupubs.onlinelibrary.wiley.com/doi/10.1029/2024GL114185, Wiley Online Library on [14/06/2026]. See the Terms and Conditions (https://onlinelibrary.wiley.com/terms-and-conditions) on Wiley Online Library for rules of use; OA articles are governed by the applicable Creative Commons LicenseGeophysical Research Letters

10.1029/2024GL114185

Figure 1. Examples of Surface Water and Ocean Topography discharge (in m3/s) estimates (including conditionally observed
reaches) for five satellite overpasses (a–e) and the average of all passes during the science orbit (21 July 2023–21 July 2024, s
(f) are shown for 654 reaches across the Ohio River basin, USA. Mean discharge in panel (f) spans from 6,478 with a median
value of 197.09 and a standard deviation of 972.6 (11 outliers with discharge 10,000 m3/s) are not shown). The inlay in panel
(f) shows the study area outline.

et al., 2022). Spatially distributed discharge can significantly enhance hydrologic modeling, as calibration against
such distributed observations can improve a model's reliability and predictive capabilities (Pan & Wood, 2013).
Moreover, spatially dense observations of discharge can aid in the better representation of lateral inflows,
withdrawals and surface storage effects on river discharge that would otherwise be challenging to capture
accurately (Papa et al., 2008). These synoptic discharge observations also have implications for many other
purposes as they play a vital role in evaluating habitat availability for fish (Wegscheider et al., 2024), assessing
pollution levels in rivers (Chidamba et al., 2016), estimating sediment transport (Segura & Pitlick, 2015),
quantifying the thermal budget of rivers (King et al., 2020), monitoring river plumes (Osadchiev et al., 2020), and
understanding surface‐groundwater interactions (Anibas et al., 2012).

Figure 1 showcases the spatial and temporal aspects of SWOT discharge estimates with synoptic scale maps
showing discharge for five different satellite overpasses, and the average of all overpasses within the study period
in the Ohio River basin, USA. The figure includes discharge derived from SWOT measurements where reaches
were conditionally observed. Each discharge measurement represents the instantaneous discharge at the satellite
overpass time over a subset of river reaches in the domain. The pass from cycle 14, on 23 April 2024 (Figure 1b),
shows higher flows on the mainstem Ohio than on the overpasses from the autumn, which is expected given that
flows throughout the Ohio River basin tends to be higher in spring than in fall. The geolocation and timing of
SWOT overpasses combine with river planform and timing of floodwave propagation to dictate “hydraulic
visibility” of each river (Garambois et al., 2016) and the ability of the satellite to map floodwave spatiotemporal
dynamics (Durand et al., 2010). For example, pass 181 (Figure 1e) is oriented along the downstream Wabash
River, observing approximately 400 km of distance along the river centerline. In contrast, pass 160 is perpen-
dicular with the upstream Wabash, and observes only approximately 200 km of river. The map of average

ANDREADIS ET AL.

5 of 11

 19448007, 2025, 9, Downloaded from https://agupubs.onlinelibrary.wiley.com/doi/10.1029/2024GL114185, Wiley Online Library on [14/06/2026]. See the Terms and Conditions (https://onlinelibrary.wiley.com/terms-and-conditions) on Wiley Online Library for rules of use; OA articles are governed by the applicable Creative Commons LicenseGeophysical Research Letters

10.1029/2024GL114185

Figure 2. Hydrographs comparing Surface Water and Ocean Topography (SWOT) discharge with in situ discharge for four
reaches, representing a wide range of SWOT performance: (a) reach 74210000201, the Mississippi River near Baton Rouge,
Louisiana, United States; (b) reach 81130400021, the Kenai River near Soldotna, Alaska, United States; (c) reach
21602400201, the Le Drac River near Grenoble, France; and (d) reach 23229000561, the Loire River near Saint‐Victor sur
Loire, France. The prior estimate (dashed line) is computed from global models as described in Durand et al. (2023).

discharge (Figure 1f) shows values ranging from 1 m3/s in the headwaters to 6,480 m3/s at the Ohio River outlet
where it flows into the Mississippi River. These variations are realistic as assessed by in situ gauges in the basin,
presenting a spatially coherent view of average flow estimated by SWOT across the river network.

4. Preliminary Validation

The preliminary analysis presented herein shows that this early version of SWOT discharge meets pre‐launch
expectations by tracking gauge discharge variations for the highest quality SWOT data where and when rea-
ches are completely observed. Figure 2 shows SWOT and gauge hydrographs for four reaches selected to
illustrate the range of SWOT discharge performance. SWOT accurately tracks the Mississippi River near Baton
Rouge, USA (Figure 2a) capturing both river discharge dynamics and magnitude (r = 0.965, normalized
bias = 1.9%). Similarly, SWOT resolves discharge variations on the Kenai River near Sodotna, USA, (r = 0.97),
but with a bias of 27% (Figure 2b, Pre‐launch studies found that bias is most often due to bias in the prior (Frasson
et al., 2021), which was − 41% for this reach, rather than other factors such as the scale discrepancy between
10 km reaches and streamgauges (Durand et al., 2024; Rodríguez et al., 2020). Note the gap present here is due to
SWOT data that are flagged as ice‐impacted in the SWOT product. This level of performance, and a modest
improvement in the prior bias, is well within expectations laid out prior to launch (Durand et al., 2023).

ANDREADIS ET AL.

6 of 11

 19448007, 2025, 9, Downloaded from https://agupubs.onlinelibrary.wiley.com/doi/10.1029/2024GL114185, Wiley Online Library on [14/06/2026]. See the Terms and Conditions (https://onlinelibrary.wiley.com/terms-and-conditions) on Wiley Online Library for rules of use; OA articles are governed by the applicable Creative Commons LicenseGeophysical Research Letters

10.1029/2024GL114185

Figure 3. Performance statistics for the three categories of Surface Water and Ocean Topography (SWOT) discharge
estimates are shown, including (a) the “conditionally observed reaches” (n = 827), (b) the “highest quality SWOT data”
(n = 65), and (c) the “hydraulic consistency” requirement additionally imposed on the “highest quality SWOT data” (n = 54).
Four measures of performance are shown: Spearman r, normalized bias, absolute value of normalized bias and Nash‐
Sutcliffe efficiency. The data are shown as empirical cumulative distribution functions. The x‐axes are truncated at 1.5 and − 1.5.
The dashed lines correspond to the 33rd and 67th percentile.

SWOT also captures discharge variations on the Le Drac River near Grenoble, (r = 0.65) but SWOT estimates are
much larger (162%) than the gauge (Figure 2c). We expect bias in SWOT discharge to drop as the length of
SWOT time series increases, and other improvements (e.g., “basin scale” algorithm designed to estimate mean
flow across river networks) are deployed in the near future (Durand et al., 2023). Moreover, SWOT discharge
appears to overestimate the “flashiness” of the Le Drac, but still capturing the direction of the changes in
discharge. This river reach is only 80 m wide, the very minimum value for which performance is assessed for this
study, and such anomalies may be more common for narrower rivers. SWOT discharge does not meaningfully
track the gauge on the Loire River near Saint‐Victor sur Loire (r = 0.2), and bias is substantial (87%, Figure 2d)
which presumably can be attributed to unflagged problems with the SWOT observations.

Across all “completely observed” reaches that had at least 10 valid observations after filters have been applied, we
find that SWOT discharge estimates generally track gauge discharge quite well, but are subject to bias. Figure 3
shows performance for discharge estimated in order of least filtered (“conditionally observed”) to most filters
applied (“completely observed” and hydraulically consistent). Discharge performance for “conditionally
observed” reaches shown in Figure 3a indicates two major differences compared with “completely observed”

ANDREADIS ET AL.

7 of 11

 19448007, 2025, 9, Downloaded from https://agupubs.onlinelibrary.wiley.com/doi/10.1029/2024GL114185, Wiley Online Library on [14/06/2026]. See the Terms and Conditions (https://onlinelibrary.wiley.com/terms-and-conditions) on Wiley Online Library for rules of use; OA articles are governed by the applicable Creative Commons LicenseGeophysical Research Letters

10.1029/2024GL114185

reaches. First, there are a total of 827 gauged reaches with at least 10 observations in this run, over an order of
magnitude more than when we require reaches to be completely observed. This may be explained by considering
that there are on average 50 nodes in each 10 km reach. The algorithms that produce discharge with only node data
may be driven by one or two node observations, therefore it is far more likely that a small number of nodes pass
the filters compared to the observations for the entire reach. Second, these observations for “conditionally
observed” reaches are far less likely to track discharge variations. The median Spearman correlation is 0.39,
approximately half the value, if we require, reaches to be completely observed. The lower correlation can be
explained by considering that in most cases when a reach observation of WSE, width and slope has cleared all
filters intended to isolate highest quality SWOT data, then most of the nodes within a reach are observed and are
of good quality.

On the other hand, the median Spearman r is 0.73 and the interquartile range is 0.5–0.89 for reaches that were
“completely observed” (Figure 3b), showing that SWOT discharge captures gauge variations well in most cases
of those 65 river reaches. The median of the absolute value of the bias is 56%, which is larger than predicted in
pre‐launch studies (Durand et al., 2023), and can be explained by two factors, both of which point to expected
future improvements in SWOT discharge. First, bias in SWOT discharge is (to first order) controlled by the bias in
prior estimates of mean annual flow, and that prior bias in this study (62%) was larger than observed seen in pre‐
launch studies (Frasson et al., 2021, 50%). This is expected to improve with both the increasing length of SWOT
timeseries, and algorithm changes designed at improving these prior estimates. Second, the expected SWOT
discharge error level was computed assuming basin‐scale algorithms that integrate information across river ba-
sins, shown by Durand et al. (2023) to reduce bias by approximately 10% (i.e., from 40% to 30% in that study), but
not run in this study due to technical challenges. SWOT algorithms improved over the prior estimates of mean
discharge for most reaches, and as technical issues are resolved we expect that future SWOT discharge will
improve. The median Nash‐Sutcliffe values are negative, which is attributable to the large bias present. The
spatial locations of these reaches are shown in Figure S2 in Supporting Information S1.

Discharge performance for reaches exhibiting “hydraulic consistency” (Figure 3c) shows further improvement
over the “completely observed reaches” (Figure 3a). There are a total of 54 reaches satisfying the consistency
criterion and having at least 10 good observations. The median Spearman correlation improves to 0.8, compared
with 0.73 for reaches requiring only complete observation and the inter‐quartile range is 0.62–0.92.

We have focused discussion on bias and correlation separately, in order to highlight the various factors controlling
SWOT discharge performance, namely the flow law parameter error, and the SWOT observation error (Durand
et al., 2023). Metrics such as Nash‐Sutcliffe efficiency (NSE) and normalized RMSE make it hard to disentangle
that information as they lump together systematic and random errors. Although they are helpful for comparison to
other studies they can be distracting for this initial look at SWOT discharge. Figure 3d shows that median NSE
values are negative for all three filtering approaches, showing the dominance of bias on the NSE statistic.
Furthermore, Figure S7 in Supporting Information S1 shows normalized RMSE with conditionally observed
reaches having higher error, similar to the Spearman r results.

Figures S5 and S6 in Supporting Information S1 explore the effect of river width on Spearman r and normalized
bias, respectively, across the conditionally observed, highest quality, and hydraulic consistency groups. In
general, wider rivers have higher correlation and lower bias. This dependence on river size is minimal in
conditionally observed reaches, but is prominent in the highest quality and hydraulically consistent groups.
Median bias is reduced from 0.72 to 0.64, and 0.34 for river widths less than 100 m, between 100 and 200 m, and
above 200 m, respectively, for the hydraulically consistent reaches. The effect is less pronounced for correlation,
but in general, larger rivers do exhibit both lower bias and higher correlation.

Using the entire SWOT data archive accessed on 24 October 2024, 11,389 reaches globally meet the criteria to be
considered highest quality SWOT data, and this should have accuracies comparable to Figure 3b, of which 115 are
gauged. That is, SWOT is likely able to track discharge variations accurately for 11,274 ungauged reaches.
Moreover, we expect this number to increase as the SWOT mission lengthens, which we further discuss in the
following section. These results are an important benchmark to improve upon for future efforts of the SWOT
Science Team Discharge Algorithm Working Group in coming years.

ANDREADIS ET AL.

8 of 11

 19448007, 2025, 9, Downloaded from https://agupubs.onlinelibrary.wiley.com/doi/10.1029/2024GL114185, Wiley Online Library on [14/06/2026]. See the Terms and Conditions (https://onlinelibrary.wiley.com/terms-and-conditions) on Wiley Online Library for rules of use; OA articles are governed by the applicable Creative Commons LicenseGeophysical Research Letters

10.1029/2024GL114185

5. Outlook

This study presents a first look at river discharge generated from SWOT observations. The value of these ob-
servations is not limited to the estimation of discharge but likely extends to many other applications such as floods
(Frasson et al., 2019) and carbon emissions (Brinkerhoff et al., 2022). Following many years of synthetic data
studies (e.g., Andreadis et al., 2007; Frasson et al., 2023), we demonstrate that it is indeed feasible to estimate
river discharge from actual SWOT observations, and we show an initial validation of the retrievals against in situ
measurements. This study shows that SWOT discharge tracks discharge variations as expected, but has a higher
bias than predicted in pre‐launch studies; discharge bias is higher than expected for reasons that are explainable
and are expected to improve in the future (Durand et al., 2023). For instance, Lin et al. (2023) published discharge
estimates applicable to truly ungauged basins using Landsat to derive river widths and then discharge with an
algorithm almost 10 years in development at that point. They showed median r values of 0.3 and 0.8 at over 3,000
gauges using static and monthly discharge priors, respectively. They also showed positive NSE results in about
25% and 50% of gauges for these same priors. SWOT discharge has achieved relatively similar accuracy “out of
the box” without any time or scope for algorithm modification. Indeed, the results presented here represent an
early benchmark which is expected to be surpassed as SWOT data quality and discharge algorithms improve and
SWOT data times series continues to grow in length. Furthermore, future studies will leverage additional SWOT
discharge algorithms: gauge‐constrained estimates of SWOT discharge and basin‐scale discharge algorithms
(Durand et al., 2023) which should improve the accuracy of the results shown here mostly due to reduction in the
estimation bias. Despite these caveats, it appears that SWOT is able to estimate discharge across a range of rivers,
for highly variable flow conditions both in terms of dynamics and magnitude without any gauge information.

These initial validation results show that SWOT accurately tracks discharge variations for select reaches, but even
these 11,289 select reaches represent more locations than in situ river discharge databases. For a point of com-
parison, we find that there are a total of 2,393 gauges in the Global Runoff Data Center with measurements within
the past 2 years, and in water agencies that make their data available publicly for rivers wider than 80 m. These
agencies include the U.S. Geological Survey in the United States, EAU in France, WSC and MELCCFP in
Canada, DEFRA in the UK, DGA in Chile, Hidroweb in Brazil, ABOM in Australia, DWA in South Africa, and
MLIT in Japan. Figure S3 in Supporting Information S1 compares the spatial distribution of the 11,289 select
reaches where SWOT is expected to perform well with available gauges. SWOT measures discharge at lower
precision and temporal resolution than gauges, and its records extend back only to launch: SWOT will never
replace stream gauges. SWOT and stream gauges are complementary, with SWOT increasing discharge estimate
coverage by an order of magnitude, spanning thousands of ungauged basins.

The uncertainties associated with these discharge estimates need to be carefully considered when using the data
for scientific analysis and applications, particularly in the context of uncertainties in gauge streamflow (Horner
et al., 2018; Kiang et al., 2018). Nonetheless, the SWOT mission's ability to estimate streamflow and its variations
represents a significant advancement in the observation of global river discharge, particularly for relatively large
rivers and in regions currently lacking in situ gauging infrastructure.

Data Availability Statement

The data utilized in this study are derived from SWOT data products, and particularly the Level 2 River Single‐
Pass Vector Data Product available at the NASA Physical Oceanography Distributed Active Archive Center
(PODAAC, https://podaac.jpl.nasa.gov/SWOT) (SWOT, 2024) and at the CNES Hydroweb next repository at
https://hydroweb.next.theia-land.fr/. These data products are distributed in compliance with FAIR requirements.
The software used to generate the discharge estimates, including the Confluence framework and individual al-
gorithms, are available at https://github.com/SWOT-Confluence. The discharge estimates from SWOT used in
this study are available at https://podaac.jpl.nasa.gov/dataset/SWOT_L4_DAWG_SOS_DISCHARGE (SWOT
Discharge Algorithm Working Group, 2023).

References

Alsdorf, D. E., Rodríguez, E., & Lettenmaier, D. P. (2007). Measuring surface water from space. Reviews of Geophysics, 45(2), RG2002. https://

doi.org/10.1029/2006RG000197

Altenau, E. H., Pavelsky, T. M., Durand, M. T., Yang, X., Frasson, R. P. D. M., & Bendezu, L. (2021). The Surface Water and Ocean Topography
(SWOT) mission river database (SWORD): A global river network for satellite data products. Water Resources Research, 57(7),
e2021WR030054. https://doi.org/10.1029/2021WR030054

9 of 11

Acknowledgments
A portion of this work was performed at
the Jet Propulsion Laboratory, California
Institute of Technology, under a contract
with the National Aeronautics and Space
Administration (80NM0018D0004).
NASA's SWOT Science Team Grants
80NSSC20K1339, 80NSSC20K1143,
80NSSC20K1340, and 80NSSC20K1141
funded Confluence development and
computation, as did NASA AIST Grant
80NSSC22K1487. Support was also
provided by CNES SWOT TOSCA Grant
DETECT B01 funded by the Deutsche
Forschungsgemeinschaft (DFG, German
Research Foundation)—SFB 1502/1–2022
‐ 45005826 provided support and the
German Federal Institute of Hydrology
(BfG) in situ data. We would like to thank
two anonymous reviewers for their
comments and feedback on earlier versions
of the manuscript.

ANDREADIS ET AL.

 19448007, 2025, 9, Downloaded from https://agupubs.onlinelibrary.wiley.com/doi/10.1029/2024GL114185, Wiley Online Library on [14/06/2026]. See the Terms and Conditions (https://onlinelibrary.wiley.com/terms-and-conditions) on Wiley Online Library for rules of use; OA articles are governed by the applicable Creative Commons LicenseGeophysical Research Letters

10.1029/2024GL114185

Andreadis, K. M., Clark, E. A., Lettenmaier, D. P., & Alsdorf, D. E. (2007). Prospects for river discharge and depth estimation through
assimilation of swath‐altimetry into a raster‐based hydrodynamics model. Geophysical Research Letters, 34(10), L10403. https://doi.org/10.
1029/2007GL029721

Anibas, C., Verbeiren, B., Buis, K., Chormański, J., De Doncker, L., Okruszko, T., et al. (2012). A hierarchical approach on groundwater‐surface
water interaction in wetlands along the upper Biebrza River, Poland. Hydrology and Earth System Sciences, 16(7), 2329–2346. https://doi.org/
10.5194/hess-16-2329-2012

Beven, K. (2006). Searching for the holy grail of scientific hydrology: Qt=(S, R, Δt)A as closure. Hydrology and Earth System Sciences, 10(5),

609–618. https://doi.org/10.5194/hess-10-609-2006

Brinkerhoff, C. B., Gleason, C. J., Feng, D., & Lin, P. (2020). Constraining remote river discharge estimation using reach‐scale geomorphology.

Water Resources Research, 56(11), e2020WR027949. https://doi.org/10.1029/2020wr027949

Brinkerhoff, C. B., Gleason, C. J., Zappa, C. J., Raymond, P. A., & Harlan, M. E. (2022). Remotely sensing river greenhouse gas exchange

velocity using the SWOT satellite. Global Biogeochemical Cycles, 36(10), e2022GB007419. https://doi.org/10.1029/2022GB007419

Carr, A. B., Trigg, M. A., Tshimanga, R. M., Borman, D. J., & Smith, M. W. (2019). Greater water surface variability revealed by new Congo river
field data: Implications for satellite altimetry measurements of large rivers. Geophysical Research Letters, 46(14), 8093–8101. https://doi.org/
10.1029/2019GL083720

Chidamba, L., Cilliers, E., & Bezuidenhout, C. C. (2016). Spatial and temporal variations in pollution indicator bacteria in the lower Vaal River,

South Africa. Water Environment Research, 88(11), 2142–2149. https://doi.org/10.2175/106143016X14733681695528

Coxon, G., Freer, J., Westerberg, I. K., Wagener, T., Woods, R., & Smith, P. J. (2015). A novel framework for discharge uncertainty quantification

applied to 500 UK gauging stations. Water Resources Research, 51(7), 5531–5546. https://doi.org/10.1002/2014wr016532

Durand, M., Dai, C., Moortgat, J., Yadav, B., de Moraes Frasson, R. P., Li, Z., et al. (2024). Using river hypsometry to improve remote sensing of

river discharge. Remote Sensing of Environment, 315, 114455. https://doi.org/10.1016/j.rse.2024.114455

Durand, M., Gleason, C. J., Garambois, P. A., Bjerklie, D., Smith, L. C., Roux, H., et al. (2016). An intercomparison of remote sensing river
discharge estimation algorithms from measurements of river height, width, and slope. Water Resources Research, 52(6), 4527–4549. https://
doi.org/10.1002/2015WR018434

Durand, M., Gleason, C. J., Pavelsky, T. M., Frasson, R. P. D. M., Turmon, M., David, C. H., et al. (2023). A framework for estimating global river
discharge from the surface water and ocean topography satellite mission. Water Resources Research, 59(4), e2021WR031614. https://doi.org/
10.1029/2021WR031614

Durand, M., Rodríguez, E., Alsdorf, D. E., & Trigg, M. (2010). Estimating River depth from remote sensing swath interferometry measurements
of river height, slope, and width. IEEE Journal of Selected Topics in Applied Earth Observations and Remote Sensing, 3(1), 20–31. https://doi.
org/10.1109/jstars.2009.2033453

Feng, D., Gleason, C. J., Lin, P., Yang, X., Pan, M., & Ishitsuka, Y. (2021). Recent changes to Arctic river discharge. Nature Communications,

12(1), 6917. https://doi.org/10.1038/s41467-021-27228-1

Frasson, R. P. D. M., Durand, M. T., Larnier, K., Gleason, C., Andreadis, K. M., Hagemann, M., et al. (2021). Exploring the factors controlling the
error characteristics of the surface water and ocean topography mission discharge estimates. Water Resources Research, 57(6),
e2020WR028519. https://doi.org/10.1029/2020WR028519

Frasson, R. P. D. M., Schumann, G. J., Kettner, A. J., Brakenridge, G. R., & Krajewski, W. F. (2019). Will the Surface Water and Ocean
Topography (SWOT) satellite mission observe floods? Geophysical Research Letters, 46(17–18), 10435–10445. https://doi.org/10.1029/
2019GL084686

Frasson, R. P. D. M., Turmon, M. J., Durand, M. T., & David, C. H. (2023). Estimating the relative impact of measurement, parameter, and flow
law errors on discharge from the Surface Water and Ocean Topography mission. Journal of Hydrometeorology, 24(3), 425–443. https://doi.org/
10.1175/JHM-D-22-0078.1

Frasson, R. P. D. M., Wei, R., Durand, M., Minear, J. T., Domeneghetti, A., Schumann, G., et al. (2017). Automated river reach definition
strategies: Applications for the Surface Water and Ocean Topography mission. Water Resources Research, 53(10), 8164–8186. https://doi.org/
10.1002/2017WR020887

Fu, L.‐L., Pavelsky, T., Cretaux, J.‐F., Morrow, R., Farrar, J. T., Vaze, P., et al. (2024). The Surface Water and Ocean Topography mission: A
breakthrough in radar remote sensing of the ocean and land surface water. Geophysical Research Letters, 51(4), e2023GL107652. https://doi.
org/10.1029/2023GL107652

Garambois, P.‐A., Calmant, S., Roux, H., Paris, A., Monnier, J., Finaud‐Guyot, P., et al. (2016). Hydraulic visibility: Using satellite altimetry to
parameterize a hydraulic model of an ungauged reach of a braided river. Hydrological Processes, 31(4), 756–767. https://doi.org/10.1002/hyp.
11033

Gejadze, I., Malaterre, P. O., Oubanas, H., & Shutyaev, V. (2022). A new robust discharge estimation method applied in the context of SWOT

satellite data processing. Journal of Hydrology, 610, 127909. https://doi.org/10.1016/j.jhydrol.2022.127909

Getirana, A., & Peters‐Lidard, C. (2013). Estimating water discharge from large radar altimetry datasets. Hydrology and Earth System Sciences,

17(3), 923–933. https://doi.org/10.5194/hess-17-923-2013

Gleason, C. J., & Durand, M. (2020). Remote sensing of river discharge: A review and a framing for the discipline. Remote Sensing, 12(7), 1107.

https://doi.org/10.3390/rs12071107

Gleason, C. J., & Hamdan, A. N. (2017). Crossing the (watershed) divide: Satellite data and the changing politics of international river basins. The

Geographical Journal, 183(1), 2–15. https://doi.org/10.1111/geoj.12155

Gleason, C. J., & Smith, L. C. (2014). Toward global mapping of river discharge using satellite images and at‐many‐stations hydraulic geometry.
Proceedings of the National Academy of Sciences of the United States of America, 111(13), 4788–4791. https://doi.org/10.1073/pnas.
1317606111

Gleason, C. J., Smith, L. C., & Lee, J. (2014). Retrieval of river discharge solely from satellite imagery and at‐many‐stations hydraulic geometry:
Sensitivity to river form and optimization parameters. Water Resources Research, 50(12), 9604–9619. https://doi.org/10.1002/2014wr016109
Horner, I., Renard, B., Le Coz, J., Branger, F., McMillan, H. K., & Pierrefeu, G. (2018). Impact of stage measurement errors on streamflow

uncertainty. Water Resources Research, 54(3), 1952–1976. https://doi.org/10.1002/2017WR022039

Ishitsuka, Y., Gleason, C. J., Hagemann, M. W., Beighley, E., Allen, G. H., Feng, D., et al. (2021). Combining optical remote sensing, McFLI
discharge estimation, global hydrologic modeling, and data assimilation to improve daily discharge estimates across an entire large watershed.
Water Resources Research, 57(3), e2020WR027794. https://doi.org/10.1029/2020wr027794

JPL. (2018). SWOT project science requirements document. (Tech. Rep.). California Institute of Technology. Retrieved from https://podaac.jpl.

nasa.gov/SWOT?tab=related-links&sections=about

JPL. (2020). SWOT product description: Level 2 Karin high rate river single pass vector product. (Tech. Rep.). California Institute of Technology.

Retrieved from https://podaac.jpl.nasa.gov/SWOT?tab=datasets-information&sections=about

ANDREADIS ET AL.

10 of 11

 19448007, 2025, 9, Downloaded from https://agupubs.onlinelibrary.wiley.com/doi/10.1029/2024GL114185, Wiley Online Library on [14/06/2026]. See the Terms and Conditions (https://onlinelibrary.wiley.com/terms-and-conditions) on Wiley Online Library for rules of use; OA articles are governed by the applicable Creative Commons LicenseGeophysical Research Letters

10.1029/2024GL114185

JPL. (2024). SWOT science data products user handbook. (Tech. Rep.). California Institute of Technology. Retrieved from https://podaac.jpl.

nasa.gov/SWOT?tab=datasets-information&sections=about

Kiang, J. E., Gazoorian, C., McMillan, H., Coxon, G., Le Coz, J., Westerberg, I. K., et al. (2018). A comparison of methods for streamflow

uncertainty estimation. Water Resources Research, 54(10), 7149–7176. https://doi.org/10.1029/2018WR022708

King, T. V., Neilson, B. T., Overbeck, L. D., & Kane, D. L. (2020). A distributed analysis of lateral inflows in an Alaskan Arctic watershed

underlain by continuous permafrost. Hydrological Processes, 34(3), 633–648. https://doi.org/10.1002/hyp.13611

Krabbenhoft, C. A., Allen, G. H., Lin, P., Godsey, S. E., Allen, D. C., Burrows, R. M., et al. (2022). Assessing placement bias of the global river

gauge network. Nature Sustainability, 5(7), 586–592. https://doi.org/10.1038/s41893-022-00873-0

Larnier, K., & Monnier, J. (2023). Hybrid neural network‐variational data assimilation algorithm to infer river discharges from SWOT‐like data.

Computational Geosciences, 27(5), 853–877. https://doi.org/10.1007/s10596-023-10225-2

Larnier, K., Monnier, J., Garambois, P.‐A., & Verley, J. (2021). River discharge and bathymetry estimation from SWOT altimetry measurements.

Inverse Problems in Science and Engineering, 29(6), 759–789. https://doi.org/10.1080/17415977.2020.1803858

Li, D., Xue, Y., Qin, C., Wu, B., Chen, B., & Wang, G. (2022). A bankfull geometry dataset for major exorheic rivers on the Qinghai‐Tibet

Plateau. Scientific Data, 9(1), 498. https://doi.org/10.1038/s41597-022-01614-w

Lin, P., Feng, D., Gleason, C. J., Pan, M., Brinkerhoff, C. B., Yang, X., et al. (2023). Inversion of river discharge from remotely sensed river
widths: A critical assessment at three‐thousand global river gauges. Remote Sensing of Environment, 287, 113489. https://doi.org/10.1016/j.rse.
2023.113489

Osadchiev, A., Medvedev, I., Shchuka, S., Kulikov, M., Spivak, E., Pisareva, M., & Semiletov, I. (2020). Influence of estuarine tidal mixing on

structure and spatial scales of large river plumes. Ocean Science, 16(4), 781–798. https://doi.org/10.5194/os-16-781-2020

Paiva, R. C. D., Durand, M. T., & Hossain, F. (2015). Spatiotemporal interpolation of discharge across a river network by using synthetic SWOT

satellite data. Water Resources Research, 51(1), 430–449. https://doi.org/10.1002/2014WR015618

Pan, M., & Wood, E. F. (2013). Inverse streamflow routing. Hydrology and Earth System Sciences, 17(11), 4577–4588. https://doi.org/10.5194/

hess-17-4577-2013

Papa, F., Prigent, C., & Rossow, W. B. (2008). Monitoring flood and discharge variations in the large Siberian rivers from a multi‐satellite

technique. Surveys in Geophysics, 29(4), 297–317. https://doi.org/10.1007/s10712-008-9036-0

Paris, A., Dias de Paiva, R., Santos da Silva, J., Medeiros Moreira, D., Calmant, S., Garambois, P., et al. (2016). Stage‐discharge rating curves
based on satellite altimetry and modeled discharge in the Amazon basin. Water Resources Research, 52(5), 3787–3814. https://doi.org/10.1002/
2014WR016618

Pavelsky, T. M., Durand, M. T., Andreadis, K. M., Beighley, R. E., Paiva, R. C. D., Allen, G. H., & Miller, Z. F. (2014). Assessing the potential
global extent of SWOT river discharge observations. Journal of Hydrology, 519, 1516–1525. https://doi.org/10.1016/j.jhydrol.2014.08.044
Pujol, L., Garambois, P.‐A., Finaud‐Guyot, P., Monnier, J., Larnier, K., Mosé, R., et al. (2020). Estimation of multiple inflows and effective
channel by assimilation of multi‐satellite hydraulic signatures: The ungauged Anabranching Negro River. Journal of Hydrology, 591, 125331.
https://doi.org/10.1016/j.jhydrol.2020.125331

Revel, M., Ikeshima, D., Yamazaki, D., & Kanae, S. (2021). A framework for estimating global‐scale river discharge by assimilating satellite

altimetry. Water Resources Research, 57(1), e2020WR027876. https://doi.org/10.1029/2020WR027876

Rodríguez, E., Durand, M., & Frasson, R. P. D. M. (2020). Observing rivers with varying spatial scales. Water Resources Research, 56(9),

e2019WR026476. https://doi.org/10.1029/2019wr026476

Segura, C., & Pitlick, J. (2015). Coupling fluvial‐hydraulic models to predict gravel transport in spatially variable flows. Journal of Geophysical

Research: Earth Surface, 120(5), 834–855. https://doi.org/10.1002/2014JF003302

Smith, L. C., Isacks, B. L., Bloom, A. L., & Murray, A. B. (1996). Estimation of discharge from three braided rivers using synthetic aperture radar
satellite imagery: Potential application to ungaged basins. Water Resources Research, 32(7), 2021–2034. https://doi.org/10.1029/96WR00752
Stuurman, C. (2024). River product water surface elevation (WSE), and slope validation, features and issues. In Presented at the 2024 SWOT
science Team meeting, June 19, 2024. University of North Carolina. Retrieved from https://drive.google.com /drive /folders /
1aIyIwZ4YPscexXqFpN8J8liFlRi9piDe

SWOT. (2024). SWOT level 2 river single‐pass vector data product [Dataset]. NASA Physical Oceanography Distributed Active Archive Center.

https://doi.org/10.5067/SWOT-RIVERSP-2.0

SWOT Discharge Algorithm Working Group. (2023). SWOT sword of science river discharge products version 1 [Dataset]. NASA Physical

Oceanography Distributed Active Archive Center. https://doi.org/10.5067/SWOT-SOS-V1

Tarpanelli, A., Camici, S., Nielsen, K., Brocca, L., Moramarco, T., & Benveniste, J. (2021). Potentials and limitations of Sentinel‐3 for river

discharge assessment. Advances in Space Research, 68(2), 593–606. https://doi.org/10.1016/j.asr.2019.08.005

Tarpanelli, A., & Domeneghetti, A. (2021). Flow duration curves from surface reflectance in the near infrared band. Applied Sciences, 11(8), 3458.

https://doi.org/10.3390/app11083458

Tourian, M. J., Schwatke, C., & Sneeuw, N. (2017). River discharge estimation at daily resolution from satellite altimetry over an entire river

basin. Journal of Hydrology, 546, 230–247. https://doi.org/10.1016/j.jhydrol.2017.01.009

Van Dijk, A. I. J. M., Brakenridge, G. R., Kettner, A. J., Beck, H. E., De Groeve, T., & Schellekens, J. (2016). River gauging at global scale using

optical and passive microwave remote sensing. Water Resources Research, 52(8), 6404–6418. https://doi.org/10.1002/2015WR018545

Wegscheider, B., Linnansaari, T., Ndong, M., Haralampides, K., St‐Hilaire, A., Schneider, M., & Curry, R. A. (2024). Fish habitat modelling in
large rivers: Combining expert opinion and hydrodynamic modelling to inform river management. Journal of Ecohydraulics, 9(1), 68–86.
https://doi.org/10.1080/24705357.2021.1938251

References From the Supporting Information

Durand, M., Chen, C., Frasson, R. P. D. M., Pavelsky, T. M., Williams, B., Yang, X., & Fore, A. (2020). How will radar layover impact SWOT
measurements of water surface elevation and slope, and estimates of river discharge? Remote Sensing of Environment, 247, 111883. https://doi.
org/10.1016/j.rse.2020.111883

ANDREADIS ET AL.

11 of 11

 19448007, 2025, 9, Downloaded from https://agupubs.onlinelibrary.wiley.com/doi/10.1029/2024GL114185, Wiley Online Library on [14/06/2026]. See the Terms and Conditions (https://onlinelibrary.wiley.com/terms-and-conditions) on Wiley Online Library for rules of use; OA articles are governed by the applicable Creative Commons License