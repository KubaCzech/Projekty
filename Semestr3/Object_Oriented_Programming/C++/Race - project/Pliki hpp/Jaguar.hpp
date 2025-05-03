#ifndef JAGUAR_H
#define JAGUAR_H
#include "FormulaECar.hpp"

class Jaguar : public FormulaE_car
{
public:
    Jaguar(const std::string Driver, const int IdOfCar, const float MalfunctionRate, float FuelOrEnergy, float Ers);
    std::string toString() const override;
    void takeTurn(float someDistance) override;
};

#endif // JAGUAR_H
