-- PORCENTAJE DE CAMAS OCUPADAS POR AREA
select 
	m.name_area, count(m.bed_serial) as total_beds,
	sum(( case  when m.bed_is_occuped = true then 1 else 0 end)) as total_beds_ocuped, 
	to_char( 
		(sum(case when m.bed_is_occuped = true then 1 else 0 end) * 100.0) / count(m.bed_serial), 'fm999.00%' 
	) as percentage_occupied_beds
from dim_movements m
inner join dim_beds b on b.id = m.bed_serial
group by m.name_area;

-- MOVIMIENTOS ERRONEOS DENTRO DEL CAMPO FINANZAS
select 
	m.name_area, b.id, p.personal_role  from dim_movements m 
	inner join dim_beds b on b.id = m.bed_serial
	inner join dim_personal p on p.id = m.personal_id
where p.personal_role = 'finanzas' and m.name_area in ('sala de operaciones', 'uci adultos');

-- LISTA TODOS LOS MOVIMIENTOS POR CADA ROL
select 
	p.personal_role, p.personal_speciality, count(m.id_record) as quantity_movements
	from dim_personal p
	inner join dim_movements m on m.personal_id = p.id
	where p.personal_role in ('medico', 'administrativo')
	group by p.personal_speciality, p.personal_role
order by count(m.id_record) desc;

-- MUESTRA LOS ROLES QUE MÁS HAN HECHO MOVIMIENTOS DENTRO DE CADA AREA
with RankedMovements as (
	select p.personal_role, p.personal_speciality, count(m.id_record) as quantity_movements,
	ROW_NUMBER() over ( partition by p.personal_role order by count(m.id_record) desc ) as ranking
	from dim_personal p
	inner join dim_movements m on m.personal_id = p.id
	WHERE p.personal_role IN ('medico', 'administrativo')
	GROUP BY p.personal_role, p.personal_speciality
) select personal_role, personal_speciality, quantity_movements
from RankedMovements
where ranking = 1;








