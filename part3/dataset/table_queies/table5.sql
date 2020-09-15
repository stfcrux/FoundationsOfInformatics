SELECT Country ,count(*) from (
	select routeID from route, airport
	where route.Source_airport_ID=airport.Airport_ID
    AND airport.Country='Australia'
    ) as p ,route,airport
    where route.routeID = p.routeID
    AND route.Destination_airport_ID=airport.Airport_ID
    GROUP by Country
    order by count(*) DESC