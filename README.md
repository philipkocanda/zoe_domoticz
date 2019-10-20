# Obtain API Keys

Visit https://renault-wrd-prod-1-euw1-myrapp-one.s3-eu-west-1.amazonaws.com/configuration/iOS/config_nl_NL.json

- Set KAMEREON_API_KEY to `servers.wired.apiKey` in the next step
- Set GIGYA_API_KEY to `servers.gigya.apiKey` in the next step

# Install pyze

Make sure you have python3!

```
git clone git@github.com:jamesremuscat/pyze.git
cd pyze

python3 setup.py install

export GIGYA_API_KEY=XXXXXXXX
export KAMEREON_API_KEY=YYYYYYYY

pyze login  # You should only need to do this once
pyze status
```

For more on `pyze`, see https://muscatoxblog.blogspot.com/2019/07/delving-into-renaults-new-api.html

# Domoticz Updater

Install dependencies:

```
pip3 install fcache
```

- Copy `config.example.yml` to `config.yml`
- Create Domoticz devices (matching the types in `config.py`)
- Update device IDs in `config.yml` to match the devices you just created
- Run `update.py` periodically to push data to Domoticz

