#include <iostream>
#include <thread>

class Pokemon
{
public:
   //constructor with parameters
   Pokemon(const std::string& name, int attack, int defense, int frozen, int health)
      : mName(name), mAttack(attack), mDefense(defense), mFrozen(frozen), mHealth(health)
   {}

   //virtual method which should be implemented in child classes
   virtual void takeTurn(Pokemon& other)
   {
      std::cout << mName << " is doing nothing" << std::endl;
   }

   //getters
   //const at the end meands that method is redonly
   //(class members can't be modified)
   std::string getName() const
   {
      return mName;
   }

   int getAttack() const
   {
      return mAttack;
   }

   int getDefense() const
   {
      return mDefense;
   }

   int getHealth() const
   {
      return mHealth;
   }

   //setters
   void setAttack(int attack)
   {
      mAttack = attack;
   }

   void setFrozen(int frozen)
   {
      mFrozen = frozen;
   }

   Pokemon& operator+=(int health)
   {
      mHealth += health;
      return *this;
   }

   Pokemon& operator-=(int health)
   {
      mHealth -= health;
      return *this;
   }
    //???
   friend std::ostream& operator<<(std::ostream& os, const Pokemon& pokemon);

protected:
   std::string mName;
   int mAttack;
   int mDefense;
   int mFrozen;
   int mHealth;
};

std::ostream& operator<<(std::ostream& os, const Pokemon& pokemon)
{
   os << pokemon.mName << " attack: " << pokemon.mAttack << " defense: " <<
      pokemon.mDefense << " frozen: " << pokemon.mFrozen << " health: " << pokemon.mHealth;
   return os;
}

class Bulbasaur : public Pokemon
{
public:
   Bulbasaur() : Pokemon("Bulbasaur", 49, 49, 0, 45)
   {}

   //dynamic polymorphism
   void takeTurn(Pokemon& other)
   {
      if (mFrozen > 0)
      {
         std::cout << mName << " is frozen!" << std::endl;
         --mFrozen;
         return;
      }
      std::cout << "g - growl" << std::endl;
      std::cout << "t - tackle" << std::endl;
      std::cout << "w - wait" << std::endl;
      char action;
      std::cin >> action;
      if (action == 'g')
      {
         if (other.getAttack() > 5)
         {
            other.setAttack(other.getAttack() - 5);
            std::cout << mName << " used growl" << std::endl;
         }
         else
         {
            std::cout << mName << " failed to use growl" << std::endl;
         }
      }
      else if (action == 't')
      {
         other -= (int)((100.f - (float)other.getDefense()) / 100.f) * (float)mAttack;
         std::cout << mName << " used tackle" << std::endl;
      }
      else
      {
         std::cout << mName << " waited" << std::endl;
      }
   }
};

class Pikachu : public Pokemon
{
public:
   Pikachu() : Pokemon("Pikachu", 55, 40, 0, 35)
   {}

   //dynamic polymorphism
   void takeTurn(Pokemon& other)
   {
      if (mFrozen > 0)
      {
         std::cout << mName << " is frozen!" << std::endl;
         --mFrozen;
         return;
      }
      std::cout << "c - charm" << std::endl;
      std::cout << "n - nuzzle" << std::endl;
      std::cout << "q - quick attack" << std::endl;
      std::cout << "w - wait" << std::endl;
      char action;
      std::cin >> action;
      if (action == 'c')
      {
         other.setFrozen(1);
         std::cout << mName << " used charm" << std::endl;
      }
      else if (action == 'n')
      {
         if (other.getAttack() > 3)
         {
            other.setAttack(other.getAttack() - 3);
            std::cout << mName << " used nuzzle" << std::endl;
         }
         else
         {
            std::cout << mName << " failed to use nuzzle" << std::endl;
         }
      }
      else if (action == 'q')
      {
         other -= (int)((100.f - (float)other.getDefense()) / 100.f) * (float)mAttack;
         std::cout << mName << " used quick attack" << std::endl;
      }
      else
      {
         std::cout << mName << " waited" << std::endl;
      }
   }
};

//main class simulation
class Simulation
{
public:
   //destructor
   ~Simulation()
   {
      //dynamic memory deallocation. Important!
      delete mPokemon1;
      delete mPokemon2;
   }

   //main function
   int run()
   {
      if (!draft())
         return 1;

      if (!battle())
         return 1;

      return 0;
   }

private:
   void printAvailablePokemons()
   {
      std::cout << "p - pikachu" << std::endl;
      std::cout << "b - bulbasaur" << std::endl;
   }

   void printBorder()
   {
      std::cout << "-------------------" << std::endl;
   }

   void printPokemonsInfo()
   {
      std::cout << "Pokemons info: " << std::endl;
      std::cout << *mPokemon1 << std::endl;
      std::cout << *mPokemon2 << std::endl;
   }

   void waitAndClear()
   {
      //Sleep(2000); only windows
      std::this_thread::sleep_for(std::chrono::seconds(2)); //cross-platform
      system("cls"); //only windows
      //system("clear"); linux etc.
   }

   Pokemon* createPokemonForPlayer(int playerNumber)
   {
      std::cout << "Player " << playerNumber << " pokemon: ";
      char p;
      std::cin >> p;
      if (p == 'p')
      {
         return new Pikachu();
      }
      else if (p == 'b')
      {
         return new Bulbasaur();
      }
      else
      {
         std::cout << "This pokemon doesn't exist!" << std::endl;
      }
      return nullptr;
   }

   //draft phase
   bool draft()
   {
      printAvailablePokemons();
      mPokemon1 = createPokemonForPlayer(1);
      if (mPokemon1 == nullptr)
         return false;

      mPokemon2 = createPokemonForPlayer(2);
      if (mPokemon2 == nullptr)
         return false;

      return true;
   }

   //battle phase
   bool battle()
   {
      std::cout << mPokemon1->getName() << " vs " << mPokemon2->getName() << std::endl;
      std::cout << "Battle is started!" << std::endl;
      waitAndClear();

      while (mPokemon1->getHealth() > 0 && mPokemon2->getHealth() > 0)
      {
         printPokemonsInfo();
         printBorder();
         if (mPokemon1startTurn)
         {
            mPokemon1->takeTurn(*mPokemon2);
            printBorder();
            mPokemon2->takeTurn(*mPokemon1);
            mPokemon1startTurn = false;
         }
         else
         {
            mPokemon2->takeTurn(*mPokemon1);
            printBorder();
            mPokemon1->takeTurn(*mPokemon2);
            mPokemon1startTurn = true;
         }
         waitAndClear();
      }
      std::cout << "The battle is over!" << std::endl;
      printPokemonsInfo();
      return true;
   }

   bool mPokemon1startTurn = true;

   Pokemon* mPokemon1;
   Pokemon* mPokemon2;
};

int main()
{
   Simulation sim;
   return sim.run();
}
