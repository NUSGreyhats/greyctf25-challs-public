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

void solve() {
  int n;
  cin >> n;
  vi a(n);
  rep(i, 0, n) cin >> a[i];
  int max0 = -1e9, max1 = -1e9, max2 = -1e9;
  rep(i, 0, n) {
    if (a[i] == 0) {
      max0 = max(max0, max1 + 4);
      max0 = max(max0, max2 + 1);
      max0 = max(max0, 0);
    } else if (a[i] == 1) {
      max1 = max(max1, max0 + 2);
      max1 = max(max1, max2 + 6);
      max1 = max(max1, 0);
    } else {
      max2 = max(max2, max0 + 3);
      max2 = max(max2, max1 + 5);
      max2 = max(max2, 0);
    }
  }
  cout << max(max2, max(max0, max1)) << endl;
}

int main() {
  ios::sync_with_stdio(false);
  cin.tie(nullptr);
  solve();
}
