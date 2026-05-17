# JOB LISTING TRACKER SYSTEM (JTS)

## A. Contributor
**Isaac Igohe**

## B. Overview
The Job Listing Tracker System (JTS) is a sophisticated desktop-based application designed to streamline the job search process for tech professionals. By aggregating real-time listings from multiple global job boards, JTS provides a centralized hub where users can discover, track, and manage their career opportunities with ease.

## C. Installation
Follow these steps to set up and run the project locally:

### 1. Clone the Repository
```bash
git clone https://github.com/IsaacIgohe/jts_project.git
cd jts_project
```

### 2. Install Dependencies
Ensure you have Python 3.10 or later installed. Run the following command to install the required libraries:
```bash
pip install pymongo bcrypt requests beautifulsoup4 mongomock
```

### 3. Run the Application
```bash
python main.py
```

## D. Usage
1. **Launch the App**: Run the `main.py` file. You will be greeted by a secure login window. If you are a new user, navigate to the registration tab to create an account.
2. **Browse Tech Jobs**: Upon logging in, the main dashboard displays a curated list of tech opportunities.
3. **Fetch Real-Time Data**: Click the **"Refresh Jobs"** button to trigger the multi-source scrapers and update the database with the latest listings.
4. **Search & Filter**: Use the integrated search bar to quickly find jobs by title, company, or specific keywords.
5. **Manage Applications**: Double-click any job to view full details. You can save jobs to your personal list, update their application status (e.g., "Applied"), or remove them once they are no longer relevant.

## E. Features
### Personalized User Dashboard
JTS offers a secure, authenticated experience where each user maintains their own private list of saved jobs and application statuses.

### Multi-Source Web Scraping
The system features a robust scraping engine that concurrently fetches data from top tech job boards including **RemoteOK, Remotive, Dice, Fuzu, and NoDesk**, ensuring a wide variety of opportunities.

### Modern GUI Architecture
Built with Python's **Tkinter**, the interface utilizes a professional "SaaS-style" layout with a dedicated navigation sidebar, clean typography, and a responsive data table for an optimal user experience.

### Persistent NoSQL Storage
Leverages **MongoDB Atlas** for cloud-based data persistence. The system manages three core collections: `users` (securely hashed credentials), `jobs` (aggregated listings), and `saved_jobs` (user-specific tracking).

### Intelligent Data Cleaning
Includes an automated HTML-stripping pipeline that cleans raw job descriptions from various websites, presenting them in a clean, readable format within the application.

## F. Tech Stack

| Layer | Technology |
| :--- | :--- |
| **Environment** | Python 3.10+ |
| **GUI Framework** | Tkinter / ttk |
| **Database** | MongoDB Atlas (NoSQL) |
| **Authentication** | Bcrypt (Password Hashing) |
| **Scraping** | BeautifulSoup4 / Requests |
| **Data Handling** | PyMongo |
