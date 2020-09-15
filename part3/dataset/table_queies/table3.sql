#depart from

SELECT airport.Country, Count(*) AS depart_from from route, airport
	where route.Source_airport_ID=airport.Airport_ID
    GROUP by airport.Country
    order by count(*) desc;



#arrive to
SELECT airport.Country, Count(*) AS depart_from from route, airport
	where route.Destination_airport_ID=airport.Airport_ID
    GROUP by airport.Country
    order by count(*) desc
