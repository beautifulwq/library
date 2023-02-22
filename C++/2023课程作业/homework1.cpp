#include <iostream>
#include <time.h>
#include <stdlib.h>
#include <random>

using namespace std;
void func1(double a, double b, char type)
{
    if (type == '+')
    {
        cout << a << '+' << b << '=' << a + b << endl;
    }
    else if (type == '-')
    {
        cout << a << '-' << b << '=' << a - b << endl;
    }
    else if (type == '*')
    {
        cout << a << '*' << b << '=' << a * b << endl;
    }
    else if (type == '/')
    {
        if (b == 0)
        {
            cout << "error a/0" << endl;
            return;
        }
        else
        {
            cout << a << '/' << b << '=' << a / b << endl;
        }
    }
}

void func2()
{
    int **p = new int *[3];
    for (int i = 0; i < 3; ++i)
    {
        p[i] = new int[5];
    }
    cout << "15 int" << endl;

    for (int i = 0; i < 3; ++i)
    {
        for (int j = 0; j < 5; ++j)
        {
            cin >> p[i][j];
        }
    }

    int max = p[0][0], min = p[0][0];
    for (int i = 0; i < 3; ++i)
    {
        for (int j = 0; j < 5; ++j)
        {

            if (max < p[i][j])
                max = p[i][j];
            if (min > p[i][j])
                min = p[i][j];
        }
    }
    cout << "max " << max << endl
         << "min " << min << endl;
    for (int i = 0; i < 3; ++i)
        delete[] p[i];
    delete[] p;
    return;
}

void func3()
{
    int cnt = 0;
    for (int i = 0; i <= 20; ++i)
        for (int j = 0; j <= 100 - 5 * i; ++j)
            for (int k = 0; k <= 100 - 5 * i - 2 * j; ++k)
                if (5 * i + 2 * j + k * 1 == 100)
                    cnt++;
    cout << "cnt" << cnt << endl;
    return;
}

void myswap(int &x, int &y)
{
    int tem = x;
    x = y;
    y = tem;
    return;
}

void quicksort(int *a, int left, int right)
{
    if (left < right)
    {
        int i = left, j = right;
        while (i < j)
        {
            while (a[j] >= a[left] && i < j)
                j--;
            while (a[i] <= a[left] && i < j)
                i++;
            swap(a[i], a[j]);
        }
        swap(a[i], a[left]);
        quicksort(a, left, i - 1);
        quicksort(a, i + 1, right);
    }
}

bool checksame(int *a, int beg, int end)
{
    int vote = 0;
    int po = a[0];
    for (int i = beg; i < end; ++i)
    {
        if (vote == 0)
            po = a[i];
        if (a[i] == po)
            vote++;
        else
            vote--;
        if (vote > 1)
            return false;
    }
    return true;
}

int *func4_generate_seed(int *seed, int size_)
{

    for (int i = 0; i < size_; ++i)
        seed[i] = rand() % 365;

    quicksort(seed, 0, size_ - 1);
    // for (int i = 0; i < size_; ++i)
    //     cout << seed[i] << ',';
    // cout << endl
    //      << endl;
    return seed;
}

bool func4(int *array, int size_)
{
    array = func4_generate_seed(array, size_);

    return (checksame(array, 0, size_));
}

int main()
{
    // func1(6, 3, '*');
    // func3();

    // int a1 = 1, a2 = 2;
    // myswap(a1, a2);
    // cout<< a1<<' ' << a2;
    int size = 100;
    int total_try_num = 1000;
    
    double succ_num = 0;
    double anw;
    int *seed = new int[size];
    for (int i = 0; i < total_try_num;++i)
        if(func4(seed, size))
            succ_num++;

    anw = succ_num / total_try_num;
    
    cout << endl
         << "succ_num" << succ_num << endl<<anw;
    
    
    return 0;
}
