# illich

Mataroa Collection list of blogs.

## Contributing

Feel free to open a PR on [GitHub](https://github.com/sirodoht/illich) or
send an email patch to [~sirodoht/public-inbox@lists.sr.ht](mailto:~sirodoht/public-inbox@lists.sr.ht).

On how to contribute using email patches see [git-send-email.io](https://git-send-email.io/).

## Development

This is a [Django](https://www.djangoproject.com/) codebase. Check out the
[Django docs](https://docs.djangoproject.com/) for general technical documentation.

### Structure

The Django project is `illich`. There is one Django app, `main`,  with all business logic.
Application CLI commands are generally divided into two categories, those under `python manage.py`
and those under `make`.

### Dependencies

Using [venv](https://docs.python.org/3/library/venv.html):

```sh
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
pip install -r requirements_dev.txt
```

This project also uses [pip-tools](https://github.com/jazzband/pip-tools) for dependency
management.

### Environment variables

A file named `.envrc` is used to define the environment variables required for this project to
function. One can either export it directly or use [direnv](https://github.com/direnv/direnv).
There is an example environment file one can copy as base:

```sh
cp .envrc.example .envrc
```

`.envrc` should contain the following variables:

```sh
export SECRET_KEY=some-secret-key
export DATABASE_URL=postgres://illich:db-password@db:5432/illich
export EMAIL_HOST_USER=smtp-user
export EMAIL_HOST_PASSWORD=smtp-password
```

When on production, also include the following variables (see [Deployment](#Deployment) and
[Backup](#Backup)):

```sh
export NODEBUG=1
export PGPASSWORD=db-password
```

### Database

This project uses PostgreSQL. Assuming one has set the `DATABASE_URL` (see above), to create the
database schema:

```sh
python manage.py migrate
```

### Serve

To run the Django development server:

```sh
python manage.py runserver
```

### Docker

If Docker and docker-compose are preferred, then:

1. Set `DATABASE_URL` in `.envrc` to `postgres://postgres:postgres@db:5432/postgres`
1. Run `docker-compose up -d`.

The database data will be saved in the git-ignored directory / Docker volume `db_data`,
located in the root of the project.

## Testing

Using the Django test runner:

```sh
python manage.py test
```

For coverage, run:

```sh
make cov
```

## Code linting & formatting

The following tools are used for code linting and formatting:

* [black](https://github.com/psf/black) for code formatting.
* [isort](https://github.com/pycqa/isort) for imports order consistency.
* [flake8](https://gitlab.com/pycqa/flake8) for code linting.

To use:

```sh
make format
make lint
```

## Deployment

Deployment is configured using [uWSGI](https://uwsgi.readthedocs.io/en/latest/)
and [nginx](https://nginx.org/).

Remember to set the environment variables before starting `uwsgi`. Depending on the deployment
environment, this could mean directly exporting the variables or just sourcing `.envrc` (with all
production variables — including `NODEBUG`):

```sh
source .envrc
uwsgi illich.ini
```

Note that the value of the `NODEBUG` variable is ignored. What matters is merely its existence
in the environment.

## Backup

To automate backup, there is [a script](backup-database.sh) which dumps the database and uploads
it into AWS S3. The script also needs the database password as an environment variable. The
key needs to be `PGPASSWORD`. The backup script assumes the variable lives in `.envrc` like so:

```sh
export PGPASSWORD=db-password
```

To restore a dump:

```sh
pg_restore -v -h localhost -cO --if-exists -d illich -U illich -W illich.dump
```

To add on cron:

```sh
0 */6 * * * /opt/apps/illich/backup-database.sh
```

## License

This software is licensed under the MIT license.
For more information, read the [LICENSE](LICENSE) file.
