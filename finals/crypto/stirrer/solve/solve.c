#include <bits/stdc++.h>
#define L 5

using namespace std;

uint8_t key[L];


// 8-bit left rotation
inline uint8_t rotl8(uint8_t x, int n) {
    return (uint8_t)((x << n) | (x >> (8 - n)));
}

inline void block(uint8_t state[L]) {
    
    for (int i = 0; i < L; i++)
        state[i] = (state[i] + key[i]) & 0xFF;
    
    state[0] = (state[0] + state[1]) & 0xFF;
    state[3] ^= state[0];
    state[3] = rotl8(state[3], 1);

    state[2] = (state[2] + state[4]) & 0xFF;
    state[0] ^= state[2];
    state[0] = rotl8(state[0], 7);

    state[1] = (state[1] + state[2]) & 0xFF;
    state[4] ^= state[1];
    state[4] = rotl8(state[4], 2);
    
    for (int i = 0; i < L; i++)
        state[i] = (state[i] + key[i]) & 0xFF;

}


map<int, vector<long long> > mp;
uint8_t *PT;
uint8_t *CT;

bool test124(int p1, int p2, int p4, int k1, int k2, int k4, int r4){
		
	int t2 = p2 + k2 + p4 + k4 & 0xff;
	int t1 = p1 + k1 + t2 & 0xff;
	int t4 = (p4 + k4 & 0xff)^t1;
	t4 = rotl8(t4, 2);
	return ((t4 + k4 & 0xff) == r4);
}


int correct = 0;		
void test(uint8_t *pt, uint8_t *pt2, uint8_t *ct, uint8_t *ct2){
	int sum1 = pt[1] + pt[2] + pt[4] - pt2[1] & 0xff;
	int sum2 = pt[2] + pt[4] - pt2[2] & 0xff;
	
	int sum1_ = ct[1] + ct[2] + ct[4] - ct2[1] & 0xff;
	int sum2_ = ct[2] + ct[4] - ct2[2] & 0xff;
	
	assert(sum1 == sum1_ && sum2 == sum2_);
	
	for (int k1 = 0; k1 < 256; k1++){
		int x = (-sum1 - 2*k1) & 0xff;
		int k2 = (-sum2 - x) & 0xff;
		int k4 = (x - k2) & 0xff;
		if (!test124(pt[1], pt[2], pt[4], k1, k2, k4, pt2[4]) || !test124(ct[1], ct[2], ct[4], k1, k2, k4, ct2[4])) continue;	
		//printf("!!! %d %d %d\n", k1, k2, k4);
		int A = pt[0] + pt[1] + k1 & 0xff;
		int B = pt[2] + pt[4] + k2 + k4 & 0xff;
		int P0_ = pt2[0];
		
		int A2 = ct[0] + ct[1] + k1 & 0xff;
		int B2 = ct[2] + ct[4] + k2 + k4 & 0xff;
		int P0_2 = ct2[0];
		for (int k0 = 0; k0 < 256; k0++){
		
			int lhs = rotl8(((A + k0)&0xff)^B, 7);
			int rhs = P0_ - k0 & 0xff;
			
			int lhs2 = rotl8(((A2 + k0)&0xff)^B2, 7);
			int rhs2 = P0_2 - k0 & 0xff;
			if (lhs != rhs || lhs2 != rhs2) continue;
			int A = pt[3];
			int B = pt[0]+pt[1]+k0+k1 & 0xff;
			int P3_ = pt2[3];
			
			int A2 = ct[3];
			int B2 = ct[0]+ct[1]+k0+k1 & 0xff;
			int P3_2 = ct2[3];
			for (int k3 = 0; k3 < 256; k3++){
				
				
				int lhs = rotl8(((A + k3)&0xff)^B, 1);
				int rhs = P3_ - k3 & 0xff;
				
				int lhs2 = rotl8(((A2 + k3)&0xff)^B2, 1);
				int rhs2 = P3_2 - k3 & 0xff;
				if (lhs != rhs || lhs2 != rhs2) continue;
				printf("%d %d %d %d %d\n",k0,k1,k2,k3,k4);
				correct++;
			}
				
		}			
			
	}
	return;
}				


int main(int argc, char** argv) {
    
    
    int N = 999 * 1000;
    
    PT = (uint8_t *)malloc(N*5);
    CT = (uint8_t *)malloc(N*5);
    if (!PT || !CT) return 1;

    fread(PT, sizeof *PT, N*5, stdin);
    fread(CT, sizeof *CT, N*5, stdin);
    
    for (int i = 0; i < N; i++){
    	uint8_t* pt = PT + (5*i);
    	uint8_t* ct = CT + (5*i);
    	int idx = (((pt[2] - ct[2] & 0xff) << 8) | (pt[1] - ct[1] & 0xff));
    	mp[idx].push_back(5*i);
    	//printf("%d %d\n", i, idx);
    }

    int CNT = 0;
    for (int i = 0; i < N; i++){
    	uint8_t* pt = PT + (5*i);
    	uint8_t* ct = CT + (5*i);
    	int key = ((((pt[2] + pt[4] - ct[2] - ct[4]) & 0xff)<<8)  | ((pt[1] + pt[2] + pt[4] - ct[1] - ct[2] - ct[4])&0xff));
    	//printf("%d %d %d\n", i, key, mp[key].size());
    	for (auto t: mp[key]){
    		CNT += 1;
    		test(pt, PT+t, ct, CT+t);
    		//printf("%d %d\n", i, t);
    	}
    }
    	
    
    
    free(PT);
    
    free(CT);
    return 0;
}

