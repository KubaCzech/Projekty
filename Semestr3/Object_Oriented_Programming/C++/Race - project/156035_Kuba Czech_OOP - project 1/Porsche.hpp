#pragma once
#include "FormulaECar.hpp"

class Porsche : public FormulaE_car
{
public:
    Porsche(const std::string Driver, const int IdOfCar, float MalfunctionRate, float FuelOrEnergy, float Ers);
    std::string toString() const override;
    void takeTurn(float someDistance) override;
};
