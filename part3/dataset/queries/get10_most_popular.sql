SELECT country as Selected_Country, count(*) FROM route,airport
	where 
    route.Destination_airport_ID = airport.Airport_ID
    group by country
	order by count(*) desc 
    Limit 10