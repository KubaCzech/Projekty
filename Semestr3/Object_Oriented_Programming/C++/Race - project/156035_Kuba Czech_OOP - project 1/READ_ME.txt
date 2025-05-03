Rules of Race:
There are 3 subclasses of Vehicle - F1 car, Formula e car and 
Heypercar

Each type of car has different abilities:
a) F1 car has Turbo (with some probability), DRS (if he is 
behind a vehicle in front by at most 10 % of travelled Distance
and F1 car can go to pit so it doesn't travel any distance
in this round but refuels itself)
b) Formula e car has ERS (additional speed) which gives extra travelled
distance but it uses some of fuelOrEnergy field and as F1 car
it can pit to charge itself
c) Hypercar can't make a pit stop but may have spoiler and it
reduces drag of the car. Because it can't be refueled when fuel
decreases below some value (depending on each car) it travels
smaller distances but uses less fuel.

All starting values are random numbers generated in some 
interval depending on the car
Drivers and its Ids are unique

Besides the above, each car can suffer from Malfunction or 
being out of fuel. In that situation vehicle stops on track
and stays there to the end of race and doesn't travel any 
distance (so if hypothetically it had biggest travelled
distance and won it wouldn't be disqualified)

Kuba Czech, 156035

