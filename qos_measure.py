import time
import requests
import statistics

BASE_URL = "https://cataas.com"
NB_REQUESTS = 20
TIMEOUT = 5

times = []
errors = 0

print("Mesure de la QoS en cours...\n")

for i in range(NB_REQUESTS):
    start = time.time()

    try:
        response = requests.get(f"{BASE_URL}/cat", timeout=TIMEOUT)
        duration = time.time() - start

        times.append(duration)

        if response.status_code != 200:
            errors += 1

        print(f"Requête {i+1}: {round(duration, 3)} s")

    except requests.RequestException:
        errors += 1
        print(f"Requête {i+1}: ERREUR")

# 📊 Calculs
mean_time = statistics.mean(times)
max_time = max(times)
min_time = min(times)

# Calcul du percentile 95
times_sorted = sorted(times)
index_p95 = int(0.95 * len(times_sorted)) - 1
p95 = times_sorted[index_p95]

error_rate = (errors / NB_REQUESTS) * 100
availability = 100 - error_rate

# 📢 Résultats
print("\n===== Résultats QoS =====")
print(f"Temps moyen: {round(mean_time, 3)} s")
print(f"Temps max: {round(max_time, 3)} s")
print(f"Temps min: {round(min_time, 3)} s")
print(f"P95: {round(p95, 3)} s")
print(f"Taux d'erreur: {round(error_rate, 2)} %")
print(f"Disponibilité: {round(availability, 2)} %")
