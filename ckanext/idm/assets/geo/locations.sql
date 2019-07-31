SELECT 
	sh.id, 
	sh.name, 
	a.alias_dot_name as path, 
	a.admin_level as level, 
	ST_Envelope(sh.geom) as geometry
FROM sd.alias_name_table a
	inner join sd.hierarchy_name_table h
		on a.hierarchy_name_id = h.id
	inner join sd.hierarchy_name_shape_map m
		on h.id = m.hierarchy_name_id
	inner join sd.shape_table sh
		on m.shape_id = sh.id	
where sh.shape_set_id = (SELECT id FROM sd.shape_set WHERE shape_set_name = 'GADM_V2.8_Shapes' LIMIT 1)  
	AND a.admin_level <= 1	

-- ogr2ogr -f GeoJSON -a_srs EPSG:4326 locations.json "PG:host=<server> dbname=idm_db" -sql @locations.sql
