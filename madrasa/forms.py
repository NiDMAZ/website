from django import forms

madrasa_classes = (
    ('Brothers:A','Brothers:A'),
    ('Brothers:B','Brothers:B'),
    ('Sisters:A','Sisters:A'),
    ('Sisters:B','Sisters:B'),
    ('Sisters:C','Sisters:C'),
)

class StudentIdsForm(forms.Form):
    student_ids = forms.CharField(label="Student ID", max_length=64)

class ClassSelectionForm(forms.Form):
    madrasa_class = forms.ChoiceField(choices=madrasa_classes, initial='Brothers:A', label='Class Name')