#pragma once
#include "Vehicle.hpp"

class FormulaE_car : public Vehicle
{
public:
    FormulaE_car(const std::string& Manufacturer, const std::string& Driver, const int IdOfCar, float MalfunctionRate, float FuelOrEnergy, const float Ers);
    virtual void takeTurn(float someDistance) =0;
    virtual std::string toString() const =0;
    //getters
    float getErs() const;

protected:
    float mErs;
};
