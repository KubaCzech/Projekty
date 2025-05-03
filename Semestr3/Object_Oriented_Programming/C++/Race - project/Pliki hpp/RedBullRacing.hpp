#ifndef REDBULLRACING_H
#define REDBULLRACING_H
#include "F1Car.hpp"

class RedBullRacing : public F1_car
{
public:
    RedBullRacing(const std::string& Driver, const int IdOfCar, float MalfunctionRate, float FuelOrEnergy, const float Drs, const float Turbo);
    std::string toString() const override;
    void takeTurn(float someDistance) override;
};

#endif

