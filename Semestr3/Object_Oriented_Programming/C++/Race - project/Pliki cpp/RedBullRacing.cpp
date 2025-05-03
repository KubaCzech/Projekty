#include "RedBullRacing.hpp"
#include "F1Car.hpp"
#include "F1Car.cpp"


    RedBullRacing::RedBullRacing(const std::string Driver, const int IdOfCar, float MalfunctionRate, float FuelOrEnergy, const float Drs, const float Turbo)
        : F1_car::F1_car("Red Bull", Driver, IdOfCar, MalfunctionRate, FuelOrEnergy, Drs, Turbo)
    {
        //std::cout<<"*Dutch anthem being played*"<<std::endl;
    }

    std::string RedBullRacing::toString() const override
    {
        return (mDriver + ", " + mManufacturer + ": " + std::to_string(mTravelledDistance));
    }

    void RedBullRacing::takeTurn(float someDistance) override
    {
        float prob = float (rand()) / float (RAND_MAX); //Which move to do
        float prob2 = float (rand()) / float (RAND_MAX); //Which 'special action' to use
        if (mFuelOrEnergy <= 0)
        {
            mFuelOrEnergy = 0;
            return;
        }

        if (prob < mMalfunctionRate)
        {
            mMalfunctionRate = 1.0;
            return;
        }

        if (prob < 0.15 + mMalfunctionRate && mMalfunctionRate < 1.f && mFuelOrEnergy < 50.0)
        {
            mFuelOrEnergy = 75.00;
            return;
        }

        else
        {
            F1_car::setDrsUsage(someDistance);
            float distance = std::max(1.00, 90.00 * (float)(rand())/(float)(RAND_MAX));
            if (prob2 < 0.9)
                distance += mTurbo;
            F1_car::setTravelledDistance(distance);
            F1_car::setFuelOrEnergy(std::max(7 * float (rand()) / float (RAND_MAX), (float) 1.8));
            return;

        }
