#include <iostream>
#include <string>

using namespace std;

// converts a number to its roman number equivalent
string numToRom(int num)
{
    // stores a set of roman numerals and their values
    enum RomanNums
    {
        I = 1,
        IV = 4,
        V = 5,
        IX = 9,
        X = 10,
        XL = 40,
        L = 50,
        XC = 90,
        C = 100,
        CD = 400,
        D = 500,
        CM = 900,
        M = 1000
    };
    
    // holds the lower and upper bounds of valid input
    const int LOWER_BOUND = 1;
    const int UPPER_BOUND = 3999;
    
    // checks for invalid input
    if (num < LOWER_BOUND || num > UPPER_BOUND)
    {
        return "Invalid";
    }
    
    // holds the roman numeral
    string romNum;
    
    // keeps looping until num reaches 0
    while (num >= LOWER_BOUND)
    {
        // checks to see what range num is in
        // when it finds the correct range it will 
        // then add the roman numeral to romNum 
        // and subtract the roman numeral's numbered 
        // equivalent from num
        if (num >= M)
        {
            romNum += "M";
            num -= M;
        }
        else if (num < M && num >= CM)
        {
            romNum += "CM";
            num -= CM;
        }
        else if (num < CM && num >= D)
        {
            romNum += "D";
            num -= D;
        }
        else if (num < D && num >= CD)
        {
            romNum += "CD";
            num -= CD;
        }
        else if (num < CD && num >= C)
        {
            romNum += "C";
            num -= C;
        }
        else if (num < C && num >= XC)
        {
            romNum += "XC";
            num -= XC;
        }
        else if (num < XC && num >= L)
        {
            romNum += "L";
            num -= L;
        }
        else if (num < L && num >= XL)
        {
            romNum += "XL";
            num -= XL;
        }
        else if (num < XL && num >= X)
        {
            romNum += "X";
            num -= X;
        }
        else if (num < X && num >= IX)
        {
            romNum += "IX";
            num -= IX;
        }
        else if (num < IX && num >= V)
        {
            romNum += "V";
            num -= V;
        }
        else if (num < V && num >= IV)
        {
            romNum += "IV";
            num -= IV;
        }
        else if (num < IV && num >= I)
        {
            romNum += "I";
            num -= I;
        }
    }
    
    return romNum;
}

int main()
{
	int num;
	
	cout << "Enter number: ";
	cin >> num;
	cout << "Roman numeral of " << num << " is " << numToRom(num);
	
	return 0;
}