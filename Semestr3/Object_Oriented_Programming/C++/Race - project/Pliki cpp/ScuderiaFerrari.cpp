#include "ScuderiaFerrari.hpp"
#include "F1Car.cpp"
#include "F1Car.hpp"


    ScuderiaFerrari::ScuderiaFerrari(const std::string& Driver, const int IdOfCar, float MalfunctionRate, float FuelOrEnergy, const float Drs, const float Turbo)
        : F1_car::F1_car("Ferrari", Driver, IdOfCar, MalfunctionRate, FuelOrEnergy, Drs, Turbo) {}

    std::string ScuderiaFerrari::toString() const override
    {
        return (mDriver + ", " + mManufacturer + ": " + std::to_string(mTravelledDistance));
    }

    void ScuderiaFerrari::takeTurn(float someDistance) override
    {
        float prob = float (rand()) / float (RAND_MAX); //Which move to do
        float prob2 = float (rand()) / float (RAND_MAX); //Which 'special action' to use
        if (mFuelOrEnergy <= 0)
        {
            //std::cout<<"Ferrari of "<<mDriver<<" is out of fuel"<<std::endl;
            mFuelOrEnergy = 0;
            return;
        }

        if (prob < mMalfunctionRate)
        {
            //std::cout<<"Ferrari has a malfunction and stopped on track"<<std::endl;
            //std::cout<<prob<<" "<<0.1 + mMalfunctionRate<<std::endl;
            mMalfunctionRate = 1.0;
            return;
        }

        if (prob < 0.1 + mMalfunctionRate && mMalfunctionRate < 1.f && mFuelOrEnergy < 80.00)
        {
            //std::cout<<"Ferrari of "<<mDriver<<" pitted and refuelled"<<std::endl;
            mFuelOrEnergy = 100.00;
            return;
        }

        else
        {
            F1_car::setDrsUsage(someDistance);
            float distance = std::max(1.00, 100.00 * (float)(rand())/(float)(RAND_MAX));
            if (prob2 < 0.9)
                distance += mTurbo;
            if (mDrsUsage == true)
                distance *= 1.00+mDrs;
            F1_car::setTravelledDistance(distance);
            F1_car::setFuelOrEnergy(std::max(5 * float (rand()) / float (RAND_MAX), 1.f));
            std::cout<<"Ferrari of "<<mDriver<<" travelled: "<<mTravelledDistance<<", fuel left: "<<mFuelOrEnergy<<std::endl;
            return;

        }
