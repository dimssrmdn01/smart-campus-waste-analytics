#  smart-campus-waste-analytics (Ultra-Pro SQL Version)

An institutional-grade IoT simulation, predictive analytics, and carbon footprint optimization engine integrated with a persistent SQL data layer. Designed specifically for smart campus sustainability logistics, this system processes real-time sensor telemetry, predicts container overflow timelines, computes the most fuel-efficient disposal collection paths, and archives metrics for ESG environmental auditing.

---

##  Key Features

* **Real-Time IoT Telemetry Simulation:** Tracks live volume fill-rates, categorical segregation (Organic vs. Anorganic), and historical accumulation speed across high-density campus sectors.
* **Predictive Overflow Engine:** Computes an automated linear accumulation rule (*Hours Until Full*) to proactively flag container overcapacity risks before environmental leakage occurs.
* **Spatial Route Optimization (Greedy TSP):** Executes a localized variant of the Traveling Salesman Problem using a Greedy Nearest Neighbor algorithm to dynamically isolate and connect critical disposal nodes based on threshold limits.
* **ESG & Carbon Mitigation Calculator:** Quantifies ecological impacts in real-time by contrasting optimized logistics paths against blind, static routes—measuring metric distances saved and grams of $CO_2$ emissions successfully mitigated.
* **Persistent SQL Data Layer:** Integrates an `SQLite3` engine to lock, commit, and archive shift logs permanently, enabling long-term historical environmental auditing.
* **Interactive Spatially-Aware Dashboard:** Built completely on a reactive Streamlit and Plotly architecture mapped dynamically onto OpenStreetMap overlays.

---

##  Repository Structure

* `dashboard.py` - Core production script housing the Streamlit interface, geospatial line visualizations, and ESG metric calculators.
* `waste_optimizer.py` - Lightweight terminal prototype showcasing raw mathematical optimization execution.
* `seed_db.py` - Database seeder script to populate historical environmental records.

---

##  Tech Stack & Dependencies

* **Language:** Python
* **GUI & Reactive Components:** Streamlit
* **Geospatial & Statistical Plots:** Plotly Express
* **Database Architecture:** SQLite3 (Native Python Module)
* **Matrix Manipulations & Data Pipelines:** NumPy, Pandas

---

##  Installation & Deployment Guide

1. **Clone the Repository:**
```bash
   git clone [https://github.com/dimssrmdn01/smart-campus-waste-analytics.git](https://github.com/dimssrmdn01/smart-campus-waste-analytics.git)
   cd smart-campus-waste-analytics
   ```

2. **Install Core Dependencies:**
```bash
   pip install streamlit plotly pandas numpy
   ```

3. **Populate Historical SQL Logs (Optional Seed):**
```bash
   python seed_db.py
   ```

4. **Launch the Real-Time Dashboard Server:**
```bash
   streamlit run dashboard.py
   ```

---

##  Analytics & Operational Metrics Inside

| Metric Indicator | Calculation Source | Optimization Target |
| :--- | :--- | :--- |
| **Fill Rate (%)** | Real-Time Ultrasonic Sensor Telemetry | Flag Overcapacity Thresholds |
| **Accumulation Rate (%/Hr)** | Spatial Densities Data Rule | Generate Proactive Maintenance Alerts |
| **Carbon Savings (g CO₂)** | Metric Distance Offset $\times$ Light-Truck Fuel Constant | Compliance Reporting & ESG Auditing |
| **SQL Logging** | Structured Query Relational Insert | Long-Term Trend Analytics & Persistence |
