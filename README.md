# python-stock-viewer
A Client-Server application for analyzing and visualizing historical stock market data.
The project demonstrates a decoupling of data processing (Backend) and data visualization (Frontend).

* ## Features:
* **Client-Server Architecture:** Separation of concerns between the API provider and the visualization client.
* **REST API:** Built with **Flask**, serving processed financial data in JSON format.
* **Data Analysis:** Utilizes **Pandas** and **NumPy** for calculating 52-week High/Low and ROI.
* **Visualization:** Interactive candlestick charts using **Matplotlib**.
* **Dynamic Fetching:** Retrieves real-time/historical data using `pandas-datareader`.

## Installation
* Clone the project repository or download the source code
* Install dependencies:
pip install -r requirements.txt

* ## Usage
* Since this is a client-server application, you need to run the server first.
Start the server from server.py. The server will run on http://127.0.0.1:5000
* Run the client from client.py.
* Follow on screen instructions.

* ## Examples
<img width="522" height="246" alt="Screenshot 2025-11-12 224838" src="https://github.com/user-attachments/assets/a576b4ac-b85c-428c-a87e-132a73dab09a" />
<img width="2560" height="1327" alt="Stock_Viewer1" src="https://github.com/user-attachments/assets/f5377781-92ab-478b-af5c-5a65ea4c0924" />
<img width="2560" height="1327" alt="Stock_Viewer3" src="https://github.com/user-attachments/assets/a434de49-c2d4-4578-8690-64a898139ea4" />
<img width="2560" height="1327" alt="Stock_Viewer2" src="https://github.com/user-attachments/assets/593018ba-7144-43f4-9613-e55b2f68fcb1" />
<img width="639" height="459" alt="Screenshot 2025-11-12 224500" src="https://github.com/user-attachments/assets/f2c5c6a3-04ab-48b3-9fb7-7dbd294c8b50" />
