# A Walk In The Park

## Concept

This is a super easy OSINT challenge which is meant to be solved very quickly by participants. 

## Solution

- First, use `exiftool` to get instagram handle `the_real_lee_kx`

- From the Instagram Stories, deduce that the person has a strava account too with same name (https://www.strava.com/athletes/170347344) 

- Find the route matching the timestamp, and use google street view along the route to get the answer.

- The flag is `grey{interim_park_upper_serangoon_road}`