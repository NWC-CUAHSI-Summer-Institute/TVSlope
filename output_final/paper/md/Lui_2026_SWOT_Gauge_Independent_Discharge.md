manuscript submitted to Water Resources Research

A SWOT-Based Framework for Gauge-Independent River Discharge Estimation

Huaichuan Liu1, 2, Di Long1, 2*, Chenqi Fang1, 2, Qi Huang3, 4, and Xingdong Li5

1 State Key Laboratory of Hydroscience and Engineering, Department of Hydraulic Engineering,
Tsinghua University, Beijing 100084, China
2 Key Laboratory of Hydrosphere Sciences of the Ministry of Water Resources, Tsinghua
University, Beijing 100084, China
3 Key Laboratory of Groundwater Conservation of Ministry of Water Resources, China
University of Geosciences, Beijing 100083, China
4 School of Water Resources and Environment, China University of Geosciences, Beijing
100083, China
5 State Key Laboratory of Water Cycle and Water Security, China Institute of Water Resources
and Hydropower Research, Beijing 100038, China

Corresponding author: Di Long (dlong@tsinghua.edu.cn)

Key Points:

  An ungauged framework for river discharge estimation was developed using SWOT

observations and a modified MetroMan algorithm.

  Width refinement using an automated extraction procedure substantially improves

framework performance and applicability.

  Historical river discharge was successfully reconstructed using Sentinel-3, with

implications for long-term hydrological research.

Keywords:

Hydrological monitoring,

SWOT,

Interferometric altimetry,

River discharge estimation,

Gauge-independent framework,

Discharge reconstruction

1

2

3
4

5
6

7
8

9
10

11
12

13

14

15
16

17
18

19
20

21

22

23

24

25

26

27

manuscript submitted to Water Resources Research

28

29
30
31
32
33
34
35
36
37
38
39
40
41
42
43
44
45
46
47
48

49

50
51
52
53
54
55
56
57
58
59
60
61
62
63
64
65

66

67
68
69
70
71

Abstract

The declined accessibility of in-situ water records has limited our ability to monitor river dynamics
and  manage  freshwater  resources.  Satellite  altimetry  provides  an  important  alternative,  but
traditional radar altimeters can only observe rivers at nadir points where the ground track crosses
the channel, offering sparse spatial coverage. The Surface Water and Ocean Topography (SWOT)
mission,  launched  in  December  2022,  marks  a  major  advance  by  delivering  wide-swath
observations,  simultaneously  measuring  water  surface  elevation,  water  surface  slope,  and  river
width, thereby  enabling discharge estimation independent of gauge data.  This study develops a
fully satellite-based framework to retrieve discharge using SWOT observations, which consists of
three  key  steps:  (1)  selecting  continuous  river  reaches,  (2)  assembling  high-quality  SWOT
observation time-space arrays, and (3) estimating discharge using a modified MetroMan algorithm.
Notably, an automated  width extraction procedure is applied to refine SWOT-observed widths.
Validation  across  391  gauging  stations  (42–1741  m  wide)  achieved  a  median  Nash–Sutcliffe
efficiency  (NSE)  of  0.30  and  a  median  Kling–Gupta  Efficiency  (KGE)  of  0.42.  Comparisons
demonstrate that width refinement is the primary driver of performance improvement, contributing
median  NSE  and  KGE  gains  of  0.37  and  0.23,  respectively.  Furthermore,  historical  discharge
reconstruction  was  achieved  by  integrating  Sentinel-3  water  levels  into  our  SWOT-based
framework, attaining a median NSE of 0.67 and a median KGE of 0.65 across 122 river reaches.
This  work  demonstrates  that  SWOT  can  generate  accurate,  gauge-independent  discharge  time
series and provides a foundation for long-term hydrologic monitoring and climate studies in data-
scarce regions.

Plain Language Summary

Rivers  are vital  for  people  and  ecosystems.  They  provide  drinking  water,  support  farming  and
energy production, and sustain biodiversity. Measuring how much water flows in rivers, known as
discharge, has become even more important as climate change drives more frequent floods and
droughts.  In  December  2022,  the  Surface  Water  and  Ocean  Topography  (SWOT)  satellite was
launched. SWOT captures wide swaths of Earth, up to 120 kilometers with a 20 km nadir gap, and
measures water elevation, slope, and width at the same time, allowing discharge to be estimated
even where no ground gauges exist. In this study, we developed a framework that uses only SWOT
observations  to  estimate  discharge  by  applying  mass  conservation  across  neighboring  river
reaches. Tests against 391 stations yielded positive Nash–Sutcliffe Efficiency (NSE) and Kling–
Gupta  Efficiency  (KGE)  values  for  61%  and  75%  reaches,  respectively,  indicating  that  our
framework  performs  well  across  rivers  with  diverse  shapes  and  sizes.  The  accuracy  improved
notably  when  river  width  measurements  were  carefully  refined,  with  median  NSE  and  KGE
increasing  by  0.37  and  0.23,  respectively.  We  also  show  that  combining  SWOT  with  earlier
satellites  can  extend  discharge  estimates  into  the  past.  Together,  these  results  demonstrate  that
SWOT  can  deliver  reliable,  gauge-independent  monitoring  of  river  discharge,  particularly  in
regions with little or no ground data.

1 Introduction

In the context of global climate warming, the frequency and intensity of regional droughts
and floods have been increasing, placing unprecedented stress on the stability of the hydrological
cycle (Bloeschl et al., 2019; Perkins-Kirkpatrick et al., 2024). As such extreme events are projected
to intensify in the future (Kreibich et al., 2022), observations over river networks have become
increasingly  critical  to  ensure freshwater  security  and  biodiversity  (Gudmundsson  et  al.,  2021;

manuscript submitted to Water Resources Research

72
73
74
75
76
77
78
79
80
81
82

83
84
85
86
87
88
89
90
91
92
93
94
95
96
97
98
99
100
101

102
103
104
105
106
107
108
109
110
111
112
113
114
115
116
117

Vörösmarty  et  al.,  2010).  Streamflow,  as  one  of  the  most  fundamental  hydrological  variables,
forms the foundation for water resources management, as well as flood forecasting and mitigation
(Cerbelaud et al., 2025). However, the accessibility of in-situ gauging data from global monitoring
network has  been steadily  declining,  due  to  maintenance  shutdowns  and  local  security  policies
(Davids et al., 2019; Fekete et al., 2015). Additionally, existing stations are unevenly distributed,
concentrated primarily in large rivers and developed regions (Krabbenhoft et al., 2022). In contrast,
sparsely populated or underdeveloped regions such as the Tibetan Plateau and Africa lack in-situ
gauging  stations  (Liu,  2023;  Tarpanelli  et  al.,  2023).  Small  streams  and  their  headwaters,
accounting for more than 70% of the total length of river networks (Amatulli et al., 2022), are also
often left unmonitored. Consequently, relying solely on in-situ measurements is insufficient for
capturing global river dynamics and understanding comprehensive hydrological processes.

Satellite remote sensing has emerged as a critical complement to in-situ observations (Fang
et  al.,  2025b;  Jaramillo  et  al.,  2024).  Optical  sensors  enable  the  retrieval  of  water  extent  by
applying water masks to imagery (X. Yang et al., 2020). However, optical sensors are susceptible
to cloud interference and exhibit reduced accuracy during nighttime conditions (Nanesso, 2024).
Spaceborne radar altimeters, when combined with algorithms such as the 50% Threshold and Ice-
1  Combined  (TIC)  algorithm  (Huang  et  al.,  2018a)  and  the  Improved  Multiple  Subwaveform
Analysis (IMSA) algorithm (Fang et al., 2025a), provide reliable water level measurements over
complex  riverine  environments.  Radar  altimeters  are  unaffected  by  cloud  cover,  but  they  only
provide  observations  near  satellite  tracks  with  limited  spatial  coverage  (Sui  et  al.,  2017).  The
Surface Water and Ocean Topography (SWOT) mission launched in December 2022 represents a
transformative breakthrough in hydrological monitoring using satellite altimetry (Fu et al., 2024).
SWOT can simultaneously measure water surface elevation (WSE), water surface slope (WSS),
and water extent, with the reported capability to monitor rivers wider than 100 m and lakes larger
than 250 × 250 m2 worldwide. Importantly, it achieves wide-swath observations of up to 120 km
with a 20 km nadir gap, while traditional altimeters such as Sentinel-3 can only provide discrete
measurements for nadir points (Archer et al., 2025; Shu et al., 2020). By providing comprehensive
observations  over  ungauged  basins,  SWOT  creates  unprecedented  opportunities  for  estimating
river discharge and advancing our understanding of global river dynamics (Getirana et al., 2024;
Huang et al., 2020).

Table 1 presents key studies on discharge estimation using remote sensing over the last two
decades.  Among  these  approaches,  Brakenridge  et  al.  (2007)  employed  radiance  ratios  of  the
surrounding terrestrial area to the water surface as the proxy of discharge estimation. The proxy
method requires in-situ data for calibration and primarily focuses on water extent while neglecting
key  hydrological  variables  such  as  water  level,  thus  lacking  physical  mechanism  foundation.
Several  studies  have  adopted  Rating  Curves  (RC)  to  establish  relationships  between  river
discharge and water level or river width. This approach faces the same limitations that require in-
situ constraints, and model uncertainty increases significantly when estimating discharge beyond
the calibrated reaches (Le Coz et al., 2014). Masafu et al. (2023) applied the Large Scale Particle
Image  Velocimetry  (LSPIV)  algorithm  to  extract  surface  velocity  from  5  Hz  high-frequency
optical images. The velocity-based method requires high-frequency images, making it unsuitable
for SWOT with a 21-day revisit period. Additionally, this method requires high-resolution digital
elevation models (DEMs) to provide cross-sectional data, which typically lack accuracy, thereby
limiting its large-scale applicability. These approaches are limited in their capacity for large-scale
discharge estimation, owing to their dependence on in-situ constraints or high-frequency remote
sensing images.

manuscript submitted to Water Resources Research

118

Table 1. Summary of relevant studies estimating river discharge using remote sensing
Variables
used

In-situ
constraint

Sensor type

Study

Details

Brakenridge
et al. (2007)

Radiometer

C/M

Yes

Tarpanelli et
al. (2015)

Radiometer &
altimeter

C/M, H

Yes

Pavelsky
(2014)

Optical

Zakharova et
al. (2019)

Optical &
altimeter

W

H

Yes

Yes

Huang et al.
(2018b)

Optical &
altimeter

H, W

Yes

Masafu et al.
(2023)

Durand et al.
(2014)

Gleason et al.
(2014)

Optical

V, A

No

Optical

H, S, W

No

Optical

W

No

Andreadis et
al. (2025)

Wide-swath
altimeter

H, S, W

No

Xu et al.
(2026)

Optical &
wide-swath
altimeter

H, W

No

This study

Wide-swath
altimeter

H, S, W

No

Developed discharge prediction models
based on radiance ratios, establishing
polynomial functional relationships
between discharge and radiometric ratios.

Estimated river velocity based on C/M
ratios and calculated discharge using an
entropy method that couples water level
and velocity. DEM was utilized to
determine cross-sectional area.

Estimated discharge using width-based
RC.

Enhanced H retrieval quality by applying
Landsat 8-based water masks, and applied
RC for discharge estimation.

The coupling equation incorporating both
H and W provided superior discharge
estimates compared to RC methods
utilizing single variables.

Applied the LSPIV algorithm to extract
river velocity from 5 Hz high-frequency
imagery, with DEM for cross-sectional
area measurement.

Employed DEM-assisted measurements
for H and S. Proposed the MetroMan
algorithm and demonstrated its feasibility
through SWOT mission simulations.

Applied AMHG to retrieve discharge
based on river morphology and channel
width.

Validated the SoS v1 product, reporting a
median Spearman correlation of 0.73 with
a median NSE below -0.5 across 65
reaches.

Developed the SWAP algorithm,
achieving positive KGE and NSE values
for 66.4% and 46.0% of the 557 stations,
respectively.

Enhance SWOT observations, and
achieved a median NSE value of 0.30 and
median KGE value of 0.42 across 391
stations

119
120

Note. Among the variables useed: C/M represents the radiance ratio of the surrounding terrestrial area to the
water surface; H denotes water surface elevation;  S refers to water surface slope;  W indicates river width; A

manuscript submitted to Water Resources Research

121
122
123

124
125
126
127
128
129
130
131
132
133
134
135
136
137
138
139

140
141
142
143
144
145
146
147
148
149
150
151
152

represents cross-sectional area; and V denotes surface velocity. Abbreviations: DEM, Digital Elevation Model;
RC,  rating  curves;  LSPIV,  Large  Scale  Particle  Image  Velocimetry;  AMHG,  at-many-stations  hydraulic
geometry; SWAP, SWOT and a-priori information.

Durand et al. (2014) developed the gauge-independent MetroMan algorithm specifically
for SWOT discharge estimation. Gleason et al. (2014) proposed the At-Many-stations Hydraulic
Geometry  (AMHG)  approach,  incorporating  river  morphology  for  discharge  estimation.
Hagemann et al. (2017) subsequently proposed a Bayesian formulation of streamflow uncertainty
by  integrating  the  Manning  equation  with  the  AMHG  framework,  establishing  the  Bayesian
AMHG-Manning  (BAM)  algorithm.  Furthermore,  the  Modified  Optimized  Manning  Method
Algorithm  (MOMMA)  was  introduced  as  an  updated  version  of  the  Mean  Flow  and
Geomorphology (MFG) algorithm (Bonnema et al., 2016). Beyond these approaches, three data
assimilation  algorithms,  i.e.,  SIC  4D-variational  (SIC4DVar)  algorithm  (Oubanas  et  al.,  2018),
Hierarchical Variational Discharge Inference (HiVDI) algorithm (Larnier et al., 2020), and SWOT
Assimilated Discharge (SAD) algorithm (Andreadis et al., 2020), leverage discrepancies between
modeled  and  remotely  sensed  variables  to  constrain  flow  law  parameters  (FLPs),  thereby
circumventing  the  need  for  in-situ  constraints.  However,  most  gauge-independent  discharge
estimates suffer from substantial magnitude bias, as reflected by negative median and mean NSE
values (Andreadis et al., 2025; Xu et al., 2026), attributable in part to the direct use of hydraulic
observations from the SWOT River Product without additional refinement.

This  study  uses  SWOT  observations  to  construct  an  ungauged  discharge  estimation
framework that encompasses three key steps: (1) selecting continuous river reaches, (2) assembling
high-quality SWOT observations into time-space arrays, and (3) applying the modified MetroMan
algorithm for discharge estimation. MetroMan was selected as the benchmark algorithm owing to
its  strong  ability  to  capture  discharge  dynamics  during  initial  validation  (see Section  4.1).  The
framework developed in this study is validated across 391 river reaches, achieving a median NSE
of 0.30 and a median KGE of 0.42. Further comparisons demonstrate that width refinement is the
primary  driver  of  performance  improvement,  while  the  modification  to  MetroMan  enhances
algorithmic  robustness.  Tributary  inflow  and  downstream  hydraulic  control  are  identified  as
contributors to performance degradation even under refined-width conditions. By incorporating
data from  conventional  altimeters such  as Sentinel-3, this framework  can  reconstruct  historical
discharge  to  provide  extended  study  periods,  supporting  long-term  hydrological  analysis  and
climate change impact assessment.

153

2 Study Area and Data

154

155
156
157
158
159
160
161
162
163
164

2.1 Study Area

This study adopts a near-globe scope, with reach selection driven by the availability of in-
situ discharge records from two primary datasets: the United States Geological Survey (USGS)
and  Global  Runoff  Data  Centre  (GRDC).  The  study  encompasses  river  reaches  across  four
continents:  North  America,  Europe,  Africa,  and  Oceania.  The  absence  of  Asian  reaches  is
attributed to the lack of available in-situ records during the SWOT observation period at the time
of  this  analysis.  South  American  reaches  were  excluded  due  to  the  insufficient  number  of
qualifying  gauging  stations.  Following  these  continental  constraints,  391  river  reaches  were
selected for validation and further analysis (Figure 1). All selected reaches are located away from
reservoirs or dams, free of tributary confluences within the reach boundaries, and situated within
1 km of an in-situ gauging station. The selected reaches span major river systems across the study

manuscript submitted to Water Resources Research

165
166
167
168
169
170

continents, including the Mississippi River in North America, the Rhine River in Europe, the Niger
River  in  Africa,  and  the  Murray  River  in  Oceania.  These  reaches  encompass  multiple  climate
types, with prior river widths ranging from 42 to 1741 m and prior discharge values spanning from
1 to 22,793 m3/s. This selection covers the full spectrum from small streams to large rivers, thereby
providing  diverse  and  representative  testing  scenarios  for  validating  SWOT-based  discharge
estimation.

171

172
173
174
175
176

177

178
179
180

Figure 1. Geographic distribution of 391 selected river reaches. Regional panels show zoomed-in views for four
continents with selected reaches. Circle sizes represent prior river widths, and colors indicate prior discharge
values. Gray lines show rivers from the SWORD network. The violin plot illustrates the distribution of prior
river widths and discharge values for the selected reaches, demonstrating good representativeness of the study
reaches.

2.2 Data

Our study used five categories of data: (1) river databases, (2) SWOT products, (3) prior
discharge database, (4) in-situ measurements,  and  (5)  Sentinel-3  altimetry.  River  datasets were
employed for reach selection, while SWOT products and prior discharge database were used to

manuscript submitted to Water Resources Research

181
182

183
184
185
186
187
188
189
190

191
192
193
194
195
196
197
198
199
200
201
202
203
204
205
206

207
208
209
210
211
212

213
214
215
216
217
218

219
220
221
222

estimate discharge. In-situ discharge measurements provided validation for discharge estimates,
and Sentinel-3 altimetry enabled historical discharge reconstruction.

The  SWOT  River  Database  (SWORD)  represents  a  global  river  database  specifically
designed  for  the  SWOT  mission  (Altenau  et  al.,  2021).  It  establishes  a  unified  topological
framework for global rivers exceeding 30 m in width, dividing them into nodes with an average
spacing of 200 m or reaches with an average length of 10 km. SWOT observations are initially
sampled as pixel clouds, which are then aggregated to nodes or reaches according to the SWORD
structure. HydroRIVERS (Lehner & Grill, 2013) provides more detailed river network delineation
compared  to  the  SWORD  dataset,  but  with  coarser  reach  boundaries.  We  used  its  discharge
estimates to analyze the impact of tributary inflow (see Section 5.1).

SWOT  transitioned  to  its  science  orbit  on  July  21,  2023,  beginning  global  wide-swath
observations with a 21-day repeat cycle. Our study period spans from November 2023, to March
2025, covering 16 months during the science phase. The SWOT Level 2 River Single-Pass Vector
Data Product (SWOT, 2024a) provides measurements of WSE, WSS, and width at node and reach
scales, with width measurements being particularly noisy (see Section 3.2). We selected reach-
scale data to smooth noise present at the node scale. The SWOT Level 2 Water Mask Raster Image
Data Product (SWOT, 2024b) provides water attributes including WSE and water extent at both
100 m and 250 m resolutions. We used the water extent measurements from the 100 m resolution
product to optimize river widths. The SWOT Sword of Science (SoS) River Discharge Products
(SWOT Discharge  Algorithm Working  Group,  2023) offer  time series  of reach-level  discharge
estimates  from  six  algorithms  based  on  the  SWOT  River  Product.  Text  S2  in  Supporting
Information presents the validation results for the SoS Version 3 product. This version exhibits
several limitations: HiVDI estimates are absent and SAD estimates are available for only a limited
number of reaches. We selected the optimal algorithm based on the SoS Version 1 product as the
benchmark for our discharge estimation framework instead, given that our primary use of the SoS
product is to evaluate the relative performance of different algorithms (see Section 4.1).

Lin  et  al.  (2019)  developed  the  Global  Reach-Level  A  Priori  Discharge  Estimates  for
SWOT (GRADES) database, providing daily discharge estimates for river reaches worldwide. Y.
Yang  et  al.  (2025)  subsequently  enhanced  the  GRADES  database  using  a  machine  learning
algorithm, producing an updated version designated as GRADES-hydroDL. The mean discharge
from the GRADES-hydroDL database averaged over the 2023–2024 period was used as the prior
discharge input to our ungauged discharge estimation framework.

USGS (https://waterdata.usgs.gov) and GRDC (https://grdc.bafg.de) collectively maintain
11,792 discharge stations with latest records extending to 2024 or beyond, from which daily mean
discharge records were used to evaluate the performance of our ungauged discharge estimation
framework (see Section 4.1). USGS additionally maintains 3,687 stage gauges across the United
States, against which daily mean water levels were used to assess the accuracy of our preprocessed
WSE (see Text S1 in Supporting Information).

We  obtained  Sentinel-3  altimetry  data  from  the  Copernicus  Data  Space  Ecosystem
(https://dataspace.copernicus.eu/explore-data). The Level-2 Non-Time Critical (NTC) Hydrology
Thematic  products  were  used  for  water  level  retrieval  using  the  IMSA  algorithm  to  enable
historical discharge reconstruction (see Section 4.3).

manuscript submitted to Water Resources Research

223

3 Methodology

224

225
226
227

228
229
230
231

232
233
234
235
236
237

238
239
240
241
242
243

244
245
246

3.1 Ungauged Discharge Estimation Framework

We  develop  a  comprehensive  discharge  estimation  framework  based  on  SWOT
observations,  specifically  designed  for  ungauged  river  systems,  as  illustrated  in  Figure  2.  The
framework comprises three main components:

(1)  Selecting  continuous  river  reaches  within  the  river  network.  A  minimum  of  three
reaches  without  intervening  dams  or  tributaries  is  required  to  effectively  establish  mass
conservation between upstream and downstream reaches, a requirement readily met by SWOT’s
100-km wide swath observations.

(2) Assembling high-quality observation time-space arrays. To ensure reliable inputs, all
SWOT  observations  undergo  dedicated  quality-improvement  procedures.  WSEs  and  WSSs
obtained  from  the  SWOT  River  Product  are  preprocessed  based  on  upstream-downstream
observation  consistency  (Section  3.2).  Water  extents  from  the  SWOT  Raster  Product  are  then
confined to the river channel and river widths are automatically extracted from the optimal reach
segment to further enhance data quality (Section 3.3).

(3) Applying a modified MetroMan algorithm to estimate river discharge. Prior FLPs are
initially  determined  using  the  prior  discharge  from  GRADES-hydroDL  database.  Mass
conservation  constraints  between  upstream  and  downstream  reaches  are  embedded  in  the
likelihood  function  as  part  of  the  optimization  objective.  Posterior  FLPs  are  inferred  through
Markov Chain Monte Carlo (MCMC) sampling and the peak of the smoothed posterior distribution
is used to estimate discharge.

The most distinctive aspect of our framework lies in its complete independence from in-
situ gauge measurements, relying exclusively on refined satellite observations for accurate river
discharge estimation. Each component is detailed below.

manuscript submitted to Water Resources Research

247

248
249
250
251

252

253
254

Figure 2. Ungauged discharge estimation framework. The framework is structured into three core components:
(1)  river  reach  selection  with  minimum  three  continuous  reaches,  (2)  high-quality  observation  matrix
construction from SWOT River and Raster Products, and (3) discharge estimation using modified MetroMan
algorithm with MCMC sampling.

3.2 WSE and WSS Preprocessing

The SWOT River Product provides observations of WSE and WSS for river reaches, but
contains numerous outliers. While the product includes quality flags, the flags tend to be overly

manuscript submitted to Water Resources Research

255
256
257
258
259

260
261
262
263
264
265
266
267
268
269
270
271
272
273
274
275
276

277
278
279
280
281
282
283
284
285
286

conservative with high water levels (Andreadis et al., 2025). Additionally, it is difficult to establish
appropriate thresholds for outlier detection when working with individual reaches, as this approach
struggles to simultaneously remove anomalous values and preserve normally elevated water levels.
Since SWOT provides synchronized observations across continuous river reaches, we can leverage
hydrological behavior consistency among neighboring reaches to identify outliers.

For WSEs, we developed a systematic approach based on reach consistency, comprising
three main components: (1) quantile-based identification, (2) suspected outlier detection, and (3)
reach consistency assessment. Initially, we defined the water level fluctuation as the difference
between  the  90th  and  10th  percentiles  of  reach  WSEs.  Observations  more  than  1.8  times  this
fluctuation  above  or  more  than  one  fluctuation  below  the  median  were  removed  as  outliers.
Additionally, observations were excluded if the “reach_q” flag indicated bad, if the dark water
fraction  exceeded  0.3,  or  during  periods  of  river  ice  cover  (Cerbelaud  et  al.,  2026).  For  the
remaining WSEs,  observations  that  exhibit differences  exceeding  half  of  the fluctuation  within
adjacent time periods were flagged as suspected outliers. At this stage, we examined WSE changes
in neighboring reaches by calculating their differences from the 22-day median. If the suspected
WSE change was more than twice as large as that of neighboring reaches, it was classified as an
outlier and removed; otherwise, it was considered a normal hydrological response and retained.
Using  this  method,  the  median  RMSE  for  WSEs  decreased  from  1.65  m  to  0.74  m,  with
approximately  25%  of  observations  removed,  effectively  balancing  observation  quality  and
quantity  (Figure  S1  in  Supporting  Information).  In  contrast  to  overly  strict  quality  flag-based
methods that typically remove 90% of observations (Andreadis et al., 2025), our approach provides
substantially more observations.

We  applied  a  similar  methodology  for  WSS  outlier  treatment,  though  with  some
adjustments tailored to the characteristics of WSS. WSSs above 10 times or below 0.1 times the
median were classified as outliers, while those above 3 times or below 1/3 of the median were
flagged as suspected outliers. During reach consistency assessment, we examined WSS changes
in neighboring reaches by  calculating  their  ratios to the 45-day  median.  For anomalous  slopes,
linear interpolation in the temporal dimension was applied for correction rather than removal, as
WSSs typically exhibit smaller temporal variations than WSEs across our study reaches (Leon et
al.,  2006).  The  preprocessing  results  for  four  example  reaches  demonstrate  successful
identification and treatment of anomalous water levels and slopes, achieving improved consistency
(Figure 3).

manuscript submitted to Water Resources Research

287

288
289
290

291

292
293
294
295
296
297
298
299
300
301
302
303
304

305
306
307
308
309
310
311
312

Figure 3. Preprocessed WSE and WSS for four continuous reaches. Yellow and blue lines represent WSS and
WSE  measurements,  respectively,  and  disconnected  crosses  mark  anomalous  WSE  and  WSS  observations
identified during preprocessing.

3.3 River Width Refinement

The  SWOT  River  Product  uses  a  threshold-based  pixel  classification  approach,  with
thresholds  largely  derived  from  prior  datasets  such  as  SWORD  (JPL,  2023).  The  river  width
measurements provided by this product (hereafter referred to as original widths) are highly noisy
across  most  river  reaches  due  to  the  simplicity  of  this  processing,  manifesting  as  abrupt
fluctuations of over 100 m within intervals as short as three days (e.g., Figure S2 in Supporting
Information). This issue is mainly attributable to two factors: (1) When SWOT observes rivers at
cross-track distances that are either too close to the nadir (e.g., within 10 km) or too far from it
(e.g., beyond 60 km), the measurement accuracy degrades, resulting in increased uncertainty in
the retrieved water  extent  (Biancamaria  et  al.,  2016;  Durand  et  al.,  2020);  (2) Water  pixels are
erroneously classified as river channel area for reaches intersecting with small lakes absent from
the  Prior  Lake  Dataset  (PLD)  or  adjacent  to  riverine  wet  fields,  as  neither  connectivity-based
filtering  nor  thresholding  can  effectively  remove  their  contribution,  resulting  in  width
measurements substantially exceeding prior widths.

An automated procedure was developed for river width extraction using the SWOT Raster
Product (Figure 4), comprising three sequential components: (1) main-channel mask delineation,
(2) optimal sub-reach selection, and (3) width time series derivation. In the first step, pixels with
water fraction below 0.1 and those located outside the 10–60 km range  from the satellite nadir
track were removed, as observations at extreme nadir distances contain more noise and data gaps
(Fjortoft et al., 2014). A buffer zone of twice the prior river width and connectivity analysis were
then  applied  to  exclude water pixels  disconnected  from  the  main  channel,  retaining  only  those
within  the buffer  zone  that  maintain  continuous  connection  to  the  river  centerline.  Pixels  were

manuscript submitted to Water Resources Research

313
314
315
316
317

318
319
320
321
322
323
324
325
326

327
328
329
330
331
332
333

subsequently  classified  as  connected  lakes  or  adjacent  wet  field  if  any  non-water  pixel  existed
along the shortest path to the river centerline, and were removed accordingly. A skeletonization
algorithm (Zhang & Suen, 1984) was then applied, with each pixel assigned to its nearest skeleton
element, to eliminate residual pixels that do not belong to the main channel following lake filtering,
yielding a refined main-channel mask.

In the second step, a 3-km optimal sub-reach was selected within each reach, as a reach
may not be fully observed by all SWOT passes and certain portions may present complex riverine
environments  unfavorable  for  width  extraction.  Three  metrics  were  used  to  quantify  sub-reach
suitability: (1) the sinuosity of the SWORD river centerline, (2) the relative standard deviation of
the water area time series, and (3) the correlation coefficient of mean water area across different
SWOT  passes.  The  optimal  sub-reach,  selected  based  on  a  combination  of  these  three  metrics
(details in Figure 4), prioritizes segments with lower sinuosity, lower inter-pass variability, and
fewer  anomalous  observations.  In  the  final  step,  the  water  area  of  each  raster  observation  was
divided by the sub-reach length (i.e., 3 km) to derive the refined river width time series.

This automated procedure eliminates anomalous high values in river width measurements
and substantially mitigates unreasonable width fluctuations, resulting in smoother width variations
(Figure  S2  in  Supporting  Information).  These  example  reaches  exhibit  a  significantly  greater
number  of  anomalous  width  measurements  compared  to  the  water  level  preprocessing,  which
confirms that width observations from the SWOT River Product are highly noisy. As discharge
estimates are highly sensitive to width measurements (see Section 4.1), width refinement plays a
critical role within our framework.

manuscript submitted to Water Resources Research

334

335
336
337
338
339

340

341
342
343

Figure 4. Flowchart of the refined width extraction procedure. First, an accurate river channel mask is derived
through  four  processing  steps:  buffer  filtering,  connectivity  filtering,  lake  filtering,  and  skeleton  pruning.
Subsequently,  a  representative  sub-reach  is  determined  based  on  a  combination  of  sinuosity,  correlation
coefficient, and relative standard deviation. Finally, the width time series is calculated from the raster ensemble
covering the sub-reach.

3.4 Modified MetroMan Algorithm

The MetroMan algorithm is grounded in MCMC and Bayesian inference principles. River
channels that can be assessed by remote sensing are typically characterized by gentle slopes with
Froude values below 0.3, allowing the energy slope to be approximated as the water surface slope

manuscript submitted to Water Resources Research

that SWOT can observe (Frasson et al., 2021). Under these conditions, river discharge estimation
relies on the modified Manning equation as its foundation:

𝑄(𝑟, 𝑡) =

1
𝑛(𝑟, 𝑡)

[𝐴(cid:2868)(𝑟) + 𝛿𝐴(𝑟, 𝑡)]

(cid:2873)
(cid:2871)𝑊(𝑟, 𝑡)(cid:2879)

(cid:2870)
(cid:2871)𝑆(𝑟, 𝑡)

(cid:2869)
(cid:2870)

(1)

where key FLPs such as the reach-averaged roughness coefficient n(r, t) and initial cross-sectional
area A0(r) require calibration, while variables including cross-sectional area change δA(r, t), river
width  W(r,  t),  and  slope  S(r,  t)  can  be  directly  obtained  from  SWOT  observations.  Our  study
reaches  were  selected  to  exclude  internal  occurrences  of  reservoirs,  dams,  and  major  tributary
confluences,  thereby  minimizing  the  interference of  backwater  effects  on  discharge  estimation.
The core novelty of the MetroMan algorithm lies in introducing mass conservation relationships
between upstream and downstream reaches to constrain FLPs, rather than calibrating against in-
situ or modeled discharge data:

(cid:2986)(cid:3018)

(cid:2986)(cid:3002)

(𝑟, 𝑡) +

𝛩(𝑟, 𝑡) =

(2)
where x denotes the along-channel distance from the start point of selected continuous reaches; A
represents the total  cross-sectional area  (A0+δA);  Θ represents the mass residual,  which  ideally
equals zero.  In our study, we neglect  the lateral inflow term  q(r, t)  in  the equation, effectively
setting it to zero. Θ characterizes mass conservation between river reaches and can be incorporated
into the likelihood function for the MCMC process.

(𝑟, 𝑡) − 𝑞(𝑟, 𝑡)

(cid:2986)(cid:3051)

(cid:2986)(cid:3047)

We implemented two primary refinements to the MetroMan algorithm: (1) replacing the
log-normal prior distribution for A0 with a truncated normal distribution, and (2) selecting posterior
A0 based on the peak of the smoothed MCMC sampling distribution rather than the mean. While
the log-normal distribution naturally constrains the sampling range to positive values, A0 selection
during  calibration  must  ensure  that  (A0+δA)  remains  positive  throughout  computation,
necessitating truncation even for log-normal distributions. Additionally, log-normal distributions
exhibit extended right-tail behavior, leaving the upper bound of A0 unconstrained during MCMC
sampling. By adopting a truncated normal distribution where values below zero and above twice
the prior A0 are excluded (see Figure 2), the upper bound of A0 becomes constrained, preventing
unlimited increases during the sampling process.

In addition, the original MetroMan algorithm selects the mean as the posterior A0, but the
mean value is highly susceptible to the predefined upper and lower bounds. While theoretically
the mean reflects the expected value of A0, we seek parameters that best satisfy mass conservation
relationships, with the peak value being most representative of this optimal condition. Therefore,
following  maximum  likelihood  estimation  principles,  we  employ  the  peak  of  the  smoothed
posterior  distribution  to  obtain  the  "most  probable"  A0.  Considering  that  MCMC  posterior
distributions  contain  noise,  we  utilize  kernel  density  estimation  (KDE)  to  obtain  a  smoothed
distribution. A bisection method is employed to determine the minimum bandwidth parameter that
ensures the smoothed distribution exhibits a single peak, thereby preventing both overfitting and
underfitting.

3.5 Evaluation Metrics

WSEs and discharge estimates for each reach were validated against the nearest available
in-situ  measurements,  with  validation  metrics  detailed  in  Table  2.  The  accuracy  of  WSE

344
345

346

347
348
349
350
351
352
353
354

355

356
357
358
359
360

361
362
363
364
365
366
367
368
369
370

371
372
373
374
375
376
377
378
379
380

381

382
383

manuscript submitted to Water Resources Research

384
385
386
387
388
389
390
391

392
393
394
395
396
397
398

observations  was  evaluated  using  the  root  mean  square  error  (RMSE).  For  discharge  estimates
from  the  SoS  product  (based  on  six  algorithms)  and  our  discharge  estimation  framework,  the
Pearson  correlation  coefficient  (CC),  normalized  root  mean  square  error  (NRMSE),  the  Nash–
Sutcliffe efficiency (NSE) and the Kling–Gupta Efficiency (KGE) were considered to provide a
more comprehensive evaluation. Among the four metrics, NSE and KGE are treated as the primary
indicators  of  estimation  performance,  as  each  capture  both  the  dynamic  behavior  and  the
magnitude of discharge, whereas CC reflects only temporal consistency and NRMSE penalizes
magnitude errors primarily.

Beyond these metric-level distinctions, a further consideration motivates the prioritization
of  NSE  specifically.  Because  WSE  and  discharge  are  physically  coupled,  discharge  estimates
incorporating  WSE  observations  tend  to  exhibit  strong  dynamic  agreement  with  in-situ
measurements. Accurate magnitude estimation, by contrast, depends critically on well-calibrated
hydraulic  parameters  and  is  therefore  the  more  demanding  and  informative  dimension  of
performance.  Within  this  context,  NSE  is  adopted  as  the  principal  benchmark,  given  that  it  is
inherently more sensitive to systematic magnitude errors than KGE.

399

Table 2. Evaluation metrics used in our study

Evaluation
indicator

Short
name

Formula

Ideal
value

Purpose

Root mean
square error

RMSE

𝑅𝑀𝑆𝐸 = (cid:3497)

1
𝑛

(cid:3041)
(cid:3533)(cid:3435)𝑊𝑆𝐸(cid:3034)(cid:3028)(cid:3048),(cid:3036) − 𝑊𝑆𝐸(cid:3046)(cid:3028)(cid:3047),(cid:3036)(cid:3439)
(cid:3036)(cid:2880)(cid:2869)

(cid:2870)

Pearson
correlation
coefficient

Normalized
root mean
square error

Nash–Sutcliffe
efficiency

Kling–Gupta
Efficiency

CC

𝐶𝐶(𝑥, 𝑦) =

∑ (𝑥(cid:3036) − 𝑥)

(cid:3041)
(cid:3036)(cid:2880)(cid:2869)
(cid:3493)∑ (𝑥(cid:3036) − 𝑥)(cid:2870)

(cid:3041)
(cid:3036)(cid:2880)(cid:2869)

(𝑦(cid:3036) − 𝑦)
(cid:3041)
(cid:3493)∑ (𝑦(cid:3036) − 𝑦)(cid:2870)
(cid:3036)(cid:2880)(cid:2869)

NRMSE

𝑁𝑅𝑀𝑆𝐸 =

(cid:3041)
(cid:3036)(cid:2880)(cid:2869)

∑ (cid:3435)𝑄(cid:3032)(cid:3046)(cid:3047),(cid:3036) − 𝑄(cid:3034)(cid:3028)(cid:3048),(cid:3036)(cid:3439)

(cid:3495)1
𝑛
𝑄(cid:3034)(cid:3028)(cid:3048),(cid:3040)(cid:3028)(cid:3051) − 𝑄(cid:3034)(cid:3028)(cid:3048),(cid:3040)(cid:3036)(cid:3041)

(cid:2870)

NSE

𝑁𝑆𝐸 = 1 −

(cid:2870)

(cid:3041)
(cid:3036)(cid:2880)(cid:2869)

∑ (cid:3435)𝑄(cid:3034)(cid:3028)(cid:3048),(cid:3036) − 𝑄(cid:3032)(cid:3046)(cid:3047),(cid:3036)(cid:3439)
(cid:2870)
∑ (cid:3435)𝑄(cid:3034)(cid:3028)(cid:3048),(cid:3036) − 𝑄(cid:3034)(cid:3028)(cid:3048)(cid:3439)

(cid:3041)
(cid:3036)(cid:2880)(cid:2869)

KGE

𝐾𝐺𝐸 = 1 − (cid:3493)(𝐶𝐶 − 1)(cid:2870) + (𝛼 − 1)(cid:2870) + (𝛽 − 1)(cid:2870)

0

1

0

1

1

WSE
validation

Discharge
validation and
width-WSE
variation
consistency

Discharge
validation

Discharge
validation

Discharge
validation

400
401
402
403
404
405
406

Note. n represents the number of measurements; WSEgau,i and WSEsat,i represent the in-situ and SWOT-derived
WSE at time step i, respectively; Qgau,i and Qest,i represent the in-situ and estimated discharge at time step i, with
overlines denoting mean values; Qgau,max and Qgau,min denote the maximum and minimum gauge discharge for
each river reach; α denotes the ratio of mean estimated discharge to mean in-situ discharge; β denotes the ratio
of the standard deviation of estimated discharge to that of in-situ discharge; x and y denote paired variables in
the CC metric: for discharge validation, they represent in-situ and estimated discharge, respectively, whereas for
width-WSE variation consistency, they represent river width and WSE, respectively.

manuscript submitted to Water Resources Research

407

4 Results

408

409
410
411
412
413
414
415
416
417
418
419
420
421
422

423
424
425
426
427
428
429
430
431
432
433
434
435
436
437
438
439
440

4.1 Discharge Estimation Performance

The SoS product provides discharge estimates using six algorithms: HiVDI, MetroMan,
MOMMA,  geoBAM,  SAD,  and  SIC4DVar.  For  each  algorithm,  validation  was  conducted  at
reaches  with  at  least  five  valid  discharge  estimates,  corresponding  to  60–681  USGS  gauging
stations depending on the algorithm. The six algorithms yielded median KGE values of -0.16, 0.23,
-0.38, -0.27, -1.61, and 0.22; median CC values of 0.40, 0.77, -0.04, 0.27, 0.44, and 0.83; median
NSE values of -0.58, -1.47, -1.38, -1.21, -15.60, and -0.12; and median NRMSE values of 37%,
53%,  51%,  49%,  128%,  and  33%  for  the  respective  algorithms  (Figure  5).  Among  these
algorithms, MetroMan demonstrated a strong ability to capture discharge dynamics, achieving the
highest KGE along with the second highest CC value. However, MetroMan showed comparatively
weaker performance than SIC4DVar in magnitude estimation. The underperformance is largely
attributable to the absence of Saint-Venant equation constraints in FLP calibration (Durand et al.,
2023), making it more sensitive to observation quality compared to SIC4DVar. Our framework
alleviates  this  limitation  by  providing  refined  observations,  which  also  serves  as  an  indirect
assessment of observation quality.

Moreover, MetroMan requires synchronous observations across continuous river reaches,
which  aligns  closely  with  SWOT’s  inherent  observational  capabilities,  suggesting  a  strong
methodological  complementarity  between  the  two.  In  contrast,  SIC4DVar  involves  a  larger
number  of  free  parameters  in  its  FLP,  necessitating  longer  reaches  and  more  extensive
observations for calibration, which imposes greater constraints on reach selection (Oubanas et al.,
2018). These are the main reasons why we selected MetroMan as the benchmark algorithm in our
framework. However, in the SoS product, MetroMan-based discharge estimates are available for
only  60  river  reaches  with  at  least  five  valid  estimates,  representing  less  than  6%  of  the  total
gauging  stations  (Figure  S3  in  Supporting  Information).  In  addition,  the  average  temporal
resolution of these estimates is 27 days, which exceeds the 21-day repeat cycle of SWOT. Given
that SWOT can observe the same reach from multiple tracks, this implies that a large portion of
available  observations  is  left  unused.  The  sparse  spatiotemporal  coverage  indicates  that  the
existing  discharge  estimation  system  removes  excessive  observations  and  requires  further
refinement. Furthermore, the median NRMSE values of all six algorithms exceed 30%, and the
median NSE values are consistently negative, with less than 45% of the gauging stations exhibiting
positive  values  even  under  the  framework  of  MetroMan  and  SIC4Var.  This  indicates  that
parameter calibration in the official products is inadequate, highlighting the necessity of substantial
refinements.

manuscript submitted to Water Resources Research

441

442
443
444
445
446
447

448
449
450
451
452
453
454
455

Figure 5. Validation performance of six algorithms across the United States. (a) Boxplots of KGE and CC, with
KGE shown on the left y-axis with a logarithmic scale and CC on the right y-axis. (b) Boxplots of NSE and
NRMSE, with NSE shown on the left y-axis with a logarithmic scale and NRMSE on the right y-axis with a
square-root scale. The box plots represent the median, 25th, and 75th percentiles, with whiskers extending to 1.5
times the interquartile range. MetroMan exhibits the highest median KGE along with the second highest CC
value, which justifies its selection for our ungauged discharge estimation framework.

Using  our  discharge  estimation  framework,  all  391  selected  reaches  achieved  a  median
KGE  of  0.42,  CC  of  0.94,  NSE  of  0.30,  and  NRMSE  of  20%,  outperforming  all  SoS-derived
discharge estimates, all of which yielded negative median NSE values. Notably, the median NSE
improved by 1.77 relative to the SoS-derived MetroMan results, demonstrating substantially more
accurate magnitude estimation enabled by the refined observations provided by our framework. In
total, 61% and 75% of reaches achieved positive NSE and KGE values, respectively, representing
competitive performance among remote sensing discharge estimation approaches without in-situ
constraints.

manuscript submitted to Water Resources Research

456
457
458
459
460
461
462
463
464
465
466

467

468
469
470
471
472
473
474
475
476

477
478
479
480
481
482
483
484

Among the 251 study reaches in the United States, 18 reaches had sufficient SoS-derived
MetroMan estimates, with median NSE and KGE values of -0.44 and 0.28, respectively; and 179
reaches had sufficient SoS-derived SIC4DVar estimates, with median NSE and KGE values of -
0.05 and 0.30, respectively. Both sets of estimates consistently yielded lower performance metrics
compared to our framework. The NSE distributions across all selected reaches are shown in Figure
S4 in Supporting Information, where clusters of negative NSE values are observed near the mouths
of the Columbia, Yukon, and Murray rivers, likely attributable to backwater effects induced by
tidal forcing (to be further discussed in Section 5.1). On average, each reach contained more than
27 discharge estimates, equivalent to one every 18 days. This demonstrates that our framework
effectively balances the quantity and quality of observations through sophisticated preprocessing
strategies.

4.2 Width Refinement Effect

We defined four scenarios to quantify the respective contributions of width refinement and
MetroMan algorithm modification to discharge estimation performance: (1) original MetroMan
(i.e.,  using  the  mean  of  the  MCMC  posterior  distribution)  with  original  widths,  (2)  modified
MetroMan  (i.e.,  using  the  peak  of  the  MCMC  posterior  distribution)  with  original  widths,  (3)
original  MetroMan  with  refined  widths,  and  (4)  modified  MetroMan  with  refined  widths.  The
corresponding median NSE values were -0.13 and -0.07 for the original-width scenarios, and 0.29
and 0.30 for the refined-width scenarios; the respective median KGE values were 0.11, 0.19, 0.44,
and 0.42; the respective median CC values were  0.89,  0.89, 0.94,  and  0.94;  and  the  respective
median NRMSE values were 24%, 24%, 20%, and 20% (Figure 6).

Regardless of whether the original or modified MetroMan was applied, width refinement
yielded substantial improvements in estimation performance, increasing NSE by 0.42 and 0.37 and
KGE  by  0.33  and  0.23,  respectively.  Given  that  WSE  and  river  width  are  generally  positively
correlated under natural channel conditions (Huang et al., 2018b), the CC between WSE and width
time series was adopted as an indirect indicator of width measurement quality. Following width
refinement, the median width-WSE CC increased from 0.24 for original widths to 0.38 for refined
widths,  demonstrating  that  the  refined  width  measurements  effectively  improved  observation
quality and thereby established a more reliable foundation for accurate discharge estimation.

manuscript submitted to Water Resources Research

485

486
487
488
489
490
491

492
493
494
495
496
497
498
499
500
501
502

Figure 6. Comparison of original and refined width measurements in terms of discharge estimation accuracy
and correlation with WSE. (a) Box plots of NSE, KGE, CC, and NRMSE across four scenarios defined by the
combination of width type (original vs. refined) and posterior selection method (mean vs. peak of the MCMC
distribution). NSE, KGE, and CC are plotted on the left y-axis with a logarithmic scale, while NRMSE is plotted
on the right y-axis. (b) Histograms of CCs between WSE and width under original and refined scenarios, with
median correlations of 0.24 and 0.38, respectively.

River  width  not  only  directly  contributes  to  the  calculation  in  Equation  1,  but  also
influences  the  estimation  of  the  cross-sectional  area  change  δA.  As  a  result,  inaccurate  width
observations can propagate errors across the entire time series of discharge estimates. Furthermore,
because  the  total  cross-sectional  area  A  (A0+δA)  must  remain  positive  during  computation,
extremely  negative  δA  values  restrict  the  allowable  lower  bound  of  A0.  Reach  25210600571
(Figure S5a in Supporting Information) illustrates a typical case of A0 misestimation. Although no
anomalously  high  width  values  were  present,  the  original  width  time  series  was  highly  noisy,
necessitating  an  unrealistically  large  A0  to  satisfy  the  positivity  of  A  throughout  computation.
Consequently,  while  the  discharge  estimates  broadly  captured  the  temporal  dynamics,  the
magnitude was severely overestimated more than 20 times the in-situ measurements, yielding an
NSE of -8829.

manuscript submitted to Water Resources Research

503
504
505
506
507
508
509
510
511
512
513

514
515
516
517
518
519
520
521
522
523
524
525

526

527
528
529
530
531
532
533
534
535
536
537
538

Replacing  the  original  widths  with  the  refined  width  time  series,  which  exhibits
substantially  smoother  temporal  variation,  resolved  this  issue  and  improved  the  NSE  to  0.95.
Reach 74292100041 (Figure S5b in Supporting Information) was also affected by both noisy width
measurements.  Width variations  exceeding  half  the  prior width  within  only three  days  induced
correspondingly  large  short-term fluctuations  in  discharge  estimates. Moreover,  the cumulative
errors  in  A  resulted  in  a  persistent  overestimation  of discharge  after  June  2024,  with  estimates
ultimately diverging entirely from in-situ observations due to width anomalies. Following width
refinement, the NSE improved from -6.84 to 0.87. These results highlight SWOT’s potential for
accurate river width observations, while also revealing notable limitations in current products that
reduce discharge estimation accuracy across many reaches. Since accurate width observations are
a prerequisite for reliable discharge estimation, addressing these limitations is critical.

Although the MetroMan modification resulted in only a marginal increase in median NSE
of 0.01 and even a slight decrease in median KGE of 0.02, the modified version was nonetheless
adopted in our framework. The higher NSE of the modified MetroMan reflects more accurate FLP
estimation, particularly for A0, which is central to reliable discharge magnitude retrieval. Beyond
this, the modified version demonstrated greater robustness across varying observation conditions.
Under the original-width scenarios, the modified version achieved an improvement of 0.06 and
0.08 over the original in median NSE and KGE, respectively. When refined widths were applied,
the performance gains became marginal; nevertheless, the modified version still yielded positive
NSE and KGE values for 11 and 4 more  reaches than  the original  version,  respectively.  These
considerations collectively favor the modified MetroMan as the more reliable version. Regardless
of  the  algorithmic  variant  employed,  however,  accurate  river  width  observations  remain  a
prerequisite for the proper convergence of FLPs, particularly for A0.

4.3 Historical Discharge Reconstruction

We combined SWOT and Sentinel-3 observations to reconstruct discharge from 2016 to
2024. Conventional altimeters like Sentinel-3 only capture single hydrologic variables (i.e., WSE)
at  discrete  nadir  points,  making  discharge  estimation  challenging  without  gauge  data.  SWOT,
however,  provides  FLP  estimates  for  these  points  and  reaches,  thereby  enabling  historical
discharge reconstruction. To explore such potential, 122 reaches in the United States with positive
validation  NSE  (see  Section  4.1)  and  at  least  one  Sentinel-3  virtual  station  were  selected  for
analysis,  with  their  spatial  distribution  shown  in  Figure  7.  We  estimated  reach-averaged  WSS
based  on  SWOT  observations  and  established  width-WSE  relationships  using  a  two-segment
piecewise linear regression following the method of Durand et al. (2024), with a mean R2 of 0.32
across  all  selected  reaches.  We  then  estimated  historical  river  widths  by  combining  Sentinel-3
WSE  retrievals  with  the  established  width-WSE  relationships.  Finally,  we  calculated  historical
discharge using Equation 1.

manuscript submitted to Water Resources Research

539

540
541
542
543
544
545
546

547
548
549
550
551
552
553
554
555

Figure  7.  NSE  performance  of  historical  discharge  reconstruction  for  122  selected  river  reaches  across  the
United States, along with the geographic locations and discharge time series of two representative reaches. Circle
sizes represent prior river widths, and colors indicate NSE values. Gray and blue lines show rivers from the
SWORD  dataset.  Red  solid  lines  and  black  dashed  lines  denote  the  nadir  tracks  of  Sentinel-3  and  SWOT,
respectively, and red stars indicate Sentinel-3 virtual stations (i.e., direct measurement points at the intersections
of satellites’ ground tracks and river channels). The violin plot illustrates the distribution of NSE and KGE values
for the selected reaches, with median values of 0.67 and 0.65, respectively.

Across  all  122  selected  reaches,  the reconstructed  discharge  estimates  achieved  median
NSE of 0.67, KGE of 0.65, CC of 0.94, and NRMSE of 15%, indicating strong agreement with in-
situ  measurements  and  demonstrating  the  ability  of  our  framework  to  accurately  capture  both
discharge  magnitude  and  temporal  dynamics.  On  average,  each  reach  provided  39  discharge
estimates over the study period, approximately equivalent to six estimates per year. This temporal
frequency  is  considerably  lower than  that  achieved  using  SWOT  observations  alone,  primarily
constrained  by  the  coarser  temporal  resolution  of  Sentinel-3.  Reach  74225000031  in  Figure  7
exemplifies high-accuracy reconstruction, achieving an NSE of 0.95 with discharge estimates that
correctly capture both the magnitude and peak flow events from 2019 to 2021. Reach 8124730001

manuscript submitted to Water Resources Research

556
557
558
559
560
561
562

represents rivers subject to seasonal ice cover; by accurately excluding ice-affected observations,
our  framework  achieves  an  NSE  of  0.72,  demonstrating  robust  performance  under  diverse
hydrological conditions. The results confirm that our ungauged discharge reconstruction approach,
integrating SWOT with conventional altimetry data, achieves high accuracy and reliability. The
extended  temporal  coverage  provided  by  historical  discharge  reconstruction  offers  valuable
insights  for  long-term  hydrological  analysis  and  climate-driven  impact  assessment,  particularly
when earlier altimetry records (e.g., Jason-1/2/3, Envisat) are incorporated.

563

5 Discussion

564

565
566
567
568
569
570
571
572
573

574
575
576
577
578
579
580
581
582
583
584

5.1 Performance Degradation Investigation

Discharge estimates yielded negative NSE values across 152 reaches (39%) under refined-
width scenarios, prompting further investigation into the reasons of framework underperformance.
We  therefore  examined  the  impacts  of  tributary  inflow  and  downstream  hydraulic  control  on
discharge  estimation.  Tributary  inflow  represents  a  potential  source  of  error  because  the  mass
conservation in Equation 2 assumes negligible lateral inflow along each reach, yet unaccounted
contributions from tributaries effectively violate this assumption. Although reach selection was
designed to exclude reaches interrupted by dams or major confluences, the SWORD network was
developed  to  represent  only  rivers  with  sufficient  width  for  SWOT  observation,  meaning  that
smaller tributaries are not consistently captured in the network.

To identify reaches likely affected by this limitation, the sum of mean tributary discharge
for  each  reach  was  estimated  using  the  HydroRIVERS  network,  and  reaches  where  this  sum
exceeded  10%  of  mainstem  mean  discharge  were  flagged  as  tributary-influenced.  Figure  8a
summarizes  this  classification:  136  reaches  (35%)  were  identified  as  tributary-influenced,  with
median  NSE  and  KGE  values  of  0.21  and  0.34,  respectively,  compared  to  0.43  and  0.42  for
unaffected  reaches,  suggesting  that  tributary  inflow  is  one  contributing  factor  to  performance
degradation. Reach 74282100111 on the Illinois River serves as an illustrative example, where a
network of lateral channels alongside the main channel contributes substantial unaccounted inflow.
The  total  mean  tributary  discharge  reaches  79  m3/s,  equivalent  to  17%  of  the  mean  mainstem
discharge of 467 m3/s, introducing systematic errors in the estimation of A0 and propagating bias
throughout the discharge retrieval, ultimately yielding an NSE of -0.83 for this reach.

manuscript submitted to Water Resources Research

585

586
587
588
589
590
591

592
593
594
595
596
597
598
599
600
601
602
603
604

605

606
607

Figure 8. Two factors degrading discharge estimation accuracy. Left panels present box plots of NSE (green)
and KGE (blue) values, while right panels illustrate the geographic locations of representative reaches for each
scenario. (a) Impact of tributary inflow. The representative reach is located on the Illinois River, where tributary
inflow  accounts  for  17%  of  mean  mainstem  discharge,  resulting  in  a  reduced  NSE  of  -0.83.  (b)  Impact  of
downstream hydraulic control. The representative reach is located on the Columbia River, with flow dynamics
controlled by a downstream lake and a reduced NSE of -13.74.

Downstream hydraulic control represents a further source of performance degradation. For
reaches subject to downstream control, backwater effects may violate the assumption underlying
Equation 1, as WSS no longer represents the energy slope (Te Chow, 1959), leading to systematic
underestimation of discharge. Reaches within 30 km upstream of a lake, reservoir, or ocean were
identified as potentially affected by downstream  boundary  conditions and backwater effects. In
total, 107 out of 391 reaches fall into this category (27%), as shown in Figure 8b. The median NSE
and  KGE  for  these  reaches  are  -0.21  and  0.09,  respectively,  compared  to  0.47  and  0.49  for
unaffected  reaches,  indicating  that  downstream  control  constitutes  an  important  source  of
estimation error. Reach 78263000031 on the Columbia River exemplifies this effect: a lake and
dam immediately downstream of the study reach impose strong backwater influence, resulting in
an NSE of -13.74. These findings suggest that reach selection should account for the presence of
downstream  hydraulic  controls  and  overlooked  tributaries  to  avoid  reaches  susceptible  to
erroneous discharge estimation.

5.2 Global Implication

Our discharge estimation framework demonstrates promising results across 391 reaches,
suggesting its potential for large-scale application to over 100,000 river reaches worldwide. Within

manuscript submitted to Water Resources Research

608
609
610
611
612

613
614
615
616
617
618
619
620
621
622
623
624
625

626
627
628
629
630
631
632
633
634
635
636
637
638
639
640
641

642

643
644
645
646
647
648
649
650

the SWORD network, 163,579 reaches are classified as non-lacustrine rivers, of which 118,665
(73%) have sufficiently long continuous upstream and downstream reaches without intervening
reservoirs, dams, or major tributary confluences, rendering them applicable for our framework.
Notably,  totaling  99,607  reaches  (61%)  have  no  downstream  hydraulic  controls  within  30  km,
making them strong candidates for higher-accuracy discharge estimation.

Furthermore, our framework achieves consistent performance across a wide range of river
widths, from narrow channels to large rivers. Among the 46 narrow reaches with widths below
100 m, median NSE and KGE values were 0.30 and 0.42, respectively, comparable to the overall
performance  across  all  reaches.  Among  the  174  reaches  with  widths  between  100  and  200  m,
median  NSE  and  KGE  values  were  0.34  and  0.38,  respectively  (Figure  S6  in  Supporting
Information). However, scaling this methodology to global rivers presents several implementation
challenges  that  must  be  addressed.  The  MetroMan  algorithm’s  requirement  for  simultaneous
observations across continuous reaches means that outliers or missing observations in any single
reach can lead to the loss of valid information across all selected reaches. This may result in an
insufficient  number  of  observations  for  FLP  calibration.  Even  when  calibration  is  successfully
performed, data gaps compromise the effectiveness of mass conservation as a MCMC constraint,
necessitating  the  reconstruction  of  missing  values  using  spatially  and  temporally  neighboring
observations.

In recent years, artificial intelligence has advanced rapidly within hydrology, offering new
opportunities to further improve river discharge  estimation (Fang  et  al., 2024; He et al., 2025).
Among these approaches, graph neural networks (GNNs) have gained attention for their ability to
capture complex, nonlinear relationships while explicitly modeling system connectivity (Jumper
et al., 2021) River networks align closely with this graph-based paradigm, as they form branching,
directed  graphs  in  which  reaches  and  confluences  act  as  nodes,  while  edges  represent  flow
connections. Processes such as directional transport and tributary merging are inherently relational
and thus naturally expressed in graph form. GNNs can also integrate physical attributes of reaches
and edges, such as WSE, WSS, and river width, ensuring that hydrological connectivity and flow
directionality are preserved during learning. This structural compatibility makes GNNs especially
advantageous  compared  to  grid-based  or  sequence-based  models.  Building  on  these  strengths,
GNNs provide a promising approach to correct anomalous and missing values in river networks
via message passing, leveraging information from neighboring reaches and adjacent timesteps. By
embedding  physical  constraints  such  as  mass  conservation,  GNNs  hold  strong  potential  for
accurate  discharge  estimation  along  consecutive  reaches,  thereby  tracking  discharge  dynamics
even in regions where SWOT observations are heavily contaminated (i.e., nadir regions of SWOT).

6 Conclusion

This  study  developed  an  ungauged  discharge  estimation  framework  using  SWOT
observations, comprising three steps: (1) selecting continuous river reaches, (2) assembling high-
quality SWOT observation time-space arrays, and (3) applying the modified MetroMan algorithm
for discharge estimation. We preprocessed water surface elevation and slope based on consistency
between neighboring river reaches and optimized river width by isolating in-channel water pixels
automatically, to obtain  high-quality measurements.  The MetroMan  algorithm  was  modified in
two  aspects:  first,  we  changed  the  prior  distribution  of  the  initial  cross-sectional  area  A0  to  a
truncated normal distribution to prevent unbounded  growth  of  A0 during the  sampling process;

manuscript submitted to Water Resources Research

second, we employed the smoothed peak of the MCMC sampling distribution rather than the mean
to determine the posterior A0, thereby better aligning with mass conservation objectives.

The performance of our framework was validated across 391 gauging stations, with river
widths  ranging  from  42  to  1741  m,  encompassing  rivers  of  varying  sizes.  Discharge  estimates
derived from our framework achieved a median NSE of 0.30, a median KGE of 0.42, a median
CC of 0.94, and a median NRMSE of 20%, indicating that our framework effectively captured the
discharge  magnitude  and  temporal  variations  for  most  study  reaches.  Comparative  analysis
indicates  that  width  refinement  emerges  as  one  of  the  critical  factors  driving  performance
improvement, increasing median NSE and KGE by 0.37 and 0.23, respectively. Additionally, the
modified MetroMan demonstrates greater robustness than the original version, and river size does
not  exert  a  significant  influence  on  discharge  estimation  performance.  Tributary  inflow  and
downstream hydraulic controls contribute to degraded performance by violating the assumptions
of mass conservation and uniform flow.

Our  framework  enables  discharge  estimation  without  in-situ  constraints  by  leveraging
SWOT’s transformative observational capabilities. Given the increasing demand for global river
monitoring  and  the  declining  accessibility  of  in-situ  water  data,  our  framework  supports  large-
scale  applications.  Over  100,000  river  reaches  were  surveyed  as  potential  candidates  for  our
framework. Moreover, by integrating water level time series derived from Sentinel-3 altimetry, we
successfully  reconstructed  historical  discharge  across  122  river  reaches,  with  median  NSE  and
KGE  of  0.67  and  0.65,  respectively.  This  framework  demonstrates  the  potential  for  providing
discharge  estimates  over  extended  temporal  scales,  thereby  enhancing  our  capacity  to  detect
climate-driven influences on hydrological systems globally.

Acknowledgments

This  work  was  supported  by  the  National  Natural  Science  Foundation  of  China  (Grant
52325901,  42571432,  and  52509043).  Reviewers  and  editors’  comments  that  are  useful  in
improving this study and manuscript are acknowledged.

Open Research

through

the  USGS  Water  Data

The Sentinel-3 altimetry data used in this study  are available from  the Copernicus Data
Space Ecosystem at https://dataspace.copernicus.eu/explore-data. The USGS gauge data  can be
at
accessed
https://api.waterdata.usgs.gov/ogcapi/v0/.  The  GRDC  gauge  data  are available  from  the  Global
Runoff  Data  Centre  at  https://portal.grdc.bafg.de/applications/public.html.  The  SWOT  mission
data, including the river product, the raster product, and the discharge product, are available from
the  NASA  Physical  Oceanography  Distributed  Active  Archive  Center  (PO.DAAC)  at
https://podaac.jpl.nasa.gov/dataset/SWOT_L2_HR_RiverSP_2.0,
https://podaac.jpl.nasa.gov/dataset/SWOT_L2_HR_Raster_2.0,
and
https://podaac.jpl.nasa.gov/dataset/SWOT_L4_DAWG_SOS_DISCHARGE,  respectively.  The
code  and  processing  algorithms  developed  for  this  research  are  openly  available  on  GitHub  at
https://github.com/Liuhuaichuan/Ungauged-Discharge-Estimation-Framework/tree/main.

the  Nation

portal

for

References

Altenau, E. H., Pavelsky, T. M., Durand, M. T., Yang, X., Frasson, R. P. d. M., & Bendezu, L. (2021). The Surface

Water and Ocean Topography (SWOT) Mission River Database (SWORD): A global river network for

651
652

653
654
655
656
657
658
659
660
661
662
663

664
665
666
667
668
669
670
671
672

673

674
675
676

677

678
679
680
681
682
683
684
685
686
687
688
689

690

691
692

manuscript submitted to Water Resources Research

693
694
695
696
697
698
699
700
701
702
703
704
705
706
707
708
709
710
711
712
713
714
715
716
717
718
719
720
721
722
723
724
725
726
727
728
729
730
731
732
733
734
735
736
737
738
739
740
741
742
743
744
745
746
747

satellite data products. Water Resources Research, 57(7), e2021WR030054.
https://doi.org/10.1029/2021WR030054

Amatulli, G., Marquez, J. G., Sethi, T., Kiesel, J., Grigoropoulou, A., Üblacker, M. M., et al. (2022).

Hydrography90m: a new high-resolution global hydrographic dataset. Earth System Science Data, 14(10),
4525–4550. https://doi.org/10.5194/essd-14-4525-2022

Andreadis, K. M., Brinkerhoff, C. B., & Gleason, C. J. (2020). Constraining the Assimilation of SWOT

Observations With Hydraulic Geometry Relations. Water Resources Research, 56(5), e2019WR026611.
https://doi.org/10.1029/2019WR026611

Andreadis, K. M., Coss, S. P., Durand, M., Gleason, C. J., Simmons, T. T., Tebaldi, N., et al. (2025). A first look at
river discharge estimation from SWOT satellite observations. Geophysical Research Letters, 52(9),
e2024GL114185. https://doi.org/10.1029/2024GL114185

Archer, M., Wang, J. B., Klein, P., Dibarboure, G., & Fu, L. L. (2025). Wide-swath satellite altimetry unveils global
submesoscale ocean dynamics. Nature, 640(8059). https://doi.org/10.1038/s41586-025-08722-8
Biancamaria, S., Lettenmaier, D. P., & Pavelsky, T. M. (2016). The SWOT Mission and Its Capabilities for Land

Hydrology. In A. Cazenave, N. Champollion, J. Benveniste, & J. Chen (Eds.), Remote Sensing and Water
Resources (pp. 117–147). Cham: Springer International Publishing.

Bloeschl, G., Hall, J., Viglione, A., Perdigao, R. A. P., Parajka, J., Merz, B., et al. (2019). Changing climate both

increases and decreases European river floods. Nature, 573(7772), 108–+. https://doi.org/10.1038/s41586-
019-1495-6

Bonnema, M. G., Sikder, S., Hossain, F., Durand, M., Gleason, C. J., & Bjerklie, D. M. (2016). Benchmarking wide
swath altimetry-based river discharge estimation algorithms for the Ganges river system. Water Resources
Research, 52(4), 2439–2461. https://doi.org/10.1002/2015WR017296

Brakenridge, G. R., Nghiem, S. V., Anderson, E., & Mic, R. (2007). Orbital microwave measurement of river

discharge and ice status. Water Resources Research, 43(4). https://doi.org/10.1029/2006wr005238

Cerbelaud, A., David, C. H., Pavelsky, T., Biancamaria, S., Garambois, P. A., Kittel, C., et al. (2025). Satellite
Requirements to Capture Water Propagation in Earth's Rivers. Reviews of Geophysics, 63(3).
https://doi.org/10.1029/2024RG000871

Cerbelaud, A., Wade, J., David, C. H., Durand, M., Frasson, R. P. M., Pavelsky, T., & Oubanas, H. (2026). Wide-

swath altimetry maps bank shapes and storage changes in global rivers. Nature, 651(8106), 666–671.
https://doi.org/10.1038/s41586-026-10218-y

Davids, J. C., Rutten, M. M., Pandey, A., Devkota, N., van Oyen, W. D., Prajapati, R., & van de Giesen, N. (2019).

Citizen science flow - an assessment of simple streamflow measurement methods. Hydrology and Earth
System Sciences, 23(2), 1045–1065. https://doi.org/10.5194/hess-23-1045-2019

Durand, M., Chen, C., Frasson, R. P. D., Pavelsky, T. M., Williams, B., Yang, X., & Fore, A. (2020). How will
radar layover impact SWOT measurements of water surface elevation and slope, and estimates of river
discharge? Remote Sensing of Environment, 247. https://doi.org/10.1016/j.rse.2020.111883

Durand, M., Dai, C., Moortgat, J., Yadav, B., de Moraes Frasson, R. P., Li, Z., et al. (2024). Using river hypsometry

to improve remote sensing of river discharge. Remote Sensing of Environment, 315, 114455.
https://doi.org/10.1016/j.rse.2024.114455

Durand, M., Gleason, C. J., Pavelsky, T. M., Prata de Moraes Frasson, R., Turmon, M., David, C. H., et al. (2023).

A Framework for Estimating Global River Discharge From the Surface Water and Ocean Topography
Satellite Mission. Water Resources Research, 59(4), e2021WR031614.
https://doi.org/10.1029/2021WR031614

Durand, M., Neal, J., Rodríguez, E., Andreadis, K. M., Smith, L. C., & Yoon, Y. (2014). Estimating reach-averaged

discharge for the River Severn from measurements of river water surface elevation and slope. Journal of
Hydrology, 511, 92–104. https://doi.org/10.1016/j.jhydrol.2013.12.050

Fang, C., Long, D., Huang, Q., Cretaux, J.-F., Papa, F., Frappart, F., et al. (2025b). Satellite altimetry reveals

intensifying global river water level variability. Nature Communications, 17(1), 958.
https://doi.org/10.1038/s41467-025-67682-9

Fang, C., Long, D., Huang, Q., Zhao, F., Liu, H., Duan, X., & Hou, A. (2025a). Improved water level retrieval in

complex riverine environments: Sentinel-3 and Sentinel-6 altimetry over China's rivers. Water Resources
Research, 61(4), e2024WR039705. https://doi.org/10.1029/2024WR039705

Fang, C., Yuan, G., Zheng, Z., Zhong, Q., & Duan, K. (2024). Monitoring discharge of mountain streams by

retrieving image features with deep learning. Hydrology and Earth System Sciences, 28(17), 4085–4098.
https://doi.org/10.5194/hess-28-4085-2024

manuscript submitted to Water Resources Research

748
749
750
751
752
753
754
755
756
757
758
759
760
761
762
763
764
765
766
767
768
769
770
771
772
773
774
775
776
777
778
779
780
781
782
783
784
785
786
787
788
789
790
791
792
793
794
795
796
797
798
799
800
801
802
803

Fekete, B. M., Robarts, R. D., Kumagai, M., Nachtnebel, H. P., Odada, E., & Zhulidov, A. V. (2015). Time for in

situ renaissance. Science, 349(6249), 685–686. https://doi.org/10.1126/science.aac7358

Fjortoft, R., Gaudin, J. M., Pourthié, N., Lalaurie, J. C., Mallet, A., Nouvel, J. F., et al. (2014). KaRIn on SWOT:
Characteristics of Near-Nadir Ka-Band Interferometric SAR Imagery. Ieee Transactions on Geoscience
and Remote Sensing, 52(4), 2172–2185. https://doi.org/10.1109/Tgrs.2013.2258402

Frasson, R. P. d. M., Durand, M. T., Larnier, K., Gleason, C., Andreadis, K. M., Hagemann, M., et al. (2021).

Exploring the factors controlling the error characteristics of the Surface Water and Ocean Topography
mission discharge estimates. Water Resources Research, 57(6), e2020WR028519.
https://doi.org/10.1029/2020WR028519

Fu, L. L., Pavelsky, T., Cretaux, J. F., Morrow, R., Farrar, J. T., Vaze, P., et al. (2024). The Surface Water and

Ocean Topography Mission: A Breakthrough in Radar Remote Sensing of the Ocean and Land Surface
Water. Geophysical Research Letters, 51(4). https://doi.org/10.1029/2023GL107652

Getirana, A., Kumar, S., Bates, P., Boone, A., Lettenmaier, D., & Munier, S. (2024). The SWOT mission will

reshape our understanding of the global terrestrial water cycle. Nature Water, 2(12), 1139–1142.
https://doi.org/10.1038/s44221-024-00352-0

Gleason, C. J., Smith, L. C., & Lee, J. (2014). Retrieval of river discharge solely from satellite imagery and at-

many-stations hydraulic geometry: Sensitivity to river form and optimization parameters. Water Resources
Research, 50(12), 9604–9619. https://doi.org/10.1002/2014wr016109

Gudmundsson, L., Boulange, J., Do, H. X., Gosling, S. N., Grillakis, M. G., Koutroulis, A. G., et al. (2021).

Globally observed trends in mean and extreme river flow attributed to climate change. Science, 371(6534),
1159–+. https://doi.org/10.1126/science.aba3996

Hagemann, M. W., Gleason, C. J., & Durand, M. T. (2017). BAM: Bayesian AMHG-Manning Inference of

Discharge Using Remotely Sensed Stream Width, Slope, and Height. Water Resources Research, 53(11),
9692–9707. https://doi.org/10.1002/2017WR021626

He, M., Jiang, S. H., Ren, L. L., Cui, H., Du, S. P., Zhu, Y. W., et al. (2025). Exploring the performance and

interpretability of hybrid hydrologic model coupling physical mechanisms and deep learning. Journal of
Hydrology, 649. https://doi.org/10.1016/j.jhydrol.2024.132440

Huang, Q., Long, D., Du, M., Han, Z., & Han, P. (2020). Daily Continuous River Discharge Estimation for

Ungauged Basins Using a Hydrologic Model Calibrated by Satellite Altimetry: Implications for the SWOT
Mission. Water Resources Research, 56(7). https://doi.org/10.1029/2020WR027309

Huang, Q., Long, D., Du, M., Zeng, C., Li, X., Hou, A., & Hong, Y. (2018a). An improved approach to monitoring
Brahmaputra River water levels using retracked altimetry data. Remote Sensing of Environment, 211, 112–
128. https://doi.org/10.1016/j.rse.2018.04.018

Huang, Q., Long, D., Du, M., Zeng, C., Qiao, G., Li, X., et al. (2018b). Discharge estimation in high-mountain

regions with improved methods using multisource remote sensing: A case study of the Upper Brahmaputra
River. Remote Sensing of Environment, 219, 115–134. https://doi.org/10.1016/j.rse.2018.10.008
Jaramillo, F., Aminjafari, S., Castellazzi, P., Fleischmann, A., Fluet-Chouinard, E., Hashemi, H., et al. (2024). The

Potential of Hydrogeodesy to Address Water-Related and Sustainability Challenges. Water Resources
Research, 60(11). https://doi.org/10.1029/2023WR037020

JPL, D. (2023). 105505,"SWOT Algorithm Theoretical Basis Document: Level 2 KaRIn High Rate River Single Pass

(L2_HR_RiverSP) Science Algorithm Software,". Retrieved from https://epdm.jpl.nasa.gov

Jumper, J., Evans, R., Pritzel, A., Green, T., Figurnov, M., Ronneberger, O., et al. (2021). Highly accurate protein

structure prediction with AlphaFold. Nature, 596(7873), 583–+. https://doi.org/10.1038/s41586-021-03819-
2

Krabbenhoft, C. A., Allen, G. H., Lin, P. R., Godsey, S. E., Allen, D. C., Burrows, R. M., et al. (2022). Assessing

placement bias of the global river gauge network. Nature Sustainability, 5(7), 586–592.
https://doi.org/10.1038/s41893-022-00873-0

Kreibich, H., Van Loon, A. F., Schröter, K., Ward, P. J., Mazzoleni, M., Sairam, N., et al. (2022). The challenge of

unprecedented floods and droughts in risk management. Nature, 608(7921), 80–+.
https://doi.org/10.1038/s41586-022-04917-5

Larnier, K., Monnier, J., Garambois, P.-A., & Verley, J. (2020). River discharge and bathymetry estimation from
SWOT altimetry measurements. Inverse problems in science and engineering, 29(6), 759–789.
https://doi.org/10.1080/17415977.2020.1803858

Le Coz, J., Renard, B., Bonnifait, L., Branger, F., & Le Boursicaud, R. (2014). Combining hydraulic knowledge and
uncertain gaugings in the estimation of hydrometric rating curves: A Bayesian approach. Journal of
Hydrology, 509, 573–587. https://doi.org/10.1016/j.jhydrol.2013.11.016

manuscript submitted to Water Resources Research

804
805
806
807
808
809
810
811
812
813
814
815
816
817
818
819
820
821
822
823
824
825
826
827
828
829
830
831
832
833
834
835
836
837
838
839
840
841
842
843
844
845
846
847
848
849
850
851
852
853
854
855
856
857
858
859

Lehner, B., & Grill, G. (2013). Global river hydrography and network routing: baseline data and new approaches to

study the world's large river systems. Hydrological Processes, 27(15), 2171–2186.
https://doi.org/10.1002/hyp.9740

Leon, J. G., Calmant, S., Seyler, F., Bonnet, M. P., Cauhopé, M., Frappart, F., et al. (2006). Rating curves and

estimation of average water depth at the upper Negro River based on satellite altimeter data and modeled
discharges. Journal of Hydrology, 328(3-4), 481–496. https://doi.org/10.1016/j.jhydrol.2005.12.006

Lin, P., Pan, M., Beck, H. E., Yang, Y., Yamazaki, D., Frasson, R., et al. (2019). Global Reconstruction of
Naturalized River Flows at 2.94 Million Reaches. Water Resources Research, 55(8), 6499–6516.
https://doi.org/10.1029/2019WR025287

Liu, Z. F. (2023). Accuracy of satellite precipitation products in data-scarce Inner Tibetan Plateau comprehensively
evaluated using a novel ground observation network. Journal of Hydrology-Regional Studies, 47.
https://doi.org/10.1016/j.ejrh.2023.101405

Masafu, C., Williams, R., & Hurst, M. D. (2023). Satellite Video Remote Sensing for Estimation of River
Discharge. Geophysical Research Letters, 50(24). https://doi.org/10.1029/2023GL105839

Nanesso, D. A. A. (2024). The application of satellite sensors, current state of utilization, and sources of remote

sensing dataset in hydrology for water resource management. Journal of Water and Health, 22(7), 1162–
1179. https://doi.org/10.2166/wh.2024.102

Oubanas, H., Gejadze, I., Malaterre, P.-O., Durand, M., Wei, R., Frasson, R. P. M., & Domeneghetti, A. (2018).
Discharge Estimation in Ungauged Basins Through Variational Data Assimilation: The Potential of the
SWOT Mission. Water Resources Research, 54(3), 2405–2423. https://doi.org/10.1002/2017WR021735

Pavelsky, T. M. (2014). Using width- based rating curves from spatially discontinuous satellite imagery to monitor
river discharge. Hydrological Processes, 28(6), 3035–3040. https://doi.org/10.1002/hyp.10157
Perkins-Kirkpatrick, S., Barriopedro, D., Jha, R., Wang, L., Mondal, A., Libonati, R., & Kornhuber, K. (2024).

Extreme terrestrial heat in 2023. Nature Reviews Earth & Environment, 5(4), 244–246.
https://doi.org/10.1038/s43017-024-00536-y

Shu, S., Liu, H., Beck, R. A., Frappart, F., Korhonen, J., Xu, M., et al. (2020). Analysis of Sentinel-3 SAR altimetry

waveform retracking algorithms for deriving temporally consistent water levels over ice-covered lakes.
Remote Sensing of Environment, 239, 111643. https://doi.org/10.1016/j.rse.2020.111643

Sui, X., Zhang, R., Wu, F., Li, Y., & Wan, X. (2017). Sea surface height measuring using InSAR altimeter. Geodesy

and Geodynamics, 8(4), 278–284. https://doi.org/10.1016/j.geog.2017.03.005

SWOT. (2024a). SWOT Level 2 River Single-Pass Vector Data Product. Retrieved from:

https://podaac.jpl.nasa.gov/dataset/SWOT_L2_HR_RiverSP_2.0

SWOT. (2024b). SWOT Level 2 Water Mask Raster Image Data Product. Retrieved from:

https://podaac.jpl.nasa.gov/dataset/SWOT_L2_HR_Raster_2.0

SWOT Discharge Algorithm Working Group. (2023). SWOT Sword of Science River Discharge Products Version 1.

Retrieved from: https://podaac.jpl.nasa.gov/dataset/SWOT_L4_DAWG_SOS_DISCHARGE
Tarpanelli, A., Brocca, L., Barbetta, S., Faruolo, M., Lacava, T., & Moramarco, T. (2015). Coupling MODIS and
Radar Altimetry Data for Discharge Estimation in Poorly Gauged River Basins. Ieee Journal of Selected
Topics in Applied Earth Observations and Remote Sensing, 8(1), 141–148.
https://doi.org/10.1109/Jstars.2014.2320582

Tarpanelli, A., Paris, A., Sichangi, A. W., O'Loughlin, F., & Papa, F. (2023). Water Resources in Africa: The Role

of Earth Observation Data and Hydrodynamic Modeling to Derive River Discharge. Surveys in Geophysics,
44(1), 97–122. https://doi.org/10.1007/s10712-022-09744-x

Te Chow, V. (1959). Open channel hydraulics.
Vörösmarty, C. J., McIntyre, P. B., Gessner, M. O., Dudgeon, D., Prusevich, A., Green, P., et al. (2010). Global
threats to human water security and river biodiversity (vol 467, pg 555, 2010). Nature, 468(7321), 334–
334. https://doi.org/10.1038/nature09549

Xu, J., Yuan, Z., Xu, Y., & Lin, P. (2026). Leveraging “SWOT and a-priori information (SWAP)” constrained

channel parameters for improved historical river discharge estimates from space. ISPRS Journal of
Photogrammetry and Remote Sensing, 235, 536–550. https://doi.org/10.1016/j.isprsjprs.2026.03.034

Yang, X., Pavelsky, T. M., Allen, G. H., & Donchyts, G. (2020). RivWidthCloud: An Automated Google Earth

Engine Algorithm for River Width Extraction From Remotely Sensed Imagery. Ieee Geoscience and
Remote Sensing Letters, 17(2), 217–221. https://doi.org/10.1109/Lgrs.2019.2920225

Yang, Y., Feng, D., Beck, H. E., Hu, W., Abbas, A., Sengupta, A., et al. (2025). Global Daily Discharge Estimation
Based on Grid Long Short-Term Memory (LSTM) Model and River Routing. Water Resources Research,
61(6), e2024WR039764. https://doi.org/10.1029/2024WR039764

manuscript submitted to Water Resources Research

Zakharova, E. A., Krylenko, I. N., & Kouraev, A. V. (2019). Use of non-polar orbiting satellite radar altimeters of

the Jason series for estimation of river input to the Arctic Ocean. Journal of Hydrology, 568, 322–333.
https://doi.org/10.1016/j.jhydrol.2018.10.068

Zhang, T. Y., & Suen, C. Y. (1984). A fast parallel algorithm for thinning digital patterns. Commun. ACM, 27(3),

236–239. https://doi.org/10.1145/357994.358023

860
861
862
863
864
865

Figure 1.

1200

)

m

(

h
t
d
W

i

800

400

200

50

)
s
/
3
m

(

e
g
r
a
h
c
s
d
r
o
i
r

i

P

6000

3000

1000

200

0

Width

Discharge

River width (m)
100
1000

Prior discharge
(m3/s)

10

5000

River

(cid:20)(cid:24)(cid:131)(cid:19)(cid:131)(cid:16)(cid:20)(cid:24)(cid:131)(cid:16)(cid:22)(cid:19)(cid:131)(cid:23)(cid:24)(cid:131)(cid:22)(cid:19)(cid:131)(cid:20)(cid:24)(cid:131)(cid:19)(cid:131)(cid:16)(cid:20)(cid:24)(cid:131)(cid:19)(cid:21)(cid:15)(cid:19)(cid:19)(cid:19)(cid:78)(cid:80)(cid:16)(cid:21)(cid:19)(cid:131)(cid:16)(cid:22)(cid:19)(cid:131)(cid:16)(cid:23)(cid:19)(cid:131)(cid:20)(cid:26)(cid:19)(cid:131)(cid:20)(cid:25)(cid:19)(cid:131)(cid:20)(cid:24)(cid:19)(cid:131)(cid:20)(cid:23)(cid:19)(cid:131)(cid:20)(cid:22)(cid:19)(cid:131)(cid:19)(cid:20)(cid:15)(cid:19)(cid:19)(cid:19)(cid:21)(cid:15)(cid:19)(cid:19)(cid:19)(cid:78)(cid:80)(cid:26)(cid:19)(cid:131)(cid:25)(cid:19)(cid:131)(cid:24)(cid:19)(cid:131)(cid:23)(cid:19)(cid:131)(cid:22)(cid:19)(cid:131)(cid:21)(cid:19)(cid:131)(cid:20)(cid:19)(cid:131)(cid:19)(cid:131)(cid:16)(cid:20)(cid:19)(cid:131)(cid:19)(cid:20)(cid:15)(cid:19)(cid:19)(cid:19)(cid:21)(cid:15)(cid:19)(cid:19)(cid:19)(cid:78)(cid:80)(cid:25)(cid:19)(cid:131)(cid:23)(cid:24)(cid:131)(cid:22)(cid:19)(cid:131)(cid:16)(cid:26)(cid:24)(cid:131)(cid:16)(cid:28)(cid:19)(cid:131)(cid:16)(cid:20)(cid:19)(cid:24)(cid:131)(cid:16)(cid:20)(cid:21)(cid:19)(cid:131)(cid:16)(cid:20)(cid:22)(cid:24)(cid:131)(cid:16)(cid:20)(cid:24)(cid:19)(cid:131)(cid:16)(cid:20)(cid:25)(cid:24)(cid:131)(cid:19)(cid:21)(cid:15)(cid:19)(cid:19)(cid:19)(cid:23)(cid:15)(cid:19)(cid:19)(cid:19)(cid:78)(cid:80)

Figure 2.

SWOT

Data acquisition

Reach 1

Reach 3

Reach 2

Reach 4

SWOT Level 2 River Product
(Width obs. is very noisy)

Apply upstream-downstream
constraints for filtering

River reach

T1

T2

T3

…

Reach 1

Reach 2

…

S11, W11, H11

S12, W12, H12

S13, W13, H13

S21, W21, H21

S22, W22, H22

S23, W23, H23

Refine
width obs.

Input

Reach 5

SWOT Level 2 Raster Product

ROI

T1
T2
T3

Determine posterior parameters

Determine prior parameters

, 0, 1

Θ) × exp[−

,
( − ̅)

,
1
2

MCMC

Constrain

−1

( − ̅)]

Peak

MCMC

, 0, 1 ∼ ln ( ,

2

)

0 = 0.27

Prior

0.39

0.5

× 7.2
for all reaches

Θ Θ
(−
Mass residual

1
2

−1

Θ =

, +

,

( , )

Posterior

for all reaches

, 0, 1

, = , × [1 +

1,

,

0, +

5/6

2

]

,

, =

1
, ( 0, +

5/3

, )

−2/3
,

,

Estimate reach discharge

River reach

Reach 1

Reach 2

…

T1

Q11

Q21

T2

Q12

Q22

T3 …

Q13

Q23

, 0, 1

0

0

0.05

0.1

Reach 1–5

̅
Figure 3.

Reach ID: 78220000171

2023-09-28

2024-03-26
Reach ID: 78220000151

2024-09-22

100

80

60

40

20

0

)

m
k
/
m
c
(

e
p
o
S

l

2023-04-01

100

80

60

40

20

0

)

m
k
/
m
c
(

e
p
o
S

l

Reach ID: 78220000161

2023-09-28

2024-03-26
Reach ID: 78220000141

2024-09-22

100

80

60

40

20

0

46

44

42

40

38

2023-04-01

100

40

80

38

60

40

20

0

36

34

32

)

m

(

E
S
W

)

m

(

E
S
W

42

40

38

36

34

36

34

32

30

28

2023-04-01

2023-09-28

2024-03-26

2024-09-22

2023-04-01

2023-09-28

2024-03-26

2024-09-22

Figure 4.

Non-water
Riverine environment

Channel water

Removed water

Skeleton

Raster observations

Buffer filtering

Connectivity    filtering

Lake filtering

Skeleton pruning

1
C
C

/
.
d
t
S

/
.
u
n
S

i

max 0.5
t1

…

tn

2 − 0.2

. +0.3

.

Distance along river

t

h
d
w

i

r
e
v
R

i

t1

…

tn

Figure 5.

(a)

1

0

E
G
K

−1

−5

−15

(b)

1

0

E
S
N

−1

−5

−15

HiVDI

MetroMan MOMMA

geoBAM

SAD

SIC4DVar

1.0

0.5

0.0

C
C

−0.5

−1.0

0

25

100

250

)

%

(

E
S
M
R
N

HiVDI

MetroMan MOMMA

geoBAM

SAD

SIC4DVar

Figure 6.

(a)

(b)

(cid:20)(cid:17)(cid:19)

(cid:19)(cid:17)(cid:24)

(cid:19)(cid:17)(cid:19)

C
C

/

E
G
K

/

(cid:237)(cid:19)(cid:17)(cid:24)

E
S
N

(cid:237)(cid:20)(cid:17)(cid:19)

(cid:237)(cid:24)(cid:17)(cid:19)

60

40

t
n
u
o
C

20

0

(cid:19)

(cid:21)(cid:19)

(cid:23)(cid:19)

(cid:25)(cid:19)

(cid:27)(cid:19)

)

%

(

E
S
M
R
N

Original obs.
(Mean-based)

Original obs.
(Peak-based)

Refined obs.
(Mean-based)

Refined obs.
(Peak-based)

Original obs.
Refined obs.

−0.4

−0.2

0.0

0.2

CC

0.4

0.6

0.8

1.0

Figure 7.

NSE

-1

1

SWOT
nadir track

Sentinel-3
nadir track

Sentinel-3
virtual station

River

Reach ID: 81247300011

In-situ
S3 Reconstruction

NSE:
0.72

2020-01-01

2021-01-01

2022-01-01

2023-01-01

2024-01-01

1.0

0.5

0.0

−0.5

−1.0

−1.5

E
G
K

NSE

KGE

Reach ID: 74225000031
In-situ
S3 Reconstruction

NSE:
0.95

)
s
/
3
m

(

e
g
r
a
h
c
s
D

i

3000

2500

2000

1500

1000

500

0

1.0

0.5

0.0

E
S
N

−0.5

−1.0

−1.5

)
s
/
3
m

(

e
g
r
a
h
c
s
D

i

2500

2000

1500

1000

500

0

2019-01-01

2020-01-01

2021-01-01

2022-01-01

2023-01-01

2024-01-01

(cid:25)(cid:24)(cid:131)(cid:25)(cid:23)(cid:131)(cid:22)(cid:19)(cid:10)(cid:16)(cid:20)(cid:23)(cid:26)(cid:131)(cid:16)(cid:20)(cid:23)(cid:26)(cid:131)(cid:22)(cid:19)(cid:10)(cid:16)(cid:20)(cid:23)(cid:27)(cid:131)(cid:25)(cid:19)(cid:131)(cid:23)(cid:24)(cid:131)(cid:22)(cid:19)(cid:131)(cid:16)(cid:26)(cid:24)(cid:131)(cid:16)(cid:28)(cid:19)(cid:131)(cid:16)(cid:20)(cid:19)(cid:24)(cid:131)(cid:16)(cid:20)(cid:21)(cid:19)(cid:131)(cid:16)(cid:20)(cid:22)(cid:24)(cid:131)(cid:16)(cid:20)(cid:24)(cid:19)(cid:131)(cid:16)(cid:20)(cid:25)(cid:24)(cid:131)(cid:19)(cid:21)(cid:15)(cid:19)(cid:19)(cid:19)(cid:23)(cid:15)(cid:19)(cid:19)(cid:19)(cid:78)(cid:80)(cid:22)(cid:22)(cid:131)(cid:23)(cid:19)(cid:10)(cid:22)(cid:22)(cid:131)(cid:22)(cid:24)(cid:10)(cid:22)(cid:22)(cid:131)(cid:22)(cid:19)(cid:10)(cid:16)(cid:28)(cid:22)(cid:131)(cid:24)(cid:19)(cid:10)(cid:16)(cid:28)(cid:22)(cid:131)(cid:24)(cid:24)(cid:10)(cid:16)(cid:28)(cid:23)(cid:131)(cid:16)(cid:28)(cid:23)(cid:131)(cid:24)(cid:10)(cid:16)(cid:28)(cid:23)(cid:131)(cid:20)(cid:19)(cid:10)

Figure 8.

(a)

(b)

1.0

0.5

0.0

E
G
K

/

E
S
N

−0.5

−1.0

1.0

0.5

0.0

E
G
K

/

E
S
N

−0.5

−1.0

NSE

KGE

Mainstem

Tributary

74282100111
Illinois River

<0.1

≥0.1

Qtrib / Qmain

78263000031
Columbia River

No

Yes

Downstream boundary control

(cid:23)(cid:27)(cid:131)(cid:20)(cid:19)(cid:10)(cid:23)(cid:27)(cid:131)(cid:24)(cid:10)(cid:23)(cid:27)(cid:131)(cid:16)(cid:20)(cid:20)(cid:28)(cid:131)(cid:22)(cid:24)(cid:10)(cid:16)(cid:20)(cid:20)(cid:28)(cid:131)(cid:23)(cid:19)(cid:10)(cid:16)(cid:20)(cid:20)(cid:28)(cid:131)(cid:23)(cid:24)(cid:10)(cid:22)(cid:28)(cid:131)(cid:24)(cid:24)(cid:10)(cid:22)(cid:28)(cid:131)(cid:24)(cid:19)(cid:10)(cid:22)(cid:28)(cid:131)(cid:23)(cid:24)(cid:10)(cid:16)(cid:28)(cid:19)(cid:131)(cid:21)(cid:19)(cid:10)(cid:16)(cid:28)(cid:19)(cid:131)(cid:21)(cid:24)(cid:10)(cid:16)(cid:28)(cid:19)(cid:131)(cid:22)(cid:19)(cid:10)(cid:16)(cid:28)(cid:19)(cid:131)(cid:22)(cid:24)(cid:10)

