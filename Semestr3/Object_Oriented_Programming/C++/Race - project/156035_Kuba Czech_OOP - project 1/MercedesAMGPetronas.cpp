#include "MercedesAMGPetronas.hpp"

    MercedesAMGPetronas::MercedesAMGPetronas(const std::string Driver, const int IdOfCar, float MalfunctionRate, float FuelOrEnergy, const float Drs, const float Turbo)
        : F1_car::F1_car("Mercedes", Driver, IdOfCar, MalfunctionRate, FuelOrEnergy, Drs, Turbo) {}

    std::string MercedesAMGPetronas::toString() const
    {
        return (mDriver + ", " + mManufacturer + ": " + std::to_string(mTravelledDistance));
    }

    void MercedesAMGPetronas::takeTurn(float someDist)
    {
        float prob = float (rand()) / float (RAND_MAX); //Which move to do
        if (mFuelOrEnergy <= 0)
        {
            //std::cout<<"Mercedes of "<<mDriver<<" is out of fuel"<<std::endl;
            mFuelOrEnergy = 0;
            return;
        }

        if (prob < mMalfunctionRate)
        {
            mMalfunctionRate = 1.0;
            return;
        }

        if (prob < 0.12 + mMalfunctionRate && mMalfunctionRate < 1.f && mFuelOrEnergy < 70.00)
        {
            mFuelOrEnergy = 90.00;
            return;
        }

        else
        {
            setDrsUsage(someDist);
            float distance = std::max(2.00, 80.00 * (float)(rand())/(float)(RAND_MAX));
            if (mDrsUsage == true)
                distance *= 1.00+mDrs;
            setTravelledDistance(distance);
            setFuelOrEnergy(std::max(8 * float (rand()) / float (RAND_MAX), 2.f));
            return;

        }
    }
