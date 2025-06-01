# By the banana tree

## Concept

This challenge uses osint research to interpret mile markers (assuming no prior knowledge), and geolocation skills like working with online map (particularly in the absense of comprehensive street view).

Or you can just use ChatGPT. 🥹

## Solution

Doing a preliminary reverse image search on google, one can identity the country: Vietnam

One can notice the mile marker in the foreground. The text on the marker is roughly readable.
- Blue top: ĐT 317   Km (?) 12
- Main face: QL.32   12 Km
- Side face: ĐT 317

![mile marker](images/milemarker.png)


Doing some research, one can find out that both QL32 and ĐT317 are valid road identifiers, but which is the relevant one? Provincial roads (tỉnh lộ or đường tỉnh, TL or ĐT) have white milestones with blue or green tops [1], so the current road must be 'more closely related' to ĐT317.

Looking up google maps, ĐT317 is lacking street view, except a short stretch closer to the city, so one should try to narrow the search area a bit more.

Mile markers (or more accurately Kilometer posts, cột kilômét) is placed on the right-hand side in the direction from the starting point (road origin) to the end point of the road, at an even distance of 1,000m [2].

Inferring that QL32 is the road origin, one can identify the rough location that the photo was taken by measuring the distance starting from where QL32 and ĐT317 intersect.

![12 km from QL32 via ĐT317](images/12_km.png)

From the image, the photo seems to be taken beside a pond or a flooded paddy field, and is much closer to hills/mountains. It seems like the above location is not quite right, but using a nearby (aerial) photo sphere, we can see some paddy fields and mountains in the distance.

![Photo sphere 1](images/photo_sphere_1.png)

Using a photo sphere closer to those paddy fields and mountains, one can notice a white church-like structure by zooming in.

![church in the distance](images/church_in_distance.png)

One can confirm that there is indeed a church at that location.

![church on map](images/church_on_map.png)

Comparing the images of the church with the provided photo, one can see the similarities, confirming that this church is the one captured in the photo (Name of church: Nhà Thờ Thanh Lâm).

![Nhà Thờ Thanh Lâm](images/nha_tho_thanh_lam.png)
![church in photo](images/church_in_photo.png)

Zooming into the provided photo, one can see that two buildings with black and green roof (respectively) are standing between the POV and the church (in purple & red boxes). A house (in yellow box) can also be seen much closer to the POV, across what seems to be a road (in blue box).

![key features (buildings) in photo](images/buildings_in_photo.png)

The black roof (in purple box) is almost colinear with the church (in white box) and POV, while the green roof (in red box) is off to the right. From this, one can determine the POV's direction relative to the church's location.

![buildings on map shows relative direction](images/buildings_on_map.png)

Though not very obvious, one might see the zebra crossing just behind the banana trees, which matches up with the zebra crossing at the first junction we encounter using the relative direction above. The roof of the house in the foreground also seems to match the roof on the map.

![other features](images/other_features.png)

Using the coordinates to the junction, and the name of the church, the flag is therefore `grey{N21-153_E105-274_nhathothanhlam}`.

## References

[1] [Driving in Vietnam](https://en.wikivoyage.org/wiki/Driving_in_Vietnam)  
[2] [National Technical Regulation on Traffic Signs and Signals of Vietnam](https://upload.wikimedia.org/wikipedia/commons/8/81/2019_standardisation_of_National_Technical_Regulation_on_Traffic_Signs_and_Signals_of_Vietnam.pdf)
