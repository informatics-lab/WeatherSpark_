# Weather Sparkline
A twitter bot that tells the weather with unicode symbols

## With thanks to:
* Weather data from the MetOffice Datapoint API
* [Molly White and her blog on twitter bots](http://blog.mollywhite.net/twitter-bots-pt2/)
* graphical web 2016 for inspiration.


## Running
[Get a Datapoint key]((http://register.metoffice.gov.uk/register/datapoint),
Get a twitter token and secret and a pair of access token and secret. See [Molly White's blog](http://blog.mollywhite.net/twitter-bots-pt2/) for help.
Set up these as environment variables (mine are called `DATAPOINT_KEY`, `WEATHERSPARK_C_TOKEN`, `WEATHERSPARK_C_SECRET`, `WEATHERSPARK_A_SECRET` and `WEATHERSPARK_A_SECRET`)
get docker and then...

Build:
```
docker build . -t weather_sparkline_bot
```

and run:
```
docker run \
 -e DATAPOINT_KEY=$DATAPOINT_KEY\
 -e TWITTER_C_TOKEN=$WEATHERSPARK_C_TOKEN\
 -e TWITTER_C_SECRET=$WEATHERSPARK_C_SECRET\
 -e TWITTER_A_TOKEN=$WEATHERSPARK_A_TOKEN\
 -e TWITTER_A_SECRET=$WEATHERSPARK_A_SECRET\
 -t weather_sparkline_bot
```
