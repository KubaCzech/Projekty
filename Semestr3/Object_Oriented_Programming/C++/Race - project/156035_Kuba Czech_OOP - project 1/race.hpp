#pragma once
#include "race.hpp"
#include "ScuderiaFerrari.hpp"
#include "RedBullRacing.hpp"
#include "MercedesAMGPetronas.hpp"
#include "Lamborghini.hpp"
#include "Bugatti.hpp"
#include "Porsche.hpp"
#include "Jaguar.hpp"
#include <vector>


template <typename V>
class Race{
public:
    int numberOfVehicles, numberOfLaps;
    //This constructor is empty because user must insert a number while program is running
    Race();

    //Memory deallocation at the end
    ~Race();

    void operator+=(Vehicle* veh);

    void operator-=(int k);

    void displayResults() const;

    //Instead of creating vector of vehicles in main I create the vector using function Factory so code is a bit more clear
    void Factory();

    void sortVector();

    void Run();

    void waitAndClear();

protected:
    std::vector<Vehicle*> vehicles;
    int driversInRace = 0;
};
#include "race.tpp"
