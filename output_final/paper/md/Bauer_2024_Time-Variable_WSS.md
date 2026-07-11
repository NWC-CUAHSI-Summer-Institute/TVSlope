Article
Hydraulics of Time-Variable Water Surface Slope in Rivers
Observed by Satellite Altimetry

Peter Bauer-Gottwein 1,2,*
and Karina Nielsen 3

, Linda Christoffersen 3

, Aske Musaeus 1,4

, Monica Coppo Frías 1

1 Department of Environmental and Resource Engineering, Technical University of Denmark,

2800 Kongens Lyngby, Denmark

2 Department of Geosciences and Natural Resource Management, University of Copenhagen,

1958 Frederiksberg, Denmark

3 National Space Center, Technical University of Denmark, 2800 Kongens Lyngby, Denmark
4 DHI, 2970 Hørsholm, Denmark
* Correspondence: pbg@ign.ku.dk

Abstract: The ICESat-2 and SWOT satellite earth observation missions have provided highly accurate
water surface slope (WSS) observations in global rivers for the first time. While water surface slope is
expected to remain constant in time for approximately uniform flow conditions, we observe time
varying water surface slope in many river reaches around the globe in the ICESat-2 record. Here, we
investigate the causes of time variability of WSSs using simplified river hydraulic models based on
the theory of steady, gradually varied flow. We identify bed slope or cross section shape changes,
river confluences, flood waves, and backwater effects from lakes, reservoirs, or the ocean as the main
non-uniform hydraulic situations in natural rivers that cause time changes of WSSs. We illustrate
these phenomena at selected river sites around the world, using ICESat-2 data and river discharge
estimates. The analysis shows that WSS observations from space can provide new insights into river
hydraulics and can enable the estimation of river discharge from combined observations of water
surface elevation and WSSs at sites with complex hydraulic characteristics.

Keywords: river hydraulics; satellite altimetry; ICESat-2; water surface slope; river discharge

1. Introduction

Satellite radar and laser altimetry have developed into mature techniques to monitor
the Earth’s inland waters. A review paper by an international team of altimetry experts [1]
provides an overview of available missions, databases, and data processing approaches.
Many global rivers have been investigated using satellite altimetry datasets [2–5], and
satellite altimetry has been incorporated into operational hydrologic-hydraulic modelling
and forecasting workflows [6–9]. ICESat-2 [10] and SWOT [11] are unique among satellite
altimetry missions because they do not only provide river water surface elevation (WSE)
at the cross-over points between a river and the satellite ground track (so-called virtual
stations) but also provide observations of local water surface slopes (WSSs, i.e., the slope
of the water surface along the river [12,13]). The mapping of river WSS at the regional
to global scale reveals that the WSS is constant in time in many river reaches but varies
significantly over time in other river reaches. The main factor causing the time variability
of WSE and WSS in rivers is the river discharge, which varies according to the weather and
rainfall-runoff response in the contributing catchment and can change by a factor of 100 or
more in highly seasonal rivers. In uniform river reaches, increased river discharge leads
to increased WSE, while the WSS remains unchanged. This unique relationship between
the WSE and discharge forms the basis for many algorithms estimating river discharge
from satellite altimetry observations (e.g., [14–18]). However, in non-uniform hydraulic
conditions, the WSS changes significantly with river discharge and observed changes

Citation: Bauer-Gottwein, P.;

Christoffersen, L.; Musaeus, A.; Frías,

M.C.; Nielsen, K. Hydraulics of

Time-Variable Water Surface Slope in

Rivers Observed by Satellite

Altimetry. Remote Sens. 2024, 16, 4010.

https://doi.org/10.3390/rs16214010

Academic Editor: Konstantinos

X. Soulis

Received: 22 August 2024

Revised: 24 October 2024

Accepted: 27 October 2024

Published: 29 October 2024

Copyright: © 2024 by the authors.

Licensee MDPI, Basel, Switzerland.

This article is an open access article

distributed under the terms and

conditions of the Creative Commons

Attribution (CC BY) license (https://

creativecommons.org/licenses/by/

4.0/).

Remote Sens. 2024, 16, 4010. https://doi.org/10.3390/rs16214010

https://www.mdpi.com/journal/remotesensing

remote sensing  Remote Sens. 2024, 16, 4010

2 of 15

in the WSS provide new insights into the hydraulic phenomena occurring in such river
reaches. Here, we classify typical non-uniform flow situations in natural rivers, in which
time-variable river WSS occurs. We develop simplified hydraulic models for each of these
typical non-uniform flow situations using the classic theory of steady gradually varied
flow [19]. We select one river site for each of the typical non-uniform flow situations and
illustrate the inter-relations between river discharge, WSE, and WSS using river discharge
records from in-situ monitoring networks or reanalysis in combination with ICESat-2 WSE
and WSS datasets.

2. Methods and Data

We first classify typical non-uniform flow situations that occur in natural rivers. Subse-
quently, we explain how these situations can be modelled using the classic theory of steady
gradually varied one-dimensional flow outlined in the textbook by Ven Te Chow [19].
We then describe how ICESat-2 data were processed into river water surface elevation
and water surface slope and how river discharge was estimated. All data processing and
modelling workflows were implemented in Python version 3.12.

2.1. Typical Non-Uniform Flow Situations in Natural Rivers

Under the assumptions of steady, uniform flow, the water surface slope is equal to
bed slope and does not change with discharge. Thus, the WSS remains constant in time as
illustrated in Figure 1A. Steady uniform flow occurs in long river reaches with constant
discharge, uniform cross section shape, uniform hydraulic roughness, and uniform bed
slope. While steady uniform flow is a reasonable approximation in many situations, we
identified four common non-uniform flow situations in natural rivers that cause the WSS
to change with discharge and thus in time: (1) changes of bed slope, cross section shape,
and/or hydraulic roughness along the river—i.e., conveyance changes (Figure 1B). If
conveyance changes abruptly, we predict a characteristic backwater profile upstream of
the change. The shape of the dimensionless backwater profile is invariant under discharge
changes (see modelling section), while the dimensional water surface elevation and water
surface slope profiles change with discharge. This non-uniform flow situation commonly
occurs upstream of waterfalls or rapids (Figure 1B1)—i.e., upstream of river cross sections
with critical flow. (2) River confluences. As described in [20] and illustrated in Figure 1C,
low flow in one tributary can coincide with high flow in the other tributary and vice versa,
leading to significant WSS variability in the backwater affected zones upstream of the
confluence in both tributaries. (3) Flood waves traveling through a river reach. Traveling
waves cause high WSS during the passage of the wavefront and low WSS in front and in
the wake of the flood wave (Figure 1D). (4) Backwater effects from lakes, reservoirs, or
the ocean. Water level changes in the receiving water bodies propagate upstream into the
tributary river, causing WSS changes in the backwater-affected zone (Figure 1E). At sites
of type A, we expect time-constant WSS, while at sites of types B-E, we expect the WSS to
change with discharge and thus in time. We will now discuss how each of these typical
non-uniform flow situations can be modelled using the theory of steady gradually varied
one-dimensional flow.

Remote Sens. 2024, 16, 4010

3 of 15

Figure 1. Hydraulic phenomena causing time-variable water surface slope in rivers. Vertical dashed
lines delineate the zone of significant WSS change. (A) River reach with uniform flow. (B) Abrupt
conveyance change. (B1) Waterfalls or rapids. (C) Reaches upstream of river confluences. (D) Flood
waves traveling through the river reach. (E) Backwater effects upstream of lakes, reservoirs, or
the ocean.

2.2. Modeling River Water Surface Elevation and Slope Using Steady Gradually Varied
Flow Model

We modelled the water surface elevation and water surface slope in the typical non-
uniform flow situations shown in Figure 1 using the theory of steady gradually varied
one-dimensional flow as explained in detail in the classic hydraulics textbook by Chow [19]
(chapter 9). This modelling approach is highly simplified and does not capture the com-
plexities of natural river flow in detail. We thus expect qualitative agreement between
the derived models and the observations but do not expect the models to fit the ob-
servations. Despite these limitations and because of its highly simplified nature, this
modeling approach provides generic insights into the inter-relations of water surface eleva-
tion, water surface slope, and river discharge in the typical non-uniform flow situations
described above.

Remote Sens. 2024, 16, x FOR PEER REVIEW 3 of 15    Figure 1. Hydraulic phenomena causing time-variable water surface slope in rivers. Vertical dashed lines delineate the zone of signiﬁcant WSS change. (A) River reach with uniform ﬂow. (B) Abrupt conveyance change. (B1) Waterfalls or rapids. (C) Reaches upstream of river conﬂuences. (D) Flood waves traveling through the river reach. (E) Backwater eﬀects upstream of lakes, reservoirs, or the ocean. 2.2. Modeling River Water Surface Elevation and Slope Using Steady Gradually Varied Flow Model We modelled the water surface elevation and water surface slope in the typical non-uniform ﬂow situations shown in Figure 1 using the theory of steady gradually varied one-dimensional ﬂow as explained in detail in the classic hydraulics textbook by Chow [19] (chapter 9). This modelling approach is highly simpliﬁed and does not capture the complexities of natural river ﬂow in detail. We thus expect qualitative agreement between the derived models and the observations but do not expect the models to ﬁt the observa-tions. Despite these limitations and because of its highly simpliﬁed nature, this modeling approach provides generic insights into the inter-relations of water surface elevation, wa-ter surface slope, and river discharge in the typical non-uniform ﬂow situations described above. Remote Sens. 2024, 16, 4010

4 of 15

In this modelling framework, the water surface elevation upstream of an anomalous
region can be described using the steady-state version of the one-dimensional De Saint-
Venant equations for flow in open channels. The equation reads as

dy
dx

=

S0 − S f
1 − Fr2

(1)

where y is the water depth in the river, x is the chainage, S0 is the bed slope, Sf is the friction
slope, and Fr is Froude’s number—i.e., the ratio of the flow velocity and the velocity of
gravity waves in shallow water. Using Chézy’s parameterization of the friction slope for a
wide river with width b and friction coefficient C, i.e., S f = Q2b−2C−2y−3, and introducing
the normalized depth u = y/yn, we obtain (see Chow [19] (p. 222)),

yn

du
dx

= S0

u3 − 1

u3 − y3

c /y3
n

(2)

(cid:16)

(cid:17)1/3

Q2b−2C−2S−1
0

, and yc is the critical depth,

where yn is the normal depth, yn =
yc = (cid:0)Q2b−2g−1(cid:1)1/3
. Normal depth, or steady uniform flow depth, is the depth in a
long river reach with uniform discharge, cross section shape, bed slope, and hydraulic
roughness. The Chézy coefficient varies with river characteristics. A widely accepted
default value for large rivers is 90 m1/2/s. We use this default value throughout this
paper but acknowledge that the coefficient varies from site to site in reality and should be
determined using an inverse modeling approach for detailed site-scale hydraulic modeling.
For a given boundary condition ub at the anomalous region, the depth profile upstream of
the anomalous region can be calculated analytically as ([19] p. 254)

x =

yn
S0

(cid:20)(cid:18)

(cid:20)

1 −

u −

(cid:21)

C2S0
g

(cid:19)

(cid:18)

−

F(u)

ub −

(cid:20)

1 −

(cid:21)

C2S0
g

F(ub)

(cid:19)(cid:21)

(3)

with F(u) = 1

6 ln

(cid:18)

(cid:19)

u2+u+1
(u−1)2

+ 1√
3

arctan

(cid:16) 2u+1√

(cid:17)

3
point corresponding to any normalized depth u in the river. Note that once depth is
known, water surface elevation can be calculated as bottom elevation plus depth, and water
surface slope can be calculated as WSS = S0 − dy/dx, where dy/dx directly results from
Equation (1).

, enabling the calculation of the chainage

The different situations illustrated in Figure 1 can now be understood in terms of
different boundary conditions ub in the application of Equation (3). In all cases, we assume
that flow is at normal depth downstream of the anomalous region—i.e., for the simulation
of the water depth upstream of the anomalous region, depth at the boundary is equal to
normal depth in the downstream reach. Case A implies that friction slope and bed slope
remain equal across the entire domain, and thus water surface slope does not vary with
discharge or chainage and is always equal to the bed slope, independent of the discharge
in the river. Using Chézy’s equation for the friction slope, steady uniform flow results in a
rating relationship between depth and discharge given by the normal flow equation.

(cid:16)

(cid:16)

(cid:17)1/3

Q2b−2C−2S−1
0,d

In case B, the boundary condition ub becomes equal to the ratio between the normal
depths in the downstream and upstream portions of the river: ub = yn,d/yn,u. In the case of
= (S0,u/S0,d)1/3, where S0,u
the slope break, ub =
is the upstream bed slope and S0,d the downstream bed slope. In the case of a cross section
=
change (changing river width), we get ub =
(bu/bd)2/3. Importantly, the boundary condition ub in case B is independent of discharge,
which implies that the shape of the water level profile remains the same but is scaled with the
normal depth in the upstream reach, as evident from equation 3. In the special case B1, i.e.,
upstream of waterfalls and rapids, the flow goes through a critical section and the boundary

Q2b−2C−2S−1
0,u

d C−2S−1

u C−2S−1
0

Q2b−2

Q2b−2

(cid:17)1/3

(cid:17)1/3

(cid:17)1/3

/

/

(cid:16)

(cid:16)

0

Remote Sens. 2024, 16, 4010

5 of 15

condition becomes ub = yc/yn = (cid:0)Q2b−2g−1(cid:1)1/3
= (cid:0)C2S0/g(cid:1)1/3
,
which is again independent of discharge. The critical section is located at some distance (a
few tens of meters) upstream of the fall [21], but for reach-scale analysis, it can be assumed
that the critical section is at the location of the waterfall.

Q2b−2C−2S−1
0

/

(cid:16)

(cid:17)1/3

In case C, the boundary condition ub becomes equal to the ratio between the normal depth
downstream of the confluence and the normal depth upstream of the confluence: ub,i = yn,d/yn,i,
where i can take values of one or two and indicates the two upstream tributaries. This boundary
is no longer independent of discharge but depends on the relative magnitude of both tributary

discharges: ub,i = yn,d/yn,i =
confluence model is also presented in [20].

(Q1 + Q2)2bd

(cid:16)

−2Cd

−2S−1

0,d /(Qi

2bi

−2Ci

−2S−1
0,i

(cid:17)(cid:17)1/3

. The same

x = 1/S0·

(cid:104)(cid:16)

(cid:104)

y + ln

Case D is a dynamic phenomenon, and the water surface elevation and water surface
slope changes quickly in time as the flood wave sweeps through the river reach. An
analytical traveling wave model (called uniformly progressive flow in [19]) exists for the
case of a flood wave traveling through a long uniform river reach [19] (pp. 528–535). While
the assumption of a traveling wave may be a significant simplification in most cases, the
analytical model provides a useful estimate of the maximum water surface slope occurring
at the wave front. The traveling wave model reads as

dy
dx

= S0

(y − y1)(y − y2)(y − y3)
y3 − q2

0/g

(4)

0C−2S−1

Here, y1 is the depth far upstream of the wave front, y2 is the depth far downstream of
2 , and q0 = y1y2(v1 − v2)(y1 − y2)−1. Flow velocities
the wavefront, y3 = q2
upstream and downstream of the wave front can be calculated with Chézy’s formula as
vi = CS1/2
(y1 − y)α·(y − y2)β·(y − y3)γ(cid:105)(cid:17)

(y1 − y0)α·(y0 − y2)β·(y0 − y3)γ(cid:105)(cid:17)(cid:105)

. An implicit analytical solution for the depth exists:

0 y1/2

1 y−1

0 y−1

y0 + ln

−

(cid:16)

(cid:104)

(5)

i

Here, y0 = y1+y2

2

is the depth at chainage x = 0 (where chainage is defined in a coordinate
(y1 − y2)−1(y1 − y3)−1,

system that moves with the speed of the wave front), α = (y 3
β = (y 3
c − y3
2
0/g(cid:1)1/3
yc = (cid:0)q2
WSS by solving

3 − y3
c
. Moreover, we can find the maximum WSS and the depth at maximum

(y1 − y2)−1(y2 − y3)−1,

(y1 − y3)−1(y2 − y3)−1,

γ = (y 3

1 − y3
c

and

(cid:17)

(cid:17)

(cid:17)

(cid:32)

(cid:19)

(cid:18) dy
dx

d
dy

=

d
dy

S0

(y − y1)(y − y2)(y − y3)
y3 − q2

0/g

(cid:33)

= 0

(6)

which leads to a 4-th order equation in y with one real root in the range between y1 and
y2. The maximum WSS can then be calculated by plugging the selected root into equation
4 and adding the bed slope. This result is useful because it enables us to estimate the
maximum water surface slope occurring during the passage of a wave front as dependent
on the water level change across the front and river characteristics.

In case E, the boundary condition ub is entirely dependent on the water level in the
lake, reservoir, or ocean into which the river flows and does not only depend on river
discharge. Depending on the water level in the receiving water body, the backwater profile
will propagate upstream to a larger or lesser extent, which will lead to significant water
surface slope changes in the backwater-affected zone of the river.

2.3. Processing of ATL03 Water Surface Elevation Data

In this section, we explain how the water surface elevation and water surface slope
were derived from the ICESat-2 data products. We derived water surface elevation and wa-
ter surface slope estimates from the ICESat-2 ATL03 product, version 6 [22,23]. Coppo Frías

Remote Sens. 2024, 16, 4010

6 of 15

et al. [24] describe the processing of ICESat-2 data for river modelling in detail. ICESat-2
ATL03 version 6 data were downloaded, re-projected to the local UTM coordinate system,
re-referenced to the EGM08 global geoid model [25], and assigned to the river-following
one-dimensional coordinate (chainage). Individual photon return coordinates were also
projected to the cross section coordinates perpendicular to the river. River overflights
(Figure 2A) were cleaned, and only high quality and high confidence photon events were
retained. Subsequently, overflight photons were classified in a histogram with 30 bins
per meter, and the bin with the highest photon count was identified (Figure 2B). The
water surface elevation was then estimated as the average of all photon events falling
between the highest photon count plus/minus 0.3 m. The water surface slope was calcu-
lated as the ratio of differences in water surface elevation at the cross-over points of the
six individual ICESat-2 ground tracks and corresponding differences in river chainage at
the cross-over points.

Figure 2. Processing of ATL03 river crossings. Example river crossing of the Peace River near
Vermillion Falls on 3 June 2019 (ATL03 file name: ATL03_20190306160236_10420202_006_02_gt1l).
(A): ATL03 elevation points along the cross section.
(B): Histogram of ATL03 heights along
cross section.

2.4. River Discharge Estimates

River discharge varies strongly in time for most rivers and is the dominant force
changing the WSE and WSS in rivers. We need river discharge estimates to analyze the inter-
relations of river discharge, WSE, and WSS. Ideally, this analysis should be conducted using
in-situ observations of river discharge only because the accuracy of in-situ observations
is higher than that of estimates derived from models and reanalysis systems. However,
in-situ, station-based river discharge estimates are scarce, and data are not publicly shared
in many countries. In this study, in-situ river discharge observations for the days of ICESat-
2 overpasses were extracted from the Global Runoff Data Center (GRDC) global runoff
database [26] for the sites for which observations were available in the GRDC archive.
For sites without available GRDC records, we extracted discharge reanalysis data from
the River Discharge and Related Forecasted Data archive produced by the Global Flood
Awareness System (GLOFAS) and archived on the Copernicus Data Store [27,28]. These
reanalysis estimates are based on the GLOFAS global runoff model and are informed with
historical in-situ observations. The uncertainty of GLOFAS reanalysis discharge is expected
to be significantly higher than the uncertainty of GRDC in-situ river discharge, but we
cannot quantify uncertainty for individual river sites and observation times. To extract
GLOFAS time series, daily gridded discharge estimates were downloaded from the archive
and pixel values for the river sites of interest were extracted and compiled into time series.

Remote Sens. 2024, 16, x FOR PEER REVIEW 6 of 15   water surface elevation was then estimated as the average of all photon events falling be-tween the highest photon count plus/minus 0.3 m. The water surface slope was calculated as the ratio of diﬀerences in water surface elevation at the cross-over points of the six in-dividual ICESat-2 ground tracks and corresponding diﬀerences in river chainage at the cross-over points.  Figure 2. Processing of ATL03 river crossings. Example river crossing of the Peace River near Ver-million Falls on 3 June 2019 (ATL03 ﬁle name: ATL03_20190306160236_10420202_006_02_gt1l). (A): ATL03 elevation points along the cross section. (B): Histogram of ATL03 heights along cross section. 2.4. River Discharge Estimates River discharge varies strongly in time for most rivers and is the dominant force changing the WSE and WSS in rivers. We need river discharge estimates to analyze the inter-relations of river discharge, WSE, and WSS. Ideally, this analysis should be con-ducted using in-situ observations of river discharge only because the accuracy of in-situ observations is higher than that of estimates derived from models and reanalysis systems. However, in-situ, station-based river discharge estimates are scarce, and data are not pub-licly shared in many countries. In this study, in-situ river discharge observations for the days of ICESat-2 overpasses were extracted from the Global Runoﬀ Data Center (GRDC) global runoﬀ database [26] for the sites for which observations were available in the GRDC archive. For sites without available GRDC records, we extracted discharge reanalysis data from the River Discharge and Related Forecasted Data archive produced by the Global Flood Awareness System (GLOFAS) and archived on the Copernicus Data Store [27,28]. These reanalysis estimates are based on the GLOFAS global runoﬀ model and are in-formed with historical in-situ observations. The uncertainty of GLOFAS reanalysis dis-charge is expected to be signiﬁcantly higher than the uncertainty of GRDC in-situ river discharge, but we cannot quantify uncertainty for individual river sites and observation times. To extract GLOFAS time series, daily gridded discharge estimates were down-loaded from the archive and pixel values for the river sites of interest were extracted and compiled into time series. 3. Results Sites corresponding to the typical non-uniform ﬂow situations shown in Figure 1 were identiﬁed on global rivers based on the literature, inspection of satellite imagery, and inspection of ICESat-2 ATL03 datasets from the sites. Sites of type A can typically be found at or close to established in-situ gauging stations because such stations require a simple and stable rating curve. We chose the Pfelling gauging station on the Danube River in Germany as an example of sites of type A. Remote Sens. 2024, 16, 4010

7 of 15

3. Results

Sites corresponding to the typical non-uniform flow situations shown in Figure 1
were identified on global rivers based on the literature, inspection of satellite imagery, and
inspection of ICESat-2 ATL03 datasets from the sites. Sites of type A can typically be found
at or close to established in-situ gauging stations because such stations require a simple and
stable rating curve. We chose the Pfelling gauging station on the Danube River in Germany
as an example of sites of type A.

Sites of type B are not very common because a natural river tends to smooth out abrupt
changes of slope and cross section shape by erosion and sedimentation processes. Bed
slope changes from high slope to low slope are typically not abrupt but gradual, smoothing
out backwater effects generated by the slope change, as illustrated for the Torne River on
the border between Sweden and Finland in Figure 3.

Figure 3. ATL03 water surface elevation profile for the Torne River. (A): Base map of the area with
selected ICESat-2 tracks. Background is Google satellite imagery. Coordinate grid as decimal latitude
and longitude (EPSG 4326). (B): ICESat-2 WSE data versus river km from Pello. Pink datapoints are
from 20 May 2023. Pello in-situ discharge data [29] show a 100-year flood event on this day.

However, rapids and waterfalls (case B1) are common in rivers around the world
and can be easily identified on high-resolution imagery as sections with whitewater. Here
we use the example of the Vermilion Falls on the Peace River in Canada to illustrate this
non-uniform flow situation.

Many major river confluences (case C) exist on the global river network. We chose the
Ganges-Ghaghara confluence close to the city of Chapra in India to illustrate the hydraulic
phenomena around river confluences. Liu et al., 2023 [20] show similar results for a number
of major river confluences in the Mississippi-Missouri river system.

Flood waves (case D) are short-term phenomena and, because of the sparse temporal
sampling pattern, are hard to observe in the ICESat-2 record. A spectacular flood wave
was generated by the June 2023 dam break of the Kakhovka Dam on the Dnipro River in
Ukraine [30]. Coincidentally, ICESat-2 provided one high-quality overpass over the area
affected by the flood wave on 6 June 2023 in the immediate aftermath of the dam break. We
use this case to illustrate the impact of flood waves on the water surface slope in rivers.

Backwater upstream of lakes and reservoirs is a common phenomenon around the
world, as there are thousands of major reservoirs on world rivers that show significant
seasonal water level variations. We choose the Toktogul reservoir on the Naryn River
in Kyrgyzstan here to illustrate this phenomenon. Coastal backwater affects all rivers as

Remote Sens. 2024, 16, x FOR PEER REVIEW 7 of 15   Sites of type B are not very common because a natural river tends to smooth out ab-rupt changes of slope and cross section shape by erosion and sedimentation processes. Bed slope changes from high slope to low slope are typically not abrupt but gradual, smoothing out backwater eﬀects generated by the slope change, as illustrated for the Torne River on the border between Sweden and Finland in Figure 3. . Figure 3. ATL03 water surface elevation proﬁle for the Torne River. (A): Base map of the area with selected ICESat-2 tracks. Background is Google satellite imagery. Coordinate grid as decimal lati-tude and longitude (EPSG 4326). (B): ICESat-2 WSE data versus river km from Pello. Pink datapoints are from 20 May 2023. Pello in-situ discharge data [29] show a 100-year ﬂood event on this day. However, rapids and waterfalls (case B1) are common in rivers around the world and can be easily identiﬁed on high-resolution imagery as sections with whitewater. Here we use the example of the Vermilion Falls on the Peace River in Canada to illustrate this non-uniform ﬂow situation. Many major river conﬂuences (case C) exist on the global river network. We chose the Ganges-Ghaghara conﬂuence close to the city of Chapra in India to illustrate the hy-draulic phenomena around river conﬂuences. Liu et al., 2023 [20] show similar results for a number of major river conﬂuences in the Mississippi-Missouri river system. Flood waves (case D) are short-term phenomena and, because of the sparse temporal sampling pattern, are hard to observe in the ICESat-2 record. A spectacular ﬂood wave was generated by the June 2023 dam break of the Kakhovka Dam on the Dnipro River in Ukraine [30]. Coincidentally, ICESat-2 provided one high-quality overpass over the area aﬀected by the ﬂood wave on 6 June 2023 in the immediate aftermath of the dam break. We use this case to illustrate the impact of ﬂood waves on the water surface slope in rivers. Backwater upstream of lakes and reservoirs is a common phenomenon around the world, as there are thousands of major reservoirs on world rivers that show signiﬁcant seasonal water level variations. We choose the Toktogul reservoir on the Naryn River in Kyrgyzstan here to illustrate this phenomenon. Coastal backwater aﬀects all rivers as they approach the oceans. However, this phenomenon is more complex because tidal varia-tions at the coastal water level are fast, leading to dynamic changes of water surface ele-vation proﬁles in coastal rivers including ﬂow reversals and anti-slopes, which cannot be modelled using the concept of steady gradually varied ﬂow and are thus beyond the scope of this paper. 3.1. Case A: Uniform Flow Remote Sens. 2024, 16, 4010

8 of 15

they approach the oceans. However, this phenomenon is more complex because tidal
variations at the coastal water level are fast, leading to dynamic changes of water surface
elevation profiles in coastal rivers including flow reversals and anti-slopes, which cannot
be modelled using the concept of steady gradually varied flow and are thus beyond the
scope of this paper.

3.1. Case A: Uniform Flow

A typical uniform flow site is the Pfelling gauging station (Lon: 12.7472, Lat: 48.8797)
on the Danube River in Germany (Figure 4). In-situ discharge data are available from the
GRDC online database [26] and has been used in this analysis. Figure 4 illustrates the
available ICESat-2 crossings and the location of the in-situ station. Panel B provides ICESat-
2 water surface elevation estimates as dependent on chainage and river discharge. We
observe a close match between the observed water surface elevations and the water surface
elevations predicted by the uniform flow equation. Panels C and D provide observed
water surface elevations and water surface slopes for the in-situ station location as well as
simulated WSE–discharge and WSS–discharge relationships. The WSE observations along
the river were extrapolated to the station location assuming a uniform WSS. It is evident
that the data are in good qualitative agreement with the uniform flow assumption—i.e.,
increasing WSE with discharge, following a power law, and a uniform WSS with discharge.
In summary, in case A, we expect increasing WSE with increasing discharge and a constant
WSS with increasing discharge. ICESat-2 data from the Pfelling site are in qualitative
agreement with this conceptual understanding.

Figure 4. Uniform flow at the Pfelling site on the Danube River. (A): Base map of the area and available
ICESat-2 overpasses. Background is Google satellite imagery. Coordinate grid as decimal latitude and
longitude (EPSG 4326). (B): Simulated (solid lines) and ICESat-2 (crosses) WSE as dependent on GRDC
discharge. Black solid line is imputed river bottom elevation. (C): Simulated (solid line) and observed
WSE at Pfelling station. Vertical lines indicate 90% confidence intervals. (D): Simulated (solid line) and
observed WSS at Pfelling station. Vertical lines indicate 90% confidence intervals.

Remote Sens. 2024, 16, x FOR PEER REVIEW 8 of 15   A typical uniform ﬂow site is the Pfelling gauging station (Lon: 12.7472, Lat: 48.8797) on the Danube River in Germany (Figure 4). In-situ discharge data are available from the GRDC online database [26] and has been used in this analysis. Figure 4 illustrates the available ICESat-2 crossings and the location of the in-situ station. Panel B provides ICE-Sat-2 water surface elevation estimates as dependent on chainage and river discharge. We observe a close match between the observed water surface elevations and the water sur-face elevations predicted by the uniform ﬂow equation. Panels C and D provide observed water surface elevations and water surface slopes for the in-situ station location as well as simulated WSE–discharge and WSS–discharge relationships. The WSE observations along the river were extrapolated to the station location assuming a uniform WSS. It is evident that the data are in good qualitative agreement with the uniform ﬂow assumption—i.e., increasing WSE with discharge, following a power law, and a uniform WSS with dis-charge. In summary, in case A, we expect increasing WSE with increasing discharge and a constant WSS with increasing discharge. ICESat-2 data from the Pfelling site are in qual-itative agreement with this conceptual understanding.  Figure 4. Uniform ﬂow at the Pfelling site on the Danube River. (A): Base map of the area and avail-able ICESat-2 overpasses. Background is Google satellite imagery. Coordinate grid as decimal lati-tude and longitude (EPSG 4326). (B): Simulated (solid lines) and ICESat-2 (crosses) WSE as depend-ent on GRDC discharge. Black solid line is imputed river bottom elevation. (C): Simulated (solid line) and observed WSE at Pfelling station. Vertical lines indicate 90% conﬁdence intervals. (D): Sim-ulated (solid line) and observed WSS at Pfelling station. Vertical lines indicate 90% conﬁdence inter-vals.   Remote Sens. 2024, 16, 4010

9 of 15

3.2. Case B: Slope or Cross Section Change

We illustrate case B1 for the Vermillion falls (Lon: −114.8707, Lat: 58.3713) on the Peace
River in Canada (Figure 5). This river section is fairly uniform but bisected by a waterfall
of several meters’ altitude, as shown in panels A and B of Figure 5. We excluded ICESat-2
data for the winter months (November to March) as the river is icebound in this period,
which complicates water level–discharge relationships. We do not have access to in-situ
river discharge at this site and thus used the GLOFAS reanalysis dataset [27,28] to estimate
river discharge. Significant river discharge uncertainty is thus to be expected. Panel B
shows good qualitative agreement of the ICESat-2 data with a hydraulic model simulating
a critical flow section just upstream of the falls. Some noise exists in the discharge–WSE
relationships, which we partly attribute to the limited accuracy of the GLOFAS river
discharge data. As illustrated in Panel C, the hydraulic model with a critical section at
the downstream boundary results in unique 1:1 relationships between the river discharge
and WSE and river discharge/WSS for any chainage point upstream of the falls within
the zone affected by the backwater from the falls. For this reason, observations of WSE
and/or WSS can be directly translated to river discharge in this case, making it possible to
estimate river discharge from space. In summary, in case B1, we expect increasing WSE and
increasing WSS with increasing discharge. The ICESat-2 dataset from Vermillion Falls is in
qualitative agreement with this conceptual understanding. Sites of type B1 are common in
global rivers and offer good conditions for estimating river discharge from satellite earth
observation using remotely sensed WSE, WSS, or a combination of both.

Figure 5. Vermillion Falls on the Peace River. (A): Base map of the area with selected ICESat-2 tracks.
Background is Google satellite imagery. Coordinate grid as decimal latitude and longitude (EPSG
4326). (B): Simulated (solid lines) and ICESat-2 (dots) WSE as dependent on GLOFAS discharge.
(C): Simulated WSE and WSS at three points upstream of the falls.

Remote Sens. 2024, 16, x FOR PEER REVIEW 9 of 15   3.2. Case B: Slope or Cross Section Change We illustrate case B1 for the Vermillion falls (Lon: −114.8707, Lat: 58.3713) on the Peace River in Canada (Figure 5). This river section is fairly uniform but bisected by a waterfall of several meters’ altitude, as shown in panels A and B of Figure 5. We excluded ICESat-2 data for the winter months (November to March) as the river is icebound in this period, which complicates water level–discharge relationships. We do not have access to in-situ river discharge at this site and thus used the GLOFAS reanalysis dataset [27,28] to estimate river discharge. Signiﬁcant river discharge uncertainty is thus to be expected. Panel B shows good qualitative agreement of the ICESat-2 data with a hydraulic model simulating a critical ﬂow section just upstream of the falls. Some noise exists in the dis-charge–WSE relationships, which we partly attribute to the limited accuracy of the GLO-FAS river discharge data. As illustrated in Panel C, the hydraulic model with a critical section at the downstream boundary results in unique 1:1 relationships between the river discharge and WSE and river discharge/WSS for any chainage point upstream of the falls within the zone aﬀected by the backwater from the falls. For this reason, observations of WSE and/or WSS can be directly translated to river discharge in this case, making it pos-sible to estimate river discharge from space. In summary, in case B1, we expect increasing WSE and increasing WSS with increasing discharge. The ICESat-2 dataset from Vermillion Falls is in qualitative agreement with this conceptual understanding. Sites of type B1 are common in global rivers and oﬀer good conditions for estimating river discharge from satellite earth observation using remotely sensed WSE, WSS, or a combination of both.  Figure 5. Vermillion Falls on the Peace River. (A): Base map of the area with selected ICESat-2 tracks. Background is Google satellite imagery. Coordinate grid as decimal latitude and longitude (EPSG 4326). (B): Simulated (solid lines) and ICESat-2 (dots) WSE as dependent on GLOFAS discharge. (C): Simulated WSE and WSS at three points upstream of the falls.   Remote Sens. 2024, 16, 4010

10 of 15

3.3. Case C: River Confluence

We illustrate river confluence effects at the confluence of the Ganges and Ghaghara
rivers (Lon: 84.7130, Lat: 25.7371) in India in Figure 6. The discharge estimates at this site
are from the GLOFAS archive [28], and we thus expect significant uncertainty in terms of
the estimated discharge. The hydraulic confluence model used here is described in the
methods section and in a recent paper [20]. Clearly, the ICESat-2 datasets are in qualitative
agreement with the predictions provided by the confluence model, while exact quantitative
matches cannot be expected given the limitations of the GLOFAS discharge estimates and
the simplifying assumptions underlying the hydraulic model. In summary, upstream of
river confluences, the WSE and WSS are determined by the discharges in both tributaries.
Discharge in one of the tributaries only is insufficient to predict the WSE and WSS in the
river. Thus, care needs to be taken when interpreting the WSE and WSS from satellite earth
observation upstream of major river confluences.

Figure 6. Confluence between the Ganges and the Ghaghara Rivers. (A): Base map of the area
with selected ICESat-2 tracks. Background is Google satellite imagery. Coordinate grid as decimal
latitude and longitude (EPSG 4326). (B): Simulated (lines) and ICESat-2 (dots) WSE in the Ganges as
dependent on Ganges River discharge (GLOFAS). (C): Simulated (lines) and ICESat-2 (dots) WSE in
the Ghaghara as dependent on Ghaghara River discharge (GLOFAS). In (B,C), solid lines indicate
simulation results for minimum flow in both Ganges and Ghaghara, dotted lines indicate maximum
flow in both Ganges and Ghaghara, dashed lines indicate minimum flow in Ganges and maximum
flow in Ghaghara, and dashed-dotted lines indicate maximum flow in Ghaghara and minimum flow
in Ganges.

Remote Sens. 2024, 16, x FOR PEER REVIEW 10 of 15   3.3. Case C: River Conﬂuence We illustrate river conﬂuence eﬀects at the conﬂuence of the Ganges and Ghaghara rivers (Lon: 84.7130, Lat: 25.7371) in India in Figure 6. The discharge estimates at this site are from the GLOFAS archive [28], and we thus expect signiﬁcant uncertainty in terms of the estimated discharge. The hydraulic conﬂuence model used here is described in the methods section and in a recent paper [20]. Clearly, the ICESat-2 datasets are in qualitative agreement with the predictions provided by the conﬂuence model, while exact quantita-tive matches cannot be expected given the limitations of the GLOFAS discharge estimates and the simplifying assumptions underlying the hydraulic model. In summary, upstream of river conﬂuences, the WSE and WSS are determined by the discharges in both tributar-ies. Discharge in one of the tributaries only is insuﬃcient to predict the WSE and WSS in the river. Thus, care needs to be taken when interpreting the WSE and WSS from satellite earth observation upstream of major river conﬂuences.  Figure 6. Conﬂuence between the Ganges and the Ghaghara Rivers. (A): Base map of the area with selected ICESat-2 tracks. Background is Google satellite imagery. Coordinate grid as decimal lati-tude and longitude (EPSG 4326). (B): Simulated (lines) and ICESat-2 (dots) WSE in the Ganges as dependent on Ganges River discharge (GLOFAS). (C): Simulated (lines) and ICESat-2 (dots) WSE in the Ghaghara as dependent on Ghaghara River discharge (GLOFAS). In (B,C), solid lines indicate simulation results for minimum ﬂow in both Ganges and Ghaghara, dotted lines indicate maximum ﬂow in both Ganges and Ghaghara, dashed lines indicate minimum ﬂow in Ganges and maximum ﬂow in Ghaghara, and dashed-dotted lines indicate maximum ﬂow in Ghaghara and minimum ﬂow in Ganges.  Remote Sens. 2024, 16, 4010

11 of 15

3.4. Case D: Flood Wave

On 6 June 2023, the Kakhovka dam on the Dnipro River in Ukraine (Lon: 33.3657,
Lat: 46.7760) collapsed, creating a massive flood wave on the river reach from Kakhovka
to the Black Sea. Water levels just downstream of the dam rose up to 16 m [30]. Several
high-quality ICESat-2 tracks over the river reach are available for the period of interest,
including one crossing on 6 June immediately after the dam break, as shown in Figure 7A.
From the ICESat-2 data, it is evident that water levels in the river rose by several meters
because of the dam break (Figure 7B) and that the water surface slope increased significantly
during the flooding event at locations close to the wavefront (Figure 7C). We used the
traveling wave model presented in the methods section to predict water surface slope
changes around the wavefront. Assuming a bed slope of 2 cm/km, a Chézy coefficient
of 90 m1/2/s, and an effective depth of 0.5 m prior to the flood event, the model predicts
a WSS change from 2 cm/km to ca. 12 cm/km during the passage of the wave front,
which travels down the river at 1.7 m/s. The available ICESat-2 data show the WSS at
around 20 cm/km on 6 June 2023, which is higher than the prediction of the traveling wave
model and indicates that the shape of the wavefront is not in steady state at the time and
place of the ICESat-2 overpass. The WSS in July–August 2023 is close to zero, indicating
quasi-stagnant water (Figure 7C). In summary, the Kakhovka case shows that the range
of WSS occurring during the passage of a flood wave can be predicted using the simple
traveling wave model presented here. This result can be used for large-scale hydraulic
analysis using SWOT and ICESat-2 data, for instance, to predict the maximum expected
WSS during the passage of flood waves in global river reaches.

Figure 7. Dnipro River downstream of Kakhovka Dam. (A): Base map of the area and available
ICESat-2 overpasses. Background is Google satellite imagery. Coordinate grid as decimal latitude and
longitude (EPSG 4326). (B): ICESat-2 WSE data. Dashed lines indicate simulated propagation of the
traveling wave through the river. (C): ICESat-2 WSS estimates with 90% confidence intervals. Dashed
lines indicate bed slope (black) and maximum slope predicted by the traveling wave model (blue).

Remote Sens. 2024, 16, x FOR PEER REVIEW 11 of 15   3.4. Case D: Flood Wave On 6 June 2023, the Kakhovka dam on the Dnipro River in Ukraine (Lon: 33.3657, Lat: 46.7760) collapsed, creating a massive ﬂood wave on the river reach from Kakhovka to the Black Sea. Water levels just downstream of the dam rose up to 16 m [30]. Several high-quality ICESat-2 tracks over the river reach are available for the period of interest, includ-ing one crossing on 6 June immediately after the dam break, as shown in Figure 7A. From the ICESat-2 data, it is evident that water levels in the river rose by several meters because of the dam break (Figure 7B) and that the water surface slope increased signiﬁcantly dur-ing the ﬂooding event at locations close to the wavefront (Figure 7C). We used the travel-ing wave model presented in the methods section to predict water surface slope changes around the wavefront. Assuming a bed slope of 2 cm/km, a Chézy coeﬃcient of 90 m1/2/s, and an eﬀective depth of 0.5 m prior to the ﬂood event, the model predicts a WSS change from 2 cm/km to ca. 12 cm/km during the passage of the wave front, which travels down the river at 1.7 m/s. The available ICESat-2 data show the WSS at around 20 cm/km on 6 June 2023, which is higher than the prediction of the traveling wave model and indicates that the shape of the wavefront is not in steady state at the time and place of the ICESat-2 overpass. The WSS in July–August 2023 is close to zero, indicating quasi-stagnant water (Figure 7C). In summary, the Kakhovka case shows that the range of WSS occurring dur-ing the passage of a ﬂood wave can be predicted using the simple traveling wave model presented here. This result can be used for large-scale hydraulic analysis using SWOT and ICESat-2 data, for instance, to predict the maximum expected WSS during the passage of ﬂood waves in global river reaches.  Figure 7. Dnipro River downstream of Kakhovka Dam. (A): Base map of the area and available ICESat-2 overpasses. Background is Google satellite imagery. Coordinate grid as decimal latitude and longitude (EPSG 4326). (B): ICESat-2 WSE data. Dashed lines indicate simulated propagation of the traveling wave through the river. (C): ICESat-2 WSS estimates with 90% conﬁdence intervals. Remote Sens. 2024, 16, 4010

12 of 15

3.5. Case E: Backwater from Lakes/Reservoirs/the Coast

We illustrate the backwater effects from reservoirs for the Toktogul Reservoir on the
Naryn River (Lon: 73.2568, Lat: 41.7755) in Kyrgyzstan (Figure 8). Seasonal water level
changes in this reservoir are several 10s of meters, leading to significant WSS changes in
the backwater-affected zones upstream of the reservoir. The ICESat-2 WSE observations
show the reservoir storage dynamics (Figure 8B), and Figure 8C clearly shows the zone
of high WSS variability at the interface between river and reservoir. In the downstream
portion, i.e., for chainages larger than −5 km, the WSS is always close to zero as this part is
always covered by the lake. In the upstream portion, i.e., for chainages between −30 km
and −20 km, the WSS is always close to the bed slope of the Naryn River. In river reaches
like this one, the water surface elevation and water surface slope are primarily controlled
by reservoir storage dynamics, and estimating river discharge from water level is thus
problematic and error prone. In summary, WSE and WSS dynamics upstream of reservoirs,
lakes, and the sea are shown to depend both on river discharge and water level in the
receiving water body. It is important to note that the backwater effects from receiving water
bodies can extend far upstream up to hundreds of kilometers in lowland rivers with low
bed slopes.

Figure 8. Toktogul Reservoir on the Naryn River. (A): Base map of the area with selected ICESat-2
tracks. Background is Google satellite imagery. Coordinate grid as decimal latitude and longitude
(EPSG 4326). (B): ICESat-2 WSE data. Dashed lines indicate simulated WSE for high and low reservoir
levels. (C): ICESat-2 WSS estimates with 90% confidence intervals. Dashed lines indicate bed slope of
Naryn River and zero WSS in the reservoir.

4. Discussion

We classified non-uniform flow situations in natural rivers, analyzed the inter-relations
between river discharge, water surface elevation, and water surface slope for the different
non-uniform flow situations using steady gradually varied one-dimensional flow theory,
and illustrated the different non-uniform flow situations using ICESat-2 laser altimetry data.

Remote Sens. 2024, 16, x FOR PEER REVIEW 12 of 15   Dashed lines indicate bed slope (black) and maximum slope predicted by the traveling wave model (blue). 3.5. Case E: Backwater from Lakes/Reservoirs/the Coast We illustrate the backwater eﬀects from reservoirs for the Toktogul Reservoir on the Naryn River (Lon: 73.2568, Lat: 41.7755) in Kyrgyzstan (Figure 8). Seasonal water level changes in this reservoir are several 10s of meters, leading to signiﬁcant WSS changes in the backwater-aﬀected zones upstream of the reservoir. The ICESat-2 WSE observations show the reservoir storage dynamics (Figure 8B), and Figure 8C clearly shows the zone of high WSS variability at the interface between river and reservoir. In the downstream por-tion, i.e., for chainages larger than −5 km, the WSS is always close to zero as this part is always covered by the lake. In the upstream portion, i.e., for chainages between −30 km and −20 km, the WSS is always close to the bed slope of the Naryn River. In river reaches like this one, the water surface elevation and water surface slope are primarily controlled by reservoir storage dynamics, and estimating river discharge from water level is thus problematic and error prone. In summary, WSE and WSS dynamics upstream of reser-voirs, lakes, and the sea are shown to depend both on river discharge and water level in the receiving water body. It is important to note that the backwater eﬀects from receiving water bodies can extend far upstream up to hundreds of kilometers in lowland rivers with low bed slopes.  Figure 8. Toktogul Reservoir on the Naryn River. (A): Base map of the area with selected ICESat-2 tracks. Background is Google satellite imagery. Coordinate grid as decimal latitude and longitude (EPSG 4326). (B): ICESat-2 WSE data. Dashed lines indicate simulated WSE for high and low reser-voir levels. (C): ICESat-2 WSS estimates with 90% conﬁdence intervals. Dashed lines indicate bed slope of Naryn River and zero WSS in the reservoir.   Remote Sens. 2024, 16, 4010

13 of 15

We did not perform high-fidelity hydraulic modeling in this study for two reasons: First,
we do not have access the required datasets such as bathymetric surveys, accurate high-
frequency discharge time series, etc., for the sites of interest. Second, we are interested in
the generic inter-relations between river discharge, WSE, and WSS and not in site-specific
phenomena. Due to the highly simplified nature of the hydraulic models used in this
study, we do not expect to fit the observations quantitatively—i.e., we do not expect that
simulated quantities are within the confidence intervals of observations. To obtain reliable
high-fidelity hydraulic models of the river sites discussed in this paper, follow-up modeling
studies using common numerical hydraulic modeling software packages are recommended.

4.1. Hydraulic Insights from WSS Observations

The water surface slope estimates provided by the latest generation of satellite radar
and laser altimetry missions (ICESat-2, SWOT) provide detailed insights into site-scale
hydraulic phenomena occurring in the investigated rivers. Specifically, analyzing the
variability of WSS observations in time, we can establish the validity of the uniform flow
assumptions at any river site. If uniform flow is a reasonable assumption for a site, the
WSS is expected to be independent of river discharge and thus constant in time. We
have outlined the most common situations in which the uniform flow assumptions are
not fulfilled in natural rivers: abrupt conveyance changes, confluences, flood waves, and
backwater effects from lakes/reservoirs. The simplified hydraulic models presented here
enable us to produce informed estimates of the expected maximum WSS during the passage
of a flood wave, the WSS changes upstream of rapids and waterfalls, and the expected WSS
dynamics upstream of river confluences.

4.2. River Discharge from WSE and WSS

A key objective of current inland water altimetry research is to estimate river discharge
from space. Based on our analysis, we can conclude that river discharge can be estimated
from the WSE alone in cases A and B, while this was not possible in cases C, D, and E. In
case C, coincident observations of WSE and WSS can lead to a well constrained discharge
estimate as shown in [20], while in cases D and E, additional information is required for
river discharge estimation. It is important to note that, while the WSS is independent of
discharge in case A, the WSS will change with discharge in case B. We highlight again
that river discharge estimates used in this study were adopted from the cited data sources
without quality assurance or verification. While we are unable to quantify river discharge
uncertainty for the different sites discussed in this study, we expect significant uncertainty
on the order of 20–30% for the GLOFAS river discharge estimates.

4.3. Limitations of Current Observation Technology and Future Potential

Currently, the WSS can be observed with a standard error of ca 2 cm/km in rivers
using ICESat-2 data [12,13]. Similar accuracy is expected from a SWOT. While this accuracy
is sufficient for the study of many inland rivers, bed slopes in coastal rivers are often around
or below 1 cm/km and WSS changes are of similar order of magnitude. Thus, the hydraulic
analysis of coastal rivers, estuaries, and river deltas is currently still challenging, except
for very large rivers with large sets of high-quality ICESat-2/SWOT observations covering
long chainage intervals.

5. Conclusions

Under approximately uniform flow conditions, river WSS is constant and independent
of discharge, and a unique relationship exists between the WSE and discharge, which
enables the direct estimation of river discharge from satellite altimetry. However, the
assumptions of uniform flow are not fulfilled along many river reaches globally including,
for instance, upstream of bed slope or cross section changes (case B in this paper), upstream
of waterfalls and rapids (case B1), upstream of river confluences (case C), during the
transition of flood waves (case D), and upstream of lakes/reservoirs/the coast (case E). In

Remote Sens. 2024, 16, 4010

14 of 15

all these cases, the WSS varies with discharge. In case B/B1, although the WSS changes
with discharge, a unique relationship between the WSE and discharge exists, just like
under uniform flow conditions. In case C, there is no unique relationship between the WSE
and discharge, but coincident observations of the WSE and WSS (such as available from
ICESat and SWOT) can constrain discharge estimates. In cases D and E, it is not possible
to estimate discharge from the WSE and WSS because both the WSS and WSE depend on
additional variables other than local discharge at the point of observation.

Author Contributions: Conceptualization, P.B.-G.; Methodology, P.B.-G., L.C., A.M., M.C.F. and K.N.;
Software, P.B.-G.; Validation, P.B.-G.; Formal analysis, P.B.-G., A.M., M.C.F. and K.N.; Data curation,
L.C., A.M., M.C.F. and K.N.; Writing—original draft, P.B.-G.; Writing—review & editing, P.B.-G., L.C.,
A.M., M.C.F. and K.N. All authors have read and agreed to the published version of the manuscript.

Funding: This work was partly funded by Horizon Europe, contract number 101081783.

Data Availability Statement: This work is based exclusively on public domain data. ICESat-2
ATL03 data can be downloaded from https://nsidc.org/data/atl03/versions/6 (accessed on 15
August 2024). GLOFAS river discharge estimates can be downloaded from https://ewds.climate.
copernicus.eu/datasets/cems-glofas-historical?tab=overview (accessed on 15 August 2024). GRDC
river discharge data can be downloaded from https://portal.grdc.bafg.de/applications/public.html?
publicuser=PublicUser#dataDownload/Stations (accessed on 15 August 2024).

Conflicts of Interest: The authors declare no conflicts of interest.

References

1.

2.

3.

Abdalla, S.; Abdeh Kolahchi, A.; Ablain, M.; Adusumilli, S.; Aich Bhowmick, S.; Alou-Font, E.; Amarouche, L.; Andersen, O.B.;
Antich, H.; Aouf, L.; et al. Altimetry for the Future: Building on 25 Years of Progress. Adv. Space Res. 2021, 68, 319–363. [CrossRef]
Paris, A.; Dias de Paiva, R.; Santos da Silva, J.; Medeiros Moreira, D.; Calmant, S.; Garambois, P.-A.; Collischonn, W.; Bonnet,
M.-P.; Seyler, F. Stage-Discharge Rating Curves Based on Satellite Altimetry and Modeled Discharge in the Amazon Basin. Water
Resour. Res. 2016, 52, 3787–3814. [CrossRef]
Papa, F.; Bala, S.K.; Pandey, R.K.; Durand, F.; Gopalakrishna, V.V.; Rahman, A.; Rossow, W.B. Ganga-Brahmaputra River Discharge
from Jason-2 Radar Altimetry: An Update to the Long-Term Satellite-Derived Estimates of Continental Freshwater Forcing Flux
into the Bay of Bengal. J. Geophys. Res. Oceans 2012, 117, C11. [CrossRef]

4. Michailovsky, C.I.; McEnnis, S.; Berry, P.A.M.; Smith, R.; Bauer-Gottwein, P. River Monitoring from Satellite Radar Altimetry in

5.

6.

the Zambezi River Basin. Hydrol. Earth Syst. Sci. 2012, 16, 2181–2192. [CrossRef]
Jiang, L.; Nielsen, K.; Dinardo, S.; Andersen, O.B.; Bauer-Gottwein, P. Evaluation of Sentinel-3 SRAL SAR Altimetry over Chinese
Rivers. Remote. Sens. Environ. 2020, 237, 111546. [CrossRef]
Schneider, R.; Ridler, M.-E.; Godiksen, P.N.; Madsen, H.; Bauer-Gottwein, P. A Data Assimilation System Combining CryoSat-2
Data and Hydrodynamic River Models. J. Hydrol. 2018, 557, 197–210. [CrossRef]

8.

7. Hossain, F.; Siddique-E-Akbor, A.H.; Mazumder, L.C.; Shahnewaz, S.M.; Biancamaria, S.; Lee, H.; Shum, C.K. Proof of Concept
of an Altimeter-Based River Forecasting System for Transboundary Flow inside Bangladesh. IEEE J. Sel. Top. Appl. Earth Obs.
Remote. Sens. 2014, 7, 587–601. [CrossRef]
Chang, C.-H.; Lee, H.; Hossain, F.; Basnayake, S.; Jayasinghe, S.; Chishtie, F.; Saah, D.; Yu, H.; Sothea, K.; Du Bui, D. A Model-
Aided Satellite-Altimetry-Based Flood Forecasting System for the Mekong River. Environ. Model. Softw. 2019, 112, 112–127.
[CrossRef]
Paiva, R.C.D.; Collischonn, W.; Bonnet, M.-P.; De Gonçalves, L.G.G.; Calmant, S.; Getirana, A.; Santos Da Silva, J. Assimilating in
Situ and Radar Altimetry Data into a Large-Scale Hydrologic-Hydrodynamic Model for Streamflow Forecast in the Amazon.
Hydrol. Earth Syst. Sci. 2013, 17, 2929–2946. [CrossRef]

9.

10. Markus, T.; Neumann, T.; Martino, A.; Abdalati, W.; Brunt, K.; Csatho, B.; Farrell, S.; Fricker, H.; Gardner, A.; Harding, D.; et al.
The Ice, Cloud, and Land Elevation Satellite-2 (ICESat-2): Science Requirements, Concept, and Implementation. Remote Sens.
Environ. 2017, 190, 260–273. [CrossRef]

11. Biancamaria, S.; Lettenmaier, D.P.; Pavelsky, T.M. The SWOT Mission and Its Capabilities for Land Hydrology. Surv. Geophys.

12.

2016, 37, 307–337. [CrossRef]
Scherer, D.; Schwatke, C.; Dettmering, D.; Seitz, F. ICESat-2 Based River Surface Slope and Its Impact on Water Level Time Series
From Satellite Altimetry. Water Resour. Res. 2022, 58, e2022WR032842. [CrossRef]

13. Christoffersen, L.; Bauer-Gottwein, P.; Sørensen, L.S.; Nielsen, K. ICE2WSS; An R Package for Estimating River Water Surface

Slopes from ICESat-2. Environ. Model. Softw. 2023, 168, 105789. [CrossRef]

14. Tourian, M.J.; Elmi, O.; Shafaghi, Y.; Behnia, S.; Saemian, P.; Schlesinger, R.; Sneeuw, N. HydroSat: Geometric Quantities of the

Global Water Cycle from Geodetic Satellites. Earth Syst. Sci. Data 2022, 14, 2463–2486. [CrossRef]

Remote Sens. 2024, 16, 4010

15 of 15

15. Leon, J.G.; Calmant, S.; Seyler, F.; Bonnet, M.-P.; Cauhopé, M.; Frappart, F.; Filizola, N.; Fraizy, P. Rating Curves and Estimation of
Average Water Depth at the Upper Negro River Based on Satellite Altimeter Data and Modeled Discharges. J. Hydrol. 2006, 328,
481–496. [CrossRef]

16. Kouraev, A.V.; Zakharova, E.A.; Samain, O.; Mognard, N.M.; Cazenave, A. Ob’ River Discharge from TOPEX/Poseidon Satellite

Altimetry (1992-2002). Remote. Sens. Environ. 2004, 93, 238–245. [CrossRef]

17. Alsdorf, D.E.; Rodríguez, E.; Lettenmaier, D.P. Measuring Surface Water from Space. Rev. Geophys. 2007, 45, 2. [CrossRef]
18. Bjerklie, D.M.; Moller, D.; Smith, L.C.; Dingman, S.L. Estimating Discharge in Rivers Using Remotely Sensed Hydraulic

Information. J. Hydrol. 2005, 309, 191–209. [CrossRef]

19. Chow, V.T. Open-Channel Hydraulics. McGraw-Hill: New York, NY, USA, 1959.
20. Liu, J.; Bauer-Gottwein, P.; Frias, M.C.; Musaeus, A.F.; Christoffersen, L.; Jiang, L. Stage-Slope-Discharge Relationships Upstream

of River Confluences Revealed by Satellite Altimetry. Geophys. Res. Lett. 2023, 50, e2023GL106394. [CrossRef]

21. Christodoulou, G.C.; Noutsopoulos, G.C.; Andreou, S.A. Factors Affecting Brink Depth in Rectangular Overfalls. In Proceedings of

the Channels and Channel Control Structures; Smith, K.V.H., Ed.; Springer: Berlin/Heidelberg, Germany, 1984; pp. 3–17.

22. Neumann, T.A.; Brenner, A.; Hancock, D.; Robbins, J.; Gibbons, A.; Lee, J.; Harbeck, K.; Saba, J.; Luthcke, S.B.; Rebold, T.
ATLAS/ICESat-2 L2A Global Geolocated Photon Data, Version 6; NASA National Snow and Ice Data Center Distributed Active
Archive Center: Boulder, CO, USA, 2023.

23. Neumann, T.A.; Martino, A.J.; Markus, T.; Bae, S.; Bock, M.R.; Brenner, A.C.; Brunt, K.M.; Cavanaugh, J.; Fernandes, S.T.; Hancock,
D.W.; et al. The Ice, Cloud, and Land Elevation Satellite—2 Mission: A Global Geolocated Photon Product Derived from the
Aadvanced Ttopographic Llaser Aaltimeter Ssystem. Remote. Sens. Environ. 2019, 233, 111325. [CrossRef]

24. Coppo Frias, M.; Liu, S.; Mo, X.; Nielsen, K.; Ranndal, H.; Jiang, L.; Ma, J.; Bauer-Gottwein, P. River Hydraulic Modeling with

ICESat-2 Land and Water Surface Elevation. Hydrol. Earth Syst. Sci. 2023, 27, 1011–1032. [CrossRef]

25. Pavlis, N.K.; Holmes, S.A.; Kenyon, S.C.; Factor, J.K. The Development and Evaluation of the Earth Gravitational Model 2008

(EGM2008). J. Geophys. Res. Solid Earth 2012, 117, B4. [CrossRef]

26. The Global Runoff Data Centre—Data Download The Global Runoff Data Centre. Available online: https://portal.grdc.bafg.de/

applications/public.html?publicuser=PublicUser#dataDownload/Stations (accessed on 8 April 2024).

27. Harrigan, S.; Zsoter, E.; Alfieri, L.; Prudhomme, C.; Salamon, P.; Wetterhall, F.; Barnard, C.; Cloke, H.; Pappenberger, F.
GloFAS-ERA5 Operational Global River Discharge Reanalysis 1979-Present. Earth Syst. Sci. Data 2020, 12, 2043–2060. [CrossRef]
28. Copernicus Climate Change Service (C3S). River Discharge and Related Forecasted Data from the Global Flood Awareness
System. 2020. Available online: https://ewds.climate.copernicus.eu/datasets/cems-glofas-historical?tab=overview (accessed on
15 August 2024).

29. VESI Waterinfo.Fi. Available online: https://www.vesi.fi/en/karttapalvelu/ (accessed on 12 April 2024).
30. Ukrainian Nature Conservation Group The Consequences of the Russian Terrorist Attack on the Kakhovka Hydroelectric Power
Plant (HPP) for Wildlife. Available online: https://uncg.org.ua/en/the-consequences-of-the-russian-terrorist-attack-on-the-
kakhovka-hydroelectric-power-station-hps-for-wildlife/ (accessed on 11 April 2024).

Disclaimer/Publisher’s Note: The statements, opinions and data contained in all publications are solely those of the individual
author(s) and contributor(s) and not of MDPI and/or the editor(s). MDPI and/or the editor(s) disclaim responsibility for any injury to
people or property resulting from any ideas, methods, instructions or products referred to in the content.

