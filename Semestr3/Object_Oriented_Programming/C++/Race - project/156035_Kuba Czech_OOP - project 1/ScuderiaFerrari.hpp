#pragma once
#include "F1_car.hpp"

class ScuderiaFerrari : public F1_car
{
public:
    ScuderiaFerrari(const std::string& Driver, const int IdOfCar, float MalfunctionRate, float FuelOrEnergy, const float Drs, const float Turbo);
    std::string toString() const override;
    void takeTurn(float someDistance) override;
};
