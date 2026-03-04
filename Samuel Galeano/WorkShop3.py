import tkinter as tk
from tkinter import messagebox
import random
import math
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg


# -----------------------------
# CLASE SERVIDOR
# -----------------------------
class Servidor:

    def __init__(self, id_servidor, cpu, temperatura, energia):
        self.id = id_servidor
        self.cpu = cpu
        self.temperatura = temperatura
        self.energia = energia
        self.estado = "OK"
        self.procesos_restantes = 0

    def evaluar_estado(self):

        # Regla principal de estado
        if self.temperatura > 75 and self.cpu > 80:
            self.estado = "CRITICO"

        elif self.temperatura > 75 or self.cpu > 80:
            self.estado = "ADVERTENCIA"

        else:
            self.estado = "OK"

        # Regla de procesos restantes
        if self.cpu >= 90 and self.cpu < 100:
            capacidad_restante = 100 - self.cpu
            self.procesos_restantes = math.floor(capacidad_restante / 2)

        elif self.cpu >= 100:
            self.procesos_restantes = 0


# -----------------------------
# CLASE PRINCIPAL
# -----------------------------
class GuardianApp:

    def __init__(self, root):
        self.root = root
        self.root.title("The Data Center Guardian")

        self.servidores = []

        # ---------------- FRAME ENTRADAS
        frame_inputs = tk.Frame(root)
        frame_inputs.pack(pady=10)

        tk.Label(frame_inputs, text="Cantidad:").grid(row=0, column=0, padx=5)
        self.entry_n = tk.Entry(frame_inputs, width=8)
        self.entry_n.grid(row=0, column=1, padx=5)

        tk.Label(frame_inputs, text="Seed:").grid(row=0, column=2, padx=5)
        self.entry_seed = tk.Entry(frame_inputs, width=8)
        self.entry_seed.grid(row=0, column=3, padx=5)

        tk.Button(frame_inputs, text="Generar", command=self.generar_datos)\
            .grid(row=0, column=4, padx=10)

        # ---------------- FRAME MÉTRICAS
        frame_metricas = tk.Frame(root)
        frame_metricas.pack(pady=10)

        self.label_total = tk.Label(frame_metricas, text="Total: 0")
        self.label_total.grid(row=0, column=0, padx=10)

        self.label_ok = tk.Label(frame_metricas, text="OK: 0")
        self.label_ok.grid(row=0, column=1, padx=10)

        self.label_adv = tk.Label(frame_metricas, text="Advertencia: 0")
        self.label_adv.grid(row=0, column=2, padx=10)

        self.label_crit = tk.Label(frame_metricas, text="Crítico: 0")
        self.label_crit.grid(row=0, column=3, padx=10)

        self.label_promedio = tk.Label(frame_metricas, text="Promedio CPU: 0")
        self.label_promedio.grid(row=0, column=4, padx=10)

        # ---------------- GRÁFICOS
        self.fig, self.ax = plt.subplots(1, 2, figsize=(8, 4))
        self.canvas = FigureCanvasTkAgg(self.fig, master=root)
        self.canvas.get_tk_widget().pack()

    # -----------------------------
    # GENERAR DATOS
    # -----------------------------
    def generar_datos(self):

        try:
            n = int(self.entry_n.get())
            seed = int(self.entry_seed.get())

            if n <= 0:
                messagebox.showerror("Error", "N debe ser mayor que 0")
                return

        except:
            messagebox.showerror("Error", "Ingrese valores válidos")
            return

        random.seed(seed)
        self.servidores = []

        for i in range(n):
            cpu = random.uniform(0, 100)
            temperatura = random.uniform(40, 120)
            energia = random.uniform(100, 600)

            servidor = Servidor(f"S{i+1}", cpu, temperatura, energia)
            servidor.evaluar_estado()
            self.servidores.append(servidor)

        self.actualizar_metricas()
        self.actualizar_graficos()

    # -----------------------------
    # ACTUALIZAR MÉTRICAS
    # -----------------------------
    def actualizar_metricas(self):

        total = len(self.servidores)
        ok = 0
        adv = 0
        crit = 0
        suma_cpu = 0

        for s in self.servidores:
            suma_cpu += s.cpu

            if s.estado == "OK":
                ok += 1
            elif s.estado == "ADVERTENCIA":
                adv += 1
            elif s.estado == "CRITICO":
                crit += 1

        promedio_cpu = suma_cpu / total if total > 0 else 0

        self.label_total.config(text=f"Total: {total}")
        self.label_ok.config(text=f"OK: {ok}")
        self.label_adv.config(text=f"Advertencia: {adv}")
        self.label_crit.config(text=f"Crítico: {crit}")
        self.label_promedio.config(text=f"Promedio CPU: {promedio_cpu:.2f}")

    # -----------------------------
    # ACTUALIZAR GRÁFICOS
    # -----------------------------
    def actualizar_graficos(self):

        self.ax[0].clear()
        self.ax[1].clear()

        temperaturas = [s.temperatura for s in self.servidores]
        estados = [s.estado for s in self.servidores]

        # Histograma Temperatura
        self.ax[0].hist(temperaturas)
        self.ax[0].set_title("Histograma Temperatura")

        # Barras Estados
        ok = estados.count("OK")
        adv = estados.count("ADVERTENCIA")
        crit = estados.count("CRITICO")

        self.ax[1].bar(["OK", "ADV", "CRIT"], [ok, adv, crit])
        self.ax[1].set_title("Estados")

        self.canvas.draw()


# -----------------------------
# EJECUCIÓN
# -----------------------------
root = tk.Tk()
app = GuardianApp(root)
root.mainloop()