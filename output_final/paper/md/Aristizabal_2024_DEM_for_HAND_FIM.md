Hydrol. Earth Syst. Sci., 28, 1287–1315, 2024
https://doi.org/10.5194/hess-28-1287-2024
© Author(s) 2024. This work is distributed under
the Creative Commons Attribution 4.0 License.

Effects of high-quality elevation data and explanatory
variables on the accuracy of ﬂood inundation
mapping via Height Above Nearest Drainage

Fernando Aristizabal1,2,3, Taher Chegini4, Gregory Petrochenkov2,5, Fernando Salas2, and Jasmeet Judge3
1Earth Resources Technology, 14401 Sweitzer Lane Suite 300, Laurel, MD 20707, USA
2National Water Center, Ofﬁce of Water Prediction, National Oceanic and Atmospheric Administration,
205 Hackberry Ln, Tuscaloosa, AL 35401, USA
3Center for Remote Sensing, Agricultural and Biological Engineering,
University of Florida, 1741 Museum Rd, Gainesville, FL 32603, USA
4Civil and Environmental Engineering, University of Houston, 4226 Martin Luther King Boulevard,
Houston, TX 77204, USA
5Lynker, 338 E Market St, Leesburg, VA 20176, USA

Correspondence: Fernando Aristizabal (fernando.aristizabal@noaa.gov)

Received: 25 June 2023 – Discussion started: 10 July 2023
Revised: 17 November 2023 – Accepted: 5 January 2024 – Published: 22 March 2024

Abstract. Given the availability of high-quality and high-
spatial-resolution digital elevation maps (DEMs)
from
the United States Geological Survey’s 3D Elevation Pro-
gram (3DEP), derived mostly from light detection and rang-
ing (lidar) sensors, we examined the effects of these DEMs
at various spatial resolutions on the quality of ﬂood inunda-
tion map (FIM) extents derived from a terrain index known
as Height Above Nearest Drainage (HAND). We found that
using these DEMs improved the quality of resulting FIM
extents at around 80 % of the catchments analyzed when
compared to using DEMs from the National Hydrography
Dataset Plus High Resolution (NHDPlusHR) program. Addi-
tionally, we varied the spatial resolution of the 3DEP DEMs
at 3, 5, 10, 15, and 20 m (meters), and the results showed
no signiﬁcant overall effect on FIM extent quality across
resolutions. However, further analysis at coarser resolutions
of 60 and 90 m revealed a signiﬁcant degradation in FIM
skill, highlighting the limitations of using extremely coarse-
resolution DEMs. Our experiments demonstrated a signiﬁ-
cant burden in terms of the computational time required to
produce HAND and related data at ﬁner resolutions. We ﬁt a
multiple linear regression model to help explain catchment-
scale variations in the four metrics employed and found that
the lack of reservoir ﬂooding or inundation upstream of river

retention systems was a signiﬁcant factor in our analysis. For
validation, we used Interagency Flood Risk Management (In-
FRM) Base Level Engineering (BLE)-produced FIM extents
and streamﬂows at the 100- and 500-year event magnitudes
in a sub-region in eastern Texas.

1

Introduction

Floods are among the most frequent, damaging, and deadly
of natural disasters (Doocy et al., 2013; Strömberg, 2007;
Kahn, 2005). The frequency and intensity of ﬂood events, as
well as the exposure of people and property to them, have
been increasing in recent times, driven by secular changes in
climate, infrastructure, and demographics (Berz, 2000; Mal-
lakpour and Villarini, 2015; Downton et al., 2005; Kunkel
et al., 1999; Pielke and Downton, 2000; Corringham and
Cayan, 2019; Gourevitch et al., 2023). These upward trends
are expected to continue placing additional pressure on hy-
drological extremes (Kahn, 2005; Tabari, 2020; Milly et al.,
2002; Wing et al., 2018; Gourevitch et al., 2023). Floods
impact mortality and morbidity through drowning or physi-
cal trauma at the individual-health scale while increasing the
risk of infectious disease at the public-health level (Jonkman,

Published by Copernicus Publications on behalf of the European Geosciences Union.

1288

F. Aristizabal et al.: Effects of high-quality elevation data and other variables on FIM skill

2005; Beinin, 2012; Alajo et al., 2006; French et al., 1983).
Flooding disrupts systems that provide for human needs
such as transportation routes, supply chains, water deliv-
ery, waste management, communications, shelter, and energy
grids (Wijkman and Timberlake, 2021; Gourevitch et al.,
2023). These impacts disproportionately affect certain de-
mographics such as the socioeconomically disadvantaged,
youth, and elderly, who are more likely to live in vulner-
able areas with less access to educational resources, early-
warning systems, and the capacity or resources to evacuate
impacted areas (Kahn, 2005; Smiley et al., 2022; Strömberg,
2007; Jonkman, 2005; Tellman et al., 2020, 2021). These
inequitable impacts further entrench poverty and inequal-
ities (Stallings, 1988; Birkmann et al., 2010). In political
terms, severe disasters, including ﬂoods, can reduce social
order, strain governance systems, collapse social safety nets,
and increase the risk of social conﬂict (Drury and Olson,
1998; Xu et al., 2016; Zahran et al., 2009). These dire con-
sequences motivate adaption and mitigation efforts such as
early-warning systems, protective infrastructure (e.g., stor-
age, defenses, drainage, inﬁltration), public awareness and
education, and zoning regulations (Tumbare, 2000; Tauhid
and Zawani, 2018; Charlesworth and Warwick, 2011).

Due to these growing ﬂood risks, early-warning systems or
forecasting systems can help in understanding future condi-
tions and can provide intelligence to furnish adequate warn-
ings to protect life, prevent damage, and enhance resilience
(Strömberg, 2007; Cools et al., 2016; UNISDR, 2015; Bau-
doin et al., 2014; Golnaraghi, 2012; UNEP, 2012; C. Liu
et al., 2018; Schumann et al., 2013). The early warning of
ﬂood disasters at national scales often requires the use of
continental-scale forecast hydrology models and modeling
frameworks that span intranational political boundaries. The
applications of these models extend beyond early-warning
systems to providing historical trends for applications in in-
frastructure planning, public planning, insurance underwrit-
ing, and more. The Ofﬁce of Water Prediction (OWP), an
ofﬁce of the National Oceanic and Atmospheric Adminis-
tration (NOAA), along with partners at the National Cen-
ter for Atmospheric Research (NCAR), developed such a
continental-scale model known as the United States (US)
National Water Model (NWM) (Salas et al., 2018; Gochis
et al., 2021; Cosgrove et al., 2019; Cohen et al., 2018;
NOAA, 2016; Ofﬁce of Water Prediction, 2022). The NWM
is based on a conﬁguration of the Weather Research and
Forecasting Hydro (WRF-Hydro) model that accounts for
land surface processes, as well as overland and channel rout-
ing (Gochis et al., 2021; Salas et al., 2018; Cosgrove et al.,
2019). Operationally, the NWM produces streamﬂow anal-
ysis and forecasts at multiple time horizons depending on
location, which includes the conterminous US (CONUS),
Puerto Rico, Hawaii, and portions of Alaska (Cosgrove et al.,
2019; NOAA, 2016; Ofﬁce of Water Prediction, 2022). The
NWM routes streamﬂow across the NWM Version 2.1 (V2.1)
stream network, which is based on the National Hydrogra-

phy Dataset Plus Version 2 (NHDPlusV2) network and is
comprised of more than 5.5 × 106 km (kilometers) of lines
discretized into more than 2.8 million forecast points (Aris-
tizabal et al., 2023c). The NWM V2.1 stream network be-
longs to the NWM “hydrofabric”, deﬁned as a catalog of
geospatial layers relevant to hydrology modeling, including
stream network ﬂow paths, catchments, reservoirs, and more
(Ofﬁce of Water Prediction, 2022; Cosgrove et al., 2019).
While streamﬂow is an important variable for engineering
and scientiﬁc applications of ﬂuvial ﬂooding, ﬂood inunda-
tion stages, extents, and depths are much more tangible vari-
ables to the stakeholders that ﬂood events directly impact.

The shallow-water equations, a system of two hyperbolic
partial differential equations, formally govern the ﬂow of
ﬂuvial surface water by conserving both mass (ﬁrst equa-
tion) and momentum (second equation) and can be ex-
pressed in both one-dimensional (1D) (Saint-Venant equa-
tions) and two-dimensional (2D) forms. Solving this sys-
tem in full 2D form requires numerical methods that can be
very cost prohibitive and numerically unstable in an oper-
ational setting across continental scales at high spatial dis-
cretizations (10 m (meters) or higher). This use case moti-
vates the implementation of an inundation proxy, also known
as a zero-physics or simpliﬁed conceptual model, that is ag-
nostic to the shallow-water equations while still computing
accurate ﬂuvial inundation extents and depths (Teng et al.,
2015; Bates and De Roo, 2000). Height Above Nearest
Drainage (HAND) de-trends elevations within digital eleva-
tion models (DEMs) to compute drainage potentials by nor-
malizing elevations to the nearest relevant ﬂow path instead
of data that represent mean sea level (Rennó et al., 2008; No-
bre et al., 2011, 2016). HAND, as a terrain index, has been
used extensively for producing ﬂood inundation maps (FIMs)
from both modeled or observed streamﬂows and stages (No-
bre et al., 2016; Afshari et al., 2018; Garousi-Nejad et al.,
2019; Johnson et al., 2019; Zheng et al., 2018a, b; Zhang
et al., 2018; Teng et al., 2015; Li et al., 2022), as well as for
assisting in the remote sensing detection of ﬂuvial inundation
(Aristizabal et al., 2020; Shastry et al., 2019; Aristizabal and
Judge, 2021; Huang et al., 2017; Twele et al., 2016). HAND
operates as an inundation proxy by thresholding the relative
elevation (or HAND) values with a singular river stage value
for each catchment, corresponding to the drainage area of a
given river reach (Nobre et al., 2016; Garousi-Nejad et al.,
2019; Johnson et al., 2019; Zheng et al., 2018a; Teng et al.,
2015; Liu et al., 2016; Maidment, 2017; Y. Y. Liu et al., 2018;
Liu et al., 2020; C. Liu et al., 2018). When used to gener-
ate inundation extents and depths from streamﬂow, reach-
averaged synthetic rating curves (SRCs) sample geometric
variables along an entire reach and normalize these using the
length of the reach to create stage–discharge relationships
(Zheng et al., 2018b; Aristizabal et al., 2023c; Godbout et al.,
2019). These relationships depend on the friction parameter,
Manning’s n, and are used to convert streamﬂows to stages
for eventual 2D mapping with HAND. Numerous investiga-

Hydrol. Earth Syst. Sci., 28, 1287–1315, 2024

https://doi.org/10.5194/hess-28-1287-2024

F. Aristizabal et al.: Effects of high-quality elevation data and other variables on FIM skill

1289

tions have validated the use of HAND for ﬂood-mapping
applications as a suitable alternative to more sophisticated
physics-based techniques for large-scale and high-resolution
use cases (Johnson et al., 2019; Li et al., 2023; Aristizabal
et al., 2023c; Nobre et al., 2016; Godbout et al., 2019; Af-
shari et al., 2018; Zhang et al., 2018; Teng et al., 2015, 2017;
Diehl et al., 2021; Hocini et al., 2021; Bates et al., 2003).

Several prior and active large-scale HAND implementa-
tions catered to operational early-warning-system applica-
tions, including the National Flood Interoperability Experi-
ment (NFIE) (Maidment, 2017; Liu et al., 2016; Y. Y. Liu
et al., 2018), GeoFlood (Zheng et al., 2018a; Hocini et al.,
2021; D’Angelo et al., 2022; Carruthers, 2021; Zheng et al.,
2022), and PyGFT (Petrochenkov and Viger, 2020; Verdin
et al., 2016). The NFIE was a broad, inter-institutional, and
pioneering effort to apply HAND to the initial versions of the
NWM, which leveraged 1/3 arcsec (10 m) seamless elevation
data available at the time (Maidment, 2017; Liu et al., 2016;
Y. Y. Liu et al., 2018) from the USGS’s National Elevation
Dataset (NED) (Gesch et al., 2002; Gesch and Maune, 2007).
Zheng et al. (2018a) applied HAND to operational applica-
tions with 1/27 arcsec (1 m) elevation data with a novel least-
cost, geodesic-based stream delineation method (Passalac-
qua et al., 2010, 2012; Zheng et al., 2018a, 2019; Carruthers,
2021; D’Angelo et al., 2022; Zheng et al., 2022). For applica-
tions with the NWM, an advanced version of HAND coupled
with the use of SRCs, known as OWP FIM, converts NWM
analysis, reanalysis, and forecast streamﬂows to river stages
and operationally based ﬂuvial inundation depths and extents
to CONUS while extending the modeling domain to Puerto
Rico and Hawaii (Aristizabal et al., 2023c, b). OWP FIM
utilizes some of the latest datasets, including the National
Hydrography Dataset Plus High Resolution (NHDPlusHR)
(Moore et al., 2019), the National Levee Database (NLD)
(US Army Corps of Engineers, 2021), and the NWM V2.1
hydrofabric (Ofﬁce of Water Prediction, 2022; NOAA, 2016;
OWP/ESIP, 2021; Gochis et al., 2021). These datasets en-
force hydrologically relevant features such as levees and the
general location of ﬂow paths to facilitate conﬂation with the
forecast stream network (Aristizabal et al., 2023c, b). Ad-
ditionally, OWP FIM advanced a fundamental limitation of
HAND that limits sourcing ﬂuvial inundation to be from only
the nearest relevant ﬂow path (McGehee et al., 2016; Aristi-
zabal et al., 2023c; Zhang et al., 2018; Li et al., 2023; Zheng
et al., 2018a, b; Nobre et al., 2016). Flow paths of higher
Horton–Strahler stream order that could contribute inunda-
tion to a given area have no way of extending beyond catch-
ment lines, which creates artiﬁcial bottlenecks in inundation
extents, especially along junctions of high-order rivers with
their lower-ﬂow tributaries (Aristizabal et al., 2023c; McGe-
hee et al., 2016). To resolve this limitation, OWP FIM disag-
gregates the NWM V2.1 stream network into segments of ef-
fective unit stream order referred to as level paths in a version
of HAND called Generalized Mainstems (GMS) (Aristizabal
et al., 2023c). In terms of terrain data, OWP FIM uses the

10 m DEM from the NHDPlusHR elevation dataset, which is
the elevation basis, derived in batches from the 3D Elevation
Program (3DEP), for additional hydrography products within
the NHDPlusHR (Aristizabal et al., 2023c; Moore et al.,
2019). The previous advances in OWP FIM stopped short
of accounting for light detection and ranging (lidar) point el-
evation observations (Aristizabal et al., 2023c) that are now
nearing their ﬁrst collection cycle to form a novel, seamless,
continental-scale DEM from 3DEP (USGS, 2021b, 2022a).
Broad-scale terrain information in the form of DEMs is
fundamental to all FIM models and has a signiﬁcant inﬂu-
ence on inundation skill (Bales and Wagner, 2009; Dobbs,
2010; Wang and Zheng, 2005; Merwade et al., 2008; Witt,
2015; Garousi-Nejad et al., 2019; Li et al., 2022; Neal
et al., 2011). The National Geospatial Program, under the
USGS, is the primary authority on collecting, processing,
and maintaining terrestrial elevation data within the US in
collaboration with federal partners within the National Digi-
tal Elevation Program (NDEP) (Ofﬁce of Management and
Budget, 2016; Dewberry, 2011; National Research Coun-
cil, 2007, 2009; Sugarbaker et al., 2014). The NED (Gesch
et al., 2002; Gesch and Maune, 2007) forms the seamless
elevation layers of The National Map (TNM) (Gesch et al.,
2009; Archuleta et al., 2017; S. Arundel et al., 2015; Arun-
del et al., 2018; Kelmelis et al., 2003). Prior to the introduc-
tion of 3DEP, TNM was originally composed of three seam-
less DEMs at 1/3 (10 m), 1 (30 m), and 2 (90 m) arcsec res-
olutions produced from a variety of legacy sources includ-
ing digital photogrammetry, cartographic contours, mapped
hydrography, and elevations from the Shuttle Radar To-
pography Mission (SRTM) (Gesch et al., 2002; Gesch and
Maune, 2007; S. Arundel et al., 2015). High-quality eleva-
tions derived from lidar and interferometric synthetic aper-
ture radar (InSAR) have been integrated into TNM seam-
less elevation products, as made available prior to and after
the introduction of 3DEP (Snyder et al., 2013; Gesch et al.,
2002; S. Arundel et al., 2015). Work by Gesch et al. (2014),
Gesch and Maune (2007), and Dobbs (2010) illustrated that
the inclusion of higher-quality elevation data sources brought
about a signiﬁcant improvement in the accuracy of NED
data when compared to the National Geodetic Survey (NGS)
(Roman et al., 2010). Gesch et al. (2014) identiﬁed that the
NED 1/3 arcsec DEM, as of April 2013, had a mean error of
−0.29 m, with a root mean squared error (RMSE) of 1.55 m,
when compared to over 25 000 reference points. At the time
of evaluation, the NED was subject to legacy, lower-quality
data sources dating back almost a century in the past (Sug-
arbaker et al., 2014; Gesch et al., 2014; Gesch and Maune,
2007). This reduction in error and its impact on people and
commerce (Dewberry, 2011) motivated action on the collec-
tion of elevation data from higher-quality data sources (Sug-
arbaker et al., 2014).

The 3DEP is a national, multi-organizational effort by the
NDEP to survey elevations with high-quality sensors on a
recurring collection cycle of no more than 8 years in re-

https://doi.org/10.5194/hess-28-1287-2024

Hydrol. Earth Syst. Sci., 28, 1287–1315, 2024

1290

F. Aristizabal et al.: Effects of high-quality elevation data and other variables on FIM skill

sponse to growing stakeholder needs (Dewberry, 2011; Sny-
der et al., 2013; Sugarbaker et al., 2014). The 3DEP lever-
ages two main collection technologies, including lidar for the
CONUS, Hawaii, and US territories and InSAR for Alaska.
The lidar, the collection source of focus in this study, is a light
emission, reﬂection, and collection technology that beams
concentrated, powerful light of wavelengths between 1000–
1600 nm (nanometers) (Muhadi et al., 2020). The reﬂection
of the light is collected while recording the travel time and in-
tensity of return; lidar sensors are mounted on top of a variety
of mobile or static platforms whose positions are geo-tracked
as they collect lidar returns (Passalacqua et al., 2015). The
travel time of the returns, along with knowledge of the speed
of light, serves as a relative positioning of the target(s) refer-
enced to a common vertical datum, while the intensities serve
as indicators of what the target(s) represents. Modes within
the relationship of return intensities with respect to travel
time or distance from the lidar wave forms can be indicative
of vegetation or other land uses and land covers (LULCs) that
reﬂect signals at varying distances and magnitudes and inﬂu-
ence elevation errors (Gesch et al., 2014). These modes can
be discretized into varying DEM products representing bare
earth, structures, or canopy elevations. The horizontal and
vertical accuracies and the horizontal resolutions of terrain
observations derived from lidar, and even the consequential
economic beneﬁts (Dewberry, 2011, 2022), are dependent on
a variety of sensor, platform, target, and collection speciﬁ-
cations and practices, such as nominal pulse spacing, nom-
inal pulse density, and the LULC of the target (Heidemann,
2018; Passalacqua et al., 2015; Smith et al., 2019; Salach
et al., 2018; Gesch et al., 2014). The lidar produces point
cloud datasets, which are scattered, geo-referenced points
representing full wave forms or discretized return intensities.
Various assessments of the vertical accuracies of lidar point
clouds have yielded satisfactory results in agreement with
3DEP requirements (Stoker and Miller, 2022; Kim et al.,
2022; Callahan and Berber, 2022; Kim et al., 2022; Salach
et al., 2018; Passalacqua et al., 2015). Point clouds must un-
dergo a series of operations to produce analysis-ready, seam-
less DEMs (Passalacqua et al., 2015).

The 3DEP extends TNM to include a 1/27 arcsec (1 m),
lidar-derived DEM product for CONUS, Hawaii, and US ter-
ritories, as well as a 1/2 arcsec (5 m) DEM derived from In-
SAR for Alaska (Sugarbaker et al., 2014; Stoker et al., 2015).
To create bare-earth DEMs, lidar observations must undergo
a series of processes that ﬁlter out returns from vegetation,
anthropogenic, and other features and then grid the obser-
vations with resampling methods (Passalacqua et al., 2015).
The 1 m 3DEP product is a hydrologically ﬂattened, topo-
graphic, and bare-earth raster DEM gridded to 1 km square-
shaped tiles with 6 pixels of overlap (S. T. Arundel et al.,
2015). Hydro-ﬂattening refers to a process in which hy-
drologic features such as lakes, reservoirs, streams, rivers,
and more are ﬂattened in elevation for bathymetric regions
from lower bank to lower bank, as represented by break

lines (Archuleta et al., 2017; Maune and Nayegandhi, 2018).
This ﬂattening excludes along-gradient directions, parallel to
the direction of the break lines, for hydrologic features that
naturally exhibit water conveyance such as streams, rivers,
and long reservoirs (S. T. Arundel et al., 2015). This pro-
cess includes elevations underneath bridges that are not ac-
curately observed by topographic lidar (Bales and Wagner,
2009). According to speciﬁcations, the horizontal accuracy
of the 1 m 3DEP is within 1 m, while the vertical accuracies
are within 19.6 and 30 cm (centimeters) at the 95 % conﬁ-
dence interval for non-vegetative and vegetative regions, re-
spectively (S. T. Arundel et al., 2015; Heidemann, 2018).
Non-vegetative vertical accuracies fall within an RMSE of
10 cm (S. T. Arundel et al., 2015; Heidemann, 2018). Work
by Stoker and Miller (2022), Callahan and Berber (2022),
and Kim et al. (2022) has veriﬁed the vertical accuracies and
general quality of the DEMs for 3DEP speciﬁcations.

The quality of FIM extents is subject to a wide variety of
terrain-related factors including collection technology, grid-
ding methods, resampling techniques, hydrological condi-
tioning processes, presence of bathymetry, vertical accura-
cies, and horizontal resolutions (Merwade et al., 2008). The
main enhancement of including 3DEP data within HAND-
based OWP FIM is the broader availability of high-quality
data sources for elevations, such as lidar with enhanced verti-
cal accuracies and horizontal resolutions (S. T. Arundel et al.,
2015; Stoker and Miller, 2022; Archuleta et al., 2017). Gen-
erally speaking, with regard to the quality of FIM extents, the
literature has demonstrated the sensitivity to, and improved
effect of, using 3DEP or lidar data, mostly due to the en-
hanced vertical accuracies that these data sources provide
(Podhorányi and Fedorcak, 2015; Bales and Wagner, 2009;
Merwade et al., 2008; Witt, 2015; Mason et al., 2007; Zheng
et al., 2018a). Limitations have been noted with respect to
vertical accuracies in areas with vegetation, buildings, or
bridges and/or areas that have been classiﬁed as bathymetric
(Merwade et al., 2008; Mason et al., 2007; Bales and Wag-
ner, 2009; Podhorányi and Fedorcak, 2015). FIM extents in
areas of low topographic relief or areas behind natural or an-
thropogenic ﬂow divides can be very sensitive to vertical ac-
curacies (Sanyal and Lu, 2004; Garousi-Nejad et al., 2019;
Godbout et al., 2019; Jafarzadegan and Merwade, 2017; Pa-
paioannou et al., 2017). Speciﬁcally for HAND, research by
Zheng et al. (2018a) and Garousi-Nejad et al. (2019) noted
improvement when utilizing higher-resolution lidar-derived
DEMs for HAND-based FIM.

The spatial resolution of topography likely interacts with
many other sources of FIM extent uncertainties, including
but not limited to elevation source quality, LULC, stream-
ﬂow intensities, physics employed, and model parameteriza-
tions (Fewtrell et al., 2008; Savage et al., 2016; Neal et al.,
2011; Thomas Steven Savage et al., 2016). Numerous re-
searchers have evaluated resolution more generally across
the spectrum of FIM models to focus more on urban areas
where resolution could play an integral part in determining

Hydrol. Earth Syst. Sci., 28, 1287–1315, 2024

https://doi.org/10.5194/hess-28-1287-2024

F. Aristizabal et al.: Effects of high-quality elevation data and other variables on FIM skill

1291

extents (Fewtrell et al., 2008; Neal et al., 2011; Ozdemir
et al., 2013; Muthusamy et al., 2021; Savage et al., 2016;
de Almeida et al., 2018; Dixon and Earls, 2009). While the
studies evaluating HAND are extensive (Afshari et al., 2018;
Nobre et al., 2011; Garousi-Nejad et al., 2019; Godbout et al.,
2019; Speckhann et al., 2018; McGrath et al., 2018; McGe-
hee et al., 2016; Li et al., 2020, 2022, 2023; Liu et al., 2016;
Y. Y. Liu et al., 2018; C. Liu et al., 2018; Li and Demir, 2022;
Liu et al., 2020; Aristizabal et al., 2023c; Maidment, 2017;
Zheng et al., 2018a, b, 2019; Diehl et al., 2021; Johnson et al.,
2019; Jafarzadegan and Merwade, 2019), only a few stud-
ies have investigated the effects of high-quality DEMs and
their spatial resolutions on FIM extents when derived from
HAND. Li et al. (2022) evaluated HAND-based FIM over a
small domain and concluded that resampled lidar performed
best at the 5 m spatial resolution when compared to coarser,
resampled grids. Zheng et al. (2018a) incorporated lidar-
derived elevations while also incorporating a novel stream
delineation method and concluded that both combined per-
formed better than utilizing legacy NED 10 m datasets with
NHDPlusV2 hydrography as the data for HAND computa-
tion. Lastly, working in ﬂat areas with some anthropogenic
inﬂuence, Garousi-Nejad et al. (2019) used a 3 m DEM and
found improvement in FIM quality extents when compared
to the use of a 10 m DEM derived from different sources. In
contrast to the other studies, Speckhann et al. (2018) eval-
uated the sensitivity of HAND-based FIM extents to DEM
resolution in Brazil using DEMs from SRTM and found little
to no effect in this region. Both Garousi-Nejad et al. (2019)
and Zheng et al. (2018a) highlighted the importance of high-
resolution elevations and novel stream delineation tools to
avoid the negative effects of little to no bathymetric infor-
mation. Due to the interacting uncertainties and the dearth
of research on this question with respect to HAND, it is dif-
ﬁcult to conclude what the effect would be on the quality
of HAND-based OWP FIM of incorporating the latest 3DEP
data at varying spatial resolutions.

As the spatial coverage of the 3DEP 1 m product rapidly
approaches the CONUS scale in 2023, we investigate the in-
tegration of 3DEP data into OWP FIM for model-speciﬁc
evaluation (USGS, 2021b, 2022a). We use 3DEP data for the
HAND computation process to generate the FIM hydrofab-
ric. OWP FIM uses a novel combination of input datasets,
hydrological conditioning (hydro-conditioning) processes,
level-path-scale processing, and parameterizations to pro-
duce HAND, and these speciﬁc combinations of methods
could interact with terrain-related variables including source
and resolution. Additionally, we investigated the utility of
varying spatial resolutions at 3, 5, 10, 15, and 20 m, specif-
ically its effect on FIM extents. HAND depends on the
drainage assumptions which require DEMs to undergo a long
series of enforcement processes to ensure monotonically de-
creasing elevations with hydrologically correct ﬂow direc-
tions (Garousi-Nejad et al., 2019; Nobre et al., 2011, 2016;
Aristizabal et al., 2023c). The resampling of DEMs into

varying spatial resolutions could interact with these hydro-
conditioning operations, thus inﬂuencing the FIM hydrofab-
ric and the resulting quality of the FIMs produced. OWP FIM
is scheduled for public release in 2023 for a region covering
10 % of the US population. Evaluations are needed speciﬁ-
cally for this region and of how 3DEP elevations at varying
resolutions affect skill. As validation, we used the 1D Hy-
drologic Engineering Center River Analysis System (HEC-
RAS)-modeled ﬂood inundation extents from the Base Level
Engineering (BLE) published by the Interagency Flood Risk
Management (InFRM) team. By varying the spatial reso-
lution of 3DEP DEMs, we seek to quantify in an empiri-
cal fashion the relationship between the spatial resolution
and FIM skill produced from HAND; this requires signif-
icant DEM manipulations to satisfy inherent assumptions.
For analysis purposes, we consider a series of potential,
catchment-scale explanatory variables with multi-variable
regression analysis to help explain some of the catchment-
scale variation in the metrics we employed to describe agree-
ment with the BLE FIMs.

2 Materials and methods

2.1 Overview

Investigating the effects of lidar-derived DEMs and their spa-
tial resolutions involved a multi-step process of data curation,
production, evaluation, and analysis. Source information was
gathered to produce HAND and its associated datasets, most
speciﬁcally the DEMs, from multiple sources and spatial res-
olutions, including 3, 5, 10, 15, and 20 m. Later in the analy-
sis, the resolutions of 60 and 90 m were assessed to help iden-
tify if and when spatial resolution begins to inﬂuence FIM
quality. The FIM hydrofabric, or the collection of datasets
required to convert streamﬂows to FIM extents, was pro-
duced using these various DEMs (Aristizabal et al., 2023c;
Aristizabal and Judge, 2021). FIMs were produced by in-
tersecting the BLE cross-sections, as described by Aristiz-
abal et al. (2023c), furnished by the InFRM team for both
the 1 % (100-year) and 0.2 % (500-year) recurrence ﬂows
(FEMA, 2016, 2021a, b; Strategic Alliance for Risk Reduc-
tion II, 2019a, b, c, d, e, f, g). These intersected ﬂows were
converted to reach-averaged stages using SRCs (Aristizabal
et al., 2023c; Liu et al., 2016; Y. Y. Liu et al., 2018; Zheng
et al., 2018b). Reach-averaged stages were used to threshold
HAND values on a per-catchment basis, which translates to
a ﬂooded pixel when the stage value exceeds zero (Zheng
et al., 2018b; Aristizabal et al., 2023c). Catchments are de-
ﬁned here as the unique surface drainage areas assigned to
each river reach. These extents at the 100- and 500-year
ﬂow magnitudes were then compared to the original BLE-
furnished extents for the corresponding magnitudes. Agree-
ment statistics and maps were computed for binary categori-
cal variables (inundated indicates positive and not inundated

https://doi.org/10.5194/hess-28-1287-2024

Hydrol. Earth Syst. Sci., 28, 1287–1315, 2024

1292

F. Aristizabal et al.: Effects of high-quality elevation data and other variables on FIM skill

2.2 Datasets

We used a wide variety of datasets for investigating the ef-
fects of DEM source and spatial resolution on FIMs pro-
duced from HAND. We compared legacy DEMs, used by
Aristizabal et al. (2023c) and sourced from the NHDPlusHR
program, that were available for the entire NWM domain at
the hydrologic unit code (HUC)-4 scale. As the 3DEP pro-
gram rapidly approaches continental-scale availability, the
inclusion of 3DEP DEMs was considered here at various spa-
tial resolutions (USGS, 2022a; Stoker et al., 2015; USGS,
2021b; Chegini et al., 2021; USGS, 2022b). Aristizabal et al.
(2023c) provided more details for the datasets listed in Fig. 1,
as denoted by “Other”. The remaining datasets used in this
study for DEM experimentation and for analysis are elab-
orated on in Table 1. The analysis datasets are those used
to help explain some of the spatial variation in the met-
rics. NWM catchments were used to resample the agreement
maps and metrics down to the catchment scale. Analyses
of the importance of various attributes within NWM catch-
ments considered ﬂow path properties such as channel slope,
length, presence of reservoirs, and catchment area. Other at-
tributes, aggregated to the catchment scale for consideration,
included terrain slope, imperviousness, overland roughness,
and LULC from the National Land Cover Database (NLCD),
which were used as either covariates or factors in the statisti-
cal analysis of this study.

2.3 Data retrieval

(HyRiver)
We used the Hydroclimate Data Retriever
(Chegini et al., 2021) for retrieving topographic, LULC, im-
perviousness, and overland roughness data. HyRiver is a
suite of nine open-source Python packages that provide ac-
cess to a wide variety of hydrology and climatology datasets
within the US through web services. In this study, we
used two of these packages: the Python 3D Elevation Pro-
gram (Py3DEP) and Python Hydrogeological (PyGeoHydro)
datasets.

Py3DEP provides access to 3DEP’s dynamic and static
services. The dynamic service retrieves topographic data at
any resolution using the best available raw elevation data
for a requested region, whereas the static service only pro-
vides DEM data at 10, 30, and 60 m resolutions. It has some
other utilities, including querying the availability of raw el-
evation data at different resolutions from various sources. In
this study, we used the dynamic service to obtain DEMs at
different resolutions and the raw data availability function-
ality of Py3DEP for determining the highest-resolution data
available in the region of our study.

While Py3DEP is developed only for retrieving topo-
graphic data from a single source, PyGeoHydro can query
various types of data from different sources, e.g.,
the
National Inventory of Dams (United States Army Corps
the Watershed Boundary Dataset
of Engineers, 2023),

Figure 1. This ﬁgure illustrates the overall process for generating
Height Above Nearest Drainage (HAND) and evaluating the use
of light detection and ranging (lidar)-derived digital elevation mod-
els (DEMs) and their resolutions. Input datasets were collected from
two different source DEMs, the 3D Elevation Program (3DEP) and
the National Hydrography Dataset Plus High Resolution (NHD-
PlusHR). The 3DEP DEMs were resampled with the Python 3D
Elevation Program (Py3DEP) to 3, 5, 10, 15, and 20 m spatial reso-
lutions. Both source DEMs and their resolutions were used to com-
pute the ﬂood inundation map (FIM) hydrofabric, which is com-
prised of various datasets used to produce FIM, including HAND,
catchments, and synthetic rating curves (SRCs). Base Level Engi-
neering (BLE) cross-sections were intersected with the National
Water Model (NWM) stream network to obtain streamﬂow esti-
mates. These estimates were used to produce FIM using the SRC
coupled with HAND to produce estimates of the 100- and 500-year
extents. These extents were then compared to the extents from the
BLE, thus removing hydrology-related errors that could be intro-
duced if NWM streamﬂows were used. The agreement statistics
were resampled to the NWM catchment level and then were ref-
erenced to a long series of catchment-level covariates and factors
that were used for statistical analysis and inference.

indicates negative) and then were resampled to the catchment
scale. A number of covariates and factors were selected at
the catchment scale for analysis purposes to explain some of
the catchment-to-catchment variance in the selected metrics
with the help of regression models. A high-level graphical
summary of this explanation is presented in Fig. 1.

Hydrol. Earth Syst. Sci., 28, 1287–1315, 2024

https://doi.org/10.5194/hess-28-1287-2024

F. Aristizabal et al.: Effects of high-quality elevation data and other variables on FIM skill

1293

Table 1. Dataset sources, names, descriptions, and citations. Datasets used to generate Height Above Nearest Drainage (HAND), except for
the digital elevation model (DEMs), are not listed in detail here but are explained by Aristizabal et al. (2023c).

Source

USGS

Dataset

3DEP

Description

Citations

Continental-scale high-resolution (1 m) DEMs from
high-quality sources

USGS (2022a, 2021b), Stoker
et al. (2015), Chegini et al.
(2021)

USGS

NHDPlusHR DEM

DEMs available from NHDPlusHR program at the
HUC-4 level for the entire country

USGS (2021a), Moore et al.
(2019)

Various

Other datasets (see Fig. 1)

Other datasets used for production of HAND-based
FIM hydrofabric

Aristizabal et al. (2023c)

InFRM

Flood inundation extents

InFRM

Cross-sections

OWP

NWM catchments

OWP

NWM stream network

USGS

Terrain slope

Inundation depths produced by InFRM BLE HEC-
RAS 1D for 1 % and 0.2 % recurrence interval
events

FEMA (2021b, 2016, 2021a),
Strategic Alliance for Risk Re-
duction II (2019a, b, c, d, e, f, g)

BLE HEC-RAS 1D cross-sections for 100-year
(1 %) and 500-year (0.2 %) streamﬂow magnitudes
used to intersect with NWM reaches

FEMA (2021b, 2016, 2021a),
Strategic Alliance for Risk Re-
duction II (2019a, b, c, d, e, f, g)

Surface drainage area corresponding to each reach
in the NWM, adapted from the NHDPlusV2 catch-
ment feature class

Stream network ﬂow paths used by NWM for
routing and forecasting, adapted from NHDPlusV2
NHDFlowline network feature class

Terrain slope (vertical/horizontal) computed from
3DEP DEMs.

NLCD

LULC

LULC as produced by the NLCD 2019 at the 30 m
resolution, derived partly from Landsat imagery

NLCD

Imperviousness

Urban impervious surface as a percentage of
developed surface over 30 m pixels

NLCD

Overland roughness

Overland roughness or Manning’s n for given pixel
within NLCD

OWP/ESIP (2021)

OWP/ESIP (2021)

Dewitz (2021), Yang et al.
(2018), Chegini et al. (2021),
USGS (2022b)

Dewitz (2021), Yang et al.
(2018), Chegini et al. (2021),
Multi-Resolution Land Charac-
teristics Consortium (2022)

Dewitz (2021), Yang et al.
(2018), Chegini et al. (2021),
Multi-Resolution Land Charac-
teristics Consortium (2022)

Dewitz (2021), Yang et al.
(2018), Chow (1959), Chegini
et al. (2021), Multi-Resolution
Land Characteristics Consor-
tium (2022), McCuen et al.
(2005), Kalyanapu et al. (2009)

(United States Geological Survey, 2023), and the National
Land Cover Database (Multi-Resolution Land Characteris-
tics Consortium, 2022). It also includes additional function-
alities, including a look-up table for associating overland
roughness to land cover type based on Liu et al. (2019). In
this study, we obtained HUC geometries, reservoirs, LULC,
imperviousness, and overland roughness data using PyGeo-
Hydro.

2.4 DEM preparation

DEMs underwent a curation procedure prior to use with
HAND computation and our experimental design. To match
the existing framework with the use of NHDPlusHR DEMs,
Py3DEP was used to query the image server to acquire
3DEP elevations at an HUC-4 scale. To counter pixel limi-
tations within the web service, queries were completed using
overlapping tiles and were mosaicked together using virtual
rasters (VRTs) (USGS, 2022b). To investigate the effect of

https://doi.org/10.5194/hess-28-1287-2024

Hydrol. Earth Syst. Sci., 28, 1287–1315, 2024

1294

F. Aristizabal et al.: Effects of high-quality elevation data and other variables on FIM skill

varying spatial resolutions on FIM skill and computational
performance, queries were elected to be taken at 3, 5, 10, 15,
and 20 m spatial resolutions. As stated previously, the resolu-
tions of 60 and 90 m were also used to help understand if and
when spatial resolution begins to affect quality. Utilizing the
check_3dep_availability tool, we determined that 1 m 3DEP
information is available for the entire study region (see Sect.
2.5). Py3DEP queries a US Geological Survey (USGS) dy-
namic web service for the best available DEM when generat-
ing its mosaics and resamples them given the user-furnished
resolution (USGS, 2022b). Use of the Py3DEP function
query_3dep_source conﬁrmed availability of 1 m lidar data
for the entire study area, which means the functionality uses
it for resampling purposes (Chegini et al., 2021; Stoker et al.,
2015; USGS, 2022b, a, 2021b). The availability of the 1 m
data and of the other available source DEMs is illustrated in
Fig. 2. The selected resolutions of 3, 5, 10, 15, and 20 m were
bounded by computational demands since further optimiza-
tions within the code and external dependencies should be
considered prior to transitioning to 1 m elevation information
for HAND computation.

2.5 Study area

The site selection process considered several factors. The lo-
cation of the site was limited by the availability of validation
data (discussed in Sect. 2.6), as well as the availability of 1 m
3DEP information (USGS, 2022a, 2021b). Additionally, the
location of the site was inﬂuenced by OWP’s plan to release
FIM services in stages as a function of the percentage of the
population served. The ﬁrst release will serve 10 % of the
US population and cover portions of eastern Texas (TX), as
well as the Mid-Atlantic states. On the other hand, the size
of the evaluation site was constrained by the computational
burdens of producing the FIM hydrofabric at multiple reso-
lutions.

With these criteria in mind, we selected the Neches River
sub-region as the study area for this experiment. The HUC-
4 (1202) sub-region comprises seven HUC-8 sub-basins,
ranging continuously from 12020001 to 12020007. Lo-
cated in southeastern TX near the Louisiana border, the site
stretches from Tyler to Beaumont and includes the towns
of Nacogdoches and Lufkin, as depicted in Fig. 3. Numer-
ous braided streams and 15 reservoirs, including one of the
largest ones, the Sam Rayburn Reservoir, populate the study
area. Figure 4 depicts the spatial distribution of LULCs
as deﬁned in the 2019 NLCD but grouped to the top tier
of categories for visibility and interpretability. The study
area features a low slope, with low-lying areas mostly com-
prising four LULCs: evergreen forests (31.1 %), pasture or
hay (17.2 %), woody wetlands (16.7 %), and mixed forests
(11.4 %). The developed LULCs together account for only
7.3 % of the site’s area. In summary, the study area has low
terrain slope and minimal anthropogenic inﬂuence.

2.6 Evaluation

We chose the BLE FIM extents for evaluation, which are
HEC-RAS-1D-based models provided by InFRM and the
Federal Emergency Management Agency (FEMA) (FEMA,
2016, 2021a, b; Strategic Alliance for Risk Reduction II,
2019a, b, c, d, e, f, g). FEMA’s Region 6 publishes these
FIMs, which are available at both 1 % (100-year) and 0.2 %
(500-year) ﬂow magnitudes, and they also include cross-
sectional information with the associated ﬂows for each
level. Despite being a modeled dataset, HEC-RAS appears
frequently in the literature for comparison purposes as it is
an engineering-scale model (Cook and Merwade, 2009; Ra-
jib et al., 2016; Zheng et al., 2018a; Afshari et al., 2018; Wing
et al., 2017; Criss and Nelson, 2022; Follum et al., 2017). We
chose to intersect the cross-sections with NWM ﬂow paths
to remove errors and uncertainties associated with hydro-
logical and meteorological inputs used to produce stream-
ﬂows within the NWM (Aristizabal et al., 2023c). This pro-
cess enabled us to associate BLE-derived 100- and 500-
year streamﬂow magnitudes with NWM forecasting points.
If multiple intersections occurred per NWM stream reach,
we took the median ﬂow value. Even though this process
may lead to conﬂation errors, we believe it allows for a bet-
ter comparison with BLE FIM extents by removing any er-
rors introduced from variances in other hydrological pro-
cesses outside of inundation (Aristizabal et al., 2023c). For
more detailed information on this technique and its applica-
tion, see Sect. 2.7 in Aristizabal et al. (2023c). It is crucial
to emphasize that the BLE benchmark FIMs utilize DEMs
derived from high-quality lidar data, with a spatial resolu-
tion of approximately 1 m, for conducting hydraulic analy-
ses and creating ﬂoodplain maps throughout our entire se-
lected study region (Strategic Alliance for Risk Reduction II,
2019a, b, c, d, e, f, g). The benchmark’s dependence on lidar-
derived DEMs at 1 m resolutions enables the answering of
our central question pertaining to the effect of DEM source
and resolution on HAND-based FIM skill. We would like to
acknowledge here that producing HAND with 1 m informa-
tion to match that of the BLE is computationally very ex-
pensive, leading to substantial increases in central process-
ing unit (CPU) time and memory usage, which we discuss in
Sects. 3 and 4.

In order to quantify agreement with the BLE FIM ex-
tents, we elected to apply binary contingency statistics. The
primary metrics calculated within a contingency table in-
clude true positives (TPs), false positives (FPs), false nega-
tives (FNs), and true negatives (TNs). We again note that the
positive condition is considered to be inundated, while the
negative condition is considered to not be inundated. In order
to summarize the contingency table into secondary metrics,
we employed the commonly used metrics within ﬂood mod-
eling, including critical success index (CSI), true-positive
rate (TPR), and false-alarm rate (FAR), shown in Eqs. (1)–

Hydrol. Earth Syst. Sci., 28, 1287–1315, 2024

https://doi.org/10.5194/hess-28-1287-2024

F. Aristizabal et al.: Effects of high-quality elevation data and other variables on FIM skill

1295

Figure 2. This ﬁgure illustrates the source digital elevation model (DEM) available within the 3D Elevation Program (3DEP) for the study
area. High-resolution 1 m information is available for the entire study area, meaning it was used as the source resolution for resampling to
the resolutions used for Height Above Nearest Drainage (HAND) computation, including 3, 5, 10, 15, and 20 m. See Sect. 2.5 for more
information with regard to the study area. © OpenStreetMap contributors 2023. Distributed under the Open Data Commons Open Database
License (ODbL) v1.0.

(3), respectively (Gerapetritis and Pelissier, 2004; Schaefer,
1990).

CSI =

TP
TP + FP + TN

TPR =

FAR =

TP
TP + FN
FP
TP + FP

(1)

(2)

(3)

TPR, also known as sensitivity, recall, and probability of
detection or hit rate, was used to describe a model’s abil-
ity to detect ﬂooding as it represents performance in regions
that are considered to be ﬂooded within the benchmark. It
is formally described as the proportion of inundated pixels
that are accurately detected as ﬂooded. FAR, also known
as false-discovery rate, the inverse of precision, or the in-
verse of positive predictive value, conveys the opposite since
it is used to represent over-prediction. This is formally de-
scribed as the proportion of pixels incorrectly predicted to be
ﬂooded with respect to the total number of pixels predicted to
be ﬂooded. Work by Gerapetritis and Pelissier (2004) illus-
trated how these two metrics, TPR and FAR, are mathemati-
cally related to CSI where correctly predicted, non-inundated

regions (TNs) are not considered. This leads to CSI be-
ing considered to be inequitable or exhibiting frequency de-
pendency, which could limit its use in comparing predicted
datasets in scenarios with varying frequencies (Gerapetritis
and Pelissier, 2004; Schaefer, 1990).

While these three widely adopted metrics are considered to
be highly interpretable, we elected to include the Matthews
correlation coefﬁcient (MCC), shown in Eq. (4), which is
considered to be more equitable when dealing with cases of
extreme class imbalance (Chicco and Jurman, 2020; Chicco
et al., 2021a, b; Boughorbel et al., 2017). However, it does
value both conditions (inundated and not inundated) as hav-
ing equal impact (Chicco and Jurman, 2020; Chicco et al.,
2021a, b; Boughorbel et al., 2017).

MCC =

√

TP · TN − FP · FN
(TP + FP)(TP + FN)(TN + FP)(TN + FN)

(4)

2.6.1 Analysis

Evaluations for this HUC-4 study region were conducted at
the HUC-8 scale, which produces seven HUC-8 metric val-
ues across all ﬁve spatial resolutions evaluated, as well as
over both ﬂood magnitudes, yielding about 70 samples to an-
alyze (7 · 5 · 2 = 70). Analysis at this large HUC scale tends

https://doi.org/10.5194/hess-28-1287-2024

Hydrol. Earth Syst. Sci., 28, 1287–1315, 2024

1296

F. Aristizabal et al.: Effects of high-quality elevation data and other variables on FIM skill

themselves, including channel slope, catchment area, stream
order, and reservoir.

The term reservoir is used here with respect to catchments
that intersect with NWM reservoirs. While NWM reservoirs
are masked out for evaluation and are also not modeled
within OWP FIM, the BLE FIM extents do model reservoir
inundation. This creates regions of BLE inundation that ex-
tend beyond NWM reservoir deﬁnitions, thus leading to FNs.
NWM catchments that intersect with NWM reservoirs are
denoted as reservoir catchments and used as a factor to help
account for the performance within these regions. This is bet-
ter illustrated in Fig. 5.

In addition to catchment-level attributes within the NWM
hydrofabric, we collected a variety of datasets associated
with hydrological processes, including NLCD LULC, im-
perviousness, overland roughness, and terrain slope. These
factors and covariates were obtained utilizing the HyRiver
suite of tools described in Sect. 2.3. Overland roughness
was determined by the NLCD LULCs and previous research-
assigned coefﬁcients for each category (Dewitz, 2021; Yang
et al., 2018; Chow, 1959; Chegini et al., 2021; Multi-
Resolution Land Characteristics Consortium, 2022; McCuen
et al., 2005; Kalyanapu et al., 2009). In order to aggregate to
the catchment scale, LULC was taken as the dominant cat-
egory by catchment, while the covariates’ imperviousness,
overland roughness, and terrain slope were aggregated by
taking the catchment-level mean value. This procedure cre-
ated a total of 10 catchment-level covariates and factors sum-
marized as spatial resolution, DEM source, channel slope,
catchment area, stream order, reservoir, LULC, impervious-
ness, overland roughness, and terrain slope. These covariates
and factors are collectively known as features, predictors, ex-
planatory variables, or independent variables and were used
to correlate to dependent, response, or outcome variables
which include the four metrics of interest in this study. These
are described in more detail in Table 2.

Given the fact that we aggregated a variety of catchment-
scale features for each associated catchment-scale metric, we
used the regression analysis to help explain the magnitude
and signiﬁcance of the linear relationships between the ex-
planatory variables and the four responses (metrics: MCC,
CSI, TPR, and FAR) (Montgomery et al., 2021; Chatterjee
and Simonoff, 2013; Merrill et al., 2017). We avoided includ-
ing the metrics with the NHDPlusHR DEM in the regression
analysis since it was already clear that using 3DEP DEMs
led to signiﬁcant skill improvements. To build our regression
model, we opted to use forward model selection of all one-
way and two-way interactions utilizing the Akaike informa-
tion criterion (AIC) and terminating the model selection after
a minimum is reached. Explanatory variables were feature
scaled from 0 to 1 prior to ﬁtting to better compare across
explanatory variables – meaning this procedure added vari-
ables to the regression model for each metric ﬁrst. Identifying
the explanatory variable that reduced the Akaike information
criterion (AIC) to its minimum, the procedure retained this

Figure 3. Overview of study area nestled in southeastern
Texas (TX) near the Louisiana border. Known as the Neches River
sub-region or HUC-4 1202, the site is composed of seven sub-
basins or hydrologic unit code (HUC) 8s. © OpenStreetMap con-
tributors 2023. Distributed under the Open Data Commons Open
Database License (ODbL) v1.0.

to erode away valuable information that could be used if a
ﬁner grain unit of measurement were used instead. Under
this justiﬁcation, we opted to sub-sample agreement maps
down to the NWM catchment scale and recompute each of
the four metrics for each catchment. There are 5786 NWM
catchments available for this study area, which generates
405 020 effective samples to analyze (70 · 5786 = 405 020).
This yielded a much ﬁner grain spatial distribution of per-
formance but also enabled the introduction of covariates
and factors that can help explain some of the catchment-
to-catchment variance in the metrics. Factors are categori-
cal variables in our analysis and have a ﬁnite number of dis-
tinct categories. Covariates, on the other hand, are continuous
variables that are assumed to have a linear relationship with
the dependent variable. The term covariate serves the same
function as the factors with the only distinction being that co-
variates are of continuous data types. We investigated the in-
teraction of explanatory variables by multiplying all possible
combinations to capture the variance in the dependent vari-
able more comprehensively. The combination of covariates
and factors was carried out by including interaction terms in
the regression model. Interaction terms are created by multi-
plying a covariate and a factor or two factors, which allows
us to investigate whether the effect of one variable depends
on the level of the other variable. Many of these covariates
and factors stemmed from NWM catchments or ﬂow paths

Hydrol. Earth Syst. Sci., 28, 1287–1315, 2024

https://doi.org/10.5194/hess-28-1287-2024

F. Aristizabal et al.: Effects of high-quality elevation data and other variables on FIM skill

1297

Figure 4. A detailed view showing the spatial distribution of the 2019 National Land Cover Database (NLCD) land use and land cov-
ers (LULCs) grouped to the top-tier categories for visibility and interpretability. About three-quarters of the site is made up of just four land
covers, including evergreen forest (31.1 %), pasture or hay (17.2 %), woody wetlands (16.7 %), and mixed forests (11.4 %). Only about 7.2 %
of the site is considered to be developed. © OpenStreetMap contributors 2023. Distributed under the Open Data Commons Open Database
License (ODbL) v1.0.

Table 2. Summary of catchment-level covariates and factors used for statistical analysis. Included are the dataset, its statistical data type for
analysis (factor or covariate), its units if it is a covariate, and its levels if it is a factor.

Dataset

Spatial resolution

DEM source

Channel slope

Catchment area

Statistical data
type

Factor

Factor

Covariate

Covariate

Levels for factors or units for covariates

Five levels in meters: 3, 5, 10, 15, & 20

Two levels: NHDPlusHR & 3DEP

Vertical or horizontal as percentage

Surface area (in km2)

Horton–Strahler stream order

Factor

Six levels: 1–6

Reservoir

Factor

Two levels: true (1) and false (0)

NLCD 2019 dominant LULC

Factor

Fifteen levels: woody wetlands; pasture or hay; evergreen forest; developed, low
intensity; shrub forest; mixed fores; developed, open space; cultivated crops;
developed, medium intensity; emergent herbaceous wetlands; water; herbaceous
forest; developed, high intensity; deciduous forest; and grasslands or herbaceous

Imperviousness

Overland roughness

Terrain slope

Stream order

Covariate

Covariate

Covariate

Covariate

Percentage of pixel area that is impervious surface

Unitless: friction coefﬁcient for overland water ﬂow

Vertical or horizontal as percentage

Horton–Strahler stream order as deﬁned in NWM stream network

https://doi.org/10.5194/hess-28-1287-2024

Hydrol. Earth Syst. Sci., 28, 1287–1315, 2024

1298

F. Aristizabal et al.: Effects of high-quality elevation data and other variables on FIM skill

3.1

3DEP data

For the given study area, we decided to investigate the effect
on HAND-based FIM extents by utilizing the 3DEP data in-
stead of the legacy source DEMs from the NHDPlusHR. We
conducted this comparison on an NWM catchment scale in
order to have a sense of the distribution of the results across
some spatial deﬁnition ﬁner than the HUC scale. Addition-
ally, this comparison was conducted by resampling the 3DEP
1 m data to a spatial resolution of 10 m to match that of the
legacy DEM. Figure 6 details the results of this comparison
in a scatterplot format. Each individual data point represents
a sample of the metrics taken at the NWM catchment scale.
The points are sampled across two axes, representing their
performance with NHDPlusHR DEMs on the x axis and with
3DEP DEMs on the y axis. The 45° diagonal line represents
a dividing line where the metric values for both DEMs are
the same. Catchment samples symbolized in green represent
enhanced FIM extents for that catchment for the given case,
while samples symbolized in red signify poorer-quality ex-
tents. We also included descriptive statistics on each sub-
ﬁgure representing the mean and standard deviation of the
metric differences across DEMs (3DEP − NHDPlusHR), as
well as the percentage of differences greater than or less than
zero.

Overall, the use of the higher-quality, more recently pro-
duced 3DEP DEMs generally enhances FIM extents across
all the metrics and magnitudes examined. This is made evi-
dent by observing the high proportion of catchments repre-
sented in green and the high percentage of samples greater
than zero for the ﬁrst three metrics. The FAR is minimized,
so a lower proportion of samples above zero is considered
to be better. Overall, approximately four in every ﬁve catch-
ments are considered to beneﬁt from the use of 3DEP when
compared to the use of NHDPlusHR. This approximate rela-
tionship holds true across metrics and event magnitudes for
our given experimental design.

Figure 5. Figure shows Lake Tyler reservoir within hydrologic unit
code (HUC)-8 12020004 of the study area. Background represents
an agreement map between the Ofﬁce of Water Prediction (OWP)
ﬂood inundation map (FIM) and the Base Level Engineering (BLE)
FIM at a 10 m spatial resolution for the 500-year (yr) magnitude.
Gray area shows masked-out National Water Model (NWM) reser-
voirs since these are not being modeled within OWP FIM. The
NWM catchments shaded in green represent catchments associated
with this NWM reservoir as they are shown to spatially intersect.
These reservoir catchments were used in analysis to quantify the
catchment variance in performance, partly due to not accounting
for reservoir inundation within BLE FIM.

variable within the model before proceeding to evaluate the
remaining variables, provided that the newly added variable
offered an improvement of at least 0.001 over the preced-
ing model. This process helps build models with explanatory
power while avoiding unnecessary complexity.

3 Results

3.2 Regression analysis

Based on the observation of our results, we conducted an in-
depth analysis of the effects of utilizing 3DEP DEMs ﬁrst
when compared to the legacy NHDPlusHR DEMs. After
conﬁrming the positive effect of using 3DEP information,
we varied the spatial resolution of these DEMs and observed
the impact on performance. To further investigate the effects
of additional explanatory variables, we built a multiple lin-
ear regression model with forward model selection to help
explain some of the catchment-to-catchment variance in the
four metrics. Lastly, we decided to do an in-depth analysis of
a few of these variables that we found to be of importance.

After we established the effect of the new elevation data
source on FIM extents, we elected to conduct regression
analysis on the remaining explanatory variables of interest.
As explained in the methods, we regressed the four met-
rics of interest independently and ﬁt the model in a forward-
selection fashion, utilizing AIC as a measure of model ﬁt.
Figure 7 represents the resulting models from that forward
model selection in graphical form. The four subplots repre-
sent the results of the model ﬁt to each metric or response
variable. The y-axis labels represent explanatory variables,
starting with the intercept followed by the remaining vari-
ables and their two-way interactions in the order of selection
as per the AIC metric. By two-way interactions, we refer to
the statistical interaction between pairs of explanatory vari-
ables, implying that the effect of one explanatory variable on

Hydrol. Earth Syst. Sci., 28, 1287–1315, 2024

https://doi.org/10.5194/hess-28-1287-2024

F. Aristizabal et al.: Effects of high-quality elevation data and other variables on FIM skill

1299

the response variable may change depending on the value of
another explanatory variable. The points on the graph repre-
sent the values of the coefﬁcients, while the shape represents
the level of signiﬁcance from ≥ 0.05 (circle) to < 0.05 (pen-
tagon), < 0.01 (triangle), and < 0.001 (star). The green and
red colors represent the nature of the effects as either positive
(direct) or negative (indirect), respectively. Since AIC lacks
interpretability, we elected to show the coefﬁcient of deter-
mination or R2 at each step of the forward-selection process.
Additionally, Table 3 presents the results shown in Fig. 7 in
a tabular format (Jann, 2005).

Further examining Fig. 7, we can infer interesting pieces
of information as regression analysis is a tool to synthesize
data into something interpretable. The coefﬁcients of de-
termination or the R2 values across the metrics vary from
about 0.21 to 0.33. Translating this into other terms, one
can say that about one-ﬁfth to one-third of the catchment-
to-catchment variance in the metrics can be explained by the
11 catchment-scale explanatory variables and their two-way
interactions selected in this study. Additionally, observations
from the ﬁgure illustrate the prevalence of certain explana-
tory variables near the beginning of the selection process
that seem to explain a fair amount of the variation while also
exhibiting strong effect sizes. Some of the variables of note
include reservoir, stream order, terrain slope, channel slope,
and LULC. These explanatory variables and their effect on
catchment-level performance in FIM will be examined later
on in Sect. 3.4.

3.3

3DEP DEM spatial resolution

We investigated the effect of varying the spatial resolution
of the 3DEP DEMs on the quality of FIMs produced from
HAND. The 3DEP DEMs were varied at 3, 5, 10, 15, and
20 m prior to HAND computation.

Figure 8 examines the relationship of DEM spatial resolu-
tion at ﬁve levels for each of the four metrics selected. The re-
lationships are illustrated as distributions of catchment-scale
metric values for both event magnitudes (100 and 500 year).
We computed the distributions as Gaussian kernel density es-
timations (KDEs), which is a non-parametric statistical tech-
nique that determines the probability distribution of a random
variable (Virtanen et al., 2020; Scott, 2015; Silverman, 2018;
Turlach et al., 1993; Bashtannyk and Hyndman, 2001). For
each metric–magnitude distribution of catchment-scale met-
rics, the 75th, 50th, and 25th percentiles are calculated and
displayed from top to bottom as dashed, solid, and dotted
lines, respectively. Additionally, we ﬁt two linear regression
lines, one for each magnitude and for all four metrics, relat-
ing the linear effects of spatial resolution on metric values.
The effect sizes, or the slopes of the regression lines, are dis-
played along with their respective p values. Low p values
denote effect sizes that are unlikely to be equal to zero.

Examination of Fig. 8 shows statistically signiﬁcant yet
marginal values in terms of effect sizes for the TPR and FAR

Figure 6. Figure shows catchment-scale metric values. The eight
sub-ﬁgures are organized by magnitude (100 and 500 year) across
the columns and for the four metrics across the rows. These
values within each sub-ﬁgure are plotted on an axis represent-
ing Height Above Nearest Drainage (HAND)-based ﬂood in-
undation maps (FIMs) generated from the National Hydrogra-
phy Dataset Plus High Resolution (NHDPlusHR) digital elevation
model (DEMs) (x axis) and the same FIMs generated from 3D El-
evation Program (3DEP) DEMs resampled to the 10 m spatial res-
olution (y axis). The diagonal 45° line divides catchments that per-
form better with the legacy DEM (in red) and the catchments that
perform better with the 3DEP DEM (in green). The majority of
catchments perform better across all four metrics and both mag-
nitudes with the higher-quality 3DEP information. Additional de-
scriptive statistics quantifying the distribution of metric differences
(3DEP–NHDPlusHR) are also presented, including the mean and
standard deviation of the differences. We also included the percent-
age of samples whose difference is greater than or less than zero
depending on the metric referenced.

https://doi.org/10.5194/hess-28-1287-2024

Hydrol. Earth Syst. Sci., 28, 1287–1315, 2024

1300

F. Aristizabal et al.: Effects of high-quality elevation data and other variables on FIM skill

Figure 7. Figure illustrates the coefﬁcients from multiple linear regression models ﬁtted to four response variables independently. The
points on the graph represent the values of the coefﬁcients, while the shape represents the level of signiﬁcance from ≥ 0.05 (circle) to
< 0.05 (pentagon), < 0.01 (triangle), and < 0.001 (star). The green and red colors represent the nature of the effects as either positive
(direct) or negative (indirect), respectively. The models were built in a stepwise fashion using forward model selection and AIC as criteria
for terminating the process. A total of 11 explanatory variables were considered for these models, as well as their two-way interactions. An
intercept was also included by default. As the models built, we recorded the R2 of each successive model and tracked as the complexity of
the model increased. The ﬁnal R2 values for each ﬁnal model are reported as well for each step of the forward selection.

Hydrol. Earth Syst. Sci., 28, 1287–1315, 2024

https://doi.org/10.5194/hess-28-1287-2024

F. Aristizabal et al.: Effects of high-quality elevation data and other variables on FIM skill

1301

Table 3. Regression analysis table showing coefﬁcient values and their level of signiﬁcance for each agreement metric. Coefﬁcient val-
ues are based on feature-scaled explanatory variables in the range of 0 to 1. Variable deﬁnitions: intercept (IN), reservoir (RE), terrain
slope (TS), overland roughness (OR), channel slope (CS), stream order (SO), magnitude (M), land cover (LC), catchment area (A), spatial
resolution (SR), and imperviousness (IM).

MCC

CSI

TPR

FAR

Variable

IN
RE
SO
OR
TS
IM
CS
LC
M
A
OR : CS
TS : CS
SO : OR
CS : A
LC : OR
RE : OR
RE : SO
SO : A
SO : TS
SO : CS
IM : CS
TS : A
OR : TS
LC : IM
SO : IM
LC : TS

R2

Coefﬁcient
−0.011∗
0.084∗∗∗
0.300∗∗∗
0.764∗∗∗
2.581∗∗∗
0.295∗∗∗
5.547∗∗∗
0.283∗∗∗
0.015∗∗∗
0.230∗∗∗
−7.786∗∗∗
−10.562∗∗∗
−0.192∗∗∗
21.287∗∗∗
0.330∗∗∗
−0.978∗∗∗
−0.134∗∗∗
−0.474∗∗∗
−0.429∗∗∗
1.086∗∗∗
−5.120∗∗∗
−4.135∗∗∗
−1.617∗∗∗
−0.229∗∗∗
−0.203∗∗∗
−0.405∗∗∗

0.3235

∗ p ≤ 0.05. ∗∗ p ≤ 0.01. ∗∗∗ p ≤ 0.001.

Variable

Coefﬁcient
0.522∗∗∗
IN
0.315∗∗∗
SO
−0.169∗∗∗
RE
−1.433∗∗∗
CS
1.155∗∗∗
TS
A
0.016
−0.228∗∗∗
IM
0.020∗∗∗
M
−0.036∗∗∗
OR
−0.009∗∗∗
LC
−0.493∗∗∗
SO : A
SO : OR −0.065∗∗∗
3.328∗∗∗
SO : CS
SO : RE −0.169∗∗∗
RE : OR −0.714∗∗∗
SO : TS −0.869∗∗∗
−6.771∗∗∗
CS : TS
0.249∗∗∗
SO : IM
2.873∗∗∗
CS : IM
10.129∗∗∗
CS : A
−1.653∗∗∗
TS : A

Variable Coefﬁcient

Variable

IN
RE
SO
A
IM
M
SR
CS
LC
RE : SO
A : CS
SO : A
SO : IM
SO : CS
IM : CS
SO : SR
RE : IM
RE : A

0.736
−0.630
0.152
−0.063
−0.243
0.018
0.002
0.776
0.018
0.028
−20.899
−0.701
0.329
−1.444
2.396
−0.002
0.408
−0.546

IN
CS
TS
SO
A
OR
SR
LC
RE
CS : A
SO : CS
LC : OR
SO : TS
SO : A
RE : A
SO : OR
SO : LC
CS : OR
CS : TS
LC : TS
CS : SR
SO : RE

Coefﬁcient
0.118∗∗∗
4.604∗∗∗
−1.053∗∗∗
−0.076∗∗∗
0.035∗∗∗
0.278∗∗∗
0.000∗∗
0.249∗∗∗
−0.08∗∗∗
−30.385∗∗∗
−3.317∗∗∗
−0.313∗∗∗
0.81∗∗∗
0.029∗∗∗
1.289∗∗∗
−0.246∗∗∗
−0.094∗∗∗
−2.596∗∗∗
4.180∗∗∗
−0.541∗∗∗
0.036∗∗∗
0.037∗∗

0.3159

0.2110

0.3314

metrics. For example, the effect size of the TPR and 100-
year case is 0.0015, which represents a 0.0015 increase in
the value of TPR for every meter increase in the magnitude
of the resolution. Thus, for approximately 10 m, one would
expect TPR to increase by 0.015. While coarser-resolution
DEMs appear to improve the detection of inundation when
compared to the BLE FIMs, they also appear to have an un-
desirable effect on FAR as its expected values increase as
DEMs are coarsened. These competing effects on TPR and
FAR seem to have a canceling effect on the overall perfor-
mance metrics of MCC and CSI. Both MCC and CSI have
statistically insigniﬁcant trend lines, which hints at little to no
overall improvement in catchment-scale metrics of HAND-
based FIM as a result of varying the spatial resolution of the
input DEMs used to produce HAND.

Furthermore, we analyzed the mean and standard devia-
tions of the inundated areas for the ﬁve spatial resolutions
selected. Table 4 shows the HUC-8 level mean and standard

deviation of inundated areas (in km2) by spatial resolution
and across magnitudes. Very little variation in the inundated
areas was seen across the resolutions, which suggests that,
while there was an increase in TPR and FAR with coarser
DEMs, there is also little change in the inundated areas. This
suggests that most of the trade-offs in resolution were related
to trading type-I errors (FPs) in certain areas with type-II er-
rors (FNs) in other areas, with little to no overall change in
the inundated areas.

A ﬁnal observation related to the spatial resolution relates
to its relatively low importance or the lack of interaction
variables in the models built for the regression analysis in
Sect. 3.2 and Fig. 7. This denotes that spatial resolution pro-
vided little to no effect when considering impactful variables
such as LULC, imperviousness, stream order, or reservoir.

DEM resolution was found to have a signiﬁcant effect on
the computational demands of producing HAND. We aggre-
gated the times to compute HAND at the seven DEM spatial

https://doi.org/10.5194/hess-28-1287-2024

Hydrol. Earth Syst. Sci., 28, 1287–1315, 2024

1302

F. Aristizabal et al.: Effects of high-quality elevation data and other variables on FIM skill

Figure 8. This ﬁgure illustrates the distribution of the four catchment-scale metrics as violin plots across every spatial resolution selected,
including 3, 5, 10, 15, and 20 m. Each half of the violin represents a given magnitude of events (100 and 500 year). Linear trend lines are
ﬁt for each metric–magnitude combination, establishing linear relationships between spatial resolutions and metric values at the catchment
scale.

Table 4. Mean and standard deviations of inundated areas across
hydrologic unit code (HUC) 8s and magnitudes (100 and 500 year)
in square kilometers (km2) for each spatial resolution in meters (m).

Spatial
resolution
(m)

Mean
inundated
area (km2)

3
5
10
15
20

653.46
650.58
652.85
654.10
659.15

Standard
deviation of
inundated
area (km2)

161.58
161.12
153.46
158.22
154.58

resolutions and found a signiﬁcant effect on CPU time, espe-
cially at ﬁner resolutions. Figure 9 shows the change in log
CPU times in seconds by HUC-8. A change of almost an en-
tire order of magnitude in CPU time (in seconds) is observed
when using DEMs of 3 m versus 20 m resolutions. The num-
ber of pixels for a given domain of squared pixels is known to
have an inverse relationship with the square of spatial resolu-
tion (number of pixels ∝ squared resolution). Thus, reducing
the spatial resolution from 10 to 1 m represents a 100-fold in-
crease in the number of pixels for the ﬁxed domain. It is im-
portant to note that all computational benchmarks were com-
puted on an Amazon Web Services t3.2xlarge instance with
eight processing units; 32 GB of memory; and a 2000 GB
solid-state, elastic-block storage unit. The operating system
was based on GNU/Linux with an Ubuntu 22.04 distribution
on an x86 64-bit architecture. Despite having a minimal ob-

Hydrol. Earth Syst. Sci., 28, 1287–1315, 2024

https://doi.org/10.5194/hess-28-1287-2024

F. Aristizabal et al.: Effects of high-quality elevation data and other variables on FIM skill

1303

further within this analysis. Other variables, while important,
were out of the scope of this paper but should be analyzed
further in future studies.

3.4.1 Reservoirs

Given the relative importance of reservoirs in explaining
catchment-to-catchment variance in many of the metrics, as
shown in Fig. 7 and Sect. 3.2, we isolate this factor for fur-
ther analysis here. Figure 10 shows the catchment-level dis-
tribution of the four metrics across spatial resolutions as vio-
lin plots built with KDEs. The halves of the violins are split
across catchments that intersect with NWM reservoirs and
those that do not. The trend lines, as well as their displayed
slopes and p values, represent catchment-scale metric vari-
ance as a function of spatial resolution for each reservoir
group.

Figure 10 primarily shows a large statistical difference in
the catchment-scale variation of three metrics – MCC, CSI,
and TPR – across the catchments that intersect with reser-
voirs and those that do not. Explaining this variation is simple
as OWP FIM does not currently account for reservoir-related
inundation, while the BLE does. While the NWM reservoirs
are currently masked out for evaluation purposes, the BLE
reservoir inundation extents go beyond these masked regions,
thus contributing to FNs. Due to this fact, FAR illustrates
very little performance difference across reservoir groups as
FAR considers FPs and omits FNs (see Eq. 3). Another im-
portant trend to note from Fig. 9 is the relative lack of in-
teraction between spatial resolution and the reservoir factor,
as shown by the similarity in the slopes of trend lines across
reservoir groups. This can be interpreted as spatial resolu-
tion having little effect across the reservoir groups, which
can also be seen in Fig. 7, where the selection of a reservoir
spatial resolution predictor was omitted. Until OWP FIM
accounts for reservoir ﬂooding or until some higher-order
masking technique is applied, the presences of reservoir-
related catchments will continue to contribute to a high vari-
ance in catchment-scale metrics.

3.4.2 Land use and land cover

We analyzed catchment-scale metrics by taking the dominant
land cover per catchment (mode). While the linear analysis
in Sect. 3.2 grouped the NLCD categories into two groups
depending on their degree of anthropogenic inﬂuence, we de-
cided to un-group the categories for Fig. 11. In this ﬁgure, we
illustrate the distribution of the four catchment-scale metrics
in box plots, which are grouped by both NLCD LULC and
event magnitude. This chart does not appear to have a clear
trend until further inspection leads one to see a pattern per-
taining to the catchment-scale agreement and the nature of
the LULCs. To reveal this trend, we decided to group LULC
categories according to their relative level of anthropogenic
inﬂuence.

Figure 9. Total log central processing unit (CPU) time in sec-
onds (s) across varying digital elevation map (DEM) spatial reso-
lutions of 3, 5, 10, 15, 20, 60, and 90 m and listed by the seven
hydrologic unit code (HUC) 8s in the study region. Resolution was
found to have a signiﬁcant effect on total CPU time for computing
Height Above Nearest Drainage (HAND) as a reduction of nearly an
entire order of magnitude in seconds was observed from changing
the DEM resolution from 3 to 20 m. All computational benchmarks
were computed on an Amazon Web Services t3.2xlarge instance
with eight processing units; 32 GB of memory; and a 2000 GB
solid-state, elastic-block storage unit. The operating system was
based on GNU/Linux with an Ubuntu 22.04 distribution on an x86
64-bit architecture.

served effect on skill, we found that higher resolutions tended
to exhibit an excessive computational cost.

While this initial analysis demonstrates little inﬂuence of
DEM spatial resolution on FIM extent quality, it also begged
the following question: when might spatial resolution begin
to exhibit some signiﬁcant effect? In order to answer this
question, the spatial resolutions of 60 and 90 m were selected
and used to produce HAND and subsequent FIMs. These ex-
tents were again compared at the catchment scale for the en-
tire study region for both 100- and 500-year ﬂow magnitudes.
Since 10 m is the current standard resolution for elevations
within the NHDPlusHR and seamless 3DEP datasets, we il-
lustrate the mean catchment-scale metrics across the entire
study region for both ﬂow magnitudes in Table 5. These re-
sults illustrate how spatial resolution does eventually exhibit
a strong negative effect on FIM performance as the resolution
is coarsened beyond the standard 10 m, which was specif-
ically found to be around the medium resolutions between
20 and 60 m.

3.4 Explanatory-variable focus

Since reservoirs and LULCs are valuable for forecasting op-
erations, we elected to focus on those explanatory variables

https://doi.org/10.5194/hess-28-1287-2024

Hydrol. Earth Syst. Sci., 28, 1287–1315, 2024

1304

F. Aristizabal et al.: Effects of high-quality elevation data and other variables on FIM skill

Table 5. Mean catchment-scale agreement metrics for the National Hydrography Dataset (NHD) (10 m resolution) and 3D Elevation Pro-
gram (3DEP) (3, 5, 10, 15, 20, 60, and 90 m resolutions) digital elevation models (DEMs) across the entire study domain for both 100- and
500-year ﬂow magnitudes. Values are presented as percentages (%) instead of native decimal values for readability.

NHD

3DEP

Agreement metric

10 m

3 m

5 m

10 m

15 m

20 m

60 m

90 m

MCC
CSI
TPR
FAR

63.02
54.58
67.35
23.35

70.63
62.94
76.16
17.94

70.69
62.99
76.18
18.23

70.81
63.18
76.36
18.70

70.75
63.12
76.43
18.78

70.67
63.01
76.38
18.98

52.02
43.93
65.52
40.74

61.33
52.01
72.71
32.39

Figure 10. Catchment-scale variation illustrated as distributions modeled as kernel density estimations (KDEs). The distributions are grouped
by metric and by spatial resolution. The halves of the violins are divided by the presence of a National Water Model (NWM) catchment that
intersects (or does not intersect) an NWM reservoir. Signiﬁcant differences are observed between catchments identiﬁed with and without
reservoirs for all resolutions and metrics employed. Reservoirs are not currently modeled within the Ofﬁce of Water Prediction (OWP) ﬂood
inundation map (FIM), while the Base Level Engineering (BLE) does account for reservoir-related inundation extents. While the NWM
reservoirs are masked out for evaluation purposes, some of the BLE inundation extents reach beyond these boundaries, leading to a signiﬁcant
number of false negatives (FNs). The trend lines, as well as their corresponding slopes and p values, were constructed by regressing the two
reservoir groups independently by spatial resolution. Little to no interaction between reservoir groups and spatial resolutions was observed.

Hydrol. Earth Syst. Sci., 28, 1287–1315, 2024

https://doi.org/10.5194/hess-28-1287-2024

F. Aristizabal et al.: Effects of high-quality elevation data and other variables on FIM skill

1305

Figure 11. The distributions of four catchment-scale agreement metrics are shown as box plots and grouped by the dominant National Land
Cover Database (NLCD) land use and land cover (LULC) per catchment, as well as the event magnitude.

In grouping the LULCs by two categories of “more” and
“less” anthropogenic inﬂuence, we are able to see a clearer
trend as to how LULC affects catchment-scale agreement.
The LULCs grouped into the more category include the de-
veloped categories (open space, low intensity, medium in-

tensity, and high intensity) and the cultivated-crops cate-
gory, which, depending on the cropping system, can have
signiﬁcant hydrological implications. The remaining LULCs
within the study area were placed in the less category. Fig-
ure 12 shows the distribution of catchment-scale metrics

https://doi.org/10.5194/hess-28-1287-2024

Hydrol. Earth Syst. Sci., 28, 1287–1315, 2024

1306

F. Aristizabal et al.: Effects of high-quality elevation data and other variables on FIM skill

sorted by grouped LULC and event magnitude. We ﬁt a
multiple linear regression model for each metric using the
grouped LULC and magnitude, as well as their interactions,
as factors. The resulting formulas for this linear modeling are
shown above each ﬁgure with the parameter values and their
relative level of signiﬁcance. Since only p values greater
than 0.05 and less than 0.001 were encountered, we denoted
those with no asterisk and three asterisks, respectively. Addi-
tionally, we plot the trend lines resulting from another regres-
sion that associates the metric values with the LULC group-
ing, and we do this for each event magnitude independently.
Illustrating this regression demonstrates these relationships
in a qualitative manner, highlighting the lack of interaction
of event magnitude and grouped LULC.

Judging from Figs. 11 and 12, there is a clear indica-
tion that LULC has a signiﬁcant inﬂuence over catchment-
scale agreement. Grouped LULCs in Fig. 12 show the impor-
tance of anthropogenic inﬂuence in explaining catchment-
scale variation in metric values, with a negative relationship
being observed for having more relative anthropogenic in-
ﬂuence. We found that LULC affected all the metrics ex-
cept for FAR, where over-prediction was found not to be
as affected by the anthropogenic inﬂuence. Under-prediction
does appear to be prevalent in regions of anthropogenic in-
ﬂuence, which could be explained by a variety of factors,
including DEM inconsistencies or adverse effects on hydro-
conditioning in areas with rapidly varying or uncertain el-
evations. It does appear that anthropogenic inﬂuence also
contributes to more variation within the more case than in
the less case, which could be a result of noise that is in-
herited from elevation inputs. While the magnitude per se
is a signiﬁcant factor in explaining catchment-scale agree-
ment, it does not interact with grouped LULCs, meaning an-
thropogenic inﬂuence seems to have a similar effect across
event magnitudes. Another interesting observation related to
LULC is that the grouped LULCs do not seem to interact
with spatial resolution. Thus, for this study area, higher reso-
lutions did not provide an improvement in metrics for regions
with more anthropogenic inﬂuence. We leave further analy-
sis of the effect of LULCs and the anthropogenic inﬂuence
on catchment-scale agreement to future work.

4 Discussion

Our results and analysis demonstrated several key meth-
ods that can improve the agreement of continental-scale
FIMs using HAND when compared to engineering-scale
FIM models. The inclusion of higher-quality terrain informa-
tion from 3DEP was able to signiﬁcantly improve the qual-
ity of continental-scale HAND-based FIMs. This ﬁnding is
consistent with previous studies that have come to similar
conclusions (Li et al., 2022; Zheng et al., 2018a; Garousi-
Nejad et al., 2019; Speckhann et al., 2018) while also meet-
ing the goal of the 3DEP objectives set out in justifying the

collection effort (Dewberry, 2011; Snyder et al., 2013; Sug-
arbaker et al., 2014). As the program approaches continental-
scale availability, 3DEP data can be justiﬁed for direct use in
HAND computation for the entire US, leading to enhanced
FIM and forecast quality.

However, varying the spatial resolution of the 3DEP
DEMs from their native 1 m was found to have little ef-
fect on the quality of HAND-based FIMs, at least within
20 m resolution. Additional analysis extending comparisons
of HAND-based FIMs at coarser resolutions, 60 and 90 m,
revealed a signiﬁcant degradation of performance at these
scales. Previous studies examining this (Li et al., 2022;
Zheng et al., 2018a; Garousi-Nejad et al., 2019; Speckhann
et al., 2018) have varied in their experimental design and
modeling assumptions. The modeling assumptions in those
studies were different to those used in our HAND methods as
we employ different datasets and hydro-conditioning proce-
dures and compute HAND at ﬁner scales (Aristizabal et al.,
2023c). The experimental design of some previous studies
(Zheng et al., 2018a; Garousi-Nejad et al., 2019) looked at
high-resolution terrain data but did not explicitly isolate that
factor for analysis purposes. Additionally, previous studies
failed to denote a consistent relationship with spatial resolu-
tion and FIM performance (Li et al., 2022; Speckhann et al.,
2018). While the mechanisms of this relationship have not
been thoroughly explored with HAND, others have found
that spatial resolution may have a spurious relationship with
FIM performance due to inherent uncertainties related to this
problem (Savage et al., 2016). Future research can expand the
analysis of spatial resolution’s effect on FIM quality to more
study sites across broader domains of interest. Future re-
search can also explore the effect spatial resolution may have
on the quality of FIM depths as they likely behave some-
what independently to an extent. Additionally, we would like
to motivate alternative benchmark datasets that could further
our understanding of how DEM source and resolution affect
the quality of HAND-based FIMs (Afshari et al., 2018). Uti-
lizing 2D hydraulic models along with high-resolution and
high-quality DEMs could furnish additional insights into this
relationship as higher-order physics would produce varying
extents compared to that of our 1D HEC-RAS benchmark
(Afshari et al., 2018).

Further analysis sought to explain some of the catchment-
level variation in the four agreement metrics with the aim
of indicating where future progress can be made in extend-
ing FIM quality for continental-scale applications. As a re-
sult of the regression analysis, one-ﬁfth to one-third of the
catchment-scale variation of the agreement metric values
was explained by building linear models with 11 explana-
tory variables and their two-way interactions. These models,
while used for analysis purposes in this study, can have pre-
dictive performance, which could have calibration applica-
tions. Previous works have used a variety of methods to help
calibrate Manning’s n or bathymetry (Zheng et al., 2018b;
Johnson et al., 2019; Jian et al., 2017; Neal et al., 2021; Liu

Hydrol. Earth Syst. Sci., 28, 1287–1315, 2024

https://doi.org/10.5194/hess-28-1287-2024

F. Aristizabal et al.: Effects of high-quality elevation data and other variables on FIM skill

1307

Figure 12. Distribution of catchment-scale agreement across four metrics illustrated as box plots and grouped by the level of anthropogenic
inﬂuence in the National Land Cover Database (NLCD) land use and land covers (LULCs) and the two event magnitudes. The results of
a linear model that regresses the catchment-scale metrics according to grouped LULC, magnitude, and their interaction are shown. The
coefﬁcients for the model are labeled with their p values by no asterisk and three asterisks for the p values greater than 0.05 and less
than 0.001, respectively. Additionally, the trend lines resulting in a regression with catchment-scale metrics in grouped LULC are shown per
event magnitude. It is important to note that LULC was found not to interact with spatial resolution within our regression analysis, meaning
that various LULCs perform similarly across varying spatial resolutions.

https://doi.org/10.5194/hess-28-1287-2024

Hydrol. Earth Syst. Sci., 28, 1287–1315, 2024

1308

F. Aristizabal et al.: Effects of high-quality elevation data and other variables on FIM skill

et al., 2019). Due to the complex and interconnected nature
of the source hydrography, hydro-conditioning operations,
reach-averaged channel geometry, and Manning’s n, any sort
of calibration for SRCs would involve using the same sets of
methods and datasets used to produce our version of HAND-
based FIM.

Some of the explanatory variables were explored in fur-
ther detail to provide insights into possible future skill im-
provements for OWP HAND-based FIM. Reservoirs were
found to be one of the leading independent variables in ex-
plaining catchment-scale variation in three of the four met-
rics, mostly driven by under-prediction or FNs. These errors
are caused by not accounting for reservoir inundation within
OWP HAND FIM. Several methods exist for accounting for
reservoir inundation, which could leverage volume compu-
tations with the NWM (Gochis et al., 2021; Chen et al.,
2018; Shin et al., 2019). It is important to note here that,
while reservoirs explained a signiﬁcant amount of variation
in the metrics, this does not mean that accounting for reser-
voir inundation properly would lead to a signiﬁcant increase
in agreement. Agreement will only change in response to the
quality of the new method employed, as well as the preva-
lence of reservoir inundation in a given region. Another vari-
able of interest further analyzed included the effect of LULC
on agreement metrics. We found that HAND FIMs did not
perform as well in catchments that are labeled as developed
or cultivated crops. Regions of high anthropogenic inﬂuence
negatively inﬂuence the performance of inundation models
by adding extra complexity to the terrain information and the
physics employed. Furthering the performance in these re-
gions could beneﬁt from the use of hyper-resolution mod-
els that better account for urban water features (Grimley
et al., 2017; Smith et al., 2020; Deo et al., 2018; Gurung
et al., 2018; Smith et al., 2021; Leandro et al., 2016; Chegini
et al., 2021). Further exploring these and other independent
variables could help inform future development directions
to help improve the quality of continental-scale FIM tech-
niques.

maps (DEMs), so we evaluated its use at 10 m spatial reso-
lution within the derivation of HAND and found signiﬁcant
increases in the quality of FIM performance. Additionally,
we varied the resolution to include 3, 5, 15, and 20 m but did
not ﬁnd any signiﬁcant trends on an overall basis, leading one
to justify its use within these study regions. However, a sig-
niﬁcant degradation in FIM skill was observed at the coarser
resolutions of 60 and 90 m. As one would expect, the compu-
tational time increased to compute HAND with the number
of DEM cells considered, which goes up with the inverse of
the DEM resolution squared. We determined that more stud-
ies are required in other regions to help explore the poten-
tial beneﬁts of the use of higher-resolution DEMs along with
HAND. A multiple linear regression model ﬁtting 11 factors
and covariates to the four agreement metrics, all at the catch-
ment scale, revealed that about one-ﬁfth to one-third of the
variation can be explained by these explanatory variables.

Above

Code and data availability. Height
Nearest
Drainage (HAND) data produced for this study can be found
on our Earth Science Information Partners (ESIP)-backed Ama-
(https://noaa-nws-owp-ﬁm.s3.
zon Web Services S3 bucket
amazonaws.com/hand_ﬁm, Aristizabal et al., 2023a). Software
used in this study is available on GitHub (https://github.com/
NOAA-OWP/inundation-mapping, Aristizabal et al., 2023b).
A permanent version of this code and data is available as well
(https://doi.org/10.4211/hs.3d98a9e5a6d84020b72800fd27c87f9a,
Aristizabal, 2023).

Author contributions. Conceptualization: FA, GP, and FS. Method-
ology: FA, FS, GP, and JJ. Software: FA, GP, and TC. Validation: FA
and GP. Formal analysis: FA, GP, and FS. Investigation: FA, GP,
and FS. Resources: FS. Data curation: FA, GP, and TC. Writing –
original draft preparation: FA and TC. Writing – review and edit-
ing: FA, FS, GP, TC, and JJ. Visualization: FA. Supervision: FS
and JJ. Project administration: FS and JJ. Funding acquisition: FS.
All authors have read and agreed to the published version of the
paper.

5 Conclusions

Floods are a signiﬁcant source of natural disasters in the
United States (US), leading to loss of property and lives.
The National Oceanic and Atmospheric Administration’s Of-
ﬁce of Water Prediction (OWP) has implemented the Na-
tional Water Model (NWM) to help forecast streamﬂows at
nearly 3 million locations across the continuous US, Hawaii,
Puerto Rico, and portions of Alaska at hourly time steps and
multiple forecast horizons. OWP has developed its own ver-
sion of Height Above Nearest Drainage (HAND) that ac-
counts for multiple ﬂuvial sources of inundation instead of
just that from the local, nearest ﬂow path. The United States
Geological Survey’s 3D Elevation Program is rapidly ap-
proaching continental-scale availability of digital elevation

Competing interests. The contact author has declared that none of
the authors has any competing interests.

Disclaimer. Publisher’s note: Copernicus Publications remains
neutral with regard to jurisdictional claims made in the text, pub-
lished maps, institutional afﬁliations, or any other geographical rep-
resentation in this paper. While Copernicus Publications makes ev-
ery effort to include appropriate place names, the ﬁnal responsibility
lies with the authors.

Acknowledgements. We would like to thank Jason Stoker and his
team of the 3D Elevation Program (3DEP) for producing analysis-
friendly services and for answering our questions related to these

Hydrol. Earth Syst. Sci., 28, 1287–1315, 2024

https://doi.org/10.5194/hess-28-1287-2024

F. Aristizabal et al.: Effects of high-quality elevation data and other variables on FIM skill

1309

services. Additionally, we would like to thank Fred Ogden, chief
scientist of the Ofﬁce of Water Prediction (OWP), for his help re-
viewing and providing scientiﬁc direction. We would like to ac-
knowledge the use of large language models (LLMs) in the editing
process of this paper to enhance the clarity, coherence, and gram-
matical accuracy of our writing.

Financial support. This research has been supported by the Na-
tional Oceanic and Atmospheric Administration (grant no. WY351-
3001-01).

Review statement. This paper was edited by Roger Moussa and re-
viewed by two anonymous referees.

References

Afshari, S., Tavakoly, A. A., Rajib, M. A., Zheng, X., Follum, M. L.,
Omranian, E., and Fekete, B. M.: Comparison of new generation
low-complexity ﬂood inundation mapping tools with a hydrody-
namic model, J. Hydrol., 556, 539–556, 2018.

Alajo, S. O., Nakavuma, J., and Erume, J.: Cholera in endemic dis-
tricts in Uganda during El Niño rains: 2002–2003, Afr. Health
Sci., 6, 93–97, 2006.

Archuleta, C.-A. M., Constance, E. W., Arundel, S. T., Lowe, A. J.,
Mantey, K. S., and Phillips, L. A.: The National Map seamless
digital elevation model speciﬁcations, Tech. rep., US Geological
Survey, https://doi.org/10.3133/tm11B9, 2017.

Aristizabal, F.: Data

and Software

for Effects of High-
on
Quality Elevation Data
the Accuracy of Flood Inundation Mapping via Height
Above Nearest Drainage, Hydroshare [code and data set],
https://doi.org/10.4211/hs.3d98a9e5a6d84020b72800fd27c87f9a,
2023.

and Explanatory Variables

Clustering

J.: Mapping Fluvial

Aristizabal, F. and Judge,

from Unsupervised
Imagery,

Inundation
Extents with Graph Signal Filtering of River Depths
Determined
Syn-
thetic Aperture Radar
in: 2021 IEEE Inter-
and Remote Sensing Symposium
national Geoscience
IGARSS, 11–16 July 2021, Brussels, Belgium, 6124–6127,
https://doi.org/10.1109/IGARSS47720.2021.9553575, 2021.
Aristizabal, F., Judge, J., and Monsivais-Huertero, A.: High-
Resolution Inundation Mapping for Heterogeneous Land Covers
with Synthetic Aperture Radar and Terrain Data, Remote Sens.,
12, 900, https://doi.org/10.3390/rs12060900, 2020.

of

Aristizabal, F., Bates, B., Avant, B., Chadwick, N., Grout, T.,
Spies, R., Luck, M., Salas, F., Pruitt, C., Hanna, R., and Cocks,
G.: noaa-nws-owp-ﬁm, NOAA, https://noaa-nws-owp-ﬁm.s3.
amazonaws.com/hand_ﬁm (last access: 30 June 2023, access re-
quires the installation of the AWS command line interface [AWS-
CLI] and might be subject to payment), 2023a.

Aristizabal, F., Bates, B., Avant, B., Chadwick, N., Grout, T.,
Spies, R., Luck, M., Salas, F., Pruitt, C., Hanna, R., and Cocks,
G.: NOAA-OWP/inundation-mapping, NOAA, GitHub [code],
https://github.com/NOAA-OWP/inundation-mapping (last ac-
cess: 30 June 2023), 2023b.

Aristizabal, F., Salas, F., Petrochenkov, G., Grout, T., Avant, B.,
Bates, B., Spies, R., Chadwick, N., Wills, Z., and Judge, J.:
Extending Height Above Nearest Drainage to Model Multi-
ple Fluvial Sources in Flood Inundation Mapping Applica-
tions for the US National Water Model, Water Resour. Res.,
59, e2022WR032039, https://doi.org/10.1029/2022WR032039,
2023c.

Arundel, S., Phillips, L., Lowe, A., Bobinmyer, J., Mantey, K.,
Dunn, C., Constance, E., and Usery, E.: Preparing The National
Map for the 3D Elevation Program – products, process and re-
search, Cartogr. Geogr. Inform. Sci., 42, 40–53, 2015.

Arundel, S., Bulen, A., Adkins, K., Brown, R., Lowe, A., Mantey,
K., and Phillips, L.: Assimilation of the National Elevation
Dataset and launch of the 3D elevation program through the
USGS spatial data infrastructure, Int. J. Cartogr., 4, 129–150,
2018.

Arundel, S. T., Archuleta, C.-A. M., Phillips, L. A., Roche, B. L.,
and Constance, E. W.: 1-meter digital elevation model speciﬁca-
tion, chap. 7, USGS, https://doi.org/10.3133/tm11B7, 2015.
Bales, J. and Wagner, C.: Sources of uncertainty in ﬂood inundation

maps, J. Flood Risk Manage., 2, 139–147, 2009.

Bashtannyk, D. M. and Hyndman, R. J.: Bandwidth selection for
kernel conditional density estimation, Comput. Stat. Data Anal.,
36, 279–298, 2001.

Bates, P., Marks, K., and Horritt, M.: Optimal use of high-resolution
topographic data in ﬂood inundation models, Hydrol. Process.,
17, 537–557, 2003.

Bates, P. D. and De Roo, A.: A simple raster-based model for ﬂood

inundation simulation, J. Hydrol., 236, 54–77, 2000.

Baudoin, M.-A., Henly-Shepard, S., Fernando, N., and Si-
tati, A.: Early warning systems and livelihood resilience:
Exploring opportunities for community participation, UNU-
EHS Working Paper Series No. 11, UNU-EHS – United
Nations University Institute of Environment and Human
https://collections.unu.edu/eserv/UNU:
Security,
3174/Early_Warning_Systems_WP_No_11_.pdf
(last access:
19 March 2024), 2014.

Bonn,

Beinin, L.: Medical consequences of natural disasters, Springer Sci-

ence & Business Media, ISBN 978-0387155067, 2012.

Berz, G.: Flood disasters: lessons from the past – worries for the
future, in: Proceedings of the institution of civil engineers-water
and maritime engineering, vol. 142, Thomas Telford Ltd, 3–8,
https://doi.org/10.1680/maen.148.1.57.40368, 2000.

Birkmann, J., Buckle, P., Jaeger, J., Pelling, M., Setiadi, N.,
Garschagen, M., Fernando, N., and Kropp, J.: Extreme events
and disasters: a window of opportunity for change? Analysis of
organizational, institutional and political changes, formal and in-
formal responses after mega-disasters, Nat. Hazards, 55, 637–
655, 2010.
Boughorbel, S.,
for

Jarray, F.,
classiﬁer
imbalanced
12,
relation Coefﬁcient metric, PloS One,
https://doi.org/10.1371/journal.pone.0177678, 2017.

and El-Anbari, M.: Optimal
using Matthews Cor-
data
e0177678,

Callahan, D. and Berber, M. M.: Vertical accuracy of

the
USGS 3DEP program data: study cases in Fresno County and
in Davis, California, Boletim de Ciências Geodésicas, 9 pp.,
https://doi.org/10.1590/s1982-21702022000100004, 2022.

Carruthers, A.: The assessment, improvement, and application of
the GeoFlood ﬂood inundation mapping framework, PhD thesis,

https://doi.org/10.5194/hess-28-1287-2024

Hydrol. Earth Syst. Sci., 28, 1287–1315, 2024

1310

F. Aristizabal et al.: Effects of high-quality elevation data and other variables on FIM skill

University of Texas, Austin, https://doi.org/10.26153/tsw/14294,
2021.

Charlesworth, S. M. and Warwick, F.: 15 Adapting to and Mitigat-
ing Floods Using Sustainable Urban Drainage Systems, Flood
Hazards: Impacts and Responses for the Built Environment,
CRC Press, p. 207, https://doi.org/10.1201/b11050-19, 2011.
Chatterjee, S. and Simonoff, J. S.: Handbook of regression analysis,

John Wiley & Sons, ISBN 9780470887165, 2013.

Chegini, T., Li, H.-Y., and Leung, L. R.: HyRiver: Hy-
droclimate Data Retriever, J. Open Sour. Softw., 6, 1–3,
https://doi.org/10.21105/joss.03175, 2021.

Chen, W., Nover, D., He, B., Yuan, H., Ding, K., Yang, J., and Chen,
S.: Analyzing inundation extent in small reservoirs: A combined
use of topography, bathymetry and a 3D dam model, Measure-
ment, 118, 202–213, 2018.

Chicco, D. and Jurman, G.: The advantages of the Matthews cor-
relation coefﬁcient (MCC) over F1 score and accuracy in binary
classiﬁcation evaluation, BMC Genom., 21, 1–13, 2020.

Chicco, D., Starovoitov, V., and Jurman, G.: The beneﬁts of the
Matthews correlation coefﬁcient (MCC) over the diagnostic odds
ratio (DOR) in binary classiﬁcation assessment, IEEE Access, 9,
47112–47124, 2021a.

Chicco, D., Warrens, M. J., and Jurman, G.: The Matthews correla-
tion coefﬁcient (MCC) is more informative than Cohen’s Kappa
and Brier score in binary classiﬁcation assessment, IEEE Access,
9, 78368–78381, 2021b.

Chow, V. T.: Development of uniform ﬂow and its formulas,
Open-channel hydraulics, edited by: Harmer, D. E., McGraw-
Hill Book Company, USA, 89–114,
ISBN 007085906X,
ISBN 9780070859067, 1959.

Cohen, S., Praskievicz, S., and Maidment, D. R.: Featured collec-
tion introduction: National water model, J. Am. Water Resour.
Assoc., 54, 767–769, https://doi.org/10.1111/1752-1688.12664,
2018.

Cook, A. and Merwade, V.: Effect of topographic data, geometric
conﬁguration and modeling approach on ﬂood inundation map-
ping, J. Hydrol., 377, 131–142, 2009.

Cools, J., Innocenti, D., and O’Brien, S.: Lessons from ﬂood early

warning systems, Environ. Sci. Policy, 58, 117–122, 2016.

Corringham, T. W. and Cayan, D. R.: The effect of El Niño on ﬂood
damages in the western United States, Weather Clim. Soc., 11,
489–504, 2019.

Cosgrove, B., Gochis, D., Graziano, T. M., Clark, E. P., and
Flowers, T.: The Evolution of NOAA’s National Water Model:
An Overview of Version 2.1 and Future Operational Plans,
AGUFM, H51D-01, American Geophysical Union, https://ui.
adsabs.harvard.edu/abs/2019AGUFM.H51D..01C/abstract
(last
access: December 2021), 2019.

Criss, R. E.

and Nelson, D. L.: Stage-based ﬂood in-
2385–2401,

112,

undation mapping, Nat. Hazards,
https://doi.org/10.1007/s11069-022-05270-6, 2022.

D’Angelo, C., Passalacqua, P., Fiori, A., and Volpi, E.: Identiﬁca-
tion of ﬂood-prone areas with GeoFlood: Lessons learned from
the Tiber River case study, J. Flood Risk Manage., 15, e12795,
https://doi.org/10.1111/jfr3.12795, 2022.

de Almeida, G. A., Bates, P., and Ozdemir, H.: Modelling urban
ﬂoods at submetre resolution: challenges or opportunities for
ﬂood risk management?, J. Flood Risk Manage., 11, S855–S865,
2018.

Deo,

I., Modi, P., Zarekarizi, M., and Valle, J.: Sensitiv-
subsurface storm
ity of urban ﬂooding to presence of
low-gradient
for
drainage systems
in hydrologic models
Innovators Program
watersheds, National Water Center
Institute Report 53, Consortium of Universi-
Summer
ties
Inc.,
the Advancement of Hydrologic Science,
for
https://doi.org/10.4211/hs.c7ee150767114d3a927b67a94f0edc04,
2018.
Dewberry:

the National

Final

Report
of
Assessment,

Enhanced
https://www.dewberry.

Elevation
com/services/geospatial-mapping-and-survey/
national-enhanced-elevation-assessment-ﬁnal-report
access: March 2023), 2011.

(last

Dewberry: 3D Nation Elevation Requirements and Beneﬁts Study
– Final Report, Tech. rep., Dewberry, Fairfax, VA, 22031–4666,
https://www.dewberry.com/docs/default-source/documents/
3d-nation-elevation-requirements-and-beneﬁts-study/3d_
nation_study_ﬁnal_report.pdf (last access: September 2023),
2022.

Dewitz, J. U. G. S.: National Land Cover Database (NLCD)
2021): US Geolog-
Survey,

2019
ical
https://doi.org/10.5066/P9KZCM54, 2021.

release, US Geological

Products
Survey

June

(ver.

data

2.0,

Diehl, R. M., Gourevitch, J. D., Drago, S., and Wemple, B. C.:
Improving ﬂood hazard datasets using a low-complexity, prob-
abilistic ﬂoodplain mapping approach, PloS One, 16, e0248683,
https://doi.org/10.1371/journal.pone.0248683, 2021.

Dixon, B. and Earls, J.: Resample or not?! Effects of resolution of
DEMs in watershed modeling, Hydrol. Process., 23, 1714–1724,
2009.

Dobbs, K. E.: Evaluation of the Usgs National Elevation Dataset
and the Kansas Biological Survey’s FLDPLN (“Floodplain”)
Model for Inundation Extent Estimation, PhD thesis, Uni-
versity of Kansas, http://hdl.handle.net/1808/6431 (last access:
April 2010), 2010.

Doocy, S., Daniels, A., Murray, S., and Kirsch, T. D.: The
human impact of ﬂoods: a historical
review of events
1980–2009 and systematic literature review, PLoS Curr., 5,
https://doi.org/10.1371/currents.dis.f4deb457904936b07c09daa,
2013.

Downton, M. W., Miller, J. Z. B., and Pielke Jr, R. A.: Reanalysis of
US National Weather Service ﬂood loss database, Nat. Hazards
Rev., 6, 13–22, 2005.

Drury, A. C. and Olson, R. S.: Disasters and political unrest: An
empirical investigation, J. Conting. Cris. Manage., 6, 153–161,
1998.

Federal

FEMA: Guidance

for Flood Risk Analysis

and Map-
ping: Automated Engineering, Guidance Document 27,
FEMA –
Emergency Management Agency,
https://www.fema.gov/sites/default/ﬁles/2020-02/Automated_
Engineering_Guidance_May_2016.pdf (last access: May 2021),
2016.
FEMA:

Engineering

Level

Tools

Base

Resources,
base-level-engineering-ble-tools-and-resources
February 2024), 2021a.

and
(BLE)
https://www.fema.gov/media-collection/
access:

(last

FEMA: estBFE Viewer, https://webapps.usgs.gov/infrm/estBFE/

(last access: February 2024)„ 2021b.

Hydrol. Earth Syst. Sci., 28, 1287–1315, 2024

https://doi.org/10.5194/hess-28-1287-2024

F. Aristizabal et al.: Effects of high-quality elevation data and other variables on FIM skill

1311

Fewtrell, T., Bates, P. D., Horritt, M., and Hunter, N.: Evaluating
the effect of scale in ﬂood inundation modelling in urban envi-
ronments, Hydrol. Process., 22, 5107–5118, 2008.

Follum, M. L., Tavakoly, A. A., Niemann, J. D., and Snow, A. D.:
AutoRAPID: a model for prompt streamﬂow estimation and
ﬂood inundation mapping over regional to continental extents,
J. Am. Water Resour. Assoc., 53, 280–299, 2017.

French, J., Ing, R., Von Allmen, S., and Wood, R.: Mortality from
ﬂash ﬂoods: a review of national weather service reports, 1969–
81, Public Health Reports, 98, 584–588, 1983.

Garousi-Nejad, I., Tarboton, D. G., Aboutalebi, M., and Torres-Rua,
A. F.: Terrain analysis enhancements to the height above nearest
drainage ﬂood inundation mapping method, Water Resour. Res.,
55, 7983–8009, 2019.

Gerapetritis, H. and Pelissier, J. M.: On the behavior of the critical
success index, National Weather Service, https://www.weather.
gov/media/erh/ta2004-03.pdf (last access: April 2021), 2004.
Gesch, D., Oimoen, M., Greenlee, S., Nelson, C., Steuck, M., and
Tyler, D.: The National Elevation Dataset: Photogrammetric en-
gineering and remote sensing, Photogram. Eng. Remote Sens.,
68, 5–32, 2002.

Gesch, D., Evans, G., Mauck, J., Hutchinson, J., and Carswell Jr.,
W. J.: The national map – Elevation, US geological survey fact
sheet 3053, US Geological Survey, https://api.semanticscholar.
org/CorpusID:126546678 (last access: April 2022), 2009.
Gesch, D. B. and Maune, D.: Digital elevation model

tech-
nologies and applications: the DEM users manual, The na-
tional elevation dataset, 2nd Edn. American Society for
Photogrammetry and Remote Sensing, Bethesda, 99–118,
https://doi.org/10.3133/ofr20141008, 2007.

Gesch, D. B., Oimoen, M. J., Evans, G. A., et al.: Accu-
racy assessment of the US Geological Survey National Ele-
vation Dataset, and comparison with other large-area eleva-
tion datasets: SRTM and ASTER, vol. 1008, US Department
of the Interior, US Geological Survey, Sioux Falls, SD, USA,
https://doi.org/10.3133/ofr20141008, 2014.

Gochis, D., Dugger, A., Barlage, M., Cabell, R., FitzGerald,
K., McAllister, M., McCreight, J., RaﬁeeiNasab, A., Read,
L., Sampson, K., Yates, D., and Zhang, Y.: The WRF-
Hydro modeling system technical description (Version 5.2),
Tech. rep., NCAR, https://ral.ucar.edu/sites/default/ﬁles/public/
WRFHydroV511TechnicalDescription.pdf (last access: Decem-
ber 2022), 2021.

Godbout, L., Zheng, J. Y., Dey, S., Eyelade, D., Maidment, D., and
Passalacqua, P.: Error assessment for height above the nearest
drainage inundation mapping, J. Am. Water Resour. Assoc., 55,
952–963, 2019.

Golnaraghi, M.: An Overview: Building a global knowledge
base of lessons learned from good practices in multi-hazard
early warning systems,
Institutional partnerships in multi-
hazard early warning systems, Springer, Berlin, Heidelberg, 1–8,
https://doi.org/10.1007/978-3-642-25373-7_1, 2012.

Gourevitch, J. D., Kousky, C., Liao, Y. P., Nolte, C., Pol-
lack, A. B., Porter, J. R., and Weill, J. A.: Unpriced cli-
mate risk and the potential consequences of overvaluation
in US housing markets, Nat. Clim. Change, 13, 250–257,
https://doi.org/10.1038/s41558-023-01594-8, 2023.

Grimley, L. E., Tijerina, D., Khanam, M., Tiernan, E. D., Frazier,
N., Ogden, F. L., Steinke, R. C., Maxwell, R. M., and Cohen, S.:

Grid vs Mesh: The case of Hyper-resolution Modeling in Urban
Landscapes, in: vol. 2017, AGU Fall Meeting Abstracts, Decem-
ber 2017, New Orleans, LA, USA, H53F-1541, 2017.

Gurung, D., Goenner, A., Perez, F., and Rouf, T.: Effects
of Spatial Resolution on a Distributed Hydrologic Model
through Dynamical Forcings: Flood Extent and Depth in
Inno-
Low Gradient Watersheds, National Water Center
vators Program Summer
Institute Report 2018, National
Water Center Innovators Program Summer Institute, p. 40,
https://doi.org/10.4211/hs.c7ee150767114d3a927b67a94f0edc04,
2018.

Heidemann, H. K.: Lidar base speciﬁcation, chap. 4, USGS,

https://doi.org/10.3133/tm11b4, 2018.

Hocini, N., Payrastre, O., Bourgin, F., Gaume, E., Davy, P.,
Lague, D., Poinsignon, L., and Pons, F.: Performance of au-
tomated methods for ﬂash ﬂood inundation mapping: a com-
parison of a digital terrain model (DTM) ﬁlling and two hy-
drodynamic methods, Hydrol. Earth Syst. Sci., 25, 2979–2995,
https://doi.org/10.5194/hess-25-2979-2021, 2021.

Huang, C., Nguyen, B. D., Zhang, S., Cao, S., and Wagner, W.:
A comparison of terrain indices toward their ability in assisting
surface water mapping from Sentinel-1 data, ISPRS Int. J. Geo-
Inform., 6, 140, https://doi.org/10.3390/ijgi6050140, 2017.

Jafarzadegan, K. and Merwade, V.: A DEM-based approach for
large-scale ﬂoodplain mapping in ungauged watersheds, J. Hy-
drol., 550, 650–662, 2017.

Jafarzadegan, K. and Merwade, V.: Probabilistic ﬂoodplain map-
ping using HAND-based statistical approach, Geomorphology,
324, 48–61, 2019.

Jann, B.: Making regression tables from stored estimates, Stata J.,

5, 288–308, 2005.

Jian, J., Ryu, D., Costelloe, J. F., and Su, C.-H.: Towards hydrologi-
cal model calibration using river level measurements, J. Hydrol.:
Reg. Stud., 10, 95–109, 2017.

Johnson, J. M., Munasinghe, D., Eyelade, D., and Cohen, S.: An
integrated evaluation of the National Water Model (NWM)–
Height Above Nearest Drainage (HAND) ﬂood mapping
methodology, Nat. Hazards Earth Syst. Sci., 19, 2405–2420,
https://doi.org/10.5194/nhess-19-2405-2019, 2019.

Jonkman, S. N.: Global perspectives on loss of human life caused

by ﬂoods, Nat. Hazards, 34, 151–175, 2005.

Kahn, M. E.: The death toll from natural disasters: the role of in-
come, geography, and institutions, Rev. Econ. Stat., 87, 271–284,
2005.

Kalyanapu, A. J., Burian, S. J., and McPherson, T. N.: Effect of
land use-based surface roughness on hydrologic model output, J.
Spat. Hydrol., 9, 2, 2009.

Kelmelis, J. A., DeMulder, M. L., Ogrosky, C. E., Van Driel, N. J.,
and Ryan, B. J.: The National Map from geography to mapping
and back again, Photogram. Eng. Remote Sens., 69, 1109–1118,
2003.

Kim, M., Stoker, J.,

Absolute Accuracy Assessment
Using Amorphous Objects, Remote Sens.,
https://doi.org/10.3390/rs14194767, 2022.

Irwin, J., Danielson, J., and Park, S.:
of Lidar Point Cloud
4767,

14,

Kunkel, K. E., Pielke Jr, R. A., and Changnon, S. A.: Temporal
ﬂuctuations in weather and climate extremes that cause economic
and human health impacts: A review, B. Am. Meteorol. Soc., 80,
1077–1098, 1999.

https://doi.org/10.5194/hess-28-1287-2024

Hydrol. Earth Syst. Sci., 28, 1287–1315, 2024

1312

F. Aristizabal et al.: Effects of high-quality elevation data and other variables on FIM skill

Leandro, J., Schumann, A., and Pﬁster, A.: A step towards consid-
ering the spatial heterogeneity of urban key features in urban hy-
drology ﬂood modelling, J. Hydrol., 535, 356–365, 2016.

Li, Z. and Demir,

I.: U-Net-based Semantic Classiﬁcation
for Flood Extent Extraction using SAR Imagery and GEE
Platform: A Case Study for 2019 Central US Flooding,
https://doi.org/10.1016/j.scitotenv.2023.161757, 2022.

Li, Z., Mount, J., and Demir,
rameters of HAND Model
tion Mapping:
https://doi.org/10.31223/osf.io/hqpzg, 2020.

I.: Evaluation of Model Pa-
for Real-Time Flood Inunda-
Iowa Case Study, Earth Arxiv [prepint],

Li, Z., Mount, J., and Demir, I.: Accounting for uncertainty in real-
time ﬂood inundation mapping using HAND model: Iowa case
study, Nat. Hazards, 112, 977–1004, 2022.

Li, Z., Duque, F. Q., Grout, T., Bates, B., and Demir,
I.: Comparative Analysis of Performance and Mechanisms
of Flood Inundation Map Generation using Height Above
Nearest Drainage, Environ. Model. Softw., 159, 105565,
https://doi.org/10.1016/j.envsoft.2022.105565, 2023.

Liu, C., Guo, L., Ye, L., Zhang, S., Zhao, Y., and Song, T.: A review
of advances in China’s ﬂash ﬂood early-warning system, Nat.
Hazards, 92, 619–634, 2018.

Liu, Y., Tarboton, D. G., and Maidment, D. R.: Height Above Near-
est Drainage (HAND) and Hydraulic Property Table for CONUS,
Tech. rep., ORNL – Oak Ridge National Lab., Oak Ridge, TN,
USA, https://doi.org/10.13139/ORNLNCCS/1630903, 2020.
Liu, Y. Y., Maidment, D. R., Tarboton, D. G., Zheng, X.,
Yildirim, A., Sazib, N. S., and Wang, S.: A CyberGIS
approach to generating high-resolution height above near-
for national ﬂood mapping,
est drainage (HAND)
in: The Third International Conference on CyberGIS and
Geospatial Data Science, 26–28 July 2016, Urbana,
IL,
https://doi.org/10.13140/RG.2.2.24234.41925/1, 2016.

raster

Liu, Y. Y., Maidment, D. R., Tarboton, D. G., Zheng, X., and
Wang, S.: A CyberGIS integration and computation framework
for high-resolution continental-scale ﬂood inundation mapping,
J. Am. Water Resour. Assoc., 54, 770–784, 2018.

Liu, Z., Merwade, V., and Jafarzadegan, K.: Investigating the
role of model structure and surface roughness in generat-
ing ﬂood inundation extents using one-and two-dimensional
hydraulic models,
J. Flood Risk Manage., 12, e12347,
https://doi.org/10.1111/jfr3.12347, 2019.

Maidment, D. R.: Conceptual Framework for the National Flood
Interoperability Experiment, J. Am. Water Resour. Assoc., 53,
245–257, https://doi.org/10.1111/1752-1688.12474, 2017.

Mallakpour, I. and Villarini, G.: The changing nature of ﬂooding
across the central United States, Nat. Clim. Change, 5, 250–254,
2015.

Mason, D. C., Horritt, M. S., Hunter, N. M., and Bates, P. D.: Use of
fused airborne scanning laser altimetry and digital map data for
urban ﬂood modelling, Hydrol. Process., 21, 1436–1447, 2007.
Maune, D. F. and Nayegandhi, A.: Digital elevation model technolo-
gies and applications: The DEM users manual, American Society
for Photogrammetry and Remote Sensing, ISBN 1-57083-102-5,
2018.

McCuen, R. H. et al.: Hydrologic analysis and design,

in:
vol. 3, Pearson, prentice hall, Upper Saddle River, NJ,
ISBN 13:9780134313122, 2005.

McGehee, R., Li, L., and Poston, E.: The Modiﬁed HAND
Method, in: National Water Center Innovators Program Sum-
mer Institute Report 2016, vol. 4, edited by: Maidment, D. R.,
Rajib, A., Lin, P., and Clark, E. P., Consortium of Uni-
versities for the Advancement of Hydrologic Science, Inc.,
https://doi.org/10.4211/technical.20161019, 2016.

McGrath, H., Bourgon, J.-F., Proulx-Bourque, J.-S., Nastev, M., and
Abo El Ezz, A.: A comparison of simpliﬁed conceptual models
for rapid web-based ﬂood inundation mapping, Nat. Hazards, 93,
905–920, 2018.

Merrill, H. R., Grunwald, S., and Bliznyuk, N.: Semiparametric re-
gression models for spatial prediction and uncertainty quantiﬁ-
cation of soil attributes, Stoch. Environ. Res. Risk A., 31, 2691–
2703, 2017.

Merwade, V., Olivera, F., Arabi, M., and Edleman, S.: Uncertainty
in ﬂood inundation mapping: current issues and future directions,
J. Hydrol. Eng., 13, 608–620, 2008.

Milly, P. C. D., Wetherald, R. T., Dunne, K., and Delworth, T. L.:
Increasing risk of great ﬂoods in a changing climate, Nature, 415,
514–517, 2002.

Montgomery, D. C., Peck, E. A., and Vining, G. G.: Introduction to
linear regression analysis, John Wiley & Sons, ISBN 978-1-119-
57872-7, 2021.

Moore, R. B., McKay, L. D., Rea, A. H., Bondelid, T. R., Price,
C. V., Dewald, T. G., and Johnston, C. M.: User’s guide
for the National Hydrography Dataset plus (NHDPlus) High
Resolution, Open-File Report, US Geological Survey, p. 60,
https://doi.org/10.3133/ofr20191096, 2019.

Muhadi, N. A., Abdullah, A. F., Bejo, S. K., Mahadi,
M. R., and Mijic, A.: The use of LiDAR-derived DEM
in ﬂood applications: A review, Remote Sens., 12, 2308,
https://doi.org/10.3390/rs12142308, 2020.

Multi-Resolution Land Characteristics Consortium: Data Ser-
vices Page, https://www.mrlc.gov/data-services-page (last ac-
cess: September 2020), 2022.

Muthusamy, M., Casado, M. R., Butler, D., and Leinster, P.:
Understanding the effects of Digital Elevation Model resolu-
tion in urban ﬂuvial ﬂood modelling, J. Hydrol., 596, 126088,
https://doi.org/10.1016/j.jhydrol.2021.126088, 2021.

National Research Council: Elevation Data for Floodplain Map-
ping, The National Academies Press, Washington, D.C.,
https://doi.org/10.17226/11829, 2007.

National Research Council: Mapping the Zone: Improving Flood
Map Accuracy, The National Academies Press, Washington,
D.C., https://doi.org/10.17226/12573, 2009.

Neal, J., Schumann, G., Fewtrell, T., Budimir, M., Bates, P., and
Mason, D.: Evaluating a new LISFLOOD-FP formulation with
data from the summer 2007 ﬂoods in Tewkesbury, UK, J. Flood
Risk Manage., 4, 88–95, 2011.

Neal, J., Hawker, L., Savage, J., Durand, M., Bates, P., and Samp-
son, C.: Estimating river channel bathymetry in large scale ﬂood
inundation models, Water Resour. Res., 57, e2020WR028301,
https://doi.org/10.1029/2020WR028301, 2021.

Nobre, A., Cuartas, L., Hodnett, M., Rennó, C., Ro-
drigues, G., Silveira, A., Waterloo, M.,
and Saleska,
S.: Height Above the Nearest Drainage – a hydrologi-
cally relevant new terrain model, J. Hydrol., 404, 13–29,
https://doi.org/10.1016/j.jhydrol.2011.03.051, 2011.

Hydrol. Earth Syst. Sci., 28, 1287–1315, 2024

https://doi.org/10.5194/hess-28-1287-2024

F. Aristizabal et al.: Effects of high-quality elevation data and other variables on FIM skill

1313

NOAA: National Water Model:

Improving NOAA’s Wa-
https://water.noaa.gov/documents/

ter Prediction Services,
wrn-national-water-model.pdf (last access: May 2022), 2016.
Nobre, A. D., Cuartas, L. A., Momo, M. R., Severo, D. L., Pinheiro,
A., and Nobre, C. A.: HAND contour: a new proxy predictor of
inundation extent, Hydrol. Process., 30, 320–333, 2016.

Ofﬁce of Management and Budget: Coordination of Geographic
Information and Related Spatial Data Activities, Tech. Rep.
Circular A-16 revised, Washington, DC, https://www.fgdc.gov/
policyandplanning/a-16 (last access: September 2020), 2016.
Ofﬁce of Water Prediction: The National Water Model, NOAA,
https://water.noaa.gov/about/nwm (last access: September 2022),
2022.

OWP/ESIP: NWM Hydrofabric V2.1, NOAA,

https:

//noaa-nws-owp-ﬁm.s3.amazonaws.com/hand_ﬁm/ﬁm_3_
(last access: March 2024,
0_34_1/inputs/nwm_hydrofabric/
access requires the installation of the AWS command line
interface [AWS-CLI] and might be subject to payment), 2021.
Ozdemir, H., Sampson, C. C., de Almeida, G. A. M., and Bates, P.
D.: Evaluating scale and roughness effects in urban ﬂood mod-
elling using terrestrial LIDAR data, Hydrol. Earth Syst. Sci., 17,
4015–4030, https://doi.org/10.5194/hess-17-4015-2013, 2013.
Papaioannou, G., Vasiliades, L., Loukas, A., and Aronica, G. T.:
Probabilistic ﬂood inundation mapping at ungauged streams due
to roughness coefﬁcient uncertainty in hydraulic modelling, Adv.
Geosci., 44, 23–34, https://doi.org/10.5194/adgeo-44-23-2017,
2017.

Passalacqua, P., Do Trung, T., Foufoula-Georgiou, E., Sapiro,
G., and Dietrich, W. E.: A geometric framework for
channel network extraction from lidar: Nonlinear diffusion
and geodesic paths, J. Geophys. Res.-Earth, 115, F01002,
https://doi.org/10.1029/2009JF001254, 2010.

Passalacqua, P., Belmont, P., and Foufoula-Georgiou, E.: Auto-
matic geomorphic feature extraction from lidar in ﬂat and
engineered landscapes, Water Resour. Res., 48, W03528,
https://doi.org/10.1029/2011WR010958, 2012.

Passalacqua, P., Belmont, P., Staley, D. M., Simley, J. D., Arrow-
smith, J. R., Bode, C. A., Crosby, C., DeLong, S. B., Glenn, N. F.,
Kelly, S. A., Lague, L., Sangireddy, H., Schaffrath, K., Tarboton,
D. G., Wasklewicz, T., and Wheaton, J. M.: Analyzing high res-
olution topography for advancing the understanding of mass and
energy transfer through landscapes: A review, Earth-Sci. Rev.,
148, 174–193, 2015.

Petrochenkov, G. and Viger, R.: pygft: Rapid ﬂood inundation
modeling tool, USGS, Reston, VA, https://code.usgs.gov/gft/
python-gis-ﬂood-tool (last access: April 2021), 2020.

Pielke Jr., R. A. and Downton, M. W.: Precipitation and damag-
ing ﬂoods: Trends in the United States, 1932–97, J. Climate, 13,
3625–3637, 2000.

Podhorányi, M. and Fedorcak, D.: Inaccuracy introduced by
LiDAR-generated cross sections and its impact on 1D hydrody-
namic simulations, Environ. Earth Sci., 73, 1–11, 2015.

Rajib, A., Merwade, V., and Liu, Z.: Large scale high resolution
ﬂood inundation mapping in near real-time, in: Proceedings of
the 40th Anniversary of the Association of State Flood Plain
Managers National Conference, 19–24 June 2016, Grand Rapids,
MI, USA, 19–24, https://www.asfpmfoundation.org/ace-images/
Adnan_Full2016.pdf (last access: March 2024), 2016.

Rennó, C. D., Nobre, A. D., Cuartas, L. A., Soares, J. V., Hodnett,
M. G., and Tomasella, J.: HAND, a new terrain descriptor us-
ing SRTM-DEM: Mapping terra-ﬁrme rainforest environments
in Amazonia, Remote Sens. Environ., 112, 3469–3481, 2008.
Roman, D. R., Wang, Y. M., Saleh, J., and Li, X.: Geodesy, geoids,
and vertical datums: A perspective from the US National Geode-
tic Survey, in: vol. 11, FIG Congress, https://api.semanticscholar.
org/CorpusID:126725780 (last access: March 2024), 2010.

Salach, A., Bakuła, K., Pilarska, M., Ostrowski, W., Górski, K., and
Kurczy´nski, Z.: Accuracy assessment of point clouds from Li-
DAR and dense image matching acquired using the UAV plat-
form for DTM creation, ISPRS Int. J. Geo-Inform., 7, 342,
https://doi.org//10.3390/ijgi7090342, 2018.

Salas, F. R., Somos-Valenzuela, M. A., Dugger, A., Maidment,
D. R., Gochis, D. J., David, C. H., Yu, W., Ding, D., Clark, E. P.,
and Noman, N.: Towards real-time continental scale streamﬂow
simulation in continuous and discrete space, J. Am. Water Re-
sour. Assoc., 54, 7–27, 2018.

Sanyal, J. and Lu, X. X.: Application of remote sensing in ﬂood
management with special reference to monsoon Asia: a review,
Nat. Hazards, 33, 283–301, 2004.

Savage, J. T. S., Bates, P., Freer, J., Neal, J., and Aronica, G.: When
does spatial resolution become spurious in probabilistic ﬂood in-
undation predictions?, Hydrol. Process., 30, 2014–2032, 2016.
Schaefer, J. T.: The critical success index as an indicator of warning

skill, Weather Forecast., 5, 570–575, 1990.

Schumann, G.-P., Neal, J. C., Voisin, N., Andreadis, K. M., Pappen-
berger, F., Phanthuwongpakdee, N., Hall, A. C., and Bates, P. D.:
A ﬁrst large-scale ﬂood inundation forecasting model, Water Re-
sour. Res., 49, 6248–6257, 2013.

Scott, D. W.: Multivariate density estimation: theory, practice, and
visualization, John Wiley & Sons, ISBN 9780471697558, 2015.
Shastry, A., Egbert, R., Aristizabal, F., Luo, C., Yu, C.-W., and
Praskievicz, S.: Using Steady-State Backwater Analysis to Pre-
dict Inundated Area from National Water Model Streamﬂow
Simulations, J. Am. Water Resour. Assoc., 55, 940–951, 2019.
Shin, S., Pokhrel, Y., and Miguez-Macho, G.: High-resolution mod-
eling of reservoir release and storage dynamics at the continental
scale, Water Resour. Res., 55, 787–810, 2019.

Silverman, B. W.: Density estimation for statistics and data analysis,

Routledge, https://doi.org/10.1201/9781315140919, 2018.

Smiley, K. T., Noy, I., Wehner, M. F., Frame, D., Sampson, C. C.,
and Wing, O. E.: Social inequalities in climate change-attributed
impacts of Hurricane Harvey, Nat. Commun., 13, 1–10, 2022.
Smith, M., Patrick, N., Frazier, N., Kim, J., Flowers, T., and Og-
den, F.: Hyper Resolution Modeling of Urban Flood Inundation,
NOAA National Weather Service, https://doi.org/10.25923/9t55-
tn77, 2020.

Smith, M., Patrick, N., Frazier, N., and Kim,

J.: Valida-
tion of Urban Flood Inundation Models Applied Using Na-
tionally Available Data Sets: Novel Analyses of Observed
Information, J. Hydrol. Eng., 26, 04021039,
High Water
https://doi.org/10.1061/(ASCE)HE.1943-5584.0002129, 2021.
Smith, T., Rheinwalt, A., and Bookhagen, B.: Determining
the optimal grid resolution for topographic analysis on an
airborne lidar dataset, Earth Surf. Dynam., 7, 475–489,
https://doi.org/10.5194/esurf-7-475-2019, 2019.

Snyder, G. I., Sugarbaker, L., Jason, A. L., and Maune, D. F.: Na-
tional requirements for enhanced elevation data, US Department

https://doi.org/10.5194/hess-28-1287-2024

Hydrol. Earth Syst. Sci., 28, 1287–1315, 2024

1314

F. Aristizabal et al.: Effects of high-quality elevation data and other variables on FIM skill

of the Interior, open-File Report 2013-1237, US Geological Sur-
vey, https://doi.org/10.3133/ofr20131237, 2013.

Speckhann, G. A., Borges Chaffe, P. L., Fabris Goerl, R., Abreu,
J. J. d., and Altamirano Flores, J. A.: Flood hazard mapping in
Southern Brazil: a combination of ﬂow frequency analysis and
the HAND model, Hydrolog. Sci. J., 63, 87–100, 2018.

Stallings, R. A.: Conﬂict in natural disasters: A codiﬁcation of con-
sensus and conﬂict theories, Social Sci. Quart., 69, 569, 1988.
Stoker, J. and Miller, B.: The Accuracy and Consistency of 3D Ele-
vation Program Data: A Systematic Analysis, Remote Sens., 14,
940, https://doi.org/10.3390/rs14040940, 2022.

Stoker, J. M., Brock, J. C., Soulard, C. E., Ries, K. G., Sugarbaker,
L., Newton, W. E., Haggerty, P. K., Lee, K. E., and Young, J. A.:
USGS lidar science strategy: mapping the technology to the sci-
ence, vol. 10, US Department of the Interior, US Geological Sur-
vey, https://doi.org/10.3133/ofr20151209, 2015.

Strategic Alliance for Risk Reduction II: Base Level Engi-
neering Analysis: Region 6 Neches River Watershed –
Lower Angelina (HUC8 – 12020005), MIP Deliverable
16-09-0654S, Strategic Alliance for Risk Reduction II (STAR-
RII),
fEMA IDIQ Contract: HSFE60-15-D-0005, FEMA,
https://ebfedata.s3.amazonaws.com/12020005_LowerAngelina/
12020005_Documents.zip (last access: February 2021), 2019a.
Strategic Alliance for Risk Reduction II: Base Level Engi-
neering Analysis: Region 6 Neches River Watershed –
Lower Neches (HUC8 – 12020003), MIP Deliverable 16-
09-0654S, Strategic Alliance for Risk Reduction II (STAR-
RII),
fEMA IDIQ Contract: HSFE60-15-D-0005, FEMA,
https://ebfedata.s3.amazonaws.com/12020003_LowerNeches/
12020003_Documents.zip (last access: February 2021), 2019b.
Strategic Alliance for Risk Reduction II: Base Level Engi-
neering Analysis: Region 6 Neches River Watershed –
Middle Neches (HUC8 – 12020002), MIP Deliverable 16-
09-0654S, Strategic Alliance for Risk Reduction II (STAR-
RII),
fEMA IDIQ Contract: HSFE60-15-D-0005, FEMA,
https://ebfedata.s3.amazonaws.com/12020002_MiddleNeches/
12020002_Documents.zip (last access: February 2021), 2019c.
Strategic Alliance for Risk Reduction II: Base Level Engi-
neering Analysis: Region 6 Neches River Watershed –
Pine Island Bayou (HUC8 – 12020007), MIP Deliver-
able 16-09-0654S, Strategic Alliance
for Risk Reduc-
tion II
fEMA IDIQ Contract: HSFE60-15-D-
0005, FEMA, https://ebfedata.s3.amazonaws.com/12020007_
PineIslandBayou/12020007_Documents.zip (last access: Febru-
ary 2021), 2019d.

(STARRII),

Strategic Alliance for Risk Reduction II: Base Level Engi-
neering Analysis: Region 6 Neches River Watershed –
Upper Angelina (HUC8 – 12020004), MIP Deliverable
16-09-0654S, Strategic Alliance for Risk Reduction II (STAR-
RII),
fEMA IDIQ Contract: HSFE60-15-D-0005, FEMA,
https://ebfedata.s3.amazonaws.com/12020004_UpperAngelina/
12020004_Documents.zip (last access: February 2021), 2019e.
Strategic Alliance for Risk Reduction II: Base Level Engi-
neering Analysis: Region 6 Neches River Watershed –
Upper Neches (HUC8 – 12020001), MIP Deliverable 16-
09-0654S, Strategic Alliance for Risk Reduction II (STAR-
fEMA IDIQ Contract: HSFE60-15-D-0005, FEMA,
RII),
https://ebfedata.s3.amazonaws.com/12020001_UpperNeches/
12020001_Documents.zip (last access: February 2021), 2019f.

Strategic Alliance for Risk Reduction II: Base Level Engineering
Analysis: Region 6 Neches River Watershed – Village (HUC8
– 12020006), MIP Deliverable 16-09-0654S, Strategic Alliance
for Risk Reduction II
fEMA IDIQ Contract:
(STARRII),
HSFE60-15-D-0005, FEMA, https://ebfedata.s3.amazonaws.
com/12020006_Village/12020006_Documents.zip (last access:
February 2021) 2019g.

Strömberg, D.: Natural disasters, economic development, and hu-

manitarian aid, J. Econ. Perspect., 21, 199–222, 2007.

Sugarbaker, L., Constance, E. W., Heidemann, H. K., Jason, A. L.,
Lucas, V., Saghy, D., and Stoker, J. M.: The 3D Elevation Pro-
gram initiative: a call for action, US Geological Survey Reston,
VA, USA, https://doi.org/10.3133/cir1399, 2014.

Tabari, H.: Climate change impact on ﬂood and extreme precip-
itation increases with water availability, Sci. Rep., 10, 13768,
https://doi.org/10.1038/s41598-020-70816-2, 2020.

Tauhid, F. A. and Zawani, H.: Mitigating climate change related
ﬂoods in urban poor areas: green infrastructure approach, J. Reg.
City Plan., 29, 98–112, 2018.

Tellman, B., Schank, C., Schwarz, B., Howe, P. D., and
de Sherbinin, A.: Using disaster outcomes to validate com-
ponents of social vulnerability to ﬂoods: Flood deaths and
property damage across the USA, Sustainability, 12, 6006,
https://doi.org/10.3390/su12156006, 2020.

Tellman, B., Sullivan, J., Kuhn, C., Kettner, A., Doyle, C., Braken-
ridge, G., Erickson, T., and Slayback, D.: Satellite imaging re-
veals increased proportion of population exposed to ﬂoods, Na-
ture, 596, 80–86, 2021.

Teng, J., Vaze, J., Dutta, D., and Marvanek, S.: Rapid inundation
modelling in large ﬂoodplains using LiDAR DEM, Water Re-
sour. Manage., 29, 2619–2636, 2015.

Teng, J., Jakeman, A. J., Vaze, J., Croke, B. F., Dutta, D., and Kim,
S.: Flood inundation modelling: A review of methods, recent
advances and uncertainty analysis, Environ. Model. Softw., 90,
201–216, 2017.

Thomas Steven Savage, J., Pianosi, F., Bates, P., Freer, J., and Wa-
gener, T.: Quantifying the importance of spatial resolution and
other factors through global sensitivity analysis of a ﬂood inun-
dation model, Water Resour. Res., 52, 9146–9163, 2016.
Tumbare, M. J.: Mitigating Floods in Southern Africa,

in:
First WAFSA/WATERNET Symposium, 1–2 November 1-
2, 2000, Maputo, https://api.semanticscholar.org/CorpusID:
129970052 (last access: March 2024), 2000.

Turlach, B. A., Heidenreich, N. B., Schindler, A., and Sper-
lich, S.: Bandwidth selection in kernel density estimation:
a review, Tech. rep., Humboldt Universitaet Berlin, Berlin,
https://doi.org/10.1007/s10182-013-0216-y, 1993.

Twele, A., Cao, W., Plank, S., and Martinis, S.: Sentinel-1-based
ﬂood mapping: a fully automated processing chain, Int. J. Re-
mote Sens., 37, 2990–3004, 2016.

UNEP: Early warning systems: a state of the art analysis and
future directions, https://wedocs.unep.org/20.500.11822/32230
(last access: 10 June 2022), 2012.

UNISDR: Making development sustainable: the future of disas-
ter risk management, https://api.semanticscholar.org/CorpusID:
112818444 (last access: 10 July 2022), 2015.

United States Army Corps of Engineers: National Inventory
of Dams, https://nid.sec.usace.army.mil/ (last access: 13 Au-
gust 2022), 2023.

Hydrol. Earth Syst. Sci., 28, 1287–1315, 2024

https://doi.org/10.5194/hess-28-1287-2024

F. Aristizabal et al.: Effects of high-quality elevation data and other variables on FIM skill

1315

United

States Geological

Dataset,
watershed-boundary-dataset
2023.

Survey: Watershed Boundary
https://www.usgs.gov/national-hydrography/
(last access: 1 October 2020),

US Army Corps of Engineers: National Levee Database, National
Levee Database, https://levees.sec.usace.army.mil/ (last access:
July 2020), 2021.

USGS: NHDPlusHR DEM, https://prd-tnm.s3.amazonaws.com/
index.html?preﬁx=StagedProducts/Hydrography/NHDPlusHR/
Beta/GDB/ (last access: 21 January 2020), 2021a.

USGS: 3D Elevation Program: FY21 Status of 3DEP Quality
Data, https://www.usgs.gov/3d-elevation-program (last access:
28 September 2022), 2021b.

USGS: 3D Elevation Program: FY22 Partnerships, https://
www.usgs.gov/3d-elevation-program (last access: 28 Septem-
ber 2022), 2022a.

USGS:

3DEPElevation

(ImageServer),

https://elevation.

nationalmap.gov/arcgis/rest/services/3DEPElevation/
ImageServer (last access: April 2022), 2022b.

Verdin, J., Verdin, K., Mathis, M. L., Magadzire, T., Kabuchanga,
E., Woodbury, M., and Gadain, H.: A software tool for rapid
ﬂood inundation mapping, Tech. rep., US Geological Survey,
https://doi.org/10.3133/ofr20161038, 2016.

Virtanen, P., Gommers, R., Oliphant, T. E., Haberland, M., Reddy,
T., Cournapeau, D., Burovski, E., Peterson, P., Weckesser, W.,
Bright, J., van der Walt, S. J., Brett, M., Wilson, J., Millman,
K. J., Mayorov, N., Nelson, A. R. J., Jones, E., Kern, R., Larson,
E., Carey, C. J., Polat, ˙I., Feng, Y., Moore, E. W., VanderPlas, J.,
Laxalde, D., Perktold, J., Cimrman, R., Henriksen, I., Quintero,
E. A., Harris, C. R., Archibald, A. M., Ribeiro, A. H., Pedregosa,
F., van Mulbregt, P., and SciPy 1.0 Contributors: SciPy 1.0: Fun-
damental Algorithms for Scientiﬁc Computing in Python, Nat.
Meth., 17, 261–272, https://doi.org/10.1038/s41592-019-0686-2,
2020.

Wang, Y. and Zheng, T.: Comparison of light detection and ranging
and national elevation dataset digital elevation model on ﬂood-
plains of North Carolina, Natl. Hazards Rev., 6, 34–40, 2005.
Timberlake,
acts

Wijkman,
ters:
https://doi.org/10.4324/9780429351969, 2021.

Natural
disas-
of man?, Routledge,

and
of God

acts

L.:

A.

or

Wing, O. E., Bates, P. D., Sampson, C. C., Smith, A. M., Johnson,
K. A., and Erickson, T. A.: Validation of a 30 m resolution ﬂood
hazard model of the conterminous United States, Water Resour.
Res., 53, 7968–7986, 2017.

Wing, O. E., Bates, P. D., Smith, A. M., Sampson, C. C.,
Johnson, K. A., Fargione, J., and Moreﬁeld, P.: Estimates of
present and future ﬂood risk in the conterminous United States,
Environ. Res. Lett., 13, 034023, https://doi.org/10.1088/1748-
9326/aaac65, 2018.

Witt III, E. C.: Evaluation of the US Geological Survey standard
elevation products in a two-dimensional hydraulic modeling ap-
plication for a low relief coastal ﬂoodplain, J. Hydrol., 531, 759–
767, 2015.

Xu, J., Wang, Z., Shen, F., Ouyang, C., and Tu, Y.: Natural disasters
and social conﬂict: A systematic literature review, Int. J. Disast.
Risk Reduct., 17, 38–48, 2016.

Yang, L., Jin, S., Danielson, P., Homer, C., Gass, L., Bender, S. M.,
Case, A., Costello, C., Dewitz, J., Fry, J., Funk, M., Granneman,
B., Liknes, G. C., Rigge, M., and Xian, G.: A new generation of
the United States National Land Cover Database: Requirements,
research priorities, design, and implementation strategies, ISPRS
J. Photogram. Remote Sens., 146, 108–123, 2018.

Zahran, S., Shelley, T. O., Peek, L., and Brody, S. D.: Natural dis-
asters and social order: Modeling crime outcomes in Florida, Int.
J. Mass Emerg. Disast., 27, 26–52, 2009.

Zhang, J., Huang, Y.-F., Munasinghe, D., Fang, Z., Tsang, Y.-P.,
and Cohen, S.: Comparative analysis of inundation mapping ap-
proaches for the 2016 ﬂood in the Brazos River, Texas, J. Am.
Water Resour. Assoc., 54, 820–833, 2018.

Zheng, X., Maidment, D. R., Tarboton, D. G., Liu, Y. Y., and Pas-
salacqua, P.: GeoFlood: Large-Scale Flood Inundation Mapping
Based on High-Resolution Terrain Analysis, Water Resour. Res.,
54, 10013–10033, 2018a.

Zheng, X., Tarboton, D. G., Maidment, D. R., Liu, Y. Y., and Pas-
salacqua, P.: River channel geometry and rating curve estimation
using height above the nearest drainage, J. Am. Water Resour.
Assoc., 54, 785–806, 2018b.

Zheng, X., Godbout, L., Zheng, J., McCormick, C., and Passalac-
qua, P.: An automatic and objective approach to hydro-ﬂatten
high resolution topographic data, Environ. Model. Softw., 116,
72–86, 2019.

Zheng, X., D’Angelo, C., Maidment, D. R., and Passalacqua,
P.: Application of a Large-Scale Terrain-Analysis-Based Flood
Mapping System to Hurricane Harvey, J. Am. Water Resour. As-
soc., 58, 149–163, 2022.

https://doi.org/10.5194/hess-28-1287-2024

Hydrol. Earth Syst. Sci., 28, 1287–1315, 2024

