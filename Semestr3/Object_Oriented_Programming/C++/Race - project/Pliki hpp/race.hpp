#ifndef RACE_H
#define RACE_H

#include "ScuderiaFerrari.hpp"
#include "MercedesAMGPetronas.hpp"
#include "RedBullRacing.hpp"
#include "Lamborghini.hpp"
#include "Bugatti.hpp"
#include "Jaguar.hpp"
#include "Porsche.hpp"


template <class V>
class Race{
public:
    int numberOfVehicles;
    Race();

    //Memory deallocation at the end
    ~Race();
    void operator+=(const V& veh);

    void operator-=(int k);

    void displayResults();

    void Factory();

    void sortVector();

    void Run();

protected:
    std::vector<V> vehicles;
    int driversInRace = 0;

};

#endif // RACE_H
