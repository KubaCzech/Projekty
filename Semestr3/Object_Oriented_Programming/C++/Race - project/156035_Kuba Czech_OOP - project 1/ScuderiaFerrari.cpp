#include "ScuderiaFerrari.hpp"

    ScuderiaFerrari::ScuderiaFerrari(const std::string& Driver, const int IdOfCar, float MalfunctionRate, float FuelOrEnergy, const float Drs, const float Turbo)
        : F1_car("Ferrari", Driver, IdOfCar, MalfunctionRate, FuelOrEnergy, Drs, Turbo) {}

    std::string ScuderiaFerrari::toString() const
    {
        return (mDriver + ", " + mManufacturer + ": " + std::to_string(mTravelledDistance));
    }

    void ScuderiaFerrari::takeTurn(float someDistance)
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

        if (prob < 0.1 + mMalfunctionRate && mMalfunctionRate < 1.f && mFuelOrEnergy < 80.00)
        {
            mFuelOrEnergy = 100.00;
            return;
        }

        else
        {
            setDrsUsage(someDistance);
            float distance = std::max(1.00, 100.00 * (float)(rand())/(float)(RAND_MAX));
            if (prob2 < 0.95)
                distance += mTurbo;
            if (mDrsUsage == true)
                distance *= 1.00+mDrs;
            setTravelledDistance(distance);
            setFuelOrEnergy(std::max(5 * float (rand()) / float (RAND_MAX), 1.f));
            //std::cout<<"Ferrari of "<<mDriver<<" travelled: "<<mTravelledDistance<<", fuel left: "<<mFuelOrEnergy<<std::endl;
            return;

        }
    }
