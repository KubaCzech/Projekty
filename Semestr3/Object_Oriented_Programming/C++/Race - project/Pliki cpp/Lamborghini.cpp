#include "Lamborghini.hpp"
#include "Hypercar.hpp"
#include "Hypercar.cpp"


    Lamborghini::Lamborghini(const std::string Driver, const int IdOfCar, const float MalfunctionRate, float FuelOrEnergy, const bool Spoiler)
        : Hypercar::Hypercar("Lamborghini", Driver, IdOfCar, MalfunctionRate, FuelOrEnergy, Spoiler)
    {
        //std::cout<<"Lambordziiiiini"<<std::endl;
    }

    std::string Lamborghini::toString() const override
    {
        return (mDriver + ", " + mManufacturer + ": " + std::to_string(mTravelledDistance));
    }

    void Lamborghini::takeTurn(float someDistance) override
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
                Hypercar::setTravelledDistance(distance * 0.6);
                Hypercar::setFuelOrEnergy(FuelConsumption * 0.35);
                //std::cout<<"Fuel management"<<std::endl;
                return;
            }
            else
            {
                if (mSpoiler == true)
                    Hypercar::setTravelledDistance(distance * 1.2);
                else
                    Hypercar::setTravelledDistance(distance);
                Hypercar::setFuelOrEnergy(FuelConsumption);
                return;
            }
        }
