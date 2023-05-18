# VOTER VALIDATION
*Description :* To get details related to [VOTER]("https://electoralsearch.in/#!#resultArea") website.


> ## POST login
```
http://10.10.4.62:5005/eci
```

> ### **Body (json):**
```json
{
    "epic" : "Z********2",
    "state" : "Andhra Pradesh",
    "txnid" : 1234
}
```
| Key           | Description            |
| --------------| ---------------------- |
| epic          | voter id number        |
| state         | 'Karnataka', 'Maharashtra', 'Meghalaya', 'Nagaland', 'Tripura', 'Uttar Pradesh', 'West Bengal','Lakshadweep', 'Jammu and Kashmir', 'Ladakh', 'Andaman & Nicobar Islands', 'Andhra Pradesh', 'Arunachal Pradesh','Assam', 'Bihar', 'Chandigarh', 'Chattisgarh', 'Dadra & Nagar Haveli and Daman & Diu', 'Goa', 'Gujarat', 'Haryana', 'Himachal Pradesh', 'Jharkhand','Kerala','Madhya Pradesh','Manipur','Mizoram','NCT OF Delhi','Odisha','Puducherry','Punjab', 'Rajasthan', 'Sikkim', 'Tamil Nadu', 'Telangana', 'Uttarakhand'|
| txnid         | transaction ID         |


> ### **Response (json):**

**Case 1:**
*HTTP STATUS CODE: 200*

```json
{
    "data": {
        "age": "29",
        "assembly_constituency": "Kurnool",
        "dist": "Kurnool",
        "epic_number": "Z********2",
        "name": "S ********* -\nయస్ ముజమ్మిల్ అహ్మద్",
        "parlimentary_constituency": "Kurnoolu",
        "polling_station": "Everest **************************************** Station",
        "relative_name": "S ******* AHMED -\nయస్ మక్బుల్ అహ్మద్",
        "state": "Andhra Pradesh"
    },
    "respcode": 200,
    "respdesc": "Success"
}
```
&nbsp;
**Case 2 :**
*HTTP STATUS CODE : 400*
```json
 {
    "data": null,
    "respcode": 400,
    "respdesc": "Bad request"
 }
```
**Case 3 :**
*HTTP STATUS CODE : 402*
```json
{
    "data": null,
    "respcode": 402,
    "respdesc": "Invalid voter_id"
}
```

## Response Codes 

| Response Code      | Description                                             |
| ------------------ | ------------------------------------------------------- |
| 200                | Success                                                 |
| 400                | Empty Request Body                                      |
| 401                | Invalid Headers                                         |
| 402                | Invalid Voter Number                                    |
| 403                | Invalid Request                                         |
| 500                | Internal Error                                          |
| 502                | Details Fetching Failed                                 |
| 503                | Derails Not Found                                       |
| 504                | Connetion Error                                         |


