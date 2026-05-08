# MPA3 DDE Controller for Python

**A Python wrapper to control MPA3 data acquisition software via DDE (Dynamic Data Exchange).**
---

## 📌 About

This project provides a **Python interface** to interact with **MPA3 data acquisition software** using the **DDE (Dynamic Data Exchange) protocol**. It allows you to:

- Start/stop data acquisition.
- Retrieve data and configurations.
- Control ADC (Analog-to-Digital Converter) settings.
- Save/load MPA3 configurations.

> ⚠️ **Note**: DDE is a legacy Windows protocol. This library is designed for systems where **MPA3 is already installed** and configured to accept DDE connections.

---

## 🛠️ Prerequisites

- **Operating System**: Windows (DDE is not available on Linux/macOS).
- **Python**: 3.6 or higher.
- **Python Libraries**:
  - `pywin32` (for `win32ui` and `dde` support):
    ```bash
    pip install pywin32
    ```
- **MPA3 Software**: Must be installed and running to connect.

## 💻 Usage

### Basic Example

```python
from dde_mpa3_control import DDEMPA3Control

# Initialize and connect to MPA3
mpa = DDEMPA3Control()
if mpa.connect():
    try:
        mpa.start()          # Start data acquisition
        data = mpa.get_data() # Retrieve data as a list of integers
        print(f"Data: {data}")
    finally:
        mpa.close()          # Close the DDE connection
```

### Available Methods


| Method                       | Description                                                 |
| ---------------------------- | ----------------------------------------------------------- |
| `connect()`                  | Connects to the MPA3 DDE server.                            |
| `close()`                    | Closes the DDE connection.                                  |
| `start()`                    | Starts data acquisition.                                    |
| `stop()`                     | Stops data acquisition.                                     |
| `resume()`                   | Resumes paused data acquisition.                            |
| `clear()`                    | Clears current data in MPA3.                                |
| `beep()`                     | Triggers a beep sound in MPA3.                              |
| `set_current_adc(adc_index)` | Sets the ADC index for data retrieval
| `get_data()`                 | Retrieves data as a list of integers.                       |
| `get_range()`                | Retrieves the current ADC range.                            |
| `set_path(path)`             | Sets the file path for MPA3 operations (max 90 characters). |
| `save_mpa()`                 | Saves the current MPA3 configuration.                       |
| `load_mpa()`                 | Loads the MPA3 configuration.                               |


---

## 📜 Authorship & Acknowledgments

- **Original Author**: [Ange Maurice](https://github.com/AngeAM)
- **AI-Assisted Improvements**: This code was refined with the help of **Le Chat (Mistral AI)**, including:
  - Adding **logging** and **comments**.
  - Improving **error handling**.
  - Structuring the code for better readability and maintainability.

> ⚠️ **Disclaimer**:  
> This code was enhanced with AI assistance (Le Chat by Mistral AI). The AI suggested structural improvements, but the original logic and functionality were written by Ange Maurice. Users are responsible for validating the correctness and suitability of this code for their use case. No warranty or liability is provided.

---

## 🤝 Contributing

Contributions are welcome! Feel free to open an **issue** or submit a **pull request** for improvements.
