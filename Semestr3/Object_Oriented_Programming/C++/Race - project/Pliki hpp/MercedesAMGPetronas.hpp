#ifndef MERCEDESAMGPETRONAS_H
#define MERCEDESAMGPETRONAS_H
#include "F1Car.hpp""

class MercedesAMGPetronas : public F1_car
{
public:
    MercedesAMGPetronas(const std::string Driver, const int IdOfCar, float MalfunctionRate, float FuelOrEnergy, const float Drs, const float Turbo);
    std::string toString() const override;
    void takeTurn(float someDist) override;
};

#endif // MERCEDESAMGPETRONAS_H
