#pragma once
#include "F1_car.hpp"

class MercedesAMGPetronas : public F1_car
{
public:
    MercedesAMGPetronas(const std::string Driver, const int IdOfCar, float MalfunctionRate, float FuelOrEnergy, const float Drs, const float Turbo);
    std::string toString() const override;
    void takeTurn(float someDist) override;
};

