#include <iostream>
#include <string>
#include <map>

using namespace std;

// converts a number to its roman numeral equivalent
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
    
    // holds the roman numeral equivalent of the decimal numeral
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

// converts a roman numeral to its number equivalent
int romToNum(string rom)
{
	// holds the lower and upper bounds of valid input
    const int LOWER_BOUND = 1;
    const int UPPER_BOUND = 3999;
    
	// used to check if rom is a valid input
    int valid;
    
	/*
		this is highly unoptimized because we have to call numToRom 
		3999 times for bad input but I can't find another way to reject 
		bad roman numeral input
	*/
	// checks to see if rom is valid by comparing it with all valid input
	// if not then valid will be set to 4000 which is out of bounds
    for (valid = LOWER_BOUND; valid <= UPPER_BOUND; valid++)
    {
        if (rom == numToRom(valid))
        {
            break;
        }
    }
    
    // checks for invalid input
    if (valid > UPPER_BOUND)
    {
        return 0;
    }
    
	// map that holds roman numerals and their values
    map<char, int> romanNums;
    romanNums['M'] = 1000;
    romanNums['D'] = 500;
    romanNums['C'] = 100;
    romanNums['L'] = 50;
    romanNums['X'] = 10;
    romanNums['V'] = 5;
    romanNums['I'] = 1;
    
	// holds the decimal numeral equivalent of the roman numeral
    int decNum = 0;
    
	// loop through all characters in rom (except for the last one 
	// to avoid accessing garbage values in romanNums[rom[i+1]])
    for (int i = 0; i < rom.length()-1; i++)
    {
		// if the current roman numeral's value is less than the next 
		// then we must subtract by the current numeral's value 
		// Ex. The I in IV sets decNum to -1 then add 5 for 4
		// else just add the current numeral's value
        if (romanNums[rom[i]] < romanNums[rom[i+1]])
        {
            decNum -= romanNums[rom[i]];
        }
        else
        {
            decNum += romanNums[rom[i]];
        }
    }
    
	// add the last roman numeral's value to the sum
    decNum += romanNums[rom[rom.length()-1]];
    
    return decNum;
}

int main()
{
	int decNum;
	
	cout << "Enter number: ";
	cin >> decNum;
	
	string romNum = numToRom(decNum);
	cout << "Roman numeral of " << decNum << " is " << romNum << endl;
	cout << "Decimal numeral of " << romNum << " is " << romToNum(romNum);
	
	return 0;
}