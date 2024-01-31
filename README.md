## To setup locally 
First git clone the repo 
Make a virtual environment 
```
virtualenv env
```
Activate this env (mac command)
```
source env/bin/activate
```
Download packages required 
```
pip install -r requirements.txt
```
Now migrate
```
python manage.py makemigrations
python manage.py migrate
```
Run server
```
python manage.py runserver
```
## Testing 
Use postman for easier testing  
Base endpoint -> http://127.0.0.1:8000/api  

File upload -> POST /fileupload ( Attach the file in body)  
header for file upload -> Content-Disposition : attachment; filename="myfile.xlsx"  

Tag statements -> POST /tagstatement (Attach tags in JSON format in body)
example ->  
```
{
    "data": [
        {
            "statement" : "The rooms were bad but staff was friendly.",
            "aspect" : "room",
            "sentiment" : "NEG"
        },{
            "statement" : "It is hot but scenery is good .",
            "aspect" : "weather",
            "sentiment" : "NEG"
        },
        {
            "statement" : "It is hot but scenery is good .",
            "aspect":"scenery",
            "sentiment":"POS"
        }
        
    ],
    "filename" : "myfile.xlsx"
}
```
Download Tagged File -> GET /downloadfile (give original file name in request param)  
Get all aspcets for a statement -> GET /getaspects (give statement in request param)  








## Considerations 
Serializers   
All thought it is considered good practice to use serializers everywhere I used minimum serializers (Only one) as I wanted more control over everything and most of them would just be extra steps to achieve the same thing.  
Cacheing   
Most of this api is doing writting into file rather than sending results to the client. So not a lot of cacheing is used but I have used it in when the client wants to get all the aspects for a particular statement as the project stated to use cacheing.  
