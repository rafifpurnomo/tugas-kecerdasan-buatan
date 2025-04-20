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


# Fungsi objektif yang ingin diminimalkan
def objective_function(x1, x2):
    try:
        result = - (math.sin(x1) * math.cos(x2) * math.tan(x1 + x2) +
                    (3/4) * math.exp(1 - math.sqrt(x1**2)))
        return result
    except:
        return float('inf')

# Fungsi fitness
def fitness(chromosome):
    x1, x2 = decode(chromosome)
    f_value = objective_function(x1, x2)
    return 1 / (1 + f_value) if f_value >= 0 else 1 + abs(f_value)


# Inisialisasi populasi awal
def initialize_population():
    return [''.join(random.choice('01') for _ in range(CHROMOSOME_LENGTH)) for _ in range(POPULATION_SIZE)]

# Seleksi: tournament selection
def selection(population, tournament_size=3):
    tournament = random.sample(population, tournament_size)
    tournament_fitnesses = [(ind, fitness(ind)) for ind in tournament]
    tournament_fitnesses.sort(key=lambda x: x[1], reverse=True)
    return tournament_fitnesses[0][0], tournament_fitnesses[1][0]

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
            p1, p2 = selection(population)
            c1, c2 = crossover(p1, p2)
            c1 = mutate(c1)
            c2 = mutate(c2)
            new_population.extend([c1, c2])

        population = new_population[:POPULATION_SIZE]

        for chrom in population:
            fit = fitness(chrom)
            if fit > best_fit:
                best_fit = fit
                best_chrom = chrom

        x1, x2 = decode(best_chrom)
        # print(f"Generasi {gen+1} | Best Fitness: {best_fit:.5f} | x1: {x1:.4f}, x2: {x2:.4f}")

    return best_chrom

# Jalankan GA
best = genetic_algorithm()
x1_final, x2_final = decode(best)
print("\n=== HASIL AKHIR DENGAN tournament selection ===")
print(f"Kromosom terbaik: {best}")
print(f"x1 = {x1_final:.4f}, x2 = {x2_final:.4f}")
print(f"f(x1, x2) = {objective_function(x1_final, x2_final):.5f}")