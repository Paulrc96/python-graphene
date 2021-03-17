from django import forms

class TestForm(forms.Form):
    firstUsers = forms.IntegerField(label='Usuarios', required=True, initial=1)
    serverType = forms.CharField(label='Servidor', initial='PYTHON')
    caseId = forms.CharField(label='Caso', initial='case1')

class TestMutationForm(forms.Form):
    clientsTotal = forms.IntegerField(label='Clientes a crear', required=True, initial=1)
    serverType = forms.CharField(label='Servidor', initial='PYTHON')
