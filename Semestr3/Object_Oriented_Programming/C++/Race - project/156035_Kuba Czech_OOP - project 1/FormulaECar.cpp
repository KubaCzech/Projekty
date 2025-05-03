#include "FormulaECar.hpp"

    FormulaE_car::FormulaE_car(const std::string& Manufacturer, const std::string& Driver, const int IdOfCar, float MalfunctionRate, float FuelOrEnergy, const float Ers)
        : Vehicle(Manufacturer, Driver, IdOfCar, MalfunctionRate, FuelOrEnergy), mErs(Ers){}
    //getters
    float FormulaE_car::getErs() const
    {
        return mErs;
    }
