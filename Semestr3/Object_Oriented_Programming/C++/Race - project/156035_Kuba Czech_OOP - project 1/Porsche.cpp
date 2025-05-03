#include "Porsche.hpp"

Porsche::Porsche(const std::string Driver, const int IdOfCar, float MalfunctionRate, float FuelOrEnergy, float Ers)
        : FormulaE_car("Porsche", Driver, IdOfCar, MalfunctionRate, FuelOrEnergy, Ers){}

    std::string Porsche::toString() const
    {
        return (mDriver + ", " + mManufacturer + ": " + std::to_string(mTravelledDistance));
    }

    void Porsche::takeTurn(float someDistance)
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
                setTravelledDistance(distance * (1+mErs));
                setFuelOrEnergy(EnergyConsumption * 1.1);
                return;
            }
            else
            {
                if (someDistance - mTravelledDistance < 2.5)
                    setTravelledDistance(3.f);
                setTravelledDistance(distance);
                setFuelOrEnergy(EnergyConsumption);
                return;
            }
        }
    }
