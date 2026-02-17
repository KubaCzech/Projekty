#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include <pthread.h>

#define N 1000                  // number of visitors in our museum
#define sec_wait 3              // maximal time in A and B
#define A_capacity 100          // capacity of hall A
#define B_capacity 50		// capacity of hall B
#define short_version 1         // if results should be writen in the form of stats (list of all visitors otherwise)

int a_to_go=A_capacity;       // maximum of people that can go to A
int b_to_go=B_capacity;       // maximum of people in B
int threadsCompleted=0;         // to check if all threads have terminated

char st[N];			//status of all visitors

pthread_mutex_t mx;             // introducing mutex and conditional variables
pthread_cond_t cond_a;          // for entering A
pthread_cond_t cond_b;          // for entering B

void enter_A(int n) {
        pthread_mutex_lock(&mx);
        while (a_to_go <=1 ) {			 // we leave one place in A for those in B who want to leave and enter hall A once again(preventing deadlock)
                pthread_cond_wait(&cond_a, &mx); // waiting for permission to enter the museum
        }
        a_to_go--;
        st[n] = 'A';
        pthread_mutex_unlock(&mx);
}

//We have only one case after visiting B - enter A once again

void enter_A_from_B(int n) {
        pthread_mutex_lock(&mx);
        while (a_to_go == 0) { //checking if there is free place
                pthread_cond_wait(&cond_a, &mx); // waiting in the hall B
        }
        a_to_go--;
        b_to_go++;
        st[n] = 'A';
        pthread_cond_signal(&cond_b); // someone may enter the hall B
        pthread_mutex_unlock(&mx);
}

//We have two cases after visiting A - enter_B or leave

void enter_B(int n) {
        pthread_mutex_lock(&mx);
        while (b_to_go == 0) { //checking if there is a free place
                pthread_cond_wait(&cond_b, &mx); // waiting in the hall A
        }
        b_to_go--;
        a_to_go++;
        st[n] = 'B';
        pthread_cond_signal(&cond_a); // someone may enter the hall A
        pthread_mutex_unlock(&mx);
}

void leave(int n) {
        pthread_mutex_lock(&mx);
        a_to_go++; //someone leaves, someone can enter A
        st[n] = '|';
        pthread_cond_signal(&cond_a);
        pthread_mutex_unlock(&mx);
}

void* visitor(void* info) {
        int id = *(int*)info;

        enter_A(id); // enter the museum
        sleep(rand()%sec_wait+1); // stay in hall A for some time

        if (rand()%2) { // with probability half
                enter_B(id); // enter hall B
                sleep(rand()%sec_wait+1); // stay in hall B for some time
                enter_A_from_B(id); // come back to A
        }

        leave(id); // leave the museum
        threadsCompleted++;

        return NULL;
}

void printStats(int k) {
        int inA=0, inB=0, outside=0, terminated=0;
        for (int i=0; i<N; i++) {
                if (st[i] == 'O') {
                        outside++;
                } else if (st[i] == 'A') {
                        inA++;
                } else if (st[i] == 'B') {
                        inB++;
                } else {
                        terminated++;
                }
        }
        printf("%3d:", k);
        printf("   A: %4d   B: %4d   Waiting: %4d   Gone: %4d\n", inA, inB, outside, terminated);
}

void printTable(int k) {
        printf("%3d:", k);
        for (int i=0; i<N; i++) {
                printf("   %c", st[i]);
        }
        printf("\n");
}

int main() {
        pthread_t th[N];
        int tid[N], k=0;

        pthread_mutex_init(&mx, NULL);
        pthread_cond_init(&cond_a, NULL);
        pthread_cond_init(&cond_b, NULL);

        for (int i=0; i<N; i++) { // create N visitors
                tid[i]=i;
                st[i] = 'O';
                pthread_create(&th[i], NULL, visitor, &tid[i]);
        }

        if (short_version) { // print current state as a short line of statistics
                while(threadsCompleted < N) {
                        printStats(k);
                        k++;
                        sleep(1);
                }
                printStats(k);
        } else { // print current state in a form of a table
                while(threadsCompleted < N) {
                        printTable(k);
                        k++;
                        sleep(1);
                }
                printTable(k);
        }

        for (int i=0; i<N; i++) { // close all threads
                pthread_join(th[i], NULL);
        }

	return 0;
}
     
