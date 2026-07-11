Environmental Modelling and Software 196 (2026) 106786

Contents lists available at ScienceDirect

Environmental Modelling and Software

journal homepage: www.elsevier.com/locate/envsoft

A framework for the evaluation of flood inundation predictions over
extensive benchmark databases

, Supath Dhital a, Dinuke Munasinghe a, Sagy Cohen a, Anupal Baruah a,

Dipsikha Devi a,*
Yixian Chen a, Dan Tian a, Carson Pruitt b
a Department of Geography and the Environment, The University of Alabama, Tuscaloosa, USA
b NOAA Office of Weather Prediction Affiliate, Tuscaloosa, USA

A R T I C L E  I N F O

A B S T R A C T

Keywords:
Flood inundation maps
Evaluation
OWP HAND-FIM
Remote sensing

Accurate  Flood  Inundation  Mapping  (FIM)  is  essential  for  forecasting  and  evaluation.  Traditional  pixel-based
approaches can be time-intensive and error-prone. Here, we introduced the Flood Inundation Mapping Evalu-
ation  Framework  (FIMeval),  an  open-source  toolset  for  large-scale  FIM  evaluation.  FIMeval  links  to  a  bench-
marking database that includes high-quality FIM benchmarks across the Contiguous United States, derived from
remote sensing and high-fidelity model-predicted datasets. FIMeval supports pixel-based metrics and integrates
impact-based  assessments  using  building  footprint  data.  We  demonstrated  its  application  using  (a)  high-
resolution aerial imagery FIM for 2016 Midwest Flood (b) remote sensing-derived benchmarks from Hurricane
Matthew (2016), and (b) simulated 100-year and 500-year FIM across 45 Hydrologic Unit Code-8 watersheds
using the Federal Emergency Management Agency’s Base Level Engineering dataset. The NOAA Office of Water
Prediction Height Above Nearest Drainage (OWP HAND-FIM) was the model-predicted FIM for all case studies.
We tested the influence of data-imbalance on the scores using two inbuilt methods.

1. Introduction

Flood Inundation Mapping (FIM) can provide crucial information on
the total area of submergence, depicting hazard zonation, flood water
depth, and flow of the flood water (Büchele et al., 2006; Luu et al., 2018;
Liu et al., 2019) and can be utilized by disaster management authorities
to execute emergency action plans (Lumbroso et al., 2012; Zheng et al.,
2018). FIM can typically be categorized into retrospective FIM (gener-
ated using historical streamflow data), near real-time FIM (FIM gener-
ated  using  remote  sensing),  and  forecasted  FIM  (generated  using
model-forecasted streamflow data).

Remote  Sensing-based  FIM  can  be  a  valuable  asset  for  disaster
response in near real-time and can be used as a Benchmark FIM (B-FIM)
for  evaluating  predictive  models  (Mason  et  al.,  2012;  Giordan  et  al.,
2018; Huang et al., 2018; Shen et al., 2019). It has many advantages in
providing  synoptic  views  of  large-scale  floods  and  providing  FIM  in
ungauged locations. The utility of remote sensing based FIM is affected
by (a) the spatial and temporal resolution of the Earth Observing (EO)
sensor (b) the modality of the EO sensor (optical or Synthetic Aperture
Radar  (SAR))  and  (c)  environmental  conditions  at  the  time  of  image

acquisition. Higher resolution EO sensors capture floods in greater detail
but tend to have lower revisit frequency or high acquisition costs (i.e.,
commercial satellites or aerial photography campaigns). Imagery from
optical EO platforms is susceptible to cloud cover, atmospheric condi-
tions,  and  illumination,  leading  to  obscured  flooded  areas  and  infor-
mation gap during peak flooding (gaps in the flood map). SAR provides
all-weather capability, but is prone to the double bounce phenomenon
(limiting  flood  detection  in  urban  and  vegetated  areas)  and  water
look-a-like  conditions,  increasing  the  false  positives  during  confusion
matrix raster generation (Matikainen et al., 2016; Aasen et al., 2018;
Cohen et al., 2019).Additional uncertainties also arise from mixed pixels
at flood boundaries, temporal mismatch between flood peaks and sat-
ellite  overpasses,  and  limited  ground  observations  for  validation.
Regardless  of  its  source,  comprehensive  post-processing,  including
rigorous  quality  control  of  remote  sensing  products,  is  critical  to
generate a high-quality benchmark dataset from remote sensing imagery
(Barsi et al., 2019; Sumbul et al., 2019).

Model  Predicted  FIM  (M-FIM)  is  essential  for  flood  planning  and
management (Wing et al., 2017; Bates, 2022). Existing approaches to
FIM  generation  include  numerical  methods  (hydrodynamic  models),

* Corresponding author.

E-mail address: ddevi@ua.edu (D. Devi).

https://doi.org/10.1016/j.envsoft.2025.106786
Received 21 June 2025; Received in revised form 24 October 2025; Accepted 13 November 2025
Available online 17 November 2025
1364-8152/© 2025 The Authors. Published by Elsevier Ltd. This is an open access article under the CC BY license ( http://creativecommons.org/licenses/by/4.0/ ).

D. Devi et al.

Environmental Modelling and Software 196 (2026) 106786

low fidelity models (terrain-based models with limited mapping capa-
bilities),  and  deep  learning  and  machine  learning  applications.  The
proliferation of large-scale (national to global) hydrological forecasting
frameworks  necessitates  a  paradigm  shift  in  accuracy  assessment,
enabling the quantification of uncertainty across diverse geographic and
hydrological  settings.  Hydrodynamic  models  generate  FIM  by  solving
one-dimensional or two-dimensional shallow water equations (Stoleriu
et al., 2020; Sosa et al., 2020; Devi et al., 2022; Arash and Yasi, 2023;
Baruah  et  al.,  2024). Models  based  on  terrain, like  the  Height  Above
Nearest  Drainage  (HAND)  (Nobre  et  al.,  2011;  Godbout  et  al.,  2019;
Johnson et al., 2019) and AutoRoute (Follum et al., 2017, 2020), use
stage-discharge  relationships  to  map  river  flow  onto  the  landscape.
Recently,  a  wide  range  of  applications  of  data-driven  models  using
machine  learning  and  deep  learning  have  proven  successful  in  FIM
generation (Bentivoglio et al., 2022; Feng et al., 2023). However, most
of these M-FIM methods have their limitations and, thus, are plagued by
uncertainties. Terrain-based model-derived FIM relies on simple spatial
association  for  flood  extent  generation.  It  can  be  weak  in  predictive
prowess in complex riverine environments (e.g., river confluences, areas
with backwater effects) (Sanders et al., 2024). Purely data-driven ML
methods suffer from knowledge transfer limitations (time and space),
resulting  in  weak  FIM  predictions  for  unseen  locations/conditions.
Increasing diversity of FIM solvers is a welcome trend, which mandates
means for assessing their accuracy (Cohen et al., 2025).

The  accuracy  of  M-FIM  plays  a  pivotal  role  in  operational  flood
forecasting  systems  that  ensure  the  effective  dissemination  of  early
warnings to the communities (Akıncı and Erdo˘gan, 2014; Nevo et al.,
2022). Accurate flood maps help emergency managers identify high-risk
zones  and  plan  evacuations  efficiently.  Overestimations  may  lead  to
unnecessary evacuations, while underestimations can put lives at risk.
For infrastructure protection, authorities use flood maps to design and
construct flood defenses like levees/embankments that can match actual
risk.  Inaccurate  FIM  can  lead  to  under-/over-designed  structures.
Lack/loss of trust in predictive tools is highly detrimental.

Numerous challenges exist while evaluating the accuracy of M-FIM
(Teng et al., 2017; Nikrou et al., 2024) including the lack of standardized
evaluation  metrics  (Cohen  et  al.,  2025),  uncertainty  in  model  input
parameters (Merwade et al., 2008; Papaioannou et al., 2016), sensitivity
to  the  ratio  of  the  wet  to  dry  (W/D)  pixels,  i.e.,  imbalance  between
flooded  and  non-flooded  classes  (Landwehr  et  al.,  2024),  and  lack  of
accurate ground truth information (Bales and Wagner, 2009; Assumpç˜ao
et  al.,  2018).  The  availability  of  high  quality  flood  maps  is  an  indis-
pensable  pre-requisite  for pixel-based  cartographic spatial evaluation.
Enhancing  the  benchmark  FIM  therefore  necessitates  the  systematic
post-processing of raw remote sensing imagery. Several scientific studies
have utilized confusion matrix to perform pixel-based geospatial eval-
uations (Salmon et al., 2015; Scriven et al., 2021; Hooker et al., 2022).
The National Oceanic and Atmospheric Administration (NOAA) Office
of Water Prediction (OWP) has developed a Python-based framework,
‘GVAL’,  to  calculate  the  skill  scores  of  both  binary  and  continuous
geospatial  datasets  by  comparing  the  benchmark  and  a  candidate
dataset
the  manual
pre-processing of M-FIM and B-FIM (in GIS platforms), removal of per-
manent  water  bodies  (PWB)  for  analyses,  can  be  extremely  laborious
and time-consuming, thus hindering evaluation against a large number
of  case  studies  in  a  short  time.  GVAL  lacks  the  capability  for
impact-based assessment utilizing building footprints, whereas FIMeval
incorporates a dedicated module for building-hit evaluation.

(Petrochenkov  et  al.,  2023).  However,

To  address  these  issues  and  improve  the  accuracy  assessments  of
large-scale  FIM  prediction  frameworks,  we  introduce  a  modular  FIM
evaluation  framework,  the  Flood  Inundation  Mapping  Evaluation
Framework  (FIMeval).  FIMeval  is  a  model  and  benchmark-source
agnostic. Here we introduce a new modular and cloud FIM benchmark
database  that  consists  of  FIM  from  various  sources,  including  remote
sensing and model-generated FIM for CONUS. FIMeval is an efficient,
user-friendly, and open-source framework designed to automate M-FIM

evaluation using scalable benchmark datasets. In this paper, we discuss
the data and software architecture of FIMeval, present the methodology
of  M-FIM  evaluation,  and  demonstrate  applications  of  the  framework
using two types of benchmarks: observed (remote sensing) and synthetic
(modeled). The procedure of evaluating FIM includes a pixel-based bi-
nary  confusion  matrix  and  impact-based  assessment  incorporating
building footprint data. Other evaluation approaches and metrics can be
added to the framework through its open-source Python script (Jupyter
Notebook).  We  use  remotely  sensed  B-FIM  as  a  benchmark  for  the
observed flooding to evaluate the OWP HAND-FIM predictions. For in-
dependent validation, we have used a very high resolution FIM gener-
ated from aerial imagery as B-FIM and OWP HAND FIM as M-FIM. For
the synthetic floods, we use simulations of 100-year flood (Scenario (S)
1) and 500-year flood (Scenario (S)2) of the Federal Emergency Man-
agement  Agency’s  (FEMA)  Base  Level  Engineering  (BLE)  product
covering  45  Hydrologic  Unit  Code  (HUC)-8  watersheds  in  the  United
States as benchmarks. We have utilized all the methods of flood extent
extraction  i.e.  Smallest  Extent  (SE),  Convex  Hull  (CH)  and  Area  of
Intereest (AOI) in the cases mentioned above and stated the applicability
and potential use-cases across different types of flood. This paper dem-
onstrates  the  impact  of  data  imbalance  on  the  performance  scores
through  the  application  of  SE  and  CH  across  difference  case  studies.
Through these applications, FIMeval demonstrates its ability to provide
automated  and  reliable  evaluations,  facilitating  consistency  and  scal-
ability in flood evaluation.

2. Methodology

2.1. Flood Inundation Mapping Evaluation Framework (FIMeval)

FIMeval’s underlying principle is based on a pixel-to-pixel compar-
ison between Model-predicted and Benchmark FIMs (M-FIM and B-FIM).
The comparison is initiated by converting M- and B-FIM into a binary
raster representing flooded and non-flooded pixels. Next, the permanent
water bodies (PWB) are eliminated from the binary rasters to only ac-
count for flooded regions in the domain of interest. This is performed by
masking  out  the  permanent  water  bodies  using  a  user-defined  PWB
shapefile. Then, binary rasters M-FIM and B-FIM are superimposed and
compared against each other to create a confusion matrix raster, which
is used to calculate the evaluation metrics. Finally, the confusion matrix
raster is used as a proxy for flood impact assessment by superimposing it
with a ‘Building Footprint’ layer to provide statistics on the building hits
incurred by the specific M-FIM used for comparison. Each of the afore-
mentioned processes is described in detail following the schematic di-
agram  of  the  workflow  in  Fig.  1.  FIMeval  allows  the  comparison  of
multiple M-FIMs  (e.g., FIMs  generated from different models)  against
one benchmark. It is also designed to support the comparison of multiple
case studies at once to enable a consistent analysis of a large number of
case  studies.  The  framework  has  been  successfully  implemented  for
various  M-FIMs  generated  from  HEC-RAS,  LISFLOOD-FP,  and  NOAA
OWP HAND-FIM against high-quality remote sensing B-FIM, which de-
picts its broad applicability over different M-FIM products (Devi et al.,
2024) (Appendix).

The FIMeval framework processing chain follows the seven steps: (1)
Reprojection and Resampling, (2) Conversion to Binary FIM, (3) Selec-
tion  of Area  of Interest, (4) Removal of  Permanent  Water Bodies,  (5)
Generation of the Confusion Matrix Raster (6) Calculation of the eval-
uation metrics (7) Impact analysis using Building Footprints.

Step 1: Reprojection and Resampling

The  framework  initiates  by  processing  the  rasters  for  reprojection
and resampling to align the pixels of the rasters uniformly prior to the
generation of the confusion matrix raster (using the rasterio and pyproj
packages). rasterio handles the pixel alignment properly as long as the
transformation, resolution and resampling method is handled properly

2

D. Devi et al.

Environmental Modelling and Software 196 (2026) 106786

Fig. 1. Flow chart of the flood inundation mapping evaluation framework.

during  reprojection.  It  uses  the  module  calculate_default_transform(),
which computes the new affine transform and dimensions, ensuring the
grid is aligned with the target CRS and resolution, and then it uses the
reproject () to resample the source raster into that aligned grid.

Thus, the rasters are initially reprojected to a specified coordinate
system (projected coordinate system), then resampled to standardized
pixel  sizes.  For  datasets  within  CONUS,  the  framework  will  reproject
both B-FIM and M-FIM rasters to EPSG:5070. The framework also pro-
vides flexibility in specifying a target projected coordinate system and
resolution. If no resolution is provided, the framework will automati-
cally resample all rasters to match the coarsest resolution among them,
ensuring  consistent  spatial  alignment  throughout  the  analysis.  We
evaluated the process using B-FIMs and M-FIMs of varying resolutions to
test its reliability. Results show that even when resampled to the coarsest
resolution, the pixel-based statistics remain consistent, with only trivial
variations  (up  to  the  third  decimal  place),  which  are  considered
insignificant.

Step 2: Conversion to Binary FIM

The B-FIM and M-FIMs are converted into binary FIMs of two classes:
(a) Classes with flooded pixels and (b) classes with non-flooded pixels.
For the B-FIM, the class of flooded pixels is assigned as 2; for the non-
flooded pixels, 0. For the M-FIM, the class of flooded pixels is assigned
as 2, and non-flooded pixels as 1. Thus, the final confusion matrix raster
will  consist  of  four  classes:  1,2,3,  and  4,  representing  True  Negatives
(TN), False Positives (FP), False Negatives (FN), and True Positives (TP),
respectively.

Step 3: Selection of the ‘Area of Interest’

The Area of Interest (AOI), a bounding box of the evaluated domain
extent, plays a significant role when comparing M- and B-FIM, as the
performance scores are sensitive to the area of evaluation. AOI selection
relates to: (a) original extents of M-FIM and B-FIM not identical, thus
requiring  a  common  region  for  comparison,  (b)  user  needs  to  only

compare a specific, smaller region within the larger extents of the M- and
B-FIMs, and (c) to avoid comparing areas with No Data values that skew
accuracy metrics. If there is no clear distinction between non-flooded
and no-data in B-FIM, accurate delineation of the non-flooded portion
becomes challenging. It is also important to note that validation limited
to true positives and false negatives, ignoring the false alarms, may lead
to  misleading  conclusions, as  false alarms  carry  significant inferences
from  a  disaster  response  perspective  provided  the  flood  domain  is
accurately defined. Thus, FIMeval offers three strategies for AOI selec-
tion to accommodate a range of such scenarios (with rasterio, geopandas,
shapely packages), catering to the needs of different use cases described
in detail below.

(i)  User-defined flood extent: The framework allows the users to
input an AOI in a polygon shapefile (Fig. 2a). Accuracy assess-
ment  between  the  M-  and  B-FIMs  will  only  occur  inside  the
boundaries governed by this vector layer. This ensures that the
assessment  remains  relevant  to  the  user’s  region  of  interest,
improving the efficiency and applicability of the accuracy eval-
uation process.

(ii)  The Smallest Extent (SE): The framework detects the region that
is the intersected bounding box among the B-FIM and M-FIMs.
Once  the  region  is  determined,  a  shapefile  is  generated  repre-
senting  this  extent,  which  will  be  utilized  to  demarcate  the
boundaries of B-FIM and M-FIMs (Fig. 2b). In FIM evaluation, the
intersection  of  the  bounding  box  ensures  that  the  comparison
between M-FIM and B-FIM’s flood extent is spatially consistent.
When the spatial extents of the M-FIM and B-FIM differ, direct
comparison can introduce error. Suppose that the domain of the
M-FIM is larger than the B-FIM, the outside area might be counted
as FP. Whereas if the extent of B-FIM is larger than the M-FIM,
then the outside area might be incorrectly counted as FN. Flood
extent comparison suffers from imbalances between dry and wet
pixels. A large bounding box dominated by dry pixels can inflate
the  TN,  thereby  generating  biases  in  the  scores.  Intersected
bounding boxes reduce this issue by restricting the evaluation to a

3

D. Devi et al.

Environmental Modelling and Software 196 (2026) 106786

Fig. 2. Methods of flood extent extraction into the framework: (a) User-defined shapefile of the Area of Interest, (b) Smallest Extent, (c) Convex Hull.

region  where  flooding  is  plausible  in  both  datasets.  By  mini-
mizing  the  evaluation  domain,  the  intersected  bounding  boxes
improve  the  computational  efficiency.  However,  this  approach
has  certain  limitations  and  is  not  universally  applicable  in  all
cases. In some cases of FIM, this method may exclude areas where
flooding  occurs  in  one  dataset  but  not  in  the  other,  thereby
neglecting the overprediction and underprediction.

Convex Hull (CH): FIMeval incorporates an algorithm that gener-
ates the minimum bounding geometry using Convex Hull (CH). The CH
algorithm determines the minimum bounding polygon that encloses a
given set of points. The algorithm will convert all the flood pixels of the
B-FIM into vector point features. From these features, the convex hull is
automatically generated and stored as a polygon shapefile (Fig. 2c). This
polygon vector file is the basis for delineating the flood extents for the B-
FIM and M-FIMs. This algorithm is helpful for large flood maps with high
numbers  of  non-flooded  pixels  by  wrapping  tightly  around  the  flood
extent, unlike SE. CH helps to infer a more realistic flood boundary by
excluding the redundant edge pixels. CH can be applicable to local flood
extents or large basins, adapting to irregular shapes without constraints
on  coordinate  axis  alignment,  unlike  SE.  However,  there  are  various
limitations of this approach. The CH ignores concavities in flood shapes
(e.g.,  meandering  rivers  or  floodplains  with  indentations),  thereby
overgeneralizing the true extent. This simplification may affect accuracy
metrics.

Although  several  limitations  are  associated  with  both  SE  and  CH
approaches,  their  effective  utilization  requires  clear  understanding  of
topographical
the  flood

type  considering  geographical  and

characteristics. The choice between SE and CH can also be utilized by
using the Convexity Ratio (CR), which is the ratio of the area of flood
polygon and the area of convex hull. According to Bozeman and Pilling
(2013),a  polygon  is  considered  nearly  convex  if  CR>=0.5.  It  is  only
convex if CR=1.

Step 4: Removal of Permanent Water Bodies (PWB)

PWB needs to be removed to ensure that only flood water is evalu-
ated. Misclassification of the wet pixels of PWB into the flooded pixel
category can lead to erroneous inferences on floodwater propagation.
Categorizing  the  PWB  clusters  into  non-flooded  pixels  mitigates  this.
FIMeval  can  ingest  any  vector  shapefile  of  PWB  (with  rasterio,  geo-
pandas and shapely packages). By default, using rasterio, if more than
50 % of a pixel overlaps with the PWB layer, it is considered part of the
PWB and excluded; otherwise, it is retained as flooded or non-flooded.
We  have  used  this  default  setting  in  our  framework.  The  ESRI  USA
Detailed  Water  Bodies  dataset  (https://hub.arcgis.com/datasets/
esriusa-detailed-water-bodies/about)
in  this  study.  The
mentioned PWB shapefile of the Contiguous United States (CONUS) is
hosted in an AWS S3 bucket, which allows seamless integration of PWB
into the framework. This allows for efficient access to PWB boundary
data, transferring the data into temporary memory for seamless spatial
analysis and integration. Integrating cloud communication, temporary
file handling, and geospatial processing automates the workflow from
remote  data  acquisition  to  ready-to-use  vector  datasets,  significantly
reducing manual intervention in FIM evaluation.

is  used

4

D. Devi et al.

Environmental Modelling and Software 196 (2026) 106786

Step 5: Generation of Confusion Matrix Raster

The binary B-FIM and M-FIMs are compared using map algebra to
generate the final confusion matrix raster (Fig. 3). The resulting raster
values represent the following classifications: True Positive (TP), False
Positive (FP), True Negative (TN), and False Negative (FN). The B-FIM
contains  two  classes:  flooded  pixels  (value  2)  and  non-flooded  pixels
(value  0). M-FIM  includes  three classes: non-flooded pixels (value 1),
flooded pixels (value 2), and no data (value 0). When the B-FIM and M-
FIM are merged, the final confusion matrix raster generates six distinct
classes: PWB: 5; No-Data: 0; TN: 1; FP: 2; FN: 3; TP: 4. The pixel count for
each class is then utilized to calculate the evaluation metrics.

Step 6: Calculation of the Evaluation Metrics

FIMeval enumerates the total pixel counts of the confusion matrix
raster (i.e., TN, FP, FN, and TP), which are used to calculate evaluation
metrics. A set of evaluation metrics is calculated, including the Accu-
racy, Precision, Sensitivity, Critical Success Index (CSI), Probability of
Detection (POD), F1 values, False Alarm Rate (FAR), False Positive Rate
(FPR), and False Negative Rate (FNR). Additional metrics can easily be
added within the FIMeval code (Jupyter Notebook). For the application
shown in this paper, we utilized four metrics: FPR, F1 score, POD, and
CSI.  FPR  is  used  to  understand  the  false  alarm  rate  over  the  whole
domain (i.e., the pixel counts in M-FIM that are erroneously classified as
water).  The  F1  score  denotes  the  harmonic  mean  of  precision  and
sensitivity. This score is predominantly utilized in imbalanced datasets
(Kamalov et al., 2023; Wang et al., 2024). The POD, also known as Hit
Rate,  measures  how  well  the  model  can  identify  actual  flood  pixels
accurately.  The  CSI  score  measures  the  accuracy  of  the  hits  while
considering  hits,  misses,  and  false  alarms.  The  metric  POD  does  not
penalize  the  false  alarms,  whereas  the  metric  CSI  penalizes  the  false
alarms. The metrics utilized in the study are mentioned in Table 1.

Step 7: Impact Analysis using Building Footprints

Table 1
Description of evaluation metrics utilized in the framework.

Metrics

Formula

Description

False Positive Rate

FP/(FP + TN)

(FPR)
F1 Score

Probability of

Detection (POD)

Critical Success
Index (CSI)

2TP/(2 TP +
FP + FN)

TP/(TP + FN)

TP/(FN + TP
+ FP)

A value of 0 indicates perfect score, 1
indicates remarkably high false alarm.
A value of 1 indicates perfect precision and
recall, 0 indicates poor balance between
precision and recall.
A value of 1 indicates a perfect score,
0 indicate most imperfect score.
A value of 1 indicates perfect TP detection
and 0 indicates no successful detection.

Impact-based assessment is an integral part of emergency managers
executing management strategies. The disaster management authorities
are more likely concerned with the impact-based assessment of build-
ings and transportation (Cohen et al., 2025). Using a building footprint
layer, FIMeval can calculate the number of buildings impacted by B-FIM.
The Microsoft building footprint dataset is used under the Open Data
Commons  Open  Database  License  (https://github.com/microsoft/Glo
balMLBuildingFootprints).  FIMeval  can  also  automate  the  global
building footprint dataset in Google Earth Engine (GEE) (https://gee-co
mmunity-catalog.org/projects/global_buildings/). FIMeval employs the
‘msfootprint’  framework  (Dhital,  S.  2025),  which  optimizes  building
footprint  extraction  through  a  PySpark-based  computational  engine.
This facilitates parallel computation while processing large study areas.
However, the PySpark library often encounters compatibility challenges
on Windows systems and may not function properly as it does on macOS
or LinuxOS. In addition, FIMeval allows the ingestion of a user-provided
building vector file. While comparing the total number of building hits
provides a straightforward evaluation of the count of affected buildings
relative to the B-FIM, such a comparison may introduce biases. In such
cases, identical building counts may sometimes correspond to spatially
different B-FIM and M-FIM flood extents. To address this, FIMeval also
supports a pixel-based evaluation approach that overlays the building
footprints dataset onto the confusion matrix raster. This grants a more

Fig. 3. Generation of the confusion matrix raster.

5

D. Devi et al.

Environmental Modelling and Software 196 (2026) 106786

spatially  explicit  comparison  of  M-FIM  and  B-FIM  performance.  This
paper used CSI, POD, and F1 scores for pixel-based accuracy assessment
of building hits for this exercise.

their local system, input their M-FIM, and run FIMeval automatically,
simplifying the workflow significantly.

2.2. Libraries and packaging

FIMeval is an open-source framework that leverages a wide range of
open-source Python libraries to support different operations for vector
and raster processing. The rasterio library is used for reading, writing,
and masking out rasters. The coordinate projection and transformation
operation of the raster are handled by pyproj. The pyproj, in conjunction
with rasterio, enables the reprojection and transformation of the rasters.
For vector data processing, the libraries shapely and geopandas are used
for geospatial geometry data processing. The module numpy performs
numerical and array operations, whereas the module pandas manages
the  tabular  outputs  from  the  framework  in  the  CSV  format.  The  os
module of Python is used in the framework to interact with the operating
system, such as file and folder manipulation, including the automatic
reading  of  files  from  the  specified  directory.  For  AWS  cloud  storage
integration,  the  code  utilizes  boto3  for  secure  S3  bucket  interactions
using  anonymous  authentication,  ensuring  access  to  public  datasets
without requiring credential management.

Users need to construct a directory structure to run FIMeval. The B-
FIM  and  M-FIMs  must  be  provided  in  geotiff  format.  M-FIMs  from
different  sources  can  be  placed  against  one  B-FIM  within  the  main
directory  for  a  single  case  study.  However,  when  the  user  wishes  to
evaluate multiple case studies, the directory structure follows a nested
format  where  the  main  directory  contains  the  subfolders,  each  corre-
sponding to the individual case studies (Fig. 4). Within each folder of
case studies, the associated B-FIM and M-FIMs are stored in a similar
fashion to that of the single case study. The filename of the B-FIM must
include  the  term  ‘BM’  so  that  the  framework  can  identify  it  as  the
benchmark among all the rasters. Currently, users with their own B-FIM
and  M-FIM  need  to  create  the  folder  structure  manually.  In  a  future
version of FIMeval, the benchmark database will be integrated with a
predefined folder structure. Users will be able to access the database to

Fig.  4. Illustration  of  the  directory  structure  of  FIMeval  for  multiple
case studies.

6

2.3. Benchmarking database

The Benchmarking FIM Database consists of four tiers of benchmark
FIM from various sources, including remote sensing and a high-fidelity
model  FIM.  The  four  tiers  are  classified  based  on  the  quality  of  the
FIM.  Tier  1  FIM  includes  the  hand-labelled  rasters  generated  from
NOAA’s Emergency Response Imagery with a resolution of 40 cm. Tier 2
corresponds  to  the  high-resolution  FIM  generated  from  Planet’s  inte-
grated with a gap-filled algorithm. Tier 3 comprises the FIM generated
from Sentinel-1 integrated with a gap-filled algorithm. Tier 4 features
the synthetic FIM from FEMA’s BLE with a spatial resolution of 10 m on
HUC-8 scale.

2.4. Versions and installation

FIMeval is currently available as (a) a Python package, (b) a Jupyter
notebook,  and  (c)  an  ArcGIS  Pro  Toolbox.  The  GitHub  Repository  of
FIMeval  is  available  at  https://github.com/sdmlua/fimeval.  A sample
code (test_evaluationfim.py) is provided in the GitHub link, depicting
the framework’s modules to run. The complete functionality of the flood
evaluation tools has been divided into a coherent and replicable Python
package by utilizing the Poetry (https://python-poetry.org/) packaging
architecture. Each framework functionality is written as a separate Py-
thon module, which connects them to streamline the framework. Users
can  install  the  package  on  their  local  system  and  cloud  services  like
Google Colab, Cooperative Institute for Research to Operations in Hy-
drology (CIROH) ’s 2i2c cloud computing Jupyter Notebook, etc, using
“pip install fimeval” by setting a Python virtual environment. This will
automatically  download  all  the  dependencies  and  libraries  into  the
system.

All the required arguments of the different modules are listed in the
FIMeval  GitHub  repo. The  steps from 1  to 6  are  performed  using the
EvaluateFIM module (Fig.  5). For  printing the confusion matrix raster
and  the  evaluation  scores  and  storing  them  as  output,  the  modules
PrintContingencyMap  and  PlotEvaluationMetrics  are  used,  respectively.
For  impact-based analysis, the  module EvaluationWithBuildingFootprint
can generate building hit analysis (Step 7) (Fig. 5).

FIMeval  is  also  implemented  as  a  geoprocessing  tool  within  the
ArcGIS Pro software (Fig. 6). This code-free, ‘click and run,’ Graphical
User Interface is envisioned to provide a secondary, GIS software-based
option for flood map comparison and broaden the application to non-
code-savvy users. The tool ingests user-provided benchmark and target
rasters to generate the same output files as the Jupyter notebook (i.e.,
model  agreement  raster,  performance  statistics,  flooded  building
counts).  Currently,  the  ArcGIS  toolbox  operates  using  a  user-defined
shapefile  of  building  footprints.  In  future  versions,  we  plan  to  inte-
grate automated building footprints from the S3 bucket. The tool can
also  generate  a  detailed  Infographic  (Supplementary  Material).  This
capability aids in a) rapid visualization of maps and charts on a single
layout and b) a map layout that facilitates consistency of visualizations
across different flood events. The ArcGIS Toolbox, an installation guide,
and Toolbox Documentation are in the FIMeval GitHub repo.

3. Demonstration of FIMeval applications

We  demonstrate  FIMeval’s  utility  through  an  observed  flood  and
multiple  synthetic  (model-predicted)  flood  cases.  The  NOAA  OWP
developed  an  operational  FIM  framework  that  combines  streamflow
outputs from the US National Water Model (NWM) with the HAND-FIM
model (Maidment, 2017; Cosgrove et al., 2024; Neisary et al., 2025) to
generate FIM at the HUC-8 watershed scale. This framework employs
Synthetic Rating Curves (SRC) derived from reach-averaged parameters
to  translate  streamflow  into  a  stage  and  generate  flood  inundation

D. Devi et al.

Environmental Modelling and Software 196 (2026) 106786

Fig. 5. Screenshot of the FIMeval Jupyter Notebook with notation of the processing steps.

Fig. 6. Screenshot of the ArcGIS toolbox of flood inundation mapping evaluation framework.

rasters (Zheng et al., 2018; Aristizabal et al., 2023). Currently, these FIM
services cover 30 % of the US population, both as a test of their effec-
tiveness  and  as  a  training  tool  for  National  Weather  Service  field
personnel to enhance Impact-Based Decision Support Services in daily
operations (Pruitt et al., 2025). The main advantage of OWP HAND FIM
is its scalability and lower computational expense; however, the model
has  certain
in  under-
prediction/overprediction in flood extent. This model mostly represents
a static flow, unlike the hydraulic models, which use the shallow water

limitations,  which  potentially

result

equation to model the propagation of waves. The 10 m resolution DEMs
currently used in inundation mapping do not capture detailed channel
geometry.  Consequently,  this  lack  of  bathymetric  detail  can  lead  to
overpredictions  of  inundation  extent.  In  addition  to  the  missing  ba-
thymetry,  two  other  major  contributors  to  FIM  extent  error  are  the
reach-averaged slope and the roughness coefficient used in Manning’s
equation.  We  applied  FIMeval  for  historical  (observed)  flooding  and
synthetic (model-predicted) cases. For the historical flood, we used the
case of flooding in the Neuse River, North Carolina, due to Hurricane

7

D. Devi et al.

Environmental Modelling and Software 196 (2026) 106786

Matthew,  which  occurred  from  9th  to  October  15,  2016.  Remote
sensing-derived FIM were employed as benchmarks for 9th, 10th, 14th,
and  October  15,  2016.  We  also  utilized  a  very  high  resolution  FIM
generated from NOAA’s Emergency Response Imagery (ERI) as B-FIM
with  OWP  HAND  FIM  as  M-FIM.  For  the  synthetic  flooding,  we  used
FEMA’s BLE FIM for the B-FIM for the scenarios S1 and S2 against OWP
HAND FIM as M-FIM.

We used the OWP HAND-FIM ‘as a service’ (FIMserv; Baruah et al.,
2025a), an open-source Python toolset, to generate the model-predicted
flood maps (M-FIM). FIMserv supports various functionalities, including
multi-watershed simulation for flood events and processing both retro-
spective  and  forecast  NWM  discharge.  The  model  is  first  set  up  by
identifying the HUC-8 boundaries encompassing the main study area.
The  next  step  involves  extracting  the  NWM  retrospective  streamflow
data linked to the unique ‘River-IDs’ from the FIM’ hydro fabrics.’ These
hydrofabric  datasets  contain  essential  attributes  such  as  the  Relative
Elevation Model (REM) and Height Above Nearest Drainage (HAND) in
both raster and vector formats, accompanied by a CSV file. The CSV file
includes  parameters  such  as  wetted  area,  hydraulic  radius,  wetted
perimeter, roughness, and slope. Using the NWM streamflow data, flood
inundation maps are generated at a spatial resolution of 10 m.

3.1. Historical case studies

We have tested FIMeval with two historical case studies to depict its
broad applicability. In the first case study, the framework was imple-
mented using a remote  sensing-based benchmark dataset of the flood
event that occurred in the Neuse River, North Carolina, US (Fig. 7b), due
to Hurricane Matthew in October 2016. Hurricane Matthew was ranked
as the fourth costliest and fifth-deadliest tropical cyclone on record in
North Carolina. Around 35 km of the river reach was considered for the
flood extent based on the availability of the B-FIM. For the B-FIM, high-
resolution remote-sensing flood maps of Planet satellite extracted from
the FIM database (Tier 2) were utilized for 9th, 10th, 14th, and October
15, 2016. The gaps of the FIM generated from Planet imagery were filled
with  a  hydrologically  guided  region-growth  algorithm  incorporating

high-resolution DEM to enhance the remote sensing flood maps (Tian
et al., 2024).

The  second  case  study  considered  the  2016  Midwest  flood  that
occurred  on  the  Arkansas  River  (FIM  Database  Tier  1).  The  NOAA
Emergency Response Imagery (ERI), collected by the United States Na-
tional  Geodetic  Survey’s  Remote  Sensing  Division,  provides  high-
resolution  aerial  data  over  major  U.S.  flood  events  to  support  home-
land security and emergency operations. Four different image classifi-
cation algorithms (i.e., Maximum Likelihood, Random Forest, Support
Vector  Machine,  and  Unsupervised  classification)  were  used  on  raw
aerial imagery to derive a first-pass flood map. The flood map with the
highest classification accuracy was then selected for further refinement.
An  expert  GIS  analyst  manually  corrected  flooded  and  non-flooded
areas, using the raw aerial imagery as reference. This process involved
working at highly zoomed-in, ground-level detail to generate the final
high-quality benchmark flood map of 40 cm (Chen et al., 2025). The
analysis was done for one case study, as we have one benchmark data for
the  mentioned  date.  For  the  evaluation,  we  already  have  the  exact
boundary of the flooded domain of the benchmark, which consists of the
flooded, non-flooded pixels. We have utilized the ‘AOI’, ’SE’ and ’CH’
methods. We also compared the result with NOAA OWP’s GVAL. For the
generation of the M-FIM, we used the NWM discharge corresponding to
the  flood  period  and  generated  a  series  of  flood  maps.  We  have
considered the flood map as M-FIM whose extent is quite nearer to the
B-FIM.

3.2. Synthetic flooding (HUC-8 watersheds)

The FEMA BLE simulation results are provided at HUC-8 watershed
scales. The BLE production approach leverages high-resolution ground
elevation  data  and  hydraulic  modeling  approaches  to  generate  flood
maps. FEMA developed BLE to provide communities with credible and
accessible  flood  hazard  information  (https://webapps.usgs.gov/infr
m/estbfe/).  The  generation  of  BLE  flood  maps  relies  on  high-
resolution terrain data and hydraulic modeling using HEC-RAS. How-
ever,  these  models  do  not  incorporate  surveyed  cross-sectional

Fig. 7. Study Area (a) 45 HUC-8  watersheds of Region 6  and (b) the Arkansas River Case  Study (2016 Midwest  Flood) (c) the Neuse  River Case Study (Hurri-
cane Matthew).

8

D. Devi et al.

Environmental Modelling and Software 196 (2026) 106786

bathymetric data. The BLE streamflow dataset is primarily derived from
regression  equations  applied  to  USGS  gauges.  For  areas  beyond  the
coverage of these regressions, gauge-based flows are extrapolated using
drainage  area  interpolation  (https://tinyurl.com/32tkc98d,  FEMA
Guidance for Flood Risk Analysis and Mapping). Since these estimates
are grounded in observed gauge data, the associated uncertainty or bias
is generally considered minimal (Baruah et al., 2025b).

For this study, we used publicly available BLE 100-year and 500-year
synthetic flood maps and the associated streamflow data for FEMA Re-
gion 6 from our FIM database (Tier 4). This dataset was selected for its
extensive spatial coverage with available cross-sections and streamflow
information (Aristizabal et al., 2023). We generated OWP HAND-FIM for
45  HUC-8  watersheds,  for  S1  and  S2  scenarios  using  FIMserv  across
Region 6 (Fig. 7a).

4. Results and discussions

4.1. Historical flood case study

4.1.1. 2016 Midwest Flood

The  evaluation  of  the  model-predicted  FIM  (M-FIM)  against  the
benchmark  FIM  (B-FIM)  using  the  EvaluateFIM  module  of  FIMeval
yielded substantial differences in the confusion matrix (Fig. 8a) raster
and performance scores (Fig. 8b). The evaluation of OWP HAND FIM
against the Tier 1 FIM as a benchmark yielded a substantial difference in
the scores. The computational time, memory and the output of the two
frameworks are shown in Table 2.

The performance comparison between GVAL and FIMeval, using the
three built-in methods, showed broadly consistent performance scores.
We have used the same system configuration and the same memory. For
preparing the input data for GVAL, the rasters are pre-processed in Arc
GIS  Pro,  which  includes  converting  the  B-FIM  into  classes  of  0  (non-
flooded) and 2 (flooded), and M-FIM as 1 (non-flooded) and 2 (flooded).
The permanent water bodies are also removed during pre-processing.
The  total computational  time of  GVAL  to  generate the  confusion  ma-
trix and scores was around 127.68 s. However, for FIMeval, the total
elapsed time took 100.33 s, which includes preprocessing of the rasters
like reprojection, resampling, removal of permanent water bodies, and
generating  the  rasters  and  scores  in  geotif  format  and  csv  format,
respectively.

Both frameworks exhibit a similar true positive rate, with Probability
of  Detection  (POD)  remaining  consistent  at  around  71  %  across  all
methods. The Critical Success Index (CSI) and F1 are marginally higher

Table 2
Comparison of FIMeval and GVAL for the 2016 Midwest flood.

Memory

Computational
Time (secs)

CSI

POD

F1
Score

FPR

GVAL

FIMeval
(AOI)
FIMeval
(SE)
FIMeval
(CH)

Mac OS
M2 64 GB
Mac OS
M2 64 GB
Mac OS
M2 64 GB
Mac OS
M2 64 GB

127.68

100.33

102

95

0.637

0.710

0.778

0.107

0.634

0.709

0.776

0.105

0.613

0.709

0.753

0.035

0.615

0.709

0.757

0.108

for GVAL (0.637 and 0.778) and FIMeval-AOI (0.634 and 0.776), indi-
cating balanced performance between hits and false alarms. In contrast,
the FIMeval-SE method yields a slightly lower CSI (0.613) and F1 Score
(0.753), whereas FIMeval-CH also showed a similar score for CSI (0.615)
and F1 Score (0.757). In the context of FPR, similar scores are observed
for  GVAL  (0.107),  FIMeval-AOI  (0.105),  and  FIMeval-CH  (0.108).
However,  a  significant  change  in  the  FPR  is  observed  for  FIMeval-SE
(0.035), indicating a larger domain with an increased number of true
negatives. Since FPR is calculated as FP/(FP + TN), a higher TN count
reduces  the overall ratio. Overall, FIMeval  provides results consistent
with  GVAL  with  reduced  computation  time.  However,  the  evaluation
scores derived from the SE and CH methods are influenced by the spatial
extent of the selected domain.

Apart from the conventional pixel-based statistical analysis, FIMeval
provides  impact-based  secondary  evaluation  using  building  footprint
data  and  the  module  EvaluationWithBuildingFootprint.  This  allows  for
assessing the total number of building hits by both B-FIM and M-FIM,
and  pixel-based  building  hits.  The  Building  Deviation  Ratio  (BDR)
measures how well an M-FIM captures building hit compared to the B-
FIM (Eq. (1)). This index reflects the model’s capability to capture the
exposure of buildings to flood risk.
BDR = No. of Building Hit by MFIM (cid:0) No.of Building Hit by BFIM

(1)

No.of Building Hit by BFIM

The impact-based analysis using building footprint showed that the
building count by the candidate (M-FIM) underpredicts the benchmark
(B-FIM) (Fig. 9 (a)) by 5 % (BDR = (cid:0) 0.05). Considering the building hit/
miss statistics, the scores of CSI, FAR, and POD were estimated as 0.34,
0.472, and 0.49, respectively.

Fig. 8. Results of 2016 Midwest Flood Arkansas from FIMeval using AOI (a) Confusion Matrix Raster (b) Performance Scores.

9

D. Devi et al.

Environmental Modelling and Software 196 (2026) 106786

Fig. 9. (a) Total counts of the flooded buildings inundated by Candidate (M-FIM) and Benchmark (B-FIM) (b) Total counts of the building hit/miss.

Fig. 10. (a) Confusion matrix raster for 9th October with SE (upper extreme left panel),with CH (upper middle left panel), values of CSI, POD, F1 with performance
improvement (%) with CH (bar plot top left of (a)), values of FPR with performance improvement (%) with CH (bar plot bottom left of (a)) (b) Confusion matrix raster
for 10th October with SE (lower extreme left panel),with CH (lower middle left panel), values of CSI, POD, F1 with performance improvement (%) with CH (bar plot
top left of (b)), values of FPR with performance improvement (%) with CH (bar plot bottom left of (b)) (c) Confusion matrix raster for 14th October with SE (upper
extreme right panel),with CH (upper middle right panel), values of CSI, POD, F1 with performance improvement (%) with CH (bar plot top right of (c)), values of FPR
with performance improvement (%) with CH (bar plot bottom right of (c)), (d) Confusion matrix raster for 15th October with SE (lower extreme right panel),with CH
(lower  middle  right  panel),  values  of  CSI,  POD,  F1  with  performance  improvement  (%)  with  CH  (bar  plot  top  right  of  (d)),  values  of  FPR  with  performance
improvement (%) with CH (bar plot bottom right of (d)).

4.1.2. Hurricane Matthew

The EvaluateFIM module of FIMeval was employed for the case study
of Hurricane Matthew, Neuse River, North Carolina produced significant
differences in the performance scores. A high degree of variability in all
the  scores  can  be  observed  across  the  four  benchmarking  dates:  9th,
10th,  14th,  and  October  15,  2016  (Fig.  10).  We  demonstrated  the
analysis using the SE and CH methods of flood domain extraction. On
average, the CH method demonstrated a 7.7 % difference compared to
SE in CSI, POD, and F1 scores across all four dates. When including FPR,
the mean difference was 10.92 % on October 9th, 11.88 % on October
10th,  14.50  %  on  October  14th,  and  2.73  %  on  October  15th.  The
maximum  difference  in  all  the  scores  was  recorded  on  10th  October,
with around 13 % and 8 % higher CSI and F1 scores, respectively, when
using the CH method (Fig. 10b).

The  overall  reduction  in  the  FPR  with  the  CH  method  averaged
approximately 24.6 % across all the dates. The most significant reduc-
tion  in  FPR  was  observed  on  October  14th,  with  a  decrease  of  48  %
(Fig. 10c). This decline in the FPR values reflects lower overpredictions,
suggesting higher accuracy. Despite this improvement, the FPR values
remained very low across all cases, indicating minimal overall influence

10

Table 3
The Building Deviation ratio considering SE and CH for the days.

Date

9th Oct 2016
10th Oct 2016
14th Oct 2016
15th Oct 2016

BDR(SE)

(cid:0) 0.729
1.246
(cid:0) 0.974
(cid:0) 0.833

BDR(CH)

(cid:0) 0.856
1.189
(cid:0) 0.977
(cid:0) 0.833

of FPR on the FIM evaluation. Furthermore, the POD values remained
unchanged  regardless  of  the  methods  employed.  This  indicates  no
variation in the actual positive rate between the CH and SE approaches.
The increase in CH evaluation results is attributed to applying a mini-
mum bounding geometry derived from the B-FIM, which limits the flood
extent and eliminates extraneous edge pixels. This states that the per-
formance  scores  are  highly  sensitive  to  the  flood  domain  utilized  for
evaluation.
The

Eval-
uationWithBuildingFootprint of FIMeval states the BDR using SE and CH
across the mentioned dates are showed in Table 3.

the  module

impact-based

analysis

using

D. Devi et al.

Environmental Modelling and Software 196 (2026) 106786

The  negative  BDR  indicates  that  for  most  dates,  the  number  of
buildings detected by M-FIM underpredicts the buildings detected by B-
FIM. However, an exception was observed on October 10th, where M-
FIM detected a high number of building hits with the BDR for CH lower
than  the  SE.  This  exception  is  likely  due  to  the  peak  flood  on  10th
October, which may have enhanced the model’s ability to capture the
inundation  extent,  thereby  capturing  more  buildings.  The  lower  BDR
values observed with the CH method imply the exclusion of the clipped
buildings from the extraneous edge pixels, which were included in the
SE method.

A pixel-based building hit statistics was conducted to evaluate M-FIM
with B-FIM. The overall score difference (CSI, POD, F1) was estimated to
be  approximately  3.83  %  with  CH  compared  to  the  SE.  The  analysis
states that the estimated scores were very low (0.02–0.39) for all the
mentioned dates, highlighting poor agreement with B-FIM (Fig. 11). The
maximum values for all the scores were observed for 10th October with
a modest difference of 2.10 % for CSI (0.141 (SE); 0.144 (CH)) and 1.83
% (0.246 (SE); 0.25 (CH)) for F1 Score (Fig. 11a; 11(b)). However, no
change was observed in the POD with both CH and SE (Fig. 11c).

The low CSI and negative BDR states that the model was not able to
capture the building level impact. The impact-based building hit anal-
ysis  depends  on  multiple  factors  like  type  of  the  settlement  area,
building density etc. The lower score is not indicative of a limitation in
the statistics but rather an emphasis on differences/inconsistencies in
model  evaluation  approaches.  Cohen  et  al.  (2025) demonstrated  this
more explicitly. This uncovers that for a comprehensive impact-based
assessment, along with the total count of buildings hit by M-FIM and
B-FIM, a pixel-based comparative analysis is also necessary to get a clear
picture of the impact-based assessment.

The computational time taken for FIMeval using EvaluateFIM mod-
ule took nearly 6 min using one method for the generation of perfor-
mance scores (Table 4). This includes the generation of the confusion
matrix raster, all the clipped rasters along with png and csv files. The
computational time required to generate the confusion matrix, and the
performance scores include:

For  building

footprint  analysis  with

the  module  Eval-
uationWithBuildingFootprint, it took around 4 min and 2 s to assess the
building statistics, including the generation of the output CSV and PNG
files.

4.2. Synthetic case studies

4.2.1. Evaluation with Base Level Engineering for 45 HUC8

The M-FIM  (OWP  HAND-FIM) evaluation  against the  B-FIM (BLE)
shows  minimal  differences  in  performance  scores  across  the  HUC-8
watersheds. The overall difference between CH and SE was estimated
as 0.31 % for S1 and 0.32 % for S2 (Fig. 12). The values of the FPR differ
from  a  minimum  of  0.002  to  a  maximum  of  0.073  for  all  the  cases
considered.  The  magnitudes  of  the  FPR  values  are  remarkably  low,
which indicates that the false positives have a minimal impact on overall

performance.

A  marginal  degree  of  variability  in  the  performance  scores  was
observed in the M-FIMs across the HUC-8 watersheds for both SE and CH
methods. The minimal differences is due to at HUC-8 scale, flood extents
are broad and continuous especially in the context of 100-year and 500-
year flood covering large areas. The box plot indicates that the range of
values  for  CSI  and  F1  was  consistent  between  scenarios  S1  and  S2.
However, the median values were increased for S2 (Fig. 12a; Fig. 12c).
The values of all the scores except FPR range from 0.4 to 0.89, which
depicts that the M-FIM demonstrates moderate to high accuracy scores,
though not perfect. For instance, under S1, there was an increment of
0.59 % for CSI and 0.35 % for the F1 score with CH. Similarly, for S2,
with CH, an increase of 0.63 % was estimated for CSI and 0.4 % for F1.
In  the  case  of  POD,  S2  exhibits  an  increased  range  and  a  higher
median value than S1(Fig. 12e). This analysis states that the POD has the
least  influence  on  implemented  methods.  Both  methods  yielded  the
same number of TP, irrespective of the methods employed.

The overall analysis of the 45 HUC-8 watersheds states the marginal
variability of the M-FIM against the B-FIM. An individual analysis of the
percentage improvement of all the HUC-8 was undertaken to test the
difference  between  the  two  methods  utilized  for  evaluation.  The
maximum  difference  in  the  scores  can  be  observed  for  the  HUC-8
13020102  with  CSI  values  of  3.09  %  (S1)  and  3.10  %  (S2)  and  F1
scores of 2.11 % (S1) and 2.16 % (S2) (Fig. 12b; Fig. 12d).

The impact-based evaluation with building footprint states that with
the application of CH, the data points of BDR are more clustered around
0  compared  to  those  of  SE  (Fig.  13).  This  is  because  the  CH  method
excludes the low confidence flooded areas compared to the SE method.
From the box plot, it can be ascertained that the maximum positive value
was estimated as 0.73 for both SE and CH, and the maximum negative
BDR was (cid:0) 4.18 for SE and (cid:0) 1.11 for CH (Fig. 13e). Similarly, for S2, the
maximum  negative  values  of  BDR  were  estimated  as  (cid:0) 3.86  (SE)  and
(cid:0) 0.97 (CH) (Fig. 13f). The maximum positive BDR value remained the
same for both methods at 0.71.

The pixel-based building hit statistics highlight the variability in the
performance scores. There was a significant increase in the ranges of the
scores for S2 compared to S1 as per the KDE plots (Fig. 13). For S1, there
is a minute change in the data range of the CSI for both methods (3 %
change in the mean). However, the ranges of the CSI values can be seen
increasing for the S2 compared to the S1 (Fig. 13a). Considering the F1
score, the difference in the mean value for both methods was estimated
to be around 2.49 % for S1. In S2, however, the differences were trivial,
with an increase of only 0.013 % in the mean. Regarding the POD, the
mean values were the same for both S1 and S2, considering SE and CH
(Fig. 13c).

4.2.2. Computational efficiency of FIMeval

Using the FIMeval framework with one method, the computational
time required to estimate pixel-based evaluation scores for the 45 HUC-8
watersheds,  including  the  generation  of  confusion  matrix  rasters  in

Fig. 11. Performance Scores considering building hits analysis (a) CSI, (b) F1 Score, (c) POD.

11

D. Devi et al.

Environmental Modelling and Software 196 (2026) 106786

Table 4
Computational time in secs against the number pixels within the area of interest.

Computational Time (secs) (SE)

No. of pixels (SE)

Computational Time(secs) (CH)

No. of pixels (CH)

Oct 9, 2016
Oct 10, 2016
Oct 14, 2016
Oct 15, 2016

80
70
81
91

5,844,832
4,428,554
4,603,058
7,728,384

89
91
95
96

1,855,112
1,504,247
2,313,156
3,368,433

Fig. 12. (a) Box Plot of CSI for S1 (left panel) and S2 (right panel) (b) Spatial Distribution of the mean percentage improvement in CSI for S1 (left panel) S2 (right
panel) (c) Box Plot of F1 values for S1 (left panel) and S2 (right panel) (d) Spatial Distribution of the mean percentage improvement in F1 values for S1 (left panel) S2
(right panel) (e) Box Plot of POD values for S1 (left panel) and S2 (right panel) (f) Spatial Distribution of the mean percentage improvement in POD values for S1 (left
panel) S2 (right panel) (g) Box Plot of FPR values for S1 (left panel) and S2 (right panel) (h) Spatial Distribution of the mean percentage improvement in FPR values
for S1 (left panel) S2 (right panel).

12

D. Devi et al.

Environmental Modelling and Software 196 (2026) 106786

Fig. 13. (a) CSI for SE and CH for 100 years return period flow (KDE-Box plots left panel) 500 years return period flow (KDE-Box plots right panel) (b) F1score for SE
and CH for 100 years return period flow (KDE-Box plots left panel) 500 years return period flow (KDE-Box plots right panel) (c) POD score for SE and CH for 100
years return period flow (KDE-Box plots left panel) 500 years return period flow (KDE-Box plots right panel) (e) Box Plot of BDR for S1 (f) Box Plot of BDR for S2.

Fig. 14. Computational time v/s the number of pixels in AOI (a) Using Smallest Extent (b) Using Convex Hull.

geotiff format along with the png and csv outputs, was approximately 1
h  and  4  min.  The  computational  time  to  generate  only  the  confusion
matrix and the performance scores against the total number of pixels
inside the flood domain is shown in Fig. 14 for the 45 HUC8 considering
SE and CH.

In addition, for the building footprint analysis, the processing time
took around an additional 2 h and 95 min. The primary reason for this
computational  demand  is  the  spatial  extent  of  the  watersheds,  which
ranges  from  1769.4  km2  to  8429.22  km2,  thereby  reflecting  the  sub-
stantial size of the catchments.

5. Conclusions

We present a novel framework for the evaluation of Flood Inundation
Maps (FIM).  The framework,  FIMeval,  streamlines evaluation  proced-
ures for a large number of case studies with diverse benchmark datasets.
FIMeval  is  based  on  an  open-source  (Python)  Jupyter  Notebooks,  of-
fering a highly modular and customizable interface. The FIMeval Python
package  was  developed  to  be  compatible  with  cloud  computing  plat-
forms like CIROH’s 2i2c and Google Colab, thereby depicting its flexi-
bility  and  usability.  Additional  functionality  of  this  framework  is  the

13

D. Devi et al.

Environmental Modelling and Software 196 (2026) 106786

built-in methods for automatic flood extent delineation. Apart from the
statistical  analysis  of  the  flooded  pixels  using  the  confusion  matrix,
FIMeval also offers an evaluation procedure based on building impact.
The framework was demonstrated using three types of case studies:
optical remote-sensing and aerial imagery derived benchmarks of his-
torical flood events, and 100 and 500-yr simulations of a high-fidelity
model  over  multiple  large  catchments.  These  case  studies  were  uti-
lized to study the impact of flood extent delineation methods on FIM
evaluation  outcomes. Results stated that significant  differences in the
scores  were  observed  while  applying  the  two  methods,  Convex  Hull
(CH) and Smallest Extent (SE). The overall difference in the scores (CSI,
POD, F1) with CH was estimated to be approximately 7.7 % compared to
SE,  for the historical benchmarks. For the simulated benchmarks, the
rate of change of CH with respect to SE was only about 0.3 % on average.
This states that the performance metrics of the pixel-based FIM evalu-
ation is highly sensitive to the extent of the flood. Evaluation using the
building footprint provides another perspective on model-predicted FIM
(M-FIM) accuracy. For the historical case study, a minor variation in the
buildings can be seen with both extent delineation methods. During the
peak  flow,  the  M-FIM  overpredicts  B-FIM,  with  CH  yielding  fewer
accurately  detected  buildings.  In  the  synthetic  flooding  scenario,  the
range of BDR values with CH concentrates near zero compared to SE,
leading to a significantly lower underprediction.

The use of SE and CH in our study is intended to address the choice of
evaluation  domain  influences  performance  metrics  in  pixel-based  as-
sessments.  While  these  methods  offer  practical  alternatives  when  the
actual flood extent is unavailable, they come with inherent limitations.
Their effectiveness greatly relies on the floodplain geometry and user’s
understanding of the flood patterns. Among the available approaches,
the method ‘AOI’ is the most accurate as it clearly distinguishes between
flooded and non-flooded pixels. The utilization of SE and CH are based
on the flood pattern and the expertise of the users if the actual domain is
not  available.  When  SE  or  CH  is  used,  it  becomes  crucial  to  select
evaluation  metrics  that  are  less  sensitive  to  domain-related  biases.
Metrics such as CSI, POD, and F1 Score, which are independent of true
negatives, may be less affected by large dry areas and thus offer more
reliable comparisons.

The  analyses  performed  in  this  paper  highlighted  the  challenges
associated with the FIM evaluation and the necessity of a systematic FIM
evaluation  requirement.  The  metrics  utilized  in  the  quantitative
assessment from the confusion matrix are accompanied by biases asso-
ciated  with  data  imbalance  of  flooded  and  non-flooded  pixel  classes.
There is a lack of standards for utilizing these metrics. Therefore, eval-
uating FIM solely based on these statistical metrics may not generate a
comprehensive understanding of the actual flooding impact. Therefore,
additional  evaluation  of  FIM  based  on  impact-based  assessment  is
necessary.  However,  the  pixel-based  building  hit/miss  statistics  are
influenced  by  multiple  factors  including  the  type  of  settlement  area
(urban, suburban, rural), building density and size of the study area. In
addition  to  the  traditional  pixel-based  approach,  an  object-based
method  can  be  integrated  to  provide  a  more  comprehensive  under-
standing of FIM evaluation. We plan to incorporate an object-based FIM
evaluation  strategy  into  future  versions  of  FIMeval,  which  will  help
reduce the biases associated with traditional pixel-based assessments.

the large-scale FIM database, which will streamline the process of FIM
evaluation. This database already follows a specific naming convention,
allowing FIMeval to operate without requiring users to rename the B-
FIM. We plan to incorporate the evaluation strategy presented in Cohen
et al. (2025) which excludes pixels that were classified as flooded by the
RS-FIM enhancement algorithm (region-growing in this paper). Future
work  also  involves  linking  FIMeval  with  FIMserv,  which  will  help
generate  the  NOAA  OWP  HAND  FIM  and  its  evaluation  against  the
high-quality benchmark datasets.

CRediT authorship contribution statement

Dipsikha Devi: Writing –  original draft, Visualization, Validation,
Methodology,  Data  curation,  Conceptualization.  Supath  Dhital:
Writing  –  review  &  editing,  Visualization,  Software,  Methodology.
Dinuke Munasinghe: Writing – review & editing, Validation, Software,
Methodology.  Sagy  Cohen:  Writing  –  review  &  editing,  Supervision,
Resources, Investigation, Funding acquisition, Conceptualization. Anu-
pal  Baruah:  Writing  –  review  &  editing,  Validation,  Methodology.
Yixian Chen: Writing – review & editing, Validation, Methodology. Dan
Tian: Writing – review & editing, Validation, Resources. Carson Pruitt:
Resources, Methodology, Data curation.

Software and data availability

• Name of software: FIMeval
• Developers: Dipsikha Devi, Supath Dhital
• Contact:ddevi@ua.edu,  sdhital@crimson.ua.edu,  sagy.cohen@ua.

edu

• Software required: Anaconda
• Program language: Python
• Source code at: https://github.com/sdmlua/fimeval
• Documentation:  Detailed  documentation  of  the  framework,  its
application,  and  installation  can  be  found  at:  https://github.com/
sdmlua/fimeval/README.md

• FIMeval in PyPI repository: https://pypi.org/project/fimeval/
• FIMeval  listing  on  CIROH  DocuHub:  https://docs.ciroh.org/do

cs/products/community-fim/fimeval/

Declaration of competing interest

The authors declare that they have no known competing financial
interests or personal relationships that could have appeared to influence
the work reported in this paper.

Acknowledgement

Funding for this project was provided by the National Oceanic and
Atmospheric Administration (NOAA) and awarded to the Cooperative
Institute for Research to Operations in Hydrology (CIROH) through the
NOAA  Cooperative  Agreement  with  The  University  of  Alabama
(NA22NWS4320003).

This  work  utilized  data  made  available  through  the  NASA  Com-

Further enhancement of the framework includes the integration of

mercial Smallsat Data Acquisition (CSDA) Program.

14

D. Devi et al.

Environmental Modelling and Software 196 (2026) 106786

APPENDIX

Fig. 1. Output from ArcGIS toolbox.

Fig. 2. Outputs from FIMeval from different M-FIMs for Hurricane Matthew, Oct 15, 2016 using SE (a) Confusion Matrix Raster (b) Performance Metrics (c) Building
Hit Statistics (Devi et al., 2024).

15

D. Devi et al.

Environmental Modelling and Software 196 (2026) 106786

Fig. 3. Outputs from FIMeval from different M-FIMs for Hurricane Matthew, Oct 15, 2016 using CH (a) Confusion Matrix Raster (b) Performance Metrics (c) Building
Hit Statistics (Devi et al., 2024).

Data availability

I have shared the link of the code in the paper.

References

Aasen, H., Honkavaara, E., Lucieer, A., Zarco-Tejada, P.J., 2018. Quantitative remote

sensing at ultra-high resolution with UAV spectroscopy: a review of sensor
technology, measurement procedures, and data correction workflows. Remote Sens.
10 (7), 1091.

Akıncı, H., Erdo˘gan, S., 2014. Designing a flood forecasting and inundation-mapping

system integrated with spatial data infrastructures for Turkey. Nat. Hazards 71 (1),
895–911.

Arash, A.M., Yasi, M., 2023. The assessment for selection and correction of RS-based

DEMs and 1D and 2D HEC-RAS models for flood mapping in different river types.
J. Flood Risk Manag. 16 (1), e12871.

Aristizabal, F., Salas, F., Petrochenkov, G., Grout, T., Avant, B., Bates, B., et al., 2023.
Extending height above nearest drainage to model multiple fluvial sources in flood
inundation mapping applications for the US National Water model. Water Resour.
Res. 59 (5) e2022WR032039.

Assumpç˜ao, T.H., Popescu, I., Jonoski, A., Solomatine, D.P., 2018. Citizen observations
contributing to flood modelling: opportunities and challenges. Hydrol. Earth Syst.
Sci. 22 (2), 1473–1489.

Bales, J.D., Wagner, C.R., 2009. Sources of uncertainty in flood inundation maps.

J. Flood Risk Manag. 2 (2), 139–147.

Barsi,

´
A., Kugler, Z., Juh´asz, A., Szab´o, G., Batini, C., Abdulmuttalib, H., et al., 2019.
Remote sensing data quality model: from data sources to lifecycle phases. Int. J.
Image Data Fusion 10 (4), 280–299.

Baruah, A., Barman, D., Arjun, B.M., Chyne, B.L., Aggarwal, S.P., 2024. Holistic

framework for flood hazard assessment in a trans-boundary basin. Acta Geophys. 72
(2), 1017–1032.

Baruah, A., Dhital, S., Cohen, S., Nhan, T., Tran, D., Elhaddad, H., et al., 2025a. FIMserv
v. 1.0: a tool for streamlining Flood Inundation Mapping (FIM) using the United
States operational hydrological forecasting framework. Environ. Model. Software,
106581.

Baruah, A., Spies, R., Devi, D., Cohen, S., Aristizabal, F., Nikrou, P., et al., 2025b.
Predicting synthetic rating curve adjustment factors with explainable machine
learning for enhancing the United States operational flood inundation mapping
framework. J. Hydrol., 134086

Bates, P.D., 2022. Flood inundation prediction. Annu. Rev. Fluid Mech. 54 (1), 287–315.
Bentivoglio, R., Isufi, E., Jonkman, S.N., Taormina, R., 2022. Deep learning methods for
flood mapping: a review of existing applications and future research directions.
Hydrol. Earth Syst. Sci. Discuss. 2022, 1–50.

Bozeman, J.R., Pilling, M., 2013. The convexity ratio and applications. Sci. Math. Jpn. 76

(1), 47–53.

Büchele, B., Kreibich, H., Kron, A., Thieken, A., Ihringer, J., Oberle, P., et al., 2006.

Flood-risk mapping: contributions towards an enhanced assessment of extreme
events and associated risks. Nat. Hazards Earth Syst. Sci. 6 (4), 485–503.

Chen, Y., Cohen, S., Baruah, A., Devi, D., Dhital, S., Tian, D., Munasinghe, D., 2025.

Merging remote sensing derived river slope datasets with high-resolution
hydrofabrics for the United States. Sci. Data 12 (1), 1657.

Cohen, S., Baruah, A., Nikrou, P., Tian, D., Liu, H., 2025. Toward robust evaluations of
flood inundation predictions using remote sensing derived benchmark maps. Water
Resour. Res. 61 (8), e2024WR039574.

16

Cohen, S., Raney, A., Munasinghe, D., Loftis, J.D., Molthan, A., Bell, J., et al., 2019. The
floodwater depth estimation tool (FwDET v2. 0) for improved remote sensing
analysis of coastal flooding. Nat. Hazards Earth Syst. Sci. 19 (9), 2053–2065.
Cosgrove, B., Gochis, D., Flowers, T., Dugger, A., Ogden, F., Graziano, T., et al., 2024.

NOAA’s National Water model: advancing operational hydrology through
continental-scale modeling. JAWRA J. Am Water Res. Associat. 60 (2), 247–272.

Devi, D., Baruah, A., Sarma, A.K., 2022. Characterization of dam-impacted flood

hydrograph and its degree of severity as a potential hazard. Nat. Hazards 112 (3),
1989–2011.

Devi, D., Baruah, A., Nikrou, P., Cohen, S., 2024. FIMPEF: a framework for automatic
evaluation of flood inundation mapping predictions over large and scalable
benchmark datasets. AGU24.

Dhital, S., 2025. Msfootprint: a Python package for extracting Microsoft’s global building
footprints based on user-defined boundaries. Zenodo. https://doi.org/10.5281/
zenodo.14597326, v0.1.24.

Feng, D., Tan, Z., He, Q., 2023. Physics-informed neural networks of the saint-venant

equations for downscaling a large-scale River model. Water Resour. Res. 59 (2)
e2022WR033168.

Follum, M.L., Tavakoly, A.A., Niemann, J.D., Snow, A.D., 2017. AutoRAPID: a model for
prompt streamflow estimation and flood inundation mapping over regional to
continental extents. JAWRA J. Am Water Res. Associat. 53 (2), 280–299.

Follum, M.L., Vera, R., Tavakoly, A.A., Gutenson, J.L., 2020. Improved accuracy and

efficiency of flood inundation mapping of low-, medium-, and high-flow events using
the AutoRoute model. Nat. Hazards Earth Syst. Sci. 20 (2), 625–641.

Giordan, D., Notti, D., Villa, A., Zucca, F., Cal`o, F., Pepe, A., et al., 2018. Low cost,
multiscale and multi-sensor application for flooded area mapping. Nat. Hazards
Earth Syst. Sci. 18 (5), 1493–1516.

Godbout, L., Zheng, J.Y., Dey, S., Eyelade, D., Maidment, D., Passalacqua, P., 2019. Error

assessment for height above the nearest drainage inundation mapping. JAWRA J.
Am Water Res. Associat. 55 (4), 952–963.

Hooker, H., Dance, S.L., Mason, D.C., Bevington, J., Shelton, K., 2022. Spatial scale

evaluation of forecast flood inundation maps. J. Hydrol. 612, 128170.
Huang, X., Wang, C., Li, Z., 2018. A near real-time flood-mapping approach by

integrating social media and post-event satellite imagery. Annals GIS 24 (2),
113–123.

Johnson, J.M., Munasinghe, D., Eyelade, D., Cohen, S., 2019. An integrated evaluation of
the national water model (NWM)–height above nearest drainage (HAND) flood
mapping methodology. Nat. Hazards Earth Syst. Sci. 19 (11), 2405–2420.
Kamalov, F., Thabtah, F., Leung, H.H., 2023. Feature selection in imbalanced data.

Annals Data Sci. 10 (6), 1527–1541.

Landwehr, T., Dasgupta, A., Waske, B., 2024. Towards robust validation strategies for EO

flood maps. Rem. Sens. Environ. 315, 114439.

Liu, J., Xu, Z., Chen, F., Chen, F., Zhang, L., 2019. Flood hazard mapping and assessment

on the Angkor world heritage site, Cambodia. Remote Sens. 11 (1), 98.

Lumbroso, D.M., Di Mauro, M., Tagg, A.F., Vinet, F., Stone, K., 2012. FIM FRAME: a

method for assessing and improving emergency plans for floods. Nat. Hazards Earth
Syst. Sci. 12 (5), 1731–1746.

Luu, C., Von Meding, J., Kanjanabootra, S., 2018. Assessing flood hazard using flood

marks and analytic hierarchy process approach: a case study for the 2013 flood event
in Quang Nam, Vietnam. Nat. Hazards 90, 1031–1050.

Maidment, D.R., 2017. Conceptual framework for the national flood interoperability

experiment. J. Am. Water Resour. Assoc. 53 (2), 245–257.

Mason, D.C., Davenport, I.J., Neal, J.C., Schumann, G.J.P., Bates, P.D., 2012. Near real-
time flood detection in urban and rural areas using high-resolution synthetic
aperture radar images. IEEE Trans. Geosci. Rem. Sens. 50 (8), 3041–3052.

D. Devi et al.

Environmental Modelling and Software 196 (2026) 106786

Matikainen, L., Lehtom¨aki, M., Ahokas, E., Hyypp¨a, J., Karjalainen, M., Jaakkola, A.,
et al., 2016. Remote sensing methods for power line corridor surveys. ISPRS J.
Photogrammetry Remote Sens. 119, 10–31.

Merwade, V., Olivera, F., Arabi, M., Edleman, S., 2008. Uncertainty in flood inundation
mapping: current issues and future directions. J. Hydrol. Eng. 13 (7), 608–620.
Neisary, S.N., Johnson, R.C., Alam, M.S., Burian, S.J., 2025. A post-processing machine
learning framework for bias-correcting National Water model outputs by accounting
for dominant streamflow drivers. Environ. Model. Software 190, 106459.

Nevo, S., Morin, E., Gerzi Rosenthal, A., Metzger, A., Barshai, C., Weitzner, D., et al.,

2022. Flood forecasting with machine learning models in an operational framework.
Hydrol. Earth Syst. Sci. 26 (15), 4013–4032.

Nikrou, P., Baruah, A., Gangrade, S., Kao, S.C., Seyvani, S., Tian, D., Cohen, S., 2024.

Comparative analysis of flood inundation mapping techniques: evaluating
hydrodynamic and terrain-based models for enhanced precision and efficiency using
remote sensing. In: AGU Fall Meeting Abstracts.

Nobre, A.D., Cuartas, L.A., Hodnett, M., Renn´o, C.D., Rodrigues, G., Silveira, A.,

Saleska, S., 2011. Height above the nearest Drainage–a hydrologically relevant new
terrain model. J. Hydrol. 404 (1–2), 13–29.

Papaioannou, G., Loukas, A., Vasiliades, L., Aronica, G.T., 2016. Flood inundation

mapping sensitivity to riverine spatial resolution and modelling approach. Nat.
Hazards 83, 117–132.

Petrochenkov, G., Aristizabal, F., Salas, F.R., 2023. GVAL: a python package for model
agnostic geospatial evaluations using open-source, cloud-native technologies. In:
AGU Fall Meeting Abstracts, 2023. IN21A-07.

Pruitt, C., Giardino, D., Salas, F., Spies, R., Hanna, R., Luck, M., et al., 2025.

Improvements in continental-scale flood inundation mapping at NOAA’s office of
water prediction. In: 105th AMS Annual Meeting. AMS.

Salmon, B.P., Kleynhans, W., Schwegmann, C.P., Olivier, J.C., 2015. Proper comparison

among methods using a confusion matrix. In: 2015 IEEE International Geoscience
and Remote Sensing Symposium (IGARSS). IEEE, pp. 3057–3060.

Sanders, B.F., Wing, O.E., Bates, P.D., 2024. Flooding is not like filling a bath. Earths

Future 12 (12) e2024EF005164.

Scriven, B.W.G., McGrath, H., Stefanakis, E., 2021. GIS derived synthetic rating curves

and HAND model to support on-the-fly flood mapping. Nat. Hazards 109,
1629–1653.

Shen, X., Anagnostou, E.N., Allen, G.H., Brakenridge, G.R., Kettner, A.J., 2019. Near-

real-time non-obstructed flood inundation mapping using synthetic aperture radar.
Rem. Sens. Environ. 221, 302–315.

Sosa, J., Sampson, C., Smith, A., Neal, J., Bates, P., 2020. A toolbox to quickly prepare

flood inundation models for LISFLOOD-FP simulations. Environ. Model. Software
123, 104561.

Stoleriu, C.C., Urzica, A., Mihu-Pintilie, A., 2020. Improving flood risk map accuracy

using high-density LiDAR data and the HEC-RAS river analysis system: a case study
from north-eastern Romania. J. Flood Risk Manag. 13, e12572.

Sumbul, G., Charfuelan, M., Demir, B., Markl, V., 2019. Bigearthnet: a large-scale

benchmark archive for remote sensing image understanding. In: IGARSS 2019-2019
IEEE International Geoscience and Remote Sensing Symposium. IEEE,
pp. 5901–5904.

Teng, J., Jakeman, A.J., Vaze, J., Croke, B.F., Dutta, D., Kim, S.J.E.M., 2017. Flood
inundation modelling: a review of methods, recent advances and uncertainty
analysis. Environ. Model. Software 90, 201–216.

Tian, D., Liu, H., Wang, L., Cohen, S., Thapa, P., 2024. Enhancing satellite image-derived
flood maps with hydrologically guided region growing method and high-resolution
DEMs. In: Chapman Conference on Remote Sensing of the Water Cycle. AGU.
Wang, H., Meng, Y., Xu, H., Wang, H., Guan, X., Liu, Y., et al., 2024. Prediction of flood
risk levels of urban flooded points though using machine learning with unbalanced
data. J. Hydrol. 630, 130742.

Wing, O.E., Bates, P.D., Sampson, C.C., Smith, A.M., Johnson, K.A., Erickson, T.A., 2017.
Validation of a 30 m resolution flood hazard model of the conterminous United
States. Water Resour. Res. 53 (9), 7968–7986.

Zheng, X., Maidment, D.R., Tarboton, D.G., Liu, Y.Y., Passalacqua, P., 2018. GeoFlood:
large-scale flood inundation mapping based on high-resolution terrain analysis.
Water Resour. Res. 54 (12), 10–13.

17

