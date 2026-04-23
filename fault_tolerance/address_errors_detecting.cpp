#include <iostream>
#include <zlib.h>
#include <cstdint>

using namespace std;


int edc(int c){
    uLong crc = crc32(0L, Z_NULL, 0);
    crc = crc32(crc, (const Bytef*) &c, sizeof(c));
    return crc;
}

// Writing
void save (int a, uintptr_t addr, uintptr_t comb[]){
    comb[0] = a;
    comb[1] = addr;
    comb[2] = edc(a ^ addr);
}

// Reading and verif. with edc
bool load (int a, uintptr_t addr, uintptr_t comb){
    int code = edc(a ^ addr);
    return code == comb;
}


int main(int argc, char const *argv[])
{
    int a = 10;
    int *ptr = &a;
    
    uintptr_t ptr_int = reinterpret_cast<uintptr_t>(ptr);


    uintptr_t combined[3] = {};

    cout << "Value of a: " << a << endl;
    cout << "Address of a: " << &a << endl;
    cout << "Numeric value of address of a: " << ptr_int << endl;

    save(a, ptr_int, combined);
    
    cout << "\n----- RESULTS AFTER SAVING -----" << endl;
    cout << "Value of a: " << combined[0] << endl;
    cout << "Value of addr: " << combined[1] << endl;
    cout << "Value of combined values: " << combined[2] << endl;

    // Output = 1
    cout << "\nIs it the same?\n" << (load(a, ptr_int, combined[2]));

    // Output = 0
    cout << "\nIs it the same?\n" << (load(a, ptr_int+1, combined[2]));

    // Output = 0
    cout << "\nIs it the same?\n" << (load(a+1, ptr_int, combined[2]));
    return 0;
}
