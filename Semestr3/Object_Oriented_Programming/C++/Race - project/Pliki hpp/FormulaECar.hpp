#ifndef FORMULAECAR_H
#define FORMULAECAR_H
#include "Vehicle.hpp"

class FormulaE_car : public Vehicle
{
public:
    FormulaE_car(const std::string& Manufacturer, const std::string& Driver, const int IdOfCar, const float MalfunctionRate, float FuelOrEnergy, float Ers);
    virtual void takeTurn(float someDistance) =0;
    virtual std::string toString() const =0;
    //getters
    float getErs();

protected:
    float mErs;
};

#endif // FORMULAECAR_H
