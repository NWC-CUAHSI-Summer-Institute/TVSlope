Remote Sensing of Environment 241 (2020) 111732

Contents lists available at ScienceDirect

Remote Sensing of Environment

journal homepage: www.elsevier.com/locate/rse

Hindcast and forecast of daily inundation extents using satellite SAR and
altimetry data with rotated empirical orthogonal function analysis: Case
study in Tonle Sap Lake Floodplain
Chi-Hung Changa, Hyongki Leea,⁎
Farrukh Chishtiee,f, Susantha Jayasinghee, Senaka Basnayakee
a Department of Civil and Environmental Engineering, University of Houston, 5000 Gulf Fwy, Bldg. 4, Rm#216, Houston, TX 77204, USA
b Department of Military Strategy, Joint Forces Military University, Jaun-ro, Yuseong-gu, Daejeon, 34059, South Korea
c Water Resources Research Center, K-Water Institute, 200 Sintanjin-ro, Daedeok-gu, 34350 Daejeon, South Korea
d Department of Civil & Environmental Engineering, University of Washington, Wilcox Hall 167, 2117 Mason Rd., Seattle, WA 98195, USA
e Asian Disaster Preparedness Center, SM Tower, 24th floor, 979/69 Paholyothin Road, Samsen Nai Phayathai, Bangkok 10400, Thailand
f Spatial Informatics Group, LLC, 2529 Yolanda Ct., Pleasanton, CA 94566, USA

, Donghwan Kima,b, Euiho Hwangc, Faisal Hossaind,

T

A R T I C L E I N F O

A B S T R A C T

Edited by Menghua Wang

Keywords:
Daily inundation extents estimation
Mekong River Basin
Tonle Sap Lake
SAR
Satellite altimetry
EOF analysis
Flood forecast

The Tonle Sap Lake (TSL) is the largest natural freshwater lake in Southeast Asia and is called the “heart of the lower
Mekong” due to its high aquatic biodiversity and is considered as one of the most productive freshwater ecosystems
of the world. Its floodplain eco-system, which is strongly tied to seasonal flood pulse, is extremely important for food
security, trade and economy of Cambodia, supporting the livelihoods of about 1.7 million people. On the other hand,
flood can also be extremely devastating in the region along the TSL. In recent years, studies have pointed out that
rapid growing number of water infrastructures as well as future climate changes may alter the hydrological cycle of
the Mekong River Basin (MRB) and are expected to influence the flood pulse of the TSL and surrounding TSL
floodplain. Therefore, it is timely to understand historical inundation extent and predict its likely future state. In this
study, we proposed a Rotated Empirical Orthogonal Function (REOF) analysis-based daily inundation extent esti-
mation framework, integrating multi-temporal stack of Sentinel-1A Synthetic Aperture Radar (SAR) imagery and
Jason-series satellite altimetry data. The framework can generate daily, cloud-free and gap-free inundation extents
for any given time depending on the altimetry data provided. A long-term El Niño and Southern Oscillation (ENSO)
index-based daily TSL level forecasting method with months of lead time was also proposed to fulfill the framework's
forecasting capacity. In this study, the framework was adopted in the TSL floodplain area for hindcast (2003 to 2015)
and forecast (January to July 2019) of daily inundation extents. Estimated inundation extents were cross-compared
with MODIS-derived and Sentinel-1-derived inundation maps, resulting in up to higher than 90% of Critical Success
Index (CSI). The proposed framework has (1) innovative capacity of estimation of future daily areal inundation
extents and is (2) a fully remote sensing-based framework which can empower local authorities tasked with water
resource management decisions without relying on upstream countries. The framework has potential to be im-
plemented in other major river basins or wetlands (e.g., Amazon River Basin, and Congo River Basin). The im-
plementation on SAR imagery from other satellites with different bands of electromagnetic wave is also possible but
requires more investigation.

1. Introduction

The Tonle Sap Lake (TSL) is the largest natural freshwater lake in
the Southeast Asia. The lake is well known for its unique seasonally
reversed flow. In the wet season, the Mekong River (MR) level con-
level.
tinuously rises and eventually exceeds

the TSL water

Consequently, water flows across the floodplain toward the lake. In the
dry season, water flows from the lake and floodplains down the Tonle
Sap River toward the sea, as the MR level recedes (Campbell et al.,
2009). Such flow reversal cannot be found anywhere else in the world
and has significant impact on the surrounding TSL floodplain eco-
system. Thanks to the unique reversed flow, during wet season, water

⁎

Corresponding author.
E-mail addresses: cchang21@uh.edu (C.-H. Chang), hlee@uh.edu (H. Lee), donghwan.kma@gmail.com (D. Kim), ehhwang@kwater.or.kr (E. Hwang),

fhossain@uw.edu (F. Hossain), Farrukh.chishtie@adpc.net (F. Chishtie), susantha@adpc.net (S. Jayasinghe), senaka_basnayake@adpc.net (S. Basnayake).

https://doi.org/10.1016/j.rse.2020.111732
Received 29 August 2019; Received in revised form 26 January 2020; Accepted 18 February 2020
0034-4257/ © 2020 Elsevier Inc. All rights reserved.

C.-H. Chang, et al.

Remote Sensing of Environment 241 (2020) 111732

area, volume, and depth of the TSL can increase by several folds relative
to dry season, leading to large extents of seasonally inundated areas
(MRC, 2009). Such high flood level and large inundated habitat create a
rich breeding ground for high fisheries productivity (Baran and Coates,
2000; Hortle et al., 2004; MRC, 2009; Sarkkula et al., 2005; Sarkkula
et al., 2003) as well as bio-diversity (Campbell et al., 2006), making TSL
the “heart of the lower Mekong” and is considered as one of the most
productive ecosystems in the world (Lamberts, 2006). Such feature
makes the TSL floodplain extremely important for Cambodia for food
security and economy (Fisheries Administration of Cambodia, 2011;
Hortle et al., 2004; Kummu et al., 2006).

In recent years, several studies have pointed out that climate change
and water infrastructure development would pose stress on flood pulse
and intensity of Mekong River Basin (MRB) and TSL (Kummu and
Sarkkula, 2008; Pokhrel et al., 2018). Wet season flow in the MRB is
dominated by precipitation from monsoon which have considerably
changed in recent years. On the other hand, temperature rise also alters
the stream flows of the MR. Since MR is the main source of water inflow
for the TSL (Kummu et al., 2006), climate change may significantly
alter the flood pulse of the TSL and consequently impact the ecosystem
and productivity of agriculture and aquaculture in the TSL floodplain
ecosystem (Adamson, 2006; Fredén, 2011; Lauri et al., 2012; Lutz et al.,
2014; MRC, 2010; Pokhrel et al., 2018). On the other hand, due to rapid
change and economy boost of countries in the MRB these years, dam
construction has been accelerated. Such anthropogenic factor can alter
the flood pulse of the MRB and the TSL. Studies have shown that up-
stream water regulation can increase and reduce dry season and wet
season water level in the TSL, respectively, which is expected to in-
fluence the TSL floodplain ecosystem since the seasonally inundated
area would become smaller and thus reduce the transfer of floodplain
terrestrial organic matter and energy into aquatic phase (Kummu and
Sarkkula, 2008; Lamberts and Koponen, 2008; Pokhrel et al., 2018;
Västilä et al., 2010). Studies have revealed that flood amplitude and
duration in TSL floodplain can directly affect available biomass and
thus fish size, fish catches, and sustainability of fish population (Halls
et al., 2008; Hortle, 2009; Van Zalinge et al., 2003). Simulation of
Västilä et al. (2010) also shown that increase of the average and max-
imum water levels and flood duration may cause more severe damages
to roads, buildings and other infrastructures located over the floodplain
as well as other flood-related impacts such as destruction of rice crops,
rise of hygienic problems and more human victims particularly those
living close to the TSL (Keskinen, 2006; Nuorteva et al., 2010). In the
Disaster Management Reference Handbook of Cambodia published by
Center for Excellence in Disaster Management and Humanitarian
Assistance (CFE-DMHA) (2017), statistics also shown that the extreme
flood striking in 2011 caused the most severe damage in 4 provinces
along TSL and MR among 18 affected provinces. Therefore, to have
better understaning of dynamics of TSL floodplain inundation extents
and even forecast future inundation extents are of great importance and
urgently needed which can be helpful by providing more information
for assessing the change of fish catches and potential flooding damages
as well as corresponding relief services (Schumann and Moller, 2015).
Beginning from the use of the Multi-Spectral Scanner sensor onboard
the first Earth Resources Technology Satellite launched in 1972, which
was later renamed as Landsat-1 (Smith, 1997), optical imaging sensors
onboard the follow-on Landsat satellites and others have provided us with
opportunity to continuously monitor inundation extents over large areas
ever since. Among all satellite optical sensors, MODerate resolution Ima-
ging Spectroradiometer (MODIS), onboard NASA Terra and Aqua satellites
has high potential for operational application in hydrology, as its data is
freely available, well-calibrated and archived and has spatial resolution
(250 m, 500 m and 1000 m depending on spectral bands) adequate for
small and large river floods mapping. It also provides high temporal (up to
twice daily) and spectral resolution (36 bands) images with global cov-
erage (Crétaux et al., 2011). There are many studies using daily or multi-
day composite MODIS images for flood mapping and analysis (Ahamed

and Bolten, 2017; Fayne et al., 2017; Lin et al., 2019; Slayback et al., 2012;
Sakamoto et al., 2007). However, the application of satellite optical ima-
gery is hindered by cloud cover, which obscures Earth's surface observa-
tions, resulting in data gaps and inability to comprehensively delineate
outline of inundation especially during wet season (e.g., Martinis et al.,
2015; Pierdicca et al., 2013).

Synthetic Aperture Radar (SAR), on the other hand, is considered
the most useful sensor in detecting flooded areas under cloud cover
(Yan et al., 2015). Its use of active microwave signal allows it to pe-
netrate clouds and be independent from illumination and atmospheric
conditions, giving it capacity to provide surface observations without
spatial gaps in both day and night under all weather conditions. The
launch of European Space Agency's (ESA) Sentinel-1A in 2014 further
promotes the use of SAR imagery in flood mapping. Its consistent data
acquisition, shorter revisit time than previous SAR satellites, and free
data accessibility allow continuous monitoring of ground features and
their changes over time (Tsyganskaya et al., 2018a; White et al., 2014)
for public users, making its imagery frequently be applied on a variety
of research and operational use on depicting flood inundation (Markert
et al., 2018; Tsyganskaya et al., 2018a). For example, Cazals et al.
(2016) used Sentinel-1 Ground Range Detection High (GRDH) resolu-
tion images of both vertical-transmit and vertical-receive (VV) and
vertical-transmit and horizontal-receive (VH) polarizations with a
hysteresis thresholding algorithm to distinguish open water, flooded
vegetation and non-flooded grassland, which successfully detected open
water with moderate accuracy over flooded grasslands. They also
pointed out the high temporal frequency of Sentinel-1 acquisitions have
great potential on monitoring variations of seasonal floods. Twele et al.
(2016) proposed a fully automated processing chain for flood mapping
using Sentinel-1 GRDH images and tested in the Evros River in the East
Europe, giving promising accuracies. They pointed out the use of VV
polarizations gives slightly higher thematic accuracies. Recent studies
have focused on using Sentinel-1 images for rapid flood mapping as
well. Amitrano et al. (2018) proposed an unsupervised fuzzy classifi-
cation-based two-level processing method on Sentinel-1 GRDH images
for rapid flood mapping. Bioresita et al. (2018) proposed a processing
chain using modified split-based approach, finite mixture models and
bilateral filtering approach for delineating flood boundary also using
Sentinel-1 GRDH products. Moreover, short revisit times of Sentinel-1
also paves the way for the application of using time series of SAR
images for flood monitoring (Schlaffer et al., 2015). For example,
Tsyganskaya et al. (2018b) developed a time series classification ap-
proach to extract flood extent over temporary flooded vegetation.

Despite the rapid development and growing use of satellite imagery
on inundation extent detection, the number of studies working on
providing cloud-free and gap-free inundation extents based on satellite
imagery with high temporal resolution, often at daily or higher fre-
quency, is still quite challenging and limited (Ahmad et al., 2019). In
fact, studies have suggested the importance of such data on environ-
mental monitoring, water resource management, emergency response
and improving our understanding of variability of flood pulse (Klein
et al., 2015, 2017; Ticehurst et al., 2014). Many of these variabilities
resulted from environmental, climatic or anthropogenic changes occur
at a gradual rather than abrupt pace and would not be detectable
without information of inundation extent acquired at high temporal
frequency (Klein et al., 2015). However, despite the inherent cloud-
penetrating, and weather/sunlight independent advantage of SAR over
optical sensors, there is still no such study using SAR imagery to per-
form daily, cloud-free and gap-free areal inundation extent mapping.
Yet, the use of satellite imagery on performing forecasting of areal in-
undation extents has never been investigated before either despite the
increasing importance of knowing inundation extents in advance for
better first response and water resource management.

In this study, to address the need of forecasting high temporal fre-
quency areal inundation extents, we propose a daily areal inundation
estimation framework based on synthesized SAR intensity imagery. The

2

C.-H. Chang, et al.

Remote Sensing of Environment 241 (2020) 111732

framework first applies Rotated Empirical Orthogonal Function (REOF)
analysis (Kaiser, 1958; Lorenz, 1956), which has been shown to have
interpretability than conventional EOF analysis
improved physical
(Hannachi et al., 2006, 2007; Lian and Chen, 2012), on multi-temporal
SAR intensity images to extract their spatiotemporal patterns. The ex-
tracted spatiotemporal patterns were then associated with satellite al-
timetry-derived water levels. Next, satellite altimetry-derived water
levels were used as input to synthesize SAR intensity images, in which
the synthesized SAR intensity images are of the same date as the input
satellite altimetry-derived water levels. In other words, SAR intensity of
any time can be synthesized if satellite altimetry-derived water level is
available. Finally, corresponding inundation extents were estimated
from the use of both synthesized SAR intensity imagery and the Multi-
Error-Removed Improved-Terrain Digital Elevation Model (MERIT
DEM) (Yamazaki et al., 2017) thru unsupervised K-means clustering
algorithm (Arthur and Vassilvitskii, 2007; Lloyd, 1982). Note that even
though EOF analysis (Lorenz, 1956) has been widely used in climate
sciences for coupling different fields, reconstruction, and prediction
(Bracher et al., 2015; Church et al., 2004; Imani et al., 2017; Taylor
et al., 2013; Yosef et al., 2017), this is the first study applying EOF
analysis-related method on SAR imagery for SAR intensity synthesis
and depicting areal inundation extents by integrating with satellite al-
timetry data, which particularly addresses the need for forecasting fu-
ture inundations extents to the best of our knowledge. Such application
of satellite altimetry is also not reported in literature despite the tech-
nique being known for such as for oceanography studies (Chang et al.,
2016; Nerem et al., 2018; Sánchez-Reales et al., 2012; Willis et al.,
2010) as well as retrieval of inland water levels (Biancamaria et al.,
2017; Boergens et al., 2019; Da Silva et al., 2012; Kim et al., 2017; Lee
et al., 2011; Sulistioadi et al., 2015; Tourian et al., 2016), calibration of
hydrodynamic model (Jiang et al., 2019), estimation of lake and re-
servoir water volumes (Busker et al., 2019; Zhou et al., 2016), river
discharges (Kim et al., 2019a, 2019b; Paris et al., 2016; Tarpanelli
et al., 2019; Tourian et al., 2017), and bathymetry (Brêda et al., 2019),
and water level forecasting (Biancamaria et al., 2011; Chang et al.,
2019; Hossain et al., 2014a, 2014b).

Here, the framework was applied to the TSL floodplain for daily
hindcasting and forecasting of areal inundations by using multi-temporal
Sentinel-1A imagery and daily Jason series altimetry-derived TSL levels.
The daily hindcasting and forecasting are fulfilled by using daily linear-
interpolated historical and El Niño/Southern Oscillation (ENSO) index-
forecasted altimetry-derived TSL levels. The estimated inundation extents
were cross-compared with reference datasets including inundation maps
derived from 8-day composite MODIS product as well as Sentinel-1
images. The proposed framework has features including: (1) Synthesis of
SAR intensity image and estimation of areal inundation extents of any time
as long as altimetry-derived water level is available; (2) The framework is
fully remote sensing-based in which computationally expensive model is
not required; (3) Since the framework exploits SAR imagery, the resulting
estimated inundation extents are free from cloud cover with no spatial
gap; (4) The framework has potential to be applied to the floodplains of
other major river basins such as Amazon River Basin and Congo River
Basin. The implementation using SAR imagery from other satellites with
different bands of electromagnetic wave (e.g., L-band ALOS) is also pos-
sible but requires further investigation.

This paper is structured as follows: Section 2 describes the data we
used, including (1) Sentinel-1 SAR intensity imagery, (2) MODIS sur-
face reflectance data and water mask, (3) MERIT DEM, (4) satellite
altimetry-derived and in-situ water levels at the TSL, and (5) index
representing strength of ENSO event. Section 3 explains (1) the pro-
posed REOF-based daily inundation extent estimating framework as
well as the generation of cross-comparison use Sentinel-1 inundation
maps, (2) the long-term ENSO-based forecasting of TSL levels, (3) the
generation of cross-comparison use MODIS inundation maps, and (4)
the skill evaluation indices in detail. Section 4 presents cross-compar-
ison and discussion of the results. Section 5 concludes this paper.

2. Data

2.1. Sentinel-1 SAR data

Sentinel-1 is a two-satellite-constellation mission (Sentinel-1A/-1B),
equipped with C-band (5.405 GHz) SAR, under the Copernicus Earth
observation program of ESA. The first satellite Sentinel-1A was laun-
ched on April 3rd, 2014, while Sentinel-1B was launched on April 25th,
2016. Both satellites feature free accessibility and 12 days of consistent
and short revisit time, which have expanded the use of SAR imagery in
the study of environmental change (Markert et al., 2018; Tsyganskaya
et al., 2018a; White et al., 2014). Sentinel-1 VV-polarization images of
GRDH product were downloaded from the Alaska Satellite Facility
(ASF). In order to have image scene covering whole TSL and sur-
rounding floodplain area, two frames including frame 552 and 547 of
path 91 acquired on the same date were used. Images of two frames on
each acquisition date were first mosaicked into one single scene (See
Fig. 1).

In this study, Sentinel-1A data were used solely for building the
framework. This is to avoid the influence of potential systematic dif-
ference between backscattering intensities acquired by two satellites
(Sentinel-1A/-1B) on the results of REOF analysis, which would affect
coupling the extracted temporal patterns with altimetry data, and thus
the estimated inundation extents (For detail of the framework, see
Section 3.1). The purpose was to reduce the extent of influence of signal
not related to natural phenomena to the least. Time span of images used
for building the framework is from April 3rd, 2016 to December 31st,
2018, giving us 78 images in total after mosaic. On the other hand,
Sentinel-1A images with temporal coverage from January 6th to July

Fig. 1. Frames of Sentinle-1 GRDH intensity images used in this study. The
image acquired on April 3rd, 2016 was used as an example.

3

C.-H. Chang, et al.

Remote Sensing of Environment 241 (2020) 111732

29th, 2019, and Sentinel-1B images from January 12th to July 23th,
2019, were used as reference datasets in addition to MODIS imagery for
cross-comparison purpose, giving us 54 images in total after mosaic.
Since our proposed framework exploits Sentinel-1 SAR imagery, using
Sentinel-1A/-1B imagery for cross-comparison can avoid the influence
of inherent inconsistency between radar and optical imagery on the
cross-comparison results. The cross-comparison using Sentinel-1 ima-
gery as reference dataset was conducted in the forecasting case with
time span starting from January 2019 since the earlier Sentinel-1
images were all acquired within the time span of imagery used for
building the framework and may loss independence of cross-compar-
ison to some degree.

Mosaicked images were then pre-processed (multi-looked, radio-
metric terrain corrected, and geocoded) and co-registered with respect
to the image acquired on April 3rd, 2016, which is the image with the
earliest acquisition date. Note that in this study we multi-looked the
images to 500 m of spatial resolution to fit the MODIS reference dataset.
Image mosaic and pre-processing procedure were all performed using
GAMMA software (Werner et al., 2000).

2.2. MODIS surface reflectance data and yearly water mask

The MODIS spectro-radiometer onboard the Terra and Aqua sa-
tellite, launched in 1999 and 2002, respectively, acquires Earth surface
radiances in 36 spectral bands. (https://modis.gsfc.nasa.gov/). MODIS
data is the only dataset that has long temporal coverage starting from
2000 and has high temporal resolution as well as high spectral re-
solution (36 bands). Since we would like to investigate the skills of the
proposed framework with more reference data as possible as it can to
have more robust cross-comparison results, MODIS data was used as
reference data despite its relatively coarse spatial resolution. In fact,
MODIS data has been used for monitoring and long-term analysis of
inundation extents in many previous studies due to its high temporal
resolution (Frappart et al., 2018; Gumma et al., 2014; Huang et al.,
2014; Islam et al., 2010; Normandin et al., 2018; Sakamoto et al., 2007,
2009) in spite of the cloud cover issue (Huang et al., 2013, 2014).

Earthexplorer website

In this study, tile H28V07 of MODIS products of MOD09A1 and
MOD44W were downloaded from the United States Geological Survey
(USGS)
(https://earthexplorer.usgs.gov/).
MOD09A1 is surface reflectance data derived from Terra satellite raw
radiance measurements. It includes surface spectral reflectance of band
1 to band 7 at 500 m spatial resolution with atmospheric conditions,
including gasses, aerosols, and Rayleigh scattering, being corrected. For
each pixel, the best surface reflectance data during 8-day period was
selected based on criteria of cloud and solar zenith. Here, MOD09A1
images of over a decade from 2003 to 2015 and January to July in 2019
at 500 m spatial resolution were used as cross-comparison reference
dataset.

MOD44W is a 250 m resolution water mask product which is
available from 2000 to 2015. Since year 2015 is the year with the
minimum inundation extent in the TSL floodplain area in about the last
two decades (Frappart et al., 2018), the MOD44W water mask in 2015
was adopted as permanent water body mask when building the fra-
mework. This is to avoid the influence of surface roughness change-
induced intensity variation over permanent water body on the REOF
analysis results (see Section 3.1 for detail).

2.3. MERIT DEM

MERIT DEM (Yamazaki et al., 2017) is a global DEM with respect to
Earth Gravitational Model 1996 (EGM96) with 3 arc-second spatial
resolution (about 90 m at the equator) with multiple errors being re-
moved. The baseline DEMs include the 3 arc-second spatial resolution
Shuttle Radar Topography Mission DEM of (SRTM3 DEM) and the
Advanced land observing satellite World 3D-30 m DEM (AW3D-30 m
DEM), in the region of 60° S to 60° N and 60° N to 90° N, respectively.

The unobserved gaps in both SRTM3 and AW3D-30 m DEMs are filled
with the Viewfinder Panoramas DEM. The NASA Ice, Cloud, and land
Elevation Satellite (ICESat) laser altimetry global land surface elevation
data (GLAH14) is used as the reference ground elevation for DEM bias
estimation. DEM errors due to forest canopy are estimated with the use
of University of Maryland Landsat forest cover data (Hansen et al.,
2013) and NASA global forest height data (Simard et al., 2011). For
more detail, please refer to Yamazaki et al. (2017). In this study, the
DEM was multi-looked to spatial resolutions of 500 m as preprocessed
Sentinel-1 GRDH images.

2.4. Jason altimetry-derived and in-situ water levels at TSL

In this study, we used the TSL water levels from two data sources,
including Jason series satellite altimetry and in-situ gauge at Kampong
Luong. Jason series altimetry are the successors of the Topex/Poseidon
(T/P). The satellite series consist of Jason-1, Jason-2 and Jason-3,
launched on December 7th, 2001, June 20th, 2008 and January 17th,
2016, respectively. The series of missions are under the cooperation of
the NASA and Centre National d'Etudes Spatiales (CNES), with addi-
tional partnership of
the National Oceanic and Atmospheric
Administration (NOAA), and EUropean organization for the exploita-
tion of METeorological SATellites (EUMETSAT) for Jason-2 and Jason-
3. As the series of satellite maintain the same orbit configuration as T/P,
they continuously provide highly accurate altimetry data with an about
10-day repeat cycle and allow a long-term inland water level mon-
In this study, we used 20-Hz ICE-retracked ranges from
itoring.
Geophysical Data Record (GDR) E and D for Jason-1 and Jason-2/-3,
respectively, to extract water levels at Virtual Station (VS) at the TSL.
Outliers in each cycle of measurements were removed (Okeowo et al.,
2017). Biases between water level time series of different Jason mis-
sions were calculated based on the difference of mean water level time
series during overlapped period between missions and were aligned
with those of Jason-1. The concatenated Jason-1/-2/-3 water levels
consist of Jason-1 data from cycle 1 to cycle 238, Jason-2 data from
cycle 1 to cycle 280, and Jason-3 data of cycle 1 to cycle 106 and are
with respect to World Geodetic System 1984 (WGS84) ellipsoid. In-situ
water levels at Kampong Luong with respect to local zero gauge up to
2016 were provided by the Asian Disaster Preparedness Center (ADPC)
and were treated as in-situ water levels of the TSL. Locations of Jason
satellites ground track and VS and in-situ gauge are shown in Fig. 2(a).
Fig. 2(b) shows the time series of altimetry-derived and in-situ water
levels at the TSL up to 2016. Bias between altimetry-derived and in-situ
water levels is 14.53 m. By shifting altimetry-derived time series toward
in-situ time series allows us to obtain accuracy (root mean square error,
RMSE) of Jason-1/-2/-3 concatenated altimetry-derive TSL water le-
vels, which is of 0.43 m with high temporal correlation of 0.99. On the
other hand, in-situ TSL levels from January to July of 2019 were also
used for cross-comparison of forecasted inundation extents.

2.5. ENSO index – MEI

The second version of Multivariate ENSO Index (MEI) (Wolter and
Timlin, 1993, 1998, 2011) used in this study was processed, organized
and distributed by Physical Sciences Division of NOAA Earth System
Research Laboratory (ESRL)
(https://www.esrl.noaa.gov/psd/enso/
mei/). It uses 5 variables, including sea level pressure, sea surface
temperature, surface zonal and meridional winds, and outgoing long-
wave radiation, to generate time series of ENSO conditions since 1979.
The sea surface temperature, sea level pressure, and surface winds are
obtained from the high-quality Japanese 55-year Reanalysis (JRA-55)
(Kobayashi et al., 2015). The outgoing longwave radiations are ob-
tained from NOAA Climate Data Record (CDR) monthly outgoing
longwave radiation product of version 2.2-1. All of data fields are in-
terpolated to 2.5° of grid size. Standardized anomalies of each field are
then computed with respect to the period of 1980–2018. MEI is then

4

C.-H. Chang, et al.

Remote Sensing of Environment 241 (2020) 111732

Fig. 2. (a) Geographical locations of Jason altimetry satellite ground track passing through the TSL and the corresponding VS and in-situ gauge at Kampong Luong,
(b) Jason-1/-2/-3 concatenated altimetry-derived water levels at the TSL and validation with in-situ data.

Fig. 3. Eigenvalues and corresponding sampling errors calculated by the rule of thumb of North et al. (1982) and cumulative percentages of explained variances of
significant modes in the cases of using 500 m spatial resolutions of Sentinel-1A GRDH images as input.

calculated as the leading principal component time series of the EOF of
the standardized anomalies of 5 combined variables within the region
of 30°S – 30°N, 100°E – 70°W, excluding the Atlantic Ocean and land
with latitudinal weighting. Positive MEIs represent El Niño events,
while negative MEIs represent La Niña events.

3. Method

3.1. REOF-based daily inundation extent estimation framework

3.1.1. REOF analysis

The REOF analysis starts from conventional EOF analysis (Lorenz,
1956). Consider X is an array of input data which is p-dimensional time
series data with n observations.

(1)

We can take X as an aggregation of n maps, each map has p pixels;
therefore, each row of X is a map at an acquisition time, while each
column is a time series of values of a pixel from n maps. Since the
essence of EOF analysis is to find the variables that can effectively re-
present the variability of X, a covariance matrix of X need to be formed
first. In this study, we attempt to retrieve temporal variability of X;
therefore, a temporal anomaly array X′ is first calculated by subtracting
temporal average array

from X

where each column of

is a column vector whose elements have the

(2)

5

=×Xxxxxxxxxxnpppnnnp1,11,22,12,21,2,,1,2,X=×××XXXnpnpnpXC.-H. Chang, et al.

Remote Sensing of Environment 241 (2020) 111732

same value that is the average value of elements in the corresponding
column in X.

Then a p-by-p covariance matrix R of input data X can be obtained

by

(3)

The covariance matrix R here describes the temporal variability of X
as its derivation adopts temporal anomalies of X. Then an p-by-p array U
whose column vectors are eigenvectors of R and a p-by-p diagonal array
Λ whose elements are corresponding eigenvalues λ that can be calcu-
lated by solving eigenvalue problem of

(4)

Each eigenvector is a unit vector in p-dimensional space, pointing to
the direction where X has significant variances. Each column j of U,
where j can be from 1 to p, is also called a mode of eigenvector which
can be plotted as a map, representing the pattern of spatial variability of
X, that is Spatial Mode (SM). The eigenvector array U is an orthogonal
array that is UTU = UUT = I, meaning that eigenvectors are un-
correlated (orthogonal) to each other over space.

How each mode of SM evolves in time can be determined by pro-

jecting X onto it

(5)

where each column of Z is a n-dimensional vector representing time
series of evolution of corresponding SM, that is Temporal Principal
Component (TPC), which is uncorrelated (orthogonal) in time. Each
row of Z represents a time epoch, while each column corresponds to a
mode of SM. The explained variance of each mode is the variances of
columns of Z. Columns of U and Z, which are SMs and TPCs, respec-
tively, are sorted by corresponding explained variances. Hereafter, the
sorted U and Z are simply called U′ and Z′. Therefore, the first column of
U′ and Z′ is the SM that explains the maximum extent of variability in X
(called mode-1), while the second-column one explains the second most
variability (called mode-2), so on so forth. Then by using Z′ and U′,
input data at specific acquisition time, noted as X(t) can be synthesized
through linear combination as follow if k = p

(6)

where z′t, j is a scalar that is the element of the mode-j TPC at time
epoch t and u′j is the mode-j SM. Such process is called synthesis. If
k = m < p, it is called truncated synthesis, which is often our primary
motivation when applying EOF analysis (Wilks, 2011). Since these
modes of SMs and TPCs from conventional EOF are orthogonal to each
other, difficulty can be raised if ones are interested in physically in-
terpreting SMs and corresponding TPCs as nature phenomena which are
rarely mutually independent.

REOF analysis, on the other hand, is able to relieve the orthogon-
ality constraint of EOF, and improves physical interpretability of SMs
and TPCs (Hannachi et al., 2006, 2007; Lian and Chen, 2012). Since we
are associating TPCs with altimetry-derived water levels, which is a
way of physical interpretation (will be explained later in Section 3.1.2),
REOF analysis is applied. Other advantages of REOF analysis such as
the ability to avoid unphysical dipole-like pattern from EOF analysis
and simplify spatial structures while retaining robust pattern have been
mentioned by several previous studies (Cheng et al., 1995; Dommenget
and Latif, 2002; Hannachi et al., 2006; Houghton and Tourre, 1992).
REOF analysis is based on rotation of SMs with linear transformation of
a truncated m subset of U′

where
is array whose column vectors are modes of Rotated SMs
(RSMs) and T is a rotation matrix. The number of modes to be truncated
m is arbitrary which typically are the number of leading EOF modes and

(7)

6

F
O
E
R
f
o
s
t
l
u
s
e
r

r
e
t
l
a
n
a
c
h
c
i
h
w

,
L
S
T
e
h
t

r
e
v
o

s
e
i
t
i
s
n
e
t
n
i

f
o

e
g
n
a
h
c

e
h
T

.
s
e
m

i
t
n
o
i
t
i
s
i
u
q
c
a

t
n
e
r
e
ff
i
d
n
o
m
3
2
w
o
l
e
b
n
o
i
t
a
v
e
l
e
M
E
D
T
I
R
E
M
h
t
i

w
W
S
T
e
h
t
n
i
h
t
i

w
s
e
g
a
m

i

H
D
R
G
A
1
-
l
e
n
i
t
n
e
S

f
o

s
e
l
p
m
a
x
e

e
r
a

)
c
(
o
t

)
a
(

.
4
.
g
i
F

e
l
p
m
a
x
e
n
a

s
i

)
d
(

.
s
i
s
y
l
a
n
a
F
O
E
R
g
n
i
m
r
o
f
r
e
p
e
r
o
f
e
b
s
e
g
a
m

i

A
1
-
l
e
n
i
t
n
e
S
e
h
t
k
s
a
m
o
t
d
e
i
l
p
p
a
s
a
w
d
n
a
k
s
a
m
y
d
o
b
r
e
t
a
w

t
n
e
n
a
m
r
e
p
s
a
d
e
r
e
d
i
s
n
o
c

s
a
w
5
1
0
2
f
o
k
s
a
m

r
e
t
a
w
W
4
4
D
O
M

,
e
r
o
f
e
r
e
h
T

.

n
e
e
s
y
l
r
a
e
l
c

e
b
n
a
c

,
s
i
s
y
l
a
n
a

.

6
1
0
2

,

d
r
3

l
i
r
p
A
n
o

d
e
r
i
u
q
c
a

s
a
w
h
c
i
h
w

,
s
e
g
a
m

i

h
c
u
s

f
o

=×××RXXppTpnnp=××××RUUpppppppp=×××ZXUnpnppp=+==XtzuXtn();1,2,,jktjj1,=×××UUTpmpmmmUC.-H. Chang, et al.

Remote Sensing of Environment 241 (2020) 111732

Fig. 5. Mode-1 to mode-4 RSMs (top), and corresponding RTPCs (bottom) of input multi-temporal stack of Sentinel-1 GRDH intensity images at 500 m spatial
resolution. The percentages of explained variance from mode-1 to mode-4 are 26.77%, 21.54%, 14.91%, and 9.52%, respectively.

Fig. 6. Polynomial regression models between altimetry-derived water levels w.r.t. WGS84 ellipsoid at the TSL and the mode-1 to mode-4 RTPCs of Sentinel-1 GRDH
intensity images at 500 m spatial resolution.

can be selected based on some truncation criteria (Wilks, 2011). Here,
the “rule of thumb” of North et al. (1982) was used to select significant
modes for truncation. The differences between eigenvalue of a mode
and its adjacent mode need to be at least the sampling error for a mode
to be significant. The sampling errors of eigenvalues were first calcu-
lated by

where δλ is sampling error of a specific eigenvalue λ, and N is number
of samples which is the number of observations. The rule of thumb
results in m = 4, taking 72.7% of total explained variances (see Fig. 3).
Then varimax orthogonal rotation (Kaiser, 1958), the most com-
monly used rotating approach (Richman, 1986), was applied to rotate
U′, which is determined by choosing the elements of T that maximizes
the condition of

(8)

7

=N2C.-H. Chang, et al.

Remote Sensing of Environment 241 (2020) 111732

pixels within the study area excluding those over the permanent water
bodies were adopted into input data X (See Fig. 4). This is to ensure the
spatiotemporal patterns retrieved by the analysis are really from sur-
rounding floodplain. The extraction of pixels was conducted using TSW
boundary shapefile provided by Open Development Cambodia (http://
www.opendevelopmentcambodia.net/maps/downloads/), MERIT DEM,
and MOD44W water mask of 2015. The resulting RSMs and RTPCs are
shown in Fig. 5.

3.1.2. Synthesis of SAR intensity images

Following synthesis formula as Eq. (6), Sentinel-1 GRDH intensity
images, either historical or forecasted ones, can be generated by mul-
tiplying RSMs with corresponding RTPCs at time of the past or future.
To achieve this, estimating temporally varying RTPCs at the given time
is the core. Here, we coupled the resulting RTPCs with the TSL water
levels based on polynomial regression. We applied 1-degree (linear)
polynomial model in the case of mode-1 and mode-2. For mode-3 and
mode-4, 2-degree (quadratic) polynomial model was adopted. The
choice of degree of polynomial models for different modes can be jus-
tified by the corresponding RSMs. As Fig. 5 shows, RSMs of mode-1 and
mode-2 have strong negative signals in the area around the TSL, while
those of mode-3 and mode-4 RSMs are distributed in the area farther
from the TSL. Therefore, RTPCs of mode-1 and mode-2 quickly respond
to the change of TSL water levels, leading to linear pattern in the scatter
plots. RTPCs of mode-3 and mode-4, on the other hand, would respond
when the TSL water surface rises up to certain level. The data dis-
tribution in scatter plot reflects such fact (See Fig. 6). There is relatively
flat and dense data distribution in the scatter plot when the TSL water
level is not high enough. Once the TSL water level reaches certain level,
data distribution shows a rising slope. The fitted polynomial models are
shown in Fig. 6 as well. With given TSL water levels at specific time
epoch, modes of RTPCs can be estimated. Then data at given time can
be synthesized by using Eq. (6).

As the error of REOF-based synthesized SAR intensity can influence
the estimation of inundation extents, we analyzed the difference be-
tween synthesized and original SAR intensity. SAR images adopted for
REOF analysis were used for analysis. The sign of both synthesized and
original SAR intensity of each pixel was first investigated. Fig. 7 shows
time series of the percentages of pixels whose original and synthesized
intensities are both negative, which are nearly 100%, of each SAR
image. It means that when differences between synthesized and original
SAR intensities (subtracting original ones from synthesized ones) are
large positive values, the original SAR intensities would be much
smaller than the synthesized ones. For example, red circles in Fig. 8(c)
mark areas with large positive difference values. These areas match
with areas where original intensities are much smaller than synthesized
ones and may be a source of underestimated inundation extents,
leading to omission errors. These areas have relatively higher

Fig. 7. Percentages of pixels of each SAR image whose original and synthesized
intensity are both negative.

where

is element of

at j-th row and k-th column, and

is row-

(9)

, array

. By replacing U in Eq. (5) with

normalized
whose
column vectors are Rotated TPCs (RTPCs) can be obtained. The varimax
rotation was calculated using the National Center for Atmospheric
Research (NCAR) Common Language (NCL) (NCL, 2019). Since REOF
analysis redistributes the variance represented by the results from
conventional EOF, columns of
, were reordered based on the
and
explained variance of each mode, that is the variance of columns of
.
with each column
The reordered
representing a mode of RSM and RTPC, respectively. By plotting RSMs
as maps and RTPCs as time series, spatiotemporal patterns of input
multi-temporal stack of Sentinel-1 GRDH intensity images can be seen.
Since we performed REOF analysis up to mode 4, we have 4 such time
series of RTPCs and corresponding RSMs. Data synthesis can be fulfilled
by replacing z′t, j and u′j of Eq. (6) with their counterparts in
.
Therefore, by estimate historical or future
, we are able to hindcast
historical data or perform forecasting. This will be covered in the next
section.

is then noted as and

and

and

In this study, areas within the Tonle Sap Watershed (TSW) with
elevation below 23 m was taken as study area (Frappart et al., 2018).
Consider change of surface roughness over the water bodies can increase
the intensities on SAR images and alters the REOF analysis results, only

Fig. 8. Example of (a) original SAR intensity, (b) synthesized SAR intensity, and (c) difference by subtracting (a) from (b) where there are large positive difference
values in high-elevation areas (red circles in (c)), indicating potential underestimation in our estimated inundation extents (omission errors). (For interpretation of
the references to colour in this figure legend, the reader is referred to the web version of this article.)

8

=====pupuuuu11kmjpjkjpjkjkjkkmjk11,41,22,,1,2ujk,Uujk,ujk,UZUZZUZZZUZC.-H. Chang, et al.

Remote Sensing of Environment 241 (2020) 111732

Fig. 9. Example of (a) original SAR intensity, (b) synthesized SAR intensity, and (c) difference by subtracting (a) from (b) where there are large positive difference
values in the areas around the boundary of TSL floodplain (red circles in (c)), indicating potential underestimation in our estimated inundation extents (omission
errors). (For interpretation of the references to colour in this figure legend, the reader is referred to the web version of this article.)

Fig. 10. Example of (a) original SAR intensity, (b) synthesized SAR intensity, and (c) difference by subtracting (a) from (b). Red circles mark areas where there are
really small negative difference values in (c), indicating potential overestimation in our resulting inundation extents (commission errors). (For interpretation of the
references to colour in this figure legend, the reader is referred to the web version of this article.)

Fig. 11. Illustration of how data were clustered into non-inundated (blue) and inundated (red) clusters by K-means algorithm. (a) is an example in the dry season
while (b) is in the wet season. (For interpretation of the references to colour in this figure legend, the reader is referred to the web version of this article.)

elevations. Since the synthesis of SAR intensity is based on coupling
temporal patterns of SAR intensity variations with TSL levels, the SAR
intensity variations over areas with elevation higher than TSL levels
may not be synthesized accurately as they are not necessarily caused by
TSL level variations. Another example shows that there are large po-
sitive difference values in the areas around the boundary of TSL
floodplain (Fig. 9(c)). The original intensities in these areas are much
than the synthesized ones as well and may lead to
smaller

underestimation in our estimated inundation extents. Since the areas
are along the boundary of TSL floodplain, the intensity variations are
possibly related to TSL levels. Hence, the large positive differences in
these areas may be caused by discrepancies between real temporal
patterns and the altimetry-estimated ones.

On the other hand, if the differences are really small negative values,
the synthesized SAR intensities would be much smaller than the original
ones, which may result in overestimated inundation extents and lead to

9

C.-H. Chang, et al.

Remote Sensing of Environment 241 (2020) 111732

Fig. 12. Flowchart of the proposed REOF-based daily inundation extent estimation framework. (*Altimetry-derived TSL levels were used to build regression models
with RTPCs. #Altimetry-derived TSL levels were used for estimated RTPCs.)

commission errors. This can be seen in the red circles in Fig. 10(c) which
are along the boundary of TSL. As these areas are along the boundary of
TSL, the intensity variations are also possibly related to TSL levels. The
differences in these areas may be also due to errors of our altimetry-esti-
mated temporal patterns. For related discussion about skill of framework,
omission errors and commission errors of results, and influence of high-
elevation inundation extent, please refer to Section 4.

Finally, since pixels over permanent water bodies have been ex-
cluded before REOF analysis based on MOD44W water mask of 2015,
long-term temporal averages of intensities over these permanent water
body pixels were calculated and filled back to the synthesized data to
obtain a complete scene, which then can be used to estimate inundation
extents. Note that for Sentinel-1 images used as reference datasets for
cross-comparing with our estimated inundation extents, intensities over
permanent water body pixels were also replaced with long-term tem-
poral averages. It is because intensities over permanent water body can

be enhanced by surface roughness change, which influences the esti-
mation of inundation extents.

3.1.3. K-means clustering inundation extent classification

After successfully synthesizing SAR intensity images, the K-means
clustering algorithm (Lloyd, 1982) was adopted to classify pixels on
synthesized intensity maps into inundated and non-inundated classes
with the aid of MERIT DEM. K-means clustering is one of the most
frequently used clustering techniques which can be easily implemented
and provides relatively high-quality clusters with low computational
effort (Chang et al., 2018; Lin et al., 2013; Tsyganskaya et al., 2018b)
and has been applied on SAR images in recent studies for change de-
tections (Celik, 2009; Zheng et al., 2014) and water pixel segmentation
(Ruzza et al., 2019). The advantage of K-means algorithm is that it is an
unsupervised method which does not acquire additional training data
as “ground truth.” The only necessary input of the algorithm is the user-

10

C.-H. Chang, et al.

Remote Sensing of Environment 241 (2020) 111732

Fig. 13. Illustration on the data used to build regression models between MEIs and TSL levels.

predefined number of classes K. In this study, the number of classes is
K = 2, representing inundated and non-inundated clusters. The algo-
rithm first randomly selects K points as initial “centroids”. Each cen-
troid corresponds to a class. Data are then assigned to the class whose
centroid is the nearest based on squared Euclidean distance until the
sum of squared distance from data to the centroid of each class has been
minimized

data points and centroids. Fig. 11 is an illustration of how data were
clustered by K-means algorithm where x-axis is the normalized MERIT
DEM and y-axis is the normalized synthesized SAR intensities. Fig. 12
shows comprehensive flowchart of the proposed REOF-based daily in-
undation extent estimation framework. For Sentinel-1 images used as
reference datasets for cross-comparison, inundated extents were di-
rectly estimated by K-means algorithm with the same setting.

(10)

3.2. Long-term forecasting of TSL levels using ENSO index

where Gi is the class i, y is the data which belongs to class i and μi is the
centroid of class i. The mean of data assigned to the same class is then
taken as the new centroid. The algorithm iteratively updates centroid
and data may be assigned to from one class to another until centroid
stay unchanged. We used the “K-means” function of MATLAB software
R2017b. The software implements K-means++ algorithm (Arthur and
Vassilvitskii, 2007) to initialize the centroid which has been proved to
have improved running time, robustness, and quality of the final solu-
tion than Lloyd's classical K-means method (Lloyd, 1982). The number
of times to repeat clustering using new initial cluster centroid positions
was set to be 20 (see Supplementary data) to find a lower local minima
to ensure the quality of clustering results. For each of 20 initial cluster
centroid positions, the K-means clustering algorithm iterates up to 100
times to satisfy Eq. (10). The final solution is the one among 20 in-
itializations resulting in the minimum total sum of distance between

Inspired by Frappart et al. (2018) and Räsänen and Kummu (2013),
both pointing out a negative correlation between MRB's flood pulse and
El Niño and La Niña events, linear regression models between MEIs
(Wolter and Timlin, 1993, 1998, 2011) and TSL levels were built for
forecasting of TSL levels with months of lead time. Similar work has
been done by Fok et al. (2018) in which water levels in the MD is
predicted. We performed regression analysis between Jason-2/-3-de-
rived daily TSL levels from 2009 to 2018 and monthly MEIs. First, for
each date that we would like to have forecasted TSL level (hereafter
called forecasting date), its corresponding month was used as reference
month. We then used years of MEIs of each of past 12 months with
respect to the reference month to build linear regression models with
years of the TSL levels of the forecasting dates. For example, if we
would like to forecast the TSL level on June 1st, June would be the
reference month. Therefore, MEIs of June to December of previous

Fig. 14. Biases between datums of TSL water levels, which include WGS84 ellipsoid, local zero gauge of in-situ TSL water level data at Kampong Luong, and EGM96
geoid.

11

minyµyGi2iC.-H. Chang, et al.

Remote Sensing of Environment 241 (2020) 111732

Fig. 15. Flowchart of generation of MODIS-derived inundation extents (* Time span of data could be different depends on the time of estimated inundation extents to
be validated).

Fig. 16. A 2 × 2 confusion matrix, which displays the counts of combinations of framework estimated and observed event pairs.

years and January to May of current years were used. Since we were
building the regression model using Jason-2/-3 daily TSL levels from
2009 to 2018, for each month within June to December, MEIs of pre-
vious years from 2008 to 2017 were used. For each month within
January to May, MEIs of current years from 2009 to 2018 were used.

Fig. 13 shows an illustration of the idea. Hence, there would have 10
MEIs and 10 Jason-2/-3-derived daily TSL levels for each forecasting
date for linear regression analysis. After performing the linear regres-
sion analysis, MEIs of the month with the highest adjusted R2 with
Jason-2/-3-derived daily TSL level on forecasting dates were used as

12

C.-H. Chang, et al.

Remote Sensing of Environment 241 (2020) 111732

Table 1
Climatological monthly averages and STDs of CSI, omission and commission error, overall accuracy, and statistics of altimetry-derived TSL levels including average
level and RMSE. In-situ average TSL levels and STDs are shown as well.

Month

CSI
(%)

Omission error
(%)

Commission error
(%)

Overall accuracy
(%)

Statistics of TSL levels

May

Jun.

Jul.

Aug.

Sep.

Oct.

Nov.

Dec.

Jan.

Feb.

Mar.

Apr.

87.17
±8.45
85.48
±7.50
79.69
±7.52
70.09
±7.27
76.30
±5.68
79.47
±5.03
75.17
±7.15
70.38
±7.61
75.00
±8.81
87.93
±4.06
90.83
±0.79
91.07
±0.58

11.93
±8.64
13.40
±7.66
16.13
±6.98
24.59
±9.05
16.33
±7.68
14.33
±6.61
18.12
±9.51
26.26
±8.16
22.24
±8.63
10.68
±3.64
8.12
±0.86
7.96
±0.56

1.02
±0.15
1.36
±0.74
5.99
±4.00
8.61
±3.89
9.67
±5.30
7.94
±4.88
9.07
±5.10
6.02
±1.94
4.62
±2.39
1.58
±1.06
1.02
±0.14
1.01
±0.20

98.14
±2.28
97.78
±1.66
96.29
±2.03
90.83
±3.76
88.77
±2.86
89.04
±2.23
90.07
±2.02
91.68
±3.17
95.22
±2.78
98.53
±0.75
98.95
±0.21
98.90
±0.30

a Altimetry-derived TSL water levels in this table are with respect to WGS84 ellipsoid.
b In-situ TSL water levels are with respect to local zero gauge.

Altimetry-derived

In-situ

aAverage levels
(m)

RMSE
(m)

bAverage levels
(m)

−13.63
±0.27
−12.97
±0.60
−11.43
±0.97
−9.29
±1.10
−7.62
±1.01
−6.82
±1.06
−7.76
±1.19
−9.46
±1.20
−10.99
±0.92
−12.45
±0.69
−13.31
±0.36
−13.70
±0.30

0.26

0.52

0.68

0.40

0.28

0.38

0.38

0.32

0.52

0.52

0.46

0.36

0.81
±0.21
1.17
±0.53
2.55
±1.02
4.94
±1.27
6.97
±1.10
7.86
±1.16
6.96
±1.24
5.28
±1.16
3.81
±0.96
2.34
±0.79
1.47
±0.50
0.96
±0.29

Fig. 17. (a) Climatological monthly variation of CSIs and RMSEs of altimetry-derived TSL levels. Corresponding scatter plots with fitted linear regression models are
in (b).

input of the regression models to forecast the TSL levels with months of
lead time.

3.3. MODIS-derived inundation maps for cross-comparison

In this study, MODIS-derived inundation maps were used as one of
reference datasets for cross-comparing with our estimated inundation
extents. The approach was originally proposed by Sakamoto et al.
(2007) in studying change of inundation extents in the Lower Mekong.
Normandin et al. (2018) simplified the approach and applied it over the
Mackenzie Delta. The approach uses thresholdings on indices including
the Enhanced Vegetation Index (EVI), Land Surface Water Index
(LSWI), and Difference Value between EVI and LSWI (DVEL), derived
from 8-day composite MODIS images of surface reflectance to classify
pixels into classes of non-flooded, mixture, flooded or permanent water

13

body. Frappart et al. (2018) also applied it for long-term MODIS-based
inundation mapping and analysis over the TSL area which additionally
considers SRTM DEM and altimetry-derived water levels in the TSL to
judge whether a mixture class pixel is inundated or not.

According to Sakamoto et al. (2007), in order to implement the
approach, the EVI, LSWI and DVEL are first calculated. The EVI (Huete
et al., 1997) and LSWI (Xiao et al., 2002) are defined as

(11)

ρNIR

where
reflectance
(841–875 nm, band 2), ρR is the surface reflectance in the red

Infra-Red (NIR)

the Near

surface

is

=×+××+=+EVI2.567.51LSWINIRRNIRRBNIRSWIRNIRSWIRC.-H. Chang, et al.

Remote Sensing of Environment 241 (2020) 111732

Fig. 18. Climatological monthly variation of (a-1) CSIs and altimetry-derived TSL levels, (b-1) omission errors and altimetry-derived TSL levels, and (c-1) CSIs and
omission errors. (a-2) to (c-2) are corresponding scatter plots with fitted regression models.

Fig. 19. Climatological monthly variation of (a-1) commission errors and altimetry-derived TSL levels, and (b-1) CSIs and commission errors. (a-2) to (b-2) are
corresponding scatter plots with fitted regression models.

14

C.-H. Chang, et al.

Remote Sensing of Environment 241 (2020) 111732

amount of difference between their means, which is 2.92 m. Fig. 14
shows biases between datums of TSL water levels including WGS84
ellipsoid, local zero gauge of in-situ water levels at Kampong Luong,
and EGM96 geoid. Finally, a pixel was considered as inundated if it was
classified as (1) flooded pixel or (2) mixture pixel and with elevation
lower than in- situ TSL water level on that date or (3) the pixel is taken
as permanent water bodies. Fig. 15 shows the flowchart summarizes the
whole procedure of generation of MODIS-based inundation maps.

3.4. Framework skill evaluation statistics

Evaluation of framework skill was based on a 2 × 2 confusion
matrix (Kohavi and Provost, 1998) which displays the absolute counts
of combinations of framework estimated and observed event pairs. As
Fig. 16 shows, a and d means the counts of observed flood and non-
flood events that the framework correctly estimates, representing hits
and correct negative, respectively. Contrarily, b and c are the counts of
events that are misestimated, representing false alarms and misses, re-
spectively. It this study, these statistics were based on the number of
pixels by comparing estimated inundation maps with MODIS-derived
ones.

In this study, we used overall accuracy, critical success index (CSI),
omission error and commission error as evaluation indices. The overall
accuracy is the percentage of pixels which were estimated correctly by
our framework over total number of pixels:

(12)

The range of overall accuracy is from 0% to 100%, indicating zero

skill to perfect skill.

CSI (Gilbert, 1884), also called threat score, is the number of cor-
rectly estimated inundated pixels over the number of pixels which are
either really or framework-estimated inundated

(13)

CSI accounts for both false alarms and misses and is considered to be
more complete. It avoids the possible bias in the analysis results caused
by correct negative (d) (Wing et al., 2017). Its value ranges from 0% to
100% where 0% means there is no match between observed and fra-
mework estimation, while 100% means perfect framework skill. CSI is
frequently used as standard validation measure (World Meteorological
Organization, 2017).

Omission error represents the percentage of pixels which are actu-
ally inundated but are not captured by our framework over total
number of actually inundated pixels and can be determined by:

Fig. 20. Climatological monthly variation of omission errors and rapidity of
changes of altimetry-derived TSL levels.

(621–670 nm, band 1), ρB is the surface reflectance in the blue
(459–479 nm, band 3), and ρSWIR is the surface reflectance of the Short-
Wave Infra-Red (SWIR) (1628–1652 nm, band 6). DVEL is defined by
subtracting LSWI from EVI. The pixels with ρB ≥ 0.2 were identified as
cloud-covered and were excluded. Remaining pixels were then classi-
fied into two major classes including (1) non-flooded (EVI > 0.3 or
EVI ≤ 0.3 but DVEL > 0.05) and (2) water-related pixels (EVI ≤ 0.3
and DVEL ≤ 0.05 or EVI ≤ 0.05 and LSWI ≤ 0). The water-related
class comprises 3 sub-classes including flooded pixels when EVI ≤ 0.1,
mixture pixels when 0.1 < EVI ≤ 0.3 and permanent water bodies if
the number of a pixel being classified as either flooded or mixture pixel
exceeds two-thirds of total number of MODIS images. Note that before
calculating these indices, we conducted quality control upon all above-
mentioned bands using the reflectance band quality layer within each
MOD09A1 image. Only those pixels with the highest quality in all
above-mentioned bands were kept for cross-comparison use. This was
to ensure the derived reference dataset has the best quality.

To generate final MODIS-based inundation maps, we used the
MERIT DEM and in-situ water levels of the TSL at Kampong Luong
provided by the ADPC as auxiliary data. We assumed that the TSL
surface is parallel to geoid surface. Hence, the TSL levels with respect to
the geoid would be the same everywhere. As datum of the MERIT DEM
is EGM96 geoid, in-situ water levels of the TSL at Kampong Luong with
respect to EGM96 geoid were generated and were used as in-situ water
levels of the TSL. This was achieved by calculating the means of the
Jason-1/-2/-3 altimetry-derived water levels with respect to EGM96
geoid and the in-situ water levels at the TSL with respect to local zero
gauge, where the latter were then shifted toward the former by the

Fig. 21. (a) Climatological monthly variation of omission errors and RMSEs of altimetry-derived TSL levels. Corresponding scatter plots with fitted linear regression
models are in (b).

15

=++++×Overall accuracyadabcd100(%)=++×aabcCSI100(%)C.-H. Chang, et al.

Remote Sensing of Environment 241 (2020) 111732

(14)

Its value also ranges from 0% to 100% with 0% means perfect skill.

It indicates the extent of misses pixels.

Commission error, on the other hand, is the percentage of frame-
work-estimated inundated pixels which are actually non-inundated
over total number of framework-estimated inundated pixels which can
be calculated as:

Its value also ranges from 0% to 100% with 0% means perfect skill.

It indicates the extent of false alarm pixels.

(15)

4. Results and discussion

4.1. Evaluation and analysis of framework skills using long-term historical
data

Since 2003 is the first complete year of Jason-1 observations and
2015 is the last complete year before acquisition time of Sentinel-1
GRDH used to build the proposed framework, we cross-compared the
inundation extents in the TSL floodplain estimated by our framework
from 2003 to 2015 to provide a long-term evaluation of framework
skill. The spatial resolution of our estimation is 500 m in order to fit the
resolution of MODIS inundation maps derived from MOD09A1 8-day
composite product. For each MOD09A1 image, we first counted the
number of pixels of each date within 8-day period using day-of-year
layer in the product. The dates, which have the greatest number of
pixels in MOD09A1 images within corresponding 8-day periods, were
considered as cross-comparison dates. The inundation extents estimated
by our framework on the cross-comparison dates were evaluated by
corresponding MOD09A1-derived inundation maps. This way was to
mitigate the influence of date differences between our daily estimated
inundation extents and those derived from 8-day composite MOD09A1
images. We adopted CSI, omission error and commission error, and
overall accuracy as evaluation indices of our framework skill. The
evaluation results are listed in Table 1 from climatological monthly
perspective to see the performance of our framework skill in each
month in the order of a “hydrological year”, starting from May to April
of next year (Kummu et al., 2015; Kummu and Sarkkula, 2008). Note
that since number of valid pixels in each of MOD09A1 images are dif-
ferent due to different extents of cloud cover and data missing, the
climatological monthly average and standard deviations (STDs) of CSIs,
overall accuracies, omission errors and commission errors here are
weighted average and STDs, considering total number of valid pixels of
each MOD09A1 image. CSIs indicate that among pixels which were
inundated either on MODIS images or estimated by our framework,
there are 70% to 91% of pixels were both really inundated and suc-
cessfully captured by our framework. CSIs are from 85% to 91% in
relatively dry period of February to June, and are about 75% to 80% in
July, September, October, November and January, but are relatively
low of about 70% in August and December. Omission errors indicate
that there are about 10% to 26% of pixels, which were inundated as
MODIS images show, were missed in our framework estimation. On the
other hand, commission errors indicate that 1% to 10% of our frame-
work-estimated inundated pixels were actually not inundated in MODIS
images. The overall accuracies of our framework indicate that there are
90% to 99% of pixels, considering both inundated and non-inundated,
can be correctly classified.

We further analyzed the connection between variation of our fra-
mework skills of all months and the corresponding altimetry-derived
TSL levels. Table 1 listed the climatological monthly variation of alti-
metry-derived TSL levels with corresponding RMSEs, which are of
0.3 m to 0.7 m. Fig. 17(a) shows the climatological monthly variation of
CSIs, and RMSEs of altimetry-derived TSL levels and corresponding

16

e
h
t

f
o
n
o
i
t
a
t
e
r
p
r
e
t
n
i

r
o
F
(

.
r
u
o
l
o
c
d
n
u
o
r
g
k
c
a
b
s
i
n
e
e
r
g
e
l
i
h
w

,
e
u
l
b
n
i
n
w
o
h
s

e
r
a

s
l
e
v
e
l
L
S
T
n
a
h
t

r
e
w
o
l

s
n
o
i
t
a
v
e
l
e
h
t
i

w
s
a
e
r
A

.
)

w
o
l
l
e
y
(

s
l
e
v
e
l
L
S
T
y
r
a
r
o
p
m
e
t
n
o
c
n
a
h
t

r
e
h
g
i
h
s
n
o
i
t
a
v
e
l
e
h
t
i

w
n
o
i
t
a
d
n
u
n
i

f
o
s
e
l
p
m
a
x
E

.
2
2
.
g
i
F

)
.
e
l
c
i
t
r
a

s
i
h
t

f
o

n
o
i
s
r
e
v

b
e
w
e
h
t

o
t

d
e
r
r
e
f
e
r

s
i

r
e
d
a
e
r

e
h
t

,

d
n
e
g
e
l

e
r
u
g
fi

s
i
h
t

n
i

r
u
o
l
o
c

o
t

s
e
c
n
e
r
e
f
e
r

=+×Omission errorcac100(%)=+×Commission errorbab100(%)C.-H. Chang, et al.

Remote Sensing of Environment 241 (2020) 111732

Table 2
Climatological monthly averages and STDs of CSI, omission and commission error and overall accuracy with high-elevation inundated pixels being excluded. Changes
of framework skills are also listed.

Month

CSI
(%)

Omission error
(%)

Commission error
(%)

Overall accuracy
(%)

Change of framework skills

May

Jun.

Jul.

Aug.

Sep.

Oct.

Nov.

Dec.

Jan.

Feb.

Mar.

Apr.

91.29
±0.45
91.63
±0.77
86.35
±5.48
73.98
±6.24
78.00
±5.30
80.81
±5.03
75.03
±7.17
70.24
±7.61
75.00
±7.17
88.84
±3.58
91.15
±0.50
91.43
±0.49

7.55
±0.50
7.14
±0.54
8.39
±3.27
18.78
±7.39
12.37
±7.70
11.31
±6.39
17.24
±9.63
25.15
±8.25
20.70
±8.58
9.57
±3.11
7.51
±0.61
7.57
±0.49

1.02
±0.15
1.43
±0.75
6.32
±4.28
10.60
±3.77
11.76
±5.76
9.42
±5.52
10.36
±5.08
7.87
±2.30
6.00
±3.14
1.78
±1.35
1.04
±0.20
1.01
±0.20

98.97
±0.16
98.94
±0.24
97.77
±1.50
92.66
±2.85
90.09
±1.92
90.19
±1.31
90.11
±2.07
91.71
±3.16
95.37
±2.77
98.66
±0.62
98.99
±0.11
98.94
±0.24

CSI
(%)

4.12
±8.54
6.15
±7.44
6.66
±5.68
3.88
±3.79
1.71
±2.45
1.34
±2.24
−0.14
±0.90
−0.14
±0.91
0.57
±0.79
0.91
±1.16
0.32
±0.75
0.32
±0.66

Omission error
(%)

Commission error
(%)

Overall accuracy
(%)

−4.38
±8.60
−6.26
±7.59
−7.74
±6.13
−5.81
±4.11
−3.96
±3.51
−3.01
±2.55
−0.88
±0.82
−1.11
±0.71
−1.54
±0.79
−1.11
±1.20
−0.61
±0.76
−0.39
±0.68

0.00
±0.00
0.07
±0.25
0.33
±0.57
1.99
±1.18
2.09
±1.07
1.48
±1.03
1.29
±0.79
1.85
±0.93
1.38
±1.35
0.21
±0.46
0.02
±0.14
0.00
±0.00

0.84
±2.28
1.16
±1.64
1.48
±1.25
1.82
±1.89
1.32
±1.77
1.15
±1.72
0.04
±0.40
0.03
±0.44
0.15
±0.36
0.13
±0.34
0.03
±0.18
0.04
±0.20

Fig. 23. Climatological monthly variations of difference of CSIs and difference of omission errors when excluding inundation with elevation higher than con-
temporary TSL levels (a). Corresponding scatter plot is in (b).

Fig. 24. Climatological monthly variations of difference of CSIs and difference of commission errors when excluding inundation with elevation higher than con-
temporary TSL levels (a). Corresponding scatter plot is in (b).

17

C.-H. Chang, et al.

Remote Sensing of Environment 241 (2020) 111732

fitted linear regression model in Fig. 17(b), where we can see there is no
correlation between CSIs, and RMSEs of altimetry-derived TSL levels
with adjusted R2 of −0.09 in fitted linear regression model. It indicates
that the skills of our inundation extent estimation framework have no
significant connection with such level of errors of altimetry-derived TSL
levels. However, interestingly, when pairing CSIs with TSL levels as in
Fig. 18(a-2), we found a relation with convex quadratic shape between
CSIs and TSL levels. The fitted convex quadratic curve between them
has adjusted R2 of 0.86. Such quadratic shape of connection also in-
dicates that the relation between CSIs and TSL levels changes depends
on the altimetry-derived TSL levels. As Fig. 18(a-2) shows, when alti-
metry-derived TSL levels with respect to WGS84 ellipsoid are lower
than about −9 m, there is a negative correlation between CSIs and TSL
levels. On the contrary, the correlation changes to be positive when TSL
levels with respect to WGS84 ellipsoid exceed −9 m. Such TSL level,
which is in August and December, seems to be a turning point of the
relation between CSIs and altimetry-derived TSL levels. In August and
December, CSIs are also the lowest. Similar pattern can be seen in the
case of omission errors as well. When pairing omission errors with al-
timetry-derived TSL levels, there is a concave quadratic-shape relation
with adjusted R2 of 0.75 between them with the same turning point at
about −9 m of TSL level with respect to WGS84 ellipsoid, as Fig. 18(b-
2) shows. It means that when TSL levels with respect to WGS84 ellip-
soid are below −9 m, there is positive correlation between omission
errors and TSL levels which then changes to a negative correlation
when TSL levels with respect to WGS84 ellipsoid exceeds the turning
point of about −9 m. These facts also imply a strong connection be-
tween CSIs and omission errors. As Fig. 18(c-2) shows, CSIs are nega-
tively correlated with omission errors, resulting in a fitted linear model
with adjusted R2 of 0.91. Commission errors, on the other hand, do not
have obvious quadratic shape of relation with altimetry-derived TSL
levels. The relation between commission errors and TSL levels is more
like a uniformly positive correlation, resulting in fitted linear model
with adjusted R2 of 0.88 shown in Fig. 19(a-2). Furthermore, the con-
nection of CSIs with commission errors is weaker than that with
omission errors as the adjusted R2 of fitted linear model between CSIs
and commission errors is of 0.67 as Fig. 19(b-2) shows, which is lower
than the adjusted R2 of fitted linear model between CSIs and omission
errors. It indicates that the impact of omission errors on the variation of
CSIs is more dominant than commission errors consider all months of
results.

As the relation between variation of omission errors and the TSL
levels has a concave quadratic shape with the highest errors occur when
TSL level with respect to WGS84 ellipsoid is about −9 m in August and
December, we inferred that this “-9 m” of turning point may correspond
to the influence of specific vegetation around the TSL on SAR back-
scatter characteristic. Since Sentinel-1 is a C-band SAR satellite, which
has limited vegetation penetration depth, its radar backscattering may
be dominated by volume scattering if TSL levels are not high enough.
Consequently, intensities over some of the inundated areas may not be
low enough for K-means clustering algorithm to be able to distinguish
them properly from non-inundated areas, leading to the positive cor-
relation between omission errors and TSL levels. By contrast, when TSL
rises above this level, water surface scattering may become dominant
over most of inundated areas, leading to intensities which are low en-
ough for K-means clustering to recognize. Thus, connection between
omission errors and TSL levels turns to a negative correlation. In fact,
according to Van Trung et al. (2013), there is a rapid increase in areas
which change from lowland shrubs to water surfaces in the TSL
floodplain when in-situ TSL level with respect to local zero gauge is
about 5 m, which agrees with the “-9 m” altimetry-derived TSL level
with respect to WGS84 ellipsoid (See Table 1). Fig. 10(b) of Van Trung
et al. (2013) shows the land cover variation model in terms of flooded
areal percentages and the variation of in-situ TSL levels during a flood
pulse, where a “trough” can be clearly seen in the curve of variation of
flooded lowland shrubs when in-situ TSL level exceeds about 5 m.

Table 3
Temporal correlation coefficients and corresponding P-values (in the bracket)
of number of high-elevation inundated pixels with change of CSI, omission
error, commission error, and overall accuracy.

Month Correlation coefficient and P-value of number of high-elevation inundated

pixels with change of

CSI

0.99
0.99
0.92
0.66
0.81
0.83
0.00
−0.52
−0.19
0.82
0.89
0.85

May
Jun.
Jul.
Aug.
Sep.
Oct.
Nov.
Dec.
Jan.
Feb.
Mar.
Apr.

Omission
error

Commission
error

Overall
accuracy

(0.00) −0.99
(0.00) −0.99
(0.00) −0.96
(0.00) −0.72
(0.00) −0.94
(0.00) −0.94
(0.97) −0.44
(0.00)
0.01
(0.18) −0.51
(0.00) −0.91
(0.00) −0.80
(0.00) −0.83

(0.00)
(0.00)
(0.00)
(0.00)
(0.00)
(0.00)
(0.00)
(0.93)
(0.00)
(0.00)
(0.00)
(0.00)

NaN
0.05
0.34
0.62
0.68
0.49
0.46
0.74
0.91
0.46
0.05
NaN

0.97
(NaN)
0.97
(0.74)
0.94
(0.01)
0.92
(0.00)
0.90
(0.00)
0.80
(0.00)
(0.00)
0.09
(0.00) −0.35
0.12
(0.00)
0.51
(0.00)
0.87
(0.72)
0.73
(NaN)

(0.00)
(0.00)
(0.00)
(0.00)
(0.00)
(0.00)
(0.56)
(0.02)
(0.42)
(0.00)
(0.00)
(0.00)

Interestingly, the “trough” of variation of area of flooded lowland
shrubs also crosses the curve of in-situ TSL level at the point when the
latter is about 5 m. Such “trough” may be resulted from the change of
land cover from flooded lowland shrubs to fully inundated water sur-
faces as Van Trung et al. (2013) pointed out. Hence, it indicates that the
flooded lowland shrubs start to completely submerge under water when
in-situ TSL level rises above 5 m, which corresponds to the altimetry-
derived TSL level of −9 m. Besides, the lowland shrub is the dominant
land cover type over the TSL floodplain as Fig. 3(a) of Sáenz et al.
(2016) shows. Arias et al. (2012) also pointed out that shrubland is the
dominant land cover type in the areas, which were flooded 5 to
9 months in average year, in the TSL floodplain. Hence, the relation

Table 4
Climatological monthly averages and STDs of number of high-elevation in-
undated pixels, and changes of CSI, omission, commission error and overall
accuracy. Correlation coefficients and corresponding P-values (in the bracket)
between STDs are also listed.

Month Number of

Change of framework skills

high-elevation
inundated
pixels

CSI
(%)

Omission
error
(%)

Commission
error
(%)

Overall
accuracy
(%)

May

Jun.

Jul.

Aug.

Sep.

Oct.

Nov.

Dec.

Jan.

Feb.

Mar.

Apr.

752.28
±1796.20
914.49
±1347.05
1240.79
±1088.77
2191.74
±1882.02
2432.74
±2110.79
2176.02
±1604.01
850.96
±369.61
884.77
±488.59
650.96
±536.17
199.33
±210.77
58.57
±91.15
49.11
±74.51

Correlation coefficient
between STDs

18

4.12
±8.54
6.15
±7.44
6.66
±5.68
3.88
±3.79
1.71
±2.45
1.34
±2.24
−0.14
±0.90
−0.14
±0.91
0.57
±0.79
0.91
±1.16
0.32
±0.75
0.32
±0.66
0.64 (0.03)

−4.38
±8.60
−6.26
±7.59
−7.74
±6.13
−5.81
±4.11
−3.96
±3.51
−3.01
±2.55
−0.88
±0.82
−1.11
±0.71
−1.54
±0.79
−1.11
±1.20
−0.61
±0.76
−0.39
±0.68
0.70 (0.01)

0.00
±0.00
0.07
±0.25
0.33
±0.57
1.99
±1.18
2.09
±1.07
1.48
±1.03
1.29
±0.79
1.85
±0.93
1.38
±1.35
0.21
±0.46
0.02
±0.14
0.00
±0.00
0.29 (0.36)

0.84
±2.28
1.16
±1.64
1.48
±1.25
1.82
±1.89
1.32
±1.77
1.15
±1.72
0.04
±0.40
0.03
±0.44
0.15
±0.36
0.13
±0.34
0.03
±0.18
0.04
±0.20
0.96
(0.03)

C.-H. Chang, et al.

Remote Sensing of Environment 241 (2020) 111732

Fig. 25. Time series of number of high-elevation inundated pixels of each month within 2013 to 2015.

between the variation of area of flooded lowland shrubs and TSL level
found by Van Trung et al. (2013) may also explain the connection be-
tween both CSIs and omission errors of our results with the TSL levels.
Furthermore, August and December also have peak rapidity of changes
of TSL levels at rising stage and receding stage of flood pulse, respec-
tively, as Fig. 20 shows. It means that August and December are months
when TSL levels experience the most significant change, which also
explains why these two months are the months when radar back-
scattering characteristic changes, leading to a reverse correlation be-
tween omission errors (thus CSIs), and TSL levels. On the other hand,
omission errors have no connection with RMSEs of altimetry-derived
TSL levels, which means that such amount of errors of altimetry-derived
TSL levels does not have significant impact on the inundation extent
estimating skills of our framework (See Fig. 21).

Furthermore, since estimation of inundation extents of our frame-
work is based on the relation between TSL levels and SAR backscatter
intensity changes, inundation caused by regional rainfall, river over-
flow in the areas with higher elevation could not be captured and can

lead to some degree of omission errors as well. Fig. 22 shows example of
inundation occurred in areas higher than contemporary TSL levels in
yellow (hereafter was called high-elevation inundated pixels), while
areas with elevations below contemporary TSL levels are in blue with
background in green. We then performed evaluation of our framework
skills in the case when influence of such high-elevation inundation,
which could be unrelated to the TSL levels, was excluded. This was
achieved by not considering the high-elevation inundated pixels, as
yellow pixels in Fig. 22, when calculating evaluation indices as de-
scribed before. The climatological monthly average and STD of updated
framework skills and the original framework skill and differences be-
tween them (hereafter called change of skills) are listed in Table 2 for
comparison. When excluded high-elevation inundation, omission errors
decrease by from 1% to 8% with CSIs increase by up to 7%, while
commission errors slightly increase by up to 2%. The difference of CSIs
is highly negatively correlated with change of omission errors as there
is a fitted linear regression model with adjusted R2 of 0.90 between
them as Fig. 23 shows. The more the omission errors decrease, the more

19

C.-H. Chang, et al.

Remote Sensing of Environment 241 (2020) 111732

Table 5
Climatological monthly averages and STDs of the number of high-elevation
inundated pixels, differences between elevations of such inundated pixels and
contemporary TSL levels and their products, called extent of influence.

Month

Number of high-elevation
inundated pixels

Difference of
elevations (m)

aExtent of
influence

May
Jun.
Jul.
Aug.
Sep.
Oct.
Nov.
Dec.
Jan.
Feb.
Mar.
Apr.

752.28 ± 1796.20
914.49 ± 1347.05
1240.79 ± 1088.77
2191.74 ± 1882.02
2432.74 ± 2110.79
2176.02 ± 1604.01
850.96 ± 369.61
884.77 ± 488.59
650.96 ± 536.17
199.33 ± 210.77
58.57 ± 91.15
49.11 ± 74.51

9.79 ± 3.56
9.32 ± 3.55
6.76 ± 3.82
3.68 ± 3.32
2.74 ± 2.96
2.30 ± 2.47
1.52 ± 2.35
1.41 ± 2.38
1.92 ± 2.98
3.54 ± 4.13
6.80 ± 4.58
8.09 ± 3.09

7368.42
8526.73
8388.84
8056.12
6671.90
5006.12
1293.16
1249.11
1249.39
706.61
398.49
397.29

a The extent of influence was determined as the product of the average of
number of high-elevation inundated pixels and corresponding average of ele-
vation differences with TSL levels.

the enhancement of CSIs, as can be seen in Fig. 23(b). Change of
commission errors, contrarily, has no connection with change of CSIs
(Fig. 24).

As Table 2 shows there are some of months giving high climatolo-
gical monthly STDs of changes of skills, since STDs represent temporal
variation, we then analyzed the temporal correlation between change of
framework skills, and the number of high-elevation inundated pixels
which are listed in Table 3. In most of months, both changes of CSI and
overall accuracy have significantly strong positive temporal correlation,
while change of omission error has significantly strong negative cor-
relation with the number of high-elevation inundated pixels. It means
that when there are more high-elevation inundated pixels, omission
error will be reduced when such pixels are excluded, leading to more
improvement in CSI and overall accuracy. Change of commission error,
on the other hand, has relatively moderate positive correlation with the
number of high-elevation inundated pixels. This may be caused by the

increase of “false alarm” pixels when excluding high-elevation in-
undated pixels, but the correlation is relatively weak compared with
those of other skills. Temporal correlations in April and May are both
“NaN” because there are no changes of commission error in these two
months when excluding high-elevation inundated pixels, indicating the
existence of such pixels has no influence on commission errors in these
two months (See Table 2.). The analysis results indicated that the
temporal variations and thus STDs of change of skills including CSI,
omission error, and overall accuracy are related to the temporal var-
iation of number of high-elevation inundated pixels to some degree,
while change of commission error is not necessarily influenced by it.

Additionally, in Table 4, the climatological monthly averages and
STDs of number of high-elevation inundated pixels and change of skills,
together with the correlation coefficients and P-values between their
STDs, are shown. The STD of number of high-elevation inundated pixels
were found to have moderate to strong temporal correlation with STDs
of change of CSI, omission error, and overall accuracy, while its tem-
poral correlation with STD of change of commission error is weak. The
analysis results supported what we inferred from Table 3. On the other
hand, we found in Table 4 that there are STDs of number of high-ele-
vation inundated pixels larger than the corresponding averages in
months including February to June. It means there were large temporal
variations of number of such type of pixels for the period of 2003 to
2015 in these months. Fig. 25 shows time series of number of high-
elevation inundated pixels of each different month where more abrupt
peaks in February to June can be observed. This may result from sudden
heavy rainfalls on the acquisition dates of certain MODIS images,
leading to large STDs in these months.

Table 5 listed the climatological monthly average and STD of
number of high-elevation inundated pixels, together with elevation
differences of such pixels with contemporary TSL levels as well as their
extent of influence. Derivation of the extent of influence of high-ele-
vation inundated pixels assumes that if the elevation differences are
larger, the inundation was more likely be caused by factors such as
regional rainfall or river overflow rather than TSL levels. Therefore, we
weighted the climatological monthly average of number of such in-
undated pixels with average elevation differences to provide a reference

Fig. 26. Climatological monthly variations of difference of CSIs, omission errors, and commission errors with extent of influence of high-elevation inundated pixels
with order of (a-1) to (c-1), respectively. Corresponding scatter plots with fitted linear regression models are in (a-2) to (c-2).

20

C.-H. Chang, et al.

Remote Sensing of Environment 241 (2020) 111732

.

n
w
o
h
s

s
i

h
t
n
o
m
h
c
a
e

f
o

h
t
5
1

e
h
t

n
o

t
n
e
t
x
e

n
o
i
t
a
d
n
u
n
I

.
)
2
1
0
2

l
i
r
p
A
o
t

1
1
0
2

y
a
M

(

1
1
0
2

f
o

r
a
e
y

l
a
c
i
g
o
l
o
r
d
y
h

e
h
t

n
i

s
t
n
e
t
x
e

n
o
i
t
a
d
n
u
n
i

f
o

n
o
i
t
u
l
o
v
E

.
7
2

.
g
i
F

21

C.-H. Chang, et al.

Remote Sensing of Environment 241 (2020) 111732

.

n
w
o
h
s

s
i

h
t
n
o
m
h
c
a
e

f
o

h
t
5
1

e
h
t

n
o

t
n
e
t
x
e

n
o
i
t
a
d
n
u
n
I

.
)
6
1
0
2

l
i
r
p
A
o
t

5
1
0
2

y
a
M

(

5
1
0
2

f
o

r
a
e
y

l
a
c
i
g
o
l
o
r
d
y
h

e
h
t

n
i

s
t
n
e
t
x
e

n
o
i
t
a
d
n
u
n
i

f
o

n
o
i
t
u
l
o
v
E

.
8
2

.
g
i
F

22

C.-H. Chang, et al.

Remote Sensing of Environment 241 (2020) 111732

of extents of influence of such high-elevation inundated pixels. We
found that there is significant negative correlation between change of
omission errors when excluding high-elevation inundated pixels and
the extents of influence of high-elevation inundated pixels, leading to
fitted linear regression model with adjusted R2 of 0.91. The significant
negative correlation indicates the stronger the influence of high-ele-
vation inundated pixels, the more the omission errors decrease when
excluding them. On the other hand, change of commission errors has no
connection with extent of influence of high-elevation inundated pixels
with negative adjusted R2. Change of CSIs has significant positive cor-
relation with extent of influence of high-elevation inundated pixels,
resulting in fitted linear regression model with adjusted R2 of 0.78 (See

Fig. 26(a-2) to Fig. 26(c-2)). The strong positive correlation of change
of CSIs with extent of influence of high-elevation inundated pixels in-
dicates that the stronger the influence of high-elevation inundated
pixels, the more the CSIs increase when excluding them. It explains why
there are different degrees of enhancement of our framework skills in
different months, if high-elevation inundated pixels were not con-
sidered.

In Figs. 27 and 28, inundation maps on the 15th of each month in
the hydrological years of 2011 and 2015 (May to April of next year)
were chosen to display the evolutions of inundation extents, as these
two years were the years of extreme scenarios with the maximum and
minimum inundation extents, respectively (Frappart et al., 2018).

Fig. 29. Correlation coefficients between TSL levels of each date and monthly MEIs in the past 12 months.

23

C.-H. Chang, et al.

Remote Sensing of Environment 241 (2020) 111732

Distinct differences in inundation extents between these two hydro-
logical years, especially from July to January, can be seen. Animations
of corresponding daily inundation extents in these two years are in
Supplementary data.

4.2. Evaluation of skills of forecasted inundation extents

In this section, the capacity of our framework in forecasting daily
inundation extents in the TSL floodplain is demonstrated. The results
were evaluated by cross-comparing with MODIS-derived and Sentinel-
1-derived inundation maps. To forecast inundation extents, daily TSL
levels were first forecasted using MEI based on the linear regression
models between them. Due to relatively poor accuracy of Jason-1 al-
timetry-derived water levels over inland water bodies (Ablain et al.,
2010; Martin-Puig et al., 2016), only Jason-2/−3 altimetry-derived
TSL levels were used to build the linear regression model with MEIs.
Time span covers from 2009 to 2018. Fig. 29 shows correlation coef-
ficients between altimetry-derived TSL level of each date and each
month of MEIs of the past 12 months. Strong negative correlations of up
to −0.8 between interannual variation of TSL levels on each date and
MEIs of months ago can be observed. Such negative correlation with
months of lead time when flood pulses in the MRB responds to ENSO
events indicated the teleconnection between them, which have been
proved and discussed in several previous studies (Fok et al., 2018;
Frappart et al., 2018; Räsänen and Kummu, 2013). Here, for each date
that we intend to forecast the TSL levels, the month of MEI which has
the highest adjusted R2 of linear regression models with the TSL levels
was selected as Fig. 30(a) shows with corresponding lead time. The
months of MEI in the past 12 months which have the highest adjusted

R2 of linear regression models with each date of TSL levels are from
May of previous year to June of current year, resulting in lead time
within the range of 2 to 11 months. The lead times of forecasted alti-
metry-derived TSL levels are also the lead times of forecasted inunda-
tion extents. Note that the lead time here did not consider the day of
month since MEI is a monthly index.

Fig. 30(b) shows the highest adjusted R2 value of linear regression
model of each date and corresponding p-value. The highest adjusted R2
values are from about 0.3 to 0.8 with p-values from 0 to 0.05. From late
March to the mid of July, the highest adjusted R2 values have larger
oscillation which may because these months are in the dry period,
hence the influence of ENSO events is not that consistent as wet period.
Despite the lower highest adjusted R2 values within the period, the
correlations are still significant with 95% of confidence interval as p-
values are only up to 0.05. We then forecasted the TSL levels in 2019.
Fig. 31(a) shows cross-comparison of our forecasted TSL levels with in-
situ data from January to July 2019. We can see that overall RMSE of
our forecasting is about 0.78 m with high positive correlation of 0.9.
Note that we were performing long-term forecasting with 2 to
11 months of lead time. Fig. 31(b) shows our forecasted TSL levels in
entire 2019, with clear seasonal variation. The results demonstrated the
possibility to forecast TSL levels using ENSO index.

The forecasted TSL levels were then used as input of our REOF-
based daily inundation extent estimation framework to forecast the
inundation extents over the TSL floodplain. The forecasted inundation
extents were validated by MOD09A1-derived inundation maps based on
CSI, omission error, commission error, and overall accuracy as we did
in Section 4.1. On the other hand, to have an understanding about the
framework skill without the influence of inherent inconsistency be-

Fig. 30. (a) Months of MEIs which have the highest adjusted R2 of linear regression models with the TSL levels on the date when forecasting is performed and
corresponding lead time. The highest adjusted R2 and p-value are shown in (b).

Fig. 31. (a) MEI-forecasted TSL levels with months of lead time which were validated by in-situ data up to July 2019, and (b) MEI-forecasted TSL levels in entire
2019.

24

C.-H. Chang, et al.

Remote Sensing of Environment 241 (2020) 111732

Table 6
Climatological monthly averages and STDs of CSI, omission and commission
error, and overall accuracy of our forecasting in January to July 2019.

Month

Jan.

Feb.

Mar.

Apr.

May

Jun.

Jul.

CSI
(%)

80.25
±2.59
90.28
±0.96
91.53
±0.50
91.30
±0.46
91.00
±0.00
91.44
±0.50
90.91
±0.70

Omission error
(%)

Commission error
(%)

Overall accuracy
(%)

11.50
±3.20
7.36
±0.48
7.23
±0.42
7.30
±0.46
7.70
±0.46
7.55
±0.50
7.43
±1.30

10.50
±1.50
2.72
±0.96
1.00
±0.00
1.00
±0.00
1.00
±0.00
1.00
±0.00
2.66
±0.83

97.00
±0.71
99.00
±0.00
98.85
±0.36
99.00
±0.00
98.81
±0.39
98.81
±0.39
99.00
±0.00

tween radar and optical imagery, inundation extents directly derived
from updated Sentinel-1A/-1B SAR imagery using K-means algorithm
were used as another reference dataset in addition to MODIS-derived
inundation maps.

Table 6 shows cross-comparing results of our forecasted inundation
extents in 2019 from January to July using MODIS imagery as reference
dataset. Monthly average CSIs, omission errors, commission errors, and
overall accuracies are from 80% to 91%, 7% to 11%, 1% to 10%, 97%
to 99%, respectively, during the period of January to July. Table 7
shows monthly averages and STDs of CSI, omission and commission
error, and overall accuracy of our forecasted inundation extent when
excluding high-elevation inundated pixels and the difference compared
with original skills. CSIs, omission errors, commission errors, and
overall accuracy are from 81% to 92%, 6% to 7%, 1% to 13%, and 97%
to 99%, respectively. The differences with original skill are mostly less
than or around 1% except the omission error and commission error in
January.

For cross-comparison with Sentinel-1-derived inundation maps,
climatological monthly averages of CSI, omission error and commission
error and overall accuracy are listed in Table 8. Monthly average CSIs
are from 84% to 98%, omission errors are from 0.5% to about 1%,
commission errors are from 0.2% to 15%, and overall accuracies are
from 98% to 100%. These statistics were compared with those obtained
by cross-comparing with MODIS-derived inundation maps (For cross-
comparison results with MODIS-derived inundation maps, please refer
to Table 6.). Results show that when cross-comparing with Sentinel-1-

Table 8
Climatological monthly averages and STDs of CSI, omission and commission
error, and overall accuracy of our forecasting in January to July 2019, which
were obtained by cross-comparing with inundation extents directly estimated
from updated Sentinel-1A/-1B SAR imagery with K-means clustering algorithm.

Month

Jan.

Feb.

Mar.

Apr.

May

Jun.

Jul.

CSI
(%)

84.20
±4.02
95.00
±1.41
97.50
±0.84
97.80
±0.45
98.00
±0.71
97.80
±0.84
96.25
±0.96

Omission error
(%)

Commission error
(%)

Overall accuracy
(%)

1.00
±0.00
1.00
±0.00
1.17
±0.41
1.20
±0.45
1.60
±0.89
1.60
±1.14
0.50
±0.58

15.20
±4.15
4.00
±1.41
1.33
±1.03
1.00
±0.00
0.20
±0.45
0.20
±0.45
3.00
±1.41

97.80
±0.84
99.50
±0.58
100.00
±0.00
100.00
±0.00
100.00
±0.00
100.00
±0.00
99.75
±0.50

derived inundation maps, omission errors are much lower than com-
paring with MODIS-derived ones, while commission errors are of the
same level except the relatively higher value in January. These may
lead to slightly higher CSIs and overall accuracies. The much lower
omission errors may be because of the fact that Sentinel-1-derived in-
undation maps were used as reference dataset for cross-comparison.
Since the framework we proposed is based on Sentinel-1 SAR imagery,
both can be influenced by limited vegetation-penetrating capacity of C-
band signal which would lead to similar extent of underestimation, and
thus omission errors of the inundation extents estimated by our fra-
mework were reduced. Vegetation-penetrating capacity is also a main
inherent difference between SAR imagery and optical imagery. By using
Sentinel-1-derived inundation maps as reference data for cross-com-
parison instead of MODIS-derived ones, impact of such inherent dif-
ference on cross-comparison results were mitigated.

By using MEI-forecasted altimetry-derived TSL levels

(See
Fig. 31(b)) and the REOF-based inundation extent estimation frame-
work, forecasted inundation extents from January 1st to December 31st
of 2019 were estimated. Fig. 32 shows the forecasted inundation ex-
tents on the 15th day of each month in 2019, displaying the evolution
of
inundation extent from long-term forecasting perspective with
months of lead time. Animation of corresponding daily inundation ex-
tents can be seen in Supplementary data. Consider the huge impact of
inundation extent over the TSL floodplain on local fishery, livelihoods,

Table 7
Climatological monthly averages and STDs of CSI, omission and commission error, and overall accuracy of our forecasting in January to July 2019 with high-
elevation inundated pixels being excluded. Changes of framework skills are also listed.

Month

CSI
(%)

Omission error
(%)

Commission error
(%)

Overall accuracy
(%)

Change of framework skills

Jan.

Feb.

Mar.

Apr.

May

Jun.

Jul.

81.50
±2.18
90.91
±0.79
91.53
±0.50
91.30
±0.46
91.19
±0.34
92.00
±0.00
91.77
±0.42

7.00
±1.58
6.27
±0.45
7.00
±0.00
7.00
±0.00
7.22
±0.42
7.25
±0.43
6.04
±0.71

13.25
±1.48
3.44
±1.23
1.00
±0.00
1.00
±0.00
1.00
±0.00
1.00
±0.00
2.66
±0.83

CSI
(%)

1.25
±0.83
0.63
±0.48
0.00
±0.00
0.00
±0.00
0.19
±0.39
0.56
±0.50
0.86
±0.84

97.25
±0.43
99.00
±0.00
98.85
±0.36
99.00
±0.00
98.81
±0.39
98.81
±0.39
99.00
±0.00

25

Omission error
(%)

Commission error
(%)

Overall accuracy
(%)

−4.50
±1.80
−1.09
±0.79
−0.23
±0.42
−0.30
±0.46
−0.48
±0.50
−0.30
±0.46
−1.38
±1.11

2.75
±0.83
0.73
±0.45
0.00
±0.00
0.00
±0.00
0.00
±0.00
0.00
±0.00
0.00
±0.00

0.25
±0.43
0.00
±0.00
0.00
±0.00
0.00
±0.00
0.00
±0.00
0.00
±0.00
0.00
±0.00

C.-H. Chang, et al.

Remote Sensing of Environment 241 (2020) 111732

.

9
1
0
2

n
i

h
t
n
o
m
h
c
a
e

f
o

y
a
d

h
t
5
1

e
h
t

n
o

s
t
n
e
t
x
e

n
o
i
t
a
d
n
u
n
i

d
e
t
s
a
c
e
r
o
F

.
2
3

.
g
i
F

26

C.-H. Chang, et al.

Remote Sensing of Environment 241 (2020) 111732

and economy, the long-term forecasted inundation extent with months
of lead time has potential to help stakeholders make plans on effective
water resource management in advance.

5. Conclusions

In this study, we proposed an innovative REOF-based daily in-
undation extent estimation framework by exploiting multi-temporal
stack of Sentinel-1A SAR intensity images and Jason altimetry-derived
water levels. The framework takes advantage of the physical inter-
pretability of results of REOF analysis, the capacity of cloud penetra-
tion, weather and sunlight independence of SAR imagery, and the short
revisiting time and consistent data acquisition of Sentinel-1 and Jason
altimetry satellites and has features including: (1) daily synthesis of
SAR intensity image and estimation of areal inundation extents of any
time as long as altimetry-derived water level is available; (2) Fully re-
mote sensing-based in which computationally expensive model is not
required; (3) Cloud-free daily inundation extents estimation. The fra-
mework has potential to be applied to the floodplains of other major
river basins such as Amazon River Basin and Congo River Basin as well.
The implementation using SAR imagery from other satellites with dif-
ferent bands of electromagnetic wave (e.g., L-band ALOS) as well as on
SAR imagery with finer spatial resolution is also possible but need more
investigation. In this study, the framework was implemented to the TSL
floodplain. A method capable of performing long-term TSL level fore-
casting with months of lead time was also proposed to fulfill the fore-
casting capacity of proposed framework.

We first hindcasted historical inundation extents from 2003 to 2015
with the use of historical altimetry-derived TSL levels. The skills of our
framework were first evaluated by cross-comparing hindcasted histor-
ical inundation extents with 8-day composite MODIS-derived inunda-
tion maps. The connection between framework skills and various pos-
sible influential factors, including input altimetry-derived water level
and its RMSE was then analyzed. Based on the evaluation of long-term
hindcasted historical
inundation extents, climatological monthly
average CSIs of our estimated inundation extents are from 70% to 91%
and have significant negative correlation with omission errors. Both
CSIs and omission errors have no significant connection with the level
of RMSEs of altimetry-derived TSL levels in this study. Interestingly,
they have significant connection with altimetry-derived TSL levels.
Since Sentinel-1 is a C-band SAR satellite with limited vegetation-pe-
netrating ability, its radar backscattering characteristics may change
between surface backscattering or volume scattering and specular
scattering depending on TSL levels. Therefore, the band of SAR elec-
tromagnetic wave is important in the proposed framework and should
be selected carefully by taking local vegetation type into account when
implementing. On the other hand, the CSIs increase to 75% to 91%
when excluding high-elevation inundation. It is because our framework
is based on connecting TSL levels with temporal variation of intensities
of Sentinel-1A imagery, high-elevation inundation which may be
caused by regional rainfall or upstream river overbank flooding but not
necessarily caused by TSL level change may not be well captured by our
framework.

In the forecasting case, the forecasted TSL levels in January to July
2019 were used as inputs of the proposed framework to estimate
forecasted inundation extents. The skills of forecasted inundation ex-
tents were evaluated by MODIS-derived inundation maps as well as
Sentinel-1-derived inundation maps. When using MODIS-derived in-
undation maps as reference dataset for cross-comparison, CSIs are from
80% to 91% and increase to 81% to 92% when excluding high-elevation
inundated pixels. On the other hand, when using Sentinel-1-derived
inundation maps as reference dataset for cross-comparison, CSIs are
from 84% to 98%. The improvement of CSIs when cross-comparing
with Sentinel-1-derived inundation maps is probably due to the re-
duction of omission error. Since our framework is based on Sentinel-1
SAR imagery, there is omission error caused by inherent difference

between MODIS optical imagery and Sentinel-1 SAR imagery as the
latter can be influenced by limited vegetation penetrating capacity.
When using Sentinel-1-derived inundation maps as reference dataset,
influence of such inherent difference between data sources was miti-
gated. However, since only data from January to July of 2019 were
used for cross-comparison in forecasting case, more data is needed to
have a more comprehensive understanding about the framework skill in
the future.

Consider potential future anthropogenic and climatic impact on
hydrology of MRB and TSL, daily inundation maps over TSL floodplain
estimated by our framework, especially the forecasted ones, can have
great contribution to authorities concerned for meaningful water re-
source management, socioeconomic impact evaluation, and decision-
making purpose without dependence on upstream countries. Since our
forecast of inundation extents is based on forecast of TSL levels, which
currently only considers influence of ENSO, further investigation is
needed to address the impact of anthropogenic factor such as the con-
struction of upstream dams to have a more comprehensive under-
standing about how future TSL levels and TSL floodplain inundation
extents will evolve.

CRediT authorship contribution statement

-

review & editing. Hyongki

Chi-Hung Chang: Conceptualization, Methodology, Software,
Validation, Formal analysis, Investigation, Data curation, Writing -
original draft, Writing
Lee:
Conceptualization, Methodology, Resources, Writing - review & editing,
Supervision, Project administration, Funding acquisition. Donghwan
Kim: Investigation, Data curation, Writing - review & editing. Euiho
Hwang: Writing - review & editing. Faisal Hossain: Writing - review &
editing. Farrukh Chishtie: Resources, Writing - review & editing.
Susantha Jayasinghe: Resources, Writing - review & editing. Senaka
Basnayake: Resources, Writing - review & editing.

Acknowledgement

Supply

This study is partly supported by NASA's Applied Sciences Program
for GEOGLOWS (80NSSC18K0423) and SERVIR (80NSSC20K0152),
and by the Ministry of Environment, South Korea, under the Demand
Responsive Water
number
Service
2019002650004). We would like to acknowledge Archiving, Validation
and Interpretation of Satellite Oceanographic data (AVISO) and ESA
Copernicus Open Access Hub, Alaska Satellite Facility for providing
Jason satellite altimetry data and Sentinel-1 data, respectively. We
would also like to thank Dr. Dai Yamazaki and Dr. Igor Klein for fruitful
discussions about inundations in lower Mekong.

Program (Grant

Declaration of competing interest

The authors declare that they have no known competing financial
interests or personal relationships that could have appeared to influ-
ence the work reported in this paper.

Appendix A. Supplementary data

Supplementary data to this article can be found online at https://

doi.org/10.1016/j.rse.2020.111732.

References

Ablain, M., Philipps, S., Picot, N., Bronner, E., 2010. Jason-2 global statistical assessment
and cross-calibration with Jason-1. Mar. Geod. 33, 162–185. https://doi.org/10.
1080/01490419.2010.487805.

Adamson, P., 2006. Hydrological and water resources modelling in the Mekong region: a
brief overview. In: Explor. Water Futures Together Mekong Reg. Waters Dialogue, pp.
69–74.

Ahamed, A., Bolten, J.D., 2017. A MODIS-based automated flood monitoring system for

27

C.-H. Chang, et al.

Remote Sensing of Environment 241 (2020) 111732

southeast asia. Int. J. Appl. Earth Obs. Geoinf. 61, 104–117. https://doi.org/10.
1016/j.jag.2017.05.006.

Ahmad, S.K., Hossain, F., Eldardiry, H., Pavelsky, T.M., 2019. A fusion approach for water
area classification using visible, near infrared and synthetic aperture radar for South
Asian conditions. IEEE Trans. Geosci. Remote Sens. 1–10. https://doi.org/10.1109/
TGRS.2019.2950705.

Amitrano, D., Di Martino, G., Iodice, A., Riccio, D., Ruello, G., 2018. Unsupervised rapid
flood mapping using Sentinel-1 GRD SAR images. IEEE Trans. Geosci. Remote Sens.
56, 3290–3299. https://doi.org/10.1109/TGRS.2018.2797536.

Arias, M.E., Cochrane, T.A., Piman, T., Kummu, M., Caruso, B.S., Killeen, T.J., 2012.
Quantifying changes in flooding and habitats in the Tonle Sap Lake (Cambodia)
caused by water infrastructure development and climate change in the Mekong Basin.
J. Environ. Manag. 112, 53–66. https://doi.org/10.1016/j.jenvman.2012.07.003.

Arthur, D., Vassilvitskii, S., 2007. K-means++: The advantages of careful seeding. In:

Proc. 18th Annu. ACM-SIAM Symp. on Discrete Algorithms. Philadelphia, PA, U.S, pp.
1027–1035. https://doi.org/10.1145/1283383.1283494.

Dommenget, D., Latif, M., 2002. A cautionary note on the interpretation of EOFs. J. Clim.

15, 216–225. https://doi.org/10.1175/1520-0442(2002)015<0216:ACNOTI>2.0.
CO;2.

Fayne, J.V., Bolten, J.D., Doyle, C.S., Fuhrmann, S., Rice, M.T., Houser, P.R., Lakshmi, V.,
2017. Flood mapping in the lower Mekong River Basin using daily MODIS observa-
tions. Int. J. Remote Sens. 38, 1737–1757. https://doi.org/10.1080/01431161.2017.
1285503.

Fisheries Administration of Cambodia, 2011. Status of the Fishery Sector in 2011 and

Targets for 2012. Fisheries Administration, Phnom Penh, Cambodia.

Fok, S.H., He, Q., Chun, P.K., Zhou, Z., Chu, T., 2018. Application of ENSO and drought
indices for water level reconstruction and prediction: a case study in the lower
Mekong River Estuary. Water 10, 58. https://doi.org/10.3390/w10010058.

Frappart, F., Biancamaria, S., Normandin, C., Blarel, F., Bourrel, L., Aumont, M., Azemar,
P., Vu, P.L., Le Toan, T., Lubac, B., Darrozes, J., 2018. Influence of recent climatic
events on the surface water storage of the Tonle Sap Lake. Sci. Total Environ. 636,
1520–1533. https://doi.org/10.1016/j.scitotenv.2018.04.326.

Baran, E., Coates, D., 2000. Hydro-biological models for water management in the

Fredén, F., 2011. Impacts of Dams on Lowland Agriculture in the Mekong River

Mekong River. In: Proc. Workshop on Hydrologic and Environmental Modelling in
Mekong Basin. Phnom Penh, Cambodia, pp. 328–334.

Catchment. Lunds Universitets Naturgeografiska Institution-Seminarieuppsatser,
Lund, Sweden.

Biancamaria, S., Hossain, F., Lettenmaier, D.P., 2011. Forecasting transboundary river

water elevations from space. Geophys. Res. Lett. 38, 1–5. https://doi.org/10.1029/
2011GL047290.

Biancamaria, S., Frappart, F., Leleu, A.S., Marieu, V., Blumstein, D., Desjonquères, J.D.,
Boy, F., Sottolichio, A., Valle-Levinson, A., 2017. Satellite radar altimetry water
elevations performance over a 200 m wide river: evaluation over the Garonne River.
Adv. Sp. Res. 59, 128–146. https://doi.org/10.1016/j.asr.2016.10.008.

Bioresita, F., Puissant, A., Stumpf, A., Malet, J.P., 2018. A method for automatic and rapid
mapping of water surfaces from Sentinel-1 imagery. Remote Sens. 10, 217. https://
doi.org/10.3390/rs10020217.

Boergens, E., Dettmering, D., Seitz, F., 2019. Observing water level extremes in the

Mekong River Basin: the benefit of long-repeat orbit missions in a multi-mission sa-
tellite altimetry approach. J. Hydrol. 570, 463–472. https://doi.org/10.1016/j.
jhydrol.2018.12.041.

Bracher, A., Taylor, M.H., Taylor, B., Dinter, T., Röttgers, R., Steinmetz, F., 2015. Using
empirical orthogonal functions derived from remote-sensing reflectance for the pre-
diction of phytoplankton pigment concentrations. Ocean Sci. 11, 139–158. https://
doi.org/10.5194/os-11-139-2015.

Gilbert, G.K., 1884. Finley’s tornado predictions. Am. Meteorol. J. 1, 166–172.
Gumma, M.K., Thenkabail, P.S., Maunahan, A., Islam, S., Nelson, A., 2014. Mapping

seasonal rice cropland extent and area in the high cropping intensity environment of
Bangladesh using MODIS 500m data for the year 2010. ISPRS J. Photogramm.
Remote Sens. 91, 98–113. https://doi.org/10.1016/j.isprsjprs.2014.02.007.

Halls, A.S., Lieng, S., Ngor, P., Tun, P., 2008. New research reveals ecological insights into

dai fishery. Catch Cult 13, 8–12.

Hannachi, A., Jolliffe, I.T., Stephenson, D.B., Trendafilov, N., 2006. In search of simple
structures in climate: simplifying EOFs. Int. J. Climatol. 26, 7–28. https://doi.org/10.
1002/joc.1243.

Hannachi, A., Jolliffe, I.T., Stephenson, D.B., 2007. Empirical orthogonal functions and
related techniques in atmospheric science: a review. Int. J. Climatol. 27, 1119–1152.
https://doi.org/10.1002/joc.1499.

Hansen, M.C., Potapov, P.V., Moore, R., Hancher, M., Turubanova, S.A., Tyukavina, A.,

Thau, D., Stehman, S.V., Goetz, S.J., Loveland, T.R., Kommareddy, A., Egorov, A.,
Chini, L., Justice, C.O., Townshend, J.R.G., 2013. High-resolution global maps of
21st-century forest cover change. Science 342, 850–853. https://doi.org/10.1126/
science.1244693.

Brêda, J.P.L.F., Paiva, R.C.D., Bravo, J.M., Passaia, O.A., Moreira, D.M., 2019.

Hortle, K.G., 2009. Fisheries of the Mekong River basin. In: Campbell, I.C. (Ed.), The

Assimilation of satellite altimetry data for effective river bathymetry. Water Resour.
Res. https://doi.org/10.1029/2018wr024010.

Busker, T., De Roo, A., Gelati, E., Schwatke, C., Adamovic, M., Bisselink, B., Pekel, J.F.,
Cottam, A., 2019. A global lake and reservoir volume analysis using a surface water
dataset and satellite altimetry. Hydrol. Earth Syst. Sci. 23, 669–690. https://doi.org/
10.5194/hess-23-669-2019.

Campbell, I.C., Poole, C., Giesen, W., Valbo-Jorgensen, J., 2006. Species diversity and
ecology of Tonle Sap Great Lake, Cambodia. Aquat. Sci. 68, 355–373. https://doi.
org/10.1007/s00027-006-0855-0.

Campbell, I.C., Say, S., Beardall, J., 2009. Tonle Sap Lake, the heart of the Lower Mekong.

In: Campbell, I.C. (Ed.), The Mekong: Biophysical Environment of an International
River Basin, Aquatic Ecology. Academic Press, San Diego, CA, U.S. pp, pp. 251–272.
https://doi.org/10.1016/B978-0-12-374026-7.00010-3.

Cazals, C., Rapinel, S., Frison, P.L., Bonis, A., Mercier, G., Mallet, C., Corgne, S., Rudant,
J.P., 2016. Mapping and characterization of hydrological dynamics in a coastal marsh
using high temporal resolution Sentinel-1A images. Remote Sens. 8, 570. https://doi.
org/10.3390/rs8070570.

Celik, T., 2009. Unsupervised change detection in satellite images using principal com-
ponent analysis and k-means clustering. IEEE Geosci. Remote Sens. Lett. 6 (4),
772–776. https://doi.org/10.1109/LGRS.2009.2025059.

CFE-DMHA, 2017. Cambodia Disaster Management Reference Handbook. CFE-DMHA,

Joint Base Pearl Harbor – Hickam, Hawaii, U.S.

Chang, C.-H., Kuo, C.-Y., Shum, C.K., Yi, Y., Rateb, A., 2016. Global surface and sub-

surface geostrophic currents from multi-mission satellite altimetry and hydrographic
data, 1996-2011. J. Mar. Sci. Technol. 24, 1181–1193. https://doi.org/10.6119/
JMST-016-1026-7.

Chang, M.J., Chang, H.K., Chen, Y.C., Lin, G.F., Chen, P.A., Lai, J.S., Tan, Y.C., 2018. A
support vector machine forecasting model for typhoon flood inundation mapping and
early flood warning systems. Water (Switzerland) 10. https://doi.org/10.3390/
w10121734.

Chang, C.-H., Lee, H., Hossain, F., Basnayake, S., Jayasinghe, S., Chishtie, F., Saah, D., Yu,
H., Sothea, K., Du Bui, D., 2019. A model-aided satellite-altimetry-based flood fore-
casting system for the Mekong River. Environ. Model. Softw. 112, 112–127. https://
doi.org/10.1016/j.envsoft.2018.11.017.

Cheng, X., Nitsche, G., Wallace, J.M., 1995. Robustness of low-frequency circulation

patterns derived from EOF and rotated EOF analyses. J. Clim. 8, 1709–1713. https://
doi.org/10.1175/1520-0442(1995)008<1709:ROLFCP>2.0.CO;2.

Church, J.A., White, N.J., Coleman, R., Lambeck, K., Mitrovica, J.X., 2004. Estimates of
the regional distribution of sea level rise over the 1950–2000 Period. J. Clim. 17,
2609–2625. https://doi.org/10.1175/1520-0442(2004)017<2609:EOTRDO>2.0.
CO;2.

Crétaux, J.-F., Bergé-Nguyen, M., Leblanc, M., Abarca del Río, R., Delclaux, F., Mognard,
N., Lion, C., Pandey, R.K., Tweed, S., Calmant, S., Maisongrande, P., 2011. Flood
mapping infrarred from remote sensing data. Int. Water Technol. J. 1, 46–58.
Da Silva, J.S., Seyler, F., Calmant, S., Rotunno Filho, O.C., Roux, E., Araújo, A.A.M.,

Guyot, J.L., 2012. Water level dynamics of Amazon wetlands at the watershed scale
by satellite altimetry. Int. J. Remote Sens. 33, 3323–3353. https://doi.org/10.1080/
01431161.2010.531914.

Mekong: Biophysical Environment of an International River Basin, Aquatic Ecology.
Academic Press, San Diego, CA, U.S, pp. 197–249. https://doi.org/10.1016/B978-0-
12-374026-7.00009-7.

Hortle, K.G., Lieng, S., Valbo-Jorgensen, J., 2004. An Introduction to Cambodia’s Inland
Fisheries, Mekong Development Series No 4. Mekong River Commission, Phnom
Penh, Cambodia.

Hossain, F., Maswood, M., Siddique-E-Akbor, A.H., Yigzaw, W., Mazumdar, L.C., Ahmed,
T., Hossain, M., Shah-Newaz, S.M., Limaye, A., Lee, H., Pradhan, S., Shrestha, B.,
Bajracahrya, B., Biancamaria, S., Shum, C.K., Turk, F.J., 2014a. A promising radar
altimetry satellite system for operational flood forecasting in flood-prone Bangladesh.
IEEE Geosci. Remote Sens. Mag. 2, 27–36. https://doi.org/10.1109/MGRS.2014.
2345414.

Hossain, F., Siddique-E-Akbor, A.H., Mazumder, L.C., ShahNewaz, S.M., Biancamaria, S.,
Lee, H., Shum, C.K., 2014b. Proof of concept of an altimeter-based river forecasting
system for transboundary flow inside Bangladesh. IEEE J. Sel. Top. Appl. Earth Obs.
Remote Sens. 7, 587–601. https://doi.org/10.1109/JSTARS.2013.2283402.

Houghton, R.W., Tourre, Y.M., 1992. Characteristics of low-frequency sea surface tem-

perature fluctuations in the tropical Atlantic. J. Clim. 5, 765–772. https://doi.org/10.
1175/1520-0442(1992)005<0765:COLFSS>2.0.CO;2.

Huang, C., Chen, Y., Wu, J., 2013. A dem-based modified pixel swapping algorithm for

floodplain inundation mapping at subpixel scale. Int. Geosci. Remote Sens. Symp.
3994–3997. https://doi.org/10.1109/IGARSS.2013.6723708.

Huang, C., Chen, Y., Wu, J., 2014. Mapping spatio-temporal flood inundation dynamics at
large river basin scale using time-series flow data and MODIS imagery. Int. J. Appl.
Earth Obs. Geoinf. 26, 350–362. https://doi.org/10.1016/j.jag.2013.09.002.

Huete, A.R., Liu, H.Q., Batchily, K., van Leeuwen, W., 1997. A comparison of vegetation

indices over a global set of TM images for EOS-MODIS. Remote Sens. Environ. 59,
440–451. https://doi.org/10.1016/S0034-4257(96)00112-5.

Imani, M., Chen, Y., You, R., Lan, W., Kuo, C., Chang, J., Rateb, A., 2017. Spatiotemporal
prediction of satellite altimetry sea level anomalies in the tropical Pacific Ocean. IEEE
Geosci. Remote Sens. Lett. 14, 1126–1130. https://doi.org/10.1109/LGRS.2017.
2699668.

Islam, A.S., Bala, S.K., Haque, M.A., 2010. Flood inundation map of Bangladesh using
MODIS time-series images. J. Flood Risk Manag. 3, 210–222. https://doi.org/10.
1111/j.1753-318X.2010.01074.x.

Jiang, L., Madsen, H., Bauer-Gottwein, P., 2019. Simultaneous calibration of multiple

hydrodynamic model parameters using satellite altimetry observations of water
surface elevation in the Songhua River. Remote Sens. Environ. 225, 229–247. https://
doi.org/10.1016/j.rse.2019.03.014.

Kaiser, H.F., 1958. The varimax criterion for analytic rotation in factor analysis.

Psychometrika 23, 187–200. https://doi.org/10.1007/BF02289233.

Keskinen, M., 2006. The Lake with floating villages: socio-economic analysis of the Tonle

Sap Lake. Int. J. Water Resour. Dev. 22, 463–480. https://doi.org/10.1080/
07900620500482568.

Kim, D., Lee, H., Laraque, A., Tshimanga, R.M., Yuan, T., Jung, H.C., Beighley, E., Chang,
C.-H., 2017. Mapping spatio-temporal water level variations over the central congo
river using palsar scansar and envisat altimetry data. Int. J. Remote Sens. 38,
7021–7040. https://doi.org/10.1080/01431161.2017.1371867.

28

C.-H. Chang, et al.

Remote Sensing of Environment 241 (2020) 111732

Kim, D., Lee, H., Chang, C.-H., Bui, D.D., Jayasinghe, S., Basnayake, S., Chishtie, F.,

Hwang, E., 2019a. Daily River discharge estimation using multi-mission radar alti-
metry data and ensemble learning regression in the lower Mekong River Basin.
Remote Sens. https://doi.org/10.3390/rs11222684.

Kim, D., Yu, H., Lee, H., Beighley, E., Durand, M., Alsdorf, D.E., Hwang, E., 2019b.

Ensemble learning regression for estimating river discharges using satellite altimetry
data: Central Congo River as a test-bed. Remote Sens. Environ. 221, 741–755.
https://doi.org/10.1016/j.rse.2018.12.010.

Klein, I., Dietz, A., Gessner, U., Dech, S., Kuenzer, C., 2015. Results of the Global

WaterPack: a novel product to assess inland water body dynamics on a daily basis.
Remote Sens. Lett. 6, 78–87. https://doi.org/10.1080/2150704X.2014.1002945.
Klein, I., Gessner, U., Dietz, A.J., Kuenzer, C., 2017. Global WaterPack – a 250 m re-

solution dataset revealing the daily dynamics of global inland water bodies. Remote
Sens. Environ. 198, 345–362. https://doi.org/10.1016/j.rse.2017.06.045.

Kobayashi, S., Ota, Y., Harada, Y., Ebita, A., Moriya, M., Onoda, H., Onogi, K., Kamahori,
H., Kobayashi, C., Endo, H., Miyaoka, K., Takahashi, K., 2015. The JRA-55 reanalysis:
general specifications and basic characteristics. J. Meteorol. Soc. Japan. Ser. II 93,
5–48. https://doi.org/10.2151/jmsj.2015-001.

Kohavi, R., Provost, F., 1998. Glossary of terms. Mach. Learn. 30, 271–274. https://doi.

org/10.1023/A:1017181826899.

Kummu, M., Sarkkula, J., 2008. Impact of the Mekong River flow alteration on the Tonle
Sap Flood Pulse. AMBIO A J. Hum. Environ. 37, 185–192. https://doi.org/10.1579/
0044-7447(2008)37[185:IOTMRF]2.0.CO;2.

Kummu, M., Sarkkula, J., Koponen, J., Nikula, J., 2006. Ecosystem management of the

Tonle Sap Lake: an integrated modelling approach. Int. J. Water Resour. Dev. 22,
497–519. https://doi.org/10.1080/07900620500482915.

Kummu, M., Tes, S., Yin, S., Adamson, P., Józsa, J., Koponen, J., Richey, J., Sarkkula, J.,
2015. Water balance analysis for the Tonle Sap Lake–floodplain system. Hydrol.
Process. 29, 5477. https://doi.org/10.1002/hyp.10763.

Lamberts, D., 2006. The Tonle Sap Lake as a productive ecosystem. Int. J. Water Resour.

Dev. 22, 481–495. https://doi.org/10.1080/07900620500482592.

Lamberts, D., Koponen, J., 2008. Flood pulse alterations and productivity of the Tonle Sap
ecosystem: a model for impact assessment. AMBIO A J. Hum. Environ. 37, 178–184.
Lauri, H., de Moel, H., Ward, P.J., Räsänen, T.A., Keskinen, M., Kummu, M., 2012. Future
changes in Mekong River hydrology: impact of climate change and reservoir opera-
tion on discharge. Hydrol. Earth Syst. Sci. 16, 4603–4619. https://doi.org/10.5194/
hess-16-4603-2012.

Lee, H., Beighley, R.E., Alsdorf, D., Jung, H.C., Shum, C.K., Duan, J., Guo, J., Yamazaki,
D., Andreadis, K., 2011. Characterization of terrestrial water dynamics in the Congo
Basin using GRACE and satellite radar altimetry. Remote Sens. Environ. 115,
3530–3538. https://doi.org/10.1016/j.rse.2011.08.015.

Lian, T., Chen, D., 2012. An evaluation of rotated eof analysis and its application to

tropical pacific SST variability. J. Clim. 25, 5361–5373. https://doi.org/10.1175/
JCLI-D-11-00663.1.

Lin, G.F., Lin, H.Y., Chou, Y.C., 2013. Development of a real-time regional-inundation
forecasting model for the inundation warning system. J. Hydroinf. 15, 1391–1407.
https://doi.org/10.2166/hydro.2013.202.

Lin, L., Di, L., Tang, J., Yu, E., Zhang, C., Rahman, M.S., Shrestha, R., Kang, L., 2019.
Improvement and validation of NASA/MODIS NRT global flood mapping. Remote
Sens. 11, 205. https://doi.org/10.3390/rs11020205.

Lloyd, S., 1982. Least squares quantization in PCM. IEEE Trans. Inf. Theory 28, 129–137.

https://doi.org/10.1109/TIT.1982.1056489.

Lorenz, E.N., 1956. Empirical Orthogonal Functions and Statistical Weather Prediction.
Statistical Forecasting Project Scientific Report No. 1. Massachusetts Institute of
Technology, Cambridge, MA, U.S.

Lutz, A.F., Immerzeel, W.W., Shrestha, A.B., Bierkens, M.F.P., 2014. Consistent increase
in High Asia’s runoff due to increasing glacier melt and precipitation. Nat. Clim.
Chang. 4, 587–592. https://doi.org/10.1038/nclimate2237.

Markert, K.N., Chishtie, F., Anderson, E.R., Saah, D., Griffin, R.E., 2018. On the merging
of optical and SAR satellite imagery for surface water mapping applications. Results
Phys 9, 275–277. https://doi.org/10.1016/j.rinp.2018.02.054.

Martinis, S., Kuenzer, C., Wendleder, A., Huth, J., Twele, A., Roth, A., Dech, S., 2015.

Comparing four operational SAR-based water and flood detection approaches. Int. J.
Remote Sens. 36, 3519–3543. https://doi.org/10.1080/01431161.2015.1060647.
Martin-Puig, C., Leuliette, E., Lillibridge, J., Roca, M., 2016. Evaluating the performance
of Jason-2 open-loop and closed-loop tracker modes. J. Atmos. Ocean. Technol. 33,
2277–2288. https://doi.org/10.1175/JTECH-D-16-0011.1.

understand the future. J. Water Clim. Chang. 1, 87–101. https://doi.org/10.2166/
wcc.2010.010.

Okeowo, M.A., Lee, H., Hossain, F., Getirana, A., 2017. Automated generation of lakes
and reservoirs water elevation changes from satellite radar altimetry. IEEE J. Sel.
Top. Appl. Earth Obs. Remote Sens. 10 (8), 3465–3481. https://doi.org/10.1109/
JSTARS.2017.2684081.

Paris, A., Dias de Paiva, R., Santos da Silva, J., Medeiros Moreira, D., Calmant, S.,

Garambois, P.-A., Collischonn, W., Bonnet, M.-P., Seyler, F., 2016. Stage-discharge
rating curves based on satellite altimetry and modeled discharge in the Amazon
basin. Water Resour. Res. 52, 3787–3814. https://doi.org/10.1002/2014WR016618.
Pierdicca, N., Pulvirenti, L., Chini, M., Guerriero, L., Candela, L., 2013. Observing floods

from space: experience gained from COSMO-SkyMed observations. Acta Astronaut
84, 122–133. https://doi.org/10.1016/j.actaastro.2012.10.034.

Pokhrel, Y., Burbano, M., Roush, J., Kang, H., Sridhar, V., Hyndman, W.D., 2018. A re-
view of the integrated effects of changing climate, land use, and dams on Mekong
River hydrology. Water 10, 266. https://doi.org/10.3390/w10030266.

Räsänen, T.A., Kummu, M., 2013. Spatiotemporal influences of ENSO on precipitation

and flood pulse in the Mekong River basin. J. Hydrol. 476, 154–168. https://doi.org/
10.1016/j.jhydrol.2012.10.028.

Richman, M.B., 1986. Rotation of principal components. J. Climatol. 6, 293–335. https://

doi.org/10.1002/joc.3370060305.

Ruzza, G., Guerriero, L., Grelle, G., Guadagno, M.F., Revellino, P., 2019. Multi-method
tracking of monsoon floods using Sentinel-1 imagery. Water. https://doi.org/10.
3390/w11112289.

Sáenz, L., Farrell, T., Olsson, A., Turner, W., Mulligan, M., Acero, N., Neugarten, R.,

Wright, M., McKinnon, M., Ruiz, C., Guerrero, J., 2016. Mapping potential freshwater
services, and their representation within Protected Areas (PAs), under conditions of
sparse data. Pilot implementation for Cambodia. Glob. Ecol. Conserv. 7, 107–121.
https://doi.org/10.1016/j.gecco.2016.05.007.

Sakamoto, T., Van Nguyen, N., Kotera, A., Ohno, H., Ishitsuka, N., Yokozawa, M., 2007.
Detecting temporal changes in the extent of annual flooding within the Cambodia and
the Vietnamese Mekong Delta from MODIS time-series imagery. Remote Sens.
Environ. 109, 295–313. https://doi.org/10.1016/j.rse.2007.01.011.

Sakamoto, T., Van Phung, C., Kotera, A., Nguyen, K.D., Yokozawa, M., 2009. Analysis of
rapid expansion of inland aquaculture and triple rice-cropping areas in a coastal area
of the Vietnamese Mekong Delta using MODIS time-series imagery. Landsc. Urban
Plan. 92, 34–46. https://doi.org/10.1016/j.landurbplan.2009.02.002.

Sánchez-Reales, J.M., Vigo, M.I., Jin, S., Chao, B.F., 2012. Global surface geostrophic
ocean currents derived from satellite altimetry and GOCE geoid. Mar. Geod. 35,
175–189. https://doi.org/10.1080/01490419.2012.718696.

Sarkkula, J., Kiirkki, M., Koponen, J., Kummu, M., 2003. Ecosystem Processes of the

Tonle Sap Lake. 1st Work. Ecotone Phase II. Phnom Penh and Siem Reap, Cambodia.
Sarkkula, J., Baran, E., Chheng, P., Keskinen, M., Koponen, J., Kummu, M., 2005. Tonle

Sap Lake pulsing system and fisheries productivity. In: SIL Proc., 1922–2010.
Stuttgart, German. 29. pp. 1099–1102. https://doi.org/10.1080/03680770.2005.
11902855.

Schlaffer, S., Matgen, P., Hollaus, M., Wagner, W., 2015. Flood detection from multi-

temporal SAR data using harmonic analysis and change detection. Int. J. Appl. Earth
Obs. Geoinf. 38, 15–24. https://doi.org/10.1016/j.jag.2014.12.001.

Schumann, G.J.P., Moller, D.K., 2015. Microwave remote sensing of flood inundation.
Phys. Chem. Earth 83–84, 84–95. https://doi.org/10.1016/j.pce.2015.05.002.

Simard, M., Pinto, N., Fisher, J.B., Baccini, A., 2011. Mapping forest canopy height

globally with spaceborne lidar. J. Geophys. Res. Biogeosci. 116, g04021. https://doi.
org/10.1029/2011JG001708.

Slayback, D.A., Brakenridge, G.R., Policelli, F.S., Tokay, M.M., Kettner, A., 2012. Near
Real-Time Global Satellite Monitoring of Flooding Events, AGU Chapman Conf.
Remote Sensing of the Terrestrial Water Cycle, Kona, Hawaii, U.S.

Smith, L.C., 1997. Satellite remote sensing of river inundation area, stage, and discharge:
a review. Hydrol. Process. 11, 1427–1439. https://doi.org/10.1002/(SICI)1099-
1085(199708)11:10<1427::AID-HYP473>3.0.CO;2-S.

Sulistioadi, Y.B., Tseng, K.H., Shum, C.K., Hidayat, H., Sumaryono, M., Suhardiman, A.,
Setiawan, F., Sunarso, S., 2015. Satellite radar altimetry for monitoring small rivers
and lakes in Indonesia. Hydrol. Earth Syst. Sci. 19, 341–359. https://doi.org/10.
5194/hess-19-341-2015.

Tarpanelli, A., Camici, S., Nielsen, K., Brocca, L., Moramarco, T., Benveniste, J., 2019.

Potentials and limitations of Sentinel-3 for river discharge assessment. Adv. Sp. Res.
https://doi.org/10.1016/j.asr.2019.08.005.

MRC, 2009. The Flow of Mekong. MRC Management Inormation Booklet Series No. 2

Taylor, M.H., Losch, M., Wenzel, M., Schröter, J., 2013. On the sensitivity of field re-

MRC, Vientiane, Lao PDR.

MRC, 2010. Mekong River Commission: State of the Basin Report 2010. MRC, Vientiane,

Laos PDR.

[Software] NCL (Version 6.6.2), 2019. Boulder, Colorado. UCAR/NCAR/CISL/TDD.

doi:https://doi.org/10.5065/D6WD3XH5.

Nerem, R.S., Beckley, B.D., Fasullo, J.T., Hamlington, B.D., Masters, D., Mitchum, G.T.,
2018. Climate-change–driven accelerated sea-level rise detected in the altimeter era.
Proc. Natl. Acad. Sci. 115, 2022 LP–2025. https://doi.org/10.1073/pnas.
1717312115.

Normandin, C., Frappart, F., Lubac, B., Bélanger, S., Marieu, V., Blarel, F., Robinet, A.,
Guiastrennec-Faugas, L., 2018. Quantification of surface water volume changes in the
Mackenzie Delta using satellite multi-mission data. Hydrol. Earth Syst. Sci. 22,
1543–1561. https://doi.org/10.5194/hess-22-1543-2018.

North, G.R., Bell, T.L., Cahalan, R.F., Moeng, F.J., 1982. Sampling errors in the estimation
of empirical orthogonal functions. Mon. Weather Rev. 110, 699–706. https://doi.
org/10.1175/1520-0493(1982)110<0699:SEITEO>2.0.CO;2.

Nuorteva, P., Keskinen, M., Varis, O., 2010. Water, livelihoods and climate change
adaptation in the Tonle Sap Lake area, Cambodia: learning from the past to

construction and prediction using empirical orthogonal functions derived from Gappy
data. J. Clim. 26, 9194–9205. https://doi.org/10.1175/JCLI-D-13-00089.1.

Ticehurst, C., Guerschman, J.P., Chen, Y., 2014. The strengths and limitations in using the

daily MODIS open water likelihood algorithm for identifying flood events. Remote
Sens. 6, 11791–11809. https://doi.org/10.3390/rs61211791.

Tourian, M.J., Tarpanelli, A., Elmi, O., Qin, T., Brocca, L., Moramarco, T., Sneeuw, N.,
2016. Spatiotemporal densification of river water level time series by multimission
satellite altimetry. Water Resour. Res. 52, 1140–1159. https://doi.org/10.1002/
2015WR017654.

Tourian, M.J., Schwatke, C., Sneeuw, N., 2017. River discharge estimation at daily re-

solution from satellite altimetry over an entire river basin. J. Hydrol. 546, 230–247.
https://doi.org/10.1016/j.jhydrol.2017.01.009.

Tsyganskaya, V., Martinis, S., Marzahn, P., Ludwig, R., 2018a. SAR-based detection of

flooded vegetation–a review of characteristics and approaches. Int. J. Remote Sens.
39, 2255–2293. https://doi.org/10.1080/01431161.2017.1420938.

Tsyganskaya, V., Martinis, S., Marzahn, P., Ludwig, R., 2018b. Detection of temporary

flooded vegetation using Sentinel-1 time series data. Remote Sens. 10, 1286. https://
doi.org/10.3390/rs10081286.

29

C.-H. Chang, et al.

Remote Sensing of Environment 241 (2020) 111732

Twele, A., Cao, W., Plank, S., Martinis, S., 2016. Sentinel-1-based flood mapping: a fully
automated processing chain. Int. J. Remote Sens. 37, 2990–3004. https://doi.org/10.
1080/01431161.2016.1192304.

Van Trung, N., Choi, J.H., Won, J.S., 2013. A land cover variation model of water level for
the floodplain of Tonle Sap, Cambodia, derived from ALOS PALSAR and MODIS data.
IEEE J. Sel. Top. Appl. Earth Obs. Remote Sens. 6, 2238–2253. https://doi.org/10.
1109/JSTARS.2012.2226437.

Van Zalinge, N., Loeung, D., Pengbun, N., Sarkkula, J., Koponen, J., 2003. Mekong flood
levels and Tonle Sap fish catches. In: Proc. 2nd Int. Sym. Mangement of Large Rivers
for Fisheries. Phnom Penh, Cambodia.

Västilä, K., Kummu, M., Sangmanee, C., Chinvanno, S., 2010. Modelling climate change
impacts on the flood pulse in the lower Mekong floodplains. J. Water Clim. Chang. 1,
67–86. https://doi.org/10.2166/wcc.2010.008.

Werner, C., Wegmüller, U., Strozzi, T., Wiesmann, A., 2000. GAMMA SAR and

Interferometric Processing Software. ERS-ENVISAT Sym. Gothenburg, Sweden.
White, L., Brisco, B., Pregitzer, M., Tedford, B., Boychuk, L., 2014. RADARSAT-2 beam
mode selection for surface water and flooded vegetation mapping. Can. J. Remote.
Sens. 40, 135–151. https://doi.org/10.1080/07038992.2014.943393.

Wilks, D.S., 2011. Statistical Methods in the Atmospheric Sciences, third ed. Academic
Press, San Diego, CA, U.S. https://doi.org/10.1016/B978-0-12-385022-5.00012-9.

Willis, J.K., Chambers, D.P., C.-Y., K., Shum, C.K., 2010. Global sea level rise: recent

progress and challenges for the decade to come. Oceanography 23, 26–35. https://
doi.org/10.5670/oceanog.2010.03.

Wing, O.E.J., Bates, P.D., Sampson, C.C., Smith, A.M., Johnson, K.A., Erickson, T.A.,

2017. Validation of a 30 m resolution flood hazard model of the conterminous United
States. Water Resour. Res. 53, 7968–7986. https://doi.org/10.1002/
2017WR020917.

Wolter, K., Timlin, M.S., 1993. Monitoring ENSO in COADS with a seasonally adjusted
principal component index. In: Proc. 17th Climate Diagnostics Workshop, pp. 52–57
Norman, OK, U.S.

Wolter, K., Timlin, M.S., 1998. Measuring the strength of ENSO events: how does 1997/

98 rank? Weather 53, 315–324. https://doi.org/10.1002/j.1477-8696.1998.
tb06408.x.

Wolter, K., Timlin, M.S., 2011. El Niño/Southern Oscillation behaviour since 1871 as
diagnosed in an extended multivariate ENSO index (MEI.ext). Int. J. Climatol. 31,
1074–1087. https://doi.org/10.1002/joc.2336.

World Meteorological Organization, 2017. Verification of flash flood warnings. In: 1st

Steering Committee Meeting of the Southeastern Asia-Oceania Flash Flood Guidance
System, (Jakarta, Indonesia).

Xiao, X., Boles, S., Liu, J., Zhuang, D., Liu, M., 2002. Characterization of forest types in
Northeastern China, using multi-temporal SPOT-4 VEGETATION sensor data. Remote
Sens. Environ. 82, 335–348. https://doi.org/10.1016/S0034-4257(02)00051-2.
Yamazaki, D., Ikeshima, D., Tawatari, R., Yamaguchi, T., O’Loughlin, F., Neal, J.C.,

Sampson, C.C., Kanae, S., Bates, P.D., 2017. A high-accuracy map of global terrain
elevations. Geophys. Res. Lett. 44, 5844–5853. https://doi.org/10.1002/
2017GL072874.

Yan, K., Di Baldassarre, G., Solomatine, D.P., Schumann, G.J.-P., 2015. A review of low-
cost space-borne data for flood modelling: topography, flood extent and water level.
Hydrol. Process. 29, 3368–3387. https://doi.org/10.1002/hyp.10449.

Yosef, G., Alpert, P., Price, C., Rotenberg, E., Yakir, D., 2017. Using EOF analysis over a
large area for assessing the climate impact of small-scale afforestation in a semiarid
region. J. Appl. Meteorol. Climatol. 56, 2545–2559. https://doi.org/10.1175/JAMC-
D-16-0253.1.

Zheng, Y., Zhang, X., Hou, B., Liu, G., 2014. Using combined difference image and $k$
-means clustering for SAR image change detection. IEEE Geosci. Remote Sens. Lett.
11, 691–695. https://doi.org/10.1109/LGRS.2013.2275738.

Zhou, Y., Jin, S., Tenzer, R., Feng, J., 2016. Water storage variations in the Poyang Lake
Basin estimated from GRACE and satellite altimetry. Geod. Geodyn. 7, 108–116.
https://doi.org/10.1016/j.geog.2016.04.003.

30

