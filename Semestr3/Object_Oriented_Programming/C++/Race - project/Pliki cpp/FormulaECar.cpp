#include "FormulaECar.hpp"
#include "Vehicle.hpp"
#include "Vehicle.cpp"

    FormulaE_car::FormulaE_car(const std::string& Manufacturer, const std::string& Driver, const int IdOfCar, const float MalfunctionRate, float FuelOrEnergy, float Ers)
        : Vehicle::Vehicle(Manufacturer, Driver, IdOfCar, MalfunctionRate, FuelOrEnergy), mErs(Ers){}
    //getters
    float FormulaE_car::getErs()
    {
        return mErs;
    }
