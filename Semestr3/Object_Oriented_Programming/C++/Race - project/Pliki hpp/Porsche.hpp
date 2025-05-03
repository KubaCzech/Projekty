#ifndef PORSCHE_H
#define PORSCHE_H
#include "FormulaECar.hpp"

class Porsche : public FormulaE_car
{
public:
    Porsche(const std::string Driver, const int IdOfCar, const float MalfunctionRate, float FuelOrEnergy, float Ers);
    std::string toString() const override;
    void takeTurn(float someDistance) override;
};

#endif
