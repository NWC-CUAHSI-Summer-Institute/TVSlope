RESEARCH ARTICLE
10.1029/2024WR039574

Key Points:
• The use of remote sensing‐derived

flood maps is an attractive but under‐
studied source of benchmark data
• Accuracy of model‐predicted inunda-
tion evaluation is greatly affected by
the quality of the benchmark maps and
the exclusion of permanent water

• A novel evaluation strategy is

presented that mitigates biases in the
evaluation analysis by excluding low‐
confidence pixels in the benchmark

Correspondence to:

S. Cohen,
sagy.cohen@ua.edu

Citation:

Cohen, S., Baruah, A., Nikrou, P., Tian, D.,
& Liu, H. (2025). Toward robust
evaluations of flood inundation predictions
using remote sensing derived benchmark
maps. Water Resources Research, 61,
e2024WR039574. https://doi.org/10.1029/
2024WR039574

Toward Robust Evaluations of Flood Inundation Predictions
Using Remote Sensing Derived Benchmark Maps
Sagy Cohen1

, Dan Tian1, and Hongxing Liu1

, Parvaneh Nikrou1

, Anupal Baruah1

1The Department of Geography and the Environment, University of Alabama, Tuscaloosa, AL, USA

Abstract Remote Sensing‐derived Flood Inundation Maps (RS‐FIM) are an attractive and commonly used
source of evaluation benchmarks. In this paper, we investigate several sources of bias in RS‐FIM benchmarking
and their effect on model‐predicted FIM (M‐FIM) evaluation results. We do so by comparing M‐FIM evaluation
results using a high‐confidence benchmark against degraded benchmarks. The evaluation results show
considerable differences in M‐FIM accuracy assessment when using lower‐quality benchmarks. An RS‐FIM
enhancement (gap‐filling) procedure is presented, and its effect on FIM evaluation results is analyzed. The
results show that the enhancement can significantly improve the robustness of the evaluation, but can also
degrade the benchmark when a considerable number of false‐positive grid cells are present in the RS‐FIM. The
impact of including/excluding Permanent Water Bodies (PWB) on FIM evaluation results is analyzed. The
results show that including PWB in FIM evaluation can significantly inflate the model accuracy. A novel
evaluation strategy is proposed, based on excluding low‐confidence grid cells and PWB from the M‐FIM
evaluation analysis. Low‐confidence grid cells are those that were estimated to be flooded by the gap‐filling
procedure, but were not classified as such by the remote sensing analysis. The results show that the proposed
evaluation strategy can considerably improve the robustness of the evaluation. The analyses showcase the many
challenges in FIM evaluation. We provide an in‐depth discussion about the need for standards, user‐centric
evaluation, the use of secondary sources, and qualitative evaluation.

Received 29 NOV 2024
Accepted 11 JUL 2025

1. Introduction

Author Contributions:

Conceptualization: Sagy Cohen
Data curation: Sagy Cohen, Dan Tian
Formal analysis: Sagy Cohen,
Anupal Baruah
Funding acquisition: Sagy Cohen,
Hongxing Liu
Investigation: Sagy Cohen
Methodology: Sagy Cohen, Dan Tian
Project administration: Sagy Cohen
Resources: Sagy Cohen, Anupal Baruah,
Parvaneh Nikrou
Software: Sagy Cohen
Supervision: Hongxing Liu
Validation: Sagy Cohen
Visualization: Sagy Cohen,
Parvaneh Nikrou
Writing – original draft: Sagy Cohen
Writing – review & editing:
Anupal Baruah, Parvaneh Nikrou,
Dan Tian, Hongxing Liu

© 2025. The Author(s).
This is an open access article under the
terms of the Creative Commons
Attribution‐NonCommercial‐NoDerivs
License, which permits use and
distribution in any medium, provided the
original work is properly cited, the use is
non‐commercial and no modifications or
adaptations are made.

COHEN ET AL.

Model‐predicted Flood Inundation Maps (FIM) are essential for flood analysis and planning (e.g., Hawker
et al., 2024; Hooker et al., 2022, 2023; Jafarzadegan et al., 2021; Sanderson et al., 2023). A proliferation of FIM
prediction capabilities has emerged in recent years within national and global hydrological forecasting frame-
works. Prime examples include the United States (US) National Oceanic and Atmospheric Administration
the European Commission's Copernicus
(NOAA) National Water Model (NWM; https://water.noaa.gov),
Emergency Management Service Global Flood Awareness System (GloFAS; https://global‐flood.emergency.
copernicus.eu) and the Google Flood Forecasting framework (https://sites.research.google/floodforecasting/).
These, and similar, frameworks link forecasted hydrological (streamflow) predictions to an FIM solver, typically
a pre‐canned hydraulic simulation results (when a series of model simulations are calculated ahead of time for
each river segment; e.g. LISFLOOD‐FP for GloFAS), a low‐complexity FIM predictor (e.g., Height Above
Nearest Drainage for NWM (Aristizabal et al., 2024)), or a data‐driven model (e.g., Remote Sensing trained
Machine Learning for Google).

FIM prediction accuracy is, naturally, of great importance for model developers and users. It becomes a crucial
element in operational forecasting systems as these aim to inform decision‐making and response, while gaining/
maintaining trust in their predictions. However, accuracy assessment of FIM predictions is challenging (Hawker
et al., 2024; Herbanu et al., 2024; Hunter et al., 2005; Schumann, Bates, et al., 2009; Schumann, Di Baldassarre, &
Bates, 2009; Stephens et al., 2012, 2014; Venkata Rao et al., 2024) due to, among other factors, (a) severe scarcity
of observational benchmarking data, (b) lack of understanding and standards in evaluation metrics, and (c) scale‐
and flood‐magnitude dependency of the evaluation results.

FIM evaluation is typically based on three approaches: (a) point‐scale comparison, either binary (hit/miss) or
water depth, derived from ground surveys (e.g., high water marks) or manual labeling from high‐resolution
imagery (e.g., Aristizabal et al., 2020, 2024; Gutenson et al., 2022; Nevo et al., 2022; Wing et al., 2019,
2021); (b) zonally‐aggregated (e.g., zip code) flood incident reports or damage (e.g., Wing et al., 2021); (c)
spatially‐continuous (aerial) comparison against benchmark FIM (e.g., Aristizabal et al., 2024; Frame
et al., 2024). All three approaches are subject to the aforementioned challenges as well as other approach‐specific

1 of 19

Water Resources Research

10.1029/2024WR039574

limitations. Relatively little research has been reported on FIM evaluation, leading to a considerable knowledge
gap about the proper use and interpretation of evaluation procedures (Stephens et al., 2014). An important study in
this context is by Wing et al. (2021), in which a US‐scale FIM modeling was evaluated against a diverse set of
observations (including high water marks and aggregated damage reports), demonstrating the limitations of the
evaluation approaches used. Another important study was by Stephens et al. (2014), which analytically
demonstrated the sensitivity (and statistical inconsistency) of common binary FIM evaluation metrics, primarily
the Critical Success Index (CSI), to flooding extent, magnitude, topographic slope, and over/underpredictions.

Remote Sensing‐derived FIM (RS‐FIM) is, in principle, an attractive source of benchmarking data for FIM
evaluation. RS‐FIM can provide observations with relatively large spatial coverage and at low data processing
costs (monetary, computational, and algorithmic). As a result, RS‐FIM has been used quite extensively over the
years for FIM model evaluation (e.g., Giezendanner et al., 2023; Konapala et al., 2021; Soria‐Ruiz et al., 2022;
Wing et al., 2021), albeit, almost exclusively, for a small number of case studies (e.g., Hooker et al., 2022; Wing
et al., 2019), that is not for large‐scale model evaluation (Hawker et al., 2020). Some exceptions include Johnson
et al. (2019), Bernhofen et al. (2022), and Hawker et al. (2020). Limitations in RS‐FIM are well known, including
gaps in observational coverage (due to dense vegetation, built environment, and cloud cover (for optical sensors);
Mason et al., 2009; Rasid & Pramanik, 1990; Sanyal & Lu, 2004; Zwenzner & Voigt, 2009; Shastry et al., 2023),
uncertainty in classification algorithms (e.g., Schumann, Bates, et al., 2009; Schumann, Di Baldassarre, &
Bates, 2009), and inclusion of permanent water. These types of biases in RS‐FIM are particularly problematic for
FIM model evaluation as often a not insignificant portion of the flooded domain may be accurately predicted by
the model as flooded while being misclassified by the RS‐FIM. This, as we will show in this paper, will translate
to biased benchmarking and greatly inaccurate model accuracy evaluation.

The limitations in using RS‐FIM as an evaluation benchmark can be mitigated by RS‐FIM enhancement (e.g., gap
filling), selective evaluation procedures (e.g., sampling), or probabilistic/fuzzy approaches (e.g., Horritt, 2006;
Pappenberger et al., 2006). RS‐FIM enhancement can be achieved by the fusion of images from different sensors
(Giezendanner et al., 2023; Konapala et al., 2021; Soria‐Ruiz et al., 2022), coupling of hydraulic simulations
(Grimaldi et al., 2016; Musa et al., 2015; Yan et al., 2015), terrain‐based gap filling (Betterle & Salamon, 2024),
and machine learning (Konapala et al., 2021; Mateo‐Garcia et al., 2021; Nemni et al., 2020; Peng et al., 2019).
These solutions are, however, problematic as they can introduce analyst bias, erode the observational quality of
the RS‐FIM (by introducing modeling and data biases), and can be challenging to apply for large‐scale evaluation
in which many case studies are used.

The use of RS‐FIM as an evaluation benchmark is, by its nature, most suitable for binary (wet/dry) analysis.
While water depth can be calculated based on RS‐FIM (e.g., Bryant et al., 2021; Cohen et al., 2019, 2022; Peter
et al., 2020), these introduce model and data bias and are thus not suitable, nor are they intended, for model
evaluation. Mason et al. (2009) proposed to analyze the distance between the predicted and observed flooding
front and water height. This approach focuses on the potential impact of a flood rather than a model's ability to
“fill” the flooded domain. This is a logical approach but is challenging to implement when using RS‐FIM as a
benchmark, considering its limitations in urban and densely vegetated areas, which likely exacerbate bench-
marking bias issues.

The predominant evaluation procedure for FIM is pixel‐to‐pixel hit‐miss statistics (Schumann, Bates, et al., 2009;
Schumann, Di Baldassarre, & Bates, 2009). A suite of agreement/disagreement metrics is commonly used in the
literature (Stephens et al., 2012). Examples, which we will use in this paper, include the “True Positive Rate
(TPR),” “False Positive Rate,” “False Alarm Rate (FAR),” “Accuracy,” “F1,” and “CSI.” These and similar
metrics calculate a variation of the proportions in true and false positives and negatives between the evaluated and
the benchmark FIM (confusion matrix). The procedure for calculating these values and metrics is quite simple and
will be covered in the Methodology section. Similar to most statistical metrics, it is generally understood, but
often ignored, that the interpretation of an individual or suite of metrics is not straightforward and should not be
taken at face value (Hunter et al., 2005; Pappenberger et al., 2007). For example, “Accuracy” tends to “reward”
overpredictions, and most metrics are sensitive to the overall ratio between wet and dry pixels in the domain (a
function of the layer extent; Stephens et al., 2014). Related to the former, many evaluation procedures do not
distinguish between permanent and flood water, that is include all wet pixels in the analysis. We will show that
this can significantly affect the evaluation results, inflating the model accuracy assessment.

COHEN ET AL.

2 of 19

 19447973, 2025, 8, Downloaded from https://agupubs.onlinelibrary.wiley.com/doi/10.1029/2024WR039574, Wiley Online Library on [14/06/2026]. See the Terms and Conditions (https://onlinelibrary.wiley.com/terms-and-conditions) on Wiley Online Library for rules of use; OA articles are governed by the applicable Creative Commons LicenseWater Resources Research

10.1029/2024WR039574

We have found that only very limited research has been reported on properly using and interpreting FIM eval-
uation metrics (e.g., Landwehr et al., 2023; Pappenberger et al., 2007; Stephens et al., 2014). Perhaps because of
that, many studies report multiple metrics but lack a proper interpretation of their meaning or a standard mean for
inferring the FIM prediction accuracy (Schumann, 2019). We will not fully address this knowledge gap in this
paper but will demonstrate and discuss it.

In this paper, we present a new FIM evaluation strategy that aims to address several key issues stemming from
using RS‐FIM as the evaluation benchmark. The presented analysis focuses on evaluating binary FIM (inundation
extent) using whole‐domain pixel‐to‐pixel hit/miss evaluation metrics. We start by quantifying the errors in
model‐predicted FIM (M‐FIM) evaluation due to biases in RS‐FIM benchmarking. An RS‐FIM enhancement
(gap‐filling) procedure is presented and its effect on FIM evaluation results is analyzed. We then present an
analysis of the impact of including/excluding Permanent Water Bodies (PWB) on FIM evaluation results. A new
evaluation strategy is presented and analyzed, showcasing an improvement in evaluation results. We finish with a
discussion aimed at broadening the scope and nuance of FIM evaluation to better fit the needs of a growing FIM
prediction end‐user base.

2. Methodology

Analyses presented in this study aimed to (a) demonstrate the impact of biases in Remote Sensing derived FIM
(RS‐FIM) benchmark on the evaluation results of model predicted FIM (M‐FIM), (b) quantify the impact of
enhanced (gap‐filled) RS‐FIM benchmark on M‐FIM evaluation results, (c) elucidate the influence of inclusion/
exclusion of PWB on M‐FIM evaluation results, and (d) quantify the improvement in M‐FIM evaluation using a
proposed evaluation strategy. These analyses are based on comparing M‐FIM evaluation results (binary FIM
evaluation metrics) using a very high‐quality RS‐FIM benchmark to evaluation results using lower‐quality
variations of the RS‐FIM (described below). The very high‐quality RS‐FIM is derived from meticulous
manual digitization of high‐resolution aerial imagery. It will be referred to herein as the “Ground Truth” FIM
(GT‐FIM), which is assumed to produce the most accurate/realistic M‐FIM evaluation results.

It is important to emphasize that this study compares the M‐FIM evaluation results using variations of the
benchmark layer and is not intended to assess the quality of a specific model or remote sensing approach. The
important aspect of the results is the relative similarity/differences between the evaluation metrics when using
different benchmark layers. It is also important to reiterate that the analyses presented here focus on binary, pixel‐
to‐pixel evaluation which is, arguably, the most commonly used FIM evaluation approach. We have also opted to
use a handful of evaluation metrics and do not aim to fully assess their utility, nor do we suggest that these are
preferable to other metrics. We did not compare it to a benchmark derived from satellite imagery as the effects of
resolution, extent, and differences in imagery acquisition time are beyond the scope of this paper.

2.1. Case Study and Data

The remote sensing benchmark layer was generated by careful manual digitization of a 3 January 2016, aerial
photography (RGB bands only) by the NOAA Emergency Response Imagery (https://storms.ngs.noaa.gov) from
the “Midwest U.S. Flooding (2015)” Survey. The area of interest is a section of the Arkansas River near Conway
Arkansas (Figure 1). The mosaiced image is at a resolution of 0.4 m and covers an area of ∼85 km2, of which
∼44 km2 is classified as water (flood + permanent; Wet to Dry Ratio (WDR) of 0.52; Figure 1). The very high
resolution of the image allowed us to visually inspect flooding below dense vegetation cover and interpret
flooding conditions of buildings (a building surrounded or partly surrounded by floodwater was classified as
flooded). This resulted in a high degree of confidence in the quality of the benchmark FIM. This layer will be
referred to as the ground‐truth FIM (GT‐FIM).

Three lower‐quality benchmark layers (at the same spatial resolution) are generated for the analyses (Figure 1):

1. TRS‐FIM—a traditional remote‐sensing product compiled with a “quick and simple” supervised classification

tool in ArcGIS Pro based on the high‐resolution mosaic of the aerial imagery;

2. DG1‐FIM—a moderately degraded version of GT‐FIM;
3. DG2‐FIM—a more severely degraded version of GT‐FIM.

DG1‐FIM and DG2‐FIM were generated by re‐classifying flooded pixels within randomly generated “holes”
(randomly sized buffers around randomly located points) in the GT‐FIM as non‐flooded. This is intended to

COHEN ET AL.

3 of 19

 19447973, 2025, 8, Downloaded from https://agupubs.onlinelibrary.wiley.com/doi/10.1029/2024WR039574, Wiley Online Library on [14/06/2026]. See the Terms and Conditions (https://onlinelibrary.wiley.com/terms-and-conditions) on Wiley Online Library for rules of use; OA articles are governed by the applicable Creative Commons LicenseWater Resources Research

10.1029/2024WR039574

Figure 1. Maps of the case study (a) area and extent, (b) mosaic of aerial photos from 3 January 2016, (c) GT‐FIM, (d) TRS‐FIM, (e) DG1‐FIM, and (f) DG2‐FIM. WDR
(Wet to Dry Ratio) is the ratio between the number of wet grid cells (value of 2) and dry grid cells (value of 0).

COHEN ET AL.

4 of 19

 19447973, 2025, 8, Downloaded from https://agupubs.onlinelibrary.wiley.com/doi/10.1029/2024WR039574, Wiley Online Library on [14/06/2026]. See the Terms and Conditions (https://onlinelibrary.wiley.com/terms-and-conditions) on Wiley Online Library for rules of use; OA articles are governed by the applicable Creative Commons LicenseWater Resources Research

10.1029/2024WR039574

Figure 2. Maps showing the overlay between the GT‐FIM and the M‐FIM (HEC‐RAS) for (a) December 26, and (b) December 27. Dark purple shows agreement (TP),
red is overprediction (FP), and blue is underprediction (FN). Wet grid cells have a value of 2 in the benchmark and M‐FIM layers; dry grid cells have a value of 0 and 1 in
the benchmark M‐FIM layers, respectively.

mimic obstructions in remote sensing classification by clouds, vegetation, etc. This means that the degradation
only emits flooded grid cells (i.e., generates false negatives) but does not mimic false water classification (false
positives). The TRS‐FIM, on the other hand, includes both false positives and negatives. The only difference
between DG1‐FIM and DG2‐FIM is the maximum size of the buffers, 250 and 400 m for DG1‐FIM and DG2‐
FIM, respectively (Figures 1e and 1f).

The Digital Elevation Model (DEM) used in this study is the USGS 3DEP 10 m product. All the FIM layers were
rescaled and spatially co‐registered with the DEM. While higher‐resolution DEMs are available for this study
location, the 10 m product is used as it was also used as input to the hydraulic (HEC‐RAS) simulations and to
more directly link this study to operational FIM predictions by the NOAA Office of Water Prediction.

The M‐FIM used in this study is from HEC‐RAS 2D simulation over the study area for December 26 and 27, 2015
(Figure 2). The HEC‐RAS 2D Model is set up with the 10 m 3DEP DEM, ESRI Landuse‐Landcover and NWM
retrospective streamflow. The discharge hydrograph is assigned at the upstream boundary condition, and at the

COHEN ET AL.

5 of 19

 19447973, 2025, 8, Downloaded from https://agupubs.onlinelibrary.wiley.com/doi/10.1029/2024WR039574, Wiley Online Library on [14/06/2026]. See the Terms and Conditions (https://onlinelibrary.wiley.com/terms-and-conditions) on Wiley Online Library for rules of use; OA articles are governed by the applicable Creative Commons LicenseWater Resources Research

10.1029/2024WR039574

downstream boundary, we used the normal depth. The Manning's roughness
value is assigned to the model based on the LULC information. The model is
run with the full momentum equation and only predicts fluvial flooding. The
simulation results used were selected from a long simulation output to
represent a strong model prediction (December 27) and an underestimation
(December 26). The dates do not match the aerial image acquisition date (3
January 2016) due to biases in the NWM input hydrograph. This has no
implication for the analysis presented in this paper, as it is focused on dif-
ferences in evaluation results.

The ESRI USA Detailed Water Bodies data set (https://hub.arcgis.com/
datasets/esri::usa‐detailed‐water‐bodies/about) is used in this study to deter-
mine PWB. Figure 3 shows the GT‐FIM with PWB removed (changed to No
Data). The Microsoft Building Footprint data set (https://services.arcgis.com/
P3ePLMYs2RVChkJx/arcgis/rest/services/MSBFP2/FeatureServer) is used
to demonstrate impact‐based analysis in the Section 4.

2.2. Experimental Design

We execute a multifaceted analysis that aims to:

A1. Quantify the effect of biases in a benchmark data set on FIM

evaluation results;

A2. Quantify the effect of RS‐FIM enhancement on FIM evaluation

results;

A3. Quantify the impact of including/excluding PWB on FIM evaluation

results;

A4. Test the robustness of the proposed FIM evaluation framework.

The M‐FIM accuracy is evaluated against the different benchmark layers
using the selected evaluation metrics (detailed in Section 2.3 below) for two
M‐FIMs (December 26 and December 27; Figure 2). Results from the eval-
uation against the GT‐FIM are considered as the “true” evaluation results
(model accuracy) and the analyses are based on comparing the evaluation
results when using the other (lower‐quality/degraded) benchmark layers.

For A1, evaluation results using the TRS‐FIM, DG1‐FIM, and DG2‐FIM
benchmarks are compared. It is expected that the evaluation results will
more significantly differ from the GT‐FIM with increasing degradation of the
benchmark. This will quantify and demonstrate, quite intuitively, that biases
in the benchmark layer will lead to errors in the evaluation results.

Figure 3. GT‐FIM with Permanent Water Bodies removed (white).
WTR = 0.35.

For A2, the effect of the FIM enhancement procedure (Section 2.4) of M‐FIM evaluation is analyzed by repeating
A1 with the enhanced benchmark layers.

For A3, the A2 experiment will be repeated but with PWB removed (classified as No Data) in all benchmark
layers, including the GT‐FIM. The analysis is expected to demonstrate, again quite intuitively, that the inclusion
of PWB can significantly affect the evaluation results.

For A4, the full evaluation strategy (Section 2.5) is evaluated by comparing the benchmark layer produced against
the results from A3. Successful results will show that the new evaluation strategy more closely resembles the
evaluation when using GT‐FIM even though the initial benchmark layer is degraded.

2.3. Evaluation Metrics and Procedure

The five evaluation metrics used in this study are commonly used in the literature but often referred to by different
names. Discussion about the lack of standards in FIM evaluation and the importance of metric selection and
proper interpretation is offered later. The five metrics used are the CSI, TPR, FAR, F1, and Accuracy (ACC).

COHEN ET AL.

6 of 19

 19447973, 2025, 8, Downloaded from https://agupubs.onlinelibrary.wiley.com/doi/10.1029/2024WR039574, Wiley Online Library on [14/06/2026]. See the Terms and Conditions (https://onlinelibrary.wiley.com/terms-and-conditions) on Wiley Online Library for rules of use; OA articles are governed by the applicable Creative Commons LicenseWater Resources Research

10.1029/2024WR039574

CSI = TP/(TP + FP + FN)

TPR = TP/(TP + FN)

FAR = FP/(TP + FP)

F1 = (2TP)/(2TP + FP + FN)

ACC = (TP + TN)/(TP + FP + TN + FN)

(1a)

(1b)

(1c)

(1d)

(1e)

Figure 4. Illustration of the calculation of the confusion matrix layer.

where TP, TN, FP, and FN are the number of pixels in the confusion matrix
layer that are classified as True Positives (agreement; flooded in both M‐FIM
and benchmark), True Negatives (agreement; not flooded in both M‐FIM and
benchmark), False Positive (disagreement; flooded in M‐FIM while not
flooded in benchmark; overprediction by the model), and False Negative (disagreement; not flooded in M‐FIM
while flooded in benchmark; underprediction by the model), respectively. To our knowledge, there are no
commonly accepted model performance classifications (e.g., strong, satisfactory, weak) for these metrics' values.

Calculation of the confusion matrix layer and evaluation metrics is scripted in an ArcGIS Pro Notebook (see Data
and Software Availability statement for link). The procedure is as follows:

1. The model‐predicted (M‐FIM) layer is reclassified with values of 1 and 2 for not‐flooded and flooded grid

cells, respectively.

2. The benchmark layer is reclassified with values of 0 and 2 for not‐flooded and flooded grid cells, respectively.
3. Using Map Algebra, the confusion matrix layer is calculated by adding (plus) the grid cell values of the two re‐
classified layers. The resulting raster values are 1, 2, 3, and 4 which represent True Negative (TN), False
Positive (FP), False Negative (FN), and False Positive (FP) respectively (Figure 4).

4. The number of pixels from each class in the confusion matrix layers is used to calculate the evaluation metrics

(Equation 1).

2.4. RS‐FIM Enhancement

A core element of the new evaluation strategy, as described in Section 2.5 below, is the reduction of bias and
uncertainty in the benchmark layer. As discussed earlier, remote sensing‐derived FIM (RS‐FIM) is susceptible to
multiple sources of bias and mismatch with the evaluated FIM (resolution, alignment, and extent). An RS‐FIM
enhancement procedure is developed which includes the following processes. The framework is scripted as an
ArcGIS Pro Notebook (see Data and Software Availability statement for link):

1. Gap Filling (Figures 5a–5c)—mitigate biases in RS‐FIM due to for example vegetation, clouds, and built
environment, by estimating flood extent between observed flooding locations. In this paper, we use a hy-
drologically guided region‐growing (HGRG) algorithm to enhance the RS‐FIM by integrating DEMs, as
described in detail below.

2. Removal of PWB—aim to ensure that the evaluation only involves the ability of the model to predict
floodwater extent. A PWB layer is used to mask all grid cells from the benchmark and Model‐predicted FIM
(M‐FIM) layers overlaying a permanent water body. These are excluded from the analysis by being classified
as NoData.

3. Matching the extent, resolution, and pixel alignment of the benchmark and M‐FIM—is important for matching
pixel alignment between the layers prior to the calculation of the confusion matrix layer. The target layer for
alignment can be either the M‐FIM, the benchmark layer (i.e., matching the M‐FIM to the benchmark or vice
versa), or, as in this paper, the DEM used in the gap filling procedure.

The HGRG algorithm (Tian et al., 2024) involves five primary steps (the framework is scripted as a QGIS Plugin
(see Data and Software Availability statement for link)):

1. Create seed objects: flood pixels in the RS‐FIM are grouped into discrete seed objects by a recursive,
connected‐component algorithm (Liu et al., 2010; Liu & Jezek, 2004; Sonka et al., 1999). Then, small flood
objects are removed because they are likely to be noise in the classification, as the HGRG algorithm is

COHEN ET AL.

7 of 19

 19447973, 2025, 8, Downloaded from https://agupubs.onlinelibrary.wiley.com/doi/10.1029/2024WR039574, Wiley Online Library on [14/06/2026]. See the Terms and Conditions (https://onlinelibrary.wiley.com/terms-and-conditions) on Wiley Online Library for rules of use; OA articles are governed by the applicable Creative Commons LicenseWater Resources Research

10.1029/2024WR039574

Figure 5. Maps of Gap Filled (a) TRS‐FIM, (b) DG1‐FIM, and (c) DG2‐FIM; Final benchmark (including the removal of permanent water bodies) for (d) TRS‐FIM,
(e) DG1‐FIM, and (f) DG2‐FIM.

COHEN ET AL.

8 of 19

 19447973, 2025, 8, Downloaded from https://agupubs.onlinelibrary.wiley.com/doi/10.1029/2024WR039574, Wiley Online Library on [14/06/2026]. See the Terms and Conditions (https://onlinelibrary.wiley.com/terms-and-conditions) on Wiley Online Library for rules of use; OA articles are governed by the applicable Creative Commons LicenseWater Resources Research

10.1029/2024WR039574

sensitive to false positive in the original RS‐FIM. In this case, only seeds with no less than 500 pixels are kept
for subsequent expansion.

2. Extract boundary and centroid points for each identified seed object.
3. Calculate local water surface elevation (LWSE): for each seed object, elevation values are extracted for all

boundary pixels, and a LWSE is computed through histogram analysis of these boundary elevations.

4. Following outlier removal, the LWSE values are interpolated across the entire study area.
5. Flood extent propagation: a seeded region‐growing algorithm is applied to expand each seed object to include

all adjacent pixels whose ground surface elevation is lower than the interpolated LWSE.

The HGRG algorithm is sensitive to the resolution and quality of the DEM and the alignment between the RS‐
FIM and the DEM. Since it is solely based on topographic gradient, misclassification of wet pixels or small PWB
in the RS‐FIM, especially with high elevation, can lead to considerable erroneous “spreading” of floodwater (see
Figure 5d). Common examples include small ponds, reservoirs, and irrigated farmland on elevated grounds. The
process of removing small flood clusters and PWB can mitigate this issue. Misalignment between the RS‐FIM
and DEM and misrepresentation of small topographic features in the DEM (e.g., levees) can also lead to erro-
neous spreading.

2.5. New Evaluation Strategy

The concept underpinning the new evaluation strategy presented herein is quite simple: the exclusion of PWB and
low‐certainty grid cells. The latter refers to pixels that were identified as flooded by the gap‐filling procedure but
were not observed as flooded in the original RS‐FIM. Exclusion of the PWB and low‐certainty grid cells is done
by classifying both as NoData in the final benchmark layer (Figures 5d–5f). This step is included in the
benchmark enhancement script. Another way to frame the strategy is to say that locations that were observed (by
remote sensing) as flooded are considered as floodwater with high confidence while locations that were not
observed as flooded and were not estimated as flooded by the gap‐filling algorithm are considered as dry with
high confidence.

The proposed RS‐FIM enhancement and new evaluation strategy do not explicitly address the issue of over-
prediction of flooding in remote sensing analysis. This issue is quite prominent in SAR‐derived FIM, in which an
empirically determined threshold is often used to segment the flooded regions. As stated earlier, the removal of
small flood patches can mitigate this type of bias but, ultimately, there is no substitution for RS‐FIM quality
control. We will discuss the strategy's limitations and potential improvements later.

3. Results

3.1. Impact of Benchmark Biases on Evaluation Outcomes

The evaluation results substantially differ between the two model predictions (M‐FIMs) (Figure 2) when using the
Ground Truth benchmark (GT‐FIM), with an overall reduction of 25% in evaluation metrics values for December
26 (see the lower section of Table 1). Note that a FAR increase indicates lower accuracy. Also note that the
absolute value for all the calculated percent changes is reported. The differences in evaluation results between the
two M‐FIM when using the lower‐quality benchmark layers (Traditional Remote Sensing (TRS‐FIM), low
degraded (DG1‐FIM), and highly degraded (DG2‐FIM)) were, on average, lower than the GT‐FIM evaluation
results (12%, 15%, and 14% for DG2‐FIM, DG1‐FIM, and TRS‐FIM, respectively). This demonstrates that the
use of biased benchmarks can considerably degrade the ability to quantify the true differences between the
predictive quality of M‐FIMs.

The accuracy of the evaluation results degraded considerably when using lower‐quality benchmarks (Table 1 and
Figure 6), leading to lower confidence in the model accuracy estimation. As expected, DG2‐FIM, with the
greatest degree of degradation, yielded the most significant difference from the GT‐FIM evaluation results (e.g.,
reduction of 34% and 22% in CSI and F1 metrics, respectively for the December 27 simulation; averaging 76%
difference from GT‐FIM results for all metrics). TRS‐FIM yielded greater evaluation differences from GT‐FIM
compared to DG1‐FIM (e.g., reduction of 12% in CSI for DG1‐FIM and 26% TRS‐FIM for the December 27
simulation; with averages of 32% and 53% difference from GT‐FIM for all metrics, respectively). The higher bias
when using TRS‐FIM compared to DG1‐FIM is somewhat unexpected, considering its conceptual similarity to
the GT‐FIM. However, qualitative examination of the two benchmarks (Figures 1d and 1e) quite clearly explains

COHEN ET AL.

9 of 19

 19447973, 2025, 8, Downloaded from https://agupubs.onlinelibrary.wiley.com/doi/10.1029/2024WR039574, Wiley Online Library on [14/06/2026]. See the Terms and Conditions (https://onlinelibrary.wiley.com/terms-and-conditions) on Wiley Online Library for rules of use; OA articles are governed by the applicable Creative Commons LicenseWater Resources Research

10.1029/2024WR039574

Table 1
Evaluation Metrics for the December 26 and December 27 Simulations Using the Original (Pre‐Enhancement) Benchmark
Layers

GT‐FIM

DG2‐FIM

DG1‐FIM

TRS‐FIM

STDV (of %)

0.47 (31%)

0.69 (3%)

0.60 (12%)

0.71 (0%)

0.50 (26%)

0.61 (14%)

0.40 (535%)

0.21 (222%)

0.26 (314%)

December 26

CSI

TPR

FAR

F1

ACC

December 27

CSI

TPR

FAR

F1

ACC

0.68

0.71

0.06

0.81

0.88

0.82

0.91

0.10

0.90

0.93

0.64 (21%)

0.83 (7%)

0.54 (34%)

0.89 (3%)

0.42 (313%)

0.70 (22%)

0.83 (11%)

% Difference Between December 26 and 27

CSI

TPR

FAR

F1

ACC

Average

21%

28%

60%

12%

5%

25%

16%

30%

4%

10%

1%

12%

0.75 (7%)

0.86 (3%)

0.71 (14%)

0.90 (0.1%)

0.24 (133%)

0.83 (8%)

0.89 (4%)

18%

28%

15%

11%

3%

15%

0.67 (18%)

0.81 (9%)

0.58 (29%)

0.77 (15%)

0.30 (192%)

0.74 (18%)

0.83 (11%)

17%

27%

13%

11%

2%

14%

0.100

0.074

1.609

0.071

0.031

0.104

0.080

0.917

0.072

0.038

0.024

0.012

0.251

0.006

0.020

0.059

Note. The absolute percent difference in metric value compared to the GT‐FIM is in parentheses. Standard deviation is
calculated based on the percent difference for each metric. The percent difference between December 26 and 27 is calculated
for each metric's value (not the %).

these results, highlighting the biases in evaluation that can stem from using a simple Remote Sensing (RS‐FIM)
analysis product as a benchmark.

A large degree of variability exists between the five metrics used in this study across the evaluation settings. CSI
and F1 show the greatest sensitivity to the differences between the benchmarks. TPR and ACC are the least
sensitive to benchmark quality. FAR yielded the highest variability among the benchmarks but this can be
explained by the introduced gaps in the degraded benchmarks (leading to more FP by the model). All the metrics,
except FAR, resulted in low differences in the evaluation results between the two M‐FIMs (December 26 and
December 27). When using the GT‐FIM, the average difference between the M‐FIM evaluation results when
considering all the metrics was 25%, mostly influenced by FAR (60% difference). This is low considering the
difference in Wet to Dry pixel Ratio (WDR) between the two M‐FIMs is a factor of 2 (WDR of 0.47 and 1.04 for
December 26 and December 27, respectively; Figure 2). TPR and CSI were the most sensitive (28% and 21%
respectively), while F1 and ACC were the least sensitive (12% and 5% respectively). The differences between the
evaluation results for the two M‐FIMs are even smaller, and similar in magnitude, when using the degraded
benchmarks (12%, 15%, and 14% for DG2‐FIM, DG1‐FIM, and TRS‐FIM, respectively). This further showcases
the biases in model evaluation analysis when using low‐quality benchmarks.

3.2. Impact of Benchmark Enhancement on Evaluation Results

The enhancement of the RS‐FIMs (removal of small clusters and gap filling) considerably altered the three
benchmarks (Figures 5a–5c). Gap‐filled DG1‐FIM and DG2‐FIM are similar to each other (WDR of 0.75 and
0.76) and to GT‐FIM (Figure 1c). This is expected as the two degraded benchmarks were derived by generating
“holes” in the GT‐FIM layer. For the Traditional Remote Sensing benchmark (TRS‐FIM), the HGRG algorithm
did, however, erroneously extend the flooding, increasing its wet‐to‐dry pixel ration (WDR) from 0.45

COHEN ET AL.

10 of 19

 19447973, 2025, 8, Downloaded from https://agupubs.onlinelibrary.wiley.com/doi/10.1029/2024WR039574, Wiley Online Library on [14/06/2026]. See the Terms and Conditions (https://onlinelibrary.wiley.com/terms-and-conditions) on Wiley Online Library for rules of use; OA articles are governed by the applicable Creative Commons LicenseWater Resources Research

10.1029/2024WR039574

Figure 6. Evaluation metrics for (a) December 26 and (b) December 27 simulations using four original (pre‐enhancement)
benchmark layers. Labels at the top of the bars are the percent difference in metric values between each degraded benchmark
and the GT‐FIM.

(Figure 1d) to 1.27 (Figure 5a; GT‐FIM WDR is 0.52). The impact of the enhancement on the evaluation results is
mixed. For DG2‐FIM, CSI and F1 show improvement in the evaluation accuracy (lower % difference from the
results of GT‐FIM; Table 2) and a total average (excluding FAR) reduction (improved evaluation accuracy) of
14%pt. and 18%pt. for December 26 and December 27, respectively. For DG1‐FIM, evaluation accuracy was
similarly improved for both December 26 and December 27 but not to the same degree as for DG2‐FIM (average
(excluding FAR) decrease (smaller difference with GT‐FIM) of 4%pt. and 9%pt., respectively, in evaluation
metrics). TRS‐FIM was negatively impacted by the enhancement with an average (excluding FAR) increase
(greater difference with GT‐FIM) of 14 and 11%pt, for December 26 and December 27, respectively.

The negative impact of the RS‐FIM enhancement procedure on TRS‐FIM can be clearly understood from
Figure 5a (compared to Figure 1d), with considerable erroneous expansion of the flood at the south‐eastern corner
of the domain. These issues in RS‐FIM enhancement could potentially be mitigated by using higher‐quality
DEMs or a more robust remote sensing analysis. We will explore these in Section 3.4.

The results of the analysis above demonstrate that the RS‐FIM enhancement used in this study will not necessarily
improve the quality of the M‐FIM evaluation. More severely biased RS‐FIM are more likely to result in worse
benchmarks, emphasizing the importance of the quality of the initial RS‐FIM.

3.3. Impact of Permanent Water Bodies (PWB) on Evaluation Outcomes

Exclusion/masking of PWB from the evaluation analysis resulted in a considerable decrease in the M‐FIM ac-
curacy assessment. Evaluation using PWB‐removed Ground‐Truth benchmark (GT‐FIM; Figure 3) yielded an
average of 18% and 5% reduction in metric values (excluding FAR) for December 26 and 27, respectively

COHEN ET AL.

11 of 19

 19447973, 2025, 8, Downloaded from https://agupubs.onlinelibrary.wiley.com/doi/10.1029/2024WR039574, Wiley Online Library on [14/06/2026]. See the Terms and Conditions (https://onlinelibrary.wiley.com/terms-and-conditions) on Wiley Online Library for rules of use; OA articles are governed by the applicable Creative Commons LicenseWater Resources Research

10.1029/2024WR039574

Table 2
Difference in Metrics Between the Evaluation Analysis Using the Original
Benchmarks (Table 1) and the Gap Filled Benchmarks for the December 26
and December 27 Simulations

DG1‐FIM

DG2‐FIM

TRS‐FIM

December 26

CSI

TPR

FAR

F1

ACC

0.08 (− 12%pt.)

0.2 (− 30%pt.)

− 0.07 (10%pt.)

− 0.03 (4%pt.)

− 0.01 (2%pt.)

− 0.17 (24%pt.)

− 0.2 (− 129%pt.)

− 0.40 (− 448%pt.)

− 0.22 (− 286%pt.)

0.06 (− 7%pt.)

0.02 (− 2%pt.)

0.17 (− 20%pt.)

− 0.06 (8%pt.)

0.05 (− 6%pt.)

− 0.14 (15%pt.)

December 27

CSI

TPR

FAR

F1

ACC

0.17 (− 21%pt.)

0.31 (− 38%pt.)

− 0.05 (6%pt.)

− 0.01 (2%pt.)

− 0.01 (1%pt.)

− 0.21 (23%pt.)

− 0.22 (− 52%pt.)

− 0.39 (− 242%pt.)

− 0.21 (− 174%pt.)

0.11 (− 12%pt.)

0.22 (− 24%pt.)

− 0.04 (4%pt.)

0.06 (− 7%pt.)

0.11 (− 12%pt.)

− 0.1 (11%pt.)

Note. A positive value indicates an increase in metric value for the Gap Filled
benchmark. The value in the parenthesis is the difference (in percent points
(%pt.)) between the two analyses of the percent difference between the
degraded benchmarks and the GT‐FIM benchmark metrics' values (e.g., top
left value: difference in CSI for DG2‐FIM was 31% in Table 1 and 13% using
the Gap Filled DG2‐FIM, leading to − 18%pt. difference). Negative %pt.
indicate closer match (i.e., less difference) between the evaluation results
using degraded benchmark and GT‐FIM.

Table 3
Difference in Metric Values Between the Evaluation Analysis Using the
Enhanced Benchmarks (Table 2) and the Permanent Water Bodies Removed
Benchmarks for the December 26 and December 27 Simulations

GT‐FIM

DG1‐FIM

DG2‐FIM

TRS‐FIM

December 26

CSI

TPR

FAR

F1

− 0.15 (− 28%)

− 0.14 (− 26%)

− 0.14 (− 27%)

− 0.14 (− 47%)

− 0.14 (− 26%)

− 0.14 (− 26%)

− 0.14 (− 26%)

− 0.14 (− 46%)

0.05 (42%)

0.0 (45%)

0.01 (45%)

0.04 (44%)

− 0.12 (− 17%)

− 0.11 (− 15%)

− 0.11 (− 16%)

− 0.15 (− 33%)

ACC − 0.01 (− 2%)

− 0.02 (− 2%)

− 0.02 (− 2%)

− 0.04 (− 6%)

December 27

CSI

TPR

FAR

F1

− 0.08 (− 10%)

− 0.05 (− 6%)

− 0.06 (− 8%)

− 0.11 (− 25%)

− 0.05 (− 5%)

− 0.05 (− 6%)

− 0.05 (− 6%)

− 0.11 (− 23%)

0.05 (32%)

0.01 (34%)

0.02 (34%)

0.04 (33%)

− 0.05 (− 6%)

− 0.03 (− 3%)

− 0.04 (− 4%)

− 0.1 (− 16%)

ACC − 0.01 (− 1%)

− 0.01 (− 1%)

− 0.01 (− 1%)

− 0.03 (− 4%)

Note. A negative value indicates a decrease in metric value for the
PWB‐removed benchmark. The value in the parenthesis is the percent dif-
ference between the two analyses.

(Table 3). CSI was lowered by 0.15 (28%) and 0.08 (10%) and F1 was lowered
by 0.12 (17%) and 0.05 (6%) for December 26 and 27, respectively.

For the degraded benchmarks, the effect of PWB is quite diverse. Average
reduction in the metrics scores (excluding FAR) for December 27 was 5%,
4%, and 17%, for DG2‐FIM, DG1‐FIM, and TRS‐FIM, respectively. For
December 26, the differences were greater, with an average metric score
reduction (excluding FAR) of 18%, 17%, and 33% of %, for DG2‐FIM, DG1‐
FIM, and TRS‐FIM, respectively. The results demonstrate that the inclusion
of PWB, which is commonly done, can considerably inflate M‐FIM accuracy
assessment, and that this issue seems to be graver for lower‐performing model
predictions (December 26 in this study) and lower quality benchmarks (33%
for December 26 when using TRS‐FIM as benchmark). ACC showed limited
sensitivity to PWB.

3.4. Implementation of the Evaluation Strategy

The proposed evaluation strategy yielded mixed results (Table 3 and
Figure 7). Evaluation results using the synthetically degraded benchmarks
(DG1‐FIM and DG2‐FIM; Figures 5e and 5f) are very closely aligned,
excluding the very low FAR, with the evaluation results using GT‐FIM, with
an average difference of just 3% for December 26%, and 5% and 4% (DG1‐
FIM and DG2‐FIM, respectively) for December 27. This can be explained by
the ability of the gap filling approach to yield benchmarks that closely
resemble the original (pre‐degradation) benchmark (GT‐FIM; Figures 1c and
5b, 5c). Removal of the gap‐filled pixels in the evaluation procedure
(Figure 5) did not significantly affect the close alignment in the evaluation
results between using GT‐FIM and, DG1‐FIM and DG2‐FIM. This is a
positive outcome as it demonstrates that a robust RS‐FIM enhancement is not
undermined by the proposed evaluation strategy.

For the Traditional Remote Sensing (TRS‐FIM; Figure 5d) benchmark, biases
in the evaluation results remained high but were considerably improved.
Evaluation results for December 26 (Table 4 and Figure 7) show a consid-
erable reduction in bias (from an average of 38%–22%) when using the
evaluation strategy. The evaluation results for December 27 show an even
greater improvement (from an average of 36%–18%). Differences (biases) in
CSI and F1 values when using the TRS‐FIM compared to the GT‐FIM
benchmarks were reduced by about half for the December 27 evaluation.
The improvement in the evaluation results demonstrates the value of the
proposed evaluation strategy. The remaining bias in the evaluation results
when using the TRS‐FIM as benchmarks showcases limitations in the eval-
uation strategy when using low‐quality RS‐FIM for which the enhancement
procedure is unable to yield considerable improvement in its quality.

3.5. Evaluation Metrics Sensitivity

The five evaluation metrics used in this study showed considerable variability
in their sensitivity to the benchmark quality and the evaluation strategy
(Table 5). FAR is highly sensitive to differences in benchmark data,
consistently having the largest difference between the evaluation results using
GT‐FIM and the degraded benchmarks (Tables 1–6). While FAR may pro-
vide important insight into specific M‐FIM accuracy applications, it does not
seem to be a particularly useful metric for a more general evaluation analysis.

ACC is the least sensitive metric to both benchmark quality and M‐FIM
accuracy (December 26 vs. December 27; Table 1). Considering the large

COHEN ET AL.

12 of 19

 19447973, 2025, 8, Downloaded from https://agupubs.onlinelibrary.wiley.com/doi/10.1029/2024WR039574, Wiley Online Library on [14/06/2026]. See the Terms and Conditions (https://onlinelibrary.wiley.com/terms-and-conditions) on Wiley Online Library for rules of use; OA articles are governed by the applicable Creative Commons LicenseWater Resources Research

10.1029/2024WR039574

Figure 7. Summary of Critical Success Index and F1 scores for the December 27 and December 26 model predictions using the four benchmarks (GT‐FIM, DG2‐FIM,
DG1‐FIM, and TRS‐FIM) and four phases of the benchmark modifications (Original, enhancement, PWR removal, and the final evaluation strategy).

differences between the benchmarks and the simulations, this suggests that ACC is not a good metric to use for the
type of evaluation analysis explored in this study. TPR also showed low sensitivity to benchmark quality
(Tables 1–6) but was sensitive to M‐FIM accuracy. The relative consistency in TPR between benchmarks used
(Table 5) is quite intriguing and merits further investigation.

Table 4
Evaluation Metrics for the December 26 and December 27 Simulations
Using the Final (Evaluation Strategy) Benchmark Layers

CSI and F1 had relatively similar sensitivity (to both benchmark quality and
simulation accuracy) and, overall, seem to be the most robust metrics for the
type of evaluation analysis explored in this study.

GT‐FIM DG1‐FIM DG2‐FIM

TRS‐FIM STDV (of %)

4. Discussion

December 26

CSI

TPR

FAR

F1

ACC

0.53

0.56

0.11

0.69

0.87

0.56 (6%)

0.54 (2%)

0.37 (29%)

0.56 (0%)

0.54 (4%)

0.40 (30%)

0.01 (91%)

0.03 (77%)

0.13 (− 17%)

0.72 (4%)

0.7 (1%)

0.55 (21%)

0.89 (3%)

0.91 (4%)

0.79 (9%)

December 27

CSI

TPR

FAR

F1

ACC

0.75

0.86

0.15

0.85

0.92

0.83 (11%)

0.79 (6%)

0.57 (23%)

0.86 (0%)

0.84 (2%)

0.65 (24%)

0.04 (74%)

0.08 (50%)

0.18 (− 18%)

0.91 (6%)

0.88 (3%)

0.73 (15%)

0.96 (4%)

0.95 (3%)

0.84 (9%)

0.147

0.161

0.586

0.109

0.034

0.091

0.134

0.475

0.061

0.030

Note. The absolute percent difference in metric value compared to the
GT‐FIM is in parentheses. Standard deviation is calculated based on the
percent difference for each metric.

The results of this study demonstrated the importance of benchmark quality
for the robust evaluation of Flood Inundation Maps (FIMs). Lower quality
benchmark FIM yielded considerably different evaluation results compared
to a high‐confidence benchmark. This is an intuitive and expected outcome.
However, this study highlights the magnitude and variability in evaluation
bias across different
levels of benchmark quality and predicted FIM
(December 26 and 27 M‐FIMs). We hope that these outcomes will foster
more awareness and research into this critical element of flood inundation
mapping (some of which will be highlighted below).

This study focused on benchmarking issues most related to remote sensing‐
derived FIM (RS‐FIM). Our working assumption was that RS‐FIM could
be used as a robust benchmarking source. This commonplace assumption and
aspiration is driven by the attractiveness of RS‐FIM for model evaluation
(outlined in the introduction). The results of this study showcase that a typical
RS‐FIM is likely to incur considerable biases in the evaluation results, mostly
yielding lower model accuracy assessment (e.g., Table 1). This is because

COHEN ET AL.

13 of 19

 19447973, 2025, 8, Downloaded from https://agupubs.onlinelibrary.wiley.com/doi/10.1029/2024WR039574, Wiley Online Library on [14/06/2026]. See the Terms and Conditions (https://onlinelibrary.wiley.com/terms-and-conditions) on Wiley Online Library for rules of use; OA articles are governed by the applicable Creative Commons LicenseWater Resources Research

10.1029/2024WR039574

Table 5
Average Percent Point (%pt.) Change for Each Evaluation Metric Between
the Percent Difference (From Using GT‐FIM as a Benchmark and the
Degraded Benchmarks) When Using the Original and Final (Proposed
Evaluation Strategy) Benchmarks

December 26

December 27

CSI

TPR

FAR

F1

ACC

− 11%pt.

5%pt.

− 296%pt.

− 7%pt.

− 1%pt.

− 12%pt.

3%pt.

− 177%pt.

− 8%pt.

− 4%pt.

Note. A negative value indicates an average improvement in the evaluation
results (i.e., lower bias).

erroneous gaps in the RS‐FIM due to, for example, vegetation cover can
“penalize” the model. The opposite evaluation bias can also occur, though not
explicitly evaluated here, in which the evaluation results may be inflated for
overpredicting models.

The use of RS‐FIM enhancement methodologies (e.g., Betterle & Sala-
mon, 2024; Tian et al., 2024) can reduce flood detection biases, thus poten-
tially improving the robustness of M‐FIM evaluation. The enhancement
procedure proposed and used in this paper yielded mixed results in terms of
improving the evaluation outcomes. There are two shortcomings in using
enhanced RS‐FIM as an evaluation benchmark: the introduction of (a) new
biases (especially overprediction of flooding extent) and (b) conceptual
degradation of the observational quality of the benchmark. The first point was
clearly the case in this study, where small errors in flood detonations were
exaggerated (expanded) into large overpredictions in the enhanced RS‐FIM.
More robust enhancement algorithms, particularly those dealing with false
(over) flood detection, could potentially mitigate much of this issue. This
needs further exploration.

The second shortcoming (erosion in observational quality) is open for debate. On one hand, RS‐FIM enhancement
can yield a more realistic (true) representation of the flooding extent, but, on the other hand, it can introduce
similar errors as the model it is meant to evaluate. For example, levees and other flood protections are often not
reflected in the DEM used for the model simulations, resulting in false positives. While the remote sensing
analysis is very likely to detect this model bias, its enhancement, using a similar DEM, is likely to mimic the
simulation error. Our proposed approach to mitigate the issue is to remove the enhancement‐predicted “new”
flooding from the analysis, thus only keeping high‐confidence wet and dry grid cells in the (Final) benchmark.
This resulted in a graphically unappealing FIM (Figures 4d–4f) but one that can yield more robust evaluation
results.

The exclusion of PWB from the evaluation is, in our opinion, a clear‐cut case considering that the typical purpose
of M‐FIM is to predict flooding. The importance of this step will vary considerably as a function of the proportion
of the PWB in the evaluated M‐FIM. For large rivers (relative to the evaluated domain), small flooding
magnitude, and lakes, water extent can be predominantly PWB. In these cases, the assessed accuracy of the
evaluated M‐FIM will be considerably inflated if PWB are included. In relatively smaller rivers and large flood
magnitudes, the effect of PWB on the evaluation result may be negligible. In this study, the proportion of PWB
(primarily the Arkansas River) was 17% of the entire domain (GT‐FIM WDR reduced from 0.52 to 0.35 after
PWB masking (Figures 1c and 3)) and its exclusion from the evaluation resulted in a considerable reduction in the
M‐FIM accuracy assessment when using the GT‐FIM benchmark (Table 3).
The reduction in evaluated M‐FIM accuracy was considerably larger for the
underprediction simulation (December 26), showing that including PWB will
more greatly “reward” model underpredictions.

Table 6
The Number of Buildings in Each Confusion Matrix Category, Predicted in
the December 27 Simulation Against the Four Final Benchmarks

GT‐FIM

DG2‐FIM

DG1‐FIM

TRS‐FIM

TN

FP

FN

TP

TP + FN

CSI

F1

595

581

2

27

10

37

3

31

30

61

0.47

0.64

590

0

26

17

43

543

3

28

10

38

0.26 (45%)

0.40 (16%)

0.24 (48%)

0.41 (36%)

0.57 (11%)

0.39 (39%)

Note. TP + FN is the total number of buildings that were observed as flooded
by the RS‐FIM benchmarks. CSI and F1 are the model accuracy metrics for
the buildings. The values in parenthesis are the percent difference in CSI and
F1 when using the degraded benchmark compared to using the GT‐FIM
benchmark in the evaluation.

Another aspect of PWB, which was not evaluated in this paper, is the quality
and type of the PWB product. Here, we used the highest quality and resolution
product (ESRI USA Detailed Water Bodies data set) we found for the case
studies. Other products (e.g., the JRC Global Surface Water Mapping Layers)
tend to have coarser resolution or were derived using different techniques.
The impact of such variabilities in PWB products on FIM evaluation results is
largely unknown and is worthy of in‐depth analysis.

The proposed evaluation strategy was successful in improving the robustness
of the evaluation for using the degraded benchmarks. For the synthetically
degraded benchmarks (DG1‐FIM and DG2‐FIM), it did not considerably
affect the results, but that is because the enhancement procedure largely
“restored” the layers to their origin, yielding minimal difference with the GT‐
FIM. The evaluation strategy considerably improved the evaluation results
when using the Traditional Remote Sensing (TRS‐FIM) benchmark, but the

COHEN ET AL.

14 of 19

 19447973, 2025, 8, Downloaded from https://agupubs.onlinelibrary.wiley.com/doi/10.1029/2024WR039574, Wiley Online Library on [14/06/2026]. See the Terms and Conditions (https://onlinelibrary.wiley.com/terms-and-conditions) on Wiley Online Library for rules of use; OA articles are governed by the applicable Creative Commons LicenseWater Resources Research

10.1029/2024WR039574

biases remained high. This leads us to conclude that (a) the robustness of the remote sensing analysis remains
critical for generating robust benchmarks and that the proposed evaluation strategy should not be considered as a
substitute for it, and (b) further research is needed to develop an enhancement or evaluation strategy that can better
deal with overpredictions in the RS‐FIM.

4.1. On the Need for Standards

In this study, we selected five evaluation metrics (CSI, TPR, FAR, F1, and Accuracy (ACC); Equation 1) as a
quantitative measure of model accuracy and its variability when using different benchmarks. As stated, the se-
lection of these five metrics, among dozens available, was not based on sound research or common practice in the
literature but rather on our, quite anecdotal, observations. The results of this study highlight the challenges in the
quantitative assessment of spatially continuous (aerial) predictions and, in particular, of binary mapping. The
results show considerable variability in the sensitivity of the metrics to evaluation layers (benchmarks and
predictions) and, in some cases, contradictory outcomes. This is aligned with the results of Stephens et al. (2014).

The evaluation approach we opted to analyze in this study is the full‐domain/pixel‐to‐pixel comparison in which
the match between the benchmark and predicted FIM is quantified based on a confusion matrix (TP, TN, FP, FN)
for all grid cells in the evaluated domain. This approach has known limitations with class imbalance (e.g.,
dominated by non‐flooded pixels) and spatial autocorrelation between neighboring grid cells. These issues can be
mitigated with a sampling procedure in which a subset of the grid cells is used. The sampling can be random or
stratified and equal proportion (i.e., 50/50 flooded/not‐flooded) or matching proportion (i.e., the number of grid
cells sampled from each class is proportionate to the class's overall proportion in the domain). Sample size is also
a factor that needs to be determined and can be quite influential on the evaluation outcomes. Landwehr
et al. (2024) presented an extensive study on sampling for RS‐FIM evaluation showing, among other important
outcomes, the complexity and uncertainty of sampling strategies.

The need for research‐based and commonly accepted standards in FIM evaluation is clear. Without at least some
degree of common practices, the utility of our FIM research and development efforts is greatly diminished, as
reported advances in model accuracy and application cannot be readily compared across studies. The FIM
community (and the hydrological science community at large) can look at the evolution of accepted practices and
standards in similar scientific disciplines (e.g., Atmospheric Sciences). While common practices often evolve
organically, large organizations (e.g., GEO, the Consortium of Universities for the Advancement of Hydrologic
Science, Inc. (CUAHSI), the Global Flood Partnership, and the Cooperative Institute for Research to Operations
in Hydrology (CIROH)) can play a role in proposing analysis standards.

We propose the following as high‐priority research needs for FIM evaluation:

1. Evaluation metrics and metric selection—elucidation of the strengths/limitations and the true meaning of

existing metrics; development of new metrics and/or metric interpretation standards.

2. Sampling strategy—elucidation of the sensitivity of FIM evaluation to sampling approach and study domain

delineation; development of best practices for the most robust approach(s).

3. Benchmark sensitivity—further explore the implications of biases in benchmark data on evaluation results.
4. RS‐FIM benchmark enhancement—development of novel algorithms focused on compiling better FIM

evaluation benchmarks, particularly, dealing with false positives in RS‐FIM.

5. User‐centric evaluation—framing of the FIM accuracy requirements and focus (e.g., buildings, extent) of
different end‐user groups (e.g., model developers, forecasters, emergency managers); development of eval-
uation approaches that better address end‐users' needs.

4.2. Qualitative/Secondary Evaluation

Quantitative evaluation approaches, such as the one used in this paper, are fundamental tools in research and
development. For FIM, different end users differ in their accuracy assessment needs/emphasis. First responders
and emergency managers, for example, are more likely to be concerned about the accuracy of flood impact
predictions on buildings and transportation. In this study, we focused on an evaluation approach that is most
useful for model developers and users. To illustrate the argument that different evaluation approaches are war-
ranted for different types of end‐users and that RS‐FIM benchmarking quality is critical for impact‐based
evaluation, we analyzed building flooding detection accuracy.

COHEN ET AL.

15 of 19

 19447973, 2025, 8, Downloaded from https://agupubs.onlinelibrary.wiley.com/doi/10.1029/2024WR039574, Wiley Online Library on [14/06/2026]. See the Terms and Conditions (https://onlinelibrary.wiley.com/terms-and-conditions) on Wiley Online Library for rules of use; OA articles are governed by the applicable Creative Commons LicenseWater Resources Research

10.1029/2024WR039574

The total number of buildings detected as flooded by the Ground Truth FIM (GT‐FIM) is 61 (Table 6). Model
prediction (December 27) was only able to detect 30 buildings (TP) accurately, with 31 erroneously predicted as
not flooded (FN), and 3 buildings were erroneously predicted as flooded (FP). This, under 50%, hit rate is re-
flected in the building‐impact CSI and F1 scores which are considerably lower than the “whole‐domain” eval-
uation analysis results (0.75 and 0.85 respectively; Table 4). The degraded benchmarks yielded considerably
lower building‐impact CSI and F1 scores, highlighting the effect of benchmark quality on impact‐based evalu-
ation results. The differences in CSI and F1 when using the degraded benchmarks are even greater than the bias
found using the original benchmarks in the “whole‐domain” analysis (Table 1). Furthermore, the number of
buildings detected as flooded (TP + FN in Table 6) by the degraded benchmarks is considerably lower than the
GT‐FIM. This is caused by the exclusion of gap‐filled grid cells in the proposed evaluation framework. These
results show that the proposed evaluation framework is not readily suitable for impact‐based or similar analysis.
This is not surprising considering its intended evaluation use, but it is worth emphasizing.

The impact‐based results showcase the discrepancies in evaluation types. The final “whole‐domain” evaluation
results yielded accuracy assessment values of 0.75 and 0.85 for CSI and F1, respectively, for the December 27
simulation using the GT‐FIM benchmark (Table 4). These values can be interpreted as good model accuracy. The
building impact analysis, on the other hand, yielded CSI and F1 values of 0.47 and 0.64, respectively, for the same
simulation and benchmark (Table 6). With a detection of less than 50% of the flooded buildings, the simulation
accuracy should be interpreted as poor. This highlights the need for end‐user‐centric and multifaceted evaluation
approaches that can provide more holistic information about the accuracy of predicted FIMs.

Qualitative assessment of FIM is rare in the scientific literature. This is understandable considering the need for
objectivity and the use of acceptable metrics in the reporting of scientific results. In operational or commercial
applications, it is often the case that an expert interpretation and/or quality control is included in the FIM
dissemination pipeline. We argue that qualitative interpretation of FIM predictions can be a useful analysis
component, one that can mitigate the limitations in quantitative FIM evaluation (Schumann, Bates, et al., 2009;
Schumann, Di Baldassarre, & Bates, 2009). Examine, for example, Figure 2 above. Numerous insights can be
drawn from a visual investigation of the FIMs that cannot be interpreted from the evaluation metrics alone. Spatial
context and dynamics are vital in FIM predictions and use. The scientific community should be encouraged to
practice it. Qualitative assessment can also rely on interpreting different types of quantitative results, for example,
the above discussion about the building impact analysis.

A common issue we observed in our own FIM modeling research is that improvement/changes in the predictive
framework may yield negligible differences in inundation (binary) evaluation metrics. This is most common
when predicting FIM over large domains or for high‐magnitude floods, in which the floodplain is nearly fully
inundated. Did the modifications not result in changes to the model predictions? Visual interpretation and the use
of secondary sources may lead us to a different conclusion as, for example, relatively minor changes in the flood
boundary (a few grid cells) can dramatically change its predictive quality. The opposite is also commonplace,
where significant improvements in evaluation metrics are reported while the predictive quality of the FIM may
have, in practice, deteriorated.

Better FIM model evaluation practices may mitigate some of these issues. For example, simulating very large
floods over an alluvial floodplain is an easy target that will lead to inflated accuracy assessment. This is, un-
fortunately, a common practice due to the availability of (simulated) 100 and 500‐year flood predictions for the
US and elsewhere and the scarcity of inundation data for historical flood events. This type of model‐to‐model
evaluation is bad practice, for obvious reasons, in most cases. Improving the availability of observational FIM
data is thus paramount for improving FIM models and their evaluation practices. This should be combined with
efforts aimed at improving our evaluation approaches and establishing standards.

5. Conclusions

The use of RS‐FIM as an evaluation benchmark of model‐predicted FIM (M‐FIM) is appealing as it can provide
information on the areal extent of real flood events, often over relatively large spatial domains. Limitations in RS‐
FIM, including, for example, omission of under‐canopy floodwater, are typically overlooked in model evaluation
analysis. M‐FIM evaluation practices, particularly those using FIM as a benchmark (as opposed to point ob-
servations), lack standards and robust interpretation of the results. This includes the use of diverse arrays of
evaluation metrics and data sampling approaches. Although RS‐FIM has been employed in numerous studies over

COHEN ET AL.

16 of 19

 19447973, 2025, 8, Downloaded from https://agupubs.onlinelibrary.wiley.com/doi/10.1029/2024WR039574, Wiley Online Library on [14/06/2026]. See the Terms and Conditions (https://onlinelibrary.wiley.com/terms-and-conditions) on Wiley Online Library for rules of use; OA articles are governed by the applicable Creative Commons LicenseWater Resources Research

10.1029/2024WR039574

many years for M‐FIM evaluation, we argue that there remains a lack of sufficient knowledge and standardized
approaches to ensure its reliability and robustness.

In this paper, we analyzed the impact of RS‐FIM biases on M‐FIM evaluation and proposed and tested a new
evaluation strategy that includes RS‐FIM and benchmarking enhancements. We used a meticulously classified
RS‐FIM from hyper‐resolution aerial imagery for a 2016 flood over a section of the Arkansas River as a Ground
Truth benchmark (GT‐FIM). This benchmark was used to calculate the “true” M‐FIM accuracy assessment. We
synthetically degraded the GT‐FIM to generate two biased RS‐FIMs, a moderately and a severely degraded FIM
(DG1‐FIM and DG2‐FIM, respectively). A simple supervised classification analysis was used to create an
additional benchmark, which we referred to as a “Traditional RS‐FIM” (TRS‐FIM). Two M‐FIM complied for
HEC‐RAS simulations of the flood event: an under‐predicting simulation (December 26) and a slightly over-
predicting simulation (December 27). The evaluation analyses approach we opted to apply in this paper is a
whole‐domain pixel‐to‐pixel (confusion matrix) quantification using five binary evaluation metrics.

Significant differences in M‐FIM accuracy assessment were found when using the different benchmarks. This
showed that M‐FIM evaluation is highly sensitive to the quality of the benchmark used and that typical biases in
RS‐FIM can severely degrade the accuracy of the evaluation analysis. Biases in the evaluation results increased
considerably for the more degraded benchmark (DG2‐FIM) and were highest for the TRS‐FIM.

An RS‐FIM enhancement methodology was introduced, which removes small flood clusters and fills gaps be-
tween observed flooding grid cells based on topography. The enhancement procedure considerably improved the
synthetically degraded benchmarks (DG1‐FIM and DG2‐FIM) as these only included missing floodwaters (false
negatives), which were successfully filled by the gap‐filling algorithm. The enhancement algorithm yielded
poorer results for the TRS‐FIM, mainly because the gap‐filling algorithm over‐extended the inundation due to
false positive errors (falsely classified as flooded) in the RS‐FIM.

Permanent Water Bodies are often included in the M‐FIM evaluation procedure, which can considerably inflate
the model's accuracy. In this paper, we demonstrated this issue by comparing the evaluation results for when PWB
are included and excluded. The results, indeed, show that the model accuracy assessment, when excluding PWD,
drops considerably for all metrics in the GT‐FIM and most metrics when using the degraded benchmarks. The
effect of PWB exclusion on M‐FIM evaluation is likely to be a function of the proportion of PWB and floodwater
in the evaluated domain. In the case study used in this paper, PWB is 17% and floodwater is ∼35% of all grid cells.
We conclude that PWB should be removed from M‐FIM evaluation, especially when the proportion of PWB is
not insignificant.

Our M‐FIM evaluation strategy is based on high‐confidence grid cells, excluding low‐confidence and PWB grid
cells. High‐confidence grid cells are those that were classified as flooded by the remote sensing analysis (assumed
to be observed floodwater) and those that were not estimated to be flooded by the RS‐FIM enhancement algo-
rithm. By excluding the grid cells “flooded” by the gap‐filling procedure, we avoid introducing modeling/esti-
mation into the benchmark data set, while removing grid cells that have a high likelihood of misclassification in
the RS‐FIM (e.g., under canopy).

The proposed evaluation strategy was assessed by comparing its evaluation results, looking for reductions in the
difference in the metric values between the use of GT‐FIM and the degraded benchmarks. The results show that
the synthetically degraded benchmarks were not considerably affected because the enhancement procedure was
able to closely align them with the GT‐FIM. The fact that the evaluation strategy did not affect the evaluation in
this case is a good outcome, as it shows that using a well‐enhanced benchmark will not adversely affect the
evaluation results. The evaluation strategy considerably improved the evaluation results when using the TRS‐
FIM. However, the biases when using this benchmark remained high. We conclude that the proposed evalua-
tion strategy improves the robustness and reliability of the M‐FIM evaluation using RS‐FIM as a benchmark, but
it cannot fully compensate for low‐quality RS‐FIM.

The analyses presented in this paper highlighted many challenges in FIM evaluation. Quantitative evaluation
metrics were shown to have a large degree of variability in their sensitivity to benchmarking quality and M‐FIM
accuracy. There is no commonly accepted practice for the interpretation of evaluation metrics' values and their
limitations and biases are often ignored in the literature. We argued that there is a great need to improve our
understanding of FIM evaluation practices and the development of widely accepted standards. These should
include an element that addresses differences between FIM end‐users. We showcased impact‐based FIM

COHEN ET AL.

17 of 19

 19447973, 2025, 8, Downloaded from https://agupubs.onlinelibrary.wiley.com/doi/10.1029/2024WR039574, Wiley Online Library on [14/06/2026]. See the Terms and Conditions (https://onlinelibrary.wiley.com/terms-and-conditions) on Wiley Online Library for rules of use; OA articles are governed by the applicable Creative Commons LicenseAcknowledgments
This research was supported by the
Cooperative Institute for Research to
Operations in Hydrology (CIROH) with
funding under award NA22NWS4320003
from the NOAA Cooperative Institute
Program. The statements, findings,
conclusions, and recommendations are
those of the author(s) and do not
necessarily reflect the opinions of NOAA.

Water Resources Research

10.1029/2024WR039574

evaluation, using a building footprint data set. The analysis showed considerable deviation in M‐FIM quality
assessment compared to the results from the “whole domain” analysis. We called for the adoption of a more
holistic approach to FIM evaluation, one that may use multiple quantitative analyses and qualitative assessments.

Data Availability Statement

All the software and pre‐processed data sets are available in open repositories. The Python scripts for the remote
sensing flood inundation mapping enhancement and the evaluation procedure are available here https://github.
com/sagycohen/FIM‐Evaluation. The QGIS plugin for the HGRG algorithm is available at https://github.com/
tian‐dandan/FIM‐Enhance‐QGIS. The aerial imagery used to generate the benchmark was downloaded from the
NOAA Strom Imagery Portal: https://storms.ngs.noaa.gov. The ESRI USA Detailed Water Bodies data set is
accessible through: https://hub.arcgis.com/datasets/esri::usa‐detailed‐water‐bodies/about. The Digital Evevation
Model was downloaded from the USGS National Maps portal: https://apps.nationalmap.gov/downloader/.

References

Aristizabal, F., Chegini, T., Petrochenkov, G., Salas, F., & Judge, J. (2024). Effects of high‐quality elevation data and explanatory variables on the
accuracy of flood inundation mapping via Height Above Nearest Drainage. Hydrology and Earth System Sciences, 28(6), 1287–1315. https://
doi.org/10.5194/hess‐28‐1287‐2024

Aristizabal, F., Judge, J., & Monsivais‐Huertero, A. (2020). High‐resolution inundation mapping for heterogeneous land covers with synthetic

aperture radar and terrain data. Remote Sensing, 12(6), 900. https://doi.org/10.3390/rs12060900

Bernhofen, M. V., Cooper, S., Trigg, M., Mdee, A., Carr, A., Bhave, A., et al. (2022). The role of global data sets for riverine flood risk man-

agement at national scales. Water Resources Research, 58(4), e2021WR031555. https://doi.org/10.1029/2021wr031555

Betterle, A., & Salamon, P. (2024). Water depth estimate and flood extent enhancement for satellite‐based inundation maps. Natural Hazards and

Earth System Sciences, 24(8), 2817–2836. https://doi.org/10.5194/nhess‐24‐2817‐2024

Bryant, S., McGrath, H., & Boudreault, M. (2021). Gridded flood depth estimates from satellite derived inundations. Natural Hazards and Earth

System Sciences Discussions, 2021, 1–21.

Cohen, S., Peter, B. G., Haag, A., Munasinghe, D., Moragoda, N., Narayanan, A., & May, S. (2022). Sensitivity of remote sensing floodwater
depth calculation to boundary filtering and digital elevation model selections. Remote Sensing, 14(21), 5313. https://doi.org/10.3390/
rs14215313

Cohen, S., Raney, A., Munasinghe, D., Loftis, J. D., Molthan, A., Bell, J., et al. (2019). The Floodwater Depth Estimation Tool (FwDET v2. 0) for
improved remote sensing analysis of coastal flooding. Natural Hazards and Earth System Sciences, 19(9), 2053–2065. https://doi.org/10.5194/
nhess‐19‐2053‐2019

Frame, J. M., Nair, T., Sunkara, V., Popien, P., Chakrabarti, S., Anderson, T., et al. (2024). Rapid inundation mapping using the US National
Water Model, satellite observations, and a convolutional neural network. Geophysical Research Letters, 51(17), e2024GL109424. https://doi.
org/10.1029/2024gl109424

Giezendanner, J., Mukherjee, R., Purri, M., Thomas, M., Mauerman, M., Islam, A. K. M. S., & Tellman, B. (2023). Inferring the past: A combined
CNN–LSTM deep learning framework to fuse satellites for historical inundation mapping. 2023 IEEE/CVF Conference on Computer Vision
and Pattern Recognition Workshops (CVPRW), 521, 2155–2165. https://doi.org/10.1109/cvprw59228.2023.00209

Grimaldi, S., Li, Y., Pauwels, V. R. N., & Walker, J. P. (2016). Remote sensing‐derived water extent and level to constrain hydraulic flood
forecasting models: Opportunities and challenges. Surveys in Geophysics, 37(5), 977–1034. https://doi.org/10.1007/s10712‐016‐9378‐y
Gutenson, J., Tavakoly, A., Islam, M., Wing, O., Lehman, W., Hamilton, C., & Massey, C. (2022). Comparison of flood inundation modeling

frameworks within a small coastal watershed during a compound flood event. Hydrological Hazards, 23(1), 261–277.

Hawker, L., Neal, J., Savage, J., Kirkpatrick, T., Lord, R., Zylberberg, Y., et al. (2024). Assessing LISFLOOD‐FP with the next‐generation digital
elevation model FABDEM using household survey and remote sensing data in the Central Highlands of Vietnam. Natural Hazards and Earth
System Sciences, 24(2), 539–566. https://doi.org/10.5194/nhess‐24‐539‐2024

Hawker, L., Neal, J., Tellman, B., Liang, J., Schumann, G., Doyle, C., et al. (2020). Comparing earth observation and inundation models to map

flood hazards. Environmental Research Letters, 15(12), 124032. https://doi.org/10.1088/1748‐9326/abc216

Herbanu, P. S., Nurmaya, A., Nisaa, R. M., Wardana, R. A., & Sahid (2024). The zoning of flood disasters by combining tidal flood and urban
flood in Semarang City, Indonesia. In IOP conference series: Earth and environmental science (Vol. 1314(1), p. 012028). IOP Publishing.
https://doi.org/10.1088/1755‐1315/1314/1/012028

Hooker, H., Dance, S. L., Mason, D. C., Bevington, J., & Shelton, K. (2022). Spatial scale evaluation of forecast flood inundation maps. Journal of

Hydrology, 612, 128170. https://doi.org/10.1016/j.jhydrol.2022.128170

Hooker, H., Dance, S. L., Mason, D. C., Bevington, J., & Shelton, K. (2023). Assessing the spatial spread–skill of ensemble flood maps with
remote‐sensing observations. Natural Hazards and Earth System Sciences, 23(8), 2769–2785. https://doi.org/10.5194/nhess‐23‐2769‐2023
Horritt, M. S. (2006). A methodology for the validation of uncertain flood inundation models. Journal of Hydrology, 326(1–4), 153–165. https://

doi.org/10.1016/j.jhydrol.2005.10.027

Hunter, N. M., Bates, P. D., Horritt, M. S., De Roo, A. P. J., & Werner, M. G. (2005). Utility of different data types for calibrating flood inundation

models within a GLUE framework. Hydrology and Earth System Sciences, 9(4), 412–430. https://doi.org/10.5194/hess‐9‐412‐2005

Jafarzadegan, K., Abbaszadeh, P., & Moradkhani, H. (2021). Sequential data assimilation for real‐time probabilistic flood inundation mapping.

Hydrology and Earth System Sciences, 25(9), 4995–5011. https://doi.org/10.5194/hess‐25‐4995‐2021

Johnson, J. M., Munasinghe, D., Eyelade, D., & Cohen, S. (2019). An integrated evaluation of the national water model (NWM)–Height above
nearest drainage (HAND) flood mapping methodology. Natural Hazards and Earth System Sciences, 19(11), 2405–2420. https://doi.org/10.
5194/nhess‐19‐2405‐2019

Konapala, G., Kumar, S. V., & Ahmad, S. K. (2021). Exploring Sentinel‐1 and Sentinel‐2 diversity for flood inundation mapping using deep
learning. ISPRS Journal of Photogrammetry and Remote Sensing: Official Publication of the International Society for Photogrammetry and
Remote Sensing, 180, 163–173.

Landwehr, T., Dasgupta, A., & Waske, B. (2023). Towards robust validation strategies for EO flood maps. Available at SSRN 4877998.

COHEN ET AL.

18 of 19

 19447973, 2025, 8, Downloaded from https://agupubs.onlinelibrary.wiley.com/doi/10.1029/2024WR039574, Wiley Online Library on [14/06/2026]. See the Terms and Conditions (https://onlinelibrary.wiley.com/terms-and-conditions) on Wiley Online Library for rules of use; OA articles are governed by the applicable Creative Commons LicenseWater Resources Research

10.1029/2024WR039574

Landwehr, T., Dasgupta, A., & Waske, B. (2024). Towards robust validation strategies for EO flood maps. Remote Sensing of Environment, 315,

114439. https://doi.org/10.1016/j.rse.2024.114439

Liu, H., & Jezek, K. C. (2004). Automated extraction of coastline from satellite imagery by integrating Canny edge detection and locally adaptive

thresholding methods. International Journal of Remote Sensing, 25(5), 937–958. https://doi.org/10.1080/0143116031000139890

Liu, H., Wang, L., Sherman, D., Gao, Y., & Wu, Q. (2010). An object‐based conceptual framework and computational method for representing
and analyzing coastal morphological changes. International Journal of Geographical Information Science, 24(7), 1015–1041. https://doi.org/
10.1080/13658810903270569

Mason, D. C., Bates, P. D., & Dall'Amico, J. T. (2009). Calibration of uncertain flood inundation models using remotely sensed water levels.

Journal of Hydrology, 368(1–4), 224–236. https://doi.org/10.1016/j.jhydrol.2009.02.034

Mateo‐Garcia, G., Veitch‐Michaelis, J., Smith, L., Oprea, S. V., Schumann, G., Gal, Y., et al. (2021). Towards global flood mapping onboard low

cost satellites with machine learning. Scientific Reports, 11(1), 7249. https://doi.org/10.1038/s41598‐021‐86650‐z

Musa, Z. N., Popescu, I., & Mynett, A. (2015). A review of applications of satellite SAR, optical, altimetry and DEM data for surface water
modelling, mapping and parameter estimation. Hydrology and Earth System Sciences, 19(9), 3755–3769. https://doi.org/10.5194/hess‐19‐
3755‐2015

Nemni, E., Bullock, J., Belabbes, S., & Bromley, L. (2020). Fully convolutional neural network for rapid flood segmentation in synthetic aperture

radar imagery. Remote Sensing, 12(16), 2532. https://doi.org/10.3390/rs12162532

Nevo, S., Morin, E., Gerzi Rosenthal, A., Metzger, A., Barshai, C., Weitzner, D., et al. (2022). Flood forecasting with machine learning models in

an operational framework. Hydrology and Earth System Sciences, 26(15), 4013–4032. https://doi.org/10.5194/hess‐26‐4013‐2022

Pappenberger, F., Frodsham, K., Beven, K., Romanowicz, R., & Matgen, P. (2007). Fuzzy set approach to calibrating distributed flood inundation
models using remote sensing observations. Hydrology and Earth System Sciences, 11(2), 739–752. https://doi.org/10.5194/hess‐11‐739‐2007
Pappenberger, F., Matgen, P., Beven, K. J., Henry, J. B., Pfister, L., & de Fraipont, P. (2006). Influence of uncertain boundary conditions and
model structure on flood inundation predictions. Advances in Water Resources, 29(10), 1430–1449. https://doi.org/10.1016/j.advwatres.2005.
11.012

Peng, B., Meng, Z., Huang, Q., & Wang, C. (2019). Patch similarity convolutional neural network for urban flood extent mapping using Bi‐

Temporal satellite multispectral imagery. Remote Sensing, 11(21), 2492. https://doi.org/10.3390/rs11212492

Peter, B. G., Cohen, S., Lucey, R., Munasinghe, D., Raney, A., & Brakenridge, G. R. (2020). Google Earth engine implementation of the
floodwater depth estimation tool (FwDET‐GEE) for rapid and large scale flood analysis. IEEE Geoscience and Remote Sensing Letters, 19, 1–
5. https://doi.org/10.1109/LGRS.2020.3031190

Rasid, H., & Pramanik, M. A. H. (1990). Visual interpretation of satellite imagery for monitoring floods in Bangladesh. Environmental Man-

agement, 14(6), 815–821. https://doi.org/10.1007/bf02394176

Sanderson, J., Mao, H., Abdullah, M. A., Al‐Nima, R. R. O., & Woo, W. L. (2023). Optimal fusion of multispectral optical and SAR images for

flood inundation mapping through explainable deep learning. Information, 14(12), 660. https://doi.org/10.3390/info14120660

Sanyal, J., & Lu, X. X. (2004). Application of remote sensing in flood management with special reference to monsoon Asia: A review. Natural

Hazards, 33(2), 283–301. https://doi.org/10.1023/b:nhaz.0000037035.65105.95

Schumann, G., Bates, P. D., Horritt, M. S., Matgen, P., & Pappenberger, F. (2009). Progress in integration of remote sensing–derived flood extent

and stage data and hydraulic models. Reviews of Geophysics, 47(4). https://doi.org/10.1029/2008rg000274

Schumann, G., Di Baldassarre, G., & Bates, P. D. (2009). The utility of spaceborne radar to render flood inundation maps based on multialgorithm

ensembles. IEEE Transactions on Geoscience and Remote Sensing, 47(8), 2801–2807. https://doi.org/10.1109/TGRS.2009.2017937

Schumann, G. J.‐P. (2019). The need for scientific rigour and accountability in flood mapping to better support disaster response. Hydrological

Processes, 33(24), 3138–3142. https://doi.org/10.1002/hyp.13547

Shastry, A., Carter, E., Coltin, B., Sleeter, R., McMichael, S., & Eggleston, J. (2023). Mapping floods from remote sensing data and quantifying
the effects of surface obstruction by clouds and vegetation. Remote Sensing of Environment, 291, 113556. https://doi.org/10.1016/j.rse.2023.
113556

Sonka, M., Hlavac, V., & Boyle, R. (1999). Image processing, analysis, and machine vision. PWS Pub.
Soria‐Ruiz, J., Fernandez‐Ordoñez, Y. M., Ambrosio‐Ambrosio, J. P., Escalona‐Maurice, M. J., Medina‐García, G., Sotelo‐Ruiz, E. D., &
Ramirez‐Guzman, M. E. (2022). Flooded extent and depth analysis using optical and SAR remote sensing with machine learning algorithms.
Atmosphere, 13(11), 1852. https://doi.org/10.3390/atmos13111852

Stephens, E., Schumann, G., & Bates, P. (2014). Problems with binary pattern measures for flood model evaluation. Hydrological Processes,

28(18), 4928–4937. https://doi.org/10.1002/hyp.9979

Stephens, E. M., Bates, P. D., Freer, J. E., & Mason, D. C. (2012). The impact of uncertainty in satellite data on the assessment of flood inundation

models. Journal of Hydrology, 414, 162–173. https://doi.org/10.1016/j.jhydrol.2011.10.040

Tian, D., Liu, H., Wang, L., Cohen, S., & Thapa, P. (2024). Enhancing satellite image‐derived flood maps with hydrologically guided region

growing method and high‐resolution DEMs. In Chapman conference on remote sensing of the water cycle. AGU.

Venkata Rao, G., Nagireddy, N. R., Keesara, V. R., Sridhar, V., Srinivasan, R., Umamahesh, N. V., & Pratap, D. (2024). Real‐time flood
forecasting using an integrated hydrologic and hydraulic model for the Vamsadhara and Nagavali basins, Eastern India. Natural Hazards,
120(7), 1–29. https://doi.org/10.1007/s11069‐023‐06366‐3

Wing, O. E., Smith, A. M., Marston, M. L., Porter, J. R., Amodeo, M. F., Sampson, C. C., & Bates, P. D. (2021). Simulating historical flood events
at the continental scale: Observational validation of a large‐scale hydrodynamic model. Natural Hazards and Earth System Sciences, 21(2),
559–575. https://doi.org/10.5194/nhess‐21‐559‐2021

Wing, O. E. J., Sampson, C. C., Bates, P. D., Quinn, N., Smith, A. M., & Neal, J. C. (2019). A flood inundation forecast of Hurricane Harvey using

a continental‐scale 2D hydrodynamic model. Journal of Hydrology X, 4, 100039. https://doi.org/10.1016/j.hydroa.2019.100039

Yan, K., Di Baldassarre, G., Solomatine, D. P., & Schumann, G. J.‐P. (2015). A review of low‐cost space‐borne data for flood modelling:

Topography, flood extent and water level. Hydrological Processes, 29(15), 3368–3387. https://doi.org/10.1002/hyp.10449

Zwenzner, H., & Voigt, S. (2009). Improved estimation of flood parameters by combining space based SAR data with very high resolution digital

elevation data. Hydrology and Earth System Sciences, 13(5), 567–576. https://doi.org/10.5194/hess‐13‐567‐2009

COHEN ET AL.

19 of 19

 19447973, 2025, 8, Downloaded from https://agupubs.onlinelibrary.wiley.com/doi/10.1029/2024WR039574, Wiley Online Library on [14/06/2026]. See the Terms and Conditions (https://onlinelibrary.wiley.com/terms-and-conditions) on Wiley Online Library for rules of use; OA articles are governed by the applicable Creative Commons License