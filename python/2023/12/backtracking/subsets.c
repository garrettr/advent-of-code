/*
 * General-purpose backtracking algorithm from
 * "Programming Challenges: The Programming Contest Training Manual", p.
 * 167-175.
 *
 * Build and run:
 * clang subsets.c -o subsets && ./subsets
 */

#include <stdbool.h>
#include <stdio.h>

#define MAXCANDIDATES 10
#define NMAX 100

bool finished = false; /* found all solutions yet? */

// 8.2 Constructing All Subsets
bool is_a_solution(int a[], int k, int n) { return (k == n); }

void construct_candidates(int a[], int k, int n, int c[], int *ncandidates) {
    c[0] = true;
    c[1] = false;
    *ncandidates = 2;
}

void process_solution(int a[], int k) {
    int i; /* counter */

    printf("{");
    for (i = 1; i <= k; i++)
        if (a[i] == true) printf(" %d", i);

    printf(" }\n");
}

void backtrack(int a[], int k, int input) {
    int c[MAXCANDIDATES]; /* candidates for next position */
    int ncandidates;      /* next position candidate count */
    int i;                /* counter */

    if (is_a_solution(a, k, input)) {
        process_solution(a, k);
    } else {
        k = k + 1;
        construct_candidates(a, k, input, c, &ncandidates);
        for (i = 0; i < ncandidates; i++) {
            a[k] = c[i];
            backtrack(a, k, input);
            if (finished) return; /* terminate early*/
        }
    }
}

void generate_subsets(int n) {
    int a[NMAX];

    backtrack(a, 0, n);
}

int main() {
    generate_subsets(3);
    return 0;
}