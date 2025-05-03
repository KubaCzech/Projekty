#include "FormulaECar.cpp"
#include "FormulaECar.hpp"
#include "Porsche.cpp"

Porsche::Porsche(const std::string Driver, const int IdOfCar, const float MalfunctionRate, float FuelOrEnergy, float Ers)
        : FormulaE_car::FormulaE_car("Porsche", Driver, IdOfCar, MalfunctionRate, FuelOrEnergy, Ers)
    {
        //std::cout<<"Favourite vehicle of Osama Bin Laden - Porsche 9/11"<<std::endl;
    }

    std::string Porsche::toString() const override
    {
        return (mDriver + ", " + mManufacturer + ": " + std::to_string(mTravelledDistance));
    }

    void Porsche::takeTurn(float someDistance) override
    {
        float prob = float (rand()) / float (RAND_MAX); //Which move to do
        float prob2 = float (rand()) / float (RAND_MAX); //Which 'special action to take'
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

        if (prob < mMalfunctionRate + 0.06 && mFuelOrEnergy < 60.00)
        {
            mFuelOrEnergy = 110.f;
        }
        else
        {
            float distance = std::max(1.00, 85.00 * (float)(rand())/(float)(RAND_MAX));
            float EnergyConsumption = std::max(4 * (float)(rand()) / (float)(RAND_MAX), float(2.3));

            if (prob2 < 0.7)
            {
                Porsche::setTravelledDistance(distance * (1+mErs));
                Porsche::setFuelOrEnergy(EnergyConsumption * 1.1);
                return;
            }
            else
            {
                if (someDistance - mTravelledDistance < 2.5)
                    Porsche::setTravelledDistance(3.f);
                Porsche::setTravelledDistance(distance);
                Porsche::setFuelOrEnergy(EnergyConsumption);
                return;
            }
        }
    }
