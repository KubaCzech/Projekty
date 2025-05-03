#include "F1Car.hpp"
#include "Vehicle.hpp"


    F1_car::F1_car(const std::string& Manufacturer, const std::string& Driver, const int IdOfCar, float MalfunctionRate, float FuelOrEnergy, const float Drs, const float Turbo)
        : Vehicle::Vehicle(Manufacturer, Driver, IdOfCar, MalfunctionRate, FuelOrEnergy), mDrs(Drs), mTurbo(Turbo), mDrsUsage(false) {}

    //getters
    float F1_car::getDrs() const
    {
        return mDrs;
    }

    float F1_car::getTurbo() const
    {
        return mTurbo;
    }

    bool F1_car::getDrsUsage()
    {
        return mDrsUsage;
    }
    //setters:
    void F1_car::setDrsUsage(float someDist)
    {
        if(mTravelledDistance/someDist <= 0.9 && someDist > 0)
            mDrsUsage = true;
        else
            mDrsUsage = false;
    }
