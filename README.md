# Knife-edge-diffraction-simulation
A real-time visualization of radio wave propagation and diffraction loss using the Single Knife-Edge model, built with Python and Pygame.

This project was created to visualize how radio signals interact with obstacles (like hills or buildings) in the line of sight (LOS). It combines physics formulas with geometric calculations to determine whether a signal is blocked and calculate the resulting loss in decibels (dB).

The simulation implements the standard Single Knife-Edge Diffraction model:
1.  **Geometry:** Distances are calculated using Euclidean distance and Heron's formula to determine the obstacle's intrusion into the Fresnel zone ($h$).
2.  **Diffraction Parameter (v):**
    $$v = h \sqrt{\frac{2}{\lambda} (\frac{1}{d_1} + \frac{1}{d_2})}$$
3.  **Loss Calculation:** Approximated using the logarithmic formula for v > -0.7$.

How to Run
1.  Install the requirements:
    ```bash
    pip install pygame
    ```
2.  Run the main script:
    ```bash
    python main.py
    ```

## Controls
* **Mouse (Left Click + Drag):** Move the Transmitter, Receiver, or Obstacle.
* **Arrow UP:** Increase Frequency (+50 MHz).
* **Arrow DOWN:** Decrease Frequency (-50 MHz).