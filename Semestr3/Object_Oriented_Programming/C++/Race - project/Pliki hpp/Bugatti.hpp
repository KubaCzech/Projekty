#ifndef BUGATTI_H
#define BUGATTI_H
#include "Hypercar.hpp"

class Bugatti : public Hypercar
{
public:
    Bugatti(const std::string Driver, const int IdOfCar, const float MalfunctionRate, float FuelOrEnergy, const bool Spoiler);
    std::string toString() const override;
    void takeTurn(float someDistance) override;
};
#endif // LAMBORGHINI_H
