/*
   COMP693 S2 2025 - Industry Project
   Script file for MySQL DBMS
   Created By: Tina Ma
   Description: Insert data into related tables
   Created Date: 28/07/2025
   Updated Date: 25/08/2025
   Version: 1.2
*/

-- Use shoppingcentre database to insert data into related tables
USE shoppingcentre;

-- City
INSERT INTO city (name, image_filename) VALUES
('Christchurch', 'Christchurch.jpg'),
('Tauranga', 'Tauranga.jpg'),
('Auckland', 'Auckland.jpg'),
('Palmerston North', 'PalmerstonNorth.jpg'),
('Rotorua', 'Rotorua.jpg');

-- Classification
INSERT INTO classification (name) VALUES
('Neighbourhood Centre'),
('Sub Regional Centre'),
('Bulk Retail'),
('City Centre'),
('Other'),
('Regional Centre'),
('Major Regional Centre');

-- Centre Type
INSERT INTO centre_type (name) VALUES
('Enclosed Mall'),
('Open Integrated Centre'),
('Open Mall'),
('Bulk Retail Centre'),
('Enclosed Integrated Centre');

INSERT INTO shopping_centre (
  city_id, classification_id, centre_type_id,
  name, osm_name, image_filename, location, date_opened, site_area_ha,
  covered_parking_num, uncovered_parking_num, redevelopments, levels, total_retail_space
) VALUES
-- Avonhead Shopping Centre
(
  (SELECT id FROM city WHERE name='Christchurch'),
  (SELECT id FROM classification WHERE name='Neighbourhood Centre'),
  (SELECT id FROM centre_type WHERE name='Enclosed Mall'),
  'Avonhead Shopping Centre',
  'Avonhead Shopping Mall',
  'AvonheadShoppingCentre_1.jpg',
  'Corner Merrin Street and Withells Road, Avonhead, Christchurch',
  '1993-11-01', 0.9211,
  0, 556, '', 1, 3689.55
),
-- Barrington
(
  (SELECT id FROM city WHERE name='Christchurch'),
  (SELECT id FROM classification WHERE name='Sub Regional Centre'),
  (SELECT id FROM centre_type WHERE name='Open Integrated Centre'),
  'Barrington',
  'Mall Barrington',
  'Barrington_2.jpg',
  '256 Barrington Street, Spreydon, Christchurch',
  '1973-11-01', 1.2629,
  0, 148,
  'May 1998 (7,000sqm). February 2012 (3,000sqm).',
  1, 14204.45
),
-- Bishopdale
(
  (SELECT id FROM city WHERE name='Christchurch'),
  (SELECT id FROM classification WHERE name='Neighbourhood Centre'),
  (SELECT id FROM centre_type WHERE name='Open Mall'),
  'Bishopdale',
  'Bishopdale Village Mall',
  'Bishopdale_3.jpg',
  'Harewood Road and Farrington Avenue, Bishopdale, Christchurch',
  NULL, 3.0966,
  0, 600, '', 2, NULL
),
-- Blenheim Square
(
  (SELECT id FROM city WHERE name='Christchurch'),
  (SELECT id FROM classification WHERE name='Bulk Retail'),
  (SELECT id FROM centre_type WHERE name='Bulk Retail Centre'),
  'Blenheim Square',
  'Mall Blenheim square',
  'BlenheimSquare_4.jpg',
  '217 Blenheim Road, Riccarton, Christchurch',
  NULL, NULL,
  0, 140, '', 1, 3780.03
),
-- BNZ Centre
(
  (SELECT id FROM city WHERE name='Christchurch'),
  (SELECT id FROM classification WHERE name='City Centre'),
  (SELECT id FROM centre_type WHERE name='Enclosed Integrated Centre'),
  'BNZ Centre',
  'BNZ Centre',
  'BNZCentre_5.jpg',
  '109 Cashel Street, 120 Hereford Street, CBD, Christchurch',
  '2016-01-01', 1.0000,
  0, 0, '', 1, 4356.04
),
-- Brackenfields
(
  (SELECT id FROM city WHERE name='Christchurch'),
  (SELECT id FROM classification WHERE name='Neighbourhood Centre'),
  (SELECT id FROM centre_type WHERE name='Open Integrated Centre'),
  'Brackenfields',
  'Woolworths, 121 Carters Road',
  'Brackenfields_6.jpg',
  '115-135 Carters Road, Amberley, Christchurch',
  '2014-07-01', 4.0000,
  0, 400, '', 1, 5739.00
),
-- Bush Inn Shopping Centre
(
  (SELECT id FROM city WHERE name='Christchurch'),
  (SELECT id FROM classification WHERE name='Sub Regional Centre'),
  (SELECT id FROM centre_type WHERE name='Enclosed Integrated Centre'),
  'Bush Inn Shopping Centre',
  'Bush Inn Shopping Centre',
  'BushInnShoppingCentre_7.jpg',
  'Corner Waimairi and Riccarton Roads, Upper Riccarton, Christchurch',
  '1988-11-01', 3.7675,
  151, 543,
  '1989, 1995, 2001, 2007, 2011, 2015, 2016, 2017',
  1, 17173.90
),
-- Dress-Smart Hornby
(
  (SELECT id FROM city WHERE name='Christchurch'),
  (SELECT id FROM classification WHERE name='Other'),
  (SELECT id FROM centre_type WHERE name='Enclosed Mall'),
  'Dress-Smart Hornby',
  'Dress Smart',
   'Dress-SmartHornby_8.jpg',
  '409 Main South Road, Hornby, Christchurch',
  '1998-10-31',1.2190,
  166, 181,
  '2002 (492sqm); 2005 (1,761.4sqm); 2009 (2,220.40sqm).',
  1, 7035.72
),
-- Eastgate Shopping Centre
(
  (SELECT id FROM city WHERE name='Christchurch'),
  (SELECT id FROM classification WHERE name='Regional Centre'),
  (SELECT id FROM centre_type WHERE name='Enclosed Mall'),
  'Eastgate Shopping Centre',
  'Mall Eastgate Shopping Centre',
  'EastgateShoppingCentre_9.jpg',
  '20 Buckleys Road, Linwood, Christchurch',
  '2003-01-01', 6.4460,
  0, 1100,
  '2003 & 2011',
  2, 24815.00
),
-- Fendalton Mall
(
  (SELECT id FROM city WHERE name='Christchurch'),
  (SELECT id FROM classification WHERE name='Neighbourhood Centre'),
  (SELECT id FROM centre_type WHERE name='Open Mall'),
  'Fendalton Mall',
  'Fendalton Shops',
  'FendaltonMall_10.jpg',
  '19-23 Memorial Avenue, Fendalton, Christchurch',
  '1970-12-01', 1.5000,
  0, 211,
  'August 1991 (650sqm); November 1994 (200sqm); additions Sep 2003 (250sqm), Oct 2003 (190sqm), Dec 2004 (926sqm).',
  1, 3772.00
),
-- Homebase
(
  (SELECT id FROM city WHERE name='Christchurch'),
  (SELECT id FROM classification WHERE name='Bulk Retail'),
  (SELECT id FROM centre_type WHERE name='Bulk Retail Centre'),
  'Homebase',
  'Home Base Shopping Centre',
  'Homebase_11.png',
  'Marshland Road, Shirley, Christchurch',
  '2008-03-01', 1.7348,
  0, 384, '', 1, 17338.53
),
-- Hornby Mega Centre
(
  (SELECT id FROM city WHERE name='Christchurch'),
  (SELECT id FROM classification WHERE name='Bulk Retail'),
  (SELECT id FROM centre_type WHERE name='Bulk Retail Centre'),
  'Hornby Mega Centre',
  'Hornby Mega Centre',
  'HornbyMegaCentre_12.jpg',
  '2 Chappie Place, Hornby, Christchurch',
  '2013-09-01', 5.5000,
  0, 800, '', 1, 23196.00
),
-- Merivale Mall
(
  (SELECT id FROM city WHERE name='Christchurch'),
  (SELECT id FROM classification WHERE name='Neighbourhood Centre'),
  (SELECT id FROM centre_type WHERE name='Enclosed Mall'),
  'Merivale Mall',
  'Mall Merivale Mall',
  'MerivaleMall_13.jpg',
  '189 Papanui Road, Merivale, Christchurch',
  '1980-01-01',1.8884,
  0, 435,
  '2018 Ambience Upgrade; 2017 Bathroom Upgrade',
  2, 6812.30
),
-- Midway Moorhouse
(
  (SELECT id FROM city WHERE name='Christchurch'),
  (SELECT id FROM classification WHERE name='Bulk Retail'),
  (SELECT id FROM centre_type WHERE name='Bulk Retail Centre'),
  'Midway Moorhouse',
  '200 Moorhouse Avenue',
  'MidwayMoorhouse_14.jpg',
  '200-218 Moorhouse Avenue, CBD, Christchurch',
  '2013-01-01',4.0000,
  0, 260, '', 1, 10353.99
),
-- Moorhouse Central
(
  (SELECT id FROM city WHERE name='Christchurch'),
  (SELECT id FROM classification WHERE name='Neighbourhood Centre'),
  (SELECT id FROM centre_type WHERE name='Open Integrated Centre'),
  'Moorhouse Central',
  '347 Moorhouse Avenue',
  'MoorhouseCentral_15.jpg',
  '347 Moorhouse Avenue, CBD, Christchurch',
  '1990-01-01',1.7000,
  0, 310, '', 1, 6430.75
),
-- Northlands
(
  (SELECT id FROM city WHERE name='Christchurch'),
  (SELECT id FROM classification WHERE name='Regional Centre'),
  (SELECT id FROM centre_type WHERE name='Enclosed Mall'),
  'Northlands',
  'Northlands Mall',
  'Northlands_16.jpg',
  '55 Main North Road, Papanui, Christchurch',
  '1967-11-01',8.5000,
  705, 1003,
  '7,614sqm (1995/96) / 19,457sqm (2003/04); minor redevelopments 2013; foodcourt playground (2015).',
  1, 40382.78
),
-- Parklands Shopping Centre
(
  (SELECT id FROM city WHERE name='Christchurch'),
  (SELECT id FROM classification WHERE name='Neighbourhood Centre'),
  (SELECT id FROM centre_type WHERE name='Open Mall'),
  'Parklands Shopping Centre',
  'Retail Parklands Shopping Centre',
  'ParklandsShoppingCentre_17.jpg',
  '60 Queenspark Drive, Parklands, Christchurch',
  '1980-01-01',1.3496,
  0, 205,
  '1989 (693sqm), 1991 (595sqm), 1993 (676sqm), 2006 (637sqm added).',
  1, 4856.00
),

-- Rolleston Square
(
  (SELECT id FROM city WHERE name='Christchurch'),
  (SELECT id FROM classification WHERE name='Neighbourhood Centre'),
  (SELECT id FROM centre_type WHERE name='Open Mall'),
  'Rolleston Square',
  'Rolleston Square',
  'RollestonSquare_18.jpg',
  'Rolleston Square, Rolleston, Christchurch',
  '2007-03-01',2.6458,
  0, 250,
  'New eastern development Jun 2014 adding 7 tenancies.',
  1, 6523.72
),
-- SOUTH CITY SHOPPING CENTRE
(
  (SELECT id FROM city WHERE name='Christchurch'),
  (SELECT id FROM classification WHERE name='City Centre'),
  (SELECT id FROM centre_type WHERE name='Enclosed Integrated Centre'),
  'SOUTH CITY SHOPPING CENTRE',
  'Mall South City Shopping Centre',
  'SOUTHCITYSHOPPINGCENTRE_19.jpg',
  '555 Colombo Street, CBD, Christchurch',
  '1990-11-01',3.3000,
  0, 600,
  'Dec 1998; Dec 2000; Foodcourt Jan 2013; Amenities Mar 2017',
  1, 13446.04
),
-- The Colombo
(
  (SELECT id FROM city WHERE name='Christchurch'),
  (SELECT id FROM classification WHERE name='Neighbourhood Centre'),
  (SELECT id FROM centre_type WHERE name='Enclosed Mall'),
  'The Colombo',
  'The Colombo',
  'TheColombo_20.jpg',
  '363 Colombo Street, Sydenham, Christchurch',
  '1984-12-01',1.4944,
  0, 257,
  '1993 upgrade; 1997, 2000 & 2005/6 refurbishments & extensions.',
  2, 7192.00
),
-- The Hub Hornby
(
  (SELECT id FROM city WHERE name='Christchurch'),
  (SELECT id FROM classification WHERE name='Sub Regional Centre'),
  (SELECT id FROM centre_type WHERE name='Enclosed Integrated Centre'),
  'The Hub Hornby',
  'The Hub Hornby Mall',
  'TheHubHornby_21.jpg',
  '416-418 Main South Road, Hornby, Christchurch',
  '1977-01-01',3.6000,
  0, 735,
  '1992; 1998/99; 2004/05; Nov 2017.',
  2, 20905.00
),
-- The Palms, Shirley
(
  (SELECT id FROM city WHERE name='Christchurch'),
  (SELECT id FROM classification WHERE name='Regional Centre'),
  (SELECT id FROM centre_type WHERE name='Enclosed Mall'),
  'The Palms, Shirley',
  'The Palms Shopping Centre Mall',
  'ThePalms,Shirley_22.jpg',
  'Corner Marshland and New Brighton Road, Shirley, Christchurch',
  '1996-10-01',5.5000,
  618, 855, '2011', 2, 27321.00
),
-- The Tannery
(
  (SELECT id FROM city WHERE name='Christchurch'),
  (SELECT id FROM classification WHERE name='Other'),
  (SELECT id FROM centre_type WHERE name='Open Integrated Centre'),
  'The Tannery',
  'The Tannery Retail',
  'TheTannery_23.jpg',
  '3 Garlands Road, Woolston, Christchurch',
  '2013-01-01',2.0000,
  0, 150, '', 1, 11040.00
),
-- Tower Junction Mega Centre
(
  (SELECT id FROM city WHERE name='Christchurch'),
  (SELECT id FROM classification WHERE name='Bulk Retail'),
  (SELECT id FROM centre_type WHERE name='Bulk Retail Centre'),
  'Tower Junction Mega Centre',
  'Tower Junction Retail',
  'TowerJunctionMegaCentre_24.jpg',
  'Corner Clarence and Foster Streets, Addington, Christchurch',
  '2006-03-01',6.4950,
  0, 900, '', 1, 31027.00
),
-- Tower Junction Village
(
  (SELECT id FROM city WHERE name='Christchurch'),
  (SELECT id FROM classification WHERE name='Bulk Retail'),
  (SELECT id FROM centre_type WHERE name='Open Mall'),
  'Tower Junction Village',
  'Tower Junction',
  'TowerJunctionVillage_25.jpg',
  'Corner Whiteleigh Ave and Troup Drive, Addington, Christchurch',
  '2005-12-01',4.1079,
  0, 294, '', 1, 4269.00
),
-- Westfield Riccarton
(
  (SELECT id FROM city WHERE name='Christchurch'),
  (SELECT id FROM classification WHERE name='Major Regional Centre'),
  (SELECT id FROM centre_type WHERE name='Enclosed Integrated Centre'),
  'Westfield Riccarton',
  'Westfield Riccarton Mall',
  'WestfieldRiccarton_26.jpg',
  '129 Riccarton Road, Riccarton, Christchurch',
  '1965-11-01',8.1773,
  1427, 973,
  '1995; 2004/05 extension; 2005 Hoyts Cinemas; 2008–09 redevelopment.',
  2, 49346.00
),
-- THE CROSSING
(
  (SELECT id FROM city WHERE name='Christchurch'),
  (SELECT id FROM classification WHERE name='City Centre'),
  (SELECT id FROM centre_type WHERE name='Open Mall'),
  'THE CROSSING',
  'The Crossing Mall',
  'THECROSSING_27.jpg',
  '166 Cashel Street, Christchurch',
  '2017-09-09',1.0000,
  650, 0, '', 3, 12904.00
),
-- FASHION ISLAND PAPAMOA
(
  (SELECT id FROM city WHERE name='Tauranga'),
  NULL, NULL,
  'FASHION ISLAND PAPAMOA',
  'FASHION ISLAND PAPAMOA',
  NULL,
  '42 Gravatt Road, Papamoa, Tauranga'
  , NULL, NULL, NULL, NULL, NULL, NULL, NULL
),
-- SILVERDALE SHOPPING CENTRE
(
  (SELECT id FROM city WHERE name='Auckland'),
  NULL, NULL,
  'SILVERDALE SHOPPING CENTRE',
  'Silverdale Centre',
  NULL,
  '61 Silverdale Street, Silverdale, Auckland'
  , NULL, NULL, NULL, NULL, NULL, NULL, NULL
),
-- THE PLAZA
(
  (SELECT id FROM city WHERE name='Palmerston North'),
  NULL, NULL,
  'THE PLAZA',
  'THE PLAZA Palmerston North',
  NULL,
  '84 The Square, Palmerston North'
  , NULL, NULL, NULL, NULL, NULL, NULL, NULL
),
-- TRADE CENTRAL
(
  (SELECT id FROM city WHERE name='Rotorua'),
  NULL, NULL,
  'TRADE CENTRAL',
  'TRADE CENTRAL Rotorua',
  NULL,
  '1490 Amohau Street, Rotorua'
  , NULL, NULL, NULL, NULL, NULL, NULL, NULL
);
