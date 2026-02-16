#include <iostream>
#include <stdlib.h>
#include <chrono>
#include <ctime>
// #include <bits/stdc++.h>

using namespace std;

struct node
{
    int value;
    struct node *next;
};

struct node *head = NULL;

void insert_data(int new_value)
{
    node *new_node = (struct node *)malloc(sizeof(struct node));
    new_node->value = new_value;
    new_node->next = head;
    head = new_node;
}

void display_list()
{
    struct node *pointer;
    pointer = head;
    while (pointer != NULL)
    {
        cout << pointer->value << ' ';
        pointer = pointer->next;
    }
    cout << "xd" << endl;
}

void fill_list(int s)
{ // filling list with random numbers
    for (int i = 0; i < s; i++)
    {
        insert_data(rand() % (s + 1));
    }
}

bool check_existance(int n)
{
    struct node *pointer;
    pointer = head;
    while (pointer != NULL)
    {
        if (n == pointer->value)
            return true;
        pointer = pointer->next;
    }
    return false;
}

void delete_element(int n)
{
    struct node *temp = head->next;
    struct node *prev = head;
    if (prev->value == n) // deleting from the beginning
    {
        head = head->next;
        free(temp);
        return;
    }
    while (temp->value != n && temp != NULL)
    {
        prev = temp;
        temp = temp->next;
    }
    if (temp == NULL)
        return; // number not found
    // cout<<"yes"<<endl;
    prev->next = temp->next; // remove node
    free(temp);              // free memory
}

void min_max_values()
{
    struct node *pointer;
    pointer = head;
    int mini;
    int maxi;
    while (pointer != NULL)
    {
        if (pointer == head)
        {
            mini = pointer->value;
            maxi = pointer->value;
        }
        else
        {
            if (pointer->value > maxi)
                maxi = pointer->value;
            if (pointer->value < mini)
                mini = pointer->value;
        }
        pointer = pointer->next;
    }
    cout << "Minimal value is: " << mini << ", maximal value is: " << maxi << endl;
}

void check_size()
{
    struct node *pointer;
    pointer = head;
    int counter = 0;
    while (pointer != NULL)
    {
        counter++;
        pointer = pointer->next;
    }
    cout << counter << endl;
}

void destroy_list()
{
    head = NULL;
}

void display_table(double T[11])
{
    for (int i = 0; i < 11; i++)
        cout << T[i] << endl;
}

int main()
{
    struct timespec start, finish;
    double table[11][10];
    double table_avg[11];
    double time_taken;
    int T[11] = {5, 10, 50, 100, 200, 500, 1000, 2000, 5000, 10000, 50000};
    for (int j = 0; j < 10; j++)
        for (int i = 0; i < 11; i++)
        {
            node *head = NULL;
            fill_list(T[i]);
            // display_list();
            // min_max_values();
            // check_size();
            // delete_element(8);
            // display_list();
            clock_gettime(CLOCK_MONOTONIC, &start);
            ios_base::sync_with_stdio(false);
            check_existance(T[i] + 1);
            clock_gettime(CLOCK_MONOTONIC, &finish);
            time_taken = (finish.tv_sec - start.tv_sec) * 1e9;
            time_taken = (time_taken + (finish.tv_nsec - start.tv_nsec)) * 1e-9;
            table[i][j] = time_taken;
            destroy_list();
        }
    for (int i = 0; i < 11; i++)
    {
        double summ = 0;
        for (int j = 0; j < 10; j++)
            summ += table[i][j];
        table_avg[i] = summ / 10;
    }
    display_table(table_avg);
    return 0;
}
