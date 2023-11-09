# bn-scout

> This is not intended for public use. Feel free to fork if you find it useful (I don't expect you will) and modify to suit your needs.

This is a simple python script to fetch jobs from Bright Network graduate technology jobs and go through them in the CLI to save time. It saves you all the extra clicks and the hassle of opening millions of tabs you would have to go through all of the jobs.

## Setting up

To set up the script, you need to follow these steps:

1. Make sure you have Python installed on your system. If you don't, you can download it from the [official Python website](https://www.python.org/downloads/).

2. Clone the repository or download the script files to your local machine.

```bash
git clone https://github.com/your-repository/bn-scout.git

cd bn-scout
```

3. Install the required dependencies using `pip`. It is recommended to use a virtual environment, but this is not necessary.

```bash
pip install -r requirements.txt
```

4. Fetch the jobs from Bright Network by running fetch-jobs.py

```bash
python fetch-jobs.py
```

The jobs and their descriptions are put in a file named bright-network-jobs.json. You can change this file name in the fetch-jobs.py file.

5. Now you can go through the jobs in the CLI by running process-jobs.py

```bash
python process-jobs.py
```

Follow the on-screen instructions to navigate through the job listings. Press `Y` to accept a job, `N` to reject it, `O` to save it for later (useful for when you're not sure about a job) and `CTRL + C` to exit the script.

```bash
git pull origin main
```

## TODO

- [ ] Add a way to interactively configure jobs index page URL
