# Dentalum audit and implementation coverage

Audited 18 October 2026. The crawl followed internal navigation, menus, footer links, robots.txt, the sitemap index and every child sitemap, then recursively followed internal HTML links.

**239 discovered URLs; 223 preserved page routes; 224 implemented pages including the searchable sitemap.**

Original public HTML, text, headings, links, image references, layout structure and source behavior were inspected. Original native booking/submit operations were not transacted. Each implemented route was then loaded in Chromium at desktop and mobile widths in both themes. Tablet overflow checks and shared interaction tests are recorded separately.

## Source failures

| Source | HTTP status | Handling |
|---|---:|---|
| [https://dentalum.com/cdn-cgi/l/email-protection](https://dentalum.com/cdn-cgi/l/email-protection) | 404 | Decoded original address markup into mailto links |
| [https://dentalum.com/wp-content/uploads/2025/12/Riktlinjer-for-direktmarknadsforing.pdf](https://dentalum.com/wp-content/uploads/2025/12/Riktlinjer-for-direktmarknadsforing.pdf) | 429 | Retained original external document link |
| [https://kungsf29.mydental.host/wp-content/uploads/2022/11/tandlakare-kvinna-2000px.webp](https://kungsf29.mydental.host/wp-content/uploads/2022/11/tandlakare-kvinna-2000px.webp) | 500 | Clearly marked unavailable source image; original link retained |

No other discovered HTML page returned a non-200 result. Redirected aliases are recorded in `audit/crawl.json`.

## Verification

- All 224 routes: one main H1, loaded local images, light/dark rendering and no desktop/mobile overflow.
- No broken internal page links, fragment targets or local image paths.
- No browser JavaScript exceptions.
- Clinic search, region filters, reset/empty states; team search and roles; treatment selector and validation; FAQ open/close/all; gallery controls/keyboard; mobile menu/Escape; booking selector/Escape; remembered theme; reduced motion; larger text.
- Representative full-page screenshots and machine-readable results are in `audit/`.
- External booking and contact submissions remain on the original services and were not submitted.
- Static reviews are dated snapshots and are not presented as a live feed.

## Page inventory

| URL | Page | Source response | Implementation | Browser |
|---|---|---:|---|---|
| `/` | Tandvård som gör skillnad – med dig i centrum | 200 | Complete | Desktop/mobile, light/dark |
| `/author/admin/` | Tandvård som gör skillnad – med dig i centrum | 200 | Complete | Desktop/mobile, light/dark |
| `/behandlingar/` | Behandlingar | 200 | Complete | Desktop/mobile, light/dark |
| `/behandlingar/airflow/` | Airflow | 200 | Complete | Desktop/mobile, light/dark |
| `/behandlingar/allmantandvard/` | Allmäntandvård | 200 | Complete | Desktop/mobile, light/dark |
| `/behandlingar/basundersokning/` | Basundersökning | 200 | Complete | Desktop/mobile, light/dark |
| `/behandlingar/bettfysiologi/` | Bettfysiologi | 200 | Complete | Desktop/mobile, light/dark |
| `/behandlingar/bettskena/` | Bettskena | 200 | Complete | Desktop/mobile, light/dark |
| `/behandlingar/estetisk-tandvard/` | Estetisk tandvård | 200 | Complete | Desktop/mobile, light/dark |
| `/behandlingar/kirurgi/` | Kirurgi | 200 | Complete | Desktop/mobile, light/dark |
| `/behandlingar/kronor-och-broar/` | Kronor och broar | 200 | Complete | Desktop/mobile, light/dark |
| `/behandlingar/lagning-och-fyllning/` | Lagning och fyllning | 200 | Complete | Desktop/mobile, light/dark |
| `/behandlingar/rotfyllning/` | Rotfyllning | 200 | Complete | Desktop/mobile, light/dark |
| `/behandlingar/skalfasader/` | Skalfasader | 200 | Complete | Desktop/mobile, light/dark |
| `/behandlingar/specialisttandvard/` | Specialisttandvård | 200 | Complete | Desktop/mobile, light/dark |
| `/behandlingar/tandblekning/` | Tandblekning | 200 | Complete | Desktop/mobile, light/dark |
| `/behandlingar/tandextraktion/` | Tandextraktion | 200 | Complete | Desktop/mobile, light/dark |
| `/behandlingar/tandhygienist/` | Behandling hos tandhygienist | 200 | Complete | Desktop/mobile, light/dark |
| `/behandlingar/tandimplantat/` | Tandimplantat | 200 | Complete | Desktop/mobile, light/dark |
| `/behandlingar/tandreglering/` | Tandreglering | 200 | Complete | Desktop/mobile, light/dark |
| `/behandlingar/tandskydd/` | Tandskydd | 200 | Complete | Desktop/mobile, light/dark |
| `/behandlingar/tandstensborttagning/` | Tandstensborttagning | 200 | Complete | Desktop/mobile, light/dark |
| `/category/nyheter/` | Nyheter | 200 | Complete | Desktop/mobile, light/dark |
| `/del-av-dentalum/` | Bli en del av Dentalum | 200 | Complete | Desktop/mobile, light/dark |
| `/dentalum-som-arbetsgivare/` | Dentalum som arbetsgivare | 200 | Complete | Desktop/mobile, light/dark |
| `/dentalums-cookiepolicy/` | Dentalums cookiepolicy | 200 | Complete | Desktop/mobile, light/dark |
| `/dentalums-dataskyddspolicy/` | Dentalums dataskyddspolicy | 200 | Complete | Desktop/mobile, light/dark |
| `/kontakt/` | Kontakt | 200 | Complete | Desktop/mobile, light/dark |
| `/nyheter/` | Nyheter | 200 | Complete | Desktop/mobile, light/dark |
| `/nyheter/city-dental-blir-dentalum-tandvard-drottninggatan/` | City Dental blir Dentalum Tandvård Drottninggatan | 200 | Complete | Desktop/mobile, light/dark |
| `/nyheter/dentalum-expanderar-i-norrbotten/` | Dentalum expanderar i Norrbotten | 200 | Complete | Desktop/mobile, light/dark |
| `/nyheter/dentalum-far-ivo-tillstand/` | Dentalum Tandvård får tillstånd från IVO | 200 | Complete | Desktop/mobile, light/dark |
| `/om-oss/` | Vilka är Dentalum? | 200 | Complete | Desktop/mobile, light/dark |
| `/patientsakerhet/` | Patientsäkerhet | 200 | Complete | Desktop/mobile, light/dark |
| `/pressrelease/` | Press release | 200 | Complete | Desktop/mobile, light/dark |
| `/vara-kliniker/` | Våra kliniker | 200 | Complete | Desktop/mobile, light/dark |
| `/vart-hallbarhetsarbete/` | Vårt hållbarhetsarbete | 200 | Complete | Desktop/mobile, light/dark |
| `/vilka-ar-vi/` | Vilka är Dentalum? | 200 | Complete | Desktop/mobile, light/dark |
| `/author/ida/` | Tandvård som gör skillnad – med dig i centrum | 200 | Complete | Desktop/mobile, light/dark |
| `/behandlingar/akut-tandvard-atvidaberg/` | Akut tandvård i Åtvidaberg | 200 | Complete | Desktop/mobile, light/dark |
| `/behandlingar/akut-tandvard-ornskoldsvik/` | Akut tandvård i Örnsköldsvik | 200 | Complete | Desktop/mobile, light/dark |
| `/behandlingar/akut-tandvard-stockholm/` | Akut tandvård i Stockholm | 200 | Complete | Desktop/mobile, light/dark |
| `/behandlingar/allmantandvard/basundersokning/` | Basundersökning | 200 | Complete | Desktop/mobile, light/dark |
| `/behandlingar/skalfasader-stockholm/` | Skalfasader i Stockholm | 200 | Complete | Desktop/mobile, light/dark |
| `/behandlingar/tandblekning-stockholm/` | Tandblekning i Stockholm | 200 | Complete | Desktop/mobile, light/dark |
| `/behandlingar/tandhygienst-stockholm/` | Tandhygienst i Stockholm | 200 | Complete | Desktop/mobile, light/dark |
| `/behandlingar/tandimplantat-stockholm/` | Tandimplantat i Stockholm | 200 | Complete | Desktop/mobile, light/dark |
| `/behandlingar/tandreglering-stockholm/` | Tandreglering i Stockholm | 200 | Complete | Desktop/mobile, light/dark |
| `/cision-tag/dental-care/` | Dentalum acquires TandCity Sweden AB | 200 | Complete | Desktop/mobile, light/dark |
| `/cision-tag/dental-market/` | Dentalum Operations AB (publ) publishes half year report, January -June 2022 | 200 | Complete | Desktop/mobile, light/dark |
| `/cision-tag/dentalum-operations-ab-publ/` | Dentalum förvärvar TandCity Sweden AB | 200 | Complete | Desktop/mobile, light/dark |
| `/cision-tag/dentalum/` | Dentalum förvärvar TandCity Sweden AB | 200 | Complete | Desktop/mobile, light/dark |
| `/cision-tag/dentist/` | Dentalum acquires TandCity Sweden AB | 200 | Complete | Desktop/mobile, light/dark |
| `/cision-tag/dentistry/` | Dentalum acquires TandCity Sweden AB | 200 | Complete | Desktop/mobile, light/dark |
| `/cision-tag/q2/` | Dentalum Operations AB (publ) publishes half year report, January -June 2022 | 200 | Complete | Desktop/mobile, light/dark |
| `/cision-tag/tandcity/` | Dentalum förvärvar TandCity Sweden AB | 200 | Complete | Desktop/mobile, light/dark |
| `/cision-tag/tandlakare/` | Dentalum förvärvar TandCity Sweden AB | 200 | Complete | Desktop/mobile, light/dark |
| `/cision-tag/tandvard/` | Dentalum förvärvar TandCity Sweden AB | 200 | Complete | Desktop/mobile, light/dark |
| `/cision/beslut-fran-dentalums-arsstamma-2022/` | Beslut från Dentalums årsstämma 2022 | 200 | Complete | Desktop/mobile, light/dark |
| `/cision/beslut-fran-dentalums-arsstamma-2023/` | Beslut från Dentalums årsstämma 2023 | 200 | Complete | Desktop/mobile, light/dark |
| `/cision/correction-dentalum-operations-ab-publ-half-year-report-january-june-2022/` | Correction: Dentalum Operations AB (publ) half year report, January -June 2022 | 200 | Complete | Desktop/mobile, light/dark |
| `/cision/dentalum-acquires-abcare-tandvard-ab/` | Dentalum acquires ABCARE Tandvård AB | 200 | Complete | Desktop/mobile, light/dark |
| `/cision/dentalum-acquires-estetikcenter-goteborg-ab/` | Dentalum acquires Estetikcenter Göteborg AB | 200 | Complete | Desktop/mobile, light/dark |
| `/cision/dentalum-acquires-karlatandlakarna-and-malarklinken/` | Dentalum acquires Karlatandläkarna and Mälarklinken | 200 | Complete | Desktop/mobile, light/dark |
| `/cision/dentalum-acquires-novo-dental/` | Dentalum acquires NOVO DENTAL | 200 | Complete | Desktop/mobile, light/dark |
| `/cision/dentalum-acquires-skelleftea-tandvard-ab/` | Dentalum acquires Skellefteå Tandvård AB | 200 | Complete | Desktop/mobile, light/dark |
| `/cision/dentalum-acquires-solna-dental-and-solna-dental-arenatandlakarna/` | Dentalum acquires Solna Dental and Solna Dental Arenatandläkarna | 200 | Complete | Desktop/mobile, light/dark |
| `/cision/dentalum-acquires-stanga-tandklinik-and-svarta-tandklinik-in-ostergotland/` | Dentalum acquires Stångå Tandklinik and Svartå Tandklinik in Östergötland | 200 | Complete | Desktop/mobile, light/dark |
| `/cision/dentalum-acquires-swedish-dental/` | Dentalum acquires Swedish Dental | 200 | Complete | Desktop/mobile, light/dark |
| `/cision/dentalum-acquires-tandcenter-umea-and-tandcenter-lovanger/` | Dentalum acquires Tandcenter Umeå and Tandcenter Lövånger | 200 | Complete | Desktop/mobile, light/dark |
| `/cision/dentalum-acquires-tandcity-sweden-ab/` | Dentalum acquires TandCity Sweden AB | 200 | Complete | Desktop/mobile, light/dark |
| `/cision/dentalum-acquires-tandlakarhuset-enkoping/` | Dentalum acquires Tandläkarhuset Enköping | 200 | Complete | Desktop/mobile, light/dark |
| `/cision/dentalum-acquires-tareqs-klinik-ab-in-hultsfred/` | Dentalum acquires Tareqs Klinik AB in Hultsfred | 200 | Complete | Desktop/mobile, light/dark |
| `/cision/dentalum-announces-change-in-executive-managment/` | Dentalum announces change in Executive Managment | 200 | Complete | Desktop/mobile, light/dark |
| `/cision/dentalum-considers-new-issue-of-shares-and-presents-financial-targets-for-the-group-as-well-as-plans-for-public-listing/` | Dentalum considers new issue of shares and presents financial targets for the group as well as plans for public listing | 200 | Complete | Desktop/mobile, light/dark |
| `/cision/dentalum-emitterar-framgangsrikt-ytterligare-obligationer-om-100-miljoner-kronor/` | Dentalum emitterar framgångsrikt ytterligare obligationer om 100 miljoner kronor | 200 | Complete | Desktop/mobile, light/dark |
| `/cision/dentalum-enters-into-a-term-sheet-with-a-leading-nordic-bank-to-refinance-the-companys-senior-bond/` | Dentalum enters into a term sheet with a leading Nordic bank to refinance the Company's Senior bond | 200 | Complete | Desktop/mobile, light/dark |
| `/cision/dentalum-etablerar-sig-i-jamtland-forvarvar-cura-tandvard-i-ostersund/` | Dentalum etablerar sig i Jämtland – förvärvar Cura Tandvård i Östersund | 200 | Complete | Desktop/mobile, light/dark |
| `/cision/dentalum-fortsatter-tillvaxtresan-genom-forvarvet-av-tandlakare-rikard-wennberg-i-karlstad/` | Dentalum fortsätter tillväxtresan genom förvärvet av Tandläkare Rikard Wennberg i Karlstad | 200 | Complete | Desktop/mobile, light/dark |
| `/cision/dentalum-forvarvar-abcare-tandvard-ab/` | Dentalum förvärvar ABCARE Tandvård AB | 200 | Complete | Desktop/mobile, light/dark |
| `/cision/dentalum-forvarvar-estetikcenter-goteborg-ab/` | Dentalum förvärvar Estetikcenter Göteborg AB | 200 | Complete | Desktop/mobile, light/dark |
| `/cision/dentalum-forvarvar-karlatandlakarna-och-malarkliniken/` | Dentalum förvärvar Karlatandläkarna och Mälarkliniken | 200 | Complete | Desktop/mobile, light/dark |
| `/cision/dentalum-forvarvar-novo-dental/` | Dentalum förvärvar NOVO DENTAL | 200 | Complete | Desktop/mobile, light/dark |
| `/cision/dentalum-forvarvar-skelleftea-tandvard-ab/` | Dentalum förvärvar Skellefteå Tandvård AB | 200 | Complete | Desktop/mobile, light/dark |
| `/cision/dentalum-forvarvar-solna-dental-och-solna-dental-arenatandlakarna/` | Dentalum förvärvar Solna Dental och Solna Dental Arenatandläkarna | 200 | Complete | Desktop/mobile, light/dark |
| `/cision/dentalum-forvarvar-stanga-tandklinik-och-svarta-tandklinik-i-ostergotland/` | Dentalum förvärvar Stångå Tandklinik och Svartå Tandklinik i Östergötland | 200 | Complete | Desktop/mobile, light/dark |
| `/cision/dentalum-forvarvar-swedish-dental/` | Dentalum förvärvar Swedish Dental | 200 | Complete | Desktop/mobile, light/dark |
| `/cision/dentalum-forvarvar-tandcenter-umea-och-tandcenter-lovanger/` | Dentalum förvärvar Tandcenter Umeå och Tandcenter Lövånger | 200 | Complete | Desktop/mobile, light/dark |
| `/cision/dentalum-forvarvar-tandcity-sweden-ab/` | Dentalum förvärvar TandCity Sweden AB | 200 | Complete | Desktop/mobile, light/dark |
| `/cision/dentalum-forvarvar-tandlakarhuset-enkoping/` | Dentalum förvärvar Tandläkarhuset Enköping | 200 | Complete | Desktop/mobile, light/dark |
| `/cision/dentalum-forvarvar-tareqs-klinik-ab-i-hultsfred/` | Dentalum förvärvar Tareqs Klinik AB i Hultsfred | 200 | Complete | Desktop/mobile, light/dark |
| `/cision/dentalum-group-ab-har-framgangsrikt-genomfort-en-nyemission-och-tillfors-harigenom-ca-153-miljoner-kronor/` | Dentalum Group AB har framgångsrikt genomfört en nyemission och tillförs härigenom ca 153 miljoner kronor | 200 | Complete | Desktop/mobile, light/dark |
| `/cision/dentalum-group-ab-har-framgangsrikt-genomfort-en-riktad-nyemission-och-tillfors-harigenom-cirka-170-miljoner-sek/` | Dentalum Group AB har framgångsrikt genomfört en riktad nyemission och tillförs härigenom cirka 170 miljoner SEK | 200 | Complete | Desktop/mobile, light/dark |
| `/cision/dentalum-group-ab-has-successfully-completed-a-directed-new-share-issue-raising-proceeds-of-approximately-sek-170-million/` | Dentalum Group AB has successfully completed a directed new share issue raising proceeds of approximately SEK 170 million | 200 | Complete | Desktop/mobile, light/dark |
| `/cision/dentalum-has-a-positive-view-on-refinancing-possibilities/` | Dentalum has a positive view on refinancing possibilities | 200 | Complete | Desktop/mobile, light/dark |
| `/cision/dentalum-ingar-ett-term-sheet-med-nordisk-storbank-for-refinansiering-av-bolagets-seniora-obligation/` | Dentalum ingår ett term sheet med nordisk storbank för refinansiering av bolagets seniora obligation | 200 | Complete | Desktop/mobile, light/dark |
| `/cision/dentalum-ingar-langsiktigt-finansiellt-partnerskap-med-danske-bank-och-fortsatter-sin-expansion-i-sverige/` | Dentalum ingår långsiktigt finansiellt partnerskap med Danske Bank och fortsätter sin expansion i Sverige | 200 | Complete | Desktop/mobile, light/dark |
| `/cision/dentalum-inleder-samarbete-med-erik-lennartsson-genom-forvarvet-av-dentalakademin/` | Dentalum inleder samarbete med Erik Lennartsson genom förvärvet av Dentalakademin | 200 | Complete | Desktop/mobile, light/dark |
| `/cision/dentalum-is-considering-raising-capital/` | Dentalum is considering raising capital | 200 | Complete | Desktop/mobile, light/dark |
| `/cision/dentalum-is-contemplating-a-subsequent-bond-issue-of-approximately-sek-100-million-and-will-receive-sek-35-million-through-an-equity-injection/` | Dentalum is contemplating a subsequent bond issue of approximately SEK 100 million and will receive SEK 35 million through an equity injection | 200 | Complete | Desktop/mobile, light/dark |
| `/cision/dentalum-meddelar-forandring-i-ledningsgruppen/` | Dentalum meddelar förändring i ledningsgruppen | 200 | Complete | Desktop/mobile, light/dark |
| `/cision/dentalum-och-skapa-i-ett-unikt-samarbete-for-framtidens-tandvard/` | Dentalum och SKaPa i ett unikt samarbete för framtidens tandvård | 200 | Complete | Desktop/mobile, light/dark |
| `/cision/dentalum-operations-ab-publ-delarsrapport-for-fjarde-kvartalet-2020/` | Dentalum Operations AB (publ.) delårsrapport för fjärde kvartalet 2020 | 200 | Complete | Desktop/mobile, light/dark |
| `/cision/dentalum-operations-ab-publ-interim-report-second-quarter-and-january-june-2023/` | Dentalum Operations AB (publ) Interim report second quarter and January-June 2023 | 200 | Complete | Desktop/mobile, light/dark |
| `/cision/dentalum-operations-ab-publ-maximum-sek-600000000-senior-secured-callable-fixed-rate-bonds-2020-2023-med-isin-se0013914462/` | Dentalum Operations AB (publ) maximum SEK 600,000,000 senior secured callable fixed rate bonds 2020/2023 med ISIN SE0013914462 | 200 | Complete | Desktop/mobile, light/dark |
| `/cision/dentalum-operations-ab-publ-maximum-sek-600000000-senior-secured-callable-fixed-rate-bonds-2020-2023-with-isin-se0013914462/` | Dentalum Operations AB (publ) maximum SEK 600,000,000 senior secured callable fixed rate bonds 2020/2023 with ISIN SE0013914462 | 200 | Complete | Desktop/mobile, light/dark |
| `/cision/dentalum-operations-ab-publ-publicerar-delarsrapport-for-andra-kvartalet-2021/` | Dentalum Operations AB (publ) publicerar delårsrapport för andra kvartalet 2021 | 200 | Complete | Desktop/mobile, light/dark |
| `/cision/dentalum-operations-ab-publ-publicerar-delarsrapport-for-andra-kvartalet-2022/` | Dentalum Operations AB (publ) publicerar delårsrapport för andra kvartalet 2022 | 200 | Complete | Desktop/mobile, light/dark |
| `/cision/dentalum-operations-ab-publ-publicerar-delarsrapport-for-andra-kvartalet-och-for-perioden-januari-juni-2023/` | Dentalum Operations AB (publ) publicerar delårsrapport för andra kvartalet och för perioden januari-juni 2023 | 200 | Complete | Desktop/mobile, light/dark |
| `/cision/dentalum-operations-ab-publ-publicerar-delarsrapport-for-fjarde-kvartalet-2021/` | Dentalum Operations AB (publ) publicerar delårsrapport för fjärde kvartalet 2021 | 200 | Complete | Desktop/mobile, light/dark |
| `/cision/dentalum-operations-ab-publ-publicerar-delarsrapport-for-fjarde-kvartalet-och-bokslutskommunike-2022/` | Dentalum Operations AB (publ) publicerar delårsrapport för fjärde kvartalet och bokslutskommuniké 2022 | 200 | Complete | Desktop/mobile, light/dark |
| `/cision/dentalum-operations-ab-publ-publicerar-delarsrapport-for-forsta-kvartalet-2021/` | Dentalum Operations AB (publ.) publicerar delårsrapport för första kvartalet 2021 | 200 | Complete | Desktop/mobile, light/dark |
| `/cision/dentalum-operations-ab-publ-publicerar-delarsrapport-for-forsta-kvartalet-2022/` | Dentalum Operations AB (publ) publicerar delårsrapport för första kvartalet 2022 | 200 | Complete | Desktop/mobile, light/dark |
| `/cision/dentalum-operations-ab-publ-publicerar-delarsrapport-for-tredje-kvartalet-2021/` | Dentalum Operations AB (publ) publicerar delårsrapport för tredje kvartalet 2021 | 200 | Complete | Desktop/mobile, light/dark |
| `/cision/dentalum-operations-ab-publ-publicerar-idag-arsredovisning-for-2021/` | Financial reports | 200 | Complete | Desktop/mobile, light/dark |
| `/cision/dentalum-operations-ab-publ-publicerar-obligationsprospekt-i-samband-med-att-bolagets-foretagsobligation-upptas-till-handel-pa-nasdaq-stockholm/` | Dentalum Operations AB (publ) publicerar obligationsprospekt i samband med att bolagets företagsobligation upptas till handel på Nasdaq Stockholm | 200 | Complete | Desktop/mobile, light/dark |
| `/cision/dentalum-operations-ab-publ-publishes-half-year-report-january-june-2022/` | Dentalum Operations AB (publ) publishes half year report, January -June 2022 | 200 | Complete | Desktop/mobile, light/dark |
| `/cision/dentalum-operations-ab-publ-publishes-interim-report-for-the-first-quarter-2022/` | Dentalum Operations AB (publ) publishes interim report for the first quarter 2022 | 200 | Complete | Desktop/mobile, light/dark |
| `/cision/dentalum-operations-ab-publ-publishes-interim-report-for-the-fourth-quarter-2021/` | Dentalum Operations AB (publ) publishes Interim report for the fourth quarter 2021 | 200 | Complete | Desktop/mobile, light/dark |
| `/cision/dentalum-operations-ab-publ-publishes-prospectus-for-the-admission-to-trading-of-its-senior-secured-fixed-rate-bonds-on-nasdaq-stockholm/` | Dentalum Operations AB (publ) publishes prospectus for the admission to trading of its Senior Secured Fixed Rate Bonds on Nasdaq Stockholm | 200 | Complete | Desktop/mobile, light/dark |
| `/cision/dentalum-operations-ab-publ-publishes-q1-interim-report/` | Dentalum Operations AB (publ.) publishes Q1 Interim Report | 200 | Complete | Desktop/mobile, light/dark |
| `/cision/dentalum-operations-ab-publ-publishes-q2-interim-report/` | Dentalum Operations AB (publ) publishes Q2 Interim Report | 200 | Complete | Desktop/mobile, light/dark |
| `/cision/dentalum-operations-ab-publ-publishes-q3-interim-report/` | Dentalum Operations AB (publ) publishes Q3 Interim Report | 200 | Complete | Desktop/mobile, light/dark |
| `/cision/dentalum-operations-ab-publ-publishes-the-first-quarter-report-2023-2/` | Dentalum Operations AB (publ) publishes the first quarter report 2023 | 200 | Complete | Desktop/mobile, light/dark |
| `/cision/dentalum-operations-ab-publ-publishes-the-first-quarter-report-2023/` | Dentalum Operations AB (publ) publishes the first quarter report 2023 | 200 | Complete | Desktop/mobile, light/dark |
| `/cision/dentalum-operations-ab-publ-publishes-the-fourth-quarter-and-year-end-report-2022/` | Dentalum Operations AB (publ) publishes the fourth quarter and year-end report 2022 | 200 | Complete | Desktop/mobile, light/dark |
| `/cision/dentalum-operations-ab-publ-publishes-today-the-annual-report-for-2021/` | Financial reports | 200 | Complete | Desktop/mobile, light/dark |
| `/cision/dentalum-operations-ab-publ-q3-rapport/` | Dentalum Operations AB (publ) Q3 rapport | 200 | Complete | Desktop/mobile, light/dark |
| `/cision/dentalum-operations-ab-publ-q3-report/` | Dentalum Operations AB (publ) Q3 report | 200 | Complete | Desktop/mobile, light/dark |
| `/cision/dentalum-operations-ab-publ-q4-interim-report/` | Dentalum Operations AB (publ.) Q4 Interim Report | 200 | Complete | Desktop/mobile, light/dark |
| `/cision/dentalum-overvager-att-genomfora-en-kapitalanskaffning/` | Dentalum överväger att genomföra en kapitalanskaffning | 200 | Complete | Desktop/mobile, light/dark |
| `/cision/dentalum-overvager-emission-av-ytterligare-foretagsobligationer-om-cirka-100-miljoner-kronor-och-aktieagartillskott-om-35-miljoner-kronor-tillfors/` | Dentalum överväger emission av ytterligare företagsobligationer om cirka 100 miljoner kronor och aktieägartillskott om 35 miljoner kronor tillförs | 200 | Complete | Desktop/mobile, light/dark |
| `/cision/dentalum-overvager-nyemission-av-aktier-och-offentliggor-finansiella-mal-for-gruppen-samt-noteringsplaner/` | Dentalum överväger nyemission av aktier och offentliggör finansiella mål för gruppen samt noteringsplaner | 200 | Complete | Desktop/mobile, light/dark |
| `/cision/dentalum-partners-up-with-erik-lennartsson-through-the-acquisition-of-dentalakademin/` | Dentalum partners up with Erik Lennartsson through the acquisition of Dentalakademin | 200 | Complete | Desktop/mobile, light/dark |
| `/cision/dentalum-publicerar-arsredovisningen-for-2020/` | Dentalum publicerar årsredovisningen för 2020 | 200 | Complete | Desktop/mobile, light/dark |
| `/cision/dentalum-publicerar-arsredovisningen-for-2022/` | Dentalum publicerar årsredovisningen för 2022 | 200 | Complete | Desktop/mobile, light/dark |
| `/cision/dentalum-publishes-annual-report-for-2022/` | Dentalum publishes Annual Report for 2022 | 200 | Complete | Desktop/mobile, light/dark |
| `/cision/dentalum-publishes-the-annual-report-for-2020/` | Dentalum publishes the Annual Report for 2020 | 200 | Complete | Desktop/mobile, light/dark |
| `/cision/dentalum-recruits-a-chief-dental-officer-and-medical-manager/` | Dentalum recruits a Chief Dental Officer and Medical Manager | 200 | Complete | Desktop/mobile, light/dark |
| `/cision/dentalum-rekryterar-en-cheftandlakare-och-odontologiskt-ansvarig/` | Dentalum rekryterar en Cheftandläkare och Odontologiskt Ansvarig | 200 | Complete | Desktop/mobile, light/dark |
| `/cision/dentalum-ser-positivt-pa-refinansieringsmojligheter/` | Dentalum ser positivt på refinansieringsmöjligheter | 200 | Complete | Desktop/mobile, light/dark |
| `/cision/dentalum-signs-a-facility-agreement-with-danske-bank-for-refinancing-of-the-companys-senior-bond/` | Dentalum signs a facility agreement with Danske Bank for refinancing of the Company's senior bond | 200 | Complete | Desktop/mobile, light/dark |
| `/cision/dentalum-starker-investerarkollektiv-for-den-fortsatta-tillvaxtresan/` | Dentalum stärker investerarkollektiv för den fortsatta tillväxtresan | 200 | Complete | Desktop/mobile, light/dark |
| `/cision/dentalum-starker-ledningsgruppen-med-en-ny-coo/` | Dentalum stärker ledningsgruppen med en ny COO | 200 | Complete | Desktop/mobile, light/dark |
| `/cision/dentalum-starker-styrelsen-med-mikael-lonn-som-ny-styrelseledamot/` | Dentalum stärker styrelsen med Mikael Lönn som ny styrelseledamot | 200 | Complete | Desktop/mobile, light/dark |
| `/cision/dentalum-starker-teamet-infor-kommande-notering/` | Dentalum stärker teamet inför kommande notering | 200 | Complete | Desktop/mobile, light/dark |
| `/cision/dentalum-strengthens-the-board-of-directors-with-mikael-lonn-as-new-board-member/` | Dentalum strengthens the Board of Directors with Mikael Lönn as new board member | 200 | Complete | Desktop/mobile, light/dark |
| `/cision/dentalum-strengthens-the-management-team-with-a-new-coo/` | Dentalum strengthens the management team with a new COO | 200 | Complete | Desktop/mobile, light/dark |
| `/cision/dentalum-strengthens-the-team-for-the-upcoming-ipo/` | Dentalum strengthens the team for the upcoming IPO | 200 | Complete | Desktop/mobile, light/dark |
| `/cision/dentalum-successfully-issues-subsequent-bonds-of-sek-100m/` | Dentalum successfully issues subsequent bonds of SEK 100m | 200 | Complete | Desktop/mobile, light/dark |
| `/cision/dentalum-undertecknar-laneavtal-med-danske-bank-for-refinansiering-av-bolagets-seniora-obligation/` | Dentalum undertecknar låneavtal med Danske Bank för refinansiering av bolagets seniora obligation | 200 | Complete | Desktop/mobile, light/dark |
| `/cision/esmaeilzadeh-holding-ab-increases-its-shareholding-in-dentalum-group-ab/` | Esmaeilzadeh Holding AB increases its shareholding in Dentalum Group AB | 200 | Complete | Desktop/mobile, light/dark |
| `/cision/esmaeilzadeh-holding-ab-utokar-sitt-innehav-i-dentalum-group-ab/` | Esmaeilzadeh Holding AB utökar sitt innehav i Dentalum Group AB | 200 | Complete | Desktop/mobile, light/dark |
| `/cision/forsta-vetenskapliga-granskningen-av-privat-tandvard-i-sverige-dentalum-lanserar-nytt-verktyg-for-systematisk-kvalitetsuppfoljning/` | Första vetenskapliga granskningen av privat tandvård i Sverige – Dentalum lanserar nytt verktyg för systematisk kvalitetsuppföljning | 200 | Complete | Desktop/mobile, light/dark |
| `/cision/noel-abdayem-blir-en-del-av-dentalums-investeringskommitte/` | Noel Abdayem blir en del av Dentalums investeringskommitté | 200 | Complete | Desktop/mobile, light/dark |
| `/cision/noel-abdayem-joins-dentalums-investment-committee/` | Noel Abdayem joins Dentalum’s Investment Committee | 200 | Complete | Desktop/mobile, light/dark |
| `/cision/operativ-chef-lamnar-dentalum-operations-ab-publ/` | Operativ Chef lämnar Dentalum Operations AB (publ) | 200 | Complete | Desktop/mobile, light/dark |
| `/cision/rattelse-dentalum-operations-ab-publ-delarsrapport-for-andra-kvartalet-2022/` | Rättelse: Dentalum Operations AB (publ), delårsrapport för andra kvartalet 2022 | 200 | Complete | Desktop/mobile, light/dark |
| `/cision/resolutions-by-dentalums-annual-general-meeting-2022/` | Resolutions by Dentalums Annual General Meeting 2022 | 200 | Complete | Desktop/mobile, light/dark |
| `/cision/resolutions-by-dentalums-annual-general-meeting-2023/` | Resolutions by Dentalums Annual General Meeting 2023 | 200 | Complete | Desktop/mobile, light/dark |
| `/cision/roosgruppen-ny-majoritetsagare-i-dentalum/` | RoosGruppen ny majoritetsägare i Dentalum | 200 | Complete | Desktop/mobile, light/dark |
| `/cision/the-chief-operating-officer-leaves-dentalum-operations-ab-publ/` | The Chief Operating Officer leaves Dentalum Operations AB (publ) | 200 | Complete | Desktop/mobile, light/dark |
| `/financial-calendar/` | Financial calendar | 200 | Complete | Desktop/mobile, light/dark |
| `/financial-reports/` | Financial reports | 200 | Complete | Desktop/mobile, light/dark |
| `/investor-reports/` | Investor reports | 200 | Complete | Desktop/mobile, light/dark |
| `/kliniker/` | Våra kliniker | 200 | Complete | Desktop/mobile, light/dark |
| `/kliniker/dalarna/gylle-tandvard/` | Gylle Tandvård | 200 | Complete | Desktop/mobile, light/dark |
| `/kliniker/dalarna/ludvikatandlakarna/` | Ludvikatandläkarna | 200 | Complete | Desktop/mobile, light/dark |
| `/kliniker/halland/tandlakarna-stenberg/` | Tandläkarna Stenberg | 200 | Complete | Desktop/mobile, light/dark |
| `/kliniker/jamtland/cura-tandvard/` | Cura Tandvård | 200 | Complete | Desktop/mobile, light/dark |
| `/kliniker/jamtland/tandlakare-annelie-alenius/` | Tandläkare Annelie Alenius | 200 | Complete | Desktop/mobile, light/dark |
| `/kliniker/jonkoping/vesalis-dental/` | Vesalis Dental | 200 | Complete | Desktop/mobile, light/dark |
| `/kliniker/kalmar/hultsfreds-tandvard-oskargatan/` | Hultsfreds Tandvård – Oskargatan | 200 | Complete | Desktop/mobile, light/dark |
| `/kliniker/kalmar/hultsfreds-tandvard-tors-plan/` | Hultsfreds Tandvård – Tors Plan | 200 | Complete | Desktop/mobile, light/dark |
| `/kliniker/norrbotten/kungsbrotandlakarna-boden/` | Kungsbrotandläkarna – Boden | 200 | Complete | Desktop/mobile, light/dark |
| `/kliniker/norrbotten/kungsbrotandlakarna-savast/` | Kungsbrotandläkarna – Sävast | 200 | Complete | Desktop/mobile, light/dark |
| `/kliniker/ostergotland/dentalum-atvidaberg/` | Dentalum Åtvidaberg | 200 | Complete | Desktop/mobile, light/dark |
| `/kliniker/ostergotland/stanga-tandklinik/` | Stångå Tandklinik | 200 | Complete | Desktop/mobile, light/dark |
| `/kliniker/ostergotland/svarta-tandklinik/` | Svartå Tandklinik | 200 | Complete | Desktop/mobile, light/dark |
| `/kliniker/skane/alfa-tandvardskliniken/` | Alfa Tandvårdskliniken | 200 | Complete | Desktop/mobile, light/dark |
| `/kliniker/skane/tandcity/` | TandCity | 200 | Complete | Desktop/mobile, light/dark |
| `/kliniker/stockholm/city-dental/` | Dentalum Drottninggatan | 200 | Complete | Desktop/mobile, light/dark |
| `/kliniker/stockholm/dentalakademin/` | Dentalakademin | 200 | Complete | Desktop/mobile, light/dark |
| `/kliniker/stockholm/dentalum-drottninggatan/` | Dentalum Drottninggatan | 200 | Complete | Desktop/mobile, light/dark |
| `/kliniker/stockholm/karlatandlakarna/` | Karlatandläkarna | 200 | Complete | Desktop/mobile, light/dark |
| `/kliniker/stockholm/malarkliniken/` | Mälarkliniken | 200 | Complete | Desktop/mobile, light/dark |
| `/kliniker/stockholm/nacka-tandvardsteam/` | Nacka Tandvårdsteam | 200 | Complete | Desktop/mobile, light/dark |
| `/kliniker/stockholm/novo-dental/` | Novo Dental | 200 | Complete | Desktop/mobile, light/dark |
| `/kliniker/stockholm/solna-dental-arenatandlakarna/` | Solna Dental – Arenatandläkarna | 200 | Complete | Desktop/mobile, light/dark |
| `/kliniker/stockholm/solna-dental-huvudstatandlakarna/` | Solna Dental – Huvudstatandläkarna | 200 | Complete | Desktop/mobile, light/dark |
| `/kliniker/stockholm/sthlm-dental-sodermalm/` | Sthlm Dental Södermalm | 200 | Complete | Desktop/mobile, light/dark |
| `/kliniker/stockholm/swedish-dental/` | Swedish Dental | 200 | Complete | Desktop/mobile, light/dark |
| `/kliniker/uppsala/tandlakarhuset-enkoping/` | Tandläkarhuset Enköping | 200 | Complete | Desktop/mobile, light/dark |
| `/kliniker/varmland/tandlakare-wennberg/` | Tandläkare Wennberg | 200 | Complete | Desktop/mobile, light/dark |
| `/kliniker/vasterbotten/lovanger-tandvard/` | Lövånger Tandvård | 200 | Complete | Desktop/mobile, light/dark |
| `/kliniker/vasterbotten/skelleftea-tandvard/` | Skellefteå Tandvård | 200 | Complete | Desktop/mobile, light/dark |
| `/kliniker/vasterbotten/tandcenter-umea/` | Tandcenter Umeå | 200 | Complete | Desktop/mobile, light/dark |
| `/kliniker/vasternorrland/dentalum-ornskoldsvik/` | Dentalum Örnsköldsvik | 200 | Complete | Desktop/mobile, light/dark |
| `/kliniker/vastra-gotaland/boras-tandvard/` | Borås Tandvård | 200 | Complete | Desktop/mobile, light/dark |
| `/kliniker/vastra-gotaland/estetikcenter-goteborg/` | Estetikcenter | 200 | Complete | Desktop/mobile, light/dark |
| `/kliniker/vastra-gotaland/kungsfors-tandvard/` | Kungsfors Tandvård | 200 | Complete | Desktop/mobile, light/dark |
| `/nyheter/tiotandvard-nya-regler-fran-2026/` | Tiotandvård – Nya regler från 2026 | 200 | Complete | Desktop/mobile, light/dark |
| `/pressrelease/page/2/` | Press release | 200 | Complete | Desktop/mobile, light/dark |
| `/priser/` | Priser | 200 | Complete | Desktop/mobile, light/dark |
| `/team/` | Teamet på Dentalum | 200 | Complete | Desktop/mobile, light/dark |
| `/behandlingar/akut-tandvard-ornskoldsvik/+46660213808/` | Akut tandvård i Örnsköldsvik | 200 | Complete | Desktop/mobile, light/dark |
| `/kliniker/dalarna/` | Tandläkare Dalarna | 200 | Complete | Desktop/mobile, light/dark |
| `/kliniker/halland/` | Tandläkare Halland | 200 | Complete | Desktop/mobile, light/dark |
| `/kliniker/jamtland/` | Tandläkare Jämtland | 200 | Complete | Desktop/mobile, light/dark |
| `/kliniker/jonkoping/` | Tandläkare Jönköping | 200 | Complete | Desktop/mobile, light/dark |
| `/kliniker/kalmar/` | Tandläkare Kalmar | 200 | Complete | Desktop/mobile, light/dark |
| `/kliniker/norrbotten/` | Tandläkare Norrbotten | 200 | Complete | Desktop/mobile, light/dark |
| `/kliniker/ostergotland/` | Tandläkare Östergötland | 200 | Complete | Desktop/mobile, light/dark |
| `/kliniker/skane/` | Tandläkare Skåne | 200 | Complete | Desktop/mobile, light/dark |
| `/kliniker/stockholm/` | Tandläkare Stockholm | 200 | Complete | Desktop/mobile, light/dark |
| `/kliniker/uppsala/` | Tandläkare Uppsala | 200 | Complete | Desktop/mobile, light/dark |
| `/kliniker/varmland/` | Tandläkare Värmland | 200 | Complete | Desktop/mobile, light/dark |
| `/kliniker/vasterbotten/` | Tandläkare Västerbotten | 200 | Complete | Desktop/mobile, light/dark |
| `/kliniker/vasternorrland/` | Tandläkare Västernorrland | 200 | Complete | Desktop/mobile, light/dark |
| `/kliniker/vastra-gotaland/` | Tandläkare Västra Götaland | 200 | Complete | Desktop/mobile, light/dark |
| `/pressrelease/page/3/` | Press release | 200 | Complete | Desktop/mobile, light/dark |
| `/pressrelease/page/4/` | Press release | 200 | Complete | Desktop/mobile, light/dark |
| `/pressrelease/page/5/` | Press release | 200 | Complete | Desktop/mobile, light/dark |
| `/sidkarta/` | Searchable page directory | New | Complete | Desktop/mobile, light/dark |

## Delivery

The prebuilt website is `dist/`; source generator, assets, original audit snapshots and reports are included. Run `npm start` to serve it locally. Publication was blocked by absent Sites source-workflow helpers; no original Dentalum site or hosting was modified.
