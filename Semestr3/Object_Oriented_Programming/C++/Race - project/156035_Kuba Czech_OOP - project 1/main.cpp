#include <iostream>
#include <cmath>
#include <cstdlib>
#include <ctime>
#include <vector>
#include <string>
#include <algorithm>

#include "ScuderiaFerrari.hpp"
#include "MercedesAMGPetronas.hpp"
#include "RedBullRacing.hpp"
#include "Bugatti.hpp"
#include "Lamborghini.hpp"
#include "Jaguar.hpp"
#include "Porsche.hpp"
#include "race.hpp"

int main()
{
    std::srand(std::time(NULL));
    Race<Vehicle*> race = Race<Vehicle*>();
    race.Run();
    return 0;
}
