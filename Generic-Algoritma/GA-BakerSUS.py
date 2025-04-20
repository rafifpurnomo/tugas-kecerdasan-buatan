import math
import random

# Konfigurasi GA
POPULATION_SIZE = 20  # Ukuran populasi
CHROMOSOME_LENGTH = 32  # 8 bit untuk x1, 8 bit untuk x2
GEN_MAX = 100  # Jumlah generasi
PC = 0.8  # Probabilitas crossover
PM = 0.1  # Probabilitas mutasi

# Fungsi konversi biner ke desimal lalu ke range -10 sampai 10
def decode(chromosome):
    x1_bin = chromosome[:16]
    x2_bin = chromosome[16:]
    x1 = -10 + int(x1_bin, 2) * 20 / 65535
    x2 = -10 + int(x2_bin, 2) * 20 / 65535
    return x1, x2


# Fungsi yang ingin diminimalkan
def objective_function(x1, x2):
    try:
        result = - (math.sin(x1) * math.cos(x2) * math.tan(x1 + x2) +
                    (3/4) * math.exp(1 - math.sqrt(x1**2)))
        return result
    except:
        return float('inf')  # Tangani nilai tak hingga

# Fitness (semakin kecil f, semakin besar fitness)
def fitness(chromosome):
    x1, x2 = decode(chromosome)
    f_value = objective_function(x1, x2)
    return 1 / (1 + f_value) if f_value >= 0 else 1 + abs(f_value)


# Inisialisasi populasi awal
def initialize_population():
    return [''.join(random.choice('01') for _ in range(CHROMOSOME_LENGTH)) for _ in range(POPULATION_SIZE)]

# Seleksi dengan metode Stochastic Universal Sampling (SUS)
def selection_stoch_unif(population, num_parents=2):
    fitnesses = [fitness(ind) for ind in population]
    total_fitness = sum(fitnesses)

    # Hitung interval antara pointer
    point_distance = total_fitness / num_parents

    # Posisi awal pointer acak
    start_point = random.uniform(0, point_distance)
    pointers = [start_point + i * point_distance for i in range(num_parents)]

    # Susun populasi kumulatif
    selected = []
    cumulative_fitness = 0
    i = 0
    for pointer in pointers:
        while cumulative_fitness < pointer:
            cumulative_fitness += fitnesses[i]
            i += 1
        selected.append(population[i - 1])
        i = 0  # reset pointer untuk next pointer
        cumulative_fitness = 0
    return selected[0], selected[1]



# Crossover satu titik
def crossover(parent1, parent2):
    if random.random() < PC:
        point = random.randint(1, CHROMOSOME_LENGTH - 1)
        child1 = parent1[:point] + parent2[point:]
        child2 = parent2[:point] + parent1[point:]
        return child1, child2
    else:
        return parent1, parent2

# Mutasi: flip bit
def mutate(chromosome):
    mutated = ''
    for bit in chromosome:
        if random.random() < PM:
            mutated += '1' if bit == '0' else '0'
        else:
            mutated += bit
    return mutated

# Proses utama algoritma genetika
def genetic_algorithm():
    population = initialize_population()
    best_chrom = None
    best_fit = 0

    for gen in range(GEN_MAX):
        new_population = []

        while len(new_population) < POPULATION_SIZE:
            p1, p2 = selection_stoch_unif(population)
            c1, c2 = crossover(p1, p2)
            c1 = mutate(c1)
            c2 = mutate(c2)
            new_population.extend([c1, c2])

        population = new_population[:POPULATION_SIZE]

        # Simpan individu terbaik
        for chrom in population:
            fit = fitness(chrom)
            if fit > best_fit:
                best_fit = fit
                best_chrom = chrom

        # Tampilkan generasi dan fitness terbaik
        x1, x2 = decode(best_chrom)
        # print(f"Generasi {gen+1} | Best Fitness: {best_fit:.5f} | x1: {x1:.4f}, x2: {x2:.4f}")

    return best_chrom

# Jalankan GA
best = genetic_algorithm()
x1_final, x2_final = decode(best)
print("\n=== HASIL AKHIR DENGAN BAKER SUS ===")
print(f"Kromosom terbaik: {best}")
print(f"x1 = {x1_final:.4f}, x2 = {x2_final:.4f}")
print(f"f(x1, x2) = {objective_function(x1_final, x2_final):.5f}")
