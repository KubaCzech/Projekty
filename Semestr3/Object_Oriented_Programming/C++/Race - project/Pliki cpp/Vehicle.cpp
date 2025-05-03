#include "Vehicle.hpp"

    //constructor with parameters
    Vehicle::Vehicle(const std::string& Manufacturer, const std::string& Driver, const int IdOfCar,  float MalfunctionRate, float FuelOrEnergy)
        : mManufacturer(Manufacturer), mDriver(Driver), mIdOfCar(IdOfCar), mMalfunctionRate(MalfunctionRate), mTravelledDistance(0), mFuelOrEnergy(FuelOrEnergy)
    {}

    //Getters
    std::string Vehicle::getManufacturer() const
    {
        return mManufacturer;
    }

    std::string Vehicle::getDriver() const
    {
        return mDriver;
    }

    int Vehicle::getIdOfCar() const
    {
        return mIdOfCar;
    }

    float Vehicle::getMalfunctionRate() const
    {
        return mMalfunctionRate;
    }

    float Vehicle::getTravelledDistance() const
    {
        return mTravelledDistance;
    }

    float Vehicle::getFuelOrEnergy() const
    {
        return mFuelOrEnergy;
    }

    //Setters
    void Vehicle::setTravelledDistance(float dist)
    {
        mTravelledDistance += dist;
    }

    void Vehicle::setFuelOrEnergy(float FuelConsumption)
    {
        mFuelOrEnergy -= FuelConsumption;
    }
};
