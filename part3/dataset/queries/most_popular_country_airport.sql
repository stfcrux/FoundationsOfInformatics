SELECT airport.Country, Airport_ID from  (
    
	SELECT country FROM route,airport
	where 
    route.Destination_airport_ID = airport.Airport_ID
    group by country
	order by count(*) desc 
    Limit 10
    )q
    JOIN airport
    on airport.Country=q.country;


