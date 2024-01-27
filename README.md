# Django🐍 Scrapy🕷️ PostgreSQL🐘

The project involves basic skills in navigating through the Django and Scrapy frameworks. The project is a replica of the [quotes.toscrape.com](https://quotes.toscrape.com) website. The project scrapes information about authors, quotes, and a list of tags, and sends them to a PostgreSQL database. The Django-based website, modeled after the original, allows user registration and password reset by sending a unique token to the email provided during registration. Upon logging in, users can add quotes, authors, and tags. It is also possible to edit and delete entire quotes. The website features a sorting form based on the most frequently used tags.
## Roadmap 📚

- [Prerequisites 🛠️](#prerequisites)
- [Installation ⬇️](#installation)
- [Configuration ⚙️](#configuration)
- [Usage 🚀](#usage)
- [Created 👤](#created)
- [License 📄](#license)

## Prerequisites 🛠️

Make sure you have the following installed on your machine:

- Python 3.11: You can download and install Python 3.11 from the official [Python website](https://www.python.org/).
- Docker: Install Docker by following the instructions on the [Docker website](https://www.docker.com/get-started).

## Installation ⬇️

1.Clone the repository:

```bash
git clone https://github.com/sebastianLedzianowski/django.git  
```

2.Navigate to the Project Directory:

```bash
cd django
```

3.Set up a virtual environment and activate it (optional but recommended):

```bash
python -m venv venv
source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
```

4.Install dependencies using Poetry:

```bash
poetry install
```
## Configuration ⚙️

To run this project, you will need to add the following environment variables to your `.env` file.

```bash
#E-mail settings
EMAIL_HOST_USER=
EMAIL_HOST_PASSWORD=
```
---

**Note**: Ensure to keep your `.env` file secure and never commit it to the repository to protect sensitive information.

---
## Usage 🚀

1.Let's run a Docker container to create a PostgreSQL server using the following command:

```bash
docker run --name quotes-postgres -p 5432:5432 -e POSTGRES_PASSWORD=567234 -d postgres
```

2.Now, let's create a superuser, but first, we need to apply the initial migration:

```bash
python manage.py migrate

```

3.Then, execute the command:

```bash
python manage.py createsuperuser
```
---

Enter your username, email address, and password. If the password is too simple, an additional prompt will appear to confirm if you are sure; you can respond affirmatively.

---

4.Run the scraping files that will simultaneously import all the data into the PostgreSQL database:

```bash
scrapy crawl authors_spyder  
scrapy crawl quotes_spyder  
```

5.Run the development server to start the application:

```bash
python manage.py runserver
```

- To access the admin panel and register as an administrator, go to the following page: http://127.0.0.1:8000/admin

- Log in using the superuser credentials we created above

- You can also go to the home page: http://127.0.0.1:8000
 
- log in or register a new user there.
## Created 👤
- [Sebastian Ledzianowski](https://github.com/sebastianLedzianowski)


## License 📄

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.