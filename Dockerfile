FROM python:2-onbuild
ENV LANG en_US.UTF-8
CMD ["python", "./src/weather_sparkline_bot.py"]
