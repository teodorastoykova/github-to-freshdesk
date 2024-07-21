
# GitHub to Freshdesk Integration

This project is a simple application that integrates GitHub with Freshdesk. It fetches user information from GitHub and creates a corresponding contact in Freshdesk. Additionally, it stores the user information in a MariaDB database.

## 🚀 Features

- Fetch user information from GitHub.
- Create a contact in Freshdesk with the fetched information.
- Records user information in a database.


## 🛠️ Requirements

- Python 3.6+
- GitHub Personal Access Token
- Freshdesk API Key and password
- MariaDB server

## 🌎 Environment Variables

To run this project, you will need to add the following environment variables to your .env file

`GITHUB_TOKEN`

`FRESHDESK_TOKEN`

`FRESHDESK_PASSWORD`

`DB_HOST`

`DB_USER`

`DB_PASSWORD`

`DB_PORT`


## ⚙️ Installation

1. Clone the Repository

```bash
git clone https://github.com/teodorastoykova/github-to-freshdesk.git
cd yourproject
```

2. Install Required Packages

Install the required Python packages using pip:

```bash
pip install -r requirements.txt
```

3. Set Up the Database

To create the database and the necessary tables, you can use the provided SQL script (database.sql) to set up the database schema via a MariaDB client or MySQL Workbench. 

Alternatively you can also use the command line to run the script:

```bash
mariadb -u <username> -p < <path-to-database.sql>
```
4. Set Up Environment Variables

Create a .env file in the root directory of the project and add the following environment variables:

```bash
GITHUB_TOKEN=your_github_token
FRESHDESK_TOKEN=your_freshdesk_api_key
FRESHDESK_PASSWORD=your_freshdesk_password
DB_HOST=your_db_host
DB_USER=your_db_user
DB_PASSWORD=your_db_password
DB_PORT=your_db_port
```

Replace your_github_token, your_freshdesk_api_key, your_freshdesk_password, your_db_host, your_db_user, your_db_password, your_db_port with your actual credentials.

5. Run the Application

You can run the application using the following command:

```bash
python main.py <github_username> <freshdesk_subdomain>
```
Replace <github_username> with the GitHub username of the user you want to fetch information for and <freshdesk_subdomain> with your Freshdesk subdomain.
    
## 💡 Usage/Examples

Running the program:

```bash
python3 main.py <github_username> <freshdesk_subdomain>
```

Example:

```bash
python3 main.py octocat domain
```

## 🧪 Running Tests

To run tests, run the following command

```bash
  python3 -m unittest discover -s tests
```

