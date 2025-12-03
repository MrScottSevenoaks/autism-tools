🧩 Autism Tools

A web application built with Python and Flask, dedicated to creating practical, accessible, and user-friendly tools to support autistic individuals, their families, and educators. This project aims to offer simple, effective digital resources that address common daily challenges.

This repository was initially generated from a Codespaces Flask template.

✨ Project Goals (Vision)

The long-term goal for this platform is to provide a collection of specialized tools, such as:

Visual Schedule Generator: A dynamic, easy-to-use tool for creating and displaying daily or weekly visual schedules.

Sensory Regulation Tracker: A simple logging system for identifying sensory triggers, calming strategies, and patterns.

Communication Aids: Basic digital boards or phrase builders for non-verbal or low-verbal communication support.

💻 Technology Stack

This application is built using a minimal, scalable web stack:

Backend: Python 3.x with Flask

Frontend: HTML5, CSS (Tailwind/Custom), and Vanilla JavaScript

Database: (Planned) SQLite for local development, potentially PostgreSQL/Firestore for production.

🚀 Getting Started

Follow these steps to set up and run the application locally.

Prerequisites

You need Python 3.8+ installed on your system.

1. Clone the Repository

git clone [https://github.com/MrScottSevenoaks/autism-tools.git](https://github.com/MrScottSevenoaks/autism-tools.git)
cd autism-tools


2. Set up the Python Environment

It is highly recommended to use a virtual environment.

# Create a virtual environment
python -m venv venv

# Activate the virtual environment
# On macOS/Linux:
source venv/bin/activate
# On Windows (Command Prompt):
venv\Scripts\activate


3. Install Dependencies

Install the necessary Python packages listed in requirements.txt:

pip install -r requirements.txt


4. Run the Application

Start the Flask application. Using the --debug flag is recommended for development as it enables automatic reloading on code changes.

flask --debug run


The application will typically be accessible at http://127.0.0.1:5000/.

🤝 Contribution

This project is open to contributions from developers, designers, educators, and community members with relevant experience or interest. Whether it's feature development, UI/UX design, or documentation, all contributions are welcome!

Fork the repository.

Create your feature branch (git checkout -b feature/AmazingFeature).

Commit your changes (git commit -m 'Add some AmazingFeature').

Push to the branch (git push origin feature/AmazingFeature).

Open a Pull Request.