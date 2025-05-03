#include "Jaguar.hpp"
#include "FormulaECar.hpp"
#include "FormulaECar.cpp"


    Jaguar::Jaguar(const std::string Driver, const int IdOfCar, const float MalfunctionRate, float FuelOrEnergy, float Ers)
        : FormulaE_car::FormulaE_car("Jaguar", Driver, IdOfCar, MalfunctionRate, FuelOrEnergy, Ers)
    {
        //std::cout<<"Dzaguar"<<std::endl;
    }

    std::string Jaguar::toString() const override
    {
        return (mDriver + ", " + mManufacturer + ": " + std::to_string(mTravelledDistance));
    }

    void Jaguar::takeTurn(float someDistance) override
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

        if (prob < mMalfunctionRate + 0.1 && mFuelOrEnergy < 55.00)
        {
            mFuelOrEnergy = 100.f;
        }
        else
        {
            float distance = std::max(1.00, 75.00 * (float)(rand())/(float)(RAND_MAX));
            float EnergyConsumption = std::max(3 * (float)(rand()) / (float)(RAND_MAX), float(1.5));

            if (prob2 < 0.8)
            {
                Jaguar::setTravelledDistance(distance * (1+mErs));
                Jaguar::setFuelOrEnergy(EnergyConsumption * 1.2);
                return;
            }
            else
            {
                Jaguar::setTravelledDistance(distance);
                Jaguar::setFuelOrEnergy(EnergyConsumption);
                return;
            }
        }
