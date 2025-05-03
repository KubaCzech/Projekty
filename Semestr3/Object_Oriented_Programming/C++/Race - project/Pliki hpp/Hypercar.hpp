#ifndef HYPERCAR_H
#define HYPERCAR_H
#include "Vehicle.hpp"

class Hypercar : public Vehicle
{
public:
    Hypercar(const std::string& Manufacturer, const std::string& Driver, const int IdOfCar, float MalfunctionRate, float FuelOrEnergy, const bool Spoiler;
    virtual void takeTurn(float someDistance)=0;
    virtual std::string toString() const =0;
    //getters
    bool getSpoiler() const;

protected:
    bool mSpoiler;
};

#endif // HYPERCAR_H
