#include <iostream>

using namespace std;

int main() {
    int L, R, a;
    cin >> L >> R >> a;
    R -= L - 1;
    int k = R / a;
    cout << 1LL * (R - k * a) * k + a * (1LL * k * (k - 1) / 2) << endl;
    return 0;
}
