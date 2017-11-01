SET statement_timeout = 0;
SET lock_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SET check_function_bodies = false;
SET client_min_messages = warning;

SET search_path = public, pg_catalog;
--
-- TOC entry 2405 (class 0 OID 25256)
-- Dependencies: 273
-- Data for Name: skills_criteria; Type: TABLE DATA; Schema: public; Owner: oscar
--

INSERT INTO skills_criteria (id, name) VALUES (1, 'Time');
INSERT INTO skills_criteria (id, name) VALUES (2, 'Group');
INSERT INTO skills_criteria (id, name) VALUES (3, 'Level');


--
-- TOC entry 2411 (class 0 OID 0)
-- Dependencies: 272
-- Name: skills_criteria_id_seq; Type: SEQUENCE SET; Schema: public; Owner: oscar
--

SELECT pg_catalog.setval('skills_criteria_id_seq', 3, true);



--
-- TOC entry 2410 (class 0 OID 25273)
-- Dependencies: 277
-- Data for Name: skills_professorcriteria; Type: TABLE DATA; Schema: public; Owner: oscar
--

INSERT INTO skills_professorcriteria (id, "order", criteria_id, professor_id) VALUES (1, 1, 1, NULL);
INSERT INTO skills_professorcriteria (id, "order", criteria_id, professor_id) VALUES (2, 2, 2, NULL);
INSERT INTO skills_professorcriteria (id, "order", criteria_id, professor_id) VALUES (3, 3, 3, NULL);
INSERT INTO skills_professorcriteria (id, "order", criteria_id, professor_id) VALUES (5, 1, 1, 1);


--
-- TOC entry 2416 (class 0 OID 0)
-- Dependencies: 276
-- Name: skills_professorcriteria_id_seq; Type: SEQUENCE SET; Schema: public; Owner: oscar
--

SELECT pg_catalog.setval('skills_professorcriteria_id_seq', 5, true);
