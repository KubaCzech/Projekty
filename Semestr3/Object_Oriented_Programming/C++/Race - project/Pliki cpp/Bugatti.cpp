#include "Hypercar.hpp"
#include "Hypercar.cpp"
#include "Lamborghini.hpp"

    Bugatti::Bugatti(const std::string Driver, const int IdOfCar, const float MalfunctionRate, float FuelOrEnergy, const bool Spoiler)
        : Hypercar::Hypercar("Bugatti", Driver, IdOfCar, MalfunctionRate, FuelOrEnergy, Spoiler)
    {
        //std::cout<<"Bugatti Veyron"<<std::endl;
    }

    std::string Bugatti::toString() const override
    {
        return (mDriver + ", " + mManufacturer + ": " + std::to_string(mTravelledDistance));
    }

    void Bugatti::takeTurn(float someDistance) override
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
                Bugatti::setTravelledDistance(distance * 0.8);
                Bugatti::setFuelOrEnergy(FuelConsumption * 0.3);
                //std::cout<<"Fuel management"<<std::endl;
            }
            else
            {
                if (mSpoiler == true)
                    Bugatti::setTravelledDistance(distance * 1.4);
                else
                    Bugatti::setTravelledDistance(distance);
                Bugatti::setFuelOrEnergy(FuelConsumption);
            }
        }
