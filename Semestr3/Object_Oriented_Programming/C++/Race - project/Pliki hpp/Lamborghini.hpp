#ifndef LAMBORGHINI_H
#define LAMBORGHINI_H
#include "Hypercar.hpp"

class Lamborghini : public Hypercar
{
public:
    Lamborghini(const std::string Driver, const int IdOfCar, const float MalfunctionRate, float FuelOrEnergy, const bool Spoiler);
    std::string toString() const override;
    void takeTurn(float someDistance) override;
};
#endif // LAMBORGHINI_H
