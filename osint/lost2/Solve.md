Check the government website for databases to get the full set of data (since you can't just input one airport): https://www.transtats.bts.gov/DataIndex.asp

![databases](https://github.com/user-attachments/assets/f8adfa41-9adb-4c35-a86a-095474a764e4)

![tables](https://github.com/user-attachments/assets/141ed982-ed6a-4d86-9d75-a0bc06f06b51)

Eventually make your way here: https://www.transtats.bts.gov/DL_SelectFields.aspx?gnoyr_VQ=FGK&QO_fu146_anzr=b0-gvzr
![transportation stats](https://github.com/user-attachments/assets/500e7ac1-8e08-420d-9b75-9f71d2d2511d)

Need to select the following:
```
IATA_Code_Marketing_Airline	
Flight_Number_Marketing_Airline

OriginCityName
DestCityName

DepDelay 
WeatherDelay
```

The first two are to get the flight number for the flag, the city names are so we can confirm they are close to each other (from the message saying he could have driven back and forth several times), the departure delay to confirm it's around 26 hours late, and weather delay to confirm the delay is due to weather.

Open in excel or other editor and sort `WeatherDelay`:
![excel](https://github.com/user-attachments/assets/fe1324ca-fdcd-4748-9266-d0400c10b4d9)

Confirmation:
![confirmation](https://github.com/user-attachments/assets/17f1ad20-90a4-4111-9fd9-780200e88995)
