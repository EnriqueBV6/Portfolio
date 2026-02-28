import matplotlib
matplotlib.use("Agg") 

import matplotlib.pyplot as plt
import uuid

def plot_calories(df):
    filename = f"static/{uuid.uuid4().hex}.png"

    plt.figure()
    plt.plot(df["Day"], df["Calories"])
    plt.xlabel("Day")
    plt.ylabel("Calories")
    plt.title("Calories Intake Over Time")
    plt.savefig(filename)
    plt.close()

    return filename