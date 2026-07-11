Environmental Modelling and Software 192 (2025) 106581

Contents lists available at ScienceDirect

Environmental Modelling and Software

journal homepage: www.elsevier.com/locate/envsoft

FIMserv v.1.0: A tool for streamlining Flood Inundation Mapping (FIM)
using the United States operational hydrological forecasting framework

, Supath Dhital a, Sagy Cohen a, Thanh Nhan Duc Tran b, Hesham Elhaddad c,

Anupal Baruah a,*
C. Lyn Watts d, Dipsikha Devi a, Yixian Chen a, Carson Pruitt e
a Department of Geography and Environment, The University of Alabama, Tuscaloosa, AL, 35401, USA
b Department of Civil and Environmental Engineering, The University of Virginia, Charlottesville, VA, 22903, USA
c Department of Geological and Environmental Sciences, Western Michigan University, Kalamazoo, MI, USA
d Department of Earth Geographic and Climate Sciences, University of Massachusetts, Amherst, MA, 01003, USA
e National Oceanic and Atmospheric Administration (NOAA), Federal, USA

A R T I C L E  I N F O

A B S T R A C T

Handling Editor: Daniel P Ames

Keywords:
Operational flood forecasting model
Global discharge
Cloud computing
United States
Fluvial flood

In the United States, the National Oceanic and Atmospheric Administration-Office of Water Prediction (NOAA-
OWP) utilizes the National Water Model (NWM) for operational hydrological forecasting. Its Flood Inundation
Mapping (FIM) framework translates NWM discharge to inundation extent using the Height Above the Nearest
Drainage (HAND) approach. The simplicity of the OWP HAND-FIM framework enables rapid, large-scale FIM
predictions across the U.S., fostering a growing user and developer community beyond NOAA. In this paper, we
introduce “FIM as a Service (FIMserv)”, an open-source toolset that streamlines OWP HAND-FIM predictions with
enhanced  functionalities:  (1)  FIM  generation  from  retrospective  and  forecasted  NWM  discharge,  (2)  Simulta-
neous simulations of multiple watersheds for various flood events, (3) FIM from Group on Earth Observations
Global Water Sustainability (GeoGLOWS) discharge, (4) evaluation of NWM and GeoGLOWS discharge against
USGS  observations.  FIMserv  operates  as  a  standalone  notebook  on  local/cloud  systems  and  as  a  Community
Resource within the CIROH cloud cyberinfrastructure.

1. Introduction

The global rise in flood events driven by climate change, environ-
mental challenges, and rapid urbanization has heightened the need for
rapid Flood Inundation Mapping (FIM) at large scales (Zhou et al., 2021;
Fohringer et al., 2015; Tran and Lakshmi, 2024; Tapas et al., 2024; Do
et al., 2024; Baruah et al., 2024; Devi et al., 2022). Currently, several
approaches are employed for flood mapping, including high-resolution
satellite imagery for near-real-time flood mapping/monitoring (Mason
et al., 2012; Shen et al., 2019; Annis et al., 2022), one-dimensional and
two-dimensional high-fidelity models (Zhang et al., 2016; Zahura et al.,
2020;  Jafarzadegan  et  al.,  2023),  low-fidelity  terrain  models  (Afshari
et al., 2018; Gutenson et al., 2022), and Machine Learning (ML) - Deep
Learning  (DL)  approaches  (Hosseiny,  2021;  Bentivoglio  et  al.,  2022;
Zhou  et  al.,  2022).  Hydrodynamic  models  generate  flood  inundation
maps  (FIM)  by  solving  one-dimensional  or  two-dimensional  shallow
water  equations.  Commonly  used  hydrodynamic  models  include
HEC-RAS (Stoleriu et al., 2020; Devi et al., 2022; Baruah et al., 2024),

MIKE-DHI (Papaioannou et  al., 2016), LISFLOOD-FP (Sharifian et  al.,
2023), and Delft-3D (Goede et al., 2020). While these models offer high
accuracy, they also entail significant computational costs (Paiva et al.,
2013). High-performance parallel computing methods can enhance the
efficiency  of  these  models  for  continental-scale  applications  at  30-m
resolution  (Wing et  al.,  2017); however,  running  such  models  in  real
time at this resolution remains computationally impractical.

The rapid generation of FIMs using remote sensing imagery offers a
valuable alternative for near real-time applications (Munasinghe et al.,
2018).  Remote  sensing-based  FIMs  are  particularly  advantageous  for
large-scale flood events. Nonetheless, this approach has several limita-
tions, including coarse resolution, cloud cover affecting optical sensors,
and  obstructions  causing  shadows  (Cohen  et  al.,  2019).  Recently,
data-driven  models  employing  machine  learning  and  deep  learning
without relying on physics-based concepts have seen wide application in
FIM generation (Bentivoglio et al., 2022). However, these methods often
struggle  with  generalization.  The  absence  of  high-quality  benchmark
flood  maps  further  limits  the  effectiveness  of  data-driven  models,

* Corresponding author.

E-mail address: abaruah@ua.edu (A. Baruah).

https://doi.org/10.1016/j.envsoft.2025.106581
Received 16 February 2025; Received in revised form 26 May 2025; Accepted 16 June 2025
Available online 17 June 2025
1364-8152/© 2025 The Authors. Published by Elsevier Ltd. This is an open access article under the CC BY license ( http://creativecommons.org/licenses/by/4.0/ ).

A. Baruah et al.

Environmental Modelling and Software 192 (2025) 106581

especially for real-time application in previously unseen areas. In recent
years,  the  Height  Above  the  Nearest  Drainage  (HAND)  method,  a
terrain-based  model  has  been  commonly  used  in  FIM.  It  involves
extensive hydro-conditioning of a Digital Elevation Model (DEM) and
converts it into a series of relative elevations (HAND grids) based on the
nearest  channel  flow  paths.  In  this  approach,  a  water  stage  value  is
assigned to the neighbouring pixels in the HAND grids to generate FIM
for  any given  stream  segment  (Godbout et  al.,  2019). Tarboton et  al.
(2018) proposed a novel approach that determines the stage-discharge
relationship  using  Synthetic  Rating  Curves  (SRCs).  This  method  in-
volves sampling reach-averaged parameters from the DEM and applying
Manning’s equation (Gauckler, 1867; Manning et al., 1890) to calculate
the stage, which is later used for FIM.

The HAND approach has been employed by the National Oceanic and
Atmospheric Administration (NOAA) Office of Water Prediction (OWP)
to generate operational fluvial FIM across the United States. The OWP
HAND-FIM utilizes detailed hydro-conditioning of a 10m DEM, converts
it to HAND raster (Aristizabal et al., 2023), and uses discharge data from
the National Water Model (NWM) to produce hourly flood maps at the
watershed scale (Hydrologic Unit Code (HUC)-8). The model translates a
static discharge value for each NWM stream into a stage using a reach
specific SRC. These FIM services are currently supplied to 30 % of the
population in the United States including Puerto Rico and the U.S. Virgin
Islands.  These  services  will  be  expanded  to  nearly  100  %  of  the  U.S.
population by 2026 (https://www.weather.gov/owp/operations).

short  computational

It is worth noting that the HAND FIM approach represents a trade-off
between accuracy and applicability, enabling the generation of large-
scale  flood  maps  within  a  very
time
(Garousi-Nejad et al., 2019), makes it appropriate for operational fore-
casting. While HAND offers notable benefits in terms of computational
efficiency, it is important to recognize its underlying assumptions and
limitations  (Aristizabal  et  al.,  2023).  Specifically,  HAND  methods
generate an inundation proxy and often fail to capture spillover effects
across the floodplain. The HAND method also assumes that all inundated
areas must drain toward a nearby flow path (Johnson et al., 2019) and
that  the  thalweg  network  drains  collectively  to  a  single  outlet  point
(Moriasi et al., 2015).

Although the OWP HAND-FIM is an open-source model (https://gith
ub.com/NOAA-OWP/inundation-mapping)  that  is  actively  used  and
developed by OWP, end users often face challenges in configuring and
running  the  model  to  generate  FIMs.  The  published  version  relies
exclusively on Docker for FIM execution. While Docker inherently en-
hances compatibility and portability (Merkel, 2014; Bernstein, 2014), its
exclusive use poses practical limitations for specific lightweight cloud
environments,  notably  interactive  notebook  platforms  such  as  Google
Colab  and  JupyterHub  via  2i2c  (Bisong,  2019;  Nelson  and  Hoover,
2020), which currently do not natively support Docker. These platforms
are  widely  used  for  educational  purposes,  rapid  prototyping,  and
collaborative computing, making a Docker-free alternative particularly
valuable  for  broadening  accessibility  and  usability  for  non-technical
users.

In this paper, we present the OWP HAND-FIM ‘as a service’  (FIM-
serv),  an  open-source  Python  toolset  for  running  the  FIM  generation
procedures  of  the  OWP  HAND-FIM  framework  using  its  operational
input data. This approach leverages virtual. env files to define essential
environment variables, such as input and output directories for the OWP
HAND-FIM’s  FIM  generation  module.  By  replicating  Docker’s  role  in
environment configuration in a simplified manner, this method bypasses
containerization while maintaining a consistent and portable setup. The
script dynamically adjusts to the local system’s structure, ensuring de-
pendencies and file paths are properly aligned for successful execution.
FIMserv includes the following additional functionalities:

1.  User-friendly and customizable notebook interface
2.  Embedded visualization
3.  Flexibility to run both locally and on the cloud

4.  Domain filtering based on stream order
5.  Multi-watershed simulations for different flood events
6.  Capability to process both retrospective and forecast (short- and

long-range) NWM discharge for FIM generation

7.  Visualization of SRCs for any reach within a HUC-8 boundary
8.  Comparison of USGS and NWMv3.0 retrospective discharge data.
9.  Ability  to  subset  from  the  HUC-8  scale  FIMs  based  on  user-

defined polygons or coordinates.

10. Inclusion of daily discharge from the Group on Earth Observa-
for  FIM

tions  Global  Water  Sustainability  (GeoGLOWS)
generation.

11.  Automatic FIM generation using USGS discharge data.

2. Methodology

2.1. The OWP HAND-FIM framework

The  NOAA-OWP  HAND-FIM  is  a  fully  operational,  national-scale
framework  developed  to  generate  high-resolution  FIM  (Aristizabal
et al., 2023). The model involves a series of DEM hydro-conditioning
processes,  including  flow  path  identification,  elevation  smoothing  to
ensure  monotonically  decreasing  terrain,  bathymetry  excavation,
stream  thalweg  breaching,  and  levee  enforcement  (Aristizabal  et  al.,
2023). The framework’s hydro fabric includes components such as the
relative elevation model (REM), or HAND grids, catchment data in both
vector  and  raster  formats,  and  a  comma-separated value  file  (hydrot-
able.csv)  containing  NWM  river  ID  (feature-id),  catchment  ID  (Hy-
droID),  DEM  derived  reach  averaged  channel  geometry  parameters
(hydraulic  radius,  wetted  perimeter)  and  Synthetic  Rating  Curves
(SRCs). These post-processed HAND grids are used to generate FIM using
discharge  input  (operationally  from  the  NWM)  and  SRCs.  SRCs  are
calculated  for  each  NWM  river  segment  using  Manning’s  equation  to
translate the discharge (m3/sec) into a stage (m). These stage values are
used to inundate the floodplain and produce a binary FIM output saved
in GeoTiff format.

2.2. Dependencies and libraries used in FIMserv

FIMserv relies on a set of dependencies, including a range of geo-
spatial  libraries,  each  chosen  to  support  different  functionalities
(defined  as  modules  within  the  framework),  ensuring  seamless  inte-
gration. In FIMserv, python libraries such as: rasterio, geopandas, Numpy,
Scipy and Bottleneck are used for reading, writing, and processing, and
optimization of raster and vector datasets handling within the frame-
work. Cloud interaction is facilitated by boto3 (https://pypi.org/project
/boto3/)  and  botocore,  which  integrate  with  Amazon  Web  Service
(AWS),  while  AWSCLI  (https://github.com/aws/aws-cli)  streamlines
data retrieval from AWS S3 bucket to framework workflows. FIMserv
framework  integrates  Tools  for  Exploratory  Evaluation  in  Hydrologic
Research  (TEEHR)  (https://github.com/RTIInternational/teehr)  to
streamline the retrieval of NWMv3.0 and United States Geological Sur-
vey  (USGS)  retrospective  discharge  data.  TEEHR  leverages  iterative
processing and distributed computing with its computation engine built
on  PySpark,  which  makes  it  efficiently  utilize  available  resources,
resulting in accelerating data downloading and processing.

For  the  statistical  evaluation  between  NWMv3.0  and  USGS  retro-
spective  discharge,  FIMserv  uses  Scikit-learn,  specifically  its  metrics
module (Pedregosa et al., 2018). Additionally, the framework utilizes
Python’s Requests library to fetch NWMv3.0 forecasted data from Google
Cloud Storage, using BeautifulSoup to parse HTML responses and identify
the required netCDF files based on user-defined date requests. These files
are  processed  with  the  netCDF4  library,  which  extracts  the  discharge
data based on different NWM stream segments according to user-defined
instructions. For data visualization and plotting, Matplotlib, geemap (Wu,
2020) and localtileserver packages are used.

2

A. Baruah et al.

Environmental Modelling and Software 192 (2025) 106581

2.3. Installation and run

sections.

The FIMserv package is now available in the PyPI repository and can
also  be  downloaded
(https://github.com/sdmlu
a/FIMserv). FIMserv currently utilizes the Jupyter Notebook interface
for installation and execution.

from  GitHub

A usage sample code (code_usage.ipynb) describing all arguments is
provided  on  GitHub  (https://github.com/sdmlua/FIMserv/tree/main/
docs). User can download this code on their local machine and install
the FIMserv tool using “pip install fimserve”. It automatically downloads
all dependencies that are needed to run the tool. The FIMserv package
can  also  be  installed  and  imported  into  cloud  environments  such  as
Google Colab and CIROH’s interactive 2i2C cloud computing Jupyter
Notebook. To install in the cloud, use the command “pip install fimserve”,
and then import it with “import fimserve”. The sample usage code for
using  FIMserv  in  Google  Colab  is  provided  here.  All  required  and
optional  arguments  for  different  modules  in  FIMserv  are  listed  in
Table 1, and detailed usage of all arguments is described in the following

Table 1
Modules in FIMserv are listed in order of execution.

Serial
No

Module

Purpose

Arguments

1

2

3

4

5

6

7

8

9

DownloadHUC8

getNWMretrospectivedata

plotNWMStreamflow

GetUSGSIDandCorrFID

getUSGSsitedate

plotUSGSStreamflow

CalculateStatistics

plotSRC

getNWMForecasteddata

10

11

runOWPHANDFIM

subsetFIM

12

vizualizeFIM

Download the
HUC8 level FIM-
Hydrofabric
dataset hosted in
CIROH S3 Bucket.
Download the
NWMv3.0
retrospective
discharge data.
Plot the discharge
time series for
NWM reach.
Get the USGS gauge
station IDs
intersecting with
NWM reaches.
Download the
USGS retrospective
discharge data.

Plot the USGS
discharge.

Statistical
evaluation of
NWMv3.0
discharge with
USGS discharge.
Plot the Synthetic
Rating Curves of
different NWM
reaches.
Download the
NWMv3.0 short,
medium and long-
range discharge
forecasts.
Run the OWP
HAND-FIM model.
Subset the HUC8
level flood
inundation map to
a user-defined
extent.
Visualize the flood
inundation map on
different base
maps.

hucIDa, stream_order

hucID, start_date,
end_date, value_time,
huc_event_dict

hucIDa, start_datea,
end_datea, feature_id

hucIDa

hucID,
start_date, end_date,
usgs_sites,
value_times
huc_event_dict
hucIDa,
usgs_sitesa,
start_datea, end_datea
hucIDa, feature_ida,
usgs_sitea, start_datea,
end_datea

hucIDa, hydro_ida,
branch_ida, discharge
value

hucIDa,
forecast_rangea,
forecast_date, hour,
sort_by,

hucIDa

boundarya, hucIDa,
methoda

inundation_rastera,
hucIDa, MapZooma
projectID

a Indicates the essential argument when calling the corresponding module.

3

2.3.1. Directory setup and data downloading

The  flowchart  of  the  work  is  shown  in  Fig.  1a,  illustrating  the
development and configuration process up to the final outputs generated
by FIMserv. Within the working directory, the DownloadHUC8 module
generates  three  primary  subdirectories:  code,  input,  and  output
(Fig. 1b). It also retrieves pre-processed HAND grids based on the user-
defined HUC-8 identifier (hucID) and stores them in the output directory
These datasets are hosted in a public Amazon Web Services (AWS) S3
bucket  from  the  Cooperative  Institute  for  Research  to  Operations  in
Hydrology
(https://ciroh-owp-hand-fim.ciroh.org/index.
html), which  includes  data for approximately  2400  HUC-8 across the
United States. The CIROH S3 bucket is a copy of the OWP ‘request-payer’
S3  bucket.  To  facilitate  this,  an  ArcGIS  Online  Repository  has  been
developed offering the location and IDs of HUC-8 watersheds (Table 2).
Using  the  same  module  (DownloadHUC8),  users  can  input  multiple
hucIDs in a (.csv) file, allowing the framework to download HAND grids
for multiple HUC8s and store them in the output directory.

(CIROH)

The second step is to clone the OWP HAND-FIM source code from
GitHub  into  the  code  directory  (https://github.com/NOAA-OWP/
inundation-mapping).  This  process  also  creates  a  localized  environ-
ment (.env) file within the code directory to manage essential variables.
In  the  third  step,  FIMserv  enables  users  to  automatically  retrieve

discharge data from NWMv3.0 and GeoGLOWS from the cloud.

The  getNWMretrospectivedata  and  getNWMForecasteddata  modules
can download both NWMv3.0 retrospective and forecast discharge data.
The  NWM  is  a  large-scale  operational  hydrological  simulator  for  the
United States developed by the National Weather Service (Follum et al.,
2020).  It  is  based  on  the  WRF-Hydro  framework  including  a  large
number  of  permutations  in  the  suite  of  land  surface,  hydrologic,  and
hydraulic physics (Read et al., 2023). In the NWM system, land surface
processes  are  represented  by  the  Noah  Multi-Parameterization
(Noah–MP)  land  surface  model  (LSM),  while  flow  routing  is  repre-
sented by the Muskingum-Cunge method. Currently, NWMv3.0 provides
discharge data for more than 2.7 million stream segments available in
the National Hydrography Dataset (NHDPlus) across the United States
(Buto and Anderson, 2020).

The  NWMv3.0  retrospective  dataset  consists  of  hourly  simulated
historical discharge data available from 1979 to 2023. These datasets
are stored in a public NOAA AWS S3 bucket (https://noaa-nwm-retro
spective-3-0-pds.s3.amazonaws.com/index.html)  and  are  provided  in
parquet format, which can be downloaded using the unique identifiers
(feature_id) of the NWM stream network. To simplify access, the OWP
HAND-FIM hydrofabric (river network) and their associated feature_ids
are hosted in the same ArcGIS Online Repository as the HUC-8 water-
sheds.  Using  the  user  defined  hucIDs  and  the  specified  event  period,
FIMserv downloads the retrospective discharge data and stores it in the
input directory. This entire process is fully automated, which helps to
significantly simplify the entire workflow.

NWMv3.0 discharge forecasts are available for three forecast hori-
zons: (a) short-range (18 h), (b) medium-range (10 days), and (c) long-
range (30 days) (Aristizabal et al., 2023). This dataset is stored in Google
(https://console.cloud.google.com/storage/browser/natio
Cloud
nal-water-model/nwm.20180917)  and  is  provided  in  NetCDF  (.nc)
format. The forecast data can also be downloaded using feature-ids of
the NWM stream network. Similar to the retrospective module, FIMserv
automatically retrieves forecast discharge based on user-defined hucID,
date and time (UTC 00Z–23Z), and stores it as a CSV file in the input
directory.

2.3.2. Running FIMserv with NWMv3.0 discharge

In the final step, the “runOWPHANDFIM” module uses discharge data
from the input directory and the downloaded HAND grids (HUC-8 scale)
to generate binary FIMs at a 10-m resolution. The outputs are then saved
in  the  output  directory  as  GeoTIFF  files.  FIMs  can  be  created  at  a

A. Baruah et al.

Environmental Modelling and Software 192 (2025) 106581

Fig. 1. (a) A complete pipeline demonstrating how the framework is designed (b) the directory structure on the user’s end when the code is executed.

Table 2
Dataset used in FIMserv.

Data

Description

Source

OWP-HAND raster

NWMv3.0

retrospective
discharge

NWMv3.0 forecast

discharge

GeoGLOWS

10m HAND raster across
CONUS
Hourly Discharge across
CONUS (1979–2023)

Long-range (6 hourly for 30
days)
Medium -range (3 hourly for
10 days)
Short-range (hourly for 18 h)
Global 3 hourly/Daily
Discharge data (1940-
Current)

HUC-8 ID, NWM

River ID and USGS
gauge sites

HUC-8 watersheds, NWM
river identifiers and USGS-
Discharge gauge stations
across CONUS

CIROH s3 bucket (s3://
ciroh-owp-hand-fim)
https://noaa-nwm-retro
spective-3-0-pds.s3.
amazonaws.com/index.
html
https://tinyurl.com/yt
3ampk2

http://GeoGLOWS-v2-re
trospective.s3-website
-us-west-2.amazonaws.
com
ArcGIS Online: Link

temporal  scale  corresponding  to  the  resolution  of  the  discharge  data.
Each  flood  map  is  assigned  a  unique  name  based  on  the  event  date,
ensuring  that  end  users  can  easily  navigate  the  map  in  the  output
directory.

Users can provide a boundary shapefile to subset a specific region of
interest from the HUC-8 scale flood map. Sub-setting enables users to
mask and extract the desired region, which is then saved in the output
directory.  Additionally,  the  framework  also provides functionality  for
visualizing flood maps overlaid with OpenStreetMap (OSM) and Google
Satellite imagery. Table 2 shows the list of different types of datasets that
can be accessed and utilized for FIMs using FIMserv across CONUS.

Currently, FIMserv uses the 10m HAND rasters generated by NOAA
OWP  (https://github.com/NOAA-OWP/inundation-mapping)  for  FIM
generation and does not offer terrain conditioning capabilities to users.
For example, if a user wants to evaluate the impact of different DEM
resolutions on FIM, they must follow the HAND pipeline developed by
OWP  and  use  the  processed  HAND  rasters  as  input  in  the  FIM
framework.

2.4. Running FIMserv with GeoGLOWS discharge

for  Medium-Range  Weather  Forecasts

GeoGLOWS  is  a  global  discharge  data  set  based  on  the  European
Centre
(ECMWF).  The
GeoGLOWS-ECMWF uses runoff depth forecasts generated by ECMWF
and applies the Muskingum method for channel routing (Gutenson et al.,
2024; Hales et al., 2022; Lozano et al., 2021). The latest version, Geo-
GLOWS v2.0, includes more than 7 million streams and 125 computa-
tional watersheds. GeoGLOWS provides two types of datasets, including
(a) retrospective discharge data based on reanalyzed ERA5 precipitation
data, available for 80 years (1940–2020) at a daily temporal resolution,
and  (b)  forecasted  discharge  data  ranging  from  3-h  to  15-day
(2021-Current).

Gutenson et al. (2024) compared GeoGLOWS and NWM discharge
predictions across four catchments in the United States and found that
catchment  hydrology  and  geography  significantly  influence  the  accu-
racy of both models. Their study showed that in snowmelt-dominated
catchments, GeoGLOWS predictions outperformed those of NWM. This
finding, along with the fact that GeoGLOWS is a continuously evolving
dataset, motivated us to integrate GeoGLOWS discharge data into the
FIMserv  toolset.  As  the  dataset  improves,  there  is  potential  for  Geo-
GLOWS to outperform NWM in certain catchments, which could result
in  better  FIM.  To  evaluate  the  potential  of  GeoGLOWS  discharge  in
improving  flood  inundation  mapping,  NWM  flowlines  were  spatially
joined with GeoGLOWS flowlines (Fig. 2), transferring their attributes to
the NWM flowlines. This integration allows GeoGLOWS discharge to be
used in FIMserv for flood inundation mapping. The GeoGLOWS (v2.0)
datasets  are  available  at  (https://data.GeoGLOWS.org/available-data)
and can be retrieved using their unique identifier (LINKNO). For spatial
joining, a conservative 100 m buffer was created around the GeoGLOWS
streamlines. This buffer facilitated a spatial join with the midpoints of
the NWM  flowlines, ensuring  that at least half of each  corresponding
NWM  flowline  fell  within  the  buffer.  Flowlines  with  midpoints  inter-
secting  the  GeoGLOWS  buffer  were  then  extracted.  This  approach
ensured that NWM flowlines spatially aligned with GeoGLOWS streams
could be identified with greater precision.

Once  the  intersecting  NWM  flowlines  are  identified,  their  connec-
tivity  is  traced  using  the  ‘ID’  field  and  the  “to”  field  (downstream
flowline identifier) in the attribute table. Starting from each identified
flowline, downstream tracing is performed until the most downstream

4

A. Baruah et al.

Environmental Modelling and Software 192 (2025) 106581

Fig. 2. (a) Overview of the GEOGLOWS streamlines and the NWM flowlines for Middle Brazos Lake Whitney watershed (hucID 12060202), (b–d) enlarged view of
joined NWM flowlines and GEOGLOWS flow lines.

flowline  is  reached.  This  process  extracted  additional  NWM  flowlines
that are not initially identified through the buffer but spatially corre-
sponded to GeoGLOWS streamlines. The midpoint of each NWM flow-
line is then used to locate the nearest GeoGLOWS streamline, ensuring
alignment over at least half the flowline. After this, the LINKNO field
from  the  GeoGLOWS  streamline  was  appended  to  the  corresponding
NWM flowline in the attribute table. Then GeoGLOWS discharge can be
used  in  FIMserv  via  the  unique  identifier  of  NWM  flowlines  in  OWP
HAND-FIM (i.e. feature_id), with LINKNO serving as an intermediate. All
spatial joins are performed in ArcGIS Pro (v3.3.2), and custom scripts
are  developed  to  automate  this  process  at  the  HUC-8  scale.  This
approach is adaptable for joining line features from other sources with
NWM  flowlines  within  the  ArcGIS  environment.  Although  this  study
demonstrated the spatial joining for one HUC-8 (hucID 12060202), we
plan to extend this process to NWM flowlines across the United States.
The resulting joined NWM flowlines, including the appended LINKNO
field, will be made publicly available.

For automatic downloading the GeoGLOWS discharge data, we have
developed a module and linked within the framework “getGEOGLOWS-
streamflow”.  It  is  callable  with  “fimserve.getGEOGLOWSstreamflow
(huc, event_time, hydrotable)”. The hydratable contains river flowline
information including ‘feature_id’ of NWM and ‘LINKNO’ of GeoGLOWS.
That  connection  is  derived  using  the  spatial  joining  of  two  flowlines
using  the  RiverJoin  method  (https://github.com/sdmlua/RiverJoin).
Using this ‘LINKNO’, this newly developed module gets the streamflow
value  based  on  the  event  date  and  assigns  it  to  the  corresponding

‘feature_id’ of NWM to generate FIM.

3. Applications and functionalities

In  this  section,  we  have  demonstrated  all  the  functionalities  of

FIMserv in different case studies.

3.1. Automated FIM generation with NWM retrospective and forecast
discharge

FIMserv automatically generate multiple flood maps using the NWM
retrospective  and  forecasted  discharge  data.  After  installation  and
import,  the  “DownloadHUC8”  module  downloads  HAND  grids  for  the
user-defined HUC-8 and stores them in the output directory, while the
‘getNWMRetrospectiveData’ module retrieves NWM retrospective hourly
discharge data for each feature_id based on the specified date and time
(Fig. 3a). The “runOWPHANDFIM”  module then uses the HAND grids,
and the extracted discharge to generate FIM.

FIMserv also enables users to perform simultaneous simulations in
multiple watersheds having different flood events. For instance, if a user
intends to generate FIM in two different HUC-8 having different flood
events,  they  need  to  provide  a  dictionary  specifying  the  hucIDs  and
corresponding  event  date-times  (Fig.  3b).  FIMserv  will  automatically
retrieve the retrospective discharge data for the designated watersheds
to generate the FIM.

To  generate  forecast  FIMs,  we  utilized  NWM  short,  medium,  and

5

A. Baruah et al.

Environmental Modelling and Software 192 (2025) 106581

Fig. 3(a). Sequential steps for FIM generation using FIMserv in Jupyter Notebook.

Fig. 3(b). FIM generation steps across multiple watersheds using FIMserv in Jupyter Notebook.

long-range  discharge  data.  The  short-range  forecast  provides  deter-
ministic discharge predictions at an hourly interval for up to 18 h. The
medium-range  forecast  provides  deterministic  discharge  predictions
every 3 h for up to 10 days, generating a total of 80 forecasts. The long-
range forecast is generated every 6 h (0z, 06Z, 12Z, 18Z), producing a
16-member ensemble forecast over 30 days, resulting in a total of 120
forecasts (Fig. 4a).

The “getNWMForecastedData” module in FIMserv retrieves discharge
forecasts  from  Google  Cloud  (link)  based  on  user-defined  hucIDs  and
date-time  (Fig.  4b).  These  forecasts  are  in  UTC  and  are  stored  in  the
FIMserv input directory.

For short-range forecasts, if no specific date-time is provided, FIM-
serv defaults to the current date-time and generates 18 flood maps at
hourly  intervals.  For  medium-  and  long-range  forecasts,  if  no  date  is
specified, FIMserv uses the current date and downloads a 10-day fore-
cast for medium-range and a 30-day forecast for long-range predictions.
By default, FIMserv selects the maximum discharge values from the
forecast, but users can customize this using the “getNWMForecastedData
(sort_by="")” argument to generate FIMs based on maximum, minimum,
or average discharge. The forecast_hour parameter in medium- and long-
range forecasts indicates that FIMserv is retrieving discharge data for
January 30, 2025, at 12Z (Fig. 4b).

Fig. 4(a). NWM long, medium and short-range forecast, where t refers to the current date-time. For short range FIMserv will extract hourly forecast for t+18 h,
medium range t+10 days and for long range t+30 days.

6

A. Baruah et al.

Environmental Modelling and Software 192 (2025) 106581

Fig. 4(b). Customizing and downloading Long-Range, Medium-Range, and Short-Range Forecasts using FIMserv in Jupyter Notebook.

In  this  example,  we  used  the  Middle  Neuse  watershed  (hucID-
03020202) and NWM retrospective data to generate FIMs for a historic
flood event in North Carolina caused by Hurricane Matthew on October
15, 2016, at 8 p.m. (Fig. 5a). We have generated the forecasted FIMs for
the Middle Neuse watershed (catchment area 2279 km2; Fig. 5b, c, d),
with  the  current  date  set  to  2024-11-14.  For  the  long-range  forecast,
daily  maximum  FIMs  for  30  days  are  generated  and  saved  as  binary
raster  in  GeoTIFF  format  in  the  output  directory.  The  medium-range
forecast  generates  10  daily  maximum  FIMs,  while  the  short-range
forecast  produces  18  hourly  FIMs.  The  maps  demonstrated  here  are
the FIM corresponding to maximum flow values taken from the retro-
spective discharge, short, medium and long-range forecast discharge.

In addition to the FIM generation process, a visualization module is
embedded in FIMserv using the ‘geemap’ framework (Fig. 6). To use this
module, users need to have a valid Google Earth Engine account and
create  a  projectID.  The  geemap  utilizes  the  localtileserver  framework
(https://github.com/banesullivan/localtileserver) to render raster data
as XYZ tiles through a lightweight local server. This method allows for
efficient visualization of flood inundation tiles using interactive maps
powered by Leaflet-based widgets like ipyleaflet or folium.

3.2. Computational efficiency

To  assess  FIMserv’s  computational  efficiency,  the  framework  is
tested on 66 randomly selected HUC-8s across the United States (Fig. S1
in  supplementary  material)  with  varying  catchment  areas.  Hourly
discharge data for 72 h is downloaded for all the stream reaches within
each watershed, and the model is executed for each HUC-8. Our results
showed that for the range of catchment area tested, a factor of four in-
crease  in  catchment  area  (900–22000  km2)  yielded  a  computational
time increased by a factor of 6 (30 s–180 s; Fig. 7). We also calculated the
cumulative computational time required for 25 watersheds by passing
HUC ID as key and one event date as value in a dictionary (Fig. S2 in
supplementary material).

In order to test the computational efficiency of FIMserv in different
platforms we took a single HUC-8 watershed (ID: 17020006), which has
a catchment area of 12,120.92 km2. We installed and run FIMserv on
Google Colab, macOS, and Windows operating systems. The assessment
includes  downloading  HAND  data  for  the  HUC-8,  retrieving  72-h
streamflow data, running the model, and generating the FIM for a sin-
gle  event.  Table  1 presents  the  system  configurations  and  time

Fig. 5. FIM generated using NWM retrospective and forecast discharge data: (a) Retrospective FIM on October 15, 2016, at 8:00 p.m. from NWM discharge (e); (b)
FIM from maximum NWM short-range discharge forecast on November 14, 2024, at 8:00 p.m. (f); (c) FIM from maximum NWM medium-range discharge forecast on
November 22, 2024 (g); (d) Fm from maximum NWM long-range discharge forecast on December 8, 2024 (h).

7

A. Baruah et al.

Environmental Modelling and Software 192 (2025) 106581

Fig. 6. Demonstration of FIM visualization in FIMserv in the Upper Neuse watershed, North Carolina: (a) code snippet for FIM visualization (b) Visualization in
FIMserv after running code in block a, c) and d) showing the inundation extents at different base maps.

3.3. Domain sub-setting and flexible input selection

FIMserv can filter and subset the (HUC-8) study domain based on
river stream order. The HUC-8s typically consist of multiple stream or-
ders, ranging from first to tenth-order streams. Sub-setting module in
FIMserv provides more flexibility and meets different requirements of
the users, for example, generating FIM for higher order streams, visu-
alizing and evaluating FIM for a specific land use-landcover etc.

One  important  implication  of  domain  sub-setting  is  during  the
evaluation the model flood maps with the benchmark. Benchmarks flood
inundation maps derived from remote sensing imagery, often exclude
small  tributaries  which  complicate  their  use  in  FIM  evaluation.  To
address this, users can opt to exclude minor tributaries and headwater
streams from model flood maps, retaining only the major streams for
simulation.  In  FIMserv,  the  stream_order  argument  in  the  “Down-
loadHUC8” module subsets the study domain based on the user-defined
minimum stream order and the “runOWPHANDFIM” module is used to
generate FIM.

This functionality is demonstrated in the Middle Neuse watershed,
North  Carolina  (hucID  (cid:0) 03020202)  in  which  the  FIMs  are  generated
(Fig.  8)  for  all  order  streams  as  well  as  for  higher-order  streams
(stream_order>3).

Another sub-setting functionality, “subsetFIM”, allows users to mask
out specific portions of the flood inundation maps based on an Area of
Interest (AOI) shapefile. Users can upload a boundary shapefile corre-
sponding  to the  benchmark  extent, and  the  framework  will  mask out

Fig. 7. Computational time versus HUC-8 watershed area.

requirement for each platform.

Nikrou  et  al.  (in  prep)  also  compared  the  computational  time  re-
quirements of different hydraulic FIM solvers, including HEC-RAS 2D,
LISFLOOD-FP, TRITON, and terrain-based solvers such as AUTOROUTE,
and FIMserv. Their findings showed that FIMserv takes approximately 1
min for data downloading and FIM generation, whereas LISFLOOD-FP
and HEC-RAS required between 4 h and 17 days to simulate the same
flood event.

8

A. Baruah et al.

Environmental Modelling and Software 192 (2025) 106581

Fig. 8. Demonstration of FIMserv sub-setting functionality for the Middle Neuse watershed, North Carolina: (a) FIM with all stream orders, and (b) FIM using stream
order 3 and higher.

that extent from the original FIM. We demonstrated this functionality
using HUC ID 03020202, where FIM for the entire HUC-8 is generated,
followed by a subset FIM based on a user-provided AOI (Fig. 9-a, b).

Table 4
Statistical metrics used in discharge comparison.

3.4. Statistical analysis of NWM and USGS observed discharge

The  availability  of  NWM  discharge  data  for  the  entire  US  river
network makes it a valuable input for large-scale flood modeling. Hy-
drological  models,  however,  introduce  uncertainties  which  propagate
into the FIM accuracy (Abdelkader et al., 2023; Cosgrove et al., 2024).
Quantifying input biases is therefore important, but often not properly
analyzed  and  reported.  FIMserv  includes  functionality  for  statistical
evaluation  of  NWM  discharge  predictions  against  USGS  gauge  data
(Fig.  10).  This  functionality  is  limited  to  NWM  streams  that  have  an
associated  USGS  station  within  the  user-selected  HUC-8s.  In  FIMserv,
“plotNWMDischarge”  modules  are  used  to  visualize  the  downloaded
NWM retrospective discharge for the user-defined streams (feature_id).
“GetUSGSIDandCorrFID”  identifies  USGS  gauges  located  within  the
HUC-8  boundary  and  their  corresponding  feature-ids  of  the  NWM
stream segments. Additionally, USGS gauge locations are hosted in the
ArcGIS Online Repository, providing easy access for users.

We demonstrated this functionality in the Middle Neuse watershed
(Fig.  11a)  for  two  NWM  river  segments  (feature_ids  = 11239465,
11239241) having USGS gauges (ID:02089500, 02091814) for the year
2015–2022. To compare NWM discharge with USGS gauge discharge,
the “CompareNWMnUSGSDischarge”  module is used (Fig. 11d–g). This
module plots the discharge data from both USGS and NWM for the user-
defined feature_ids. To calculate the evaluation statistics between NWM
and USGS discharge, the “CalculateStatistics”  module is applied. Kling-
Gupta  efficiency  (KGE)  (Gupta  et  al.,  2009),  Nash-Sutcliffe  efficiency
(NSE) (Nash and Sutcliffe, 1970), and percent bias (pBIAS) is considered
to quantify the error between the NWM and USGS discharge (Table 3).
At these two stations (Fig. 11e and f), we found that the NWM discharge
exhibits satisfactory KGE and NSE score (>0.7) with respect to observed
flow, however, there is a relatively higher value of pBIAS, (pBIAS>30

Table 3
Total time requirement in different operating system and cloud service.

RAM

Processor

OS/Cloud based
service

Google Colab
Windows-11

13 GB
32 GB

Intel Xeon
Intel Core I-7 9750 CPU @2.6
GHZ
Apple M2 Pro

Mac (Ventura 13.4)

16 GB

Time
(min)

3.3
3.05

2.2

9

Metrics

KGE

NSE

pBIAS

Expression

1 (cid:0)

1 -

100a

(r (cid:0) 1)2 + (b (cid:0) 1)2 + (g (cid:0) 1)2
∑
n
i=1

(QG (cid:0) QM)2
∑
n
(QG (cid:0) Qmean)2
i=1
∑
n
(QG (cid:0) QM)
i=1
∑
n
(QG)
i=1

Limit

-α to 1
-α to 1

-α to +α

a QG = USGS observed discharge, QM  = Discharge from models, Qmean  = Mean
value of the observed discharge, r = Pearson correlation coefficient between QG
and QM, b = ratio between mean of QM to the mean of, g = ratio of the coefficient
of variation of  QM  to QG.

%). This provides a quantitative estimate of the discharge data used in
FIM (see Table 4).

Identifying  the  relevant  NWM  flowlines  that  intersect  with  USGS
gauges (Fig. 9), users can also assign the gauge discharge data to these
flowlines and update the input discharge file from the input directory,
while using NWM-predicted discharge for the other reaches to generate
the FIM.

3.5. Synthetic rating curves for the river segments

Synthetic Rating Curves (SRCs) provide the stage (m) and discharge
(m3/s) relationships for any stream within a watershed. These curves are
derived  using  the  cross-sectional  average  parameters  of  each  reach
through Manning’s equation (Zheng et al., 2018; Scriven et al., 2021;
Gordon et al., 2023). The OWP HAND-FIM model utilizes these SRCs to
calculate the stage for a given discharge. The accuracy and reliability of
the  baseline  SRCs  are  limited  due  to  several  factors,  including  the
absence of bathymetric data, the use of generalized global Manning’s
roughness coefficients for both channels and floodplains, and artifacts
introduced  by  terrain  hydro-conditioning  (Sohrabi  et  al.,  2023).  To
mitigate  these  sources  of  bias,  the  Office  of  Water  Prediction  (OWP)
developed  SRC  adjustment  factors  at  approximately  7000  locations.
These factors are derived from USGS rating curves, calibrated HEC-RAS
1D model outputs, and high-fidelity inundation maps developed at NWS
partner flood inundation mapping sites (Pruitt et al., 2025). Recently,
Baruah et al. (2025) introduced a machine learning framework capable
of  predicting  these  adjustment  factors  at  the  national  scale,  thereby
enabling  their  application  across  the  entire  National  Water  Model
(NWM)  hydrofabric.  The  framework  was  evaluated  through  34  case

A. Baruah et al.

Environmental Modelling and Software 192 (2025) 106581

Fig. 9. (a) FIM for the entire HUC8 (hucID-03020202), and (b) AOI polygon for subsetting (c) Subset FIM obtained from subsetFIM module.

Fig. 10. a) Getting the USGS gauges and the corresponding NWM stream segments. b) Available USGS gauges intersecting with NWM stream segments, c) comparing
the NWM discharge with USGS discharge, and d) calculating the evaluation scores between the NWM and USGS discharge.

studies,  demonstrating  that  incorporating  the  predicted  adjustment
factors  led  to  significant  improvements  in  Flood  Inundation  Mapping
(FIM) performance.

The “plotSRC” module in FIMserv allows users to visualize SRCs for
any  specified  reach  and  check  the  stage  values  corresponding  to  the
user-defined discharge data. This functionality is demonstrated for the
Upper Clear Fork Brazos (hucID-12060102) in Fig. 12 with SRCs for two
feature-ids (5490493 and 5490541). The “plotSRC”  module also iden-
tifies  the  corresponding stage  values  based  on the  user-defined NWM
discharge  for  specific  stream  segments.  For  example,  for  feature-id
5490493, a discharge of 3000 m3/s corresponds to a stage of 8.23 m
(Fig.  12d),  while  for  feature-id  5490541,  a  discharge  of  3500  m3/s
corresponds to a stage of 9.75 m (Fig. 12e). Users can input multiple
feature-ids to visualize their respective SRCs.

3.6. FIM with NWM and GeoGLOWS retrospective data

FIMserv  can  retrieve  retrospective  daily  discharge  data  from  Geo-
GLOWS (cf. section 2.4). The GeoGLOWS daily discharge data is trans-
ferred  to  the  corresponding  NWM  flowlines  and  stored  in  the  input
directory as a CSV file. The ’runOWPHANDFIM’ module then uses this
discharge to generate the binary FIM, which is saved as a GeoTIFF file in
the output directory. Currently, the framework only supports the use of
retrospective GeoGLOWS discharge data. However, in future versions,
GeoGLOWS forecast discharge will also be integrated. We demonstrated
this functionality using the Middle Brazos Lake Whitney HUC-8 (hucID-

12060202) for daily discharge data from 2016. Since GeoGLOWS pro-
vides daily data, the NWM hourly discharge is aggregated to daily mean
values to ensure consistency between the datasets. Using USGS observed
discharge as a benchmark, FIMserv computes and displays key statistical
metrics, including KGE, NSE, and pBIAS for both NWM and GeoGLOWS
discharge data (Fig. 13, Table 5).

The results show that for both USGS stations, NWM demonstrates a
better NSE compared to GeoGLOWS discharge but also exhibits a very
higher pBIAS score. The framework does not apply any bias correction
or  statistical  adjustments  to  the  GeoGLOWS  or  NWM  discharge  data.
Instead,  this  functionality  helps  users  understand  the  bias  and  uncer-
tainty associated with the input flow data. Based on the statistical scores,
users can select the discharge dataset with less bias for more reliable
flood mapping (Fig. 13).

We used NWM and GeoGLOWS streamflow data from two events for
FIM generation: October 15, 2016 (a low-flow event) and June 2, 2016
(a peak-flow event). On October 15, the maximum predicted discharge
from NWM for the catchment was 29.88 m3/s, while GeoGLOWS pre-
dicted 24.85 m3/s. The resulting FIM extents were found to be nearly
identical, likely for two reasons: first, the discharge difference between
the two data sources was minimal, and second, the stages derived from
the  Synthetic  Rating  Curves  (SRC)  used  in  FIM  generation  were  not
sensitive to such a small variation in discharge.

During the peak-flow event on June 2, the maximum predicted NWM
flow  for  the  catchment  was  549  m3/s,  while  GeoGLOWS  predicted
234.22  m3/s.  This  underprediction  in  streamflow  from  GeoGLOWS

10

A. Baruah et al.

Environmental Modelling and Software 192 (2025) 106581

Fig. 11. Visualization and statistical comparison of NWM discharge and USGS observed discharge (2015–2022) for (a) Middle Neuse watershed (hucID-03020202) at
USGS gauge ids, (b) 02089500, (c) 02091814. (d, g) Plot between NWM discharge with USGS discharge obtained from “CompareNWMnUSGSDischarge” module, (e, f)
Evaluation statistics between NWM and USGS obtained from “CalculateStatistics”.

Fig. 12. (a) Watershed boundary of Upper Clear Fork Brazos (hucID-12060102) with the mainstream network and feature_ids, (b, c) feature_id-5490493, 5490541
and  (d,  e)  plot  of  SRCs,  generated  using  the  plotSRC  module,  indicating  stage  (8.23m,  9.75m)  corresponding  to  an  input  discharge  of  3000  and  3500  m3/s  for
feature_ids 5490493, 5490541.

translated into an underestimation of stage from the SRC and to the FIM
extent (Fig. 14).

3.7. FIM generation from NWM (NWM-FIM) and USGS discharge data
(USGS-FIM)

Although  this  demonstration  mainly  focuses  on  integrating  Geo-
GLOWS discharge data into FIMserv, the tool is not limited to this spe-
cific  data  source.  By  leveraging  the  spatial  joining  functionality
provided  in  the  ArcGIS  Pro  notebook  (https://github.com/sdmlua/
RiverJoin), users can incorporate discharge data from other hydrologi-
cal models, from observed records and from satellite data at any tem-
poral resolution in FIMserv to generate flood inundation maps.

Another interesting functionality embedded in FIMserv is the ability
to automatically generate FIM from USGS gauge stations. This feature
provides an additional quality check by quantifying streamflow uncer-
tainty  through  comparison  between  NWM-FIM  and  USGS-FIM.  To
execute FIM generation using USGS-observed flow, the framework first
identifies all USGS stations within the defined HUC-8 boundary. In the
second step, USGS gauge stations and their corresponding intersected

11

A. Baruah et al.

Environmental Modelling and Software 192 (2025) 106581

Fig. 13. Output FIMs in Middle Brazos Lake Whitney HUC-8 using the “runOWPHANDFIM” module for (a) NWM discharge, and (d) GeoGLOWS discharge for October
15, 2016. Hydrographs of NWM, USGS, and GeoGLOWS discharge at USGS stations (b, e) 08091000 and (c, f) 08096500.

Table 5
Comparison of GeoGLOWS and NWM discharge for the year 2016.

Source

KGE

USGS gauge ID 08091000
NWM
GeoGLOWS
USGS gauge ID: 08091500
NWM
GeoGLOWS

(cid:0) 0.08

0.0009

0.49
0.16

NSE

0.21
0.01

0.55
0.06

pBIAS (%)

158.11
91.44

70.15
69.37

NWM feature IDs are extracted using the ‘GetUSGSIDandCorrFID’ mod-
ule. In the third step, based on user-defined USGS station IDs and date-
time, the ‘getUSGSsitedata’ module downloads discharge data using the
TEEHR framework, associates it with the corresponding NWM feature
IDs,  and creates  a CSV file in the  input directory for  FIM generation.
Finally, using the ‘runOWPHANDFIM’ module, the user can generate the
flood  inundation  maps.  The  ‘getUSGSsitedata’  module  also  provides
flexibility  to  download  continuous  time-series  data,  extract  event-
specific flows, and run FIM across multiple watersheds.

We demonstrated this functionality in the Upper Neuse Watershed,
North Carolina (HUC ID: 03020201) for Hurricane Mathhew Flooding
on  October  9,  2016.  Using  the  ‘GetUSGSIDandCorrFID’  module,  we
identified  active  USGS  gauge  stations  along  with  the  corresponding
NWM feature IDs that intersect these gauges within the HUC-8 bound-
ary. Next, by applying the ‘getUSGSsitedata’ module, we structured the
retrieved  discharge  data  and  created  a  flow  input  file  (CSV  format)
required for FIM generation (see Fig. 15).

4. FIM evaluation test cases

The outputs flood inundation maps (FIM) generated from the FIM-
serv are validated against two sets of benchmarks FIM derived from 1)
High-resolution  Remote  sensing  flood  maps  for  Hurricane  Matthew

12

flooding  (October  10  and  October  14,  2016)  in  North  Carolina  (Tian
et al., 2024) and 2) HEC-RAS derived synthetic FIM (100 and 500-year
return period flow) referred to as Base Level Engineering (BLE) for the
14 HUC-8 watershed in Oklahoma. The remote sensing flood maps were
generated using the high-resolution images from the Planet small sat-
ellite constellations. The PlanetScope and RapidEye products were ob-
tained  through  NASA  Commercial  Smallsat  Data  Acquision  (CSDA)
program. The remote sensing FIMs are further enhanced by applying the
hydrologically guided region grow algorithm (Tian et al., 2024).

For  actual  flood  events  we  used  the  National  Water  Model  retro-
spective  discharge  data,  while  for  synthetic  flood  events,  we  utilized
publicly available 100-year and 500-year return period BLE discharge
data (ttps://webapps.usgs.gov/infrm/estbfe/). A pixel-based evaluation
framework  Flood  Inundation  Mapping  Prediction  Evaluation  Frame-
work (FIMPEF) (Devi et al., 2022) is used to calculate the performance
scores (Table-6).

The performance scores for the actual flood events were found to be
satisfactory. On October 10, the CSI score was 0.63, the POD was 0.88,
and the F1 score was 0.77. On October 14, the CSI score dropped to 0.55,
the POD to 0.68, and the F1 score to 0.61 (Figure-16 a, b).

For  synthetic  flooding,  we  found  that  for  100-year  return  period
flow, the mean values of CSI, F1, and POD were 0.6, 0.74, and 0.72,
respectively.  Similarly,  for  a  500-year  return  period  flow,  the  mean
values  of  CSI,  F1,  and  POD  were  estimated  as  0.63,  0.77,  and  0.75,
respectively (Fig. 17).

We also compared the NWM-FIM with the USGS-FIM (Figure-15) and
calculated the CSI, POD, and F1 scores for October 9, 2016, at the Upper
Neuse Watershed in North Carolina (Figure-18). We found that, at all
stations  except  020868449,  the  CSI,  POD,  and  F1  scores  were  quite
satisfactory. The mean CSI score across the five stations was 0.62, the
mean POD was 0.81, and the mean F1 score was 0.76. The median CSI
score was 0.55, the median POD was 0.69, and the median F1 score was
0.71. A substantial underprediction of the FIM extent was observed at

A. Baruah et al.

Environmental Modelling and Software 192 (2025) 106581

Fig. 14. Output FIMs in Middle Brazos Lake Whitney HUC-8 using the “runOWPHANDFIM” module for (a) NWM discharge, and (d) GeoGLOWS discharge for June
2, 2016.

Fig. 15. (a) USGS gauge stations within the Upper Neuse watershed (b–g): Output FIMs generated using both USGS and NWM discharge data at different gauge
locations. The blue color represents the FIM derived from NWM discharge data, while the light pink color represents the FIM generated from USGS discharge data.
The purple color indicates areas of agreement, where NWM FIM pixels match with USGS FIM pixels. (For interpretation of the references to color in this figure legend,
the reader is referred to the Web version of this article.)

13

A. Baruah et al.

Environmental Modelling and Software 192 (2025) 106581

Table 6
Metrics used in performance evaluation.

Metrics

F1 Score

Probability of

Detection (POD)

Critical Success
Index (CSI)

Formula

Description

2TP/(2 TP +
FP + FN)

TP/(TP + FN)

TP/(TP + FN
+ FP)

0-1, 1 indicates perfect precision and recall,
0 indicates poor balance between precision
and recall.
0-1, 1 indicates most perfect score,
0 indicate most imperfect score.
0-1, 1 indicates perfect TP detection and
0 indicates no successful detection.

platform for rapid flood inundation mapping. It represents a reasonable
trade-off between accuracy and usability, especially when considering
factors such as data requirements, computational time, accessibility, and
model complexity. The model requires only two primary inputs for FIM
generation 10m HAND rasters and streamflow data both of which are
easily accessible through the FIMserv platform. Another key advantage
of FIMserv is its flexibility to run on cloud-based platforms and its in-
dependence from any specific operating system.

5. Conclusion

station 020868449 (Fig.  15c), which is  attributed to a  significant un-
derestimation of the NWM streamflow—nearly five times lower than the
observed flow. The predicted flow from NWM was 18.54 m3/s, while the
observed flow was 91.22 m3/s.

Based on these evaluations, we argue that although the performance
scores may not be outstanding, FIMserv offers an efficient and practical

In this paper, we present an efficient and user-friendly Flood Inun-
dation Mapping (FIM) toolset (FIMserv) based on the NOAA Office of
Water  Prediction  (OWP)  operational  hydrological  forecasting  frame-
work.  FIMserv  streamlines  the  FIM  generation  module  of  the  OWP
HAND-FIM framework and can be run on local workstations and cloud
platforms. FIMserv introduces functionalities beyond the original OWP

Fig. 16. Contingency matrix from comparing flood inundation extents generated by FIMserv with remote sensing flood extents for (a) October 10, 2016, and (b)
October 15, 2016.

Fig. 17. Evaluation metrics of flood inundation extents generated by FIMserv with HEC RAS derived flood extent. Histograms in the top panel and bottom represent
the distribution of evaluation scores for 100-year and 500-year return period. The dots represent the spatial distribution of BLE HUC-8 watersheds in Oklahoma State
and different colors indicate the values of CSI, POD and F1 Scores. (For interpretation of the references to color in this figure legend, the reader is referred to the Web
version of this article.)

14

A. Baruah et al.

Environmental Modelling and Software 192 (2025) 106581

Fig. 18. Evaluation metrics of NWM-FIM with USGS-FIM (as benchmark) at different gauge stations.

HAND-FIM  framework  including  (1)  domain  filtering  based  on  river
stream order and AOI, (2) accuracy assessment of national water model
(NWM) against USGS discharge, (3) ability to dynamically assign USGS
discharge  values  for  selected  river  reaches,  (4)  flood  mapping  with
NWM retrospective and forecast discharge, (5) visualizing the synthetic
rating  curves  used  in  flood  mapping,  (6)  use  of  GeoGLOWS  daily
discharge. The framework has been tested and run in Windows, macOS
and cloud environments (Google Colab and 2i2C interactive computing
framework). FIMserv is useful for researchers to integrate operational
FIM into their workflows or test different scenarios and flow conditions.
FIMserv is poised to be an efficient tool for a broad range of scientists
and partitioners, including social scientists, economists, and individuals,
enabling them to generate high-resolution (10m) operational flood maps
with minimal effort. Further development of FIMserv will include (1)
introduction of additional discharge dataset (e.g. SWOT), (2) enhance-
ment of visualization using open-source web mapping, (3) inclusion of
building footprints for risk and vulnerability studies, and (4) develop-
ment of a webGIS portal for deployment as a web service as part of the
Cooperative Institute for Research to Operations in Hydrology (CIROH)
cyber
(https://docs.ciroh.org/docs/products/Flood%
20Inundation%20Mapping/FIMserv/).

enterprise

Codes and datasets

Name of tool: FIMserv.
Developers: Anupal Baruah, Supath Dhital.
Contact:  abaruah@ua.edu,

sdhital@crimson.ua.edu,

sagy.coh

en@ua.edu.

Program Language: Python.
GitHub Repository of FIMserv: https://github.com/sdmlua/fimserv.
FIMserv in PyPI repository: https://pypi.org/project/fimserve/
Arc-GIS online dataset: https://arcg.is/1LeqPD1.
FIMserv  listing  on  CIROH  DocuHub:  https://docs.ciroh.org/docs
/products/Community%20Flood%20Inundation%20Mapping/FIM%20
as%20a%20Service/

FIMserv in Google Colab:https://tinyurl.com/2z7845re.
GeoGLOWS: https://data.geoglows.org/available-data.
TEEHR: https://github.com/RTIInternational/teehr.

CRediT authorship contribution statement

Anupal Baruah: Writing – review & editing, Writing – original draft,
Visualization, Software, Methodology, Formal analysis, Conceptualiza-
tion. Supath Dhital: Writing – original draft, Visualization, Methodol-
ogy,  Formal  analysis.  Sagy  Cohen:  Writing  –  review  &  editing,
Supervision,  Methodology,  Funding  acquisition,  Conceptualization.
Thanh  Nhan  Duc  Tran:  Writing  –  review  &  editing,  Methodology.
Hesham Elhaddad: Writing – review & editing, Methodology. C. Lyn
Watts: Methodology. Dipsikha Devi: Writing – review & editing. Yix-
ian  Chen:  Writing  –  review  &  editing,  Methodology.  Carson  Pruitt:
Methodology.

Declaration of competing interest

The authors declare that they have no known competing financial
interests or personal relationships that could have appeared to influence
the work reported in this paper.

Acknowledgement

Funding  for  this  project  was  provided  by  the  National  Oceanic  &
Atmospheric  Administration  (NOAA),  awarded  to  the  Cooperative
Institute for Research to Operations in Hydrology (CIROH) through the
NOAA  Cooperative  Agreement  with  The  University  of  Alabama
(NA22NWS4320003). We utilized the Tools for Exploratory Evaluation
in  Hydrologic  Research  (TEEHR)  open-source  package,  developed  by
RTI  International,  to  download  the  NWM  retrospective  and  USGS
discharge data (https://tinyurl.com/5brv4m7m).

Appendix A. Supplementary data

Supplementary data to this article can be found online at https://doi.

org/10.1016/j.envsoft.2025.106581.

Data availability

I have shared the link for the code with the manuscript

15

A. Baruah et al.

Environmental Modelling and Software 192 (2025) 106581

References

Abdelkader, M., Temimi, M., Ouarda, T.B.M.J., 2023. Assessing the national water

model’s discharge estimates using a multi-decade retrospective dataset across the
contiguous United States. Water (Switzerland) 15 (13). https://doi.org/10.3390/
w15132319.

Afshari, S., Tavakoly, A.A., Rajib, M.A., Zheng, X., Follum, M.L., Omranian, E., Fekete, B.
M., 2018. Comparison of new generation low-complexity flood inundation mapping
tools with a hydrodynamic model. J. Hydrol. 556, 539–556. https://doi.org/
10.1016/j.jhydrol.2017.11.036.

Annis, A., Nardi, F., Castelli, F., 2022. Simultaneous assimilation of water levels from

river gauges and satellite flood maps for near-real-time flood mapping. Hydrol. Earth
Syst. Sci. 26 (4), 1019–1041. https://doi.org/10.5194/hess-26-1019-2022.

Aristizabal, F., Salas, F., Petrochenkov, G., Grout, T., Avant, B., Bates, B., Judge, J., 2023.
Extending height above nearest drainage to model multiple fluvial sources in flood
inundation mapping applications for the US national water model. Water Resour.
Res. 59 (5), e2022WR032039. https://doi.org/10.1029/2022WR032039.
Baruah, A., Barman, D., Arjun, B.M., Chyne, B.L., Aggarwal, S.P., 2024. Holistic

framework for flood hazard assessment in a trans-boundary basin. Acta Geophys. 72
(2), 1017–1032.

Baruah, A., Spies, R., Devi, D., Cohen, S., Aristizabal, F., Nikrou, P., Tien, D., Pruitt,

2025. Predicting synthetic rating curve adjustment factors with explainable machine
learning for enhancing the United States operational flood inundation mapping
framework. ESS Open Archive. https://doi.org/10.22541/
essoar.174078575.57445823/v1.

Bentivoglio, R., Isufi, E., Jonkman, S.N., Taormina, R., 2022. Deep learning methods for
flood mapping: a review of existing applications and future research directions.
Hydrol. Earth Syst. Sci. 26, 4345–4378. https://doi.org/10.5194/hess-26-4345-
2022.

Bernstein, D., 2014. Containers and cloud: from LXC to docker to kubernetes. IEEE Cloud

Comput. 1 (3), 81–84. https://doi.org/10.1109/MCC.2014.51.

Bisong, E., 2019. Building Machine Learning and Deep Learning Models on Google Cloud
Platform. Apress, Berkeley, CA, pp. 59–64. https://doi.org/10.1007/978-1-4842-
4470-8.

Buto, S.G., Anderson, R., 2020. Nhdplus High Resolution (Nhdplus HR)—A Hydrography
Framework for the Nation (No. 2020-3033). US Geological Survey, p. 2. https://doi.
org/10.3133/fs20203033.

Cohen, S., Raney, A., Munasinghe, D., Loftis, J.D., Molthan, A., Bell, J., Rogers, L.,

Galantowicz, J., Brakenridge, G.R., Kettner, A.J., Huang, Y.-F., Tsang, Y.-P., 2019.
The floodwater depth estimation tool (FwDET v2.0) for improved remote sensing
analysis of coastal flooding. Nat. Hazards Earth Syst. Sci. 19, 2053–2065. https://
doi.org/10.5194/nhess-19-2053-2019.

Cosgrove, B., Gochis, D., Flowers, T., Dugger, A., Ogden, F., Graziano, T., Clark, E.,
Cabell, R., Casiday, N., Cui, Z., Eicher, K., Fall, G., Feng, X., Fitzgerald, K.,
Frazier, N., George, C., Gibbs, R., Hernandez, L., Johnson, D., Zhang, Y., 2024.
NOAA’s national water model: advancing operational hydrology through
continental-scale modeling. J. Am. Water Resour. Assoc. 60 (2), 247–272. https://
doi.org/10.1111/1752-1688.13184.

De Goede, E.D., 2020. Historical overview of 2D and 3D hydrodynamic modelling of
shallow water flows in the Netherlands. Ocean Dyn. 70 (2), 155–172. https://doi.
org/10.1007/s10236-019-01336-5.

Devi, D., Baruah, A., Sarma, A.K., 2022. Characterization of dam-impacted flood

hydrograph and its degree of severity as a potential hazard. Nat. Hazards 112 (3),
1989–2011.

Do, S.K., Nguyen, B.Q., Tran, V.N., Grodzka-Łukaszewska, M., Sinicyn, G., Lakshmi, V.,
2024. Investigating the future flood and drought shifts in the transboundary srepok
river basin using CMIP6 projections. IEEE J. Sel. Top. Appl. Earth Obs. Rem. Sens.
https://doi.org/10.1109/JSTARS.2024.3380514.

Fohringer, J., Dransch, D., Kreibich, H., Schr¨oter, K., 2015. Social media as an

information source for rapid flood inundation mapping. Nat. Hazards Earth Syst. Sci.
15 (12), 2725–2738. https://doi.org/10.5194/nhess-15-2725-2015.

Follum, M.L., Vera, R., Tavakoly, A.A., Gutenson, J.L., 2020. Improved accuracy and

efficiency of flood inundation mapping of low-, medium-, and high-flow events using
the AutoRoute model. Nat. Hazards Earth Syst. Sci. 20 (2), 625–641. https://doi.org/
10.5194/nhess-20-625-2020.

Garousi-Nejad, I., Tarboton, D.G., Aboutalebi, M., Torres-Rua, A.F., 2019. Terrain
analysis enhancements to the height above nearest drainage flood inundation
mapping method. Water Resour. Res. 55 (10), 7983–8009. https://doi.org/10.1029/
2019WR024837.

Godbout, L., Zheng, J.Y., Dey, S., Eyelade, D., Maidment, D., Passalacqua, P., 2019. Error

assessment for height above the nearest drainage inundation mapping. JAWRA J.
Am. Water Resour. Associat. 55 (4), 952–963. https://doi.org/10.1111/1752-
1688.12783.

Gordon, C.A., Foulon, E., Rousseau, A.N., 2023. Deriving synthetic rating curves from a
digital elevation model to delineate the inundated areas of small watersheds.
J. Hydrol.: Reg. Stud. 50. https://doi.org/10.1016/j.ejrh.2023.101580.

Gupta, H.V., Kling, H., Yilmaz, K.K., Martinez, G.F., 2009. Decomposition of the mean
squared error and NSE performance criteria: implications for improving hydrological
modelling. J. Hydrol. 377 (1–2), 80–91. https://doi.org/10.1016/j.
jhydrol.2009.08.003.

Hales, R.C., Nelson, E.J., Souffront, M., Gutierrez, A.L., Prudhomme, C., Kopp, S.,

Ames, D.P., Williams, G.P., Jones, N.L., 2022. Advancing global hydrologic modeling
with the GeoGLOWS ECMWF discharge service. J. Flood Risk Manag. https://doi.
org/10.1111/jfr3.12859.

Hosseiny, H., 2021. A deep learning model for predicting river flood depth and extent.

Environ. Model. Software 145, 105186. https://doi.org/10.1016/j.
envsoft.2021.105186.

Jafarzadegan, K., Moradkhani, H., Pappenberger, F., Moftakhari, H., Bates, P.,

Abbaszadeh, P., et al., 2023. Recent advances and new frontiers in riverine and
coastal flood modeling. Rev. Geophys. 61 (2), e2022RG000788. https://doi.org/
10.1029/2022RG000788.

Lozano, J.S., Bustamante, G.R., Hales, R.C., Nelson, E.J., Williams, G.P., Ames, D.P.,
Jones, N.L., 2021. A discharge bias correction and performance evaluation web
application for GeoGLOWS ecmwf discharge services. Hydrology 8 (2). https://doi.
org/10.3390/hydrology8020071.

Mason, D.C., Davenport, I.J., Neal, J.C., Schumann, G.J.P., Bates, P.D., 2012. Near real-
time flood detection in urban and rural areas using high-resolution synthetic
aperture radar images. IEEE Trans. Geosci. Rem. Sens. 50 (8), 3041–3052. https://
doi.org/10.1109/TGRS.2011.2178030.

Merkel, D., 2014. Docker: lightweight Linux containers for consistent development and

deployment. Linux J. 239 (2), 2. https://www.seltzer.com/margo/teaching/
CS508.19/papers/merkel14.pdf.

Moriasi, D.N., Gitau, M.W., Pai, N., Daggupati, P., 2015. Hydrologic and water quality
models: performance measures and evaluation criteria. Transact. ASABE 58 (6),
1763–1785. https://doi.org/10.13031/trans.58.10715.

Munasinghe, Dinuke, Cohen, Sagy, Huang, Yu-Fen, Tsang, Yin-Phan, Zhang, Jiaqi,
Fang, Zheng, 2018. Intercomparison of satellite remote sensing-based flood
inundation mapping techniques. J. Am. Water Resour. Assoc. 54 (4), 834–846.
https://doi.org/10.1111/1752-1688.12626.

Nash, J.E., Sutcliffe, J.V., 1970. River flow forecasting through conceptual models part
I—A discussion of principles. J. Hydrol. 10 (3), 282–290. https://doi.org/10.1016/
0022-1694(70)90255-6.

Nelson, M.J., Hoover, A.K., 2020. Notes on using google colaboratory in AI education. In:

Proceedings of the 2020 ACM Conference on Innovation and Technology in
Computer Science Education, pp. 533–534. https://doi.org/10.1145/
3341525.339399.

Paiva, R.C.D., Buarque, D.C., Collischonn, W., Bonnet, M.-P., Frappart, F., Calmant, S.,

Mendes, C.A.B., 2013. Large-scale hydrologic and hydrodynamic modeling of the
amazon river basin. Water Resour. Res. 49, 1226–1243. https://doi.org/10.1002/
wrcr.2006.

Papaioannou, G., Loukas, A., Vasiliades, L., Aronica, G.T., 2016. Flood inundation
mapping sensitivity to riverine spatial resolution and modeling approach. Nat.
Hazards 83 (Suppl. 1), 117–132. https://doi.org/10.1007/s11069-016-2382.

Pedregosa, F., Varoquaux, G., Gramfort, A., Michel, V., Thirion, B., Grisel, O.,

Blondel, M., Müller, A., Nothman, J., Louppe, G., Prettenhofer, P., Weiss, R.,
Dubourg, V., Vanderplas, J., Passos, A., Cournapeau, D., Brucher, M., Perrot, M.,
Duchesnay, ´E., 2018. Scikit-learn: machine learning in python. arXiv:1201.0490).
arXiv. https://doi.org/10.48550/arXiv.1201.0490.

Pruitt, C., Giardino, D., Salas, F., Spies, R., Hanna, R., Luck, M., James Matthew, Coll,
Ghahremani, Z., 2025. Improvements in continental-scale flood inundation mapping
at NOAA’s office of water prediction. Paper Presented at 105th AMS Annual
Meeting. New Orleans, Louisiana.

Scriven, B.W.G., McGrath, H., Stefanakis, E., 2021. GIS derived synthetic rating curves
and HAND model to support on-the-fly flood mapping. Nat. Hazards 109 (2),
1629–1653. https://doi.org/10.1007/s11069-021-04892-6.

Sharifian, M.K., Kesserwani, G., Chowdhury, A.A., Neal, J., Bates, P.D., 2023. LISFLOOD-
FP 8.1: new GPU-accelerated solvers for faster fluvial/pluvial flood simulations.
Geosci. Model Dev. (GMD) 16 (9), 2391–2413. https://doi.org/10.5194/gmd-16-
2391-2023.

Shen, X., Anagnostou, E.N., Allen, G.H., Brakenridge, G.R., Kettner, A.J., 2019. Near-

real-time non-obstructed flood inundation mapping using synthetic aperture radar.
Rem. Sens. Environ. 221, 302–315. https://doi.org/10.1016/j.rse.2018.11.008.
Stoleriu, C.C., Urzica, A., Mihu-Pintilie, A., 2020. Improving flood risk map accuracy

using high-density LiDAR data and the HEC-RAS river analysis system: a case study
from north-eastern Romania. J. Flood Risk Manag. 13, e12572.

Tapas, M.R., Do, S.K., Etheridge, R., Lakshmi, V., 2024. Investigating the impacts of
climate change on hydroclimatic extremes in the Tar-Pamlico River basin, North
Carolina. J. Environ. Manag. 363, 121375. https://doi.org/10.1016/j.
jenvman.2024.121375.

Tran, T.-N.-D., Lakshmi, V., 2024. Enhancing human resilience against climate change:
assessment of hydroclimatic extremes and sea level rise impacts on the Eastern Shore
of Virginia, United States. Sci. Total Environ. 947, 174289. https://doi.org/10.1016/
j.scitotenv.2024.174289.

Wing, O.E.J., Bates, P.D., Sampson, C.C., Smith, A., Fargione, J., Johnson, K., 2017.
Validation of a 30 m resolution flood hazard model of the conterminous United
States. Water Resour. Res. 53 (7), 7968–7986. https://doi.org/10.1002/
2017WR020917.

Wu, Q., 2020. Geemap: a python package for interactive mapping with google Earth

engine. J. Open Source Softw. 5 (51), 2305. https://doi.org/10.21105/joss.02305.

Zahura, F.T., Goodall, J.L., Sadler, J.M., Shen, Y., Morsy, M.M., Behl, M., 2020. Training
machine learning surrogate models from a high-fidelity physics-based model:
application for real-time street-scale flood prediction in an urban coastal community.
Water Resour. Res. 56 (10), e2019WR027038. https://doi.org/10.1029/
2019WR027038.

Zhang, T., Feng, P., Maksimovi´c,

ˇ
C., Bates, P.D., 2016. Application of a three-

dimensional unstructured-mesh finite-element flooding model and comparison with
two-dimensional approaches. Water Resour. Manag. 30, 823–841. https://doi.org/
10.1007/s11269-015-1193-6.

Zheng, X., Tarboton, D.G., Maidment, D.R., Liu, Y.Y., Passalacqua, P., 2018. River
channel geometry and rating curve estimation using height above the nearest

16

A. Baruah et al.

Environmental Modelling and Software 192 (2025) 106581

drainage. JAWRA J. Am. Water Resour. Associat. 54 (4), 785–806. https://doi.org/
10.1111/1752-1688.12661.

Zhou, Y., Wu, W., Nathan, R., Wang, Q.J., 2021. A rapid flood inundation modelling

framework using deep learning with spatial reduction and reconstruction. Environ.
Model. Software 143, 105112. https://doi.org/10.1016/j.envsoft.2021.105112.

Zhou, Y., Wu, W., Nathan, R., Wang, Q.J., 2022. Deep learning-based rapid flood

inundation modeling for flat floodplains with complex flow paths. Water Resour.
Res. 58 (12), e2022WR033214. https://doi.org/10.1029/2022WR033214.

17

