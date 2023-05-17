#include <iostream>
#include <vector>
#include <cmath>
#include <climits>
#include <omp.h>

using namespace std;

void min_scalar_product(vector<vector<int>>& matrix, int num_threads) {
    int m = matrix.size();
    int n = matrix[0].size();

    int min_product = INT_MAX;
    int min_i = 0, min_j = 0;

#pragma omp parallel num_threads(num_threads)
    {
        int tid = omp_get_thread_num();
        int chunk_size = m / omp_get_num_threads() + 1;
        int start = tid * chunk_size;
        int end = min(start + chunk_size, m);

        int local_min_product = INT_MAX;
        int local_min_i = 0, local_min_j = 0;

        for (int i = start; i < end; i++) {
            for (int j = i + 1; j < m; j++) {
                int product = 0;
                for (int k = 0; k < n; k++) {
                    product += matrix[i][k] * matrix[j][k];
                }
                if (product < local_min_product) {
                    local_min_product = product;
                    local_min_i = i;
                    local_min_j = j;
                }
            }
        }

#pragma omp critical
        {
            if (local_min_product < min_product) {
                min_product = local_min_product;
                min_i = local_min_i;
                min_j = local_min_j;
            }
        }
    }

    cout << "Мiнiмальний скалярний добуток знаходиться мiж рядками " << min_i << " та " << min_j << endl;
}

int main() {
    setlocale(LC_ALL, "Russian");
    int m = 300;
    int n = 20;
    int num_threads_values[] = { 1, 2, 4, 6, 8, 10, 20 };

    // Generate matrix
    vector<vector<int>> matrix(m, vector<int>(n));
    for (int i = 0; i < m; i++) {
        for (int j = 0; j < n; j++) {
            matrix[i][j] = rand() % 1000;
        }
    }

    for (int i = 0; i < sizeof(num_threads_values) / sizeof(int); i++) {
        int num_threads = num_threads_values[i];
        double start_time = omp_get_wtime();
        min_scalar_product(matrix, num_threads);
        double end_time = omp_get_wtime();
        double time_taken = end_time - start_time;
        cout << "Час, витрачений на " << num_threads << " потокiв: " << time_taken << " секунд" << endl;
    }

    return 0;
}