Improved processing of multitemporal SWOT SAR images
with deep learning

1 Context

The SWOT mission developed by the space agencies NASA and CNES has been laun-
ched at the end of 2022 and, after a first commissioning phase, is now delivering its data.
With its wide-swath Ka-band radar interferometer KaRIn, SWOT delivers unprecedented
images of Earth’s lakes and rivers. The combination of a high frequency band and near-
nadir incidence maximizes the radar return of water areas and leads to images with very
different radiometric contrasts and geometric distortions compared to more conventional
synthetic aperture radar (SAR) images by satellites such as Sentinel-1.

During the preparation of the mission, research and development work supported by
two Ph.D. works supervised at Telecom Paris has led to the design of processing pipelines
to detect lakes and rivers and feed the water height estimation with water masks. With
the delivery of images captured by the satellite and the rise of powerful deep learning
techniques, advanced processing strategies can now be considered in order to (i) improve
SWOT images (reduction of speckle fluctuations and of interferometric phase noise) and (ii)
enhance information extraction from these images thanks to the combination of geometrical
models of the acquisition, multi-temporal information, and data from different sources.
The objective is to overcome current limitations that degrade the water detection (e.g. :
dark water, bright mud, wet fields, built areas,...) and prevent the level 2 products from
reaching the full potential of the SWOT data. The reduction of speckle and the analysis
of time-series of SWOT images are expected to open up new perspectives for the study of
wet areas or snow-covered lakes. In the context of a possible InSAR Sentinel-3 NG Topo
mission, more robust processing pipelines will be necessary to compensate for the less
reliable interferometric phase measurements (due to the use of a smaller interferometric
baseline and poorer signal-to-noise ratio specifications). The deployment of deep neural
networks and the tighter inclusion of complementary sources of data is a promising research
direction to achieve greater robustness.

The two modes of the SWOT mission, one for the ocean observation with a coarse resolution,
and the other one with a finer resolution for continental applications.

1

2 PhD description

In this thesis, we propose to exploit deep learning approaches to :
— improve SWOT data (speckle reduction and improvement of the interferometric

phase quality),

— extract information (water mask segmentation, height estimation, change detec-

tion).

We distinguish three lines of research : the first one based on the exploitation of single-date
data ; the second analyzing SWOT or multi-sensor time series ; the third focusing on height
extraction by combining information.

2.1 SWOT image despeckling and single-date water segmentation

SWOT data, like all radar data, are subject to the speckle phenomenon with strong
fluctuations present in amplitude or interferometric data. Reducing these fluctuations allow
a better exploitation of these data.

We propose to develop speckle reduction approaches dedicated to SWOT data by adap-
ting and extending the SAR2SAR [2] and MERLIN [3] approaches we have recently propo-
sed. The adaptation of SAR2SAR for radiometric improvement requires the availability of
independent SWOT image pairs with no displacement of scene objects. Exploiting SWOT
multi-temporal acquisitions should enable dedicated training for this sensor, provided we
can compensate or take into account not only radiometric changes but also any translations
linked to height variations. Another possibility would be to exploit data acquired with a
short revisit time of one day, between March 29 and July 10, 2023 which should present
few temporal changes. The MERLIN adaptation requires the spectrum to be symmetrical
with respect to the origin, but then allows the network to be trained on the basis of the
complex data alone. Another avenue for further research is the simultaneous use of the in-
terferometric pair as a replacement for the coherent power calculation currently performed
by [5].

It is also possible to extend these speckle reduction frameworks, in particular SAR2SAR
for complex multi-channel data, i.e. in interferometric configuration. We therefore propose
to evaluate their interest for improving interferometric phase and coherence in the SWOT
processing chain.

In addition to amplitude and interferometric phase denoising for the extraction of water
surfaces and the calculation of the 3D point cloud on rivers, deep learning approaches could
be highly effective for extracting the water mask, or other intermediate classes that are
visible on SWOT data (frozen lakes, wetlands, etc.). Works on "self-supervised learning"
have shown that training a network on an ancillary task enables the construction of an
efficient representation space for other tasks. We propose to exploit these approaches for
water surface extraction, using the ancillary task of denoising in the spirit of the "Denoiseg"
method [1] and MERLIN-Seg [4]. Indeed, even with a small number of labeled data, very
good results can be obtained. It would also be interesting to exploit coherence information
within this framework and extend the "Denoiseg" principle to the interferometric context.

2.2 Multi-temporal, multi-sensor processing

SWOT enables acquisitions with a revisit period of 22 days in nominal mode. Exploiting
multi-temporal information opens the way to very efficient strategies for speckle reduction
[6]. In the context of SWOT and the incidence angles used, variations in water height can
lead to significant translations in the image. It will be necessary to take this phenomenon
into account in the neural architecture developed (for example, by jointly calculating a wa-
ter mask or a shift mask, or by exploiting the interferometric and translation information).
It will also be important to take into account the presence of auxiliary data such as water
masks known a priori.

2

Another topic of interest is the use of other satellite data like Sentinel-1 or Sentinel-2
to help SWOT data exploitation. The preliminary registration step should be carefully
handled by taking into account SWOT specificities.

2.3 Novel methods of water height estimation

Deep neural networks can be trained to estimate the water level from different types of
information : geometric information provided by acquisitions in ascending and descending
modes, and information provided by single-pass interferometry. Water segmentation and
height estimation tasks would then be jointly performed. Beyond estimation, uncertainty
characterization is crucial to pave the way for subsequent information fusion processes.

3 Supervision of the PhD

The doctoral work will be carried out in the LTCI laboratory of Télécom Paris, under
the supervision of Prof. Florence Tupin (Télécom Paris) and Prof. Loïc Denis (Université
Jean Monnet Saint-Etienne). Links with ongoing works on swath altimetry missions will
be reached by a CNES supervision (DTN/CD/TPA : Nicolas Gasnier, DTN/TPI/TR, and
DOA/OT/OH) and regular stays at the CNES. If adequate, further association with SWOT
and Sentinel-3 NG Topo missions could translate into collaborations with the international
partners.

Références

[1] Tim-Oliver Buccholz, Mangal Prakash, Alexander Krull, and Florian Jug. Denoiseg :

Joint denoising and segmentation. In MICCAI, 2020.

[2] Emanuele Dalsasso, Loïc Denis, and Florence Tupin. SAR2SAR : a semi-supervised
despeckling algorithm for SAR images. IEEE Journal of Selected Topics in Applied
Earth Observations and Remote Sensing, pages 1–1, 2021. Article accepted for publi-
cation to IEEE Journal of Selected Topics in Applied Earth Observations and Remote
Sensing. Code is made available at https ://gitlab.telecom-paris.fr/RING/SAR2SAR.

[3] Emanuele Dalsasso, Loïc Denis, and Florence Tupin. As if by magic : self-supervised
training of deep despeckling networks with MERLIN. IEEE Transactions on Geoscience
and Remote Sensing, 60, 2022.

[4] Emanuele Dalsasso, Clément Rambour, Nicolas Trouvé, and Nicolas Thome. MERLIN-
Seg : self-supervised despeckling for label-efficient semantic segmentation. HAL
https ://cnam.hal.science/hal-04163624, 2023.

[5] Sylvain Lobry, Loïc Denis, Brent Williams, Roger Fjørtoft, and Florence Tupin. Water
Detection in SWOT HR Images Based on Multiple Markov Random Fields. IEEE Jour-
nal of Selected Topics in Applied Earth Observations and Remote Sensing, 12(11) :4315–
4326, November 2019.

[6] Inès Meraoumia, Emanuele Dalsasso, Loïc Denis, Rémy Abergel, and Florence Tupin.
IEEE

Multi-temporal speckle reduction with self-supervised deep neural networks.
Transactions on Geoscience and Remote Sensing, 61, January 2023.

3
