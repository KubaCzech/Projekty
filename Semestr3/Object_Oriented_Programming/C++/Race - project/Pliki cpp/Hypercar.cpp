#include "Hypercar.hpp"
#include "Vehicle.hpp"
#include "Vehicle.cpp"

    Hypercar::Hypercar(const std::string& Manufacturer, const std::string& Driver, const int IdOfCar, float MalfunctionRate, float FuelOrEnergy, const bool Spoiler)
        : Vehicle::Vehicle(Manufacturer, Driver, IdOfCar, MalfunctionRate, FuelOrEnergy), mSpoiler(Spoiler) {}
    //getters
    bool Hypercar::getSpoiler() const
    {
        return mSpoiler;
    }
