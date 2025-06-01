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

/*
0 -> 1: 2
1 -> 2: 5
0 -> 2: 3
1 -> 0: 4
2 -> 0: 1
2 -> 1: 6
*/

int main() {
    int n; cin>>n;
    vi arr(n);
    vi dp0(n), dp1(n), dp2(n);
    rep(i,n) cin >> arr[i];
    dp0[0] = dp1[0] = dp2[0] = -1e9;
    if (arr[0] == 0) {
        dp0[0] = 0;
    } else if (arr[0] == 1) {
        dp1[0] = 0;
    } else {
        dp2[0] = 0;
    }
    rep(i, 1, n) {
        int curscore = arr[i] == 0 ? dp0[i-1] : arr[i] == 1 ? dp1[i-1] : dp2[i-1];
        curscore = max(0, curscore);
        if (arr[i] == 0) {
            curscore = max(curscore, dp1[i-1] + 4);
            curscore = max(curscore, dp2[i-1] + 1);
            dp1[i] = dp1[i-1];
            dp2[i] = dp2[i-1];
            dp0[i] = curscore;
        } else if (arr[i] == 1) {
            curscore = max(curscore, dp0[i-1] + 2);
            curscore = max(curscore, dp2[i-1] + 6);
            dp0[i] = dp0[i-1];
            dp2[i] = dp2[i-1];
            dp1[i] = curscore;
        } else {
            curscore = max(curscore, dp0[i-1] + 3);
            curscore = max(curscore, dp1[i-1] + 5);
            dp0[i] = dp0[i-1];
            dp1[i] = dp1[i-1];
            dp2[i] = curscore;
        }
    }
    cout << max(dp0[n-1], max(dp1[n-1], dp2[n-1])) << endl;
}