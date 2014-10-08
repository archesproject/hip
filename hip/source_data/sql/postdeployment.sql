--
-- PostgreSQL database dump
--

-- Dumped from database version 9.1.4
-- Dumped by pg_dump version 9.1.4
-- Started on 2014-09-10 15:56:10

SET statement_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = off;
SET check_function_bodies = false;
SET client_min_messages = warning;
SET escape_string_warning = off;

--
-- TOC entry 12 (class 2615 OID 16061322)
-- Name: aux; Type: SCHEMA; Schema: -; Owner: postgres
--

CREATE SCHEMA aux;


ALTER SCHEMA aux OWNER TO postgres;

SET search_path = aux, pg_catalog;

SET default_tablespace = '';

SET default_with_oids = false;

--
-- TOC entry 256 (class 1259 OID 16061492)
-- Dependencies: 1605 12
-- Name: overlays; Type: TABLE; Schema: aux; Owner: postgres; Tablespace: 
--

CREATE TABLE overlays (
    overlaytype text,
    overlayvalue text,
    geometry public.geometry(Geometry,4326),
    overlayid uuid NOT NULL
);


ALTER TABLE aux.overlays OWNER TO postgres;

--
-- TOC entry 3288 (class 2606 OID 16064233)
-- Dependencies: 256 256
-- Name: overlays_pkey; Type: CONSTRAINT; Schema: aux; Owner: postgres; Tablespace: 
--

ALTER TABLE ONLY overlays
    ADD CONSTRAINT overlays_pkey PRIMARY KEY (overlayid);


--
-- TOC entry 3289 (class 1259 OID 16064226)
-- Dependencies: 256 2698
-- Name: overlays_sidx; Type: INDEX; Schema: aux; Owner: postgres; Tablespace: 
--

CREATE INDEX overlays_sidx ON overlays USING gist (geometry);


--
-- TOC entry 3290 (class 1259 OID 16064234)
-- Dependencies: 256
-- Name: overlaytype_idx; Type: INDEX; Schema: aux; Owner: postgres; Tablespace: 
--

CREATE INDEX overlaytype_idx ON overlays USING btree (overlaytype);


-- Completed on 2014-09-10 15:56:11

--
-- PostgreSQL database dump complete
--
CREATE TABLE aux.addresses
(
  addressnum text,
  addressstreet text,
  vintage text,
  geometry geometry(MultiPoint,4326)
)
WITH (
  OIDS=FALSE
);
ALTER TABLE aux.addresses
  OWNER TO postgres;

-- Index: aux.addresses_sidx

-- DROP INDEX aux.addresses_sidx;

CREATE INDEX addresses_sidx
  ON aux.addresses
  USING gist
  (geometry );

  -- Table: aux.parcels

-- DROP TABLE aux.parcels;

CREATE TABLE aux.parcels
(
  parcelapn text,
  vintage text,
  geometry geometry(MultiPolygon,4326)
)
WITH (
  OIDS=FALSE
);
ALTER TABLE aux.parcels
  OWNER TO postgres;

-- Index: aux.parcels_sidx

-- DROP INDEX aux.parcels_sidx;

CREATE INDEX parcels_sidx
  ON aux.parcels
  USING gist
  (geometry );


