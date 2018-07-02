from fabric.contrib.files import append, exists, sed
from fabric.api import env, local, run, sudo
import random

REPO_URL = 'https://github.com/cam-barts/ObeyTheTestingGoat'

def deploy():
    site_folder = f'/home/{env.user}/sites/{env.host}'
    source_folder = site_folder + '/source'
    _create_directory_structure_if_necessary(site_folder)
    _get_latest_source(source_folder)
    _download_required_options()
    _update_settings(source_folder, env.host)
    _update_virtualenv(source_folder)
    _update_static_files(source_folder)
    _update_database(source_folder)
    _sed_conf_templates(source_folder)
    _start_all_services()

def latest():
    site_folder = f'/home/{env.user}/sites/{env.host}'
    source_folder = site_folder + '/source'
    _get_latest_source(source_folder)
    _update_settings(source_folder, env.host)
    _update_virtualenv(source_folder)
    _update_static_files(source_folder)
    _update_database(source_folder)

def _create_directory_structure_if_necessary(site_folder):
    for subfolder in ('database', 'static', 'virtualenv', 'source'):
        run(f'mkdir -p {site_folder}/{subfolder}')

def _get_latest_source(source_folder):
    if exists(source_folder + '/.git'):
        run(f'cd {source_folder} && git fetch')
    else:
        run(f'git clone {REPO_URL} {source_folder}')
    current_commit = local("git log -n 1 --format=%H", capture=True)
    run(f'cd {source_folder} && git reset --hard {current_commit}')

def _download_required_options():
    sudo('add-apt-repository ppa:fkrull/deadsnakes -y')
    sudo('apt-get update -y')
    sudo('apt-get install nginx git python3.6 python3.6-venv -y')

def _update_settings(source_folder, site_name):
    settings_path = source_folder + '/superlists/settings.py'
    sed(settings_path, "DEBUG = True", "DEBUG = False")
    sed(settings_path,
        'ALLOWED_HOSTS = .+$',
        f'ALLOWED_HOSTS = ["{site_name}"]'
    )
    secret_key_file = source_folder +'/superlists/secret_key.py'
    if not exists(secret_key_file):
        chars = 'qwertyuiopasdfghjklzxcvbnm1234567890!@#$%^&*()_-=+'
        key = ''.join(random.SystemRandom().choice(chars) for _ in range(50))
        append(secret_key_file, f'SECRET_KEY = "{key}"')
    append(settings_path, '\nfrom .secret_key import SECRET_KEY')

def _update_virtualenv(source_folder):
    virtualenv_folder = source_folder + '/../virtualenv'
    if not exists(virtualenv_folder + '/bin/pip'):
        run(f'python3.6 -m venv {virtualenv_folder}')
    run(f'{virtualenv_folder}/bin/pip install -r {source_folder}/requirements.txt')

def _update_static_files(source_folder):
    run(
        f'cd {source_folder} && ../virtualenv/bin/python manage.py collectstatic --noinput'
    )

def _update_database(source_folder):
    run(f'cd {source_folder} && rm -rf  ../database/db.sqlite3')
    # run(f'cd {source_folder} && rm -rf lists/migrations/* ')
    run(f'cd {source_folder} && ../virtualenv/bin/python3.6 manage.py makemigrations')
    run(
        f'cd {source_folder} && ../virtualenv/bin/python3.6 manage.py migrate --noinput'
    )

def _sed_conf_templates(source_folder):
    nginx_path = source_folder + '/deploy-tools/nginx.template.conf'
    gunicorn_path = source_folder + '/deploy-tools/gunicorn-systemd.template.service'
    sudo(f'cd {source_folder} && sed "s/SITENAME/{env.host}/g" {nginx_path} | sudo tee /etc/nginx/sites-available/{env.host}')
    # run(f'sudo ln -s /etc/nginx/sites-available/{env.host} /etc/nginx/sites-enabled/{env.host}')
    sudo(f'cd {source_folder} && sed "s/SITENAME/{env.host}/g" {gunicorn_path} | sudo tee /etc/systemd/system/gunicorn-{env.host}')

def _start_all_services():
    sudo('systemctl daemon-reload')
    sudo('systemctl reload nginx')
    sudo(f'systemctl enable gunicorn-{env.host}')
    sudo(f'systemctl start gunicorn-{env.host}')
    sudo(f'service gunicorn-{env.host}.service restart')
