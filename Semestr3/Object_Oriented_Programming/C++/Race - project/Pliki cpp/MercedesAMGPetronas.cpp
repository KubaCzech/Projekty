#include "MercedesAMGPetronas.hpp"
#include "F1Car.hpp"
#include "F1Car.cpp"


    MercedesAMGPetronas::MercedesAMGPetronas(const std::string Driver, const int IdOfCar, float MalfunctionRate, float FuelOrEnergy, const float Drs, const float Turbo)
        : F1_car::F1_car("Mercedes", Driver, IdOfCar, MalfunctionRate, FuelOrEnergy, Drs, Turbo)
    {
        std::cout<<"Mercedes, Mercedes uber alles"<<std::endl;
    }

    std::string MercedesAMGPetronas::toString() const override
    {
        return (mDriver + ", " + mManufacturer + ": " + std::to_string(mTravelledDistance));
    }

    void MercedesAMGPetronas::takeTurn(float someDist) override
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
            F1_car::setDrsUsage(someDist);
            float distance = std::max(2.00, 80.00 * (float)(rand())/(float)(RAND_MAX));
            if (mDrsUsage == true)
                distance *= 1.00+mDrs;
            F1_car::setTravelledDistance(distance);
            F1_car::setFuelOrEnergy(std::max(8 * float (rand()) / float (RAND_MAX), 2.f));
            return;

        }
