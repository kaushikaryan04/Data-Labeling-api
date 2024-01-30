from django.db import models

class Statement(models.Model) :
    text = models.CharField(max_length = 1000)

    def save(self , *args ,**kwargs) :

        existing_statements = Statement.objects.filter(text = self.text).first()
        if not existing_statements :
            super().save(*args , **kwargs)

    def __str__(self) -> str:
        return self.text

class Tag(models.Model) :
    choices = [
        ("NEG" , "NEG"),
        ("POS","POS"),
        ("NEU","NEU")
    ]
    statement = models.ForeignKey('Statement' ,on_delete = models.CASCADE )
    aspect = models.CharField(max_length = 20)
    sentiment = models.CharField(choices = choices , max_length = 3)
    def save(self, *args, **kwargs):

        existing_tag = Tag.objects.filter(
            statement=self.statement,
            aspect=self.aspect,
            sentiment=self.sentiment
        ).first()
        if not existing_tag:
            super().save(*args, **kwargs)
            
    def __str__(self) :
        return f"Tag For Statement {self.statement.text}"
    