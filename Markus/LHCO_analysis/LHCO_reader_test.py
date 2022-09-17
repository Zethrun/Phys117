from random import sample
from selectors import EVENT_READ
from LHCO_reader import partition_problem as pp
from LHCO_reader import LHCO_reader
import matplotlib.pyplot as plt
import numpy as np
from tqdm import tqdm

#Variables
c = 3 * (10 ** 8)

filename = "C:/Users/mhals/Dropbox/PC/Documents/GitHub/Phys117/Markus/example.lhco"

events = LHCO_reader.Events(f_name = filename)
print(events)

#tau = lambda event: event.number()["tau"] == 1
#events.cut(tau)

counts = {
    "jets": 0,
    "electrons": 0,
    "taus": 0,
    "photons": 0
}

def data_pie():
    for event in tqdm(events):
        counts["jets"] += event.number()["jet"]
        counts["electrons"] += event.number()["electron"]
        counts["taus"] += event.number()["tau"]
        counts["photons"] += event.number()["photon"]

    jets = counts["jets"]
    electrons = counts["electrons"]
    taus = counts["taus"]
    photons = counts["photons"]
    total = jets + electrons + taus + photons

    (per_jets, per_electrons, per_taus, per_photons) = (100*jets/total, 100*electrons/total, 100*taus/total, 100*photons/total)
    labels = ("jets: %i - %i" %(jets, per_jets), "electrons: %i - %i" %(electrons, per_electrons), "taus: %i - %i" %(taus, per_taus), "photons: %i - %i" %(photons, per_photons))
    label_counts = (counts["jets"], counts["electrons"], counts["taus"], counts["photons"])
    fig, ax = plt.subplots()
    ax.pie(label_counts, labels = labels)
    plt.show()

#data_pie()

def event_data():
    for event in tqdm(events):
        print(event)

#event_data()

def PT_phi(sample_size):
    PT_phi_list = []
    for event in events[:sample_size]:
        phi = event["MET"][0]["phi"]
        PT = event["MET"][0]["PT"]
        PT_phi_list.append((phi, PT))
    return PT_phi_list

def PT_v_phi_graph():
    PT_phi_list = PT_phi(len(events))
    PT_phi_list.sort(key=lambda tup: tup[0])
    (phi, PT) = (np.array([temp[0] for temp in PT_phi_list]), np.array([temp[1] for temp in PT_phi_list]))
    plt.plot(phi, PT)
    plt.grid()
    plt.title("PT(phi)")
    plt.xlabel("phi")
    plt.ylabel("PT")
    plt.show()

#PT_v_phi_graph()

def MET():
    PT_phi_list = PT_phi(len(events))
    MET_list = []
    (PTx, PTy) = (0, 0)
    (phi, PT) = (np.array([temp[0] for temp in PT_phi_list]), np.array([temp[1] for temp in PT_phi_list]))
    for sample in tqdm(range(len(phi))):
        PTx += PT[sample]*np.cos([phi[sample]])
        PTy += PT[sample]*np.sin([phi[sample]])
        energy = np.sqrt(np.square(PTx) + np.square(PTy))
        MET_list.append((energy, sample))
    (x, y) = (np.array([temp[0] for temp in MET_list]), np.array([temp[1] for temp in MET_list]))
    plt.plot(x, y)
    plt.grid()
    plt.title("MET")
    plt.xlabel("Energy")
    plt.ylabel("Number of Events")
    plt.show()

MET()



