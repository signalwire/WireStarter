# Send and track Faxes with the Signalwire Fax API using Sinatra and Ruby

This is an example application that you can use to send and track faxes using the [Signalwire Fax API](https://developer.signalwire.com/compatibility-api/rest/entities/faxes).


## Running the app
You'll need the following to run the app:

* [Ruby](https://www.ruby-lang.org/en/downloads/)
* [Bundler](https://bundler.io/) for installing dependencies

Then clone the application:

```bash
git clone git@github.com:signalwire/WireStarter.git
cd examples/fax-ruby-sinatra/
```

Install the dependencies:

```bash
bundle install
```

Execute setup.sh to configure create and congfigure 'config/env.yml

Note: When setup asks for `BASE_URL` setup Fill it with  your ngrok URL or your server domain/ip with port ex: https://example.com:3000 or http://123.x.x.x:3000 .
```bash
bash setup.sh
```

Start the application:

```bash
rackup config.ru -p 3000 -b 0.0.0.0
```

Open [localhost:3000](http://localhost:3000) and start sending faxes!

