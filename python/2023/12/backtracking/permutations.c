/*
 * General-purpose backtracking algorithm from
 * "Programming Challenges: The Programming Contest Training Manual", p.
 * 167-175.
 *
 * Build and run:
 * clang permutations.c -o permutations && ./permutations
 */

#include <stdbool.h>
#include <stdio.h>

#define MAXCANDIDATES 10
#define NMAX 100

bool finished = false; /* found all solutions yet? */

// 8.3 Constructing All Permutations
bool is_a_solution(int a[], int k, int n) { return (k == n); }

void construct_candidates(int a[], int k, int n, int c[], int *ncandidates) {
    int i;
    bool in_perm[NMAX]; /* who is in the permutation? */

    for (i = 1; i < NMAX; i++) in_perm[i] = false;
    for (i = 0; i < k; i++) in_perm[a[i]] = true;

    *ncandidates = 0;
    for (i = 1; i <= n; i++) {
        if (in_perm[i] == false) {
            c[*ncandidates] = i;
            *ncandidates = *ncandidates + 1;
        }
    }
}

void process_solution(int a[], int k) {
    int i; /* counter */

    for (i = 1; i <= k; i++) printf(" %d", a[i]);

    printf("\n");
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

void generate_permutations(int n) {
    int a[NMAX]; /* solution vector */

    backtrack(a, 0, n);
}

int main() {
    generate_permutations(3);
    return 0;
}