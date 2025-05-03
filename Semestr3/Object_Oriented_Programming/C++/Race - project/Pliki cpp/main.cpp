#include <iostream>
#include <cmath>
#include <cstdlib>
#include <ctime>
#include <vector>
#include <string>
#include <algorithm>

class Vehicle
{
public:
    //constructor with parameters
    Vehicle(const std::string& Manufacturer, const std::string& Driver, const int IdOfCar,  float MalfunctionRate, float FuelOrEnergy)
        : mManufacturer(Manufacturer), mDriver(Driver), mIdOfCar(IdOfCar), mMalfunctionRate(MalfunctionRate), mTravelledDistance(0), mFuelOrEnergy(FuelOrEnergy)
    {}

    virtual ~Vehicle(){}
    virtual std::string toString() const =0;
    virtual void takeTurn(float someDistance) =0;
    //Getters
    std::string getManufacturer() const
    {
        return mManufacturer;
    }

    std::string getDriver() const
    {
        return mDriver;
    }

    int getIdOfCar() const
    {
        return mIdOfCar;
    }

    float getMalfunctionRate()
    {
        return mMalfunctionRate;
    }

    float getTravelledDistance()
    {
        return mTravelledDistance;
    }

    float getFuelOrEnergy()
    {
        return mFuelOrEnergy;
    }

    //Setters
    void setTravelledDistance(float dist)
    {
        mTravelledDistance += dist;
    }

    void setFuelOrEnergy(float FuelConsumption)
    {
        mFuelOrEnergy -= FuelConsumption;
    }


protected:
    std::string mManufacturer;
    std::string mDriver;
    int mIdOfCar;
    float mMalfunctionRate;
    float mTravelledDistance;
    float mFuelOrEnergy;

};

class F1_car : public Vehicle
{
public:
    F1_car(const std::string& Manufacturer, const std::string& Driver, const int IdOfCar, float MalfunctionRate, float FuelOrEnergy, const float Drs, const float Turbo)
        : Vehicle(Manufacturer, Driver, IdOfCar, MalfunctionRate, FuelOrEnergy), mDrs(Drs), mTurbo(Turbo), mDrsUsage(false) {}

    virtual void takeTurn(float someDistance) =0;
    virtual std::string toString() const =0;
    //getters
    float getDrs() const
    {
        return mDrs;
    }

    float getTurbo() const
    {
        return mTurbo;
    }

    bool getDrsUsage()
    {
        return mDrsUsage;
    }

    void setDrsUsage(float someDist)
    {
        if(mTravelledDistance/someDist <= 0.9 && someDist > 0)
            mDrsUsage = true;
        else
            mDrsUsage = false;
    }

protected:
    float mDrs;
    float mTurbo;
    bool mDrsUsage;
};

class FormulaE_car : public Vehicle
{
public:
    FormulaE_car(const std::string& Manufacturer, const std::string& Driver, const int IdOfCar, const float MalfunctionRate, float FuelOrEnergy, float Ers)
        : Vehicle(Manufacturer, Driver, IdOfCar, MalfunctionRate, FuelOrEnergy), mErs(Ers){}
    virtual void takeTurn(float someDistance) =0;
    virtual std::string toString() const =0;
    //getters
    float getErs()
    {
        return mErs;
    }

protected:
    float mErs;
};

class Hypercar : public Vehicle
{
public:
    Hypercar(const std::string& Manufacturer, const std::string& Driver, const int IdOfCar, float MalfunctionRate, float FuelOrEnergy, const bool Spoiler)
        : Vehicle(Manufacturer, Driver, IdOfCar, MalfunctionRate, FuelOrEnergy), mSpoiler(Spoiler) {}
    virtual void takeTurn(float someDistance)=0;
    virtual std::string toString() const =0;
    //getters
    bool getSpoiler() const
    {
        return mSpoiler;
    }

protected:
    bool mSpoiler;
};

class ScuderiaFerrari : public F1_car
{
public:
    ScuderiaFerrari(const std::string& Driver, const int IdOfCar, float MalfunctionRate, float FuelOrEnergy, const float Drs, const float Turbo)
        : F1_car("Ferrari", Driver, IdOfCar, MalfunctionRate, FuelOrEnergy, Drs, Turbo)
    {
        std::cout<<"FORZA FERRARI!!!"<<std::endl;
    }

    std::string toString() const override
    {
        return (mDriver + ", " + mManufacturer + ": " + std::to_string(mTravelledDistance));
    }

    void takeTurn(float someDistance) override
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
            std::cout<<"Ferrari has a malfunction and stopped on track"<<std::endl;
            std::cout<<prob<<" "<<0.1 + mMalfunctionRate<<std::endl;
            mMalfunctionRate = 1.0;
            return;
        }

        if (prob < 0.1 + mMalfunctionRate && mMalfunctionRate < 1.f && mFuelOrEnergy < 80.00)
        {
            std::cout<<"Ferrari of "<<mDriver<<" pitted and refuelled"<<std::endl;
            mFuelOrEnergy = 100.00;
            return;
        }

        else
        {
            setDrsUsage(someDistance);
            float distance = std::max(1.00, 100.00 * (float)(rand())/(float)(RAND_MAX));
            if (prob2 < 0.9)
                distance += mTurbo;
            if (mDrsUsage == true)
                distance *= 1.00+mDrs;
            setTravelledDistance(distance);
            setFuelOrEnergy(std::max(5 * float (rand()) / float (RAND_MAX), 1.f));
            std::cout<<"Ferrari of "<<mDriver<<" travelled: "<<mTravelledDistance<<", fuel left: "<<mFuelOrEnergy<<std::endl;
            return;

        }

    }
};

class MercedesAMGPetronas : public F1_car
{
public:
    MercedesAMGPetronas(const std::string Driver, const int IdOfCar, float MalfunctionRate, float FuelOrEnergy, const float Drs, const float Turbo)
        : F1_car("Mercedes", Driver, IdOfCar, MalfunctionRate, FuelOrEnergy, Drs, Turbo)
    {
        std::cout<<"Mercedes, Mercedes uber alles"<<std::endl;
    }

    std::string toString() const override
    {
        return (mDriver + ", " + mManufacturer + ": " + std::to_string(mTravelledDistance));
    }

    void takeTurn(float someDist) override
    {
        float prob = float (rand()) / float (RAND_MAX); //Which move to do
        if (mFuelOrEnergy <= 0)
        {
            //std::cout<<"Mercedes of "<<mDriver<<" is out of fuel"<<std::endl;
            mFuelOrEnergy = 0;
            return;
        }

        if (prob < mMalfunctionRate)
        {
            mMalfunctionRate = 1.0;
            return;
        }

        if (prob < 0.12 + mMalfunctionRate && mMalfunctionRate < 1.f && mFuelOrEnergy < 70.00)
        {
            mFuelOrEnergy = 90.00;
            return;
        }

        else
        {
            setDrsUsage(someDist);
            float distance = std::max(2.00, 80.00 * (float)(rand())/(float)(RAND_MAX));
            if (mDrsUsage == true)
                distance *= 1.00+mDrs;
            setTravelledDistance(distance);
            setFuelOrEnergy(std::max(8 * float (rand()) / float (RAND_MAX), 2.f));
            return;

        }
    }
};

class RedBullRacing : public F1_car
{
public:
    RedBullRacing(const std::string Driver, const int IdOfCar, float MalfunctionRate, float FuelOrEnergy, const float Drs, const float Turbo)
        : F1_car("Red Bull", Driver, IdOfCar, MalfunctionRate, FuelOrEnergy, Drs, Turbo)
    {
        //std::cout<<"*Dutch anthem being played*"<<std::endl;
    }

    std::string toString() const override
    {
        return (mDriver + ", " + mManufacturer + ": " + std::to_string(mTravelledDistance));
    }

    void takeTurn(float someDistance) override
    {
        float prob = float (rand()) / float (RAND_MAX); //Which move to do
        float prob2 = float (rand()) / float (RAND_MAX); //Which 'special action' to use
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

        if (prob < 0.15 + mMalfunctionRate && mMalfunctionRate < 1.f && mFuelOrEnergy < 50.0)
        {
            mFuelOrEnergy = 75.00;
            return;
        }

        else
        {
            setDrsUsage(someDistance);
            float distance = std::max(1.00, 90.00 * (float)(rand())/(float)(RAND_MAX));
            if (prob2 < 0.9)
                distance += mTurbo;
            setTravelledDistance(distance);
            setFuelOrEnergy(std::max(7 * float (rand()) / float (RAND_MAX), (float) 1.8));
            return;

        }
    }
};

class Lamborghini : public Hypercar
{
public:
    Lamborghini(const std::string Driver, const int IdOfCar, const float MalfunctionRate, float FuelOrEnergy, const bool Spoiler)
        : Hypercar("Lamborghini", Driver, IdOfCar, MalfunctionRate, FuelOrEnergy, Spoiler)
    {
        //std::cout<<"Lambordziiiiini"<<std::endl;
    }

    std::string toString() const override
    {
        return (mDriver + ", " + mManufacturer + ": " + std::to_string(mTravelledDistance));
    }

    void takeTurn(float someDistance) override
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
                std::cout<<"Fuel management"<<std::endl;
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
};

class Bugatti : public Hypercar
{
public:
    Bugatti(const std::string Driver, const int IdOfCar, const float MalfunctionRate, float FuelOrEnergy, const bool Spoiler)
        : Hypercar("Bugatti", Driver, IdOfCar, MalfunctionRate, FuelOrEnergy, Spoiler)
    {
        //std::cout<<"Bugatti Veyron"<<std::endl;
    }

    std::string toString() const override
    {
        return (mDriver + ", " + mManufacturer + ": " + std::to_string(mTravelledDistance));
    }

    void takeTurn(float someDistance) override
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
                std::cout<<"Fuel management"<<std::endl;
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
};

class Jaguar : public FormulaE_car
{
public:
    Jaguar(const std::string Driver, const int IdOfCar, const float MalfunctionRate, float FuelOrEnergy, float Ers)
        : FormulaE_car("Jaguar", Driver, IdOfCar, MalfunctionRate, FuelOrEnergy, Ers)
    {
        //std::cout<<"Dzaguar"<<std::endl;
    }

    std::string toString() const override
    {
        return (mDriver + ", " + mManufacturer + ": " + std::to_string(mTravelledDistance));
    }

    void takeTurn(float someDistance) override
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
                setTravelledDistance(distance * (1+mErs));
                setFuelOrEnergy(EnergyConsumption * 1.2);
                return;
            }
            else
            {
                setTravelledDistance(distance);
                setFuelOrEnergy(EnergyConsumption);
                return;
            }
        }
    }
};

class Porsche : public FormulaE_car
{
public:
    Porsche(const std::string Driver, const int IdOfCar, const float MalfunctionRate, float FuelOrEnergy, float Ers)
        : FormulaE_car("Porsche", Driver, IdOfCar, MalfunctionRate, FuelOrEnergy, Ers)
    {
        //std::cout<<"Favourite vehicle of Osama Bin Laden - Porsche 9/11"<<std::endl;
    }

    std::string toString() const override
    {
        return (mDriver + ", " + mManufacturer + ": " + std::to_string(mTravelledDistance));
    }

    void takeTurn(float someDistance) override
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
};

template <class V>
class Race{
protected:
    std::vector<V> vehicles;
    int driversInRace = 0;

public:
    int numberOfLaps;
    int numberOfVehicles;

    //Memory deallocation at the end
    ~Race(){
        int index=vehicles.size() - 1;
        while(vehicles.size() > 0){
            *this -= index;
            index--;
        }
    }
    void operator+=(const V& veh)
    {
        vehicles.push_back(veh);
    }

    void operator-=(int k)
    {
        vehicles.erase(vehicles.begin() + k);
    }

    void displayResults()
    {
        std::cout<<"Final results: "<<std::endl;
        for (int a=0; a<vehicles.size(); a++)
        {
            std::cout<<a+1<<". "<<vehicles[a]->getManufacturer()<<", "<<vehicles[a]->getDriver()<<std::endl;
            std::cout<<"Distance driven: "<<vehicles[a]->getTravelledDistance()<<", fuel left: "<<vehicles[a]->getFuelOrEnergy()<<std::endl;
            std::cout<<std::endl;
        }
    }

    void Factory()
    {
        std::vector <std::string> allDrivers= {"Lewis Hamilton", "Ayrton Senna", "Max Verstappen", "Kimi Raikkonen", "Fernando Alonso", "Sergio Perez", "George Russel", "Nico Rosberg", "Jenson Button", "Stoffel Vandorne", "Nick de Vries", "Lando Norris", "Oscar Piastri", "Mika Hakkinen", "Alain Prost"};
        std::vector <std::string> allFerrariDrivers = {"Charles Leclerc", "Felipe Massa", "Michael Schumacher", "Sebastian Vettel", "Carlos Sainz", "Niki Lauda"};
        std::vector <int>DriversIds = {44, 3, 33, 7, 14, 11, 63, 13, 85, 6, 21, 4, 81, 91, 46};
        std::vector <int>FerrariIds = {16, 2, 1, 5, 55, 99};

        //std::cout<<numberOfVehicles<<std::endl;
        for (int i=0; i<numberOfVehicles; i++)
        {
            std::cout<<"Vehicle number "<<i+1<<std::endl;
            int prob = rand()%8;
            std::cout<<prob<<std::endl;
            float prob2 = (float)(rand())/(float)(RAND_MAX);
            bool spoilerOrNot;
            std::string driverToPut;
            int idToPut;
            if (prob <2){
                int index = rand()% allFerrariDrivers.size();
                driverToPut = allFerrariDrivers[index];
                idToPut = FerrariIds[index];
                allFerrariDrivers.erase(allFerrariDrivers.begin()+index);
                FerrariIds.erase(FerrariIds.begin()+index);
            }
            else{
                int index = rand()%allDrivers.size();
                driverToPut = allDrivers[index];
                idToPut = DriversIds[index];
                allDrivers.erase(allDrivers.begin() + index);
                DriversIds.erase(DriversIds.begin() + index);
                if (prob2 <(float)(0.5))
                    spoilerOrNot = false;
                else
                    spoilerOrNot = true;
            }
            switch (prob){
            case 0:
                *this += new ScuderiaFerrari(driverToPut, idToPut, 0.f, std::max(90.f, (float) 110.00 * (float)(rand())/(float)(RAND_MAX)), std::min((float) 0.3, (float)(rand()/(float)(RAND_MAX))), std::min(15.f, 30 * (float)(rand()) / (float)(RAND_MAX)));
                break;
            case 1:
                *this += new ScuderiaFerrari(driverToPut, idToPut, 0.f, std::max(90.f, (float) 110.00 * (float)(rand())/(float)(RAND_MAX)), std::min((float) 0.3, (float)(rand()/(float)(RAND_MAX))), std::min(15.f, 30 * (float)(rand()) / (float)(RAND_MAX)));
                break;
            case 2:
                *this += new RedBullRacing(driverToPut, idToPut, std::max((float) 0.01, (float) 0.08 * (float)(rand())/(float)(RAND_MAX)), std::max(75.f, (float) 90.00 * (float)(rand())/(float)(RAND_MAX)), std::min((float) 0.4, (float)(rand()/(float)(RAND_MAX))), std::min(10.f, 20 * (float)(rand()) / (float)(RAND_MAX)));
                break;
            case 3:
                *this += new Lamborghini(driverToPut, idToPut, 0.f, std::max(90.f, (float) 150*(float)(rand())/(float)(RAND_MAX)), spoilerOrNot);
                break;
            case 4:
                *this += new Bugatti(driverToPut, idToPut, 0.05, std::max(80.f, (float) 120*(float)(rand())/(float)(RAND_MAX)), spoilerOrNot);
                break;
            case 5:
                *this += new Jaguar(driverToPut, idToPut, 0.1, std::max(150.f, (float) 200*(float)(rand())/(float)(RAND_MAX)), std::max(0.15, 0.5 * (float)(rand())/(float)(RAND_MAX)));
                break;
            case 6:
                *this += new Porsche(driverToPut, idToPut, 0.03, std::max(130.f, (float) 170*(float)(rand())/(float)(RAND_MAX)), std::max(0.25, 0.9 * (float)(rand())/(float)(RAND_MAX)));
                break;
            case 7:
                *this += new MercedesAMGPetronas(driverToPut, idToPut, std::max(0.005, 0.01 * (float)(rand())/(float)(RAND_MAX)), std::max(80.f, 100*(float)(rand())/(float)(RAND_MAX)), std::min((float) 0.2, 2*(float)(rand())/(float)(RAND_MAX)), std::min(20.f, 35 * (float)(rand())/(float)(RAND_MAX)));
                break;
            }

        }
    }
    void sortVector()
    {
        //std::vector<V> sortedVehicles = vehicles;
        /*for (int i=0; i<vehicles.size(); i++){
            for (int j=i; j<vehicles.size(); j++)
                if (vehicles[i]->getTravelledDistance() < vehicles[i]->getTravelledDistance())
        }*/
        std::sort(vehicles.begin(), vehicles.end(), [](const V& a, const V& b){
                  return a->getTravelledDistance() > b->getTravelledDistance();
            });
    }

    void Run()
    {
        std::cout<<"Insert number of turns"<<std::endl;
        std::cin>>numberOfLaps;
        std::cout<<"Insert number of vehicles participating"<<std::endl;
        std::cin>>numberOfVehicles;
        driversInRace = numberOfVehicles;
        std::cout<<"Factory time"<<std::endl;
        Factory();
        std::cout<<"All cars are constructed"<<std::endl;
        std::cout<<"Let's race"<<std::endl;
        for (int i=0; i<numberOfLaps && driversInRace > 0; i++){
            driversInRace = numberOfVehicles;
            for (int j=0; j<(int)vehicles.size(); j++){
                float someDistance;
                if (j == (int) vehicles.size()-1)
                    someDistance = 2* vehicles[j]->getTravelledDistance();
                else
                    someDistance = vehicles[j+1]->getTravelledDistance();
                if (vehicles[j]->getFuelOrEnergy() <=0 or vehicles[j]->getMalfunctionRate() == 1.0)
                    driversInRace--;
                vehicles[j]->takeTurn(someDistance);
                std::cout<<vehicles[j]->toString()<<std::endl;
            }
            sortVector();
        }
        if (driversInRace < 1)
            std::cout<<"Race finished earlier because all drivers are out of Race"<<std::endl;
        displayResults();
        std::cout<<111<<std::endl;

    }
};

int main()
{
    std::srand(std::time(NULL));
    Race<Vehicle*> race;
    race.Run();
    return 0;
}
