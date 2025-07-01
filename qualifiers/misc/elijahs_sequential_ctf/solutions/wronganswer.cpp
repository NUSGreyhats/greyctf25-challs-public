#include <bits/stdc++.h>
using namespace std;
#define sz(x) (int)(x).size()
#define ll long long
#define ld long double
#define ull unsigned long long
#define vi vector<int>
#define vll vector<ll>
#define vvi vector<vi>
#define pii pair<int,int>
#define vpii vector<pair<int,int>>
#define vpll vector<pair<long long, long long>>
#define all(a) (a).begin(), (a).end()
#define endl '\n'
 
template <typename Container, typename T>
bool contains(const Container& container, const T& val) { return container.find(val) != container.end(); }
 
#define repname(a, b, c, d, e, ...) e
#define rep(...)                    repname(__VA_ARGS__, rep3, rep2, rep1, rep0)(__VA_ARGS__)
#define rep0(x)                     for (int rep_counter = 0; rep_counter < (x); ++rep_counter)
#define rep1(i, x)                  for (int i = 0; i < (x); ++i)
#define rep2(i, l, r)               for (int i = (l); i < (r); ++i)
#define rep3(i, l, r, c)            for (int i = (l); i < (r); i += (c))
 
#ifdef LOCAL
#include "debug_util.h"
#else
#define debug(...)
#endif

int main() {
    ios_base::sync_with_stdio(false);
    cin.tie(nullptr);
    cout.tie(nullptr);

    // Proper initializer for unordered_map of pair<int,int> to int
    map<pair<int,int>,int> gained = {
        {{0, 1}, 2},
        {{1, 2}, 5},
        {{0, 2}, 3},
        {{1, 0}, 4},
        {{2, 0}, 1},
        {{2, 1}, 6}
    };

    int n;
    cin >> n;
    vi nums(n);
    rep(i, n) {
        cin >> nums[i];
    }
    vi resarr;
    int i = 0;
    while (i < n - 2) {
        resarr.push_back(nums[i]);
        int x = gained.count({nums[i], nums[i+1]}) ? gained[{nums[i], nums[i+1]}] : 0;
        x += gained.count({nums[i+1], nums[i+2]}) ? gained[{nums[i+1], nums[i+2]}] : 0;
        int y = gained.count({nums[i], nums[i+2]}) ? gained[{nums[i], nums[i+2]}] : 0;
        if (x < y) {
            i += 2;
        } else {
            i += 1;
        }
    }
    while (i < n) {
        resarr.push_back(nums[i]);
        i++;
    }
    int res = 0;
    rep(j, sz(resarr) - 1) {
        res += gained.count({resarr[j], resarr[j+1]}) ? gained[{resarr[j], resarr[j+1]}] : 0;
    }
    cout << res << endl;
    return 0;
}