#include "Bugatti.hpp"

    Bugatti::Bugatti(const std::string Driver, const int IdOfCar, float MalfunctionRate, float FuelOrEnergy, const bool Spoiler)
        : Hypercar("Bugatti", Driver, IdOfCar, MalfunctionRate, FuelOrEnergy, Spoiler){}

    std::string Bugatti::toString() const
    {
        return (mDriver + ", " + mManufacturer + ": " + std::to_string(mTravelledDistance));
    }

    void Bugatti::takeTurn(float someDistance)
    {
        float prob = float (rand()) / float (RAND_MAX); //Which move to do
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
        else
        {
            float distance = std::max(1.00, 80.00 * (float)(rand())/(float)(RAND_MAX));
            float FuelConsumption = (float) std::max(4 * (float)(rand()) / (float)(RAND_MAX), float(1.2));
            if (someDistance - mTravelledDistance < 10)
                FuelConsumption = (float) std::min(FuelConsumption, (float) 0.5);
            if (mFuelOrEnergy < 30.0)
            {
                setTravelledDistance(distance * 0.8);
                setFuelOrEnergy(FuelConsumption * 0.3);
            }
            else
            {
                if (mSpoiler == true)
                    setTravelledDistance(distance * 1.4);
                else
                    setTravelledDistance(distance);
                setFuelOrEnergy(FuelConsumption);
            }
        }
    }
