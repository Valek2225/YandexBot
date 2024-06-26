#include <iostream>
#include <stdlib.h>
#include <cmath>
#include <algorithm>
#include <vector>
#include <set>
#include <map>
#include <random>
#include <bitset>

#define uint unsigned int
#define ll long long
#define ull unsigned long long
#define ld long double
#define rep(i, l, r) for (int i = l; i < r; i++)
#define repb(i, r, l) for (int i = r; i > l; i--)
#define sz(a) (int)a.size()
#define fi first
#define se second
#define mp(a, b) make_pair(a, b)

using namespace std;

inline void setmin(int &x, int y) { if (y < x) x = y; }
inline void setmax(int &x, int y) { if (y > x) x = y; }
inline void setmin(ll &x, ll y) { if (y < x) x = y; }
inline void setmax(ll &x, ll y) { if (y > x) x = y; }
const int N = 100000;
const int inf = (int)1e9 + 1;
const ll big = (ll)1e18 + 1;
const int P = 239;
const int MOD = (int)1e9 + 7;
const int MOD1 = (int)1e9 + 9;
const double eps = 1e-9;
const double pi = atan2(0, -1);
const int ABC = 26;

int main()
{
    //freopen("a.in", "r", stdin);
    //freopen("dsu.out", "w", stdout);
    ios_base::sync_with_stdio(0);
    cin.tie(0);
    cout.precision(20);
    cout << fixed;
    //ll TL = 0.95 * CLOCKS_PER_SEC;
    //clock_t time = clock();
    int l, r, a;
    cin >> l >> r >> a;
    ll ans = 0;
    int x = r - l;
    if (a == 1) {
        ans = 1LL * x * (x + 1) / 2;
        cout << ans << "\n";
        return 0;
    }
    while (x >= 0) {
        int x1 = x / a * a - 1;
        ans += (x - x1) * (x / a);
        x = x1;
    }
    cout << ans << "\n";
    return 0;
}