#pragma once
#include "FormulaECar.hpp"

class Jaguar : public FormulaE_car
{
public:
    Jaguar(const std::string Driver, const int IdOfCar, float MalfunctionRate, float FuelOrEnergy, const float Ers);
    std::string toString() const override;
    void takeTurn(float someDistance) override;
};
