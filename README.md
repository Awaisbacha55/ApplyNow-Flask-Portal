# ApplyNow — Professional Job Application Portal

ApplyNow is a premium, professional recruitment platform designed to demonstrate modern web development practices. This project specifically fulfills the requirements of **Task 2: Form Handling and POST Requests**.

## 🌟 Project Overview
This application demonstrates how to properly build a web form using HTML5, handle HTTP POST requests securely with Python Flask, perform robust server-side data validation, store data safely in SQLite, and utilize the Post/Redirect/Get pattern to ensure a seamless user experience.

## ✨ Features
- **Premium User Interface:** Clean, modern SaaS-like design using Plus Jakarta Sans and Lucide icons.
- **Secure Form Handling:** Implementation of CSRF protection to prevent cross-site request forgery.
- **Post/Redirect/Get (PRG) Pattern:** Prevents duplicate form submissions upon browser refreshes.
- **Robust Validation:** Dual-layer validation (Client-side HTML5/JS + Server-side Python).
- **SQLite Database Integration:** Automatic database creation and safe parameterized SQL queries.
- **Dynamic Character Counter:** Live JavaScript counter for the cover letter field.
- **Dedicated Success Page:** Displays a unique application reference securely retrieved from the database.

## 🛠️ Technologies Used
- **Backend:** Python 3, Flask, Flask-WTF, SQLite3
- **Frontend:** HTML5, Vanilla CSS3, Vanilla JavaScript, Jinja2
- **Testing:** Python `unittest`

---

## 🚀 Setup Instructions

### 1. Prerequisites
Ensure you have Python 3.8+ installed on your system.

### 2. Set Up a Virtual Environment

**Windows (PowerShell):**
```powershell
python -m venv venv
.\venv\Scripts\activate
```

**macOS / Linux:**
```bash
python3 -m venv venv
source venv/bin/activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Configure Environment Variables
Copy the example environment file and set your secure secret key:
- Copy `.env.example` to a new file named `.env`

### 5. Run the Application
The SQLite database (`database/applynow.db`) will be initialized automatically when the app starts.
```bash
python app.py
```

### 6. Access the Application
Open your web browser and navigate to:
👉 **[http://127.0.0.1:5000](http://127.0.0.1:5000)**

---

## 🧪 Running Automated Tests
The project includes a robust test suite using a temporary SQLite database.
```bash
python -m unittest test_app.py
```

---

## 📚 Academic Concepts Demonstrated

### Browser Form → HTTP POST → Flask Route → Validation → Database → Redirect → Success Page

1. **GET Request (`/`)**: Renders the empty application form.
2. **POST Request (`/apply`)**: The browser packages the form data into the HTTP request body and sends it to the server.
3. **Server-Side Validation**: Python checks the data (length, email format, dropdown enums).
4. **SQLite Persistence**: If valid, the data is saved using parameterized SQL (preventing SQL injection).
5. **HTTP Redirect (302)**: The server immediately redirects the browser to a new URL.
6. **Success Page (`/application-success/<ref>`)**: A final GET request renders the success screen.

### GET vs. POST HTTP Methods
- **GET Method:** Requests data from a specified resource. Data is appended to the URL (e.g., `?name=John`). It is completely insecure for forms handling personal data because it is visible in the URL, browser history, and logs.
- **POST Method:** Submits data to be processed to a specified resource. Data is enclosed in the body of the HTTP request. This is the mandatory standard for forms handling sensitive data, applications, and authentication.

### The Post/Redirect/Get (PRG) Pattern
If a user refreshes a page after a standard POST request, the browser often asks, *"Confirm Form Resubmission?"* which can lead to duplicate database entries. The PRG pattern solves this: after the POST request is successfully processed, the server replies with a `302 Redirect` instead of HTML. The browser then makes a fresh GET request to the new URL (the success page), meaning refreshing the page will only reload the success message, not resubmit the data.
