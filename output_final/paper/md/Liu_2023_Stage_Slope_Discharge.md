RESEARCH LETTER
10.1029/2023GL106394

Key Points:

• The classic stage-discharge rating curve concept fails upstream of river confluences because of backwater effects
• Hydraulic modeling confirms that unique stage-slope-discharge relationships exist upstream of river confluences
• New satellite altimetry observations of river stage and slope reveal stage-slope-discharge relationships for selected river confluences

Correspondence to:

P. Bauer-Gottwein,
pbau@dtu.dk

Citation:

Liu, J., Bauer-Gottwein, P., Frias, M.
C., Musaeus, A. F., Christoffersen,
L., & Jiang, L. (2023). Stage-slope-
discharge relationships upstream of
river confluences revealed by satellite
altimetry. Geophysical Research Letters,
50, e2023GL106394. https://doi.
org/10.1029/2023GL106394

Received 15 SEP 2023
Accepted 8 NOV 2023

© 2023. The Authors.
This is an open access article under
the terms of the Creative Commons
Attribution License, which permits use,
distribution and reproduction in any
medium, provided the original work is
properly cited.

LIU ET AL.

# Stage-Slope-Discharge Relationships Upstream of River Confluences Revealed by Satellite Altimetry

Jun Liu1, Peter Bauer-Gottwein1, Monica Coppo Frias1, Aske Folkmann Musaeus1, Linda Christoffersen2, and Liguang Jiang3

1Department of Environmental and Resource Engineering, Technical University of Denmark, Kgs. Lyngby, Denmark,
2National Space Institute, Technical University of Denmark, Kgs. Lyngby, Denmark, 3School of Environmental Science and
Engineering, Southern University of Science and Technology, Shenzhen, China

## Abstract

With increasing coverage, density, and accuracy of the global inland water altimetry record,
remote sensing observations of water surface elevation (WSE) and water surface slope (WSS) are becoming
available for the world's rivers. In steady, uniform flows, WSS is invariable, while there is a unique one-to-one
relationship between WSE and discharge, the rating curve. While the assumptions of steady uniform flow are
appropriate for many rivers, they are violated upstream of river confluences. We present a simple analytical
hydraulic model of river confluences using the theory of steady, gradually varied flow. We apply the model
to four river confluences in the Mississippi-Missouri river system. We determine the spatial extent of the
backwater-affected zones and map WSE-discharge and WSS-discharge relationships. We show that coincident
measurements of WSE and WSS from new satellite altimetry missions effectively constrain discharge estimates
from space in the backwater-affected zones upstream of river confluences.

## Plain Language Summary

New satellite altimetry missions monitor water levels in global rivers
at unprecedented spatio-temporal resolution and accuracy. One principal objective of this monitoring effort
is to map river flow in space and time, understand the impacts of climatic change on river flows, and provide
river flow estimates for practical water resources applications. In many locations and situations, there is a
one-to-one relationship between river flow and river water level. This so-called rating curve can be used to
directly translate water level observations into river flow estimates. However, the concept of the rating curve
breaks down whenever the flow in the river is significantly different from steady uniform flow, which is the
flow occurring in a long and uniform river reach with constant boundary inflow. Upstream of river confluences,
conditions are often non-uniform, because high flow in one tributary can coincide with low flow in the other,
leading to significant backwater effects in both tributaries. This study models water level and water surface
slope dynamics upstream of river junctions and highlights the value that data sets from new satellite missions
provide for understanding the hydraulics around river confluences and for estimating flow upstream of river
confluences from space.

## 1. Introduction

Water resources management, flood risk assessment, and flood forecasting have been hindered by the scarcity of easily accessible, spatio-temporally resolved observations for crucial hydrometric parameters, including water surface elevation (WSE) and river discharge. This deficiency is particularly pronounced in the remote and poorly instrumented river basins of the world, and in basins, where observational data sets are not being shared because of political and national security reasons. At the same time, the availability and quality of remote sensing observations of inland surface water elevation have been increasing over the past decades (see recent review by Abdalla et al., 2021), and high-level pre-processed WSE data products are now operationally provided for thousands of virtual stations (VS) around the world by databases such as Dahiti (Schwatke et al., 2015) and Hydroweb (Santos da Silva et al., 2010). Using the latest generation of satellite altimetry missions, we can, for the first time, observe local water surface slope (WSS) along with WSE. This has been demonstrated for the ICESat-2 mission (Christoffersen et al., 2023; Scherer et al., 2022), and similar capabilities are also expected for the recently launched Surface Water and Ocean Topography (SWOT) mission (Biancamaria et al., 2016). WSE is an important parameter for hydrological applications, particularly in the flooding context. However, for water balance studies and water resources management, river discharge estimates are often required. For this reason, significant research efforts have been dedicated to the development of methods to estimate discharge from time series of WSE at VS (e.g., Bjerklie et al., 2018; Getirana & Peters-Lidard, 2013; Michailovsky et al., 2012; Nielsen et al., 2022; Paris et al., 2016; Tarpanelli et al., 2014; Tourian et al., 2017; Zakharova et al., 2006).

Most published studies use some form of stage-discharge rating curves to convert stage to discharge, that is, a one-to-one relationship between WSE and discharge is established, either using regression techniques with observed in-situ discharge data sets or site-scale hydraulic models. However, rating curves are only valid for sites with constant energy slope (World Meteorological Organization (WMO), 2010). When the energy slope varies over time, for example, due to variable backwater effects, relationships between WSE and discharge become more complex, and the WSE does not uniquely determine the discharge. Utilizing WSE-discharge rating curves to estimate discharge from water level in river sections with variable backwater effects, can cause large uncertainties. For instance, Meade et al. (1991) found that backwater from major tributaries downstream caused a varying stage spanning 2–3 m in the Amazon River at a given discharge; Hidayat et al. (2011) used WSE-discharge rating curves to estimate discharge in River Mahakam, and the estimated discharge spanned more than 2,000 m³/s for a specific stage (the maximum discharge is 3,250 m³/s).

Stage-slope-discharge or WSE-WSS-discharge rating curves are one way of handling variable backwater effects in discharge estimation. WSS is approximately equal to the energy slope, if local and convective acceleration terms are small, that is, the diffusive wave approximation of the De Saint Venant equations is applicable. The slope can be determined using stage records from a base gauge and an auxiliary reference gauge at some distance from the base gauge, which is known as the twin-gauge approach (Herschy, 2008; Kennedy, 1984; Rantz, 1982), and further developed in more recent publications by Mansanarez et al., 2016; Petersen-Øverleir & Reitan, 2009. Traditional, nadir-looking radar altimetry missions (e.g., Jason-1/2/3, Sentinel-3 A/B) cannot provide WSS observations, due to the narrow swath widths and wide spacing of ground tracks, and because overpasses at neighboring VS occur at different times. Some studies attempted to densify the spatio-temporal resolution of WSE measurements using multiple satellite missions to produce slope estimates. Paris et al. (2016) estimated a monthly average slope from the interpolated WSE series for one specific VS located at the mouth of the Negro River, showing that a WSE-WSS-discharge rating curve outperformed a WSE-discharge rating curve for discharge estimation. Accurate observation of WSS for a broad range of river reaches has only recently become possible due to the availability of ICESat-2 data sets (Christoffersen et al., 2023; Scherer et al., 2022). In the near future, WSS observations from the recently launched SWOT mission will also become available.

Figure 1 illustrates the conceptual framework of this study. We investigate four major river confluences (Missouri/Yellowstone, Missouri/Platte, Mississippi/Missouri and Mississippi/Ohio rivers), where we expect significant upstream backwater effects as illustrated in Figure 1b. In the backwater-affected reaches of the rivers, we expect non-unique relationships between WSE and discharge as well as WSS and discharge, as illustrated in Figures 1c and 1d. The objectives of this study are to (a) investigate the relationship between WSE, WSS, and discharge upstream of river confluences using simple hydraulic modeling concepts; (b) to demonstrate the applicability of WSE-WSS-discharge rating curves upstream of river confluences; and (c) showcase the value of WSE and WSS observations from ICESat-2 and conventional satellite altimetry missions to understand the relationships between WSE, WSS and discharge around river confluences.

## 2. Modeling WSE-WSS-Discharge Relationships Upstream of River Confluences

We model the hydraulics around river confluences using the concept of steady gradually varied flow as presented in Chow (1959), Chapters 9 and 10. We assume that downstream of the confluence, the flow is uniform, that is, that depth is equal to normal depth for the sum of both tributary flows. Normal depth in the downstream reach is then taken as the boundary condition for backwater calculations in both tributary rivers. The starting point for model development is the differential equation for the flow depth, y, in the tributaries, which varies as a function of the chainage:

    dy/dx = (S0 − Sf) / (1 − Fr²)                                      (1)

In this equation, x is the river chainage (m), assumed to be zero at the confluence and positive in the downstream direction, S0 is the bed slope (m/m), Sf is the friction slope (m/m), and Fr is Froude's number (dimensionless). Given the boundary condition at the confluence, that is, uniform depth downstream, this differential equation can be solved to provide the depth profile in the backwater zones of both tributaries. These depth profiles will asymptotically approach normal flow depth in both tributaries in the upstream direction. Please note that, once the depth is known, WSE and WSS can be immediately calculated. WSE is the sum of depth and bottom elevation and WSS is equal to the difference between bed slope and dy/dx from Equation 1.

As shown in Chow (1959), using the Chézy formulation for the friction slope in a wide river, Equation 1 can be manipulated to yield

    yn (du/dx) = S0 (u³ − 1) / (u³ − yc³/yn³)                          (2)

Here, yn is the normal depth, defined as yn = (Q² b⁻² C⁻² S0⁻¹)^(1/3), u is the scaled dimensionless depth, u = y/yn, and yc is the critical depth, defined as yc = (Q² b⁻² g⁻¹)^(1/3). The symbol Q denotes river discharge (m³/s), b is the river width (m), C is the Chézy coefficient (assumed as 90 m^(1/2)/s throughout this paper), and g is the gravitational acceleration (=9.81 m/s²). Integrating Equation 2 yields the following implicit equation, linking the chainage to the scaled depth:

    x = (yn/S0) [ (u − [1 − C²S0/g] F(u)) − (ub − [1 − C²S0/g] F(ub)) ]  (3)

Here, ub is the scaled boundary depth, that is, the downstream normal depth divided by the normal depth in the tributary, and F(u) is a tabulated primitive:

    F(u) = (1/6) ln( (u² + u + 1) / (u − 1)² ) + (1/√3) arctan( (2u + 1)/√3 )   (4)

Because of the implicit format of Equation 3, normalized depth is first sampled over the interval between the boundary condition and 1 and chainages corresponding to normalized depth grid points are calculated using Equation 3. Subsequently, normalized depth for any requested chainage point is determined by linear interpolation. Once normalized depth is known, WSS can be immediately calculated using Equation 1.

Like Samuels (1989), we provide a simple analytical formula to estimate the length of the backwater-affected region upstream of river confluences. For downstream depth larger than normal depth in the tributary, we calculate the length of the chainage interval affected by backwater effects as

    xbw = (yn/S0) [ (1.01 − [1 − C²S0/g] F(1.01)) − (ub − [1 − C²S0/g] F(ub)) ]  (5)

assuming that backwater effects become negligible, once the difference between the flow depth and the normal depth is less than 1%. For downstream depth less than normal depth in the tributary, we replace 1.01 in Equation 5 with 0.99.

Chézy's equation for the friction slope reads Sf = Q² b⁻² C⁻² y⁻³. For steady uniform flow (i.e., kinematic wave approximation of the De Saint Venant equations, Sf = S0), Chézy's equation thus defines a rating curve of the format

    Q = b C S0^(1/2) · (WSE − z0)^(3/2)                                (6)

where z0 is the river bottom elevation (mamsl). For the diffusive wave approximation of the De Saint Venant equations, Sf = WSS, we can write a WSE-WSS-discharge rating curve as

    Q = b C · WSS^(1/2) · (WSE − z0)^(3/2)                             (7)

For details on the derivation of these equations please refer to hydraulics textbooks such as Chow (1959).

Application of this model to the investigated river confluences requires several input data sets. We extracted river width and bed slope estimates from the SWOT River Database (SWORD, Altenau et al., 2021), and river discharge time series from the United States Geological Survey (USGS) National Water Information System online archive (NWIS). If available, in-situ observations of WSE were also extracted from NWIS.

## 3. Satellite Altimetry Observations of WSE and WSS

Inland water satellite altimetry has produced an ever-expanding record of global WSE observations from multiple missions, including Earth Resources Satellite, Envisat, Jason, and Sentinel-3. Progress in inland water altimetry was recently summarized in Abdalla et al. (2021). WSE time series for thousands of VS are provided by several operational global databases. We extracted all available virtual station time series in the vicinity of the river confluences from the Hydroweb (Santos da Silva et al., 2010) and Dahiti (Schwatke et al., 2015) databases.

The ICESat-2 mission (Markus et al., 2017) is a multi-beam laser altimetry mission, which provides temporally sparse observations of WSE with high accuracy (10 cm or better) and high along-track spatial resolution (ca. 10 m). The laser pulses from the ICESat-2 Advanced Topographic Laser Altimeter System illuminate three left/right pairs of spots on the surface that, and, as ICESat-2 orbits Earth, trace out six ground tracks at the time. Left/right spots within each pair are approximately 90 m apart, and track pairs are approximately 3 km apart in the across-track direction. Under normal conditions, each spot can provide WSE at the cross-over point with the river. Thus, WSS can be calculated from the simultaneously monitored WSE along an approximately 6km-long river chainage interval (Christoffersen et al., 2023; Scherer et al., 2022). These studies estimated the standard error of ICESat-2 WSS as ca. 2 cm/km, depending on the orbit-river geometry, the width of the river, and other environmental factors. We used the ICE2WSS package by Christoffersen et al. (2023), to extract WSS observations in the vicinity of the river confluences. The recently launched SWOT satellite mission (Biancamaria et al., 2016) is expected to also provide WSS (and WSE) observations at high spatial and temporal resolution and the findings presented here are thus relevant for the interpretation of the upcoming SWOT data sets.

## 4. Results

We investigated four river confluences in the Mississippi-Missouri river system in North America (Figure 2). We chose this river system for illustration because long-term records of river discharge are publicly available from NWIS, and because this river system has many confluences where discharges from both tributaries are of the same order of magnitude. However, the phenomena illustrated here occur in many other river systems around the world, for instance the confluence of the Niger and Benue rivers near Lokoja in Nigeria, the confluence of the Amur and Zeya rivers near Blagoveshchensk in Russia, the confluence of the Ganges and Ghaghara rivers near Chapra in India, the confluence of the Ucayali and Marañón rivers near Iquitos in Peru, and the confluence of the Amazon and Negro rivers near Manaus in Brazil.

Figure 3 illustrates the significance of backwater effects occurring at the four confluences. The background contour plots give the maximum extent of backwater in kilometers upstream of the confluence for the main river. The maximum extent is calculated using Equation 5. All discharge combinations of the two tributaries observed in the historical record are plotted as black dots. Upstream of the Missouri-Yellowstone confluence, backwater effects can extend to ca. 50 km for extreme discharge combinations. Note that, due to the significantly lower bed slope of the downstream reach, backwater effects are observed for all discharge combinations at this confluence, while for all other confluences, backwater effects vanish for certain discharge combinations, for which normal depths in the upstream and downstream reaches are equal. The significance of backwater effects further depends on the degree of correlation between both tributary flows. At the Ohio-Mississippi confluence, the correlation between the two inflows is low. Thus, high flows in the Mississippi could coincide with low flows in the Ohio River and vice versa. Such asymmetric inflows lead to significant backwater effects upstream of the confluence.

Figure 4 illustrates simulated WSE-discharge and WSS-discharge relationships at selected in-situ and VS upstream of the river confluences. Clearly, WSE-discharge relationships are non-unique, different combinations of tributary discharges lead to the same WSE. The relationship between WSS and tributary discharges is non-unique too, but the direction of the WSS isolines is not aligned with the direction of WSE isolines. In contrast, a combined rating quantity according to Equation 7, WSS^(1/2)·(WSE − z0)^(3/2), shows almost vertical isolines, which indicates that there is a unique relationship between this quantity and discharge in the river. From these simulation results, we expect that simultaneous measurements of WSE and WSS in rivers upstream of confluences should enable robust discharge estimation in such places.

Observed relationships between WSE, WSS and discharge for selected in-situ and VS are illustrated in Figure 5. For the Missouri-Yellowstone confluence, in-situ WSS was calculated from the WSE difference between stations 06185650 and 06329640, divided by the length of the chainage interval between the two stations. For the VS, WSS observations are from ICESat-2 and were extracted using ICE2WSS. All slope observations for the corresponding SWORD reach were pooled to produce Figure 5, although, depending on the exact ICESat-2 track configuration, observations are representative of different chainage intervals of the reach. The temporal sampling pattern of ICESat-2 is sparse. Because, for VS, there are few ICESat-2 WSS observations that coincide in time with WSE observations, WSS and WSE observations were matched using two-dimensional interpolation of WSE in the discharge space to the pair of discharge values for which WSS observations are available.

Observed WSE-WSS-discharge relationships (Figure 5) are qualitatively similar to their simulated counterparts (Figure 4) for all confluences. The main patterns in the simulated WSS and WSE contour plots are visible in the data. Quantitatively, simulated and observed WSE and WSS are significantly different, which is expected, given the simplified hydraulic modeling approach, uncertainties in the SWORD database, uncertainties in the observed WSE and WSS data sets, and unmodelled natural phenomena occurring in the rivers at specific times, such as local ice and debris jams.

## 5. Discussion and Conclusions

Model-based and data driven analysis of WSE-WSS-discharge relationships upstream of river confluences in the Mississippi-Missouri river system highlight complex hydraulic phenomena and show that discharge in such locations cannot be estimated from WSE alone. Using WSS data sets from in-situ stations and ICESat-2, we show that WSS can be combined with WSE to obtain a unique rating relationship. This implies that river discharge can be estimated with high confidence upstream of river confluences, if both WSE and WSS observations are available. The recent ICESat-2 mission has enabled accurate, space-borne, local WSS observation in rivers for the first time, but sampling frequency is low. The recently launched SWOT mission is expected to complement and expand the global inland water WSS record significantly. Interpretation of new spatio-temporally distributed WSS data sets will have to take into account hydraulic phenomena that lead to changes of WSS in time at specific locations. Key locations in river systems, where such time changes are expected, are confluences of major rivers.

In this study, we used simplified hydraulic modeling concepts to efficiently screen different river confluences and get first insights into the importance of variable backwater effects at these locations. In order to get detailed and quantitatively accurate results, screening analysis must be followed by detailed hydraulic modeling studies, using observed river bathymetry data sets, local estimates of hydraulic roughness and detailed knowledge of local conditions. For instance, upstream of the Mississippi-Missouri confluence on the Mississippi River, between stations 05587498 and DH-16795, the river is bisected by the Melvin Price Locks and Dam. Water levels upstream of the dam are thus primarily controlled by dam operation and not backwater effects from the Mississippi-Missouri confluence. Another important limitation is the coarse temporal resolution of available ICESat-2 WSS estimates. Soon, WSS estimates from the SWOT mission will become available, which will have a much higher temporal resolution and greatly enhance our ability to observe variable backwater effects upstream of river confluences.

Notwithstanding these limitations, this study clearly illustrates the value of new WSE and WSS data sets from satellite earth observation for detailed and quantitative understanding of the relationships between WSE, WSS, and discharge, which are shaped by the hydraulic phenomena occurring at these locations. The findings are important for ongoing efforts to estimate river discharge from space, pursued by an interdisciplinary community of hydrologists and satellite geodesists.

## Data Availability Statement

The data sets used in this study are all publicly available. ICESat-2 ATL03 is from Neumann et al. (2023), ATL08 from Neuenschwander et al. (2023), and ATL13 from Jasinski et al. (2023). Virtual station WSE time series are from Hydroweb (Santos da Silva et al., 2010) and Dahiti (Schwatke et al., 2015). In-situ discharge and river stage data were downloaded from the USGS National Water Information System (U.S. Department of the Interior, U.S. Geological Survey, 2023).

Acknowledgments
This study was supported by Innovation Fund Denmark through the ChinaWaterSense project (File number: 8087-00002B), the National Key Research and Development Program of China project (2018TFE0106500), and the European Space Agency through the Hydrocoastal project. The first author expresses thanks to China Scholarship Council for supporting his study.

## References

Abdalla, S., Abdeh Kolahchi, A., Ablain, M., Adusumilli, S., Aich Bhowmick, S., Alou-Font, E., et al. (2021). Altimetry for the future: Building on 25 years of progress. Advances in Space Research, 68(2), 319–363. https://doi.org/10.1016/j.asr.2021.01.022

Altenau, E. H., Pavelsky, T. M., Durand, M. T., Yang, X., Frasson, R. P. D. M., & Bendezu, L. (2021). The surface water and ocean topography (SWOT) mission river database (SWORD): A global river network for satellite data products. Water Resources Research, 57(7). https://doi.org/10.1029/2021WR030054

Biancamaria, S., Lettenmaier, D. P., & Pavelsky, T. M. (2016). The SWOT mission and its capabilities for land hydrology. Surveys in Geophysics, 37(2), 307–337. https://doi.org/10.1007/s10712-015-9346-y

Bjerklie, D. M., Birkett, C. M., Jones, J. W., Carabajal, C., Rover, J. A., Fulton, J. W., & Garambois, P. A. (2018). Satellite remote sensing estimation of river discharge: Application to the Yukon River Alaska. Journal of Hydrology, 561, 1000–1018. https://doi.org/10.1016/J.JHYDROL.2018.04.005

Chow, V. T. (1959). Open-channel hydraulics. McGraw-Hill.

Christoffersen, L., Bauer-Gottwein, P., Sørensen, L. S., & Nielsen, K. (2023). ICE2WSS; an R package for estimating river water surface slopes from ICESat-2. Environmental Modelling & Software. 105789. https://doi.org/10.1016/J.ENVSOFT.2023.105789

Getirana, A. C. V., & Peters-Lidard, C. (2013). Estimating water discharge from large radar altimetry datasets. Hydrology and Earth System Sciences, 17(3), 923–933. https://doi.org/10.5194/hess-17-923-2013

Herschy, R. W. (2008). Streamflow measurement. CRC Press. https://doi.org/10.1201/9781482265880

Hidayat, H., Vermeulen, B., Sassi, M. G., & Hoitink, P. A. J. F. (2011). Discharge estimation in a backwater affected meandering river. Hydrology and Earth System Sciences, 15(8), 2717–2728. https://doi.org/10.5194/hess-15-2717-2011

Jasinski, M. F., Stoll, J. D., Hancock, D., Robbins, J., Nattala, J., Pavelsky, T. M., et al. ICESat-2 Science Team. (2023). ATLAS/ICESat-2 L3A along track inland surface water data, version 6. [Dataset]. Boulder, Colorado USA. NASA National Snow and Ice Data Center Distributed Active Archive Center. https://doi.org/10.5067/ATLAS/ATL13.006

Kennedy, E. J. (1984). Discharge ratings at gaging stations. https://doi.org/10.3133/twri03A10

Mansanarez, V., Le Coz, J., Renard, B., Lang, M., Pierrefeu, G., & Vauchel, P. (2016). Bayesian analysis of stage-fall-discharge rating curves and their uncertainties. Water Resources Research, 52(9), 7424–7443. https://doi.org/10.1002/2016WR018916

Markus, T., Neumann, T., Martino, A., Abdalati, W., Brunt, K., Csatho, B., et al. (2017). The ice, cloud, and land elevation satellite-2 (ICESat-2): Science requirements, concept, and implementation. Remote Sensing of Environment, 190, 260–273. https://doi.org/10.1016/j.rse.2016.12.029

Meade, R. H., Rayol, J. M., Da Conceicão, S. C., & Natividade, J. R. G. (1991). Backwater effects in the Amazon River basin of Brazil. Environmental Geology and Water Sciences, 18(2), 105–114. https://doi.org/10.1007/BF01704664

Michailovsky, C. I., McEnnis, S., Berry, P. a. M., Smith, R., & Bauer-Gottwein, P. (2012). River monitoring from satellite radar altimetry in the Zambezi River basin. Hydrology and Earth System Sciences, 16(7), 2181–2192. https://doi.org/10.5194/hess-16-2181-2012

Neuenschwander, A. L., Pitts, K. L., Jelley, B. P., Robbins, J., Markel, J., Popescu, S. C., et al. (2023). ATLAS/ICESat-2 L3A land and vegetation height, version 6. [Dataset]. Boulder, Colorado USA. NASA National Snow and Ice Data Center Distributed Active Archive Center. https://doi.org/10.5067/ATLAS/ATL08.006

Neumann, T. A., Brenner, A., Hancock, D., Robbins, J., Gibbons, A., Lee, J., et al. (2023). ATLAS/ICESat-2 L2A global geolocated photon data, version 6. [Dataset]. Boulder, Colorado USA. NASA National Snow and Ice Data Center Distributed Active Archive Center. https://doi.org/10.5067/ATLAS/ATL03.006

Nielsen, K., Zakharova, E., Tarpanelli, A., Andersen, O. B., & Benveniste, J. (2022). River levels from multi mission altimetry, a statistical approach. Remote Sensing of Environment, 270, 112876. https://doi.org/10.1016/j.rse.2021.112876

Paris, A., Dias de Paiva, R., Santos da Silva, J., Medeiros Moreira, D., Calmant, S., Garambois, P.-A., et al. (2016). Stage-discharge rating curves based on satellite altimetry and modeled discharge in the Amazon basin. Water Resources Research, 52(5), 3787–3814. https://doi.org/10.1002/2014WR016618

Petersen-Øverleir, A., & Reitan, T. (2009). Bayesian analysis of stage-fall-discharge models for gauging stations affected by variable backwater. Hydrological Processes, 23(21), 3057–3074. https://doi.org/10.1002/hyp.7417

Rantz, S. E. (1982). Measurement and computation of streamflow. https://doi.org/10.3133/wsp2175

Samuels, P. G. (1989). Backwater lengths in rivers. Proceedings - Institution of Civil Engineers. Part 2. Research and Theory, 87(4), 571–582. https://doi.org/10.1680/iicep.1989.3779

Santos da Silva, J., Calmant, S., Seyler, F., Rotunno Filho, O. C., Cochonneau, G., & Mansur, W. J. (2010). Water levels in the Amazon basin derived from the ERS 2 and ENVISAT radar altimetry missions. Remote Sensing of Environment, 114(10), 2160–2181. https://doi.org/10.1016/j.rse.2010.04.020

Scherer, D., Schwatke, C., Dettmering, D., & Seitz, F. (2022). ICESat-2 based river surface slope and its impact on water level time series from satellite altimetry. Water Resources Research, 58(11). https://doi.org/10.1029/2022WR032842

Schwatke, C., Dettmering, D., Bosch, W., & Seitz, F. (2015). DAHITI - An innovative approach for estimating water level time series over inland waters using multi-mission satellite altimetry. Hydrology and Earth System Sciences, 19(10), 4345–4364. https://doi.org/10.5194/hess-19-4345-2015

Tarpanelli, A., Brocca, L., Barbetta, S., Faruolo, M., Lacava, T., & Moramarco, T. (2014). Coupling MODIS and radar altimetry data for discharge estimation in poorly gauged river basins. IEEE Journal of Selected Topics in Applied Earth Observations and Remote Sensing, 8(1), 1–8. https://doi.org/10.1109/JSTARS.2014.2320582

Tourian, M. J., Schwatke, C., & Sneeuw, N. (2017). River discharge estimation at daily resolution from satellite altimetry over an entire river basin. Journal of Hydrology, 546, 230–247. https://doi.org/10.1016/j.jhydrol.2017.01.009

U.S. Department of the Interior, U.S. Geological Survey. (2023). USGS surface-water historical instantaneous data for the nation. Retrieved from https://waterdata.usgs.gov/nwis/uv?

World Meteorological Organization (WMO). (2010). Manual on stream gauging, volume II – Computation of discharge. WMO-No. 1044.

Zakharova, E. A., Kouraev, A. V., Cazenave, A., & Seyler, F. (2006). Amazon River discharge estimated from TOPEX/Poseidon altimetry | Estimation du débit de l'Amazone à partir de donnèes altimétriques du satellite Topex/Poséidon. Comptes Rendus Geoscience, 338(3), 188–196. https://doi.org/10.1016/j.crte.2005.10.003

LIU ET AL.

9 of 9
