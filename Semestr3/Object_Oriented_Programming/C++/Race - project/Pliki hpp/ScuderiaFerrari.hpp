#ifndef SCUDERIAFERRARI_H
#define SCUDERIAFERRARI_H
#include "F1Car.hpp"

class ScuderiaFerrari : public F1_car
{
public:
    ScuderiaFerrari(const std::string& Driver, const int IdOfCar, float MalfunctionRate, float FuelOrEnergy, const float Drs, const float Turbo);
    std::string toString() const override;
    void takeTurn(float someDistance) override;
};

#endif // SCUDERIAFERRARI_H
