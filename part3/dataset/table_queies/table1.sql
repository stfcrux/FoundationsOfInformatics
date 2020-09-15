SELECT countries.Country,count(*),Population FROM airport,countries
	where 
    airport.Country=countries.Country
    GROUP BY airport.Country
    ORDER BY count(*) desc