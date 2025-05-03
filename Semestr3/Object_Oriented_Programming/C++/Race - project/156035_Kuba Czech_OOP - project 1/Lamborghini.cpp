#include "Lamborghini.hpp"


    Lamborghini::Lamborghini(const std::string Driver, const int IdOfCar, float MalfunctionRate, float FuelOrEnergy, const bool Spoiler)
        : Hypercar("Lamborghini", Driver, IdOfCar, MalfunctionRate, FuelOrEnergy, Spoiler){}

    std::string Lamborghini::toString() const
    {
        return (mDriver + ", " + mManufacturer + ": " + std::to_string(mTravelledDistance));
    }

    void Lamborghini::takeTurn(float someDistance)
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
            float distance = std::max(1.00, 90.00 * (float)(rand())/(float)(RAND_MAX));
            if (someDistance - mTravelledDistance < 5.f)
                distance += 2.f;
            float FuelConsumption = (float) std::max(5* (float)(rand()) / (float)(RAND_MAX), float(1.6));

            if (mFuelOrEnergy < 40.0)
            {
                setTravelledDistance(distance * 0.6);
                setFuelOrEnergy(FuelConsumption * 0.35);
                //std::cout<<"Fuel management"<<std::endl;
                return;
            }
            else
            {
                if (mSpoiler == true)
                    setTravelledDistance(distance * 1.2);
                else
                    setTravelledDistance(distance);
                setFuelOrEnergy(FuelConsumption);
                return;
            }
        }
    }
