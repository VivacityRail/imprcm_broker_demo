--
-- PostgreSQL database dump
--

-- Dumped from database version 10.14 (Ubuntu 10.14-1.pgdg18.04+1)
-- Dumped by pg_dump version 12.0

-- Started on 2020-10-10 19:47:47

SET statement_timeout = 0;
SET lock_timeout = 0;
SET idle_in_transaction_session_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SELECT pg_catalog.set_config('search_path', '', false);
SET check_function_bodies = false;
SET xmloption = content;
SET client_min_messages = warning;
SET row_security = off;

--
-- TOC entry 2962 (class 0 OID 17519)
-- Dependencies: 202
-- Data for Name: ugms_s_and_c_summary; Type: TABLE DATA; Schema: public; Owner: pete
--

COPY public.ugms_s_and_c_summary (sample_date, left_top_35m_sd_mm, right_top_35m_sd_mm, mean_top_70m_sd_mm, twist_3m_sd_mm, pseudo_align_35m_sd_mm, pseudo_align_70m_sd_mm, unique_id, direction_of_travel, main_elr, main_track_id, miles_decimal_from, miles_plus_yards_from, miles_cln_chains_from, miles_decimal_to, miles_plus_yards_to, miles_cln_chains_to) FROM stdin;
2019-01-06	0.893157184	1.00537491	\N	1.50681102	7.04370022	\N	16898	-1	MLN1	1200	34.3268509	 034+0575	\N	34.4039001	 034+0711	\N
2019-01-06	0.870637298	0.998201251	\N	1.41648102	6.55993223	\N	17092	-1	MLN1	1200	32.4717598	 032+0830	\N	32.5599976	 032+0986	\N
2019-01-06	2.58083558	2.78477263	\N	2.02576661	3.50355268	\N	16898	1	MLN1	1200	1.32778203	 001+0577	\N	1.40483403	 001+0713	\N
2019-01-06	2.22651172	2.40211082	\N	1.91689885	4.1739049	\N	17092	1	MLN1	1200	3.17168999	 003+0302	\N	3.25992703	 003+0457	\N
2019-01-08	0.893157184	1.00537491	\N	1.50681102	7.04370022	\N	16898	-1	MLN1	1200	34.3268509	 034+0575	\N	34.4039001	 034+0711	\N
2019-01-08	0.870637298	0.998201251	\N	1.41648102	6.55993223	\N	17092	-1	MLN1	1200	32.4717598	 032+0830	\N	32.5599976	 032+0986	\N
2019-01-08	2.71048665	2.92367578	\N	2.02576661	3.50355268	\N	16898	1	MLN1	1200	1.32778203	 001+0577	\N	1.40483403	 001+0713	\N
2019-01-08	2.3152597	2.49719286	\N	1.91689885	4.1739049	\N	17092	1	MLN1	1200	3.17168999	 003+0302	\N	3.25992703	 003+0457	\N
2019-01-10	0.893157184	1.00537491	\N	1.50681102	7.04370022	\N	16898	-1	MLN1	1200	34.3268509	 034+0575	\N	34.4039001	 034+0711	\N
2019-01-10	0.870637298	0.998201251	\N	1.41648102	6.55993223	\N	17092	-1	MLN1	1200	32.4717598	 032+0830	\N	32.5599976	 032+0986	\N
2019-01-10	2.84803367	3.0710361	\N	2.02576661	3.50355268	\N	16898	1	MLN1	1200	1.32778203	 001+0577	\N	1.40483403	 001+0713	\N
2019-01-10	2.40400863	2.59227395	\N	1.91689885	4.1739049	\N	17092	1	MLN1	1200	3.17168999	 003+0302	\N	3.25992703	 003+0457	\N
2019-01-12	0.893157184	1.00537491	\N	1.50681102	7.04370022	\N	16898	-1	MLN1	1200	34.3268509	 034+0575	\N	34.4039001	 034+0711	\N
2019-01-12	0.870637298	0.998201251	\N	1.41648102	6.55993223	\N	17092	-1	MLN1	1200	32.4717598	 032+0830	\N	32.5599976	 032+0986	\N
2019-01-12	2.99395704	3.22737026	\N	2.02576661	3.50355268	\N	16898	1	MLN1	1200	1.32778203	 001+0577	\N	1.40483403	 001+0713	\N
2019-01-12	2.49275637	2.68735361	\N	1.91689885	4.1739049	\N	17092	1	MLN1	1200	3.17168999	 003+0302	\N	3.25992703	 003+0457	\N
2019-01-14	0.893157184	1.00537491	\N	1.50681102	7.04370022	\N	16898	-1	MLN1	1200	34.3268509	 034+0575	\N	34.4039001	 034+0711	\N
2019-01-14	0.870637298	0.998201251	\N	1.41648102	6.55993223	\N	17092	-1	MLN1	1200	32.4717598	 032+0830	\N	32.5599976	 032+0986	\N
2019-01-14	3.14876676	3.39322495	\N	2.02576661	3.50355268	\N	16898	1	MLN1	1200	1.32778203	 001+0577	\N	1.40483403	 001+0713	\N
2019-01-14	2.58150601	2.78243279	\N	1.91689885	4.1739049	\N	17092	1	MLN1	1200	3.17168999	 003+0302	\N	3.25992703	 003+0457	\N
2019-01-16	0.893157184	1.00537491	\N	1.50681102	7.04370022	\N	16898	-1	MLN1	1200	34.3268509	 034+0575	\N	34.4039001	 034+0711	\N
2019-01-16	0.870637298	0.998201251	\N	1.41648102	6.55993223	\N	17092	-1	MLN1	1200	32.4717598	 032+0830	\N	32.5599976	 032+0986	\N
2019-01-16	3.31300282	3.56918001	\N	2.02576661	3.50355268	\N	16898	1	MLN1	1200	1.32778203	 001+0577	\N	1.40483403	 001+0713	\N
2019-01-16	2.67025352	2.87751198	\N	1.91689885	4.1739049	\N	17092	1	MLN1	1200	3.17168999	 003+0302	\N	3.25992703	 003+0457	\N
2019-01-18	0.893157184	1.00537491	\N	1.50681102	7.04370022	\N	16898	-1	MLN1	1200	34.3268509	 034+0575	\N	34.4039001	 034+0711	\N
2019-01-18	0.870637298	0.998201251	\N	1.41648102	6.55993223	\N	17092	-1	MLN1	1200	32.4717598	 032+0830	\N	32.5599976	 032+0986	\N
2019-01-18	3.48724389	3.75585127	\N	2.02576661	3.50355268	\N	16898	1	MLN1	1200	1.32778203	 001+0577	\N	1.40483403	 001+0713	\N
2019-01-18	2.75900173	2.97259426	\N	1.91689885	4.1739049	\N	17092	1	MLN1	1200	3.17168999	 003+0302	\N	3.25992703	 003+0457	\N
2019-01-20	0.893157184	1.00537491	\N	1.50681102	7.04370022	\N	16898	-1	MLN1	1200	34.3268509	 034+0575	\N	34.4039001	 034+0711	\N
2019-01-20	0.870637298	0.998201251	\N	1.41648102	6.55993223	\N	17092	-1	MLN1	1200	32.4717598	 032+0830	\N	32.5599976	 032+0986	\N
2019-01-20	3.67209268	3.95389199	\N	2.02576661	3.50355268	\N	16898	1	MLN1	1200	1.32778203	 001+0577	\N	1.40483403	 001+0713	\N
2019-01-20	2.84775066	3.06767488	\N	1.91689885	4.1739049	\N	17092	1	MLN1	1200	3.17168999	 003+0302	\N	3.25992703	 003+0457	\N
2019-01-22	0.893157184	1.00537491	\N	1.50681102	7.04370022	\N	16898	-1	MLN1	1200	34.3268509	 034+0575	\N	34.4039001	 034+0711	\N
2019-01-22	0.870637298	0.998201251	\N	1.41648102	6.55993223	\N	17092	-1	MLN1	1200	32.4717598	 032+0830	\N	32.5599976	 032+0986	\N
2019-01-22	3.86820316	4.16399145	\N	2.02576661	3.50355268	\N	16898	1	MLN1	1200	1.32778203	 001+0577	\N	1.40483403	 001+0713	\N
2019-01-22	2.93649864	3.16275477	\N	1.91689885	4.1739049	\N	17092	1	MLN1	1200	3.17168999	 003+0302	\N	3.25992703	 003+0457	\N
\.


-- Completed on 2020-10-10 19:47:47

--
-- PostgreSQL database dump complete
--

