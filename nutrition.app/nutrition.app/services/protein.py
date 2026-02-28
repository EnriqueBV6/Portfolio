import matplotlib
matplotlib.use("Agg") 

import matplotlib.pyplot as plt
import uuid
def plot_protein(df):
    filename = f"static/{uuid.uuid4().hex}.png"

    plt.figure()
    plt.plot(df["Day"], df["Protein"])
    plt.xlabel("Day")
    plt.ylabel("Protein (g)")
    plt.title("Protein Intake Over Time")
    plt.savefig(filename)
    plt.close()

    return filename